from fastapi import APIRouter, UploadFile, File

from backend.app.models.schemas import ESGProfile, Passport

router = APIRouter()


@router.post("/scan", response_model=ESGProfile)
async def scan_invoices(file: UploadFile = File(...)) -> ESGProfile:
    # TODO: call ingestion → classification → scoring services
    pass


@router.post("/passport", response_model=Passport)
async def create_passport(esg_profile: ESGProfile) -> Passport:
    # TODO: call passport assembler, store under a UUID, return passport
    pass
