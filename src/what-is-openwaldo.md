# What OpenWALDO Is

OpenWALDO is both a public training-data commons and the toolchain that makes
the commons independently inspectable.

The name expands the parts of AI that the project aims to keep connected:
**Open Weights, Open Artifacts, Open Licenses, Open Data, and Open Origins.**

## Who it serves

| Role | Primary goal |
| --- | --- |
| Data consumer | Select, verify, and export suitable corpora. |
| Corpus contributor | Turn acquired material into a reviewable, signed-off index change. |
| Model builder | Bind exact training data and starting weights to runs and releases. |
| Curator | Review metadata, evidence, licenses, and namespace changes in Git. |
| Storage operator | Maintain object availability without controlling corpus meaning. |

## Questions WALDO helps answer

- Which index revision and paths were selected?
- Which manifests, sources, asserted licenses, and conversion recipes applied?
- Did fetched object bytes match their declared hashes?
- Which exact records and totals were audited?
- What starting model and training plan preceded a result?
- What did the backend report consuming and producing?
- Which artifact hashes belong to a model release?

## What it deliberately does not claim

A valid BOM does not prove that a source license assertion is correct. A hash
proves identity and integrity, not permission. A recorded training run does not
prove an untrusted backend consumed every declared byte. A generated EU
disclosure is evidence preparation, not a legal compliance determination.

OpenWALDO keeps those boundaries visible because trustworthy infrastructure is
more useful when its claims are precise.

