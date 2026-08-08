# Explore an Index

An index checkout is a navigable metadata tree. Commands recurse from the path
you select, so you can work at the whole-index, category, or individual-corpus
level.

```console
$ waldo index list
$ waldo index list science
$ waldo index show science/plos
$ waldo index summary
```

With no configuration, these commands use the managed public checkout at
`~/.waldo/index`. WALDO clones it automatically on first use and safely updates
it before online reads.

## Path resolution

WALDO handles three forms:

- A logical or `./` path such as `science/plos` resolves beneath the checkout
  selected by `config.index`, or beneath managed `~/.waldo/index` when unset.
- An absolute path or a path beginning with `~/` explicitly discovers the
  enclosing checkout by walking upward.
- An omitted path selects the entire resolved index.

The first path to a multi-selection command establishes the checkout. Later
logical paths resolve within that same checkout.

Before online use, WALDO fetches the selected checkout's tracking branch and
fast-forwards only when the worktree is clean and strictly behind. It refuses
dirty, ahead, diverged, or detached states and missing tracking configuration
without modification.
`waldo index pull` runs this explicitly; `index verify --offline` skips it.

## Read the output

`index list` reports path, title, shard/document/token/byte totals, and license.
`index summary` aggregates those measures and partitions totals by license.
These are manifest declarations; use verification or audit to increase the
level of evidence.

`index show` prints navigation entries when a directory contains several
children. When a directory contains exactly one manifest, it shows that corpus
directly.

## Automation

```console
$ waldo --json index list science
$ waldo --json index show science/plos
$ waldo --json index summary science
```

Use JSON for scripts instead of parsing the aligned human-readable tables.
