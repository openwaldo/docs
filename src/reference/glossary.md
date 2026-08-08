# Glossary

**Audit** — Full record-level validation, including content hashes, reference
token counts, required fields, duplicates, and aggregate reconciliation.

**Bill of Materials (BOM)** — An immutable machine-readable inventory that
binds identity, inputs, declarations, and hashes at a system boundary.

**Canonical object** — Self-contained schema-1 Parquet bytes whose SHA-256 is
the lookaside identity.

**Compose** — A portable model architecture and ordered training-stage plan,
consumed by `waldo model compose`. It is not an acquisition recipe.

**Corpus** — A named collection described by one index manifest and its
resolved shard set.

**DCO** — Developer Certificate of Origin; a commit sign-off asserting the
contributor has the right to submit the change under the project terms.

**Index** — Git-governed metadata tree recording corpus meaning, evidence,
counts, and canonical object references.

**Ingest recipe** — Strict file that explicitly names acquisition executables
and corpus metadata before WALDO's normal ingestion pipeline.

**Lookaside** — Content-addressed storage for large object bytes. Use this term,
not “store,” for the WALDO domain and command group.

**Manifest** — Schema-1 corpus metadata: identity, description, asserted
license, sources, conversion facts, shards, and totals.

**Materialization** — Fetching and hash-verifying all objects named by a BOM for
export, audit, or training.

**Mirror** — Ordered fallback object location. It preserves object identity and
does not redefine the canonical URL.

**OpenWALDO BOM** — The immutable resolved handoff that pins exact data or model
lineage. For corpus use, it is the boundary consumed by model workflows.

**Origin** — Immutable pinned external model checkpoint lineage recorded before
continued training.

**Reference tokens** — Manifest/record token measure produced by the recorded
corpus tokenizer; not necessarily the exact token budget for a model.

**Rollup / submanifest** — Content-addressed external tree used when a shard
inventory is too large for comfortable Git review.

**Shard** — One bounded canonical Parquet object containing many logical
records.

**Verification** — Tiered proof from local structure through availability and
whole-object SHA-256. Record-level proof is an audit.

