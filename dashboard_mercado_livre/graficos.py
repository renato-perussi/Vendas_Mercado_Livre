"""Template Plotly e helpers visuais para os gráficos do dashboard."""

import plotly.graph_objects as go
import plotly.io as pio

# Paleta inspirada no Mercado Livre: tons de azul com cores de apoio.
PALETA = [
    "#2D3277",
    "#2D315E",
    "#282A45",
    "#868AC4",
    "#ADB0DE",
    "#DADCF7",
    "#D1D4FF",
    "#B8BCFF",
    "#9EA5FF",
    "#858DFF",
]

COR_PRIMARIA = "#2D3277"
COR_ACCENT = "#4F8AF7"
COR_TEXTO = "#1A1B2E"
COR_GRID = "#EAECEF"
COR_FUNDO = "#FFFFFF"

ALTURA_GRAFICO = 380


def _template_ml() -> dict:
    """Define o template padrão reaproveitável em todos os gráficos."""
    return {
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "colorway": PALETA,
            "font": {
                "family": "Inter, 'Segoe UI', system-ui, sans-serif",
                "color": COR_TEXTO,
                "size": 13,
            },
            "title": {
                "font": {"size": 16, "color": COR_PRIMARIA, "family": "Inter, sans-serif"},
                "x": 0.02,
                "xanchor": "left",
            },
            "xaxis": {
                "showgrid": True,
                "gridcolor": COR_GRID,
                "gridwidth": 1,
                "zeroline": False,
                "linecolor": COR_GRID,
                "tickfont": {"color": COR_TEXTO, "size": 12},
            },
            "yaxis": {
                "showgrid": True,
                "gridcolor": COR_GRID,
                "gridwidth": 1,
                "zeroline": False,
                "linecolor": COR_GRID,
                "tickfont": {"color": COR_TEXTO, "size": 12},
                "tickprefix": "R$ ",
                "separatethousands": True,
            },
            "legend": {
                "bgcolor": "rgba(0,0,0,0)",
                "font": {"color": COR_TEXTO, "size": 12},
                "orientation": "h",
                "yanchor": "bottom",
                "y": 1.02,
                "xanchor": "right",
                "x": 1,
            },
            "margin": {"l": 60, "r": 24, "t": 56, "b": 48},
            "hoverlabel": {
                "bgcolor": "white",
                "bordercolor": COR_PRIMARIA,
                "font": {"family": "Inter, sans-serif", "color": COR_TEXTO, "size": 13},
            },
        }
    }


def registrar_template() -> None:
    """Registra o template no Plotly (idempotente)."""
    pio.templates["ml_moderno"] = _template_ml()
    pio.templates.default = "ml_moderno"


def aplicar_layout(fig: go.Figure, *, altura: int = ALTURA_GRAFICO, **kwargs) -> go.Figure:
    """Ajustes finais compartilhados por todos os gráficos."""
    fig.update_layout(height=altura, **kwargs)
    return fig
