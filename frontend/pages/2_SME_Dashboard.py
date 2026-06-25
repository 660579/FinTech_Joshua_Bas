import streamlit as st

from components.esg_display import render_classified_items_table, render_dimension_chart, render_score_header
from components.theme import page_setup

page_setup(title="ESG Dashboard — GreenLedger")

st.title("ESG Dashboard")
st.caption("Step 2 of 3 — SME flow")

esg_profile = st.session_state.get("esg_profile")
if esg_profile is None:
    st.info("No ESG scan yet. Upload your invoices first.")
    if st.button("Go to upload"):
        st.switch_page("pages/1_SME_Upload.py")
    st.stop()

render_score_header(esg_profile)

st.subheader("Sustainability dimensions")
st.caption("Share of total spend matched to each EU Taxonomy objective.")
render_dimension_chart(esg_profile["dimension_scores"])

st.subheader("Classified line items")
render_classified_items_table(esg_profile["classified_line_items"])

st.divider()
if st.button("Continue to Financing Passport →", type="primary"):
    st.switch_page("pages/3_SME_Passport.py")
