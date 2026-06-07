from __future__ import annotations

from pathlib import Path

from backend.app.models.schemas import Passport

REPORTS_DIR = Path("backend/data/reports")


def export_vsme_report(passport: Passport) -> Path:
    # TODO: serialise Passport into a VSME-structured JSON file,
    #       save to REPORTS_DIR/<passport_id>.json, return the path
    pass
