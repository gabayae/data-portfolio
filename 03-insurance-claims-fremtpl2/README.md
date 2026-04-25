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
| Frequency | Poisson GLM (log-link, exposure offset) + negative-binomial alternative |
| Severity | Gamma GLM on positive claims |
| Pure premium (unified) | Tweedie / compound-Poisson GLM |
| ML challenger | XGBoost with Poisson and Gamma objectives |

## Validation

- 5-fold cross-validation on normalized deviance and Gini
- Reliability plots for calibration
- Lorenz curves and top-decile lift for segmentation power
- Compare GLM vs. Tweedie vs. XGBoost head-to-head

## Deployment

- Model artifacts (coefficients, tree ensembles) exported as a scoring function for the rating engine
- Actuarial memo with partial-dependence plots and sensitivity tables for the review committee

## Business outcome

- Measurable lift in segmentation while preserving explainability
- Reserve recommendations and tier-pricing adjustments delivered as actionable insights for underwriting
