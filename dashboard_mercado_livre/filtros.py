"""Lógica de filtragem do DataFrame conforme seleção do usuário."""

import pandas as pd


def aplicar_filtros(
    df: pd.DataFrame,
    data_inicial,
    data_final,
    publicidades: list[str],
    estados: list[str],
    produtos: list[str],
    variacoes: list[str],
) -> pd.DataFrame:
    """Devolve um novo DataFrame contendo apenas as linhas que satisfazem os filtros."""
    mascara = (
        (df["Data da venda"] >= data_inicial)
        & (df["Data da venda"] <= data_final)
        & df["Venda por publicidade"].isin(publicidades)
        & df["Estado"].isin(estados)
        & df["Título do anúncio"].isin(produtos)
        & df["Variação"].isin(variacoes)
    )
    return df.loc[mascara]
