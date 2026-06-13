"""Componentes visuais reutilizáveis do dashboard."""

import pandas as pd
import plotly.express as px
import streamlit as st

from . import agregacoes, formatacao, graficos, metricas
from .constantes import (
    COLUNA_RECEITA,
    VALOR_ADS,
    VALOR_ORGANICO,
)


graficos.registrar_template()


def exibir_kpis(df: pd.DataFrame) -> None:
    col1, col2, col3, col4, col5 = st.columns(5, gap="small", vertical_alignment="top")

    col1.metric("Receita Total", formatacao.formatar_moeda(metricas.receita_total(df)))
    col2.metric("Pedidos", metricas.total_pedidos(df))
    col3.metric("Ticket Médio", formatacao.formatar_moeda(metricas.ticket_medio(df)))
    col4.metric(
        "Receita Ads",
        formatacao.formatar_moeda(metricas.receita_por_publicidade(df, VALOR_ADS)),
    )
    col5.metric(
        "Receita Orgânico",
        formatacao.formatar_moeda(metricas.receita_por_publicidade(df, VALOR_ORGANICO)),
    )


def exibir_evolucao_vendas(df: pd.DataFrame) -> None:
    st.markdown("### Evolução das Vendas")
    receita = agregacoes.receita_mensal(df)
    fig = px.line(
        receita,
        x="Ano_Mes",
        y=COLUNA_RECEITA,
        markers=True,
        labels={"Ano_Mes": "Ano e Mês", COLUNA_RECEITA: "Receita (R$)"},
    )
    fig.update_traces(
        line=dict(color=graficos.COR_PRIMARIA, width=3, shape="spline"),
        marker=dict(size=8, color=graficos.COR_PRIMARIA, line=dict(color=graficos.COR_PRIMARIA, width=2)),
        fill="tozeroy",
        fillcolor="rgba(45, 50, 119, 0.08)",
    )
    st.plotly_chart(graficos.aplicar_layout(fig), use_container_width=True)


def exibir_sazonalidade(df: pd.DataFrame) -> None:
    st.markdown("### Sazonalidade")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        receita_dia = agregacoes.receita_por_dia_semana(df)
        fig = px.bar(
            receita_dia,
            x="Dia_Nome",
            y=COLUNA_RECEITA,
            labels={"Dia_Nome": "Dia da Semana", COLUNA_RECEITA: "Receita (R$)"},
        )
        fig.update_traces(marker_color=graficos.COR_PRIMARIA, marker_line_width=0)
        st.plotly_chart(graficos.aplicar_layout(fig, altura=320), use_container_width=True)

    with col2:
        receita_hora = agregacoes.receita_por_hora(df)
        fig = px.bar(
            receita_hora,
            x="Hora",
            y=COLUNA_RECEITA,
            labels={"Hora": "Hora do Dia", COLUNA_RECEITA: "Receita (R$)"},
        )
        fig.update_traces(marker_color=graficos.COR_PRIMARIA, marker_line_width=0)
        fig.update_yaxes(tickprefix="R$ ")
        st.plotly_chart(graficos.aplicar_layout(fig, altura=320), use_container_width=True)


def _ranking_com_barra(series: pd.Series, titulo: str) -> None:
    st.markdown(f"###### {titulo}")
    st.dataframe(
        series,
        column_config={
            COLUNA_RECEITA: st.column_config.ProgressColumn(
                COLUNA_RECEITA,
                min_value=series.min(),
                max_value=series.max(),
                format="R$ %.2f",
                color=graficos.COR_PRIMARIA,
            )
        },
        height=360,
    )


def exibir_rankings(df: pd.DataFrame) -> None:
    st.markdown("### Vendas por Produto")

    produtos_ranking = agregacoes.ranking_produtos(df)
    sabores_ranking = agregacoes.ranking_sabores(df)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        _ranking_com_barra(produtos_ranking, "Receita por Produto")
    with col2:
        _ranking_com_barra(sabores_ranking, "Receita por Sabor")


def exibir_geografia(df: pd.DataFrame) -> None:
    st.markdown("### Vendas por Localidade")

    receita_estados = agregacoes.receita_por_estado(df)
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        fig = px.bar(
            receita_estados,
            x=COLUNA_RECEITA,
            y="Estado",
            orientation="h",
            labels={COLUNA_RECEITA: "Receita (R$)", "Estado": "Estado"},
        )
        fig.update_traces(marker_color=graficos.COR_PRIMARIA, marker_line_width=0)
        fig.update_yaxes(tickprefix="")
        st.plotly_chart(graficos.aplicar_layout(fig, altura=380), use_container_width=True)

    with col2:
        fig = px.pie(
            receita_estados,
            values=COLUNA_RECEITA,
            names="Estado",
            hole=0.55,
            color_discrete_sequence=graficos.PALETA,
        )
        fig.update_traces(textinfo="percent", textposition="inside")
        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.1,
                xanchor="center",
                x=0.5,
            ),
            margin=dict(t=24, b=80, l=24, r=24),
        )
        st.plotly_chart(graficos.aplicar_layout(fig, altura=380), use_container_width=True)


def exibir_tabela_completa(df: pd.DataFrame) -> None:
    st.markdown("### Dataset Completo")
    st.dataframe(df, use_container_width=True, height=480)
