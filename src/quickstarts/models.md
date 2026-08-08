# Training Quickstart

This guide is the shortest safe path from a WALDO installation to a local
model, a recorded training run, and a portable release. It covers both starting
from a blank architecture and using compatible open weights.

> Training uses real compute and can move substantial data. Inspect and
> forecast the exact corpus selection before starting a run. Never omit the
> selection unless you intentionally want the entire public index.

## 1. Compile and install WALDO system-wide

WALDO currently requires Go 1.25 or newer.

```console
$ git clone https://github.com/openwaldo/waldo.git
$ cd waldo
$ go build -o ./waldo ./cmd/waldo
$ sudo install -m 0755 ./waldo /usr/local/bin/waldo
$ waldo --version
```

The commands above are for a regular user. When already operating as root, use:

```console
# go build -o ./waldo ./cmd/waldo
# install -m 0755 ./waldo /usr/local/bin/waldo
```

Both forms install the executable at `/usr/local/bin/waldo`, which is normally
on the system-wide command path.

## 2. Optional: install for one user and persist PATH

When system-wide installation is unavailable, install beneath your home
directory:

```console
$ mkdir -p "$HOME/.local/bin"
$ go build -o "$HOME/.local/bin/waldo" ./cmd/waldo
```

Add the following line to your shell startup file, not only to the current
terminal:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Use `~/.zshrc` for zsh, `~/.bashrc` for bash, or `~/.profile` for a POSIX login
shell, then start a new terminal and run `waldo --version`.

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

## 3. Use the managed public index

Normal model users do not clone or configure an index:

```console
$ waldo index list core/common-pile
$ waldo index show core/common-pile/public-domain-review
```

On a fresh installation, `config.index` is unset by default. WALDO therefore
clones the public index into the managed, read-only
`~/.waldo/index` checkout on first use. Online commands then fetch and
fast-forward it automatically when safe. `waldo index pull` performs the same
synchronization explicitly.

If this machine was previously configured for contribution work, return to the
managed default with `waldo config unset index`.

Relative paths resolve beneath that managed checkout. An omitted selection
means the entire resolved index, including for `model forecast` and
`model train`.

## 4. Check the training plan before creating state

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

## 5. Select a real backend

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

## 6. Recommended: define training with a compose

A model compose is the primary reproducible training interface. It pins the
architecture, ordered corpus stages, objective, tokenizer, and training
parameters in strict YAML or JSON. Create `model.yaml`:

```yaml
kind: waldo-model-compose
schema: 1

architecture:
  family: decoder-transformer
  context_tokens: 512
  vocabulary_size: 259
  hidden_size: 384
  intermediate_size: 1024
  layers: 6
  attention_heads: 6
  key_value_heads: 2
  tie_embeddings: true
  parameter_dtype: bfloat16
  tokenizer:
    name: byte
    revision: builtin-byte-schema-1

stages:
  - name: pretrain
    type: pre-training
    objective: causal-language-modeling
    corpora:
      - core/common-pile/public-domain-review
    parameters:
      profile: causal-pretrain-v1
      steps: 1000
      batch_size: 1
      sequence_length: 256
      learning_rate: 0.0003
      seed: 7
      checkpoint_every: 100
      evaluate_every: 100
```

Forecast the complete declared plan, then run it:

```console
$ waldo model forecast ./model.yaml
$ waldo model compose quickstart-compose ./model.yaml
$ waldo model summary quickstart-compose
$ waldo model bom quickstart-compose ./quickstart-compose-bom.json
```

WALDO rejects unknown fields, incomplete architectures, empty corpus
selections, duplicate stage names, unsupported objectives, and invalid
parameters before training. It preflights every stage and pins the compose and
each corpus BOM in a durable transaction. Repeating the same command after an
interruption resumes verified staged work. Use `--replace` only when
intentionally replacing an existing model; the old model remains published
until every stage succeeds.

To continue from compatible pulled weights, add a `base` block. The named base
is verified and never mutated:

```yaml
base:
  model: base-model
  origin_sha256: <origin-bom-sha256>
```

Compose files deliberately omit machine-local framework choices. The same file
can use MLX, PyTorch, or TorchTitan according to `model.backend` on the host.

## 7. Direct training by corpus

Direct training remains useful for a short experiment. Initialize an immutable
architecture, then train it on the inspected selection:

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

## 8. Generate with compatible weights

After a complete real run:

```console
$ waldo model chat quickstart-10m "Once upon a time"
$ waldo model chat quickstart-10m
```

Generation currently requires compatible MLX. WALDO's built-in pretrained
models perform raw causal continuation and carry no chat template; they are not
instruction-tuned assistants. Interactive mode supports `/clear`, `/help`, and
`/exit`.

## 9. Alternative: start from open weights

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

## 10. Export a release

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
| Run the recommended reproducible plan | `waldo model compose <name> <file>` |
| Inspect lineage | `waldo model summary <name>` / `waldo model bom <name>` |
| Generate | `waldo model chat <name> [prompt]` |
| Publish | `waldo model export <name> <directory>` |
