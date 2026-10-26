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

- 60-day held-out backtest at the end of the series.
- Metrics: MAPE, RMSE, 95% prediction-interval coverage with Clopper-Pearson CI.

**60-day multi-step forecasts, like-for-like:**

| Model | MAPE | RMSE (MW) | 95% PI coverage |
|---|---|---|---|
| **GBM recursive 60-step** | **9.0%** | 4,414 | — |
| SARIMA (multi-step) | 14.5% | 6,676 | 54/60 (CP CI [0.79, 0.96]) |
| UC state-space (multi-step) | 19.3% | 8,295 | 60/60 (CP CI [0.94, 1.00]) |

GBM beats SARIMA by 38% MAPE once both are evaluated as 60-day multi-step forecasts. The UC state-space variant *lost* to SARIMA on this run (−33% lift). The 1-step-ahead GBM (MAPE 6.2%) is reported in the notebook as context, labeled as such — it assumes revealed previous-day load, which is not a 60-day forecast.

## Deployment sketch

- The recursive GBM is the operational pick on this run; SARIMA offers the only well-calibrated 95% PI (54/60 inside the band).
- Scheduled retrain + pickled artifact; not a production system — the notebook stops at offline forecasting on real PJME data.

## Business outcome

- Day-ahead load forecasting on real PJME data; GBM with recursive multi-step evaluation is the fair point-error leader.
- SARIMA's PI coverage (54/60 at 95% nominal, consistent with any true coverage ≥ 79%) remains the operational choice for procurement/hedging decisions where interval calibration matters more than point error.
