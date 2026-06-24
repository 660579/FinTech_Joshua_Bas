# Backend build plan

The backend delivers GreenLedger's pipeline: turning raw invoice data into ESG signals and packaging them into a lender-ready Financing Passport. It is the engine the frontend calls — no business logic lives anywhere else.

**Framework:** FastAPI (Python). Chosen for lightweight routing and automatic API docs, which makes it easy to test endpoints during development and hand off to the frontend.

## Build service-first

Do **not** start with API routes. Build and test each service independently before wiring it into a route. When all services pass their tests, wrap them in routes — the services don't change. This is what lets the pipeline be validated piece by piece before the full flow exists.

## Services

### Pipeline

1. **Ingestion** — parse a CSV or JSON file into structured `Invoice` and `LineItem` models.
2. **Classification** — the core of the pipeline:
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
4. Populate `backend/data/taxonomy/` with EU Taxonomy activity definition texts. Each file covers one **activity** (not one objective; activities roll up to objectives via the `EU Taxonomy Objective:` field). The set of activities to cover is driven by the spend categories in `demo_invoices.csv` — add or remove files as the demo data evolves. See *Taxonomy file format* below for the required structure. After generation, do a light manual check that NACE codes and technical screening criteria are plausible against the actual delegated acts. Commit.
5. Implement the classification service: `build_index.py` first, then `embedder.py`, `matcher.py`, `rag.py`, `classifier.py`. Run `test_classification.py`. Commit.
6. Implement `scorer.py`. Run `test_scoring.py`. Commit.
7. Implement `assembler.py` and `vsme_export.py`. Commit.
8. Wire everything into `routes_sme.py` and `routes_lender.py`. Test with `uvicorn` and curl. Commit.
9. Joshua swaps `mock/` calls for real API calls. Test the full SME → lender hand-off end to end.

## Taxonomy file format

Each file in `backend/data/taxonomy/` must follow this exact structure so `build_index.py` can parse it reliably. Filename: `<snake_case_activity_name>.txt`.

```
Category: <Human-readable activity name>
EU Taxonomy Objective: <One of: Climate Change Mitigation | Climate Change Adaptation | Water & Marine Resources | Circular Economy | Pollution Prevention & Control | Biodiversity & Ecosystems>
NACE Code Reference: <Code(s) and short description, e.g. "F43.21 (Electrical installation activities)">

Definition:
<2–4 sentence plain-English description of the economic activity and what makes it environmentally sustainable under the EU Taxonomy.>

Qualifying activities include:
- <bullet>
- <bullet>
...

Example invoice descriptions:
<comma-separated keywords and short phrases a supplier invoice might contain; used by the embedder to match line items>

Do substantial harm considerations:
<1–3 sentences covering DNSH conditions relevant to this activity (waste handling, hazardous substances, other environmental objectives).>
```

**Agent instructions for writing taxonomy files:**
- Cover the six EU Taxonomy environmental objectives: Climate Change Mitigation, Climate Change Adaptation, Water & Marine Resources, Circular Economy, Pollution Prevention & Control, Biodiversity & Ecosystems.
- Derive the activity list from `demo_invoices.csv` — every spend category in the demo data should map to at least one file. Add files for adjacent green activities that the demo might plausibly classify against.
- Keep NACE codes accurate; cross-check against the delegated acts (Annexes I and II to Regulation (EU) 2021/2139 for mitigation/adaptation; Annexes to Regulation (EU) 2023/2485 for the remaining objectives).
- The `Example invoice descriptions` field is the most important for RAG quality — make it specific and varied (brand-agnostic technical terms, abbreviations, colloquial names).
- Do not invent objectives or sub-objectives that do not exist in the Taxonomy. Stick to the six above.
- After writing, a human should do a light sanity-check of NACE codes and DNSH conditions against the actual delegated acts before the demo.

## Configuration (must be done manually)

- **Anthropic API key** — create a `.env` file in the project root (git-ignored) with `ANTHROPIC_API_KEY=your_key_here`. Get the key from console.anthropic.com. Also create `.env.example` with the same keys but empty values — this goes in the repo.
- **Sector benchmarks** — the hardcoded benchmark scores in `scorer.py` must be defensible. Decide which NACE sector the demo SME operates in, pick a realistic benchmark score, and be ready to justify it in the video.
- **Synthetic invoice content** — review what `generate_synthetic_invoices.py` produces before the demo. Line item descriptions must be specific enough to classify well (e.g. "solar panel installation" or "diesel fuel 500L"), not generic (e.g. "goods purchased").

## Notes

- All data is synthetic — no real PSD2, bank, or accounting software connections.
- Business logic lives in `services/`, never in route handlers. Routes just call services.
- Comment the *why* on all scoring weight choices.
