# Inspect Local Shards

Shard commands work directly on local canonical Parquet files. They need no
index checkout or configured lookaside.

```console
$ waldo shard summary ./data
$ waldo shard audit ./data --workers 4
$ waldo shard list-records ./data/object.parquet
$ waldo shard export-record ./data/object.parquet <record-id>
```

Summary uses trusted canonical footer metadata when complete and otherwise
scans records. It aggregates shard, record, token, content-byte, encoded-byte,
row-group, license, and writer-recipe information.

Audit streams every record, recomputes content SHA-256 and reference token
counts, validates required fields, and detects duplicate IDs across the entire
selection. Paths can be files, directories, or glob patterns; directories are
scanned recursively for `.parquet` files.

`list-records` emits compact IDs and metadata from one shard. `export-record`
writes the selected record's text to standard output, which makes it suitable
for redirection or piping without extra labels.

