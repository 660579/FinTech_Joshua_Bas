# Frontend build plan

The frontend delivers GreenLedger's two-sided flow. It is the part the lecture flagged as essential: not just a score on a screen, but the full hand-off where an SME produces a Financing Passport and a lender opens it and acts on it.

**Framework:** Streamlit (multipage app). Chosen for speed of building the two-sided flow for the demo. If we switch to React, the screens and build order stay the same; only the file layout changes.

## Build mock-first

Do **not** wait for the backend. Build every screen against a local `mock/` module that returns data shaped exactly like the agreed pydantic schemas (Invoice, ESGProfile, Passport). When the backend endpoints exist, swap the mock calls for real API calls. The screens don't change. This is what lets the frontend and backend be built in parallel.

## Screens

### SME side

1. **Upload / connect**: upload synthetic invoice data (CSV/JSON), or a mock "connect bank / accounting" button. A button triggers the ESG scan.
2. **ESG dashboard**: show the scan result: spend classified by EU Taxonomy category, the sustainability dimensions, the procurement sustainability score, and the headline **Green Credit Score** with a sector benchmark.
3. **Financing Passport**: the assembled lender-ready profile (ESG overview + basic financial-health metrics + Green Credit Score), with a **Share** action that produces a passport ID / link.

### Lender side

4. **Lender view**: open a shared passport by ID, review the borrower profile from the lender's perspective, and capture a **decision** (approve / decline + indicative terms). This closes the loop.

## File layout

```
frontend/
├── app.py                  # home: choose role (SME / Lender)
├── pages/
│   ├── 1_SME_Upload.py
│   ├── 2_SME_Dashboard.py
│   ├── 3_SME_Passport.py
│   └── 4_Lender_View.py
├── components/             # shared UI: score gauge, category breakdown chart, profile card
└── mock/                   # stubbed service responses shaped like the backend schemas
```

## Build order

1. Scaffold `app.py` with the SME/Lender role selector and empty pages.
2. SME upload → dashboard, running on `mock/` scan data.
3. Passport view + Share (store passports in session/mock so the lender can open one).
4. Lender view: open a passport by ID → review → decision.
5. Replace `mock/` calls with real backend API calls once endpoints are live.

## Notes

- All data is synthetic; no real bank/PSD2/accounting connections.
- Keep UI logic in pages/components; no business logic in the frontend (it calls the backend, which calls the services).
- UX is graded: minimal clicks, clear labels, no ESG jargon dumped on the user.
