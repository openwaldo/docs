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
	$(PYTHON) scripts/build_book.py html

pdf: check
	@if ! $(PDF_PYTHON) -c 'import reportlab' >/dev/null 2>&1; then $(MAKE) setup; fi
	$(PDF_PYTHON) scripts/build_book.py pdf

model-guide: html check
	@if ! $(PDF_PYTHON) -c 'import reportlab' >/dev/null 2>&1; then $(MAKE) setup; fi
	$(PDF_PYTHON) scripts/build_book.py model-guide

contributor-guide: html check
	@if ! $(PDF_PYTHON) -c 'import reportlab' >/dev/null 2>&1; then $(MAKE) setup; fi
	$(PDF_PYTHON) scripts/build_book.py contributor-guide

quickstarts: model-guide contributor-guide

all: html pdf model-guide contributor-guide

build: all

serve: html
	$(PYTHON) -m http.server 8000 --directory output/html

clean:
	rm -rf output/html output/pdf
