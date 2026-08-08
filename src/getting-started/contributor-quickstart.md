# Contributor Quickstart

This path turns local text into canonical shards and a reviewable index change.
Start with material you are authorized to process and evidence you can record.

## 1. Prepare a checkout and writable lookaside

```console
$ waldo config set index /path/to/your/waldo-index
$ waldo config set lookaside file:///absolute/path/to/lookaside
```

A `file://` lookaside is suitable for local development. Public contribution
usually uses an operator-provided S3 location.

## 2. Probe before writing

```console
$ waldo index ingest ./acquired-data community/example \
    --title "Example corpus" \
    --description "A small example corpus." \
    --license CC-BY-4.0 \
    --source https://example.org/dataset \
    --source-category public-dataset \
    --dry-run
```

Direct ingestion accepts text, Markdown, plain/gzip/zstd JSONL, and Parquet.
Dry-run probes the files and prints the immutable conversion plan without
uploading or changing the index.

## 3. Ingest and review

Remove `--dry-run` only after the plan is correct. WALDO converts and packs
canonical Parquet, audits every produced shard, publishes and verifies objects,
and prepares a small Git metadata overlay.

```console
$ waldo index ingest ./acquired-data community/example \
    --title "Example corpus" \
    --description "A small example corpus." \
    --license CC-BY-4.0 \
    --source https://example.org/dataset \
    --source-category public-dataset
$ cd /path/to/your/waldo-index
$ git diff --check
$ waldo index verify community/example --objects
$ git add community/example
$ git commit -s -m "Add example corpus"
```

Use the exact overlay paths printed by WALDO when staging; parent navigation
files may also change. WALDO does not commit, push, or open a pull request.

## 4. Submit with sign-off

OpenWALDO uses the Developer Certificate of Origin. `git commit -s` adds the
required `Signed-off-by` trailer. The sign-off asserts that you have the right
to submit the change under the project terms; it is not a substitute for
accurate source and license evidence.

