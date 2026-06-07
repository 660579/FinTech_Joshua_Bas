from __future__ import annotations

from pathlib import Path

import numpy as np


def load_index(vectorstore_dir: Path) -> tuple[np.ndarray, list[dict]]:
    # TODO: load taxonomy_index.npy and categories.json
    pass


def cosine_match(
    query_embedding: np.ndarray,
    index: np.ndarray,
    categories: list[dict],
    top_k: int = 1,
) -> list[dict]:
    # TODO: compute cosine similarity, return top_k category matches with scores
    pass
