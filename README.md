# OpenWALDO Quickstarts

This repository contains two focused OpenWALDO guides:

- [Training Quickstart](src/quickstarts/models.md)
- [Contributor Quickstart](src/quickstarts/contributing.md)

## Build locally

The source is ordinary Markdown and is useful without a build step. The
Makefile produces HTML pages and one printable PDF per guide:

```console
$ make html              # both HTML pages
$ make pdf               # both PDFs
$ make model-guide       # training PDF only
$ make contributor-guide # contributor PDF only
$ make quickstarts       # both formats for both guides
$ make all               # same as make quickstarts
$ make serve      # HTML at http://localhost:8000
```

Outputs are written to:

- `output/html/quickstarts/models.html`
- `output/html/quickstarts/contributing.html`
- `output/pdf/openwaldo-model-quickstart.pdf`
- `output/pdf/openwaldo-contributor-quickstart.pdf`

The PDF targets create a local `.venv` and install the pinned ReportLab dependency
on its first run. HTML generation uses only the Python standard library.
Generated artifacts and the virtual environment are intentionally ignored by
Git. Use `make clean` to remove generated HTML and PDF output.

Run the dependency-free content checks with:

```console
$ make check
```

## Documentation principles

- Document implemented behavior, and label planned behavior.
- Begin with a runnable path, then explain the machinery beneath it.
- Keep commands copyable and state their side effects.
- Separate integrity evidence from legal or safety conclusions.
- Treat the WALDO source and format contracts as authoritative.

## Source repositories

These quickstarts are maintained alongside:

- [`openwaldo/waldo`](https://github.com/openwaldo/waldo) — CLI and contracts
- [`openwaldo/waldo-index`](https://github.com/openwaldo/waldo-index) — public metadata index
- [`openwaldo/openwaldo.org`](https://github.com/openwaldo/openwaldo.org) — project website
