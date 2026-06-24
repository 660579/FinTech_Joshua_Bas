from __future__ import annotations

from backend.app.models.schemas import ClassifiedLineItem, LineItem
from backend.app.services.scoring.scorer import SECTOR_BENCHMARK, score


def _line_item(description: str, amount: float) -> LineItem:
    return LineItem(supplier="Test Supplier", description=description, quantity=1.0, amount=amount)


def _classified(description: str, amount: float, objective: str, similarity: float) -> ClassifiedLineItem:
    return ClassifiedLineItem(
        supplier="Test Supplier",
        description=description,
        quantity=1.0,
        amount=amount,
        taxonomy_category=objective,
        taxonomy_objective=objective,
        similarity_score=similarity,
    )


def test_all_classified_high_similarity_score_near_100() -> None:
    """When all spend is classified at high confidence the GCS should approach 100."""
    all_items = [
        _line_item("solar panel installation", 500.0),
        _line_item("LED lighting retrofit", 500.0),
    ]
    classified_items = [
        _classified("solar panel installation", 500.0, "Climate Change Mitigation", 0.95),
        _classified("LED lighting retrofit", 500.0, "Climate Change Mitigation", 0.95),
    ]
    # coverage=1.0, alignment=0.95, sector_position=min(1, 0.95/0.15)=1.0
    # GCS = (0.20*1.0 + 0.50*0.95 + 0.30*1.0) * 100 = 97.5
    profile = score(all_items, classified_items, sme_id="sme-1", sector="C25")
    assert profile.green_credit_score > 90.0


def test_no_classified_items_score_near_zero() -> None:
    """When nothing clears the similarity threshold the GCS must be zero."""
    all_items = [
        _line_item("diesel fuel 500L", 800.0),
        _line_item("conventional steel beams", 200.0),
    ]
    # coverage=0, alignment=0, sector_position=0 → GCS=0.0
    profile = score(all_items, classified_items=[], sme_id="sme-2", sector="C25")
    assert profile.green_credit_score == 0.0
    assert profile.procurement_sustainability_score == 0.0


def test_mixed_spend_score_in_middle_range() -> None:
    """Partial green spend with moderate similarity should land in the middle of the scale."""
    all_items = [
        _line_item("solar panel installation", 500.0),
        _line_item("diesel fuel 500L", 1000.0),
        _line_item("conventional packaging", 500.0),
    ]
    classified_items = [
        _classified("solar panel installation", 500.0, "Climate Change Mitigation", 0.60),
    ]
    # total_spend=2000, coverage=500/2000=0.25, alignment=300/2000=0.15
    # sector_position=min(1, 0.15/0.15)=1.0
    # GCS = (0.20*0.25 + 0.50*0.15 + 0.30*1.0) * 100 = 42.5
    profile = score(all_items, classified_items, sme_id="sme-3", sector="C25")
    assert 30.0 < profile.green_credit_score < 60.0
    assert abs(profile.green_credit_score - 42.5) < 0.1
