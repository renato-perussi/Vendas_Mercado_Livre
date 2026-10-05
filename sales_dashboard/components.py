"""Reusable Streamlit view components."""

import pandas as pd
import plotly.express as px
import streamlit as st

from . import aggregations, charts, formatting, metrics
from .constants import (
    ADS_NO,
    ADS_YES,
    COL_ADS,
    COL_FLAVOR,
    COL_HOUR,
    COL_PRODUCT,
    COL_REVENUE,
    COL_SALE_DATE,
    COL_STATE,
    COL_WEEKDAY_NAME,
    COL_YEAR_MONTH,
)
from .filters import FilterSelection

# Shared empty state message.
EMPTY_MESSAGE = 'No data for selected filters.'


def _ensure_template() -> None:
    """Register Plotly template lazily."""
    charts.register_template()


def render_kpis(df: pd.DataFrame) -> None:
    """Render the five headline KPI cards."""
    cols = st.columns(5, gap='small')
    cols[0].metric('Receita Total', formatting.format_currency(metrics.total_revenue(df)))
    cols[1].metric('Pedidos', metrics.order_count(df))
    cols[2].metric('Ticket Médio', formatting.format_currency(metrics.average_ticket(df)))
    cols[3].metric(
        'Receita Ads',
        formatting.format_currency(metrics.revenue_by_channel(df, ADS_YES)),
    )
    cols[4].metric(
        'Receita Orgânico',
        formatting.format_currency(metrics.revenue_by_channel(df, ADS_NO)),
    )


def render_sales_trend(df: pd.DataFrame) -> None:
    """Render monthly revenue line chart."""
    _ensure_template()
    if df.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown('### Evolução das Vendas')
    monthly = aggregations.monthly_revenue(df)
    fig = px.line(
        monthly,
        x=COL_YEAR_MONTH,
        y=COL_REVENUE,
        markers=True,
        labels={COL_YEAR_MONTH: 'Ano e Mês', COL_REVENUE: 'Receita (R$)'},
    )
    fig.update_traces(
        line={'color': charts.PRIMARY_COLOR, 'width': 3, 'shape': 'spline'},
        marker={
            'size': 8,
            'color': charts.PRIMARY_COLOR,
            'line': {'color': charts.PRIMARY_COLOR, 'width': 2},
        },
        fill='tozeroy',
        fillcolor='rgba(45, 50, 119, 0.08)',
    )
    st.plotly_chart(charts.apply_layout(fig), use_container_width=True)


def render_seasonality(df: pd.DataFrame) -> None:
    """Render weekday and hour seasonality bars."""
    _ensure_template()
    if df.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown('### Sazonalidade')
    left, right = st.columns(2, gap='medium')
    with left:
        by_day = aggregations.revenue_by_weekday(df)
        fig = px.bar(
            by_day,
            x=COL_WEEKDAY_NAME,
            y=COL_REVENUE,
            labels={COL_WEEKDAY_NAME: 'Dia da Semana', COL_REVENUE: 'Receita (R$)'},
        )
        fig.update_traces(marker_color=charts.PRIMARY_COLOR, marker_line_width=0)
        st.plotly_chart(charts.apply_layout(fig, height=320), use_container_width=True)
    with right:
        by_hour = aggregations.revenue_by_hour(df)
        fig = px.bar(
            by_hour,
            x=COL_HOUR,
            y=COL_REVENUE,
            labels={COL_HOUR: 'Hora do Dia', COL_REVENUE: 'Receita (R$)'},
        )
        fig.update_traces(marker_color=charts.PRIMARY_COLOR, marker_line_width=0)
        fig.update_yaxes(tickprefix='R$ ')
        st.plotly_chart(charts.apply_layout(fig, height=320), use_container_width=True)


def _ranking_with_bar(series: pd.Series, title: str) -> None:
    """Render a ranking table with a progress bar column."""
    if series.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown(f'###### {title}')
    st.dataframe(
        series,
        column_config={
            COL_REVENUE: st.column_config.ProgressColumn(
                COL_REVENUE,
                min_value=float(series.min()),
                max_value=float(series.max()),
                format='R$ %.2f',
                color=charts.PRIMARY_COLOR,
            )
        },
        height=360,
    )


def render_rankings(df: pd.DataFrame) -> None:
    """Render product and flavor rankings side by side."""
    _ensure_template()
    if df.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown('### Vendas por Produto')
    products = aggregations.product_ranking(df)
    flavors = aggregations.flavor_ranking(df)
    left, right = st.columns(2, gap='medium')
    with left:
        _ranking_with_bar(products, 'Receita por Produto')
    with right:
        _ranking_with_bar(flavors, 'Receita por Sabor')


def render_geography(df: pd.DataFrame) -> None:
    """Render state bar and share donut charts."""
    _ensure_template()
    if df.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown('### Vendas por Localidade')
    by_state = aggregations.revenue_by_state(df)
    left, right = st.columns(2, gap='medium')
    with left:
        fig = px.bar(
            by_state,
            x=COL_REVENUE,
            y=COL_STATE,
            orientation='h',
            labels={COL_REVENUE: 'Receita (R$)', COL_STATE: 'Estado'},
        )
        fig.update_traces(marker_color=charts.PRIMARY_COLOR, marker_line_width=0)
        fig.update_yaxes(tickprefix='')
        st.plotly_chart(charts.apply_layout(fig, height=380), use_container_width=True)
    with right:
        fig = px.pie(
            by_state,
            values=COL_REVENUE,
            names=COL_STATE,
            hole=0.55,
            color_discrete_sequence=charts.PALETTE,
        )
        fig.update_traces(textinfo='percent', textposition='inside')
        fig.update_layout(
            showlegend=True,
            legend={'orientation': 'h', 'yanchor': 'top', 'y': -0.1, 'xanchor': 'center', 'x': 0.5},
            margin={'t': 24, 'b': 80, 'l': 24, 'r': 24},
        )
        st.plotly_chart(charts.apply_layout(fig, height=380), use_container_width=True)


def render_full_table(df: pd.DataFrame) -> None:
    """Render the complete filtered dataset."""
    if df.empty:
        st.info(EMPTY_MESSAGE)
        return
    st.markdown('### Dataset Completo')
    st.dataframe(df, use_container_width=True, height=480)


def render_sidebar_filters(df: pd.DataFrame) -> FilterSelection:
    """Render sidebar widgets and return the selection."""
    min_date = df[COL_SALE_DATE].min()
    max_date = df[COL_SALE_DATE].max()
    start_date = st.date_input('Data Inicial', min_date)
    end_date = st.date_input('Data Final', max_date)
    # Clamp inverted range to avoid empty crashes.
    if end_date < start_date:
        end_date = start_date

    channels = sorted(df[COL_ADS].unique().tolist())
    selected_channels = st.multiselect('Venda por publicidade', channels, default=channels)

    states = sorted(df[COL_STATE].unique().tolist())
    selected_states = st.multiselect('Estados', states, default=states)

    products = sorted(df[COL_PRODUCT].unique().tolist())
    selected_products = st.multiselect('Produtos', products, default=products)

    flavors = sorted(df[COL_FLAVOR].unique().tolist())
    selected_flavors = st.multiselect('Sabores', flavors, default=flavors)

    return FilterSelection(
        start_date=start_date,
        end_date=end_date,
        channels=selected_channels,
        states=selected_states,
        products=selected_products,
        flavors=selected_flavors,
    )
