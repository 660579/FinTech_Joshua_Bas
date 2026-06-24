"""Lender-side API routes: retrieve a shared Financing Passport and record a lending decision."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.api.store import decision_store, passport_store
from backend.app.models.schemas import LenderDecision, Passport

router = APIRouter()


@router.get("/passport/{passport_id}", response_model=Passport)
async def get_passport(passport_id: str) -> Passport:
    passport = passport_store.get(passport_id)
    if passport is None:
        raise HTTPException(status_code=404, detail="Passport not found")
    return passport


@router.post("/decision")
async def record_decision(body: LenderDecision) -> dict:
    decision_store[body.passport_id] = body
    return {
        "status": "recorded",
        "passport_id": body.passport_id,
        "decision": body.decision,
    }
