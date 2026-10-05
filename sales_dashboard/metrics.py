"""Business metrics over the sales frame."""

import pandas as pd

from .constants import COL_ADS, COL_ORDER_ID, COL_REVENUE


def total_revenue(df: pd.DataFrame) -> float:
    """Sum product revenue rounded to cents."""
    return round(float(df[COL_REVENUE].sum()), 2)


def order_count(df: pd.DataFrame) -> int:
    """Count distinct orders."""
    return int(df[COL_ORDER_ID].nunique())


def average_ticket(df: pd.DataFrame) -> float:
    """Mean revenue per order, zero when empty."""
    orders = order_count(df)
    if orders == 0:
        return 0.0
    return round(total_revenue(df) / orders, 2)


def revenue_by_channel(df: pd.DataFrame, value: str) -> float:
    """Sum revenue filtered by advertising flag."""
    mask = df[COL_ADS] == value
    return round(float(df.loc[mask, COL_REVENUE].sum()), 2)
