# Customer Survival Analysis — MTN Nigeria Telecom

## Business question

Beyond a binary "will they churn?", how does churn risk *change with tenure*? Survival analysis lets us:
- Estimate the survival function S(t) — probability a customer is still active at month t
- Identify high-hazard tenure windows (e.g., months 1–6 after onboarding) for targeted retention
- Quantify how covariates (subscription plan, age, satisfaction) shift the hazard

## Data

- **Source:** [MTN Nigeria Customer Churn (Kaggle)](https://www.kaggle.com/datasets/oluwademiladeadeniyi/mtn-nigeria-customer-churn) — 974 customers, 17 attributes including tenure (months), subscription plan, satisfaction, churn outcome.
- **Survival framing:**
  - `duration` = `Customer Tenure in months`
  - `event` = 1 if `Customer Churn Status == 'Yes'`, else 0 (right-censored, still active)

Run `python download_data.py` to fetch (Kaggle CLI required).

## EDA targets

- Median time-to-churn vs. censoring
- Hazard differences by subscription plan, age band, satisfaction
- Reasons for churn (free-text categorization)

## Modeling

- **Kaplan–Meier** survival curves stratified by subscription plan and satisfaction
- **Cox Proportional Hazards** with covariate-adjusted hazard ratios
- **Weibull AFT** for direct interpretability of expected lifetime

## Validation

- Concordance index (C-index) on a 20% held-out test set
- Log-rank tests across strata

## Deployment

- API `POST /customer-survival` returning expected remaining tenure + churn-risk band given customer attributes
- Retention dashboard ranking customers by 90-day churn probability

## Business outcome

- Tenure-aware retention targeting beats blanket "anyone classified as risky"
- Hazard ratios drive product/pricing decisions (e.g., does plan X retain longer than plan Y, controlling for age?)
- Same pipeline applies to any subscription business with tenure + churn signal
