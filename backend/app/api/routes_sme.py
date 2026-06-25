"""SME-side API routes: invoice upload, ESG scan, and Financing Passport creation."""
from __future__ import annotations

import os
import tempfile
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from backend.app.api.store import passport_store
from backend.app.models.schemas import ESGProfile
from backend.app.services.classification import classifier
from backend.app.services.ingestion import parser
from backend.app.services.passport import assembler
from backend.app.services.report import vsme_export
from backend.app.services.scoring import scorer

router = APIRouter()


class PassportRequest(BaseModel):
    esg_profile: ESGProfile
    requested_amount_eur: float | None = None


@router.post("/scan", response_model=ESGProfile)
async def scan_invoices(file: UploadFile = File(...)) -> ESGProfile:
    contents = await file.read()

    suffix = Path(file.filename or "upload.csv").suffix.lower() or ".csv"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        invoices = parser.parse_invoices(tmp_path)
    finally:
        os.unlink(tmp_path)

    all_items = [item for invoice in invoices for item in invoice.line_items]
    all_classified = classifier.classify_line_items(all_items)
    classified_items = [item for item in all_classified if item.taxonomy_category is not None]

    sme_id = str(uuid4())
    profile = scorer.score(
        all_items=all_items,
        classified_items=classified_items,
        sme_id=sme_id,
        sector="C25",  # NACE C25 (fabricated metal products), demo default; see scorer.SECTOR_BENCHMARK
    )
    return profile


@router.post("/passport")
async def create_passport(body: PassportRequest) -> dict:
    passport = assembler.assemble_passport(
        body.esg_profile, body.esg_profile.sme_id, body.requested_amount_eur
    )
    passport_store[passport.passport_id] = passport
    vsme_export.export_vsme(passport)
    return {"passport_id": passport.passport_id}
