"""Shared pytest fixtures without hardcoded absolute paths."""

from datetime import date
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """Small in-memory frame covering all business logic columns."""
    return pd.DataFrame(
        {
            'Receita por produtos (BRL)': [100.0, 200.0, 50.0, 150.0],
            'N.º de venda': ['1', '2', '3', '2'],
            'Venda por publicidade': ['Sim', 'Não', 'Sim', 'Não'],
            'Estado': ['SP', 'RJ', 'SP', 'MG'],
            'Título do anúncio': ['Prod A', 'Prod B', 'Prod A', 'Prod C'],
            'Variação': ['Sweet', 'Salty', 'Sweet', 'Sweet'],
            'Data da venda': [
                date(2023, 1, 10),
                date(2023, 1, 12),
                date(2023, 2, 5),
                date(2023, 2, 6),
            ],
            'year_month': ['2023-01', '2023-01', '2023-02', '2023-02'],
            'weekday': [1, 3, 6, 0],
            'weekday_name': ['Tuesday', 'Thursday', 'Sunday', 'Monday'],
            'hour': [10, 14, 10, 9],
        }
    )


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    """Temporary raw CSV exercising the ETL pipeline."""
    path = tmp_path / 'sample_sales.csv'
    df = pd.DataFrame(
        {
            'N.º de venda': [101, 102],
            'Data da venda': ['2023-09-13 14:14:00', '2023-09-14 10:00:00'],
            'Data a caminho completa': ['2023-09-14 11:30:00', '2023-09-15 09:00:00'],
            'Data de entrega completa': ['2023-09-19 14:42:00', '2023-09-20 12:00:00'],
            'Unidades': [1, 2],
            'Reclamação encerrada': [0, 1],
            'Receita por produtos (BRL)': [37.71, 50.0],
            'Tarifa de venda e impostos': [-10.53, -5.0],
            'Tarifas de envio': [-44.5, -10.0],
            'Cancelamentos e reembolsos (BRL)': [0.0, -2.0],
            'Venda por publicidade': ['Não', 'Sim'],
            'Estado': ['Goiás', 'SP'],
            'Título do anúncio': ['Prod A', 'Prod B'],
            'Variação': ['Sweet', 'Salty'],
        }
    )
    df.to_csv(path, index=False)
    return path


@pytest.fixture
def project_data_path() -> Path:
    """Real dataset path resolved relative to repo root."""
    return Path(__file__).resolve().parents[1] / 'data' / 'sales_2023.csv'
