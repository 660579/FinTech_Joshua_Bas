from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from backend.app.models.schemas import Passport

REPORTS_DIR = Path("backend/data/reports")


def export_vsme(passport: Passport) -> dict:
    classified_spend = sum(
        item.amount for item in passport.esg_profile.classified_line_items
    )
    alignment_score = passport.esg_profile.procurement_sustainability_score / 100.0
    classified_weighted_spend = sum(
        item.amount * (item.similarity_score or 0.0)
        for item in passport.esg_profile.classified_line_items
    )
    # Mirror the scorer's formula to recover total_spend from the alignment ratio.
    total_spend = (
        classified_weighted_spend / alignment_score
        if alignment_score > 0
        else classified_spend
    )
    coverage_ratio = classified_spend / total_spend if total_spend > 0 else 0.0

    report: dict = {
        "sme_id": passport.sme_id,
        "passport_id": passport.passport_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "green_credit_score": passport.esg_profile.green_credit_score,
        "esg_profile": passport.esg_profile.model_dump(),
        "vsme_indicators": {
            "coverage_ratio": round(coverage_ratio, 4),
            "alignment_score": round(alignment_score, 4),
            "classified_spend": round(classified_spend, 2),
            "total_spend": round(total_spend, 2),
        },
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"{passport.passport_id}.json"
    report_path.write_text(json.dumps(report, indent=2))

    return report
