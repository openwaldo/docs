# Explore an Index

An index checkout is a navigable metadata tree. Commands recurse from the path
you select, so you can work at the whole-index, category, or individual-corpus
level.

```console
$ waldo index list /path/to/waldo-index
$ waldo index list /path/to/waldo-index/science
$ waldo index show /path/to/waldo-index/science/plos
$ waldo index summary /path/to/waldo-index
```

## Path resolution

WALDO handles three forms:

- An absolute path or `./relative/path` discovers the enclosing checkout by
  walking upward, like Git.
- A logical path such as `science/plos` uses the current enclosing checkout.
- If the current directory is not in a checkout, a logical or omitted path uses
  the configured `index` value.

The first path to a multi-selection command establishes the checkout. Later
logical paths resolve within that same checkout.

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

