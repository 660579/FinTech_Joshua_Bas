import streamlit as st
from components.theme import logo_html, page_setup

page_setup(layout="wide", show_header=False)

# Page-specific CSS: hide sidebar on the landing page, reduce top padding
st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1.5rem !important; padding-bottom: 5rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
# NOTE: no blank lines inside this HTML string: a blank line terminates a
# markdown HTML block (CommonMark spec), causing inner tags to render as text.
st.markdown(f"""
<div style="background:linear-gradient(148deg,#071410 0%,#0C3820 48%,#155C32 100%);border-radius:20px;padding:5.5rem 4rem 5rem;position:relative;overflow:hidden;text-align:center;">
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,0.032) 1px,transparent 1px);background-size:26px 26px;border-radius:20px;pointer-events:none;"></div>
<div style="position:absolute;top:-120px;right:-80px;width:480px;height:480px;background:radial-gradient(circle,rgba(74,222,128,0.09) 0%,transparent 68%);pointer-events:none;"></div>
<div style="position:absolute;bottom:-60px;left:-60px;width:300px;height:300px;background:radial-gradient(circle,rgba(15,81,50,0.4) 0%,transparent 70%);pointer-events:none;"></div>
<div style="position:relative;max-width:680px;margin:0 auto;">
<div class="gl-a1" style="display:flex;justify-content:center;margin-bottom:1.6rem;">{logo_html(height=34, color='#FFFFFF', accent='#4ADE80')}</div>
<div class="gl-a1" style="display:inline-flex;align-items:center;gap:0.45rem;background:rgba(74,222,128,0.1);border:1px solid rgba(74,222,128,0.22);border-radius:100px;padding:0.38rem 1.05rem;font-family:'Inter',sans-serif;font-size:0.76rem;font-weight:500;color:#4ADE80;letter-spacing:0.05em;margin-bottom:1.8rem;">🌿 &nbsp;ESG Intelligence Platform</div>
<h1 class="gl-a2" style="font-family:'Plus Jakarta Sans',sans-serif;font-size:3.75rem;font-weight:800;letter-spacing:-0.04em;line-height:1.07;color:#FFFFFF;margin:0 0 1.4rem;">Turn invoices into a<br><span style="color:#4ADE80;">green financing edge.</span></h1>
<p class="gl-a3" style="font-family:'Inter',sans-serif;font-size:1.08rem;font-weight:400;color:rgba(255,255,255,0.60);line-height:1.78;margin:0 auto 2.4rem;max-width:520px;">GreenLedger scans your invoice data against the EU Taxonomy, generates a <strong style="color:rgba(255,255,255,0.87);font-weight:500;">Green Credit Score</strong>, and assembles a <strong style="color:rgba(255,255,255,0.87);font-weight:500;">Financing Passport</strong> your lender can act on immediately.</p>
<div class="gl-a4" style="display:flex;justify-content:center;gap:0.5rem;flex-wrap:wrap;">
<span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.11);border-radius:100px;padding:0.32rem 0.95rem;font-family:'Inter',sans-serif;font-size:0.78rem;color:rgba(255,255,255,0.52);">EU Taxonomy</span>
<span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.11);border-radius:100px;padding:0.32rem 0.95rem;font-family:'Inter',sans-serif;font-size:0.78rem;color:rgba(255,255,255,0.52);">Green Credit Score</span>
<span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.11);border-radius:100px;padding:0.32rem 0.95rem;font-family:'Inter',sans-serif;font-size:0.78rem;color:rgba(255,255,255,0.52);">Financing Passport</span>
<span style="background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.11);border-radius:100px;padding:0.32rem 0.95rem;font-family:'Inter',sans-serif;font-size:0.78rem;color:rgba(255,255,255,0.52);">VSME Report</span>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── How it works ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#F4F7F5;border-radius:16px;padding:3.25rem 3.5rem;margin-top:1.25rem;">
<p style="text-align:center;font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#7EA88E;margin:0 0 0.55rem;">How it works</p>
<p style="text-align:center;font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5rem;font-weight:700;letter-spacing:-0.02em;color:#0D1B13;margin:0 0 2.5rem;">From invoice data to lending decision in minutes</p>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.75rem;">
<div class="gl-a4">
<div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:0.12em;color:#0F5132;margin-bottom:0.7rem;">01</div>
<div style="font-size:1.65rem;margin-bottom:0.65rem;">📂</div>
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1rem;font-weight:700;letter-spacing:-0.01em;color:#0D1B13;margin-bottom:0.4rem;">Upload Invoices</div>
<div style="font-family:'Inter',sans-serif;font-size:0.88rem;color:#5A7268;line-height:1.65;">Connect your accounting data or drop a CSV/JSON file. PSD2 is simulated for the demo.</div>
</div>
<div class="gl-a5" style="border-left:1px solid #DFE9E4;border-right:1px solid #DFE9E4;padding:0 1.75rem;">
<div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:0.12em;color:#0F5132;margin-bottom:0.7rem;">02</div>
<div style="font-size:1.65rem;margin-bottom:0.65rem;">🔬</div>
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1rem;font-weight:700;letter-spacing:-0.01em;color:#0D1B13;margin-bottom:0.4rem;">AI ESG Classification</div>
<div style="font-family:'Inter',sans-serif;font-size:0.88rem;color:#5A7268;line-height:1.65;">Each line item is embedded and matched against EU Taxonomy categories using RAG, grounded in regulation.</div>
</div>
<div class="gl-a6">
<div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:0.12em;color:#0F5132;margin-bottom:0.7rem;">03</div>
<div style="font-size:1.65rem;margin-bottom:0.65rem;">📋</div>
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1rem;font-weight:700;letter-spacing:-0.01em;color:#0D1B13;margin-bottom:0.4rem;">Financing Passport</div>
<div style="font-family:'Inter',sans-serif;font-size:0.88rem;color:#5A7268;line-height:1.65;">A scored, lender-ready ESG profile, shareable in one click. The lender opens, reviews, and decides.</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ── Role selector ──────────────────────────────────────────────────────────────
st.markdown("""
<p style="text-align:center;font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;color:#8FAF9E;margin:2.25rem 0 0.5rem;">Get started</p>
<p style="text-align:center;font-family:'Plus Jakarta Sans',sans-serif;font-size:1.5rem;font-weight:700;letter-spacing:-0.02em;color:#0D1B13;margin:0 0 1.75rem;">Who are you?</p>
""", unsafe_allow_html=True)

_, main, _ = st.columns([0.4, 5, 0.4])
with main:
    col_sme, gap, col_lender = st.columns([1, 0.1, 1])

    with col_sme:
        with st.container(border=True):
            st.markdown("""
<div class="gl-a5" style="padding:1.1rem 0.25rem 0.5rem;">
<div style="width:48px;height:48px;background:#EDF7F1;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:1rem;">🏢</div>
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;font-weight:700;letter-spacing:-0.02em;color:#0D1B13;margin-bottom:0.45rem;">SME</div>
<div style="font-family:'Inter',sans-serif;font-size:0.9rem;color:#5A7268;line-height:1.65;margin-bottom:1.25rem;">Upload invoices → get your Green Credit Score → share a Financing Passport with lenders in one click.</div>
</div>
""", unsafe_allow_html=True)
            if st.button("Start as SME →", type="primary", width="stretch"):
                st.switch_page("pages/1_SME_Upload.py")

    with col_lender:
        with st.container(border=True):
            st.markdown("""
<div class="gl-a6" style="padding:1.1rem 0.25rem 0.5rem;">
<div style="width:48px;height:48px;background:#EDF7F1;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;margin-bottom:1rem;">🏦</div>
<div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:1.15rem;font-weight:700;letter-spacing:-0.02em;color:#0D1B13;margin-bottom:0.45rem;">Lender</div>
<div style="font-family:'Inter',sans-serif;font-size:0.9rem;color:#5A7268;line-height:1.65;margin-bottom:1.25rem;">Open a shared Financing Passport → review the borrower's ESG profile → record your approve / decline decision.</div>
</div>
""", unsafe_allow_html=True)
            if st.button("Open a Passport →", type="primary", width="stretch"):
                st.switch_page("pages/4_Lender_View.py")
