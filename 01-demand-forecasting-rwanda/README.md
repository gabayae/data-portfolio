<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](./notebook.ipynb)

---

# Demand Forecasting — Rwanda Health Supply Chain

## Business question

Can we forecast 3–6 month consumption of essential medicines across districts so that stockouts **and** over-stocking both drop, and supply-chain officers can make reorder + cross-district reallocation decisions with calibrated prediction intervals?

## Data & EDA

- **Source (real):** national health-supply-chain warehouse (delivery + dispensation tables). No single fully-public dataset exists; this notebook generates synthetic-but-realistic monthly data (12 SKUs × 10 districts × 60 months). Swap `load_data()` with the real SQL query when connected.
- **EDA targets:**
  - Annual seasonality (malaria peaks around rainy seasons)
  - Structural break during COVID-19 (early 2020)
  - Intermittent demand for slow-moving SKUs (Croston regime)
  - Delayed / missing reporting from rural districts
  - Trend (population growth, program expansions)

## Modeling

| Family | Models |
|---|---|
| Classical time-series | SARIMA, exponential smoothing (ETS) |
| State-space | UnobservedComponents (trend + seasonal + AR) |
| ML for forecasting | Gradient-boosted regressor with lag/rolling/calendar features |
| Intermittent demand | Croston's method for slow-moving SKUs |

## Validation

- Rolling-origin backtest, 12-month horizon, monthly re-fit
- Metrics: **MAPE**, **WAPE**, bias, prediction-interval coverage
- Per-level evaluation: district × SKU-category
- Baselines: naïve-seasonal, ETS

## Deployment

- Streamlit dashboard with a FastAPI backend
- Monthly retraining via scheduled Python pipeline pulling from the warehouse
- Forecasts + prediction intervals written to a Postgres table that the dashboard reads

## Business outcome

- 3-month forward visibility with calibrated intervals for supply-chain officers
- Reorder quantities and cross-district reallocation decisions informed by forecasts
- Monthly S&OP meeting shortened (agreed numbers instead of debated numbers)
