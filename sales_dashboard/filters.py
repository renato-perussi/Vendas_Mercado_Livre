"""Row filtering based on user selections."""

from dataclasses import dataclass
from datetime import date

import pandas as pd

from .constants import (
    COL_ADS,
    COL_FLAVOR,
    COL_PRODUCT,
    COL_SALE_DATE,
    COL_STATE,
)


@dataclass(frozen=True)
class FilterSelection:
    """Immutable sidebar filter values."""

    start_date: date
    end_date: date
    channels: list[str]
    states: list[str]
    products: list[str]
    flavors: list[str]


def apply_filters(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    channels: list[str],
    states: list[str],
    products: list[str],
    flavors: list[str],
) -> pd.DataFrame:
    """Return rows matching every selected filter."""
    mask = (
        (df[COL_SALE_DATE] >= start_date)
        & (df[COL_SALE_DATE] <= end_date)
        & df[COL_ADS].isin(channels)
        & df[COL_STATE].isin(states)
        & df[COL_PRODUCT].isin(products)
        & df[COL_FLAVOR].isin(flavors)
    )
    return df.loc[mask].reset_index(drop=True)


def apply_selection(df: pd.DataFrame, selection: FilterSelection) -> pd.DataFrame:
    """Apply a FilterSelection object."""
    return apply_filters(
        df,
        start_date=selection.start_date,
        end_date=selection.end_date,
        channels=selection.channels,
        states=selection.states,
        products=selection.products,
        flavors=selection.flavors,
    )
