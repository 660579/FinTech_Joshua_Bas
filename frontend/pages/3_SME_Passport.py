import streamlit as st

from components.esg_display import render_classified_items_table, render_dimension_chart, render_financial_health, render_score_header
from components.theme import page_setup
from mock import mock_passport
from services import client

page_setup(title="Financing Passport — GreenLedger")

st.title("Financing Passport")
st.caption("Step 3 of 3 — SME flow")

esg_profile = st.session_state.get("esg_profile")
if esg_profile is None:
    st.info("No ESG scan yet. Upload your invoices first.")
    if st.button("Go to upload"):
        st.switch_page("pages/1_SME_Upload.py")
    st.stop()

passport = st.session_state.get("passport")

if passport is None:
    company_name = st.text_input("Company name (shown to the lender)", value="Müller & Partners GmbH")
    requested_amount = st.number_input(
        "Requested financing amount (€)", min_value=0.0, value=50_000.0, step=1_000.0
    )
    if st.button("Assemble Financing Passport", type="primary"):
        with st.spinner("Assembling passport…"):
            passport_id = client.create_passport(esg_profile, requested_amount_eur=requested_amount)
            fetched = client.get_passport(passport_id) if passport_id else None

        if fetched is None:
            st.warning(
                "Could not reach the GreenLedger backend. Showing a demo passport instead. "
                "Start the backend with `uvicorn backend.app.main:app --reload` to assemble a real one."
            )
            fetched = mock_passport()
            fetched["esg_profile"] = esg_profile
            fetched["requested_amount_eur"] = requested_amount

        st.session_state["passport"] = fetched
        st.session_state.setdefault("company_names", {})[fetched["passport_id"]] = company_name
        st.rerun()
    st.stop()

company_names = st.session_state.get("company_names", {})
display_name = company_names.get(passport["passport_id"], passport["company_name"])

st.subheader(display_name)
st.caption(f"Passport ID: `{passport['passport_id']}`  ·  created {passport['created_at']}")

requested_amount_eur = passport.get("requested_amount_eur")
if requested_amount_eur is not None:
    st.metric("Requested financing amount", f"€{requested_amount_eur:,.2f}")

render_score_header(passport["esg_profile"])

st.subheader("Financial health")
render_financial_health(passport["financial_health"])

st.subheader("Sustainability dimensions")
render_dimension_chart(passport["esg_profile"]["dimension_scores"])

st.subheader("Classified line items")
render_classified_items_table(passport["esg_profile"]["classified_line_items"])

st.divider()
st.subheader("Share with a lender")
st.write("Send this Passport ID to your lender so they can open it in the Lender View.")
st.code(passport["passport_id"], language=None)

if st.button("Start a new scan"):
    for key in ("esg_profile", "passport"):
        st.session_state.pop(key, None)
    st.switch_page("pages/1_SME_Upload.py")
