# Contributing

OpenWALDO needs corpus curation, software, documentation, testing, storage, and
review. Start in the repository that owns the fact you want to change.

## Corpus contributions

1. Establish source and license evidence.
2. Acquire locally, directly or through a reviewed recipe.
3. Run ingestion dry-run and inspect the immutable plan.
4. Ingest through a configured writable lookaside.
5. Review generated manifest and navigation changes.
6. Verify the new selection, run `git diff --check`, and commit with `-s`.
7. Open a pull request explaining source, selection, license assertion,
   conversion, and validation.

Never commit large shard bytes, credentials, environment values, or private
staging paths to the index.

## WALDO code

Begin with `VISION.md`, `docs/UX.md`, `docs/ARCHITECTURE.md`, and
`docs/COMPATIBILITY.md`. Preserve domain dependency direction and record durable
decisions in an ADR. Keep work in small vertical slices with observable commands
and tests.

Before handing off a code change:

```console
$ gofmt -w .
$ ./testing/all.sh
```

Do not advertise planned commands as working. Error messages should name the
failed object/path and a useful next action.

## Documentation

Edit ordinary Markdown under `src/`, add the page to `src/SUMMARY.md`, and keep
examples aligned with current `waldo ... --help`. Prefer runnable examples,
explicit side effects, small diagrams, and links to prerequisite concepts.

Before submitting:

```console
$ mdbook build
$ git diff --check
```

Also inspect internal Markdown links and preview narrow/wide layouts. A behavior
change should update its guide and reference in the same development window.

## DCO sign-off

All contribution commits should include a `Signed-off-by` trailer:

```console
$ git commit -s -m "Describe the change"
```

The sign-off attaches an accountable identity to the contribution. Use your
real authorship identity and ensure you have the right to submit the work.

