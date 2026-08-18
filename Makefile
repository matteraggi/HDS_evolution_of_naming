PYTHON ?= python3.13
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python
REQUIREMENTS_STAMP := $(VENV)/.requirements-installed

.PHONY: all setup reproduce check

all: reproduce

setup: $(REQUIREMENTS_STAMP)

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

$(REQUIREMENTS_STAMP): requirements.txt $(VENV_PYTHON)
	$(VENV_PYTHON) -m pip install -r requirements.txt
	touch $(REQUIREMENTS_STAMP)

reproduce: $(REQUIREMENTS_STAMP)
	$(VENV_PYTHON) src/scripts/run_pipeline.py

check: $(REQUIREMENTS_STAMP)
	$(VENV_PYTHON) -m compileall -q src/scripts
	mkdir -p .cache/matplotlib
	MPLCONFIGDIR="$(CURDIR)/.cache/matplotlib" $(VENV_PYTHON) -c "import matplotlib, pymannkendall, scipy; print('Environment OK')"
