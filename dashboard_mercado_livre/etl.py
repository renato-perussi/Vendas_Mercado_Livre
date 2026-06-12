"""Pipeline ETL: leitura, transformação de tipos e derivação de colunas temporais."""

from pathlib import Path

import pandas as pd

from .constantes import (
    COLUNAS_ABSOLUTAS,
    COLUNAS_DATAS,
    COLUNAS_INTEIRO,
    COLUNAS_STRING,
    COLUNAS_TEMPORAIS_STR,
)


def _para_datetime(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    return df.assign(**{c: pd.to_datetime(df[c]) for c in colunas})


def _para_inteiro(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    return df.assign(**{c: df[c].astype("Int64") for c in colunas})


def _para_string(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    return df.assign(**{c: df[c].astype(str) for c in colunas})


def _para_absoluto(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    return df.assign(**{c: df[c].abs() for c in colunas})


def _adicionar_colunas_temporais(df: pd.DataFrame) -> pd.DataFrame:
    base = df["Data da venda"]
    caminho = df["Data a caminho completa"] - base
    entrega = df["Data de entrega completa"] - df["Data a caminho completa"]
    total = df["Data de entrega completa"] - base

    return df.assign(
        Ano_Mes=base.dt.to_period("M").astype(str),
        Ano=base.dt.year,
        Mes=base.dt.month,
        Dia=base.dt.day,
        Hora=base.dt.hour,
        Minuto=base.dt.minute,
        Dia_Semana=base.dt.weekday,
        Trimestre=base.dt.to_period("Q").astype(str).str[-2:],
        Dia_Nome=base.dt.day_name(),
        Mes_Nome=base.dt.month_name(),
        Dias_Delta_Caminho=caminho.dt.days,
        Horas_Delta_Caminho=caminho.dt.seconds // 3600,
        Minutos_Delta_Caminho=(caminho.dt.seconds % 3600) // 60,
        Dias_Delta_Entrega=entrega.dt.days,
        Horas_Delta_Entrega=entrega.dt.seconds // 3600,
        Minutos_Delta_Entrega=(entrega.dt.seconds % 3600) // 60,
        Dias_Delta_Total=total.dt.days,
        Horas_Delta_Total=total.dt.seconds // 3600,
        Minutos_Delta_Total=(total.dt.seconds % 3600) // 60,
    )


def carregar_vendas(caminho: Path) -> pd.DataFrame:
    """Lê o CSV bruto e devolve um DataFrame tratado e ordenado por data."""
    df = pd.read_csv(caminho)

    df = _para_datetime(df, COLUNAS_DATAS)
    df = _para_string(df, COLUNAS_STRING)
    df = _para_inteiro(df, COLUNAS_INTEIRO)
    df = _para_absoluto(df, COLUNAS_ABSOLUTAS)
    df = _adicionar_colunas_temporais(df)

    df["Data da venda"] = df["Data da venda"].dt.date
    df = _para_string(df, COLUNAS_TEMPORAIS_STR)

    return df.sort_values("Data da venda").reset_index(drop=True)
