"""Mercado Livre sales dashboard entrypoint."""

import pandas as pd
import streamlit as st

from sales_dashboard import components, filters, styles
from sales_dashboard.constants import DATA_PATH
from sales_dashboard.etl import load_sales


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load and cache the cleaned sales frame."""
    return load_sales(DATA_PATH)


def main() -> None:
    """Compose sidebar, filters and dashboard sections."""
    st.set_page_config(
        page_title='Dashboard Mercado Livre',
        page_icon='📊',
        layout='wide',
    )
    styles.inject_css()

    df = load_data()

    with st.sidebar:
        styles.render_sidebar_logo()
        st.divider()
        st.markdown('##### Filtros')
        selection = components.render_sidebar_filters(df)
        st.divider()
        st.caption('Developed by Renato Perussi')

    filtered = filters.apply_selection(df, selection)

    styles.render_hero()
    components.render_kpis(filtered)
    # Central empty guard prevents chart crashes.
    if filtered.empty:
        st.info('No data for selected filters.')
        return
    st.divider()
    components.render_sales_trend(filtered)
    components.render_seasonality(filtered)
    components.render_rankings(filtered)
    components.render_geography(filtered)
    components.render_full_table(filtered)


if __name__ == '__main__':
    main()
