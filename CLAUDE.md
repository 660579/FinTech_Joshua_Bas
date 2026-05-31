# CLAUDE.md

Agent instructions for the **GreenLedger** MVP. Read this at the start of every session before editing code.

## What this project is

GreenLedger is a FinTech MVP that turns SME **invoice data into ESG sustainability signals** and packages them into a lender-ready **Financing Passport**. It is a course MVP (Erasmus / RSM FinTech), not production software: favour a **working, demonstrable end-to-end flow** over completeness or scale. If a feature can be faked convincingly for the demo, fake it cleanly rather than building real infrastructure.

The product has two sides and the demo must show **both**:
- **SME side:** upload/connect invoice data → get an ESG scan + Green Credit Score → generate and share a Financing Passport.
- **Lender side:** open a shared Financing Passport → view the enriched borrower profile → make a lending decision.

A scoring screen alone is not the MVP. The multi-party hand-off (SME shares → lender acts) is a graded, core feature. Do not drop it.

## Open decisions (not yet locked — confirm before building on these)

- **Frontend:** Streamlit (fast, single Python app) vs React (more polished for the investor video). Default assumed below: **Streamlit**. If this changes, update the layout and commands.
- **Embeddings:** local `sentence-transformers` (self-contained, free to run) vs hosted embedding API (simpler code, adds an API key + cost). Default assumed: **local**.
- **Vector store:** FAISS / Chroma / plain NumPy. For our small set of EU Taxonomy categories, **plain NumPy or Chroma** is enough. Don't add a hosted vector DB.

When one of these is decided, edit this file so the instructions stay accurate.

## Architecture (the pipeline)

```
invoice data → ingestion → classification (embed + match + RAG) → scoring → passport → report
                                                                       │
                                            SME dashboard ◄────────────┘────────► Lender view
```

1. **ingestion** — parse invoices into structured line items (supplier, description, quantity, amount).
2. **classification** (the core, where most of the grade lives):
   - embed each line item with a transformer model;
   - compare against **precomputed EU Taxonomy category embeddings** using inner-product / cosine similarity;
   - use **RAG**: retrieve the matched category's definition text and pass it as context so the classification is grounded in regulation, not the model's memory.
3. **scoring** — aggregate classified line items into sustainability dimensions → a procurement sustainability score → a headline **Green Credit Score** with simple sector benchmarking.
4. **passport** — assemble the **Financing Passport**: ESG profile + basic financial-health metrics + Green Credit Score.
5. **report** — export a VSME-format ESG report the SME can share.

## Directory layout

```
backend/app/main.py            FastAPI entry point
backend/app/api/routes_sme.py  SME endpoints (upload, scan, passport)
backend/app/api/routes_lender.py  Lender endpoints (view passport, decide)
backend/app/models/            pydantic schemas (Invoice, ESGProfile, Passport, ...)
backend/app/services/ingestion/        invoice parsing
backend/app/services/classification/   embeddings + taxonomy matching + RAG
backend/app/services/scoring/          dimensions + Green Credit Score
backend/app/services/passport/         Financing Passport assembly
backend/app/services/report/           VSME report export
backend/data/taxonomy/         EU Taxonomy category definition text
backend/data/vectorstore/      precomputed category embeddings
backend/tests/                 tests
frontend/                      SME dashboard + lender view
scripts/generate_synthetic_invoices.py   synthetic demo data
```

## Tech stack

- Python 3.11+
- FastAPI (backend), Streamlit (frontend — see open decisions)
- `sentence-transformers` for embeddings, NumPy/Chroma for similarity search
- pydantic for schemas, pytest for tests

## Commands

Adjust to match the final `pyproject.toml` / `requirements.txt`.

```bash
# setup
python -m venv .venv && source .venv/bin/activate
pip install -e .                      # or: pip install -r requirements.txt

# generate demo data (run before first demo)
python scripts/generate_synthetic_invoices.py

# precompute taxonomy embeddings
python -m backend.app.services.classification.build_index

# run backend
uvicorn backend.app.main:app --reload

# run frontend (if Streamlit)
streamlit run frontend/app.py

# tests
pytest
```

## Conventions

- Type-hint everything; use pydantic models for any data crossing a function or API boundary.
- Keep each `services/` module independently testable — they should not import from `api/` or the frontend.
- Business logic lives in `services/`, never in route handlers or UI code. Routes/UI just call services.
- Small, focused functions over large ones. Comment the *why* for any non-obvious modelling/scoring choice (graders read this).
- No secrets in the repo. Use a `.env` file (git-ignored) and read via config; provide a `.env.example`.

## Domain glossary (use these terms correctly)

- **EU Taxonomy** — EU classification of environmentally sustainable economic activities; the categories we match invoice line items against.
- **VSME** — Voluntary Sustainability Reporting Standard for non-listed SMEs; the standardised report format we export.
- **GAR (Green Asset Ratio)** — bank metric we reference as the market motivation; we do **not** compute it.
- **Financing Passport** — our core deliverable: a lender-ready SME profile (ESG + financial health + Green Credit Score).
- **Green Credit Score** — the headline ESG/creditworthiness score we produce for an SME.
- **AISP / PSD2** — the open-banking licensing/data framework the real product would use. In this MVP it is **simulated**.

## Guardrails — do NOT do these

- **No real bank / PSD2 / accounting-software integrations.** All transaction and invoice data is **synthetic** (`scripts/generate_synthetic_invoices.py`). Never add code that calls a real banking or accounting API.
- **No real personal or financial data** anywhere in the repo or commits.
- Don't over-engineer: no auth systems, no databases beyond what the demo needs, no deployment infra unless asked. Keep it runnable with the commands above on a fresh clone.
- Don't silently change the architecture or the SME↔lender flow. Flag it first.
- Don't invent EU Taxonomy / VSME categories — pull definitions from `backend/data/taxonomy/`.

## Git & collaboration (graded)

- Two contributors; both should have visible, meaningful commit history. Don't squash one person's work into the other's.
- Work on feature branches; merge to `main` via pull requests.
- Clear, present-tense commit messages describing the change.
- Decide as a team whether to keep the `Co-authored-by: Claude` trailer on AI-assisted commits.
