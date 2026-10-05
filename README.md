# Mercado Livre Sales Dashboard

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.32%2B-FF4B4B)
![Pandas](https://img.shields.io/badge/pandas-2.2%2B-150458)
![Plotly](https://img.shields.io/badge/plotly-5.22%2B-636EFA)
![Pytest](https://img.shields.io/badge/tests-pytest-green)
![Ruff](https://img.shields.io/badge/lint-ruff-black)

Interactive Streamlit dashboard for Mercado Livre sales analysis: revenue KPIs, time trend, seasonality, product rankings and geographic breakdown with sidebar filters.

## Screenshots

<div align="center">
  <img src="docs/screenshots/ML_01.png" alt="Dashboard overview with KPIs" width="100%">
  <p><em>Overview with KPIs and sales trend.</em></p>
</div>

<br>

<div align="center">
  <img src="docs/screenshots/ML_02.png" alt="Seasonality and rankings" width="100%">
  <p><em>Seasonality and product rankings.</em></p>
</div>

<br>

<div align="center">
  <img src="docs/screenshots/ML_03.png" alt="Geography and dataset" width="100%">
  <p><em>Geography and full dataset view.</em></p>
</div>

## Features

- Headline KPIs: total revenue, orders, average ticket, ads and organic revenue
- Monthly sales trend (smoothed line chart)
- Seasonality by weekday and hour
- Product and flavor rankings with progress bars
- Geography by state (bar + donut)
- Interactive filters: date range, ads channel, state, product, flavor
- Full dataset table

## Tech Stack

- Python 3.12+
- Streamlit, Pandas, Plotly, NumPy, PyArrow, Pillow
- Pytest, Ruff, Coverage (dev)

## Project Structure

```text
.
├── app.py                    # Thin Streamlit entrypoint
├── pyproject.toml            # Ruff + Pytest + Coverage config
├── requirements.txt          # Runtime deps (minimal, >=)
├── requirements-dev.txt      # Dev deps (pytest, ruff, coverage)
├── .streamlit/config.toml    # Theme
├── data/sales_2023.csv       # Example dataset (small, tracked)
├── assets/logo.png           # Runtime logo
├── docs/screenshots/         # README images
├── sales_dashboard/          # Application package
│   ├── __init__.py
│   ├── constants.py          # Paths, column keys, parameters
│   ├── etl.py                # Load, type coercion, temporal columns
│   ├── formatting.py         # Currency formatting
│   ├── metrics.py            # Business metrics
│   ├── aggregations.py       # Chart aggregations
│   ├── filters.py            # Filter logic + FilterSelection
│   ├── charts.py             # Plotly theme and layout
│   ├── styles.py             # CSS injection and hero
│   └── components.py         # Streamlit view components
└── tests/                    # Pytest suite
    ├── conftest.py
    ├── test_etl.py
    ├── test_metrics.py
    ├── test_aggregations.py
    ├── test_filters.py
    └── test_formatting.py
```

Layering: `constants.py` (config), `etl.py` (data loading), `metrics.py` / `aggregations.py` / `filters.py` (business logic), `charts.py` / `styles.py` / `components.py` (UI), `app.py` (composition only).

Raw CSV headers stay in Portuguese (source domain data) and are referenced through English constants. Derived columns are English snake_case (`year_month`, `weekday`, `hour`, `transit_days`, ...). Code identifiers, comments and docstrings are 100% English; UI labels stay in Portuguese for Brazilian users.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dev setup:

```bash
pip install -r requirements-dev.txt
```

## Usage

```bash
streamlit run app.py
```

Open `http://localhost:8501`. Data loads from `data/sales_2023.csv` via `DATA_PATH` in `sales_dashboard/constants.py`. Replace that file to analyse another export with the same schema.

## Configuration

- Theme: `.streamlit/config.toml` (primary `#2D3277`, light base).
- Logo: `assets/logo.png` referenced by `LOGO_PATH`.
- Ranking size: `TOP_N` in `constants.py`.
- Lint: `pyproject.toml` (`line-length = 100`, single quotes enforced).

## Data Schema

Expected CSV columns:

- `Data da venda`, `Data a caminho completa`, `Data de entrega completa`
- `Unidades`, `Reclamação encerrada`, `N.º de venda`
- `Tarifa de venda e impostos`, `Tarifas de envio`, `Cancelamentos e reembolsos (BRL)`
- `Receita por produtos (BRL)`, `Venda por publicidade` (`Sim`/`Não`)
- `Estado`, `Título do anúncio`, `Variação`

ETL coerces dates, nullable ints, absolute fees and derives `year_month`, `year`, `month`, `day`, `hour`, `minute`, `weekday`, `quarter`, `weekday_name`, `month_name` plus transit/delivery/total deltas.

## Testing

```bash
pytest -v
coverage run -m pytest && coverage report
```

Fixtures live in `tests/conftest.py` and use `tmp_path` (no absolute paths).

## Linting

```bash
ruff check .
ruff format --check .
ruff format .  # auto-fix when needed
```

Config enforces single quotes, isort ordering and `line-length = 100`.

## Contributing

- Use English identifiers, single quotes, type hints and docstrings.
- Keep modules small with single responsibility.
- Add Pytest coverage for business logic before refactoring.
- Run `pytest -v`, `ruff check .` and `ruff format --check .` before opening a PR.

## License

MIT — see [LICENSE](LICENSE).

## Author

Renato Perussi — June 2026. Refactored October 2026 to production-ready modular layout.
