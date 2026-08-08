# The OpenWALDO Book

This repository contains the long-form documentation for OpenWALDO: the public
training-data commons, the `waldo` command-line tool, and the public corpus
index.

Start reading at [Introduction](src/introduction.md), or browse the complete
[table of contents](src/SUMMARY.md).

## Build locally

The source is ordinary Markdown and is useful without a build step. The Makefile
can produce a multi-page HTML site or a single printable PDF:

```console
$ make html       # output/html/index.html
$ make pdf        # output/pdf/openwaldo-book.pdf
$ make all        # both formats
$ make serve      # HTML at http://localhost:8000
```

`make pdf` creates a local `.venv` and installs the pinned ReportLab dependency
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

This book is maintained alongside:

- [`openwaldo/waldo`](https://github.com/openwaldo/waldo) — CLI and contracts
- [`openwaldo/waldo-index`](https://github.com/openwaldo/waldo-index) — public metadata index
- [`openwaldo/openwaldo.org`](https://github.com/openwaldo/openwaldo.org) — project website
