from fastapi import APIRouter

from backend.app.models.schemas import Passport, LenderDecision

router = APIRouter()


@router.get("/passport/{passport_id}", response_model=Passport)
async def get_passport(passport_id: str) -> Passport:
    # TODO: retrieve passport from in-memory store by passport_id
    pass


@router.post("/decision")
async def record_decision(decision: LenderDecision) -> dict:
    # TODO: store lender decision and return acknowledgement
    pass
