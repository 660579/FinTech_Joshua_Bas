"""
Call page_setup() as the very first line of every page.
It runs st.set_page_config (must come before any other Streamlit call)
and injects the global typography, animation, and component CSS.
"""

import re
from pathlib import Path

import streamlit as st

_LOGO_SVG_PATH = Path(__file__).resolve().parent.parent / "assets" / "logo.svg"


def _load_logo_svg() -> str:
    return _LOGO_SVG_PATH.read_text(encoding="utf-8")


def logo_html(height: int = 26, color: str = "#0D1B13", accent: str = "#0F5132") -> str:
    """Build the wordmark HTML as a string (no Streamlit call) so a page can embed it
    inside its own larger markdown block, e.g. a custom hero, without splitting an
    HTML tag across two separate st.markdown calls, which Streamlit renders as separate,
    non-nested DOM blocks (an open tag in one call cannot contain content from another).
    """
    svg = re.sub(r'height="\d+"', f'height="{height}"', _load_logo_svg(), count=1)
    return f'<div style="display:inline-flex;color:{color};--gl-accent:{accent};line-height:0;">{svg}</div>'


def render_logo(height: int = 26, color: str = "#0D1B13", accent: str = "#0F5132") -> None:
    """Render the GreenLedger wordmark (leaf mark + text) as a standalone element.

    color/accent adapt the SVG (via currentColor / a CSS var) to light or dark
    backgrounds, e.g. dark text on the in-platform header vs. white on the dark hero.
    """
    st.markdown(logo_html(height, color, accent), unsafe_allow_html=True)

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

/* Staggered utility classes: use gl-a1 … gl-a6 in HTML */
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

/* Material icon glyphs (upload button icon, sidebar collapse arrows, etc.) render as
   literal ligature text (e.g. "upload") if their own icon font is overridden above. */
[data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
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


def page_setup(title: str = "GreenLedger", layout: str = "wide", show_header: bool = True) -> None:
    """Configure the page, inject global CSS, and render the persistent logo header.

    Must be the first Streamlit call on every page. show_header=False lets a page (e.g.
    the landing page, which has its own prominent hero logo) skip the slim top header.
    """
    st.set_page_config(
        page_title=title,
        page_icon="🌿",
        layout=layout,
    )
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)

    if show_header:
        st.markdown(
            '<div style="display:flex;align-items:center;padding:0.6rem 0 0.9rem;'
            f'border-bottom:1px solid #E4EDE8;margin-bottom:1.2rem;">{logo_html(height=24)}</div>',
            unsafe_allow_html=True,
        )
