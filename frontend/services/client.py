"""HTTP adapter to the GreenLedger FastAPI backend.

Each function returns the same dict shape as the corresponding frontend/mock
function (frontend.mock.mock_esg_profile / mock_passport), or None if the
backend is unreachable or errors out. Callers fall back to mock data and
surface a warning rather than crashing. See frontend/PLAN.md's mock-first
build order, step 5.
"""
from __future__ import annotations

import os

import requests

API_BASE_URL = os.environ.get("GREENLEDGER_API_URL", "http://localhost:8000")

_SCAN_TIMEOUT = 60  # embedding + per-line-item RAG calls can take a while
_DEFAULT_TIMEOUT = 10


class BackendUnavailable(Exception):
    """Raised when the GreenLedger backend cannot be reached at all (vs. answering with an error)."""


def _default_data_quality(esg_profile: dict) -> dict:
    """Derive a sensible data_quality default when the backend doesn't supply one.

    Bas's scorer doesn't compute this. We approximate "how much data the score is
    based on" from the number of successfully classified line items returned by /sme/scan.
    """
    n = len(esg_profile.get("classified_line_items") or [])
    if n >= 15:
        tier, confidence = "High", min(95.0, 70.0 + n)
    elif n >= 5:
        tier, confidence = "Medium", 55.0 + n * 2.0
    else:
        tier, confidence = "Low", 30.0 + n * 4.0
    return {
        "confidence_pct": round(min(confidence, 95.0), 1),
        "tier": tier,
        "basis": f"Based on {n} classified invoice line item{'s' if n != 1 else ''} from this scan",
    }


def _ensure_data_quality(esg_profile: dict) -> dict:
    if not esg_profile.get("data_quality"):
        esg_profile["data_quality"] = _default_data_quality(esg_profile)
    return esg_profile


def scan_invoices(file_bytes: bytes, filename: str) -> dict | None:
    """POST /sme/scan: parse, classify, and score an uploaded invoice file. Returns an ESGProfile dict, or None on any failure."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/sme/scan",
            files={"file": (filename, file_bytes)},
            timeout=_SCAN_TIMEOUT,
        )
        response.raise_for_status()
        return _ensure_data_quality(response.json())
    except requests.RequestException:
        return None


def create_passport(esg_profile: dict, requested_amount_eur: float | None = None) -> str | None:
    """POST /sme/passport: assemble and store a Financing Passport. Returns its passport_id, or None on any failure."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/sme/passport",
            json={"esg_profile": esg_profile, "requested_amount_eur": requested_amount_eur},
            timeout=_DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()["passport_id"]
    except requests.RequestException:
        return None


def get_passport(passport_id: str) -> dict | None:
    """GET /lender/passport/{id}: retrieve a previously shared Financing Passport.

    Returns the Passport dict, or None if no passport exists for that ID.
    Raises BackendUnavailable if the backend can't be reached at all, so callers
    can distinguish "wrong ID" (show an error) from "backend is down" (fall back to mock).
    """
    try:
        response = requests.get(
            f"{API_BASE_URL}/lender/passport/{passport_id}",
            timeout=_DEFAULT_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise BackendUnavailable(str(exc)) from exc

    if response.status_code == 404:
        return None
    response.raise_for_status()
    passport = response.json()
    if passport.get("esg_profile"):
        passport["esg_profile"] = _ensure_data_quality(passport["esg_profile"])
    return passport


def record_decision(
    passport_id: str,
    decision: str,
    indicative_rate: float | None = None,
    approved_amount_eur: float | None = None,
    notes: str | None = None,
) -> dict | None:
    """POST /lender/decision: record a lender's approve/decline decision. Returns the confirmation dict, or None on any failure."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/lender/decision",
            json={
                "passport_id": passport_id,
                "decision": decision,
                "indicative_rate": indicative_rate,
                "approved_amount_eur": approved_amount_eur,
                "notes": notes,
            },
            timeout=_DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
