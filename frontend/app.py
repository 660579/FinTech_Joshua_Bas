import streamlit as st

st.set_page_config(
    page_title="GreenLedger",
    page_icon="🌿",
    layout="centered",
)

st.title("GreenLedger")
st.caption("Turn invoice data into ESG signals — and into a lender-ready Financing Passport.")

st.divider()
st.subheader("Who are you?")

col_sme, col_lender = st.columns(2)

with col_sme:
    st.markdown("### SME")
    st.write("Upload invoices, get your Green Credit Score, and share a Financing Passport.")
    st.page_link("pages/1_SME_Upload.py", label="Start as SME →")

with col_lender:
    st.markdown("### Lender")
    st.write("Open a shared Financing Passport and record your lending decision.")
    st.page_link("pages/4_Lender_View.py", label="Open a Passport →")
