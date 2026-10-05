"""Aggregation tests."""

import pandas as pd

from sales_dashboard import aggregations


def test_monthly_revenue_groups(sample_df):
    """Monthly totals match expected values."""
    result = aggregations.monthly_revenue(sample_df)
    as_dict = dict(zip(result['year_month'], result['Receita por produtos (BRL)'], strict=False))
    assert as_dict == {'2023-01': 300.0, '2023-02': 200.0}


def test_revenue_by_weekday_sorted(sample_df):
    """Weekday frame is ordered by weekday code."""
    result = aggregations.revenue_by_weekday(sample_df)
    assert result['weekday'].tolist() == sorted(result['weekday'].tolist())
    assert result['Receita por produtos (BRL)'].sum() == 500.0


def test_revenue_by_hour_groups(sample_df):
    """Hour totals aggregate repeated hours."""
    result = aggregations.revenue_by_hour(sample_df)
    as_dict = dict(zip(result['hour'], result['Receita por produtos (BRL)'], strict=False))
    assert as_dict[10] == 150.0


def test_revenue_by_hour_chronological_order(sample_df):
    """Hour frame is sorted numerically, not lexicographically."""
    result = aggregations.revenue_by_hour(sample_df)
    hours = result['hour'].tolist()
    assert hours == sorted(hours)
    # Regression covers lexicographic trap with 0, 1, 10, 11.
    assert hours == sorted(hours, key=int)


def test_revenue_by_hour_lexicographic_trap():
    """Hours 0, 1, 10, 11 stay chronological."""
    df = pd.DataFrame(
        {
            'hour': [11, 0, 10, 1, 10],
            'Receita por produtos (BRL)': [10.0, 20.0, 30.0, 40.0, 50.0],
        }
    )
    result = aggregations.revenue_by_hour(df)
    assert result['hour'].tolist() == [0, 1, 10, 11]


def test_product_ranking_orders_desc(sample_df):
    """Top product is Prod B with 200 revenue."""
    ranking = aggregations.product_ranking(sample_df)
    assert ranking.index[0] == 'Prod B'
    assert ranking.iloc[0] == 200.0


def test_flavor_ranking_sums(sample_df):
    """Sweet flavor sums three rows."""
    ranking = aggregations.flavor_ranking(sample_df)
    assert ranking['Sweet'] == 300.0


def test_revenue_by_state_ascending(sample_df):
    """State frame is ascending by revenue."""
    result = aggregations.revenue_by_state(sample_df)
    values = result['Receita por produtos (BRL)'].tolist()
    assert values == sorted(values)
