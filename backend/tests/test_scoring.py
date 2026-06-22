from __future__ import annotations

import pytest

from backend.app.models.schemas import ClassifiedLineItem
from backend.app.services.scoring.scorer import (
    EU_TAXONOMY_OBJECTIVES,
    build_esg_profile,
    compute_green_credit_score,
    score_dimensions,
)


def _classified(
    description: str,
    amount: float,
    objective: str | None = None,
    similarity: float | None = None,
) -> ClassifiedLineItem:
    return ClassifiedLineItem(
        supplier="Test Supplier",
        description=description,
        quantity=1.0,
        amount=amount,
        taxonomy_objective=objective,
        taxonomy_category=objective,
        similarity_score=similarity,
    )


# --- score_dimensions ---

def test_dimension_scores_keys_match_objectives() -> None:
    items = [_classified("solar panels", 1000.0, "Climate Change Mitigation", 0.9)]
    scores = score_dimensions(items)
    assert set(scores.keys()) == set(EU_TAXONOMY_OBJECTIVES)


def test_dimension_scores_all_zero_for_no_spend() -> None:
    scores = score_dimensions([])
    assert all(v == 0.0 for v in scores.values())


def test_dimension_scores_unclassified_item_dilutes_score() -> None:
    """Diesel (unclassified) must reduce the green score, not be ignored."""
    items = [
        _classified("solar panel installation", 3000.0, "Climate Change Mitigation", 0.85),
        _classified("diesel fuel 500L", 5000.0, objective=None, similarity=None),
        _classified("LED lighting retrofit", 2000.0, "Climate Change Mitigation", 0.71),
    ]
    scores = score_dimensions(items)
    mitigation_score = scores["Climate Change Mitigation"]

    # Green weighted spend = 3000*0.85 + 2000*0.71 = 2550 + 1420 = 3970
    # Total spend = 10000
    # Expected = 3970 / 10000 * 100 = 39.7
    assert abs(mitigation_score - 39.7) < 0.1


def test_dimension_scores_fully_green_below_100() -> None:
    """Even 100% classified spend won't hit 100 because similarity < 1.0 scales it down."""
    items = [_classified("solar panels", 1000.0, "Climate Change Mitigation", 0.9)]
    scores = score_dimensions(items)
    assert scores["Climate Change Mitigation"] == 90.0


# --- compute_green_credit_score ---

def test_green_credit_score_range() -> None:
    items = [
        _classified("solar panel installation", 3000.0, "Climate Change Mitigation", 0.85),
        _classified("diesel fuel 500L", 5000.0),
        _classified("LED lighting retrofit", 2000.0, "Circular Economy", 0.71),
    ]
    scores = score_dimensions(items)
    gcs = compute_green_credit_score(scores, sector="F")
    assert 0.0 <= gcs <= 100.0


def test_green_credit_score_zero_for_empty() -> None:
    scores = {obj: 0.0 for obj in EU_TAXONOMY_OBJECTIVES}
    assert compute_green_credit_score(scores, sector="C") == 0.0


# --- build_esg_profile ---

def test_build_esg_profile_known_sector_includes_benchmark() -> None:
    items = [_classified("solar panels", 1000.0, "Climate Change Mitigation", 0.9)]
    profile = build_esg_profile(sme_id="sme-1", classified_items=items, sector="F")
    assert profile.sector_benchmark is not None
    assert profile.sector_benchmark.sector == "F"


def test_build_esg_profile_unknown_sector_no_benchmark() -> None:
    items = [_classified("solar panels", 1000.0, "Climate Change Mitigation", 0.9)]
    profile = build_esg_profile(sme_id="sme-1", classified_items=items, sector="UNKNOWN")
    assert profile.sector_benchmark is None


def test_build_esg_profile_procurement_score_uses_total_spend() -> None:
    """procurement_sustainability_score must reflect total spend, not just classified spend."""
    items = [
        _classified("solar panels", 5000.0, "Climate Change Mitigation", 1.0),
        _classified("diesel fuel", 5000.0),  # unclassified
    ]
    profile = build_esg_profile(sme_id="sme-1", classified_items=items, sector="C")
    # green_weighted_spend = 5000 * 1.0 = 5000; total = 10000 → 50.0
    assert profile.procurement_sustainability_score == 50.0
