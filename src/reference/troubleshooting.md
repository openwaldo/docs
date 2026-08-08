# Troubleshooting

## WALDO cannot discover an index

Pass an absolute checkout/subtree/manifest path or configure one:

```console
$ waldo config set index /absolute/path/to/waldo-index
$ waldo index summary
```

Logical paths require the current or configured checkout.

## Default verify works but object verification fails

Default verification proves canonical URL reachability and declared size, not
the body hash. Check the reported URL/hash, credentials, proxy, disk space, and
scratch path. Run `waldo lookaside status`, then retry `--objects`.

## Full audit says the cache is too small

Audit materializes the complete selection. Set a sufficiently large bound in an
isolated config or audit a smaller subtree:

```console
$ export WALDO_CONFIG=/tmp/waldo-audit-config.json
$ waldo config set index /path/to/waldo-index
$ waldo config set lookaside.cache /large/disk/waldo-cache
$ waldo config set lookaside.cache.max-size 200GiB
```

## Ingestion refuses the destination

New ingestion requires a destination not already indexed. Use `index update`
for an existing manifest. Ensure the checkout is clean enough for WALDO to pin
and present a reviewable overlay, and run `--dry-run` to expose preflight errors.

## Recipe command is missing or changed

Bare commands resolve through `PATH`; paths containing separators resolve from
the recipe file. Make the file executable. WALDO rejects a command whose bytes
change during the run—restore the reviewed version and retry.

## S3 login fails

Confirm `lookaside` is an `s3://` URL and the region is correct. Credentials
must permit the probe's write, list, inspect, read, and delete operations beneath
the configured prefix. WALDO stores credentials only after all checks succeed.

## Training backend is unavailable

`auto` requires usable MLX on Apple Silicon or TorchTitan/PyTorch on Linux.
WALDO tests a real operation on the target device. Follow the command's official
installation guidance, verify the selected Python/device independently, or set
an explicit backend. Do not use `fake` for release training.

## An interrupted run does not resume

Resume requires an identical corpus, parameters, profile, backend revision, and
execution environment. Changed inputs intentionally create a new run. Inspect
`model summary` and `RUN.json` for the prior attempt and checkpoint state.

## Model export reports missing disclosure facts

Set `disclosure.provider` or pass `--provider`. Missing corpus evidence can only
be fixed at its authoritative metadata source. Use `--allow-incomplete` only for
a clearly marked development artifact.

## A documented command has no handler

`index remove` and `lookaside mirror` are currently reserved placeholders. The
CLI prints them as planned vocabulary, but they are not operational yet.

