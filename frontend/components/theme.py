"""
Call page_setup() as the very first line of every page.
It runs st.set_page_config (which Streamlit requires before any other call)
and injects the Google Fonts CSS + global UI polish.
"""

import streamlit as st

_FONTS_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,300..800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
    /* ── Typography ────────────────────────────────────────────────── */
    h1, h2, h3, h4, h5, h6,
    [data-testid="stHeading"] * {
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    html, body, [data-testid], p, span, div, label, li, input {
        font-family: 'Inter', system-ui, sans-serif !important;
    }

    /* ── Layout ────────────────────────────────────────────────────── */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 4rem !important;
    }

    /* ── Cards (st.container border=True) ──────────────────────────── */
    div[data-testid="stVerticalBlockWithBorder"] {
        border-radius: 12px !important;
        border-color: #D8EAE0 !important;
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease,
                    border-color 0.2s ease !important;
    }

    div[data-testid="stVerticalBlockWithBorder"]:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 14px 40px rgba(15, 81, 50, 0.13) !important;
        border-color: #0F5132 !important;
    }

    /* ── Primary buttons ───────────────────────────────────────────── */
    [data-testid="stBaseButton-primary"] {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.01em !important;
        transition: filter 0.15s ease, transform 0.15s ease !important;
    }

    [data-testid="stBaseButton-primary"]:hover {
        filter: brightness(1.12) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Secondary / ghost buttons ─────────────────────────────────── */
    [data-testid="stBaseButton-secondary"] {
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        transition: border-color 0.15s ease, color 0.15s ease !important;
    }

    /* ── Dividers ──────────────────────────────────────────────────── */
    hr {
        border-color: #D8EAE0 !important;
    }
</style>
"""


def page_setup(title: str = "GreenLedger", layout: str = "wide") -> None:
    """Configure the page and inject typography. Must be the first Streamlit call on every page."""
    st.set_page_config(
        page_title=title,
        page_icon="🌿",
        layout=layout,
    )
    st.markdown(_FONTS_CSS, unsafe_allow_html=True)
