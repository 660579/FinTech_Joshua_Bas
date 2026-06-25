"""
Stub service responses shaped exactly like backend.app.models.schemas (ESGProfile,
Passport) and the real output of services/scoring/scorer.py and
services/passport/assembler.py. Used as a fallback when the live backend
(frontend/services/client.py) is unreachable, so the UI can still render.
"""

from __future__ import annotations


def mock_invoice() -> dict:
    return {
        "invoice_id": "INV-2024-0042",
        "sme_id": "sme-001",
        "date": "2024-03-15",
        "currency": "EUR",
        "line_items": [
            {"supplier": "EcoSupply GmbH", "description": "Solar panel installation", "quantity": 10, "amount": 12000.00},
            {"supplier": "LightTech BV", "description": "LED lighting retrofit", "quantity": 50, "amount": 3500.00},
            {"supplier": "PowerRent GmbH", "description": "Diesel generator rental", "quantity": 1, "amount": 850.00},
        ],
    }


def mock_esg_profile() -> dict:
    return {
        "sme_id": "sme-001",
        "procurement_sustainability_score": 64.0,
        "green_credit_score": 71.0,
        "dimension_scores": {
            "Climate Change Mitigation": 0.58,
            "Climate Change Adaptation": 0.0,
            "Water & Marine Resources": 0.0,
            "Circular Economy": 0.06,
            "Pollution Prevention & Control": 0.0,
            "Biodiversity & Ecosystems": 0.0,
        },
        "classified_line_items": [
            {
                "supplier": "EcoSupply GmbH",
                "description": "Solar panel installation",
                "quantity": 10,
                "unit": None,
                "amount": 12000.00,
                "taxonomy_category": "Solar energy generation",
                "taxonomy_objective": "Climate Change Mitigation",
                "similarity_score": 0.91,
                "rationale": "Installation of solar panels directly enables renewable energy generation, aligned with EU Taxonomy climate change mitigation objective.",
            },
            {
                "supplier": "LightTech BV",
                "description": "LED lighting retrofit",
                "quantity": 50,
                "unit": None,
                "amount": 3500.00,
                "taxonomy_category": "Energy efficiency in buildings",
                "taxonomy_objective": "Climate Change Mitigation",
                "similarity_score": 0.83,
                "rationale": "LED retrofit reduces building energy consumption, qualifying under EU Taxonomy energy efficiency activities.",
            },
            {
                "supplier": "PowerRent GmbH",
                "description": "Diesel generator rental",
                "quantity": 1,
                "unit": None,
                "amount": 850.00,
                "taxonomy_category": None,
                "taxonomy_objective": None,
                "similarity_score": 0.21,
                "rationale": "Diesel generator use does not align with any EU Taxonomy sustainable activity.",
            },
        ],
        "sector_benchmark": {
            "sector": "C25",
            "median_green_credit_score": 15.0,
        },
        "data_quality": {
            "confidence_pct": 42.0,
            "tier": "Low",
            "basis": "Based on 3 classified invoice line items (demo mock data)",
        },
    }


def mock_passport() -> dict:
    return {
        "passport_id": "GP-A1B2-C3D4",
        "sme_id": "sme-001",
        "company_name": "Müller & Partners GmbH",
        "esg_profile": mock_esg_profile(),
        "financial_health": {
            "total_spend_eur": 16_350.00,
            "classified_green_spend_eur": 15_500.00,
            "green_spend_share": 0.9480,
        },
        "requested_amount_eur": 50_000.00,
        "created_at": "2024-03-15T14:30:00Z",
        "shared": False,
    }
