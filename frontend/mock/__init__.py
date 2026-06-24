"""
Stub service responses shaped like the backend schemas.
Replace these calls with real API calls once the backend endpoints are live.
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
        "procurement_sustainability_score": 0.64,
        "green_credit_score": 71.0,
        "dimension_scores": {
            "climate_mitigation": 0.72,
            "resource_efficiency": 0.58,
            "pollution_prevention": 0.40,
        },
        "classified_line_items": [
            {
                "supplier": "EcoSupply GmbH",
                "description": "Solar panel installation",
                "quantity": 10,
                "amount": 12000.00,
                "taxonomy_category": "Solar energy generation",
                "taxonomy_objective": "climate_change_mitigation",
                "similarity_score": 0.91,
                "rationale": "Installation of solar panels directly enables renewable energy generation, aligned with EU Taxonomy climate change mitigation objective.",
            },
            {
                "supplier": "LightTech BV",
                "description": "LED lighting retrofit",
                "quantity": 50,
                "amount": 3500.00,
                "taxonomy_category": "Energy efficiency in buildings",
                "taxonomy_objective": "climate_change_mitigation",
                "similarity_score": 0.83,
                "rationale": "LED retrofit reduces building energy consumption, qualifying under EU Taxonomy energy efficiency activities.",
            },
            {
                "supplier": "PowerRent GmbH",
                "description": "Diesel generator rental",
                "quantity": 1,
                "amount": 850.00,
                "taxonomy_category": None,
                "taxonomy_objective": None,
                "similarity_score": 0.21,
                "rationale": "Diesel generator use does not align with any EU Taxonomy sustainable activity.",
            },
        ],
        "sector_benchmark": {
            "sector": "Manufacturing",
            "median_green_credit_score": 55.0,
        },
    }


def mock_passport() -> dict:
    return {
        "passport_id": "GP-A1B2-C3D4",
        "sme_id": "sme-001",
        "company_name": "Müller & Partners GmbH",
        "esg_profile": mock_esg_profile(),
        "financial_health": {
            "revenue_eur": 4_200_000,
            "debt_ratio": 0.38,
            "payment_days": 32,
        },
        "created_at": "2024-03-15T14:30:00Z",
        "shared": False,
    }
