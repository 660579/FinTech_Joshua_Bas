import streamlit as st
from components.theme import page_setup

page_setup(layout="centered")

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 4rem 0 2rem;">
    <div style="
        display: inline-flex;
        align-items: center;
        gap: 0.55rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: #0F5132;
        line-height: 1;
    ">
        <span style="font-size: 2.4rem;">🌿</span>
        GreenLedger
    </div>
    <div style="
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        font-weight: 400;
        color: #5A7268;
        margin-top: 1rem;
        line-height: 1.7;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
    ">
        Turn invoice data into ESG signals —<br>
        and into a lender-ready Financing Passport.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Divider ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    width: 48px;
    height: 3px;
    background: #0F5132;
    border-radius: 2px;
    margin: 0 auto 2.5rem;
    opacity: 0.35;
"></div>
""", unsafe_allow_html=True)

# ── Role label ─────────────────────────────────────────────────────────────────
st.markdown("""
<p style="
    text-align: center;
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8FAF9E;
    margin-bottom: 1.25rem;
">Select your role</p>
""", unsafe_allow_html=True)

# ── Role cards ─────────────────────────────────────────────────────────────────
col_sme, spacer, col_lender = st.columns([1, 0.08, 1])

with col_sme:
    with st.container(border=True):
        st.markdown("""
        <div style="padding: 0.25rem 0 0.75rem;">
            <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">🏢</div>
            <div style="
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.15rem;
                font-weight: 700;
                letter-spacing: -0.02em;
                color: #14211C;
                margin-bottom: 0.5rem;
            ">SME</div>
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                color: #5A7268;
                line-height: 1.6;
                min-height: 2.8rem;
            ">Upload invoices, get your Green Credit Score, and share a Financing Passport.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as SME", type="primary", use_container_width=True):
            st.switch_page("pages/1_SME_Upload.py")

with col_lender:
    with st.container(border=True):
        st.markdown("""
        <div style="padding: 0.25rem 0 0.75rem;">
            <div style="font-size: 1.75rem; margin-bottom: 0.5rem;">🏦</div>
            <div style="
                font-family: 'Plus Jakarta Sans', sans-serif;
                font-size: 1.15rem;
                font-weight: 700;
                letter-spacing: -0.02em;
                color: #14211C;
                margin-bottom: 0.5rem;
            ">Lender</div>
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                color: #5A7268;
                line-height: 1.6;
                min-height: 2.8rem;
            ">Open a shared Financing Passport, review ESG data, and record your lending decision.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Open a Passport", type="primary", use_container_width=True):
            st.switch_page("pages/4_Lender_View.py")
