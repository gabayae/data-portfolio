# Contributing

This is a personal portfolio repository — issues and pull requests are welcome but expectations are limited. The portfolio is curated to demonstrate a specific technical range, not a community project.

## Reporting issues

If you find a bug in a notebook (broken cell, wrong number, dead link), please open an issue with:
- Project folder (e.g., `06-river-flow-forecasting-kariba`)
- Cell number or section heading
- What you observed vs. what you expected
- Your environment (Python version, OS)

## Suggesting improvements

Feedback that improves the portfolio's analytical rigor is welcome:
- A more appropriate model for a given problem
- A better real-world dataset that swaps in cleanly
- A statistical issue (mis-specified test, leakage, mis-applied metric)

Please open an issue first to discuss before writing code.

## Local setup

```bash
git clone https://github.com/gabayae/data-portfolio.git
cd data-portfolio
make install        # installs dependencies from pyproject.toml
make data           # downloads all real datasets (Kaggle CLI auth needed for some)
make notebooks      # executes every notebook
```

Each project folder is self-contained — you can also `cd <project> && pip install -r requirements.txt && jupyter notebook` to work on a single project.

## Style

- **Notebooks** use the standard 7-section structure: Setup → Data → EDA → Modeling → Validation → Deployment → Outcome.
- **READMEs** mirror that structure.
- **Code** is formatted with `ruff` (`make lint` if added later); notebooks use `nbstripout` for clean diffs.

## License

By contributing, you agree your contributions are licensed under the MIT License (see `LICENSE`).
