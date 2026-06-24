"""Financing Passport assembly: combines an ESGProfile with derived financial-health metrics."""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from backend.app.models.schemas import ESGProfile, Passport

# Module-local store used by get_passport() and the unit tests.
# The route layer (api/store.passport_store) holds the same passports for
# cross-request access via HTTP — both are populated on every assemble_passport() call.
_passport_store: dict[str, Passport] = {}


def assemble_passport(esg_profile: ESGProfile, sme_id: str) -> Passport:
    classified_spend = sum(item.amount for item in esg_profile.classified_line_items)

    # Invert the scorer's alignment formula to recover total_spend so we can express
    # financial health in absolute euros rather than ratios alone.
    alignment = esg_profile.procurement_sustainability_score / 100.0
    classified_weighted_spend = sum(
        item.amount * (item.similarity_score or 0.0)
        for item in esg_profile.classified_line_items
    )
    # total_spend = weighted_green_spend / alignment; fall back to classified_spend when alignment=0
    total_spend = (
        classified_weighted_spend / alignment if alignment > 0 else classified_spend
    )

    financial_health: dict[str, float] = {
        "total_spend_eur": round(total_spend, 2),
        "classified_green_spend_eur": round(classified_spend, 2),
        "green_spend_share": round(classified_spend / total_spend, 4) if total_spend > 0 else 0.0,
    }

    passport = Passport(
        passport_id=str(uuid.uuid4()),
        sme_id=sme_id,
        company_name=sme_id,  # frontend supplies the display name; sme_id is the stable key
        esg_profile=esg_profile,
        financial_health=financial_health,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    _passport_store[passport.passport_id] = passport
    return passport


def get_passport(passport_id: str) -> Passport | None:
    return _passport_store.get(passport_id)
