"""
Call page_setup() as the very first line of every page.
It runs st.set_page_config (must come before any other Streamlit call)
and injects the global typography, animation, and component CSS.
"""

import streamlit as st

_GLOBAL_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300..800;1,300..800&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ── Entrance animations ─────────────────────────────────────────── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: translateY(0);    }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}

/* Staggered utility classes — use gl-a1 … gl-a6 in HTML */
.gl-a1 { animation: fadeUp 0.55s 0.05s ease both; }
.gl-a2 { animation: fadeUp 0.55s 0.17s ease both; }
.gl-a3 { animation: fadeUp 0.55s 0.29s ease both; }
.gl-a4 { animation: fadeUp 0.55s 0.41s ease both; }
.gl-a5 { animation: fadeUp 0.55s 0.53s ease both; }
.gl-a6 { animation: fadeUp 0.55s 0.65s ease both; }

/* ── Typography ──────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6,
[data-testid="stHeading"] * {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    font-weight: 700;
    letter-spacing: -0.022em;
}

html, body, p, span, li, label, input, textarea, div {
    font-family: 'Inter', system-ui, sans-serif !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #FAFCFB !important;
    border-right: 1px solid #E4EDE8 !important;
}

/* ── Cards (st.container border=True) ───────────────────────────── */
div[data-testid="stVerticalBlockWithBorder"] {
    border-radius: 14px !important;
    border-color: #E2EDE7 !important;
    transition: transform 0.22s ease,
                box-shadow 0.22s ease,
                border-color 0.22s ease !important;
}

div[data-testid="stVerticalBlockWithBorder"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 16px 48px rgba(15, 81, 50, 0.13) !important;
    border-color: #0F5132 !important;
}

/* ── Primary buttons ─────────────────────────────────────────────── */
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

/* ── Secondary buttons ───────────────────────────────────────────── */
[data-testid="stBaseButton-secondary"] {
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}

/* ── Inputs ──────────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    border-radius: 8px !important;
    border-color: #D4E3DA !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Dividers ────────────────────────────────────────────────────── */
hr { border-color: #E2EDE7 !important; }
</style>
"""


def page_setup(title: str = "GreenLedger", layout: str = "wide") -> None:
    """Configure the page and inject global CSS. Must be the first Streamlit call on every page."""
    st.set_page_config(
        page_title=title,
        page_icon="🌿",
        layout=layout,
    )
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)
