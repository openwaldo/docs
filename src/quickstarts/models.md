# Training Quickstart

This guide is the shortest safe path from a WALDO installation to a local
model, a recorded training run, and a portable release. It covers both starting
from a blank architecture and using compatible open weights.

> Training uses real compute and can move substantial data. Inspect and
> forecast the exact corpus selection before starting a run. Never omit the
> selection unless you intentionally want the entire public index.

## 1. Install WALDO

WALDO currently requires Go 1.25 or newer.

```console
$ git clone https://github.com/openwaldo/waldo.git
$ cd waldo
$ go install ./cmd/waldo
$ WALDO_GOBIN="$(go env GOBIN)"
$ [ -n "$WALDO_GOBIN" ] || WALDO_GOBIN="$(go env GOPATH)/bin"
$ export PATH="$WALDO_GOBIN:$PATH"
$ waldo --version
```

Models default to `~/.waldo/models`; verified corpus objects default to the
20 GiB bounded cache at `~/.waldo/cache`. Inspect or change those locations
before a large run:

```console
$ waldo config get model
$ waldo config get lookaside.cache
$ waldo config set model.root /fast-disk/waldo-models
$ waldo config set lookaside.cache /fast-disk/waldo-cache
$ waldo config set lookaside.cache.max-size 100GiB
```

## 2. Use the managed public index

Normal model users do not clone or configure an index:

```console
$ waldo config unset index
$ waldo index list core/common-pile
$ waldo index show core/common-pile/public-domain-review
```

With `index` unset, WALDO clones the public index into the managed, read-only
`~/.waldo/index` checkout on first use. Online commands then fetch and
fast-forward it automatically when safe. `waldo index pull` performs the same
synchronization explicitly.

Relative paths resolve beneath that managed checkout. An omitted selection
means the entire resolved index, including for `model forecast` and
`model train`.

## 3. Check the training plan before creating state

The small public-domain-review corpus is useful for a first lifecycle run:

```console
$ waldo index summary core/common-pile/public-domain-review
$ waldo index verify core/common-pile/public-domain-review
$ waldo model forecast core/common-pile/public-domain-review
```

Default verification validates metadata plus canonical object reachability and
declared sizes without downloading object bodies. Forecast recommends a model
rung and lists only hardware configurations expected to fit. Neither command
creates model state.

## 4. Select a real backend

```console
$ waldo config set model.backend auto
```

`auto` selects MLX on Apple Silicon. On Linux it prefers an installed
TorchTitan environment and then PyTorch. WALDO proves a real operation on the
selected device before it writes a run. If no backend is usable, it fails with
installation guidance instead of silently simulating training.

The explicit `fake` backend is only for deterministic development tests. Its
artifacts are permanently marked simulated and cannot become real release
weights.

## 5. Build a small model from scratch

Initialize an immutable architecture, then train it on the inspected selection:

```console
$ waldo model init quickstart-10m --preset 10m
$ waldo model train quickstart-10m \
    core/common-pile/public-domain-review \
    --epochs 1
$ waldo model summary quickstart-10m
$ waldo model bom quickstart-10m ./quickstart-10m-bom.json
```

Training resolves an immutable corpus BOM, downloads and audits hash-verified
Parquet, counts exact model-token targets, pins a deterministic held-out set,
writes the run plan, and only then launches the backend. The run history is
append-only. Repeating the identical command after an interruption resumes a
valid checkpoint; changed inputs or parameters create a new run.

Built-in presets are `10m`, `35m`, `90m`, `300m`, `1b`, `3b`, `7b`, `13b`,
`34b`, and `70b`. A larger preset is not automatically better for a fixed data
or hardware budget - use forecast first.

## 6. Generate with compatible weights

After a complete real run:

```console
$ waldo model chat quickstart-10m "Once upon a time"
$ waldo model chat quickstart-10m
```

Generation currently requires compatible MLX. WALDO's built-in pretrained
models perform raw causal continuation and carry no chat template; they are not
instruction-tuned assistants. Interactive mode supports `/clear`, `/help`, and
`/exit`.

## 7. Alternative: start from open weights

Instead of initializing blank weights, pull a compatible Hugging Face
Safetensors model:

```console
$ waldo model pull base-model \
    huggingface://organization/model@immutable-or-named-reference
$ waldo model summary base-model
$ waldo model train base-model \
    core/common-pile/public-domain-review \
    --epochs 1
```

WALDO resolves the provider reference to an immutable revision, hashes every
source artifact, validates architecture, tokenizer, names, shapes, and
precision, and records `ORIGIN-BOM.json`. Private or gated repositories use
`HF_TOKEN` or the standard Hugging Face token file.

Current pull support is intentionally narrow: standard bias-free Llama weights
using the OpenWALDO byte tokenizer and F32, F16, or BF16 tensors. Incompatible
models fail before publication rather than being silently converted.

## 8. Use a compose for reproducible stages

Direct `model train` is the shortest path. Use a strict model compose when you
need a reusable architecture, optional pinned base, ordered corpora, explicit
steps, batch size, sequence length, learning rate, seed, checkpoint interval,
or evaluation interval:

```console
$ waldo model forecast ./model.yaml
$ waldo model compose composed-model ./model.yaml
```

The compose describes portable model intent, not a machine-local framework.
`--replace` keeps the old published model in place until every replacement
stage completes.

## 9. Export a release

Model export requires provider disclosure facts:

```console
$ waldo config set disclosure.provider ./provider.json
$ waldo model export quickstart-10m ./quickstart-waldo
$ waldo model export quickstart-10m ./quickstart-hf \
    --format huggingface
$ waldo model export quickstart-10m ./quickstart-gguf \
    --format gguf
```

Available formats are WALDO, Hugging Face, MLX, GGUF, and Ollama. Every package
contains `BOM.json` and `EU-BOM.json`. Normal export fails when required
disclosure facts are absent; `--allow-incomplete` is only for a conspicuously
marked development draft. Configured Sigstore signing is automatic and
fail-closed.

The native WALDO package is the self-contained provenance archive. Derived
runtime packages retain artifact hashes and a hash link to the source model
BOM.

## Quick command map

| Goal | Command |
| --- | --- |
| Discover public corpora | `waldo index list` |
| Refresh the selected index | `waldo index pull` |
| Estimate hardware and duration | `waldo model forecast <selection>` |
| Start blank | `waldo model init <name> --preset 10m` |
| Start from compatible weights | `waldo model pull <name> <source>` |
| Train one or more selections | `waldo model train <name> <paths...>` |
| Run a reusable plan | `waldo model compose <name> <file>` |
| Inspect lineage | `waldo model summary <name>` / `waldo model bom <name>` |
| Generate | `waldo model chat <name> [prompt]` |
| Publish | `waldo model export <name> <directory>` |
