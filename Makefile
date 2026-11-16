# ==============================================================================
# Makefile for Hepatic-stellate-cell-etiology-scRNAseq
# Provides convenient one-command workflow execution for reviewers & researchers
# ==============================================================================

CONDA_ENV_NAME := hsc-atlas-bmj
PYTHON := python3

.PHONY: help setup-env download-data verify-config clean

help:
	@echo "======================================================================"
	@echo " Human Hepatic Stellate Cell Atlas - Reproducibility Commands"
	@echo "======================================================================"
	@echo "  make setup-env       Create Conda environment ($(CONDA_ENV_NAME))"
	@echo "  make download-data   Download & extract all 4 GEO cohorts into data/raw/"
	@echo "  make verify-config   Verify Python paths and locked gene panels"
	@echo "  make clean           Remove temporary caches (.ipynb_checkpoints, __pycache__)"
	@echo "======================================================================"

setup-env:
	conda env create -f environment.yml

download-data:
	bash scripts/download_geo_data.sh

verify-config:
	$(PYTHON) -c "import src.hsc_atlas_config as cfg; print('[OK] Repo root:', cfg.REPO_ROOT); print('[OK] 4-State genes:', sum(len(v) for v in cfg.HSC_FOUR_STATE_PROGRAMMES.values()))"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	find . -type f -name ".DS_Store" -delete