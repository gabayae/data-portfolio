<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](./notebook.ipynb)

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
  - `ALLSKY_SFC_SW_DWN` — surface shortwave irradiance (kWh/m²/day) — the **forecast target**
  - `T2M` — temperature at 2 m (°C)
  - `RH2M` — relative humidity at 2 m (%)
  - `WS2M` — wind speed at 2 m (m/s)
  - `PRECTOTCORR` — corrected precipitation (mm/day)
  - `CLOUD_AMT` — cloud cover (%)

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
- Metrics: MAPE, RMSE, prediction-interval coverage
- Baselines: naive-last, naive-seasonal (365-day lag), monthly climatology

## Deployment

- FastAPI `/forecast?horizon=30d` returning daily mean irradiance + 95% PI for the next month
- Streamlit dashboard for solar developers — irradiance forecast band, battery-state-of-charge planner, generation-impact estimator
- Daily refresh from NASA POWER; weekly model retraining
- Same pipeline trivially extends to Lagos, Cape Town, Cairo, Dakar — just change the lat/lon

## Business outcome

- 30-day forward visibility on solar irradiance with calibrated intervals — reduces uncertainty in dispatch and storage decisions
- Quantifies expected vs. worst-case generation for budgeting and grid contracts
- Fully reproducible from a free, programmatic data source — easy to audit
