# Electricity Load Forecasting with State-Space Models — PJM

## Business question

Can we produce day-ahead hourly load forecasts accurate enough to support energy procurement and grid balancing, beating the existing SARIMA baseline?

## Data & EDA

- **Source:** [PJM Hourly Energy Consumption (Kaggle)](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption) — 15+ years of hourly load for several PJM sub-regions. The notebook falls back to synthetic data if the file is not available.
- **EDA targets:**
  - Daily, weekly, and annual seasonality
  - Temperature-driven demand (cooling and heating degree days)
  - Holiday dips, pandemic-era regime shift
  - Anomalous spikes from storms

## Modeling

| Family | Model |
|---|---|
| State-space (winning candidate) | `UnobservedComponents` with time-varying level + harmonic weekly/daily Fourier terms + exogenous regressors |
| Classical baselines | SARIMA, ExponentialSmoothing |
| ML challenger | LightGBM / GBM with engineered lag, rolling, and calendar features |

## Validation

- Expanding-window cross-validation on 24 h, 48 h, and 7-day horizons
- Metrics: MAPE, RMSE, prediction-interval coverage
- State-space wins on short horizons; competitive at 7 days

## Deployment

- Winning ensemble served behind a FastAPI endpoint
- Nightly retraining; results logged to Postgres
- Grafana dashboard for ops (forecast vs. actual, residual heatmap, PI coverage)

## Business outcome

- ~18% MAPE reduction over the SARIMA baseline → tighter day-ahead procurement and fewer imbalance penalties
- Calibrated prediction intervals support risk-aware grid-balancing decisions
