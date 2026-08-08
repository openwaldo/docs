# Configuration Reference

Configuration describes machine-local transport and execution preferences. Set
corpus meaning only through reviewed index metadata.

```console
$ waldo config show
$ waldo config get
$ waldo config get lookaside
$ waldo config get lookaside.region
```

`WALDO_CONFIG` overrides the configuration file path, which is useful for CI,
tests, and isolated operations.

| Key | Meaning | Default/constraint |
| --- | --- | --- |
| `index` | Default local index checkout | Unset |
| `lookaside` | Writable `s3://` or `file://` URL | Unset |
| `lookaside.region` | AWS region when not inferred | Unset |
| `lookaside.workers` | Concurrent completed-shard uploads | 1–32 |
| `lookaside.mirrors` | Ordered fallback read URLs | Empty; set replaces list |
| `lookaside.cache` | Retained verified objects | `~/.waldo/cache` |
| `lookaside.cache.max-size` | Cache retention bound | `20GiB` |
| `lookaside.scratch` | Partial downloads | User-scoped system temp |
| `ingest.staging` | Ingestion recovery state | User-scoped system temp |
| `model.root` | Durable model tree | `~/.waldo/models` |
| `model.backend` | Training backend policy | `auto`; also `mlx`, `torchtitan`, `pytorch`, `fake` |
| `disclosure.provider` | Strict provider facts JSON | Unset |
| `signing.method` | Automatic export signing | Unset; `sigstore-keyless` or `sigstore-key` |
| `signing.key` | Private key for key signing | Required with `sigstore-key` |

Examples:

```console
$ waldo config set index /data/waldo-index
$ waldo config set lookaside.cache /fast/waldo-cache
$ waldo config set lookaside.cache.max-size 100GiB
$ waldo config set lookaside.mirrors https://mirror-a.example https://mirror-b.example
$ waldo config unset model.backend
```

S3 secret keys do not belong in configuration. Use `waldo lookaside login`,
the AWS default credential chain, or workload roles.

