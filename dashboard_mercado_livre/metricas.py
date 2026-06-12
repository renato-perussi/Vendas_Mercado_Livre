"""Cálculo das métricas de negócio."""

import pandas as pd

from .constantes import (
    COLUNA_NUMERO_VENDA,
    COLUNA_PUBLICIDADE,
    COLUNA_RECEITA,
)


def receita_total(df: pd.DataFrame) -> float:
    return round(df[COLUNA_RECEITA].sum(), 2)


def total_pedidos(df: pd.DataFrame) -> int:
    return df[COLUNA_NUMERO_VENDA].nunique()


def ticket_medio(df: pd.DataFrame) -> float:
    pedidos = total_pedidos(df)
    if pedidos == 0:
        return 0.0
    return round(receita_total(df) / pedidos, 2)


def receita_por_publicidade(df: pd.DataFrame, valor: str) -> float:
    mascara = df[COLUNA_PUBLICIDADE] == valor
    return round(df.loc[mascara, COLUNA_RECEITA].sum(), 2)
