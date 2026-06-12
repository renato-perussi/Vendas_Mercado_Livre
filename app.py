"""Ponto de entrada do dashboard de Vendas do Mercado Livre."""

import streamlit as st

from dashboard_mercado_livre import (
    componentes,
    estilo,
)


@st.cache_data
def carregar_dados():
    from dashboard_mercado_livre import constantes, etl
    return etl.carregar_vendas(constantes.CAMINHO_DADOS)


st.set_page_config(
    page_title="Dashboard Mercado Livre",
    page_icon="📊",
    layout="wide",
)

estilo.injetar_css()

df = carregar_dados()


# Sidebar --------------------------------------------------------------------

with st.sidebar:
    estilo.exibir_logo_sidebar()
    st.divider()
    st.markdown("##### Filtros")

    data_min = df["Data da venda"].min()
    data_max = df["Data da venda"].max()

    data_inicial = st.date_input("Data Inicial", data_min)
    data_final = st.date_input("Data Final", data_max)

    publicidades = df["Venda por publicidade"].unique().tolist()
    publicidades_selecionadas = st.multiselect(
        "Venda por publicidade", publicidades, default=publicidades
    )

    estados = df["Estado"].unique().tolist()
    estados_selecionados = st.multiselect("Estados", estados, default=estados)

    produtos = df["Título do anúncio"].unique().tolist()
    produtos_selecionados = st.multiselect("Produtos", produtos, default=produtos)

    variacoes = df["Variação"].unique().tolist()
    variacoes_selecionadas = st.multiselect("Sabores", variacoes, default=variacoes)

    st.divider()
    st.caption("Developed by Renato Perussi")


# Aplicação dos filtros ------------------------------------------------------

from dashboard_mercado_livre import filtros

df_filtrado = filtros.aplicar_filtros(
    df,
    data_inicial=data_inicial,
    data_final=data_final,
    publicidades=publicidades_selecionadas,
    estados=estados_selecionados,
    produtos=produtos_selecionados,
    variacoes=variacoes_selecionadas,
)


# Cabeçalho ------------------------------------------------------------------

estilo.exibir_hero()


# Conteúdo -------------------------------------------------------------------

componentes.exibir_kpis(df_filtrado)
st.divider()

componentes.exibir_evolucao_vendas(df_filtrado)
componentes.exibir_sazonalidade(df_filtrado)
componentes.exibir_rankings(df_filtrado)
componentes.exibir_geografia(df_filtrado)
componentes.exibir_tabela_completa(df_filtrado)
