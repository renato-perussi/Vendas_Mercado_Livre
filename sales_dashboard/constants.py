"""Project-wide constants: paths, column keys and parameters."""

from pathlib import Path

# Base paths.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / 'data' / 'sales_2023.csv'
LOGO_PATH = PROJECT_ROOT / 'assets' / 'logo.png'

# Raw dataset columns (Portuguese domain values from CSV header).
DATE_COLUMNS = [
    'Data da venda',
    'Data a caminho completa',
    'Data de entrega completa',
]
INT_COLUMNS = ['Unidades', 'Reclamação encerrada']
STRING_COLUMNS = ['N.º de venda']
ABS_COLUMNS = [
    'Tarifa de venda e impostos',
    'Tarifas de envio',
    'Cancelamentos e reembolsos (BRL)',
]

COL_REVENUE = 'Receita por produtos (BRL)'
COL_ADS = 'Venda por publicidade'
COL_STATE = 'Estado'
COL_PRODUCT = 'Título do anúncio'
COL_FLAVOR = 'Variação'
COL_ORDER_ID = 'N.º de venda'
COL_SALE_DATE = 'Data da venda'

# Derived temporal columns (English identifiers owned by ETL).
COL_YEAR_MONTH = 'year_month'
COL_YEAR = 'year'
COL_MONTH = 'month'
COL_DAY = 'day'
COL_HOUR = 'hour'
COL_MINUTE = 'minute'
COL_WEEKDAY = 'weekday'
COL_QUARTER = 'quarter'
COL_WEEKDAY_NAME = 'weekday_name'
COL_MONTH_NAME = 'month_name'

TEMPORAL_STR_COLUMNS = [
    COL_YEAR_MONTH,
    COL_WEEKDAY_NAME,
    COL_MONTH_NAME,
]

# Locale.
LOCALE_BR = 'pt_BR.UTF-8'

# Ranking size.
TOP_N = 10

# Advertising channel values (domain data).
ADS_YES = 'Sim'
ADS_NO = 'Não'
