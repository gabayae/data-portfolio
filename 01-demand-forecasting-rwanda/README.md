<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/01-demand-forecasting-rwanda/notebook.ipynb)

---

# Demand Forecasting — Rwanda Health Supply Chain

## Business question

Can we forecast monthly consumption of essential medicines (ARV, HRDT) so supply-chain officers can plan reorders and reduce stockouts? Rwanda is the focus country (105 monthly observations, 2007–2015, 94 non-zero months) in a real public dataset of 10,324 PEPFAR/USAID SCMS shipments across 43 countries.

## Data

- **Source:** real PEPFAR / USAID Supply Chain Management System (SCMS) shipment records — [apoorvwatsky/supply-chain-shipment-pricing-data](https://www.kaggle.com/datasets/apoorvwatsky/supply-chain-shipment-pricing-data). 10,324 shipments across 43 countries, 2006–2015. Aggregated to monthly delivered units; Rwanda is the modeled series (105 months, 94 non-zero).
- The README's previous mention of a "12 SKUs × 10 districts × 60 months synthetic fallback" is removed — the notebook models the real Rwanda-level aggregate directly.

## Modeling

| Family | Model |
|---|---|
| Classical time-series | SARIMA(1,1,1)(1,1,1)₁₂ |
| State-space | UnobservedComponents (local-linear-trend + stochastic seasonal) |
| Exponential smoothing | Holt-Winters additive triple ES |
| ML for forecasting | `GradientBoostingRegressor` on engineered lag/calendar/rolling features |
| Reference baseline | Naive-seasonal (predict next month = same month one year ago) |

## Validation

- **Rolling-origin backtest, 18 one-step-ahead folds**, all four candidates re-fit at each origin on train-only data.
- Metric: WAPE (robust to zero-sales months, unlike vanilla MAPE).
- Headline numbers on this run:

| Model | WAPE | Lift over naive |
|---|---|---|
| **GBM (recursive 1-step)** | **0.863** | **24% improvement** |
| SARIMA | 0.941 | 17% improvement |
| Naive-seasonal | 1.130 | — |
| Holt-Winters | 1.143 | −1% (worse) |

WAPE in this range is a weak *absolute* score; it reflects the realistic difficulty of intermittent-demand monthly health-supply-chain data (94 non-zero months out of 105), not weakness in the models. The 24% lift of GBM over naive-seasonal is the honest finding.

- **SARIMA 95% PI coverage** on the 18 rolling folds: **18/18 = 100%**, mean half-width ≈ 385k units — intervals are too wide (over-covered relative to the 95% nominal), not calibrated. Clopper-Pearson 95% CI around 18/18 is roughly [0.81, 1.00], so the sample is consistent with any true coverage ≥ 81%.

## Deployment sketch

- Monthly retrain per (country × product-group) series; artifacts versioned.
- Not a production system — the notebook stops at offline forecasting on the real PEPFAR extract.

## Business outcome

- 12-month forward visibility on Rwanda PEPFAR monthly delivered units; GBM is the operational pick on this run under rolling-origin WAPE.
- Intermittent-demand regime: expect WAPE in the 0.8–1.0 range on monthly health-supply-chain aggregates; interval forecasts matter more than point forecasts for reorder decisions.

**Next iterations:** hierarchical reconciliation (country → region → global), exogenous regressors (program rollouts, funding cycles), Croston's method per slow-moving SKU.
