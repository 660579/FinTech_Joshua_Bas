from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class LineItem(BaseModel):
    supplier: str
    description: str
    quantity: float
    amount: float
    unit: Optional[str] = None


class Invoice(BaseModel):
    invoice_id: str
    sme_id: str
    date: str
    currency: str = "EUR"
    line_items: list[LineItem]


class ClassifiedLineItem(LineItem):
    taxonomy_category: Optional[str] = None
    taxonomy_objective: Optional[str] = None
    similarity_score: Optional[float] = None
    rationale: Optional[str] = None


class SectorBenchmark(BaseModel):
    sector: str
    median_green_credit_score: float


class DataQuality(BaseModel):
    """Reliability indicator for the Green Credit Score; does not affect the score itself.

    More classified data (more invoices, longer history) should yield a higher
    confidence_pct/tier, so a lender can weigh the score against how much it's based on.
    """

    confidence_pct: float  # 0-100
    tier: str  # "High" | "Medium" | "Low"
    basis: str  # short human-readable explanation, e.g. "Based on 18 classified line items"


class ESGProfile(BaseModel):
    sme_id: str
    procurement_sustainability_score: float
    green_credit_score: float
    dimension_scores: dict[str, float]
    classified_line_items: list[ClassifiedLineItem]
    sector_benchmark: Optional[SectorBenchmark] = None
    data_quality: Optional[DataQuality] = None


class Passport(BaseModel):
    passport_id: str
    sme_id: str
    company_name: str
    esg_profile: ESGProfile
    financial_health: dict[str, float]
    requested_amount_eur: Optional[float] = None
    created_at: str
    shared: bool = False


class LenderDecision(BaseModel):
    passport_id: str
    decision: str  # "approve" | "decline"
    indicative_rate: Optional[float] = None
    approved_amount_eur: Optional[float] = None
    notes: Optional[str] = None
