# Consumer Quickstart

This path inspects public metadata, checks one corpus, exports it, and verifies
the portable result.

## 1. Use the managed public index

```console
$ waldo index list science
$ waldo index show science/plos
```

With no configured index, the first command clones the public index into
`~/.waldo/index`. WALDO automatically fetches and safely fast-forwards that
checkout before subsequent online reads. `list` finds corpora recursively;
`show` prints either a directory index or a single manifest.

Omit the path to select the whole index, for example `waldo index summary`.
Use `waldo index pull` when you want to synchronize explicitly.

## 2. Choose a verification cost

```console
$ waldo index verify science/plos --offline
$ waldo index verify science/plos
$ waldo index verify science/plos --objects
```

- `--offline` validates only local metadata.
- The default also checks every canonical URL and declared size without
  downloading bodies.
- `--objects` downloads every selected object and proves its SHA-256.

For record-level validation, use `waldo index audit science/plos`. This can be
expensive: it materializes the whole selection, validates every canonical
record, detects duplicate IDs, and reconciles totals.

## 3. Export a selection

```console
$ waldo index export science/plos ./plos-export --format native
$ waldo bom show ./plos-export
$ waldo bom verify ./plos-export
```

The directory contains `data/` plus `EXPORT.json`. Native export preserves the
verified Parquet object identity. JSONL export is also available:

```console
$ waldo index export core/books ./books-jsonl --format jsonl
```

## 4. Apply license policy when selecting

```console
$ waldo index export core science ./selected \
    --license 'CC-*' \
    --exclude-license 'CC-BY-NC-*'
```

Patterns are comma-separated shell-style globs. Exclusions take precedence.
The exact policy is pinned into `EXPORT.json`.
