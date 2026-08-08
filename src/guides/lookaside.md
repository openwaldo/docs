# Operate Lookaside Storage

Lookaside storage serves immutable objects. The configured writable location,
retained verified cache, and partial-download scratch directory are distinct.

## Configure local or S3 publication

```console
$ waldo config set lookaside file:///absolute/path/to/objects
$ waldo config set lookaside.workers 4
```

For S3:

```console
$ waldo config set lookaside s3://bucket/prefix
$ waldo config set lookaside.region us-east-2
$ waldo lookaside login
```

Login verifies write/list/inspect/read/delete access with a tiny probe before
storing bucket-scoped credentials in `~/.waldo/credentials` with mode `0600`.
If no WALDO login exists, standard AWS environment, shared-file, and workload
role credentials remain available.

## Inspect and scrub

```console
$ waldo lookaside status
$ waldo lookaside list
$ waldo lookaside list science/plos
$ waldo lookaside list science/plos --all
$ waldo lookaside verify
```

`list` inventories without downloading bodies. With an index path it shows
matching hashes; `--all` also shows unmatched objects. Unmatched never means
unreferenced globally.

`verify` scrubs retained cache objects against their hashes and reports
corruption. It does not audit Parquet records.

## Mirrors

Configure ordered read fallbacks with `lookaside.mirrors`. Mirrors improve
availability but do not replace canonical URL checks or change object identity.
The `waldo lookaside mirror` command is present in the command vocabulary but
does not yet have an implementation.

## Explicit deletion only

```console
$ waldo lookaside rm <64-character-sha256> [more-sha256...]
```

Every full hash is preflighted before deletion begins. WALDO rejects URLs,
prefixes, and globs and has no reachability-based garbage collector. Determine
references across indexes, historical revisions, and BOM archives before
removing an object.

