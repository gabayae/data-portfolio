# A/B Test Framework — Multi-arm Marketing Promotion

## Business question

Which of three promotion strategies (Promotion 1 vs. 2 vs. 3) drives the highest sales? A real fast-food chain ran them across stores; we apply a rigorous A/B/n testing framework to draw correct conclusions and recommend the rollout.

The toolkit demonstrated here applies directly to African retail or telecom marketing experiments (e.g., MTN Nigeria push campaigns, Jumia promo strategies).

## Data

- **Source:** [Fast Food Marketing Campaign A/B Test (Kaggle)](https://www.kaggle.com/datasets/chebotinaa/fast-food-marketing-campaign-ab-test) — 548 weekly sales observations across 137 locations × 4 weeks × 3 promotions, with market size (Small/Medium/Large) and store age.

Run `python download_data.py`.

## EDA targets

- Sales distribution per promotion arm
- Market size as a stratifier
- Store age effect

## Statistical analyses

| Test | Use |
|---|---|
| Welch's two-sample t-test | Pairwise promotion comparisons |
| One-way ANOVA | Joint test across all three promotions |
| Stratified analysis (by MarketSize) | Avoid Simpson's paradox |
| OLS with covariate adjustment | Controls for `AgeOfStore`, `MarketSize` |
| Bayesian A/B (Beta-Binomial-style on means) | Posterior P(promotion 1 > promotion 3) |

## Validation

- Multiple-comparison correction (Bonferroni / Holm)
- Effect size: Cohen's d
- Power-analysis check (was the experiment adequately sized?)

## Deployment

- Dashboard summarizing per-arm sales + 95% CI + lift estimate vs. control
- Decision rule: launch winning promotion globally if lift > 5% with p < 0.01 (corrected)

## Business outcome

- Statistically defensible promotion-rollout decision
- Stratification surfaces interaction effects (does promo 3 work better in Small markets?)
- Pipeline reusable for any randomized marketing or product experiment
