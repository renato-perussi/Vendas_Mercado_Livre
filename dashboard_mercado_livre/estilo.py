"""Estilos globais, CSS injetado e hero section do dashboard."""

import base64
from pathlib import Path

import streamlit as st

from .constantes import CAMINHO_LOGO


def _imagem_para_data_uri(caminho: Path) -> str:
    """Lê um arquivo de imagem e devolve um data URI base64."""
    if not caminho.exists():
        return ""
    mime = "image/png" if caminho.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(caminho.read_bytes()).decode()}"

CSS_GLOBAL = """
<style>
/* ---------- Tipografia e cores globais ---------- */
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

/* ---------- Títulos de seção ---------- */
h2, h3, .stMarkdown h2, .stMarkdown h3 {
    color: #2D3277 !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em;
}

/* ---------- Cards de KPI (st.metric) ---------- */
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

/* ---------- Divisores ---------- */
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


def injetar_css() -> None:
    """Aplica os estilos globais do dashboard."""
    st.markdown(CSS_GLOBAL, unsafe_allow_html=True)


def exibir_logo_sidebar(largura: int = 180) -> None:
    """Renderiza o logo do Mercado Livre no topo do sidebar."""
    logo_src = _imagem_para_data_uri(CAMINHO_LOGO)
    st.markdown(
        f"""
        <div class="ml-sidebar-logo">
            <img src="{logo_src}" width="{largura}" alt="Mercado Livre">
        </div>
        """,
        unsafe_allow_html=True,
    )


def exibir_hero(subtitulo: str = "Análise de vendas e desempenho comercial") -> None:
    """Renderiza o cabeçalho com título e subtítulo."""
    st.markdown(
        f"""
        <div class="ml-hero">
            <div class="ml-hero__text">
                <h1>Dashboard de Vendas</h1>
                <p>{subtitulo}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
