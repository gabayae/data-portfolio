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
| Classical time-series | SARIMA(1,1,1)(1,1,1)₇ on daily level |
| State-space | `UnobservedComponents` (local-linear-trend + Fourier annual exog) |
| ML challenger (fair) | `GradientBoostingRegressor`, target-only features, **recursive 30-step** |
| ML challenger (context) | GBM with lagged `turbine_discharge` + `total_outflow` + revealed previous-day level, 1-step-ahead |

## Validation

- 30-day held-out window, two GBM variants compared side-by-side.
- Metrics: MAPE, RMSE in metres, 95% PI coverage with Clopper-Pearson CI.

**Headline numbers:**

| Model | MAPE | RMSE (m) | 95% PI coverage |
|---|---|---|---|
| **SARIMA (multi-step)** | **0.027%** | **0.184** | 30/30 (CP [0.88, 1.00]) |
| UC state-space (multi-step) | 0.079% | 0.418 | 30/30 (CP [0.88, 1.00]) |
| GBM recursive 30-step (fair) | 0.085% | 0.508 | — |
| Naive-last | 0.085% | 0.501 | — |
| GBM 1-step-ahead w/ exog (context) | 0.013% | 0.069 | — |

SARIMA wins the like-for-like comparison at **18 cm RMSE** on 30-day multi-step forecasting. It is the only well-calibrated interval in the set (SARIMA 95% PI mean half-width ≈ 56 cm, 30/30 coverage with CP CI [0.88, 1.00]). The GBM recursive-mode variant degrades to 51 cm RMSE, essentially tied with naive-last, because the operator-decision covariates (`turbine_discharge`, `total_outflow`) cannot be conditioned on at 30-day horizon. The previously headlined "7 cm RMSE GBM" was a 1-step-ahead evaluation with revealed previous-day discharge, retained in the table as context rather than as the deployable number.

## Deployment sketch

- SARIMA is the operational pick for a 30-day planning forecast on this dataset: calibrated 95% PI + lowest multi-step RMSE in the comparison.
- A real-time 1-step-ahead service (next-day refresh with yesterday's discharge known) could use the GBM-with-exog variant for substantially tighter point accuracy; the use cases differ.

## Business outcome

- 30-day lake-level visibility with SARIMA's calibrated 95% PI — supports Zambezi River Authority turbine-dispatch planning when discharge is a *decision* variable.
- The GBM-with-exog variant is a 1-day operational tool, not a 30-day planning tool. The notebook now distinguishes the two regimes.

**Next iterations:** CHIRPS / NASA POWER rainfall forecasts as *exogenous rainfall-driven inflow* (which IS known at prediction time, unlike future discharge); regime-switching state-space for drought vs flood; quantile-GBM for probabilistic risk bands around turbine-threshold crossings.
