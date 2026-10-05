"""Global styles, injected CSS and hero header."""

import base64
import html
from pathlib import Path

import streamlit as st

from .constants import LOGO_PATH

GLOBAL_CSS = """
<style>
/* ---------- Global typography ---------- */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.stApp header[data-testid="stHeader"] {
    background: rgba(250, 250, 251, 0.85);
    backdrop-filter: blur(8px);
    border-bottom: 1px solid #EAECEF;
}

/* ---------- Hero section ---------- */
.ml-hero {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 0.5rem 0;
    margin: 0.25rem 0 1rem 0;
}
.ml-hero__logo {
    flex: 0 0 auto;
    background: #FFFFFF;
    border-radius: 14px;
    padding: 10px 14px;
    box-shadow: 0 2px 8px rgba(45, 50, 119, 0.08);
}
.ml-hero__logo img {
    display: block;
}
.ml-hero__text h1 {
    margin: 0 0 -0.1rem 0;
    line-height: 1.1;
    font-size: 2.1rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #2D3277 0%, #2D3277 40%, #4F8AF7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
}
.ml-hero__text p {
    margin: 0;
    line-height: 1.2;
    color: #5A5F7A;
    font-size: 1rem;
    font-weight: 400;
}

/* ---------- Section titles ---------- */
h2, h3, .stMarkdown h2, .stMarkdown h3 {
    color: #2D3277 !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* ---------- KPI cards ---------- */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #EAECEF;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    box-shadow: 0 1px 2px rgba(45, 50, 119, 0.04);
    transition: transform 120ms ease, box-shadow 120ms ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 14px rgba(45, 50, 119, 0.08);
}
div[data-testid="stMetric"] label {
    color: #5A5F7A !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #2D3277 !important;
    font-weight: 700 !important;
    font-size: 1.55rem !important;
}

/* ---------- Dataframes ---------- */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #EAECEF;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #EAECEF;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #2D3277 !important;
}

.ml-sidebar-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0.25rem 0 0.75rem 0;
}
.ml-sidebar-logo img {
    display: block;
}

/* ---------- Dividers ---------- */
hr {
    border: none;
    border-top: 1px solid #EAECEF;
    margin: 1.25rem 0;
}

/* ---------- Plotly charts ---------- */
.js-plotly-plot .plotly .modebar {
    background: transparent !important;
}
</style>
"""


def _image_to_data_uri(path: Path) -> str:
    """Read an image file and return a base64 data URI."""
    if not path.exists():
        return ''
    mime = 'image/png' if path.suffix.lower() == '.png' else 'image/jpeg'
    encoded = base64.b64encode(path.read_bytes()).decode()
    return f'data:{mime};base64,{encoded}'


def inject_css() -> None:
    """Apply global dashboard styles."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def render_sidebar_logo(width: int = 180) -> None:
    """Render the Mercado Livre logo at the top of the sidebar."""
    logo_src = _image_to_data_uri(LOGO_PATH)
    st.markdown(
        f"""
        <div class="ml-sidebar-logo">
            <img src="{logo_src}" width="{width}" alt="Mercado Livre">
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_hero(subtitle: str = 'Análise de vendas e desempenho comercial') -> None:
    """Render the header with title and subtitle."""
    safe_subtitle = html.escape(subtitle)
    st.markdown(
        f"""
        <div class="ml-hero">
            <div class="ml-hero__text">
                <h1>Dashboard de Vendas</h1>
                <p>{safe_subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
