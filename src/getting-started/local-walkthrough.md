# Local End-to-End Walkthrough

This walkthrough builds a tiny index and lookaside entirely on one machine. It
exercises initialization, dry-run, ingestion, inspection, export, and offline
BOM verification without cloud credentials.

## Create an isolated workspace

```console
$ mkdir -p /tmp/waldo-tour/input
$ printf 'The first local document.\n' > /tmp/waldo-tour/input/one.txt
$ printf 'The second local document.\n' > /tmp/waldo-tour/input/two.md
$ export WALDO_CONFIG=/tmp/waldo-tour/config.json
$ waldo index init /tmp/waldo-tour/index
$ git -C /tmp/waldo-tour/index init
$ git -C /tmp/waldo-tour/index add index.yaml
$ git -C /tmp/waldo-tour/index commit -s -m "Initialize local index"
$ waldo config set index /tmp/waldo-tour/index
$ waldo config set lookaside file:///tmp/waldo-tour/lookaside
$ waldo config set lookaside.cache /tmp/waldo-tour/cache
```

`WALDO_CONFIG` isolates the tour from your normal configuration. The index and
lookaside are separate directories even in this local setup.

## Preview and ingest

```console
$ waldo index ingest /tmp/waldo-tour/input /tmp/waldo-tour/index/examples/tour \
    --title "Local tour" \
    --description "Two documents used by the WALDO documentation tour." \
    --license CC0-1.0 \
    --source https://example.invalid/waldo-tour \
    --source-category public-dataset \
    --dry-run
```

Review the detected inputs, adapter, record count, and destination. Ingestion
uses an absolute destination because this shell is not inside the checkout.
Then repeat without `--dry-run`. WALDO will report conversion, audit,
publication, and the metadata overlay paths.

```console
$ waldo index ingest /tmp/waldo-tour/input /tmp/waldo-tour/index/examples/tour \
    --title "Local tour" \
    --description "Two documents used by the WALDO documentation tour." \
    --license CC0-1.0 \
    --source https://example.invalid/waldo-tour \
    --source-category public-dataset
$ cp -R -- /path/printed/as/contribution/. /tmp/waldo-tour/index/
$ git -C /tmp/waldo-tour/index diff --check
$ git -C /tmp/waldo-tour/index add .
$ git -C /tmp/waldo-tour/index commit -s -m "Add local tour corpus"
```

Replace `/path/printed/as/contribution` with the contribution path in WALDO's
output. Inspect that staged tree before copying it. Even for a local lookaside,
WALDO deliberately leaves application of the metadata overlay explicit.

## Inspect and verify

```console
$ waldo index list
$ waldo index show examples/tour
$ waldo index summary examples
$ waldo index verify examples/tour --objects
$ waldo lookaside list examples/tour
```

## Export and prove portability

```console
$ waldo index export examples/tour /tmp/waldo-tour/export --format jsonl
$ waldo bom show /tmp/waldo-tour/export
$ waldo bom verify /tmp/waldo-tour/export
$ waldo index export examples/tour /tmp/waldo-tour/native --format native
$ waldo shard summary /tmp/waldo-tour/native/data
```

`bom verify` needs only the export directory. It does not reopen the index or
contact lookaside storage. This is the key portability property of an export.

Remove `/tmp/waldo-tour` when you no longer need the example.
