from __future__ import annotations

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
    RAG is called only for items that clear the similarity threshold —
    unclassified items are returned with taxonomy fields left as None.
    """
    if not line_items:
        return []

    index, categories = _get_index()

    descriptions = [item.description for item in line_items]
    embeddings = embed_texts(descriptions)  # (N, D) normalised

    results: list[ClassifiedLineItem] = []
    for item, embedding in zip(line_items, embeddings):
        matches = cosine_match(embedding, index, categories, top_k=1)

        if matches:
            match = matches[0]
            rationale = build_rationale(
                line_item_description=item.description,
                taxonomy_category=match["name"],
                category_definition=match["definition"],
            )
            results.append(
                ClassifiedLineItem(
                    **item.model_dump(),
                    taxonomy_category=match["name"],
                    taxonomy_objective=match["objective"],
                    similarity_score=match["similarity_score"],
                    rationale=rationale,
                )
            )
        else:
            results.append(ClassifiedLineItem(**item.model_dump()))

    return results
