"""Agregações utilizadas pelos gráficos e tabelas."""

import pandas as pd

from .constantes import (
    COLUNA_ESTADO,
    COLUNA_PRODUTO,
    COLUNA_RECEITA,
    COLUNA_VARIACAO,
    TOP_N,
)


def receita_mensal(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Ano_Mes", as_index=False)[COLUNA_RECEITA]
        .sum()
        .round(2)
    )


def receita_por_dia_semana(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["Dia_Semana", "Dia_Nome"], as_index=False)[COLUNA_RECEITA]
        .sum()
        .round(2)
        .sort_values("Dia_Semana")
    )


def receita_por_hora(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Hora", as_index=False)[COLUNA_RECEITA]
        .sum()
        .round(2)
    )


def ranking_produtos(df: pd.DataFrame, n: int = TOP_N) -> pd.Series:
    return (
        df.groupby(COLUNA_PRODUTO)[COLUNA_RECEITA]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .head(n)
    )


def ranking_sabores(df: pd.DataFrame, n: int = TOP_N) -> pd.Series:
    return (
        df.groupby(COLUNA_VARIACAO)[COLUNA_RECEITA]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .head(n)
    )


def receita_por_estado(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(COLUNA_ESTADO, as_index=False)[COLUNA_RECEITA]
        .sum()
        .round(2)
        .sort_values(COLUNA_RECEITA)
    )
