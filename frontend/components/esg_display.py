"""Shared rendering for an ESGProfile, used by both the SME dashboard and the
Financing Passport screen (SME + lender views) so the two stay visually consistent.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st

# (text color, background color) per data_quality tier; does not affect the score itself,
# just how the confidence badge is colored.
_QUALITY_COLORS = {
    "High": ("#0F5132", "#EAF7EF"),
    "Medium": ("#92670B", "#FFF6E0"),
    "Low": ("#9B2C2C", "#FDEDED"),
}


def render_quality_badge(data_quality: dict | None) -> None:
    """Data-quality/confidence badge, shown alongside the Green Credit Score, never changes it."""
    if not data_quality:
        return
    tier = data_quality.get("tier", "Unknown")
    confidence = data_quality.get("confidence_pct")
    basis = data_quality.get("basis", "")
    text_color, bg_color = _QUALITY_COLORS.get(tier, ("#5A7268", "#F4F7F5"))
    conf_text = f" · {confidence:.0f}% confidence" if confidence is not None else ""
    st.markdown(
        f"""<div style="display:inline-flex;align-items:center;gap:0.4rem;background:{bg_color};
        border:1px solid {text_color}33;border-radius:100px;padding:0.3rem 0.85rem;
        font-family:'Inter',sans-serif;font-size:0.82rem;font-weight:600;color:{text_color};margin:0.4rem 0 0.3rem;">
        Data quality: {tier}{conf_text}</div>""",
        unsafe_allow_html=True,
    )
    if basis:
        st.caption(basis)


def render_score_header(esg_profile: dict) -> None:
    """Headline Green Credit Score, procurement sustainability score, sector benchmark, and data quality."""
    with st.container(border=True):
        benchmark = esg_profile.get("sector_benchmark") or {}
        median = benchmark.get("median_green_credit_score")

        col1, col2, col3 = st.columns(3)
        with col1:
            delta = None
            if median is not None:
                delta = f"{esg_profile['green_credit_score'] - median:+.0f} vs. sector"
            st.metric("Green Credit Score", f"{esg_profile['green_credit_score']:.0f} / 100", delta=delta)
        with col2:
            st.metric("Procurement Sustainability", f"{esg_profile['procurement_sustainability_score']:.0f} / 100")
        with col3:
            if median is not None:
                st.metric(f"Sector Benchmark ({benchmark.get('sector', 'n/a')})", f"{median:.0f} / 100")

        render_quality_badge(esg_profile.get("data_quality"))


def render_dimension_chart(dimension_scores: dict) -> None:
    """Bar chart of spend share per EU Taxonomy objective."""
    with st.container(border=True):
        if not dimension_scores:
            st.caption("No EU Taxonomy dimension data available.")
            return

        df = pd.DataFrame(
            {"Spend share (%)": {k: round(v * 100, 1) for k, v in dimension_scores.items()}}
        )
        st.bar_chart(df, horizontal=True)


def render_classified_items_table(classified_line_items: list[dict]) -> None:
    """Table of invoice line items with their matched EU Taxonomy category and rationale."""
    with st.container(border=True):
        if not classified_line_items:
            st.caption("No line items to show.")
            return

        rows = []
        for item in classified_line_items:
            rows.append(
                {
                    "Supplier": item.get("supplier"),
                    "Description": item.get("description"),
                    "Amount (€)": item.get("amount"),
                    "EU Taxonomy category": item.get("taxonomy_category") or "Not classified",
                    "Objective": item.get("taxonomy_objective") or "—",
                    "Similarity": item.get("similarity_score"),
                    "Rationale": item.get("rationale") or "—",
                }
            )

        df = pd.DataFrame(rows).sort_values("Amount (€)", ascending=False)
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
            column_config={
                "Amount (€)": st.column_config.NumberColumn(format="€%.2f"),
                "Similarity": st.column_config.ProgressColumn(min_value=0.0, max_value=1.0, format="%.2f"),
            },
        )


def render_financial_health(financial_health: dict) -> None:
    """Financial-health metrics derived alongside the ESG profile (see passport/assembler.py)."""
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total spend", f"€{financial_health.get('total_spend_eur', 0):,.2f}")
        with col2:
            st.metric("Classified green spend", f"€{financial_health.get('classified_green_spend_eur', 0):,.2f}")
        with col3:
            st.metric("Green spend share", f"{financial_health.get('green_spend_share', 0) * 100:.1f}%")
