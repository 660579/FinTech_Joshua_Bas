# Backend build plan

The backend delivers GreenLedger's pipeline: turning raw invoice data into ESG signals and packaging them into a lender-ready Financing Passport. It is the engine the frontend calls — no business logic lives anywhere else.

**Framework:** FastAPI (Python). Chosen for lightweight routing and automatic API docs, which makes it easy to test endpoints during development and hand off to the frontend.

## Build service-first

Do **not** start with API routes. Build and test each service independently before wiring it into a route. When all services pass their tests, wrap them in routes — the services don't change. This is what lets the pipeline be validated piece by piece before the full flow exists.

## Services

### Pipeline

1. **Ingestion** — parse a CSV or JSON file into structured `Invoice` and `LineItem` models.
2. **Classification** — the core, where most of the grade lives:
   - embed each line item description with `sentence-transformers`;
   - match against precomputed EU Taxonomy category embeddings using cosine similarity;
   - call the Anthropic API via RAG: retrieve the matched category definition and use it as context to generate a one-sentence rationale grounded in regulation, not model memory.
3. **Scoring** — aggregate classified line items into sustainability dimension scores and a headline **Green Credit Score** (0–100) with sector benchmarking. Weights are rule-based and commented for auditability.
4. **Passport** — assemble the Financing Passport: ESG profile + Green Credit Score, stored in an in-memory dict under a UUID passport ID.
5. **Report** — serialise the Passport into a VSME-structured JSON file the SME can share.

### API endpoints

SME side (`routes_sme.py`):
- `POST /sme/scan` — upload invoice data, run the pipeline, return an `ESGProfile`.
- `POST /sme/passport` — assemble and store a Passport, return the passport ID.

Lender side (`routes_lender.py`):
- `GET /lender/passport/{passport_id}` — retrieve a shared Passport by ID.
- `POST /lender/decision` — record approve / decline + indicative terms.

## File layout

```
backend/
├── app/
│   ├── main.py                          # FastAPI entry point, mounts routers
│   ├── api/
│   │   ├── routes_sme.py                # SME endpoints
│   │   └── routes_lender.py             # Lender endpoints
│   ├── models/                          # pydantic schemas: Invoice, ESGProfile, Passport, LenderDecision
│   └── services/
│       ├── ingestion/parser.py
│       ├── classification/
│       │   ├── build_index.py           # run once: embed taxonomy definitions → save index
│       │   ├── embedder.py
│       │   ├── matcher.py
│       │   ├── rag.py
│       │   └── classifier.py            # orchestrates embed → match → RAG
│       ├── scoring/scorer.py
│       ├── passport/assembler.py
│       └── report/vsme_export.py
├── data/
│   ├── taxonomy/                        # .txt files: one per EU Taxonomy category (supply manually)
│   ├── vectorstore/                     # taxonomy_index.npy + categories.json (generated, git-ignored)
│   └── reports/                         # generated VSME JSON reports (git-ignored)
└── tests/
    ├── test_ingestion.py
    ├── test_classification.py
    └── test_scoring.py
scripts/
└── generate_synthetic_invoices.py       # produces demo_invoices.csv
```

## Build order

1. Scaffold all directories and stub files. Commit.
2. Implement pydantic schemas in `models/`. Share with Joshua so his `mock/` data matches. Commit.
3. Implement `parser.py` and `generate_synthetic_invoices.py`. Run `test_ingestion.py`. Commit.
4. Populate `backend/data/taxonomy/` with real EU Taxonomy category definition texts — one `.txt` per category. This cannot be delegated to the agent. Commit.
5. Implement the classification service: `build_index.py` first, then `embedder.py`, `matcher.py`, `rag.py`, `classifier.py`. Run `test_classification.py`. Commit.
6. Implement `scorer.py`. Run `test_scoring.py`. Commit.
7. Implement `assembler.py` and `vsme_export.py`. Commit.
8. Wire everything into `routes_sme.py` and `routes_lender.py`. Test with `uvicorn` and curl. Commit.
9. Joshua swaps `mock/` calls for real API calls. Test the full SME → lender hand-off end to end.

## Configuration (must be done manually — do not delegate to the agent)

- **Taxonomy definitions** — populate `backend/data/taxonomy/` with real EU Taxonomy category definition texts, one `.txt` file per objective. Pull from the EU Platform on Sustainable Finance. The six objectives are: climate change mitigation, climate change adaptation, water & marine resources, circular economy, pollution prevention, and biodiversity. If the agent writes these, the RAG is grounded in fiction.
- **Anthropic API key** — create a `.env` file in the project root (git-ignored) with `ANTHROPIC_API_KEY=your_key_here`. Get the key from console.anthropic.com. Also create `.env.example` with the same keys but empty values — this goes in the repo.
- **Sector benchmarks** — the hardcoded benchmark scores in `scorer.py` must be defensible. Decide which NACE sector the demo SME operates in, pick a realistic benchmark score, and be ready to justify it in the video.
- **Synthetic invoice content** — review what `generate_synthetic_invoices.py` produces before the demo. Line item descriptions must be specific enough to classify well (e.g. "solar panel installation" or "diesel fuel 500L"), not generic (e.g. "goods purchased").

## Notes

- All data is synthetic — no real PSD2, bank, or accounting software connections.
- Business logic lives in `services/`, never in route handlers. Routes just call services.
- Comment the *why* on all scoring weight choices — graders read this.
