"""Currency formatting tests."""

from sales_dashboard.formatting import format_currency


def test_format_currency_returns_string():
    """Formatted value is a non-empty string with R$."""
    text = format_currency(1234.5)
    assert isinstance(text, str)
    assert 'R$' in text
    assert text != ''


def test_format_currency_zero():
    """Zero formats without error."""
    text = format_currency(0.0)
    assert 'R$' in text


def test_format_currency_negative_fallback():
    """Negative values still include currency symbol."""
    text = format_currency(-10.5)
    assert 'R$' in text
