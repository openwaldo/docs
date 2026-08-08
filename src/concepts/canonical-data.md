# Canonical Records and Shards

Canonical text uses record schema 1 stored in self-contained Parquet objects.
Each logical record represents one pre-training document.

## Logical record

| Field | Meaning |
| --- | --- |
| `content_sha256` | SHA-256 of the exact UTF-8 text; record identity |
| `text` | Required document text |
| `source` | Required source identifier |
| `source_name` | Optional human source label |
| `license` | Required normalized asserted license |
| `license_raw` | Optional upstream license text |
| `language` | Optional language identifier |
| `language_score` | Optional integer confidence from 0–1000 |
| `date` | Optional source date |
| `token_count` | Reference tokenizer count |
| `meta` | Canonical JSON object for additional metadata |

JSONL interchange uses the historical schema-1 names `sha256`, `kind`, `text`,
`source`, `source_name`, `license`, `license_raw`, `lang`, `lang_score`, `date`,
`tokens`, and `meta`. `kind` is `pretrain`.

Text must be valid UTF-8 and nonempty. Its content hash must match exactly.
Source and license are required. Metadata must be a JSON object. Record identity
enables exact deduplication across files and updates.

## Physical encoding

Canonical shards use a pinned Parquet recipe, currently zstd compression,
bounded pages and row groups, and stable writer metadata. Manifests record the
recipe and converter profile so changed bytes do not masquerade under an old
identity.

Only canonical Parquet objects belong in lookaside storage. There are no hidden
catalogs, metadata sidecars, or loose media files there. An object's SHA-256 is
its name and transport identity; the index provides its meaning.

## Deterministic assembly

Ingestion probes inputs into an immutable plan, maps physical records, computes
content identity, deduplicates through a disk-backed set, and packs bounded
shards. It streams large inputs and keeps recovery state, avoiding a whole-
corpus intermediate.

Each finished shard receives a full record audit before upload. The manifest
stores document count, reference token estimate, and encoded bytes. Training
later counts exact model tokens because reference-token totals describe the
corpus and may use a different tokenizer.

## Validation levels

Footer summary trusts complete canonical metadata. Full audit scans records,
recomputes text hashes and token counts, validates field invariants, and checks
duplicate identities across a selection. Object SHA-256 proves container bytes;
record hashes prove content identities inside the container.

