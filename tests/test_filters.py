"""Filter logic tests."""

from datetime import date

from sales_dashboard.filters import FilterSelection, apply_filters, apply_selection


def test_apply_filters_date_range(sample_df):
    """Only January rows survive narrow range."""
    result = apply_filters(
        sample_df,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 1, 31),
        channels=['Sim', 'Não'],
        states=['SP', 'RJ', 'MG'],
        products=['Prod A', 'Prod B', 'Prod C'],
        flavors=['Sweet', 'Salty'],
    )
    assert len(result) == 2


def test_apply_filters_channel(sample_df):
    """Ads filter isolates Sim rows."""
    result = apply_filters(
        sample_df,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        channels=['Sim'],
        states=['SP', 'RJ', 'MG'],
        products=['Prod A', 'Prod B', 'Prod C'],
        flavors=['Sweet', 'Salty'],
    )
    assert (result['Venda por publicidade'] == 'Sim').all()
    assert len(result) == 2


def test_apply_filters_empty_result(sample_df):
    """Unknown state yields empty frame."""
    result = apply_filters(
        sample_df,
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        channels=['Sim', 'Não'],
        states=['XX'],
        products=['Prod A', 'Prod B', 'Prod C'],
        flavors=['Sweet', 'Salty'],
    )
    assert result.empty


def test_apply_selection_matches_apply_filters(sample_df):
    """Dataclass wrapper delegates correctly."""
    selection = FilterSelection(
        start_date=date(2023, 1, 1),
        end_date=date(2023, 12, 31),
        channels=['Sim', 'Não'],
        states=['SP'],
        products=['Prod A', 'Prod B', 'Prod C'],
        flavors=['Sweet', 'Salty'],
    )
    assert len(apply_selection(sample_df, selection)) == 2
