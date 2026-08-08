# Trust and Verification Boundaries

WALDO separates recorded assertions from machine-verifiable evidence. The
distinction is essential when interpreting any result.

| Evidence | What it supports | What it does not prove |
| --- | --- | --- |
| Git commit and DCO sign-off | Reviewable attributable metadata change | Truth of every submitted claim |
| Source URL and acquisition hash | Specific recorded upstream evidence | Continuing availability or legal rights |
| Object SHA-256 | Identity and integrity of fetched bytes | Safety, quality, license correctness |
| Record audit | Canonical schema/content consistency | Factual correctness of document text |
| Corpus BOM | Exact resolved selection and declarations | Consumption by an untrusted trainer |
| Run observation | What the backend reported | Attested execution unless separately proven |
| Artifact inventory | Release-file integrity | Model safety or fitness |
| Sigstore bundle | Issuer identity under verifier policy | Regulatory compliance |

## Fail-closed boundaries

WALDO rejects malformed schemas, mismatched hashes, unsafe export paths,
unsupported model contracts, unusable real backends, incomplete required
disclosures, and configured signing failures. Consequential mutation commands
preflight their complete target sets where possible.

## Fetcher execution

An ingest recipe explicitly authorizes named external executables. WALDO hashes
them and constrains which produced files enter ingestion, but does not sandbox
their process permissions, network access, or inherited environment. Review a
recipe and scripts before running them.

## Credentials and secrets

Corpus meaning never contains machine credentials. Interactive S3 keys are kept
in a protected local credential file; environment and workload credentials can
remain external. Recipe environment values are inherited but never written to
manifests. Avoid putting secrets in command arguments or recipe files.

## Deletion

Content addressing makes references durable and distributed. An object absent
from one current index can still be named by another index, historical commit,
export, or model BOM. WALDO therefore supports only explicit full-hash lookaside
removal and provides no index-free garbage collection.

## Legal and regulatory interpretation

Licenses are asserted identifiers attached to attributable evidence. Policy
filters make selection reproducible; they are not legal advice. Disclosure
generation reports gaps and maps available facts; users remain responsible for
legal review and the official submission process.

