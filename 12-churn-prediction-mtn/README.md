<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/12-churn-prediction-mtn/notebook.ipynb)

---

# Churn Prediction — MTN Nigeria Telecom

> **Dataset note.** This Kaggle snapshot (974 MTN Nigeria customer rows) is approximately random-uniform in the covariates we tested — see the sister notebook `08-customer-survival-mtn-tenure/README.md` for details. Logistic AUC and RF F1 collapse; XGBoost AUC = 0.71 reflects non-linear interactions in high-cardinality one-hots, not substantively interpretable signal. **This notebook is a teaching demo of binary-churn classification end-to-end** — logistic regression, random forest, XGBoost, ROC / PR / calibration diagnostics, retention-queue ranking. For a real benchmark see the IBM Watson Telco Customer Churn dataset (7,043 customers).

## Business question

Which customers are most likely to churn in the next quarter, and which features drive their risk? A binary classifier ranks customers by churn probability so retention campaigns can target the highest-risk segment.

(Companion to project 08, which models the same data as a survival problem — same data, two analytical lenses, both useful.)

## Data

- **Source:** [MTN Nigeria Customer Churn (Kaggle)](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) — 974 customers, 17 features (age, state, plan, satisfaction, tenure, revenue, data usage, churn label).

Run `python download_data.py`.

## EDA targets

- Class balance (~29% churn)
- Univariate hazard signals: low-satisfaction, low-tenure, plan type
- State-level differences

## Modeling

| Family | Model |
|---|---|
| Linear | Logistic regression with L2 penalty (interpretable baseline) |
| Trees | Random Forest, Gradient Boosting (XGBoost) |

## Validation

- 80/20 stratified split (test-set base rate = 29%).
- Metrics: ROC-AUC, PR-AUC, F1, balanced accuracy, **Precision@k and Lift@k** for the retention-queue framing.
- Calibration plot with **Wilson 95% CIs per bin** so the ~19-obs-per-bin uncertainty is visible rather than smoothed over.

**Headline numbers (test):**

| Model | ROC-AUC | PR-AUC | P@50 | Lift@50 | P@100 | Lift@100 |
|---|---|---|---|---|---|---|
| XGBoost | 0.71 | 0.51 | **0.52** | **1.78×** | 0.40 | 1.37× |
| Random Forest | 0.59 | 0.36 | 0.34 | 1.16× | 0.38 | 1.30× |
| LogReg | 0.48 | 0.27 | 0.20 | 0.68× | 0.30 | 1.03× |

Only XGBoost's top-50 queue carries meaningful lift (1.78× over random). LogReg's top-50 is actually *worse* than random — a telltale that linear scoring is picking up anti-signal on this (near-random) data. See the dataset note above for the honest reading.

## Deployment sketch

- Retention queue ranked by XGBoost score; audit Lift@k monthly against the holdout to catch score drift.
- Not deployable on the current dataset — the dataset note at the top applies. On a real churn benchmark (IBM Watson Telco) the same code produces interpretable features and defensible top-k lift.

## Business outcome

- Retention spend allocated where predicted lift is highest; top-k is the metric that matches the campaign-targeting use case.
- Companion to project 08 (survival analysis on the same data) — two analytical lenses, both constrained by the same data provenance issue.
