<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/06-river-flow-forecasting-kariba/notebook.ipynb) · [Case study →](https://gabayae.github.io/data-portfolio/case-studies/kariba/)

---

# River Flow Forecasting — Lake Kariba (Zambezi Basin)

## Business question

Can we forecast daily Lake Kariba lake-level and total outflow so that the Zambezi River Authority and the Kariba hydroelectric stations (Kariba South, Kariba North) can plan turbine schedules and balance storage between Zambia and Zimbabwe under uncertain inflows?

Lake Kariba is the world's largest man-made reservoir by volume; its level drives ~1,800 MW of regional generation. A 1 m drop in level can cost hundreds of GWh of generation.

## Data

- **Source:** [Lake Kariba Reservoir Data — Kaggle (`marbin/lake-kariba-reservoir-data`)](https://www.kaggle.com/datasets/marbin/lake-kariba-reservoir-data)
- **Period:** 1 Jan 2020 → 28 Feb 2023 (1,155 daily observations)
- **Variables:** `lake_level` (m), `usable_storage`, `live_storage`, `turbine_discharge`, `spillage`, `total_outflow` (m³/s)
- **License:** publisher-declared open data on Kaggle

Run `python download_data.py` to fetch (requires Kaggle CLI configured).

## EDA targets

- Annual seasonality (rainy season Nov–Apr in Southern Africa)
- Long-term decline / recovery cycles in lake level
- Multivariate relationships: lake_level vs storage vs outflow
- Spillage events (mostly zero — extreme high-flow regime)

## Modeling

| Family | Model |
|---|---|
| Classical time-series | SARIMA on daily level |
| State-space | UnobservedComponents (local-linear-trend + harmonic annual seasonality) |
| ML for forecasting | Gradient-boosted regressor with lag/rolling/exogenous features (turbine discharge as covariate) |

## Validation

- Rolling-origin backtest, 30-day horizon
- Metrics: MAPE, RMSE, prediction-interval coverage
- Baselines: naive (last observation), naive-seasonal

## Deployment

- FastAPI `/forecast` returning lake-level mean + 95% PI for the next 30 days
- Streamlit dashboard for the Zambezi River Authority — daily refresh, downside scenarios, generation-impact panel
- Weekly retraining; alerting if rolling RMSE exceeds operational threshold

## Business outcome

- 30-day forward visibility on lake-level with calibrated intervals — informs turbine dispatch and inter-country storage agreements
- Quantifies the operational risk of low-inflow scenarios in advance
