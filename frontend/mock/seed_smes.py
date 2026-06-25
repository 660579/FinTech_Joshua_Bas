"""
DEMO SEED DATA: entirely fictional SMEs for the Lender View comparison roster.

None of this comes from Bas's real classification/scoring pipeline. It exists so a
lender has more than one company to compare (the whole point of Change 1: showing
network effects). Every entry is shaped EXACTLY like a real backend.app.models.schemas.Passport
(same nesting as frontend/mock/__init__.py's mock_passport()), so the rendering code
in components/esg_display.py treats them identically to a real passport.

Passport IDs are deliberately non-UUID-looking ("DEMO-SME-...") so they're obviously
demo fixtures rather than real backend-issued IDs.
"""
from __future__ import annotations

_DIMENSION_KEYS = [
    "Climate Change Mitigation",
    "Climate Change Adaptation",
    "Water & Marine Resources",
    "Circular Economy",
    "Pollution Prevention & Control",
    "Biodiversity & Ecosystems",
]


def _dimensions(**overrides: float) -> dict:
    base = {k: 0.0 for k in _DIMENSION_KEYS}
    base.update(overrides)
    return base


def _passport(
    *,
    passport_id: str,
    sme_id: str,
    company_name: str,
    sector: str,
    green_credit_score: float,
    procurement_sustainability_score: float,
    median_green_credit_score: float,
    dimension_scores: dict,
    classified_line_items: list[dict],
    total_spend_eur: float,
    classified_green_spend_eur: float,
    requested_amount_eur: float,
    quality_tier: str,
    quality_confidence_pct: float,
    quality_basis: str,
    created_at: str,
) -> dict:
    return {
        "passport_id": passport_id,
        "sme_id": sme_id,
        "company_name": company_name,
        "esg_profile": {
            "sme_id": sme_id,
            "procurement_sustainability_score": procurement_sustainability_score,
            "green_credit_score": green_credit_score,
            "dimension_scores": dimension_scores,
            "classified_line_items": classified_line_items,
            "sector_benchmark": {
                "sector": sector,
                "median_green_credit_score": median_green_credit_score,
            },
            "data_quality": {
                "confidence_pct": quality_confidence_pct,
                "tier": quality_tier,
                "basis": quality_basis,
            },
        },
        "financial_health": {
            "total_spend_eur": total_spend_eur,
            "classified_green_spend_eur": classified_green_spend_eur,
            "green_spend_share": round(classified_green_spend_eur / total_spend_eur, 4),
        },
        "requested_amount_eur": requested_amount_eur,
        "created_at": created_at,
        "shared": True,
    }


SEED_SME_PASSPORTS: list[dict] = [
    _passport(
        passport_id="DEMO-SME-CONSTRUCTION-01",
        sme_id="demo-sme-helios-construction",
        company_name="Helios Construction NV",
        sector="Construction",
        green_credit_score=82.0,
        procurement_sustainability_score=76.0,
        median_green_credit_score=22.0,
        dimension_scores=_dimensions(**{
            "Climate Change Mitigation": 0.61,
            "Circular Economy": 0.22,
            "Pollution Prevention & Control": 0.08,
        }),
        classified_line_items=[
            {"supplier": "SolarBuild Materials NV", "description": "Solar roofing membrane installation, 1200 m²", "quantity": 1200, "unit": "m2", "amount": 84000.0, "taxonomy_category": "Renovation of Existing Buildings", "taxonomy_objective": "Climate Change Mitigation", "similarity_score": 0.88, "rationale": "Demo data: solar roofing aligns with energy-efficient building renovation."},
            {"supplier": "Recycled Concrete Solutions BV", "description": "Recycled aggregate concrete, 80 tonnes", "quantity": 80, "unit": "tonne", "amount": 19500.0, "taxonomy_category": "Recycled Metals & Materials Manufacturing", "taxonomy_objective": "Circular Economy", "similarity_score": 0.74, "rationale": "Demo data: recycled aggregate supports circular construction material use."},
            {"supplier": "Crane & Plant Hire Benelux", "description": "Diesel crane rental, 2 weeks", "quantity": 2, "unit": "week", "amount": 4200.0, "taxonomy_category": None, "taxonomy_objective": None, "similarity_score": 0.18, "rationale": "Demo data: diesel plant hire does not qualify under any EU Taxonomy activity."},
        ],
        total_spend_eur=210_000.0,
        classified_green_spend_eur=165_000.0,
        requested_amount_eur=250_000.0,
        quality_tier="High",
        quality_confidence_pct=93.0,
        quality_basis="Demo data, based on 28 classified invoice line items across 14 months",
        created_at="2025-11-02T09:10:00Z",
    ),
    _passport(
        passport_id="DEMO-SME-LOGISTICS-01",
        sme_id="demo-sme-nordwind-logistics",
        company_name="Nordwind Logistics GmbH",
        sector="Logistics & Freight",
        green_credit_score=58.0,
        procurement_sustainability_score=49.0,
        median_green_credit_score=35.0,
        dimension_scores=_dimensions(**{
            "Climate Change Mitigation": 0.34,
            "Pollution Prevention & Control": 0.05,
        }),
        classified_line_items=[
            {"supplier": "EVBox Charging Solutions", "description": "Electric van fleet charging hub, 6 points", "quantity": 6, "unit": "unit", "amount": 21000.0, "taxonomy_category": "Infrastructure for Electric Mobility", "taxonomy_objective": "Climate Change Mitigation", "similarity_score": 0.71, "rationale": "Demo data: EV charging infrastructure for the delivery fleet."},
            {"supplier": "Diesel Depot Hamburg", "description": "Diesel fuel for long-haul trucks, 5000 L", "quantity": 5000, "unit": "L", "amount": 7800.0, "taxonomy_category": None, "taxonomy_objective": None, "similarity_score": 0.15, "rationale": "Demo data: diesel fuel does not qualify under the EU Taxonomy."},
            {"supplier": "Warehouse LED Retrofit BV", "description": "LED lighting retrofit, distribution hub", "quantity": 1, "unit": "installation", "amount": 9600.0, "taxonomy_category": "Energy-Efficient Lighting", "taxonomy_objective": "Climate Change Mitigation", "similarity_score": 0.62, "rationale": "Demo data: LED retrofit reduces warehouse energy consumption."},
        ],
        total_spend_eur=95_000.0,
        classified_green_spend_eur=38_000.0,
        requested_amount_eur=80_000.0,
        quality_tier="Medium",
        quality_confidence_pct=67.0,
        quality_basis="Demo data, based on 12 classified invoice line items across 6 months",
        created_at="2026-01-18T14:05:00Z",
    ),
    _passport(
        passport_id="DEMO-SME-HOSPITALITY-01",
        sme_id="demo-sme-sole-mio-bakeries",
        company_name="Sole Mio Bakeries SARL",
        sector="Food & Hospitality",
        green_credit_score=34.0,
        procurement_sustainability_score=28.0,
        median_green_credit_score=20.0,
        dimension_scores=_dimensions(**{
            "Climate Change Mitigation": 0.12,
            "Circular Economy": 0.04,
        }),
        classified_line_items=[
            {"supplier": "Local Organic Flour Co-op", "description": "Organic flour, 200 kg", "quantity": 200, "unit": "kg", "amount": 1100.0, "taxonomy_category": None, "taxonomy_objective": None, "similarity_score": 0.27, "rationale": "Demo data: organic sourcing alone doesn't meet the similarity threshold for a taxonomy match."},
            {"supplier": "EcoPack Compostable Supplies", "description": "Compostable packaging, 5000 units", "quantity": 5000, "unit": "unit", "amount": 1450.0, "taxonomy_category": "Recycled Metals & Materials Manufacturing", "taxonomy_objective": "Circular Economy", "similarity_score": 0.41, "rationale": "Demo data: compostable packaging supports circular material use."},
            {"supplier": "City Gas Utility", "description": "Natural gas for ovens, monthly", "quantity": 1, "unit": "month", "amount": 980.0, "taxonomy_category": None, "taxonomy_objective": None, "similarity_score": 0.10, "rationale": "Demo data: natural gas heating does not qualify under the EU Taxonomy."},
        ],
        total_spend_eur=22_000.0,
        classified_green_spend_eur=4_500.0,
        requested_amount_eur=15_000.0,
        quality_tier="Low",
        quality_confidence_pct=38.0,
        quality_basis="Demo data, based on 3 classified invoice line items across 1 month (recently onboarded)",
        created_at="2026-05-30T11:40:00Z",
    ),
    _passport(
        passport_id="DEMO-SME-TEXTILES-01",
        sme_id="demo-sme-vertex-textiles",
        company_name="Vertex Textiles SA",
        sector="Textile Manufacturing",
        green_credit_score=45.0,
        procurement_sustainability_score=40.0,
        median_green_credit_score=30.0,
        dimension_scores=_dimensions(**{
            "Climate Change Mitigation": 0.21,
            "Water & Marine Resources": 0.09,
            "Pollution Prevention & Control": 0.03,
        }),
        classified_line_items=[
            {"supplier": "AquaTreat Industrial Systems", "description": "Wastewater treatment system upgrade, dye house", "quantity": 1, "unit": "installation", "amount": 26500.0, "taxonomy_category": "Water Treatment and Industrial Wastewater Management", "taxonomy_objective": "Water & Marine Resources", "similarity_score": 0.69, "rationale": "Demo data: wastewater treatment reduces dye-house water pollution."},
            {"supplier": "Recycled Polyester Yarn BV", "description": "Recycled polyester yarn, 3000 kg", "quantity": 3000, "unit": "kg", "amount": 18200.0, "taxonomy_category": "Recycled Metals & Materials Manufacturing", "taxonomy_objective": "Circular Economy", "similarity_score": 0.58, "rationale": "Demo data: recycled yarn supports circular textile production."},
            {"supplier": "Coal Boiler Services Ltd", "description": "Coal-fired boiler annual maintenance", "quantity": 1, "unit": "service", "amount": 3100.0, "taxonomy_category": None, "taxonomy_objective": None, "similarity_score": 0.12, "rationale": "Demo data: coal-fired heating does not qualify under the EU Taxonomy."},
        ],
        total_spend_eur=130_000.0,
        classified_green_spend_eur=41_000.0,
        requested_amount_eur=100_000.0,
        quality_tier="Medium",
        quality_confidence_pct=63.0,
        quality_basis="Demo data, based on 9 classified invoice line items across 5 months",
        created_at="2026-03-09T16:25:00Z",
    ),
    _passport(
        passport_id="DEMO-SME-AGRICULTURE-01",
        sme_id="demo-sme-agroterra-farms",
        company_name="AgroTerra Farms BV",
        sector="Agriculture",
        green_credit_score=71.0,
        procurement_sustainability_score=65.0,
        median_green_credit_score=25.0,
        dimension_scores=_dimensions(**{
            "Climate Change Mitigation": 0.31,
            "Biodiversity & Ecosystems": 0.24,
            "Water & Marine Resources": 0.10,
        }),
        classified_line_items=[
            {"supplier": "Pentair Industrial Solutions BV", "description": "Drip irrigation system with rainwater harvesting, 12 ha", "quantity": 12, "unit": "ha", "amount": 38000.0, "taxonomy_category": "Rainwater Harvesting and Sustainable Water Management", "taxonomy_objective": "Water & Marine Resources", "similarity_score": 0.79, "rationale": "Demo data: drip irrigation with rainwater harvesting reduces water withdrawal."},
            {"supplier": "Hedgerow & Habitat Restoration Co", "description": "Native hedgerow planting for field margins, 4 km", "quantity": 4, "unit": "km", "amount": 9200.0, "taxonomy_category": "Biodiversity & Ecosystems Conservation", "taxonomy_objective": "Biodiversity & Ecosystems", "similarity_score": 0.66, "rationale": "Demo data: hedgerow restoration supports on-farm biodiversity."},
            {"supplier": "SolarTech NL BV", "description": "Solar-powered grain dryer installation", "quantity": 1, "unit": "installation", "amount": 27500.0, "taxonomy_category": "Solar Energy Generation", "taxonomy_objective": "Climate Change Mitigation", "similarity_score": 0.81, "rationale": "Demo data: solar-powered drying displaces fossil-fuel grain drying."},
        ],
        total_spend_eur=175_000.0,
        classified_green_spend_eur=120_000.0,
        requested_amount_eur=150_000.0,
        quality_tier="High",
        quality_confidence_pct=89.0,
        quality_basis="Demo data, based on 19 classified invoice line items across 11 months",
        created_at="2025-09-21T08:50:00Z",
    ),
]
