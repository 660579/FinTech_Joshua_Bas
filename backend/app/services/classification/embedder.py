from __future__ import annotations

import numpy as np

_model = None


def load_model(model_name: str = "all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(model_name)
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed texts and return L2-normalised (N, D) float32 array.

    Pre-normalising means dot product == cosine similarity — no division needed at match time.
    """
    model = load_model()
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings.astype(np.float32)
