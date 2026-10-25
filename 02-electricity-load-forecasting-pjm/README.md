<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/02-electricity-load-forecasting-pjm/notebook.ipynb) · [Case study →](https://gabayae.github.io/data-portfolio/case-studies/pjm/)

---

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
| Classical baseline | SARIMA on daily aggregated load |
| State-space | `UnobservedComponents` with time-varying level + harmonic weekly/daily Fourier terms + exogenous regressors |
| ML challenger | GBM (`GradientBoostingRegressor`) with engineered lag, rolling, and calendar features |

## Validation

- 60-day held-out backtest at the end of the series
- Metrics: MAPE, RMSE, 95% prediction-interval coverage
- SARIMA MAPE 14.5%, UC MAPE 19.3%, GBM MAPE 6.2% — but the GBM number is a 1-step-ahead evaluation with revealed previous-day load. Not directly comparable to the SARIMA / UC multi-step forecasts. See the case study for the full discussion.
- UC 95% PI empirical coverage: 60/60 (Clopper-Pearson 95% CI [0.94, 1.00] — the sample is too small to distinguish 95% from 99%).

## Deployment sketch

- Winning candidate (daily SARIMA at this scope) could be served behind a scheduled retrain + pickled artifact.
- Not a production system — the notebook stops at offline forecasting on real PJME data.

## Business outcome

- Day-ahead load forecasting on real PJME data; SARIMA is the operational pick (multi-step honest baseline) over the UC state-space variant on this run.
- Headline point-error gap between SARIMA (14.5%) and GBM (6.2%, 1-step-ahead) is largely a comparison-protocol artifact — a true recursive-mode GBM evaluation is the natural next step before any procurement claim.
