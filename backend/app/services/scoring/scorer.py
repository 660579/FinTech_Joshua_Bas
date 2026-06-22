from __future__ import annotations

from backend.app.models.schemas import ClassifiedLineItem, ESGProfile, SectorBenchmark

EU_TAXONOMY_OBJECTIVES = [
    "Climate Change Mitigation",
    "Climate Change Adaptation",
    "Water & Marine Resources",
    "Circular Economy",
    "Pollution Prevention & Control",
    "Biodiversity & Ecosystems",
]

# Weights reflect the relative importance of each objective in EU sustainable
# finance policy and their typical visibility in SME procurement data.
DIMENSION_WEIGHTS: dict[str, float] = {
    # Mitigation dominates EU green finance (SFDR, CSRD, EU Green Bond Standard)
    # and is the primary driver of lender GAR calculations.
    "Climate Change Mitigation": 0.40,
    # Circular economy is the most measurable procurement signal in invoice data:
    # waste handling, recycled materials, refurbishment services.
    "Circular Economy": 0.20,
    # Pollution prevention captures operational footprint directly visible in
    # invoices (treatment, abatement, hazardous-waste handling).
    "Pollution Prevention & Control": 0.15,
    "Water & Marine Resources": 0.10,
    "Biodiversity & Ecosystems": 0.10,
    # Adaptation investment is rarer in SME procurement than mitigation spend.
    "Climate Change Adaptation": 0.05,
}

# Median green credit scores per NACE sector code, used for benchmarking.
# WHY: relative performance matters to lenders — a score of 45 means different
# things in construction (above median) vs. utilities (below median).
# Source: approximated from EBA 2023 green asset ratio pilots and ESMA 2024
# sustainable finance data; update before demo if better data is available.
SECTOR_BENCHMARKS: dict[str, float] = {
    # F — Construction: moderate green procurement driven by EU Renovation Wave
    "F": 42.0,
    # C — Manufacturing: significant brown spend on energy and raw materials
    "C": 35.0,
    # G — Wholesale/Retail: lower green penetration, improving via supply-chain pressure
    "G": 28.0,
    # H — Transportation/Storage: heavily fossil-fuel dependent, transition underway
    "H": 22.0,
    # D — Electricity/Gas supply: highest green investment share in the real economy
    "D": 55.0,
}


def score_dimensions(classified_items: list[ClassifiedLineItem]) -> dict[str, float]:
    """Return weighted green spend per EU Taxonomy objective, normalised to 0–100.

    Denominator is total invoice spend (all items, classified or not) so that
    unclassified brown spend (e.g. diesel) correctly dilutes the score.
    Numerator uses amount × similarity_score to discount low-confidence matches.
    """
    total_spend = sum(item.amount for item in classified_items)
    if total_spend == 0:
        return {obj: 0.0 for obj in EU_TAXONOMY_OBJECTIVES}

    objective_weighted_spend: dict[str, float] = {obj: 0.0 for obj in EU_TAXONOMY_OBJECTIVES}
    for item in classified_items:
        if item.taxonomy_objective and item.similarity_score and item.taxonomy_objective in objective_weighted_spend:
            objective_weighted_spend[item.taxonomy_objective] += item.amount * item.similarity_score

    return {
        obj: round((objective_weighted_spend[obj] / total_spend) * 100, 2)
        for obj in EU_TAXONOMY_OBJECTIVES
    }


def compute_green_credit_score(dimension_scores: dict[str, float], sector: str) -> float:
    """Weighted aggregation of dimension scores into a 0–100 headline score."""
    raw = sum(
        dimension_scores.get(obj, 0.0) * weight
        for obj, weight in DIMENSION_WEIGHTS.items()
    )
    # Clamp to [0, 100]: dimension scores are on this scale but floating-point
    # arithmetic can nudge the weighted sum marginally outside bounds.
    return round(max(0.0, min(100.0, raw)), 2)


def build_esg_profile(
    sme_id: str,
    classified_items: list[ClassifiedLineItem],
    sector: str,
) -> ESGProfile:
    """Assemble an ESGProfile from classified line items.

    classified_items must contain ALL line items from the original invoices,
    not just those that matched a taxonomy category. Unmatched items have
    taxonomy_objective=None and contribute to the denominator (total spend)
    without inflating green scores.
    """
    dimension_scores = score_dimensions(classified_items)
    green_credit_score = compute_green_credit_score(dimension_scores, sector)

    total_spend = sum(item.amount for item in classified_items)
    green_weighted_spend = sum(
        item.amount * item.similarity_score
        for item in classified_items
        if item.taxonomy_objective and item.similarity_score
    )
    procurement_sustainability_score = round(
        (green_weighted_spend / total_spend * 100) if total_spend > 0 else 0.0,
        2,
    )

    benchmark_score = SECTOR_BENCHMARKS.get(sector)
    sector_benchmark = (
        SectorBenchmark(sector=sector, median_green_credit_score=benchmark_score)
        if benchmark_score is not None
        else None
    )

    return ESGProfile(
        sme_id=sme_id,
        procurement_sustainability_score=procurement_sustainability_score,
        green_credit_score=green_credit_score,
        dimension_scores=dimension_scores,
        classified_line_items=classified_items,
        sector_benchmark=sector_benchmark,
    )
