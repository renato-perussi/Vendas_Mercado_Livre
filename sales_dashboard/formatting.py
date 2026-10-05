"""Currency formatting with manual fallback."""

import locale


def format_currency(value: float) -> str:
    """Format a number as Brazilian Real."""
    try:
        return locale.currency(value, grouping=True)
    except (locale.Error, ValueError, TypeError):
        # Manual fallback avoids global locale mutation.
        text = f'{value:,.2f}'
        return f'R$ {text}'.replace(',', 'X').replace('.', ',').replace('X', '.')
