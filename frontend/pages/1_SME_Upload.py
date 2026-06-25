from pathlib import Path

import streamlit as st

from components.theme import page_setup
from mock import mock_esg_profile
from services import client

page_setup(title="Upload Invoices — GreenLedger")

st.title("Upload Invoices")
st.caption("Step 1 of 3 — SME flow")

st.write(
    "Upload your invoice data (CSV or JSON) to run an ESG scan against the EU Taxonomy. "
    "PSD2 / accounting-software connections are simulated for this demo. All data is synthetic."
)

DEMO_FILE = Path("backend/data/synthetic/demo_invoices.csv")

uploaded_file = st.file_uploader("Invoice file", type=["csv", "json"])

col_upload, col_demo = st.columns(2)
run_upload = col_upload.button("Run ESG scan", type="primary", disabled=uploaded_file is None, width="stretch")
run_demo = col_demo.button("Use demo data instead", width="stretch")

if run_upload or run_demo:
    if run_demo:
        file_bytes = DEMO_FILE.read_bytes()
        filename = DEMO_FILE.name
    else:
        file_bytes = uploaded_file.getvalue()
        filename = uploaded_file.name

    with st.spinner("Embedding line items, matching against the EU Taxonomy, and scoring…"):
        esg_profile = client.scan_invoices(file_bytes, filename)

    if esg_profile is None:
        st.warning(
            "Could not reach the GreenLedger backend. Showing demo ESG data instead. "
            "Start the backend with `uvicorn backend.app.main:app --reload` to see real results."
        )
        esg_profile = mock_esg_profile()

    st.session_state["esg_profile"] = esg_profile
    st.session_state.pop("passport", None)  # invalidate any passport assembled from a previous scan
    st.success("Scan complete.")
    st.switch_page("pages/2_SME_Dashboard.py")
