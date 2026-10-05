"""Component empty state tests."""

from unittest.mock import patch

import pandas as pd

from sales_dashboard import components


def _empty_df() -> pd.DataFrame:
    """Build an empty frame with expected columns."""
    return pd.DataFrame(
        {
            'Receita por produtos (BRL)': pd.Series(dtype=float),
            'Título do anúncio': pd.Series(dtype=str),
            'Variação': pd.Series(dtype=str),
            'Estado': pd.Series(dtype=str),
            'year_month': pd.Series(dtype=str),
            'hour': pd.Series(dtype=int),
            'weekday': pd.Series(dtype=int),
            'weekday_name': pd.Series(dtype=str),
            'Data da venda': pd.Series(dtype=object),
        }
    )


def test_ranking_with_bar_empty_shows_info():
    """Empty ranking shows info without crashing."""
    series = pd.Series(dtype=float)
    with (
        patch.object(components.st, 'info') as info,
        patch.object(components.st, 'markdown'),
        patch.object(components.st, 'dataframe'),
    ):
        components._ranking_with_bar(series, 'Title')
    info.assert_called_once_with(components.EMPTY_MESSAGE)


def test_render_sales_trend_empty_shows_info():
    """Empty trend shows info without crashing."""
    with (
        patch.object(components.st, 'info') as info,
        patch.object(components.st, 'markdown'),
        patch.object(components.st, 'plotly_chart'),
    ):
        components.render_sales_trend(_empty_df())
    info.assert_called_once_with(components.EMPTY_MESSAGE)


def test_render_seasonality_empty_shows_info():
    """Empty seasonality shows info without crashing."""
    with (
        patch.object(components.st, 'info') as info,
        patch.object(components.st, 'markdown'),
    ):
        components.render_seasonality(_empty_df())
    info.assert_called_once_with(components.EMPTY_MESSAGE)


def test_render_geography_empty_shows_info():
    """Empty geography shows info without crashing."""
    with (
        patch.object(components.st, 'info') as info,
        patch.object(components.st, 'markdown'),
    ):
        components.render_geography(_empty_df())
    info.assert_called_once_with(components.EMPTY_MESSAGE)
