from fastapi import FastAPI

from backend.app.api.routes_sme import router as sme_router
from backend.app.api.routes_lender import router as lender_router

app = FastAPI(title="GreenLedger API")

app.include_router(sme_router, prefix="/sme")
app.include_router(lender_router, prefix="/lender")
