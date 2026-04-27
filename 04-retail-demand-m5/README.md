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
| Aggregate (state, department) | SARIMA / Prophet / ETS |
| Base (SKU × store) | LightGBM with rich lag, rolling, price, calendar features |
| Reconciliation | MinT (minimum-trace) optimal combination across hierarchy |

## Validation

- Rolling-origin weighted RMSSE per the M5 protocol
- Per-level evaluation: state, store, department, category, SKU
- Reconciled forecasts must satisfy aggregation constraints

## Deployment

- Python/PySpark batch pipeline producing a weekly forecast drop
- Forecasts consumed by replenishment and buying workflows
- Coherent numbers shared between merchandising and planning teams

## Business outcome

- Multi-level forecasts that align bottom-up SKU expectations with top-down category plans
- Less reconciliation work between merchandising and planning teams
