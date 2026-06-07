from __future__ import annotations

from backend.app.models.schemas import ClassifiedLineItem, ESGProfile

# Sector benchmark scores keyed by NACE sector code.
# WHY: benchmarking the SME against its sector lets lenders assess
#      relative green performance, not just absolute score.
SECTOR_BENCHMARKS: dict[str, float] = {
    # TODO: populate with defensible benchmark values before demo
}


def score_dimensions(classified_items: list[ClassifiedLineItem]) -> dict[str, float]:
    # TODO: aggregate items by EU Taxonomy objective, compute per-dimension score
    pass


def compute_green_credit_score(
    dimension_scores: dict[str, float],
    sector: str,
) -> float:
    # TODO: weighted aggregation of dimension scores → 0-100 headline score
    #       WHY for each weight must be commented when implemented
    pass


def build_esg_profile(
    sme_id: str,
    classified_items: list[ClassifiedLineItem],
    sector: str,
) -> ESGProfile:
    # TODO: compose dimension scores + green credit score into ESGProfile
    pass
