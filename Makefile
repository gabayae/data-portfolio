# Yaé Gaba — Data Science Portfolio Makefile
# Usage:
#   make help         — list targets
#   make install      — install Python dependencies
#   make data         — run every project's download_data.py
#   make notebooks    — execute every notebook end-to-end
#   make test         — run smoke checks (notebook validity + JSON parse)
#   make clean        — remove generated artifacts (data/, *_cache/, .ipynb_checkpoints/)

PROJECTS := $(sort $(wildcard [0-9][0-9]-*))
PYTHON ?= python

.PHONY: help install data notebooks test clean

help:
	@echo "Yaé Gaba — Data Science Portfolio"
	@echo ""
	@echo "Targets:"
	@echo "  install     Install Python dependencies from pyproject.toml"
	@echo "  data        Download all real datasets (Kaggle CLI required for some)"
	@echo "  notebooks   Execute every notebook end-to-end"
	@echo "  test        Validate every notebook is well-formed JSON"
	@echo "  clean       Remove data/, artifacts/, and Jupyter caches"
	@echo ""
	@echo "Discovered projects: $(words $(PROJECTS))"

install:
	$(PYTHON) -m pip install -e ".[dev]"

data:
	@for p in $(PROJECTS); do \
	  echo "─── $$p ───"; \
	  if [ -f "$$p/download_data.py" ]; then \
	    (cd $$p && $(PYTHON) download_data.py) || echo "WARN: $$p data download failed"; \
	  else \
	    echo "  (no download_data.py — skipping)"; \
	  fi; \
	done

notebooks:
	@for p in $(PROJECTS); do \
	  echo "─── executing $$p/notebook.ipynb ───"; \
	  jupyter nbconvert --to notebook --execute "$$p/notebook.ipynb" \
	    --output notebook.ipynb --ExecutePreprocessor.timeout=900 \
	    || { echo "FAIL: $$p"; exit 1; }; \
	done

test:
	@$(PYTHON) -c "import json, glob, sys; \
	  fail=0; \
	  [ (json.load(open(p, encoding='utf-8')), print('ok:', p)) \
	    if not (lambda: (json.load(open(p, encoding='utf-8')), False)[1])() \
	    else (print('BAD:', p), fail+1) \
	    for p in sorted(glob.glob('[0-9][0-9]-*/notebook.ipynb')) ]; \
	  sys.exit(0 if fail==0 else 1)"

clean:
	@for p in $(PROJECTS); do \
	  rm -rf "$$p/data" "$$p/artifacts" "$$p/.ipynb_checkpoints"; \
	done
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@echo "cleaned data/, artifacts/, __pycache__/, .ipynb_checkpoints/"
