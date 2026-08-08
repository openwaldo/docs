# Persistent Files and Formats

Every durable WALDO format has an explicit `kind` and `schema`. Schema 1 readers
accept additive unknown fields; incompatible meaning requires a new schema.

| File/artifact | Kind or role | Owner | Purpose |
| --- | --- | --- | --- |
| `index.yaml` / `.yml` / `.json` | `index` schema 1 | Index | Directory navigation |
| Corpus manifest | `manifest` schema 1 | Index | Corpus meaning and shard declarations |
| Submanifest | Content-addressed shard tree | Index/corpus | Scale large shard inventories |
| Canonical Parquet | Record schema 1 | Record/shard | Immutable corpus object |
| Ingest recipe | `waldo-ingest-recipe` schema 1 | Acquisition handoff | Explicit fetch steps and corpus metadata |
| Input profile | Strict mapping schema | Ingest | Corpus-neutral physical-to-logical mapping |
| `EXPORT.json` | `waldo-corpus-export` schema 1 | Provenance | Corpus BOM plus materialized files |
| Model compose | `waldo-model-compose` schema 1 | Model | Portable architecture and stages |
| `ORIGIN-BOM.json` | Model origin record | Model | Pinned acquired checkpoint lineage |
| `PLAN.json` | Compose transaction plan | Model | Resolved immutable model plan |
| `RUN-BOM.json` | Planned run record | Model/provenance | Inputs and intent before execution |
| `RUN.json` | Run state/observations | Model | Attempts, terminal state, measurements |
| `MODEL.json` | Model definition | Model | Immutable architecture and identity |
| `MODEL-BOM.json` | Managed aggregate | Model/provenance | Append-only origin/run lineage |
| `BOM.json` | Native aggregate or derived release inventory | Export | Portable technical provenance |
| `EU-BOM.json` | Regulatory projection | Disclosure | Training-content evidence mapping |
| `*.sigstore.json` | Detached Sigstore bundle | Signing/export | Signature over BOM bytes |

## Compatibility policy

Existing schema-1 indexes, manifests, source/conversion/shard fields, rollup
forms, referenced legacy shard formats, SHA-256 identities, and lookaside URLs
are compatibility surfaces. Old CLI spelling, old configuration, internal Go
APIs, old model-store layouts, and undocumented behavior are not automatically
compatible.

YAML is canonical for new metadata writes. Touching JSON navigation may replace
it explicitly with YAML, but the represented schema meaning remains version 1.

## Canonical serialization

Hashes bind exact bytes, so deterministic JSON and Parquet encoding are tested
across supported platforms. Generated timestamps are observations and are not
silently treated as corpus identity. Paths stored in portable BOMs are relative
and normalized beneath their package root.

