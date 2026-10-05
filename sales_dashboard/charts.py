"""Plotly theme and shared layout helpers."""

import plotly.graph_objects as go
import plotly.io as pio

# Mercado Livre inspired palette with support tones.
PALETTE = [
    '#2D3277',
    '#2D315E',
    '#282A45',
    '#868AC4',
    '#ADB0DE',
    '#DADCF7',
    '#D1D4FF',
    '#B8BCFF',
    '#9EA5FF',
    '#858DFF',
]

PRIMARY_COLOR = '#2D3277'
ACCENT_COLOR = '#4F8AF7'
TEXT_COLOR = '#1A1B2E'
GRID_COLOR = '#EAECEF'
BACKGROUND_COLOR = '#FFFFFF'

CHART_HEIGHT = 380


def _ml_template() -> dict:
    """Build the reusable default Plotly template."""
    return {
        'layout': {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'colorway': PALETTE,
            'font': {
                'family': "Inter, 'Segoe UI', system-ui, sans-serif",
                'color': TEXT_COLOR,
                'size': 13,
            },
            'title': {
                'font': {'size': 16, 'color': PRIMARY_COLOR, 'family': 'Inter, sans-serif'},
                'x': 0.02,
                'xanchor': 'left',
            },
            'xaxis': {
                'showgrid': True,
                'gridcolor': GRID_COLOR,
                'gridwidth': 1,
                'zeroline': False,
                'linecolor': GRID_COLOR,
                'tickfont': {'color': TEXT_COLOR, 'size': 12},
            },
            'yaxis': {
                'showgrid': True,
                'gridcolor': GRID_COLOR,
                'gridwidth': 1,
                'zeroline': False,
                'linecolor': GRID_COLOR,
                'tickfont': {'color': TEXT_COLOR, 'size': 12},
                'tickprefix': 'R$ ',
                'separatethousands': True,
            },
            'legend': {
                'bgcolor': 'rgba(0,0,0,0)',
                'font': {'color': TEXT_COLOR, 'size': 12},
                'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'right',
                'x': 1,
            },
            'margin': {'l': 60, 'r': 24, 't': 56, 'b': 48},
            'hoverlabel': {
                'bgcolor': 'white',
                'bordercolor': PRIMARY_COLOR,
                'font': {'family': 'Inter, sans-serif', 'color': TEXT_COLOR, 'size': 13},
            },
        }
    }


def register_template() -> None:
    """Register the template with Plotly (idempotent)."""
    pio.templates['ml_modern'] = _ml_template()
    pio.templates.default = 'ml_modern'


def apply_layout(fig: go.Figure, *, height: int = CHART_HEIGHT, **kwargs) -> go.Figure:
    """Apply shared height and extra layout tweaks."""
    fig.update_layout(height=height, **kwargs)
    return fig
