# Verify and Audit

Verification is tiered so users can match cost to the question being asked.

| Command | Metadata | Network headers | Object hashes | Every record | Cross-shard duplicates |
| --- | --- | --- | --- | --- | --- |
| `index verify --offline` | Yes | No | No | No | No |
| `index verify` | Yes | Yes | No | No | No |
| `index verify --objects` | Yes | Yes | Yes | No | No |
| `index audit` | Yes | Yes | Yes | Yes | Yes |

## Structural verification

```console
$ waldo index verify science/plos --offline
```

This checks schema kinds and versions, navigation, manifest inheritance,
references, hashes, counts, and other local invariants. It performs no network
requests and is appropriate for review and CI.

## Availability verification

```console
$ waldo index verify science/plos
```

The default additionally checks each canonical URL and declared size using
HTTP/S3 headers or local file metadata. A mirror does not hide an unavailable
canonical URL at this level.

## Object verification

```console
$ waldo index verify science/plos --objects
```

WALDO downloads each selected object, streams SHA-256 verification, and purges
successful scratch data. This proves the fetched bytes match the manifest but
does not validate each record inside the Parquet file.

## Full audit

```console
$ waldo index audit science/plos --workers 4
```

Audit recomputes record text hashes and reference token counts, checks required
fields and metadata, detects duplicate record IDs across shards, and reconciles
documents, tokens, and encoded bytes with the BOM. Worker count is 1–32; the
automatic value is conservatively bounded.

Audit materializes the complete selection simultaneously. If the retained cache
bound is smaller than the declared corpus bytes, WALDO fails early and explains
how large `lookaside.cache.max-size` must be. Use a dedicated `WALDO_CONFIG` when
temporarily changing that bound for an operational audit.

