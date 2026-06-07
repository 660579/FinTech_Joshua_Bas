import pytest

from backend.app.models.schemas import LineItem
from backend.app.services.classification.classifier import classify_line_items


def test_classify_returns_classified_items() -> None:
    # TODO: mock embedder + matcher + rag, assert ClassifiedLineItem fields populated
    pass


def test_similarity_score_range() -> None:
    # TODO: assert similarity_score is in [0, 1]
    pass
