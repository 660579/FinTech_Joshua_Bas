from __future__ import annotations

from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path

import numpy as np

from backend.app.models.schemas import ClassifiedLineItem, LineItem
from backend.app.services.classification.embedder import embed_texts
from backend.app.services.classification.matcher import cosine_match, load_index
from backend.app.services.classification.rag import build_rationale

VECTORSTORE_DIR = Path("backend/data/vectorstore")

_index: np.ndarray | None = None
_categories: list[dict] | None = None


def _get_index() -> tuple[np.ndarray, list[dict]]:
    global _index, _categories
    if _index is None:
        _index, _categories = load_index(VECTORSTORE_DIR)
    return _index, _categories


def classify_line_items(line_items: list[LineItem]) -> list[ClassifiedLineItem]:
    """Orchestrate embed → match → RAG for a batch of line items.

    All descriptions are embedded in a single model call for efficiency.
    RAG calls are dispatched concurrently via ThreadPoolExecutor — only for
    items that clear the similarity threshold. Unclassified items are returned
    with taxonomy fields left as None.
    """
    if not line_items:
        return []

    index, categories = _get_index()

    embeddings = embed_texts([item.description for item in line_items])  # (N, D) normalised

    results: list[ClassifiedLineItem | None] = [None] * len(line_items)
    needs_rag: list[tuple[int, LineItem, dict]] = []

    for i, (item, embedding) in enumerate(zip(line_items, embeddings)):
        matches = cosine_match(embedding, index, categories, top_k=1)
        if matches:
            needs_rag.append((i, item, matches[0]))
        else:
            results[i] = ClassifiedLineItem(**item.model_dump())

    if needs_rag:
        with ThreadPoolExecutor(max_workers=8) as pool:
            pending: list[tuple[int, LineItem, dict, Future[str]]] = [
                (
                    i,
                    item,
                    match,
                    pool.submit(
                        build_rationale,
                        line_item_description=item.description,
                        taxonomy_category=match["name"],
                        category_definition=match["definition"],
                        qualifying_activities=match.get("qualifying", ""),
                    ),
                )
                for i, item, match in needs_rag
            ]
        for i, item, match, future in pending:
            results[i] = ClassifiedLineItem(
                **item.model_dump(),
                taxonomy_category=match["name"],
                taxonomy_objective=match["objective"],
                similarity_score=match["similarity_score"],
                rationale=future.result(),
            )

    return results  # type: ignore[return-value]  # all slots filled above
