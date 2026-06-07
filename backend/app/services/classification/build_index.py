"""Run once to precompute EU Taxonomy category embeddings.

Usage:
    python -m backend.app.services.classification.build_index
"""
from __future__ import annotations

from pathlib import Path


TAXONOMY_DIR = Path("backend/data/taxonomy")
VECTORSTORE_DIR = Path("backend/data/vectorstore")


def build_index() -> None:
    # TODO: load .txt files from TAXONOMY_DIR, embed them, save
    #       taxonomy_index.npy and categories.json to VECTORSTORE_DIR
    pass


if __name__ == "__main__":
    build_index()
