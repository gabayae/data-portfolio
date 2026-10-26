<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Case study](https://gabayae.github.io/data-portfolio/case-studies/solar/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/07-solar-forecasting-nairobi/notebook.ipynb)

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
- Headline MAPEs on this run: **GBM 9.4% · monthly climatology 12.6% · SARIMA 13.8% · UC 19.6%**. At Nairobi's latitude the seasonal envelope carries most of the predictability — climatology beats SARIMA. GBM wins on point error only because it sees same-day cloud and humidity covariates.
- 95% PI empirical coverage: SARIMA 89/90, UC 89/90 — Clopper-Pearson 95% CI around 89/90 is roughly [0.94, 1.00], so these samples are consistent with any true coverage ≥ 94%. The intervals are directional, not formally calibrated at this sample size.

## Deployment sketch

- Scheduled retrain + pickled SARIMA/UC artifact; same pipeline extends to any African city by changing the lat/lon in `download_data.py`.
- Weather-conditioned GBM point forecasts need a chained weather forecast at horizons beyond 1 day (same-day cloud is the lever).

## Business outcome

- 30-day forward visibility on solar irradiance with directional 95% PIs — supports dispatch and battery-sizing decisions for utility and pay-as-you-go solar.
- At this latitude, climatology is a strong baseline; the ML lift comes from same-day weather, not from the time-series structure.
- Fully reproducible from a free, programmatic data source — easy to audit.
