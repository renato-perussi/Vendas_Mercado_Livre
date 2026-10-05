"""ETL pipeline tests."""

from sales_dashboard.constants import COL_SALE_DATE
from sales_dashboard.etl import load_sales


def test_load_sales_returns_sorted_frame(sample_csv):
    """Cleaned frame is sorted by sale date."""
    df = load_sales(sample_csv)
    assert not df.empty
    assert len(df) == 2
    dates = df[COL_SALE_DATE].tolist()
    assert dates == sorted(dates)


def test_load_sales_creates_temporal_columns(sample_csv):
    """Derived English temporal columns exist."""
    df = load_sales(sample_csv)
    for col in ('year_month', 'weekday', 'hour', 'weekday_name', 'month_name'):
        assert col in df.columns


def test_load_sales_applies_absolute_values(sample_csv):
    """Fee columns are converted to absolute values."""
    df = load_sales(sample_csv)
    assert (df['Tarifa de venda e impostos'] >= 0).all()
    assert (df['Tarifas de envio'] >= 0).all()


def test_load_sales_reads_real_dataset(project_data_path):
    """Real example dataset loads when present."""
    project_data_path.exists() or __import__('pytest').skip('example dataset missing')
    df = load_sales(project_data_path)
    assert not df.empty
    assert COL_SALE_DATE in df.columns
