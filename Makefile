PYTHON ?= python3
VENV := .venv
VENV_PYTHON := $(VENV)/bin/python3
PDF_PYTHON ?= $(VENV_PYTHON)

.PHONY: check setup html pdf model-guide contributor-guide quickstarts all build serve clean

check:
	python3 scripts/check-links.py

$(VENV)/.ready: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install -r requirements.txt
	touch $(VENV)/.ready

setup: $(VENV)/.ready

html: check
	$(PYTHON) scripts/build_guides.py html

model-guide: check
	@if ! $(PDF_PYTHON) -c 'import reportlab' >/dev/null 2>&1; then $(MAKE) setup; fi
	$(PDF_PYTHON) scripts/build_guides.py model-guide

contributor-guide: check
	@if ! $(PDF_PYTHON) -c 'import reportlab' >/dev/null 2>&1; then $(MAKE) setup; fi
	$(PDF_PYTHON) scripts/build_guides.py contributor-guide

pdf: model-guide contributor-guide

quickstarts: html pdf

all: quickstarts

build: all

serve: html
	$(PYTHON) -m http.server 8000 --directory output/html

clean:
	rm -rf output/html output/pdf
