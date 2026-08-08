# CLI Reference

WALDO organizes commands by the object being managed. Run
`waldo <group> <command> --help` for the authoritative help shipped with your
installed version.

Global options are `--help`, `--version`, and `--json`. Place `--json` before
the group. Structured results go to stdout and progress to stderr.

## Index

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `init` | `waldo index init <directory>` | Write the smallest schema-1 index into a new/empty directory. |
| `list` | `waldo index list [path]` | List corpora recursively. |
| `show` | `waldo index show [path]` | Show navigation or a manifest. |
| `summary` | `waldo index summary [path]` | Aggregate corpora, licenses, and totals. |
| `verify` | `waldo index verify [path] [--offline\|--objects]` | Validate metadata, availability, or full object hashes. |
| `audit` | `waldo index audit [path] [--workers <n>]` | Validate all records and reconcile totals. |
| `ingest` | `waldo index ingest <input-or-recipe> <destination> [options]` | Convert, audit, publish, and prepare a contribution. |
| `update` | `waldo index update <input-or-recipe> <manifest> [options]` | Append new records or rebuild shards. |
| `export` | `waldo index export <path...> <directory> [options]` | Materialize verified data and `EXPORT.json`. |
| `remove` | — | Reserved command; not yet implemented. |

Ingest direct-input metadata options are `--title`, `--description`,
`--license`, `--source`, `--source-name`, `--source-category`, `--text-column`,
and `--input-profile`; the first four excluding description/source-name plus
source category are required. `--dry-run` is universal. Recipe input rejects
metadata flags.

Update supports `--rebuild-shards` and the applicable ingestion options. Export
supports `--format native|jsonl`, `--license`, `--exclude-license`, and
`--force`. Audit workers must be 1–32.

## Shard

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `summary` | `waldo shard summary <path...>` | Aggregate local Parquet metadata. |
| `audit` | `waldo shard audit <path...> [--workers <n>]` | Stream and validate all selected records. |
| `list-records` | `waldo shard list-records <shard-file>` | List compact record summaries. |
| `export-record` | `waldo shard export-record <shard-file> <record-id>` | Write exact text to stdout. |

Summary/audit accept files, directories, and glob patterns. Directory traversal
selects `.parquet` files recursively.

## Lookaside

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `login` | `waldo lookaside login` | Verify and store credentials for configured S3 publication. |
| `logout` | `waldo lookaside logout` | Remove stored WALDO S3 credentials. |
| `list` | `waldo lookaside list [index-path] [--all]` | Inventory objects and optional index references. |
| `status` | `waldo lookaside status` | Show cache, scratch, mirrors, publication, and credentials. |
| `verify` | `waldo lookaside verify` | Scrub retained cache hashes. |
| `mirror` | — | Reserved command; not yet implemented. |
| `rm` | `waldo lookaside rm <sha256>...` | Remove preflighted, explicitly named objects. |

## Model

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `init` | `waldo model init <name> --preset <preset>` | Create an untrained architecture. |
| `pull` | `waldo model pull <name> <huggingface-source>` | Pin and normalize compatible open weights. |
| `list` | `waldo model list [pattern...]` | List models with shell-style name matching. |
| `summary` | `waldo model summary <name>` | Show architecture and run history. |
| `bom` | `waldo model bom <name> [output.json]` | Emit canonical aggregate provenance. |
| `forecast` | `waldo model forecast <compose.yaml> \| <index-path...>` | Estimate fitting hardware and duration. |
| `train` | `waldo model train <name> <index-path...> [--epochs <n>]` | Append a resumable causal-training run. |
| `compose` | `waldo model compose <name> <compose-file> [--replace]` | Create/train through ordered portable stages. |
| `export` | `waldo model export <name> <directory> [options]` | Publish a release package and disclosures. |
| `chat` | `waldo model chat <name> [prompt] [options]` | Interactive or one-shot generation. |
| `rm` | `waldo model rm <name...>` | Remove exact managed model names. |

Export formats are `waldo`, `huggingface`, `mlx`, `gguf`, and `ollama`.
Quantization accepts 2, 3, 4, 5, 6, or 8 plus optional `--calibration`.
`--allow-incomplete` permits a marked disclosure draft. Chat options are
`--max-tokens`, `--temperature`, `--top-p`, and `--seed`.

## BOM

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `show` | `waldo bom show <export-directory\|EXPORT.json>` | Summarize a corpus export BOM. |
| `verify` | `waldo bom verify <export-directory\|EXPORT.json>` | Validate and hash exported files offline. |
| `export` | `waldo bom export <model> [output.json] --format eu-gpai [options]` | Map model provenance to disclosure JSON. |

BOM disclosure options are `--provider`, `--allow-incomplete`, and `--force`.

## Config

| Command | Synopsis | Purpose |
| --- | --- | --- |
| `show` | `waldo config show` | Show effective grouped configuration. |
| `get` | `waldo config get [key-or-prefix]` | Discover all keys, a group, or one value. |
| `set` | `waldo config set <key> <value...>` | Set one machine-local value. |
| `unset` | `waldo config unset <key>` | Restore one value to its default. |

