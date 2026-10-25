<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/03-insurance-claims-fremtpl2/notebook.ipynb) · [Case study →](https://gabayae.github.io/data-portfolio/case-studies/fremtpl2/)

---

# Insurance Claims Frequency & Severity Forecasting — freMTPL2

## Business question

Can we produce policy-level expected-loss estimates that improve on the incumbent GLM, while staying explainable enough for actuarial review and tier-pricing decisions?

## Data & EDA

- **Source:** [freMTPL2 / French Motor Third-Party Liability (Kaggle)](https://www.kaggle.com/datasets/floser/french-motor-claims-datasets-fremtpl2freq)
- **Volume:** ~680k policies with exposure, driver age, vehicle, region, and claim counts/amounts.
- **EDA targets:**
  - Overdispersion in claim frequency (variance > mean → negative-binomial alternative)
  - Heavy right-skew in severity (long tail → log/Gamma)
  - Region × vehicle-class interactions
  - Exposure offset (claims per policy-year)

## Modeling

| Target | Model |
|---|---|
| Frequency | Poisson GLM (log-link, exposure offset) |
| Severity | Gamma GLM on positive claims |
| Pure premium (unified) | Tweedie / compound-Poisson GLM, `var_power = 1.5` with sensitivity scan over 1.3-1.7 |
| ML challenger | `GradientBoostingRegressor` with Poisson-frequency × log1p-severity decomposition and **Duan smearing** on the severity back-transform |

## Validation

- Single deterministic 80/20 split; **5-fold CV is not run on this notebook** — the dataset is 678k policies, point estimates at that scale are stable; bootstrap on Gini is a routine extension if a formal CI is needed.
- **Lorenz curves + Gini** (actuarial-standard ranking metric) and **top-decile lift** (upper-tail segmentation).
- **Reliability curves** (predicted vs. observed pure premium by decile) added so calibration is visible, not just ranking.
- **Tweedie `var_power` sensitivity** scanned over 1.3-1.7: Gini stays in 0.307-0.313, confirming the result is robust to the Tweedie-power choice.
- **Duan smearing factor ≈ 1.55** on the GBM severity back-transform: the naive `expm1(predict_log)` was under-predicting severity by ~35% because $E[\exp(X)] \neq \exp(E[X])$ for log-fitted targets. Duan correction fixes the absolute pure-premium level (and reserve adequacy); Gini is rank-invariant and therefore unchanged by this correction.

**Headline numbers:**

| Model | Gini | Top-decile lift |
|---|---|---|
| **Tweedie GLM** | **0.310** | 2.52 |
| Poisson + Gamma GLM | 0.241 | **2.66** |
| GBM (Duan smearing) | 0.211 | 1.45 |
| GBM (naive back-transform) | 0.211 | 1.45 |

Two different metrics pick two different models. **Tweedie wins Gini (best overall ranking); Poisson + Gamma wins top-decile lift (best upper-tail segmentation).** The choice is actuarial — Gini-oriented pricing favours Tweedie; a reinsurance-driven program with upper-tail exposure favours Poisson + Gamma.

## Deployment sketch

- Export GLM coefficients (CSV, interpretable, version-controllable, audit-friendly) + pickled GBM artifacts; rating engine consumes both.
- Actuarial memo with partial-dependence plots, Lorenz curves, reliability diagram, and the var_power sensitivity table.

## Business outcome

- Measurable segmentation lift (Gini 0.31 Tweedie, lift 2.66 Poisson + Gamma) while preserving GLM-level explainability.
- GBM challenger underperforms both GLMs on segmentation on this dataset — a reminder that for actuarial pricing, structural models can beat unconstrained ML.
