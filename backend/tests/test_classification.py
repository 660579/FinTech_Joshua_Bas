from __future__ import annotations

from unittest.mock import patch

import numpy as np
import pytest

from backend.app.models.schemas import ClassifiedLineItem, LineItem
from backend.app.services.classification.classifier import classify_line_items

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FAKE_CATEGORY = {
    "name": "Solar Energy Generation",
    "objective": "Climate Change Mitigation",
    "nace_code": "D35.11",
    "definition": "Economic activities related to generation of electricity from solar.",
    "similarity_score": 0.85,
}

SOLAR_ITEM = LineItem(
    supplier="SolarCo",
    description="solar panel installation 10kW",
    quantity=1.0,
    amount=5000.0,
)

UNRELATED_ITEM = LineItem(
    supplier="OfficePlus",
    description="printer paper A4 500 sheets",
    quantity=10.0,
    amount=80.0,
)


def _fake_embed(texts: list[str]) -> np.ndarray:
    # Return deterministic unit vectors, shape (N, 4)
    n = len(texts)
    vecs = np.ones((n, 4), dtype=np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / norms


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_classify_matched_item_populates_all_fields() -> None:
    """Matched items must have taxonomy_category, objective, score, and rationale."""
    with (
        patch(
            "backend.app.services.classification.classifier.embed_texts",
            side_effect=_fake_embed,
        ),
        patch(
            "backend.app.services.classification.classifier.load_index",
            return_value=(np.ones((1, 4), dtype=np.float32), [FAKE_CATEGORY]),
        ),
        patch(
            "backend.app.services.classification.classifier.cosine_match",
            return_value=[FAKE_CATEGORY],
        ),
        patch(
            "backend.app.services.classification.classifier.build_rationale",
            return_value="This qualifies because it involves solar energy generation.",
        ),
    ):
        results = classify_line_items([SOLAR_ITEM])

    assert len(results) == 1
    item = results[0]
    assert isinstance(item, ClassifiedLineItem)
    assert item.taxonomy_category == "Solar Energy Generation"
    assert item.taxonomy_objective == "Climate Change Mitigation"
    assert item.rationale == "This qualifies because it involves solar energy generation."
    assert item.similarity_score == pytest.approx(0.85)


def test_classify_unmatched_item_leaves_taxonomy_fields_none() -> None:
    """Items below the similarity threshold must return None for all taxonomy fields."""
    with (
        patch(
            "backend.app.services.classification.classifier.embed_texts",
            side_effect=_fake_embed,
        ),
        patch(
            "backend.app.services.classification.classifier.load_index",
            return_value=(np.ones((1, 4), dtype=np.float32), [FAKE_CATEGORY]),
        ),
        patch(
            "backend.app.services.classification.classifier.cosine_match",
            return_value=[],  # below threshold, no match
        ),
        patch(
            "backend.app.services.classification.classifier.build_rationale",
        ) as mock_rag,
    ):
        results = classify_line_items([UNRELATED_ITEM])

    assert len(results) == 1
    item = results[0]
    assert item.taxonomy_category is None
    assert item.taxonomy_objective is None
    assert item.similarity_score is None
    assert item.rationale is None
    mock_rag.assert_not_called()  # RAG must not fire for unclassified items


def test_similarity_score_in_valid_range() -> None:
    """similarity_score must be in [0, 1] for matched items."""
    match_with_score = {**FAKE_CATEGORY, "similarity_score": 0.72}

    with (
        patch(
            "backend.app.services.classification.classifier.embed_texts",
            side_effect=_fake_embed,
        ),
        patch(
            "backend.app.services.classification.classifier.load_index",
            return_value=(np.ones((1, 4), dtype=np.float32), [FAKE_CATEGORY]),
        ),
        patch(
            "backend.app.services.classification.classifier.cosine_match",
            return_value=[match_with_score],
        ),
        patch(
            "backend.app.services.classification.classifier.build_rationale",
            return_value="Qualifies under EU Taxonomy.",
        ),
    ):
        results = classify_line_items([SOLAR_ITEM])

    score = results[0].similarity_score
    assert score is not None
    assert 0.0 <= score <= 1.0


def test_classify_empty_input_returns_empty_list() -> None:
    results = classify_line_items([])
    assert results == []


def test_classify_batch_preserves_order() -> None:
    """Output list must match input order."""
    items = [SOLAR_ITEM, UNRELATED_ITEM]

    def _sequential_match(embedding, index, categories, top_k=1):
        # first call matches, second does not
        _sequential_match.call_count = getattr(_sequential_match, "call_count", 0) + 1
        if _sequential_match.call_count == 1:
            return [FAKE_CATEGORY]
        return []

    with (
        patch(
            "backend.app.services.classification.classifier.embed_texts",
            side_effect=_fake_embed,
        ),
        patch(
            "backend.app.services.classification.classifier.load_index",
            return_value=(np.ones((1, 4), dtype=np.float32), [FAKE_CATEGORY]),
        ),
        patch(
            "backend.app.services.classification.classifier.cosine_match",
            side_effect=_sequential_match,
        ),
        patch(
            "backend.app.services.classification.classifier.build_rationale",
            return_value="Qualifies.",
        ),
    ):
        results = classify_line_items(items)

    assert len(results) == 2
    assert results[0].description == SOLAR_ITEM.description
    assert results[1].description == UNRELATED_ITEM.description
    assert results[0].taxonomy_category is not None
    assert results[1].taxonomy_category is None
