# Export a Corpus

Export turns one or more verified index selections into a portable directory
with data files and an immutable provenance envelope.

```console
$ waldo index export core/books ./books-export
```

The final positional argument is always the destination. Earlier positional
arguments are recursive selections and are de-duplicated.

## Native or JSONL

```console
$ waldo index export core/books ./books-native --format native
$ waldo index export core/books ./books-jsonl --format jsonl
```

Native export preserves canonical Parquet bytes, so input object and output
file hashes are equal. JSONL streams records through canonical schema-1
serialization, validates every record, and records both source-object and
derived-file identities.

## Select by license

```console
$ waldo index export core science ./permissive \
    --license 'CC0-1.0,CC-BY-*' \
    --exclude-license 'LicenseRef-*'
```

Include and exclude values accept comma-separated shell globs. Exclusions take
precedence. Policy applies to resolved shards and is preserved in the BOM.

## Resume or replace

Matching existing output files resume safely. Conflicting files cause a failure
unless `--force` is supplied. Publication is atomic: scratch downloads are
purged only after the data and `EXPORT.json` are complete.

## Consume elsewhere

```console
$ waldo bom show ./books-native
$ waldo bom verify ./books-native
$ waldo shard audit ./books-native/data
```

Keep `EXPORT.json` with the data. It is the self-contained account of the
selection and materialization.

