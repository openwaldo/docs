# Index and Manifest Format

The index is a Git-managed tree of schema-1 YAML or JSON files. YAML is primary
for new writes; existing schema-1 JSON remains readable.

## Directory index

Each navigable directory contains exactly one `index.yaml`, `index.yml`, or
`index.json`:

```yaml
kind: index
schema: 1
path: science
entries:
  - name: plos
    type: dir
  - name: overview.yaml
    type: manifest
```

Entries name a child directory or manifest. Navigation is generated metadata;
the manifests are authoritative for corpus meaning. Competing navigation files
in one directory are rejected.

## Corpus manifest

```yaml
kind: manifest
schema: 1
name: example
title: Example Corpus
description: A small illustrative corpus.
license: CC-BY-4.0
sources:
  - name: example-upstream
    source: example
    version: "2026-08 snapshot"
    url: https://example.org/data
    category: public-dataset
    sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
converted_by:
  tool: waldo index ingest
  version: 0.1.0-dev
  profile: canonical-text-schema-1@sha256:...
  recipe: parquet-go/.../v4
  tokenizer: tiktoken/cl100k_base
record_schema: 1
shards:
  - url: s3://bucket/lookaside/ab/cd/abcdef...
    sha256: abcdef...
    sources: [example-upstream]
    docs: 100
    tokens: 42000
    bytes: 123456
```

Core fields record corpus identity, human description, asserted default license,
source evidence, conversion identity, record schema, and shards. Shards may
override inherited license or conversion fields.

Source records can add collection periods, content types, languages,
geographies, tri-state data declarations, modality usage, acquisition facts,
and domain measures. Processing can record filtering, rights-reservation, and
illegal-content measures. These facts support deeper provenance and disclosure;
absence is not silently converted to a claim.

## Large shard lists

Schema-1 `shards` is polymorphic. It can be an inline array or a rollup object
pointing to a content-addressed submanifest tree:

```yaml
shards:
  url: https://example.org/manifests/root.json
  sha256: 0123...
  count: 1000
  docs: 75000000
  tokens: 120000000000
  bytes: 160000000000
```

Offline summary can use Git-pinned aggregates. Object-enabled operations verify
and recursively expand the submanifest nodes before materialization. Each node
pins its parent relationship and aggregate totals in the resolved BOM.

## Git identity

Git governs review, attribution, history, and namespace. A BOM records remote,
commit, and dirty-checkout state, while individual manifest hashes remain exact
pins even when Git identity is missing or the tree is dirty.

Schema version changes require a reader and migration story. Additive unknown
fields are accepted; changed meaning or relaxed identity invariants require a
new schema.

