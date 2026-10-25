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

- 80/20 stratified split
- Metrics: ROC-AUC, PR-AUC, F1, balanced accuracy
- Calibration plot for the best model

## Deployment

- API `POST /churn-score` returning probability + decile band + top SHAP-style feature contributions
- Retention queue prioritized by predicted churn probability × revenue

## Business outcome

- Retention spend allocated where ROI is highest (high churn probability × high revenue customers)
- Drivers (e.g., satisfaction rating, plan type) feed product/pricing roadmap
- Same pipeline applies to any subscription business
