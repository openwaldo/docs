# Contributor Quickstart

This path turns local text into canonical shards and a reviewable index change.
Start with material you are authorized to process and evidence you can record.

## 1. Prepare a checkout and writable lookaside

```console
$ waldo config set index /path/to/your/waldo-index
$ waldo config set lookaside s3://contribution-bucket/prefix
$ waldo config set lookaside.region us-east-2
$ waldo lookaside login
```

Use the writable location and region supplied by the index operator. A
`file://` lookaside is suitable only for local development; do not submit its
local object URLs to a shared index.

## 2. Probe before writing

```console
$ waldo index ingest ./acquired-data /path/to/your/waldo-index/community/example \
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
and prepares a small Git metadata overlay. It does not modify the checkout.

```console
$ waldo index ingest ./acquired-data /path/to/your/waldo-index/community/example \
    --title "Example corpus" \
    --description "A small example corpus." \
    --license CC-BY-4.0 \
    --source https://example.org/dataset \
    --source-category public-dataset
$ cp -R -- /path/printed/as/contribution/. /path/to/your/waldo-index/
$ cd /path/to/your/waldo-index
$ git diff --check
$ waldo index verify community/example --objects
$ git add index.yaml community/index.yaml community/example
$ git commit -s -m "Add example corpus"
```

First inspect the printed contribution directory, then replace the placeholder
in the copy command with that exact path. The `git add` example assumes a new
`community/example` path; stage the exact overlay paths printed by WALDO because
the set of parent navigation files varies. WALDO does not apply, commit, push,
or open a pull request.

## 4. Submit with sign-off

OpenWALDO uses the Developer Certificate of Origin. `git commit -s` adds the
required `Signed-off-by` trailer. The sign-off asserts that you have the right
to submit the change under the project terms; it is not a substitute for
accurate source and license evidence.
