<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Case study](https://gabayae.github.io/data-portfolio/case-studies/solar/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/07-solar-forecasting-nairobi/notebook.ipynb) · [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gabayae/data-portfolio/blob/main/07-solar-forecasting-nairobi/notebook.ipynb)

---

# Solar Energy Forecasting — Nairobi (NASA POWER)

## Business question

Can we forecast daily surface solar irradiance in Nairobi 7–30 days ahead so that:
- A utility-scale solar developer can plan inverter and battery dispatch
- Off-grid solar/storage operators (Kenya has one of the largest pay-as-you-go solar markets in Africa) can size battery reserves to expected sun
- Grid integrators can quantify expected solar contribution against thermal/hydro alternatives

A 1-day-ahead irradiance error of even 5% can flip whether a battery should be filled or left to discharge — the operational stakes are real.

## Data

- **Source:** [NASA POWER (Prediction Of Worldwide Energy Resources) API](https://power.larc.nasa.gov/), free, no auth.
- **Location:** Nairobi (lat -1.2921, lon 36.8219).
- **Period:** 2014-01-01 → 2023-12-31, daily (3,653 observations).
- **Variables:**
  - `ALLSKY_SFC_SW_DWN`: surface shortwave irradiance (kWh/m²/day) — the **forecast target**
  - `T2M`: temperature at 2 m (°C)
  - `RH2M`: relative humidity at 2 m (%)
  - `WS2M`: wind speed at 2 m (m/s)
  - `PRECTOTCORR`: corrected precipitation (mm/day)
  - `CLOUD_AMT`: cloud cover (%)

Run `python download_data.py` to fetch fresh data (no auth required).

## EDA targets

- Strong annual seasonality (rainy seasons March–May and October–December reduce irradiance)
- Cloud-cover and humidity inverse-correlated with irradiance
- Day-to-day persistence (autocorrelation)
- Long-term anomalies (e.g., 2019 East African floods)

## Modeling

| Family | Model |
|---|---|
| Classical time-series | SARIMA on daily irradiance |
| State-space | UnobservedComponents (level + harmonic annual seasonality + exog Fourier) |
| ML for forecasting | Gradient-boosted regressor with lag/rolling/calendar features + cloud/humidity covariates |

## Validation

- 90-day held-out test
- Metrics: MAPE, RMSE, 95% PI empirical coverage
- Baselines: naive-last, naive-seasonal (365-day lag), monthly climatology (computed on **train only** — not the full series)
- Headline MAPEs: **GBM 9.4% · monthly climatology 12.6% · SARIMA 13.8% · UC 19.6%**. At Nairobi's latitude the seasonal envelope carries most of the predictability, which is why climatology beats SARIMA. GBM wins on point error because it also sees **yesterday's cloud cover and humidity** (lag-1 exog + 7-day rolling mean; the notebook explicitly avoids same-day exog as per-cell comment: *"NEVER feed same-day exog at training time — that would be information leakage"*). At the 1-day forecast horizon used here, yesterday's observed weather is directly available at inference; extending beyond 1 day would need a chained weather forecast.
- 95% PI empirical coverage: SARIMA 89/90, UC 89/90 — Clopper-Pearson 95% CI around 89/90 is roughly [0.94, 1.00], so these samples are consistent with any true coverage ≥ 94%. The intervals are directional, not formally calibrated at this sample size.

## Deployment sketch

- Scheduled retrain + pickled SARIMA/UC artifact; same pipeline extends to any African city by changing the lat/lon in `download_data.py`.
- Weather-conditioned GBM point forecasts at the 1-day horizon work with lag-1 observed exog (what this validation uses). Extending beyond 1 day would need a chained weather forecast as input — the feature-engineering hook is there, a NASA POWER forecast ingest hasn't been wired yet.

## Business outcome

- Daily solar irradiance predicted a month out, with 95% PIs that read directional on n=90. Enough to support dispatch and battery-sizing conversations for utility and pay-as-you-go solar.
- At this latitude, climatology is a strong baseline; the ML lift comes from yesterday's weather (lag-1 cloud + humidity), not from the time-series structure.
- Fully reproducible from a free, programmatic data source — easy to audit.
