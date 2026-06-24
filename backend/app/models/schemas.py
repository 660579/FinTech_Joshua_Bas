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


class ESGProfile(BaseModel):
    sme_id: str
    procurement_sustainability_score: float
    green_credit_score: float
    dimension_scores: dict[str, float]
    classified_line_items: list[ClassifiedLineItem]
    sector_benchmark: Optional[SectorBenchmark] = None


class Passport(BaseModel):
    passport_id: str
    sme_id: str
    company_name: str
    esg_profile: ESGProfile
    financial_health: dict[str, float]
    created_at: str
    shared: bool = False


class LenderDecision(BaseModel):
    passport_id: str
    decision: str  # "approve" | "decline"
    indicative_rate: Optional[float] = None
    notes: Optional[str] = None
