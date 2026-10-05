"""Aggregations backing charts and tables."""

import pandas as pd

from .constants import (
    COL_FLAVOR,
    COL_HOUR,
    COL_PRODUCT,
    COL_REVENUE,
    COL_STATE,
    COL_WEEKDAY,
    COL_WEEKDAY_NAME,
    COL_YEAR_MONTH,
    TOP_N,
)


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue summed per year-month."""
    return df.groupby(COL_YEAR_MONTH, as_index=False)[COL_REVENUE].sum().round(2)


def revenue_by_weekday(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue summed per weekday, ordered Monday first."""
    return (
        df.groupby([COL_WEEKDAY, COL_WEEKDAY_NAME], as_index=False)[COL_REVENUE]
        .sum()
        .round(2)
        .sort_values(COL_WEEKDAY)
    )


def revenue_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue summed per hour, sorted chronologically."""
    return df.groupby(COL_HOUR, as_index=False)[COL_REVENUE].sum().round(2).sort_values(COL_HOUR)


def product_ranking(df: pd.DataFrame, limit: int = TOP_N) -> pd.Series:
    """Top products by revenue."""
    return (
        df.groupby(COL_PRODUCT)[COL_REVENUE].sum().round(2).sort_values(ascending=False).head(limit)
    )


def flavor_ranking(df: pd.DataFrame, limit: int = TOP_N) -> pd.Series:
    """Top flavors by revenue."""
    return (
        df.groupby(COL_FLAVOR)[COL_REVENUE].sum().round(2).sort_values(ascending=False).head(limit)
    )


def revenue_by_state(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue summed per state, ascending for bar display."""
    return (
        df.groupby(COL_STATE, as_index=False)[COL_REVENUE].sum().round(2).sort_values(COL_REVENUE)
    )
