"""GreenLedger FastAPI application entry point.

load_dotenv() is called before any other import so that GROQ_API_KEY and other
env vars are available to modules that read them at import time.
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from backend.app.api.routes_sme import router as sme_router
from backend.app.api.routes_lender import router as lender_router

app = FastAPI(title="GreenLedger API")

app.include_router(sme_router, prefix="/sme")
app.include_router(lender_router, prefix="/lender")
