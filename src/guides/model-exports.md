# Model Exports and Disclosures

Model export selects the current verified open-weight origin or newest complete
real run and publishes a new directory atomically. Every format contains
`BOM.json` and `EU-BOM.json`.

```console
$ waldo model export small ./small-waldo
$ waldo model export small ./small-hf --format huggingface
$ waldo model export small ./small-mlx --format mlx
$ waldo model export small ./small-gguf --format gguf
$ waldo model export small ./small-ollama --format ollama
```

| Format | Purpose | Weight behavior |
| --- | --- | --- |
| `waldo` | Authoritative archive and WALDO interchange | Complete managed tree |
| `huggingface` | Transformers package | Tensor bytes preserved; names/header mapped |
| `mlx` | MLX/MLX-LM package | Tensor bytes preserved; names/header mapped |
| `gguf` | llama.cpp-compatible inference | GGUF v3 conversion |
| `ollama` | Ollama import | GGUF plus `Modelfile` |

The native package retains complete run history. A derived package carries a
compact format-specific artifact inventory and the SHA-256 of its source model
BOM. Keep or publish the native package when consumers need self-contained full
provenance rather than a cryptographic link to separately retained history.

## Quantization and calibration

```console
$ waldo model export small ./small-q4 \
    --format gguf --quant 4 --calibration core/books
```

Quant levels map to llama.cpp recipes: 2→`Q2_K`, 3→`Q3_K_M`, 4→`Q4_K_M`,
5→`Q5_K_M`, 6→`Q6_K`, and 8→`Q8_0`. The unquantized GGUF conversion preserves
matrix precision and promotes one-dimensional normalization weights to F32.

Calibration deterministically selects a bounded 100,000-byte-token sample from
one verified index selection and measures numerical sensitivity. It performs no
gradients or optimization and does not train the model. Executable identities,
sample selection, hashes, and source corpus BOM evidence are embedded in the
release BOM.

## EU GPAI disclosure

Provider-level facts are configured once:

```console
$ waldo config set disclosure.provider ./provider.json
$ waldo bom export small ./training-content.json \
    --format eu-gpai --provider ./provider.json
```

Normal model export fails closed if required disclosure facts are missing.
`--allow-incomplete` produces a conspicuously marked development draft. WALDO
currently emits strict JSON evidence, not the official editable Word document,
and does not make a legal compliance finding.

## Signing

Unsigned export is allowed with a warning. Once signing is configured, it is
automatic and fail-closed:

```console
$ waldo config set signing.method sigstore-keyless
```

or:

```console
$ waldo config set signing.method sigstore-key
$ waldo config set signing.key /secure/path/cosign.key
```

`cosign` must be on `PATH`. Successful signing adds detached
`BOM.sigstore.json` and `EU-BOM.sigstore.json` bundles. Consumers must apply an
appropriate identity and issuer policy when verifying keyless signatures.

## Typical consumer checks

For a native package, inspect `BOM.json`, verify all referenced paths and
hashes, and retain the EU projection beside it. For a derived release, verify
each `artifacts` entry and obtain the source model BOM matching
`source_bom_sha256` when full lineage is required.

