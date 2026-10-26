<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/04-retail-demand-m5/notebook.ipynb)

---

# Hierarchical Retail Demand Forecasting — M5

## Business question

Produce coherent SKU × store × week forecasts — a category forecast must equal the sum of its SKUs — to plan shelf replenishment and department buying off the same numbers.

## Data & EDA

- **Source:** [M5 Forecasting Accuracy (Kaggle)](https://www.kaggle.com/competitions/m5-forecasting-accuracy) — Walmart daily sales for ~30k SKUs across 10 stores in 3 states, with calendar, prices, and SNAP events.
- **EDA targets:**
  - Heavy intermittency (many zero-sales days per SKU)
  - Price/promo sensitivity
  - Holiday effects (Super Bowl, Christmas, Easter)
  - SNAP event-driven demand pulls
  - Hierarchy: SKU → category → department → store → state

## Modeling

| Level | Approach |
|---|---|
| Aggregate (national weekly) | SARIMA(1,1,1)(0,1,1)₅₂ |
| Base (item × store) | `GradientBoostingRegressor` with lag/calendar/rolling features |
| Reconciliation | MinT-OLS projection across the full hierarchy: TOTAL / STATE (3) / STATE×DEPT (15) / BOTTOM (130) |

## Validation

- **8-week held-out test**, per-series RMSSE at every hierarchy level (not just TOTAL+BOTTOM), each series scaled by its own training-naive error per the canonical M5 WRMSSE protocol.
- Headline numbers:

| Level | pre-recon mean RMSSE | post-recon mean RMSSE | Δ |
|---|---|---|---|
| TOTAL (1 series) | 3.11 | 3.13 | +0.02 (slightly worsens — pulled toward bottom-up) |
| STATE (3 series) | 2.30 | 2.25 | **−0.05 (improves)** |
| STATE×DEPT (15 series) | 1.59 | 1.57 | **−0.02 (improves)** |
| BOTTOM (130 series) | 1.305 | 1.299 | −0.006 (negligible) |

What the numbers say: coherence holds by construction (bottom sums match TOTAL by linear algebra). Measurable error reduction only shows up at the mid-levels where MinT typically earns its keep (STATE, STATE×DEPT). TOTAL slightly worsens because reconciliation pulls the SARIMA aggregate toward the bottom-up sum; BOTTOM barely moves.

## Deployment sketch

- Weekly batch pipeline: base GBM per (item × store), aggregate SARIMA, MinT-OLS reconciliation, output written as a coherent `(level, series, week, forecast)` table.
- Consumers: replenishment reads BOTTOM; merchandising reads STATE×DEPT; planning reads TOTAL — all reading the same reconciled numbers.

## Business outcome

- One coherent forecast set across TOTAL → STATE → STATE×DEPT → BOTTOM; replenishment, merchandising, and planning no longer argue over which number is correct.
- MinT-OLS lift is modest in absolute terms (hundredths of RMSSE at mid-levels); the operational value is coherence, not accuracy improvement.

**Next iterations:** WLS / MinT-shrink reconciliation using empirical forecast-error covariances; add M5 calendar price/promo features; evaluate across rolling-origin windows for CI on each level's RMSSE delta.
