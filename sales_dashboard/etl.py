"""ETL pipeline: load, coerce types and derive temporal columns."""

from pathlib import Path

import pandas as pd

from .constants import (
    ABS_COLUMNS,
    COL_SALE_DATE,
    DATE_COLUMNS,
    INT_COLUMNS,
    STRING_COLUMNS,
    TEMPORAL_STR_COLUMNS,
)


def _to_datetime(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce columns to datetime."""
    return df.assign(**{c: pd.to_datetime(df[c]) for c in columns})


def _to_nullable_int(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce columns to nullable integer."""
    return df.assign(**{c: df[c].astype('Int64') for c in columns})


def _to_string(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Coerce columns to string."""
    return df.assign(**{c: df[c].astype(str) for c in columns})


def _to_absolute(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Apply abs to fee and refund columns."""
    return df.assign(**{c: df[c].abs() for c in columns})


def _add_temporal_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Derive English temporal and logistics delta columns."""
    base = df['Data da venda']
    transit = df['Data a caminho completa'] - base
    delivery = df['Data de entrega completa'] - df['Data a caminho completa']
    total = df['Data de entrega completa'] - base
    return df.assign(
        year_month=base.dt.to_period('M').astype(str),
        year=base.dt.year,
        month=base.dt.month,
        day=base.dt.day,
        hour=base.dt.hour,
        minute=base.dt.minute,
        weekday=base.dt.weekday,
        quarter=base.dt.quarter,
        weekday_name=base.dt.day_name(),
        month_name=base.dt.month_name(),
        transit_days=transit.dt.days,
        transit_hours=transit.dt.seconds // 3600,
        transit_minutes=(transit.dt.seconds % 3600) // 60,
        delivery_days=delivery.dt.days,
        delivery_hours=delivery.dt.seconds // 3600,
        delivery_minutes=(delivery.dt.seconds % 3600) // 60,
        total_days=total.dt.days,
        total_hours=total.dt.seconds // 3600,
        total_minutes=(total.dt.seconds % 3600) // 60,
    )


def load_sales(path: Path) -> pd.DataFrame:
    """Load raw CSV and return a cleaned frame sorted by sale date."""
    df = pd.read_csv(path)
    df = _to_datetime(df, DATE_COLUMNS)
    df = _to_string(df, STRING_COLUMNS)
    df = _to_nullable_int(df, INT_COLUMNS)
    df = _to_absolute(df, ABS_COLUMNS)
    df = _add_temporal_columns(df)
    df[COL_SALE_DATE] = df[COL_SALE_DATE].dt.date
    df = _to_string(df, TEMPORAL_STR_COLUMNS)
    return df.sort_values(COL_SALE_DATE).reset_index(drop=True)
