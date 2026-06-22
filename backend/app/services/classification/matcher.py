from __future__ import annotations

import json
from pathlib import Path

import numpy as np

MIN_SIMILARITY_SCORE = 0.3


def load_index(vectorstore_dir: Path) -> tuple[np.ndarray, list[dict]]:
    """Load precomputed taxonomy embeddings and category metadata."""
    vectorstore_dir = Path(vectorstore_dir)
    index = np.load(vectorstore_dir / "taxonomy_index.npy")
    categories = json.loads((vectorstore_dir / "categories.json").read_text(encoding="utf-8"))
    return index, categories


def cosine_match(
    query_embedding: np.ndarray,
    index: np.ndarray,
    categories: list[dict],
    top_k: int = 1,
) -> list[dict]:
    """Return top_k category matches above the similarity threshold.

    Both query_embedding and index rows are pre-normalised (unit length), so the
    dot product equals cosine similarity — no explicit division needed.

    Returns an empty list when the best score is below MIN_SIMILARITY_SCORE,
    leaving the line item unclassified rather than forcing a weak match.
    """
    scores: np.ndarray = index @ query_embedding  # (N,)
    top_indices = np.argsort(scores)[::-1][:top_k]

    matches = []
    for idx in top_indices:
        score = float(scores[idx])
        if score < MIN_SIMILARITY_SCORE:
            break
        matches.append({**categories[idx], "similarity_score": score})

    return matches
