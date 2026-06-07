"""
Stub service responses shaped like the backend schemas.
Replace these calls with real API calls once the backend endpoints are live.
"""

from __future__ import annotations


def mock_invoice() -> dict:
    return {
        "invoice_id": "INV-2024-0042",
        "supplier": "EcoSupply GmbH",
        "date": "2024-03-15",
        "currency": "EUR",
        "line_items": [
            {"description": "Solar panel installation", "quantity": 10, "amount_eur": 12000.00},
            {"description": "LED lighting retrofit", "quantity": 50, "amount_eur": 3500.00},
            {"description": "Diesel generator rental", "quantity": 1, "amount_eur": 850.00},
        ],
    }


def mock_esg_profile() -> dict:
    return {
        "categories": [
            {"category": "Renewable energy", "amount_eur": 12000.00},
            {"category": "Energy efficiency", "amount_eur": 3500.00},
            {"category": "Fossil fuels", "amount_eur": 850.00},
        ],
        "dimensions": {
            "climate_mitigation": 0.72,
            "resource_efficiency": 0.58,
            "pollution_prevention": 0.40,
        },
        # Weighted average of dimension scores across classified spend.
        "procurement_sustainability_score": 0.64,
        # Headline score combining procurement sustainability + financial health.
        "green_credit_score": 71,
        "sector_benchmark": {
            "sector": "Manufacturing",
            "median_green_credit_score": 55,
        },
    }


def mock_passport() -> dict:
    return {
        "passport_id": "GP-A1B2-C3D4",
        "company_name": "Müller & Partners GmbH",
        # esg_profile already carries green_credit_score — not duplicated here.
        "esg_profile": mock_esg_profile(),
        "financial_health": {
            "revenue_eur": 4_200_000,
            "debt_ratio": 0.38,
            "payment_days": 32,
        },
        "created_at": "2024-03-15T14:30:00Z",
        "shared": False,
    }
