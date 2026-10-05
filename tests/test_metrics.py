"""Business metrics tests."""

import pandas as pd

from sales_dashboard import metrics


def test_total_revenue_sums_column(sample_df):
    """Revenue total matches manual sum."""
    assert metrics.total_revenue(sample_df) == 500.0


def test_order_count_counts_distinct(sample_df):
    """Distinct order ids are counted."""
    assert metrics.order_count(sample_df) == 3


def test_average_ticket_divides_revenue(sample_df):
    """Ticket equals revenue divided by orders."""
    assert metrics.average_ticket(sample_df) == round(500.0 / 3, 2)


def test_average_ticket_empty_returns_zero():
    """Empty frame yields zero ticket."""
    empty = pd.DataFrame({'Receita por produtos (BRL)': [], 'N.º de venda': []})
    assert metrics.average_ticket(empty) == 0.0


def test_revenue_by_channel_splits_ads(sample_df):
    """Ads and organic revenue split correctly."""
    assert metrics.revenue_by_channel(sample_df, 'Sim') == 150.0
    assert metrics.revenue_by_channel(sample_df, 'Não') == 350.0
