# Update a Corpus

`index update` has two intentionally different meanings: append new content or
authoritatively rebuild all shards.

## Append and deduplicate

```console
$ waldo index update ./new-input science/example/example.yaml --dry-run
$ waldo index update ./new-input science/example/example.yaml
```

Normal update audits existing shards and seeds their exact record identities
into a disk-backed set. It publishes only records not already present. This is
the safe choice for incremental upstream additions.

Direct input accepts the same metadata options as ingestion when new source
facts must be recorded. A recipe remains the complete owner of its metadata.

## Authoritative rebuild

```console
$ waldo index update ./complete-input science/example/example.yaml \
    --rebuild-shards --dry-run
```

`--rebuild-shards` says the supplied input is the complete authoritative
corpus. WALDO does not download old shards; it replaces the manifest's source
and shard set after processing the new input. Use this only when that semantics
is true.

## Transaction and review

Both modes pin the original manifest, use the normal streaming publication
journal, and write touched metadata as schema-1 YAML. When old JSON/YML files
are superseded, WALDO lists them for removal. Inspect those removals and all
navigation changes before committing.

Old lookaside objects are not automatically deleted. Historical Git revisions,
other indexes, or exported BOMs may still reference them.

