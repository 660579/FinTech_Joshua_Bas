from __future__ import annotations

import tempfile
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.app.api.store import passport_store
from backend.app.models.schemas import ESGProfile
from backend.app.services.classification import classifier
from backend.app.services.ingestion import parser
from backend.app.services.passport import assembler
from backend.app.services.report import vsme_export
from backend.app.services.scoring import scorer

router = APIRouter()


@router.post("/scan", response_model=ESGProfile)
async def scan_invoices(file: UploadFile = File(...)) -> ESGProfile:
    contents = await file.read()

    suffix = Path(file.filename or "upload.csv").suffix.lower() or ".csv"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    invoices = parser.parse_invoices(tmp_path)

    all_items = [item for invoice in invoices for item in invoice.line_items]
    all_classified = classifier.classify_line_items(all_items)
    classified_items = [item for item in all_classified if item.taxonomy_category is not None]

    sme_id = str(uuid4())
    profile = scorer.score(
        all_items=all_items,
        classified_items=classified_items,
        sme_id=sme_id,
        sector="C25",
    )
    return profile


@router.post("/passport")
async def create_passport(esg_profile: ESGProfile) -> dict:
    passport = assembler.assemble_passport(esg_profile, esg_profile.sme_id)
    passport_store[passport.passport_id] = passport
    vsme_export.export_vsme(passport)
    return {"passport_id": passport.passport_id}
