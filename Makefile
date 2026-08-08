.PHONY: check build serve

check:
	python3 scripts/check-links.py

build: check
	mdbook build

serve: check
	mdbook serve --open

