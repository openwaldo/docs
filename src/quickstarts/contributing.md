# Contribute Training Data

This guide is the shortest safe path from acquired local files to a reviewable,
DCO-signed OpenWALDO index contribution. It keeps Git metadata and canonical
lookaside objects separate throughout.

> Start only with material you are authorized to process and evidence you can
> accurately record. Object hashes prove identity and integrity; they do not
> prove a license assertion or legal right.

## 1. Compile and install WALDO system-wide

WALDO currently requires Go 1.25 or newer:

```console
$ git clone https://github.com/openwaldo/waldo.git
$ cd waldo
$ go build -o ./waldo ./cmd/waldo
$ sudo install -m 0755 ./waldo /usr/local/bin/waldo
$ waldo --version
```

The commands above are for a regular user. When already operating as root, use:

```console
# go build -o ./waldo ./cmd/waldo
# install -m 0755 ./waldo /usr/local/bin/waldo
```

Both forms install the executable at `/usr/local/bin/waldo`, which is normally
on the system-wide command path.

## 2. Optional: install for one user and persist PATH

When system-wide installation is unavailable, install beneath your home
directory:

```console
$ mkdir -p "$HOME/.local/bin"
$ go build -o "$HOME/.local/bin/waldo" ./cmd/waldo
```

Add the following line to your shell startup file, not only to the current
terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Use `~/.zshrc` for zsh, `~/.bashrc` for bash, or `~/.profile` for a POSIX login
shell, then start a new terminal and run `waldo --version`.

## 3. Prepare the source

Gather the local files plus the facts a reviewer will need:

- upstream URL and version or collection date;
- asserted license and supporting evidence;
- source category and selection rule;
- a clear title and description; and
- any processing, modality, language, or acquisition facts available.

Direct ingestion accepts text, Markdown, plain/gzip/zstd JSONL, and Parquet.
Declarative input profiles can map structured JSON, dialogue, trees, bounded
text, and a limited XML selector subset.

## 4. Select a writable contributor checkout

On a fresh installation, `config.index` is unset and WALDO uses the managed
`~/.waldo/index` checkout. Do not contribute from that read-only consumer
cache. Clone your own checkout and set it as the contributor override:

```console
$ git clone https://github.com/openwaldo/waldo-index.git \
    /path/to/waldo-index
$ git -C /path/to/waldo-index remote add fork \
    git@github.com:YOUR-ACCOUNT/waldo-index.git
$ waldo config set index /path/to/waldo-index
$ waldo index pull
$ git -C /path/to/waldo-index status --short --branch
```

With `config.index` set, every relative index path - including `./...` - resolves
beneath that checkout, independent of the shell's current directory. Absolute
and `~/` paths explicitly select another checkout.

WALDO fetches and fast-forwards a selected tracking branch only when it is clean
and strictly behind. Dirty, ahead, diverged, detached, or untracked states are
refused without modification. Resolve those states with normal Git tooling
before ingestion.

## 5. Configure writable lookaside storage

Use the S3 destination and region supplied by the index operator:

```console
$ waldo config set lookaside s3://contribution-bucket/prefix
$ waldo config set lookaside.region us-east-2
$ waldo config set lookaside.workers 4
$ waldo lookaside login
$ waldo lookaside status
```

Login verifies write, list, inspect, read, and delete access with a tiny probe,
then stores bucket-scoped credentials in `~/.waldo/credentials` with mode
`0600`. Secrets are not written to configuration, manifests, output, or shell
history. AWS environment, shared-file, and workload-role credentials remain
available when no WALDO login exists.

A `file://` lookaside is useful for local end-to-end testing only. Never submit
local object URLs to the shared public index.

## 6. Dry-run direct ingestion

Choose a new destination beneath the contributor checkout:

```console
$ waldo index ingest ./acquired-data community/example \
    --title "Example corpus" \
    --description "A concise description of the retained material." \
    --license CC-BY-4.0 \
    --source https://example.org/dataset \
    --source-category public-dataset \
    --dry-run
```

For direct input, `--title`, `--license`, `--source`, and
`--source-category` are required. Dry-run probes files and prints the immutable
conversion plan without uploading objects or changing the checkout. Review the
detected formats, input counts, metadata, memory plan, destination, and writer
recipe.

Use `--text-column` only when Parquet text cannot be inferred uniquely. Use
`--input-profile <file>` for structured mappings. Profiles are corpus-neutral;
source-specific acquisition belongs in a fetcher or recipe.

## 7. Ingest and keep the checkout unchanged

Repeat the approved command without `--dry-run`:

```console
$ waldo index ingest ./acquired-data community/example \
    --title "Example corpus" \
    --description "A concise description of the retained material." \
    --license CC-BY-4.0 \
    --source https://example.org/dataset \
    --source-category public-dataset
```

WALDO maps and deduplicates records, packs canonical schema-1 Parquet, audits
every new shard, publishes objects in parallel, verifies their remote hashes,
purges successful staging copies, and writes a small contribution overlay.

The command deliberately does **not** modify the Git checkout. Its final output
names a contribution directory and every proposed write/removal.

## 8. Review and apply the overlay

Inspect the printed contribution directory before copying it:

```console
$ find /path/printed/as/contribution -type f -print
$ git -C /path/to/waldo-index switch -c add-example-corpus
$ cp -R -- /path/printed/as/contribution/. /path/to/waldo-index/
$ git -C /path/to/waldo-index status --short
$ git -C /path/to/waldo-index diff --check
$ git -C /path/to/waldo-index diff
```

Review the corpus manifest and every changed parent `index.yaml`. Confirm source
facts, asserted license, conversion identity, document/token/byte totals, shard
URLs, SHA-256 values, and that no credentials, local paths, or acquisition
inventories leaked into Git.

## 9. Verify, sign off, and submit

```console
$ waldo index show community/example
$ waldo index verify community/example --offline
$ git -C /path/to/waldo-index add \
    index.yaml community/index.yaml community/example
$ git -C /path/to/waldo-index commit -s -m "Add example corpus"
$ git -C /path/to/waldo-index push -u fork HEAD
$ waldo index verify community/example --objects
```

Stage the exact overlay paths printed by WALDO; the example assumes a new
`community/example` hierarchy. Offline verification is required while the
overlay is uncommitted because online commands refuse a dirty or locally-ahead
checkout. Ingestion has already audited each new shard and verified its remote
hash. After the pushed branch is clean and tracking, `--objects` downloads each
referenced object and proves its SHA-256. A full
`waldo index audit community/example` additionally validates every canonical
record, detects duplicate IDs, and reconciles totals.

`git commit -s` adds the Developer Certificate of Origin `Signed-off-by`
trailer. It asserts your right to submit the change under the project terms; it
does not replace accurate provenance or license review. Push your branch and
open the index pull request from your fork through the project's normal GitHub
workflow.

## 10. Alternative: use a reviewed ingest recipe

A strict YAML/JSON recipe can own corpus metadata and explicitly run reviewed
acquisition scripts:

```console
$ waldo index ingest ./recipes/example.yaml community/example --dry-run
$ waldo index ingest ./recipes/example.yaml community/example
```

Recipe input rejects command-line corpus metadata flags. WALDO resolves and
hashes the recipe and every executable, runs steps directly and sequentially in
a private directory exposed as `WALDO_FETCH_DIR`, rechecks executable hashes,
then enters the same probe, conversion, audit, publication, and overlay path.

Recipe execution is explicit trust, not an operating-system sandbox. Review the
recipe and scripts first. Fetchers acquire local bytes only; they never convert
canonical shards, upload to lookaside, mutate the index, or train a model.

## 11. Update an existing corpus

Normal update audits existing shards and publishes only new record identities:

```console
$ waldo index update ./new-input \
    community/example/example.yaml \
    --dry-run
```

Use `--rebuild-shards` only when the supplied input is the complete
authoritative corpus. It replaces the source and shard set instead of appending:

```console
$ waldo index update ./complete-input \
    community/example/example.yaml \
    --rebuild-shards \
    --dry-run
```

Both modes stage an explicit overlay. Neither deletes superseded lookaside
objects automatically; historical revisions, other indexes, and exported BOMs
may still reference them.

## Submission checklist

- Contributor checkout is separate, clean, tracking, and current.

- Writable lookaside is operator-approved and remotely verified.

- Source, selection, and license evidence are specific and reviewable.

- Dry-run output matches the intended corpus and destination.

- Staged overlay was inspected before application.

- No secrets, local paths, or large objects entered Git.

- `git diff --check` and object verification pass.

- Only the printed overlay paths are staged.

- Commit includes a DCO sign-off.
