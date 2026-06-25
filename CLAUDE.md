# CLAUDE.md

Agent instructions for the **GreenLedger** MVP. Read this at the start of every session before editing code.

## What this project is

GreenLedger is a FinTech MVP that turns SME **invoice data into ESG sustainability signals** and packages them into a lender-ready **Financing Passport**. It is a course MVP (Erasmus / RSM FinTech), not production software: favour a **working, demonstrable end-to-end flow** over completeness or scale. If a feature can be faked convincingly for the demo, fake it cleanly rather than building real infrastructure.

The product has two sides and the demo must show **both**:
- **SME side:** upload/connect invoice data → get an ESG scan + Green Credit Score → generate and share a Financing Passport.
- **Lender side:** open a shared Financing Passport → view the enriched borrower profile → make a lending decision.

A scoring screen alone is not the MVP. The multi-party hand-off (SME shares → lender acts) is a graded, core feature. Do not drop it.

The Lender View also shows a **multi-SME comparison roster** (the real SME that went through the pipeline this session, plus fictional demo SMEs in `frontend/mock/seed_smes.py`) so a lender can compare and choose who to finance, and a **data-quality / confidence indicator** alongside the Green Credit Score (`ESGProfile.data_quality`, does not change the score, just how much data it's based on).

## Locked decisions

- **Frontend:** Streamlit.
- **Embeddings:** local `sentence-transformers` (`all-MiniLM-L6-v2`).
- **Vector store:** plain NumPy (`backend/app/services/classification/matcher.py`) over precomputed embeddings; no hosted vector DB.

## Architecture (the pipeline)

```
invoice data → ingestion → classification (embed + match + RAG) → scoring → passport → report
                                                                       │
                                            SME dashboard ◄────────────┘────────► Lender view
```

1. **ingestion**: parse invoices into structured line items (supplier, description, quantity, amount).
2. **classification** (the core, where most of the grade lives):
   - embed each line item with a transformer model;
   - compare against **precomputed EU Taxonomy category embeddings** using inner-product / cosine similarity;
   - use **RAG**: retrieve the matched category's definition text and pass it as context so the classification is grounded in regulation, not the model's memory.
3. **scoring**: aggregate classified line items into sustainability dimensions → a procurement sustainability score → a headline **Green Credit Score** with simple sector benchmarking.
4. **passport**: assemble the **Financing Passport**: ESG profile + basic financial-health metrics + Green Credit Score + requested financing amount.
5. **report**: export a VSME-format ESG report the SME can share.

The frontend never calls backend services directly: it goes through `frontend/services/client.py`, an HTTP adapter. If the backend is unreachable, every screen falls back to `frontend/mock/` data and shows a visible warning rather than crashing. Don't break this fallback when changing either side.

## Directory layout

```
backend/app/main.py                    FastAPI entry point
backend/app/api/                       SME + lender routes, in-memory passport/decision store
backend/app/models/schemas.py          pydantic schemas (Invoice, ESGProfile, Passport, DataQuality, LenderDecision, ...)
backend/app/services/ingestion/        invoice parsing
backend/app/services/classification/   embeddings + taxonomy matching + RAG
backend/app/services/scoring/          dimensions + Green Credit Score
backend/app/services/passport/         Financing Passport assembly
backend/app/services/report/           VSME report export
backend/data/taxonomy/                 EU Taxonomy category definition text
backend/data/vectorstore/              precomputed category embeddings (run build_index before first use — empty on a fresh clone)
backend/tests/                         tests

frontend/app.py                 landing page (SME/Lender role selector)
frontend/pages/                 SME Upload, SME Dashboard, SME Passport, Lender View
frontend/components/theme.py    page_setup() — logo, header, global CSS (call this first on every page)
frontend/components/esg_display.py   shared score/quality-badge/chart/table rendering, reused by every screen
frontend/services/client.py     HTTP adapter to the backend; mock-fallback + warning on failure
frontend/mock/                  fallback mock data, plus seed_smes.py — fictional demo SMEs for the lender roster
frontend/assets/logo.svg        GreenLedger wordmark

scripts/generate_synthetic_invoices.py   synthetic demo data for the real (non-fictional) pipeline
```

## Tech stack

- Python 3.13 (3.11+ required)
- FastAPI (backend), Streamlit (frontend)
- `sentence-transformers` for embeddings, plain NumPy for similarity search
- Groq API (`llama-3.3-70b-versatile`) for RAG rationale generation, gracefully degrading to a templated sentence when `GROQ_API_KEY` is unset
- pydantic for schemas, pytest for tests, `requests` for the frontend→backend adapter

## Commands

```bash
# setup — backend
python -m venv .venv && source .venv/bin/activate
pip install -e .                              # installs backend/ from pyproject.toml

# setup — frontend (same venv)
pip install -r frontend/requirements.txt

# generate demo data (run before first demo)
python scripts/generate_synthetic_invoices.py

# precompute taxonomy embeddings — REQUIRED before the backend can classify anything
python -m backend.app.services.classification.build_index

# run backend
uvicorn backend.app.main:app --reload --reload-dir backend   # scope --reload-dir to backend/, not the repo root

# run frontend (separate terminal, same venv)
streamlit run frontend/app.py

# tests
pip install -e ".[dev]"     # adds pytest if not already installed
pytest
```

The frontend defaults to `GREENLEDGER_API_URL=http://localhost:8000`. Both servers must be running for real (non-mock) results end to end.

## Conventions

- Type-hint everything; use pydantic models for any data crossing a function or API boundary.
- Keep each `services/` module independently testable: they should not import from `api/` or the frontend.
- Business logic lives in `services/`, never in route handlers or UI code. Routes/UI just call services.
- Small, focused functions over large ones. Comment the *why* for any non-obvious modelling/scoring choice (graders read this).
- No secrets in the repo. Use a `.env` file (git-ignored) and read via config; provide a `.env.example`.

## Domain glossary (use these terms correctly)

- **EU Taxonomy**: EU classification of environmentally sustainable economic activities; the categories we match invoice line items against.
- **VSME**: Voluntary Sustainability Reporting Standard for non-listed SMEs; the standardised report format we export.
- **GAR (Green Asset Ratio)**: bank metric we reference as the market motivation; we do **not** compute it.
- **Financing Passport**: our core deliverable: a lender-ready SME profile (ESG + financial health + Green Credit Score).
- **Green Credit Score**: the headline ESG/creditworthiness score we produce for an SME.
- **Data quality / confidence**: a tier (High/Medium/Low) + confidence % shown alongside the Green Credit Score, indicating how much classified data it's based on. Never changes the score itself.
- **AISP / PSD2**: the open-banking licensing/data framework the real product would use. In this MVP it is **simulated**.

## Guardrails: do NOT do these

- **No real bank / PSD2 / accounting-software integrations.** All transaction and invoice data is **synthetic** (`scripts/generate_synthetic_invoices.py`). Never add code that calls a real banking or accounting API.
- **No real personal or financial data** anywhere in the repo or commits.
- Don't over-engineer: no auth systems, no databases beyond what the demo needs, no deployment infra unless asked. Keep it runnable with the commands above on a fresh clone.
- Don't silently change the architecture or the SME↔lender flow. Flag it first.
- Don't invent EU Taxonomy / VSME categories. Pull definitions from `backend/data/taxonomy/`.
- The lender comparison roster's fictional SMEs (`frontend/mock/seed_smes.py`) must stay clearly labelled as demo seed data and separate from the real pipeline. Never blend fabricated company data into `backend/` or the classification/scoring logic.

## Git & collaboration (graded)

- Two contributors; both should have visible, meaningful commit history. Don't squash one person's work into the other's.
- Work on feature branches; merge to `main` via pull requests.
- Clear, present-tense commit messages describing the change.
- Decide as a team whether to keep the `Co-authored-by: Claude` trailer on AI-assisted commits.
   