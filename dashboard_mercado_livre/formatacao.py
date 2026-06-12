"""Formatação de valores (moeda local, etc.)."""

import locale

from .constantes import LOCALE_BR

try:
    locale.setlocale(locale.LC_ALL, LOCALE_BR)
except locale.Error:
    locale.setlocale(locale.LC_ALL, "")


def formatar_moeda(valor: float) -> str:
    """Formata um número como moeda brasileira (R$)."""
    try:
        return locale.currency(valor, grouping=True)
    except (locale.Error, ValueError):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
