# Status and Roadmap

This page reflects the implementation inspected on **August 7, 2026**. Check
shipped CLI help and the WALDO repository roadmap for later changes.

## Implemented foundations

- Single-binary bounded-domain architecture and schema-1 compatibility.
- YAML-primary/JSON-compatible index inspection, summary, verification, and
  record-level audit.
- Verified lookaside transport, local/S3 publication, cache, inventory,
  credentials, explicit deletion, and mirrors as read fallbacks.
- Direct and recipe-driven canonical text ingestion, input profiles, recovery,
  append updates, and authoritative rebuild updates.
- Native/JSONL corpus exports with offline-verifiable `EXPORT.json`.
- Model initialization, compatible Hugging Face origin pull, forecasting,
  real MLX/PyTorch/TorchTitan causal training, deterministic evaluation, and
  resumable checkpoints/compose transactions.
- Model chat on compatible MLX, multi-format model export, quantization,
  bounded calibration, EU disclosure JSON, and optional Sigstore signing.

## In progress or bounded

- Useful model operations continue to broaden beyond the initial compatible
  Llama/byte-tokenizer contract.
- Model chat currently requires MLX and performs raw causal continuation.
- Disclosure output is strict JSON; official editable document rendering is
  not implemented.
- Training is causal pre-training/continued pre-training. SFT, preference
  objectives, and pinned chat-template behavior are deferred.

## Reserved but not implemented

- `waldo lookaside mirror`

The concepts have intentional command-tree placement, but no operational
handler in the inspected code.

## Later operational work

The source roadmap identifies operations and transition work after the major
implementation phases: release hardening, public deployment practice, expanded
compatibility fixtures, and community operating procedures. A remote index API,
automated PR creation, and fetcher discovery/install are deliberate non-goals
for the current architecture. The managed public checkout is implemented.
