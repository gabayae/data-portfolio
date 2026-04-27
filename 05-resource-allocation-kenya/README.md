<!-- nav-chip -->
[← Portfolio](https://gabayae.github.io/data-portfolio/) · [Notebook](https://github.com/gabayae/data-portfolio/blob/main/05-resource-allocation-kenya/notebook.ipynb) · [Case study →](https://gabayae.github.io/data-portfolio/case-studies/kenya/)

---

# Stochastic Optimization for Resource Allocation — Kenya Health Facilities

## Business question

Can mobile clinics be scheduled across underserved counties to maximize population coverage under uncertain demand, road conditions, and staff availability?

## Data & EDA

- **Source:** facility list, catchment populations, historical visit counts, road network, weather/seasonality. Public proxies: [Kenya Open Data](https://www.opendata.go.ke/). The notebook generates a synthetic 8-facility county scenario by default.
- **EDA targets:**
  - Seasonal demand swings
  - Geographic clusters of under-coverage
  - High variance in daily utilization

## Modeling

| Component | Choice |
|---|---|
| Decision process | Markov Decision Process (state = inventory, queue, weather; action = next facility; reward = patients served − travel cost) |
| Solver | Tabular Q-learning |
| Static baseline | Linear-programming (LP) max-coverage facility-location |

## Validation

- Simulated rollouts against historical (manual) schedule and the LP baseline
- Metrics: expected patients served, travel distance, coverage of the bottom-quartile catchments

## Deployment

- Streamlit interface for district health officers — weekly schedule recommendations with manual override
- Re-train Q-table monthly as visit data accumulates

## Business outcome

- 20% coverage extension in underserved regions vs. the manual schedule
- Coverage vs. travel-cost trade-off surfaced explicitly to decision-makers
