# Install WALDO

WALDO currently requires Go 1.25 or newer and is installed from source.

```console
$ git clone https://github.com/openwaldo/waldo.git
$ cd waldo
$ go install ./cmd/waldo
$ WALDO_GOBIN="$(go env GOBIN)"
$ [ -n "$WALDO_GOBIN" ] || WALDO_GOBIN="$(go env GOPATH)/bin"
$ export PATH="$WALDO_GOBIN:$PATH"
$ waldo --version
$ waldo --help
```

Add the resolved Go binary directory to your shell startup file for future
sessions.

## Use the public index

```console
$ waldo index summary
$ waldo index list science
```

No index setup is required for reading. On first use, WALDO clones branch
`main` from `https://github.com/openwaldo/waldo-index.git` to the managed,
read-only `~/.waldo/index` checkout using its built-in Go Git client. Later
read commands fetch and fast-forward it automatically when safe.

Set `config.index` only when you have a separate writable contributor checkout.
Relative corpus paths then resolve beneath that checkout. Absolute and `~/`
paths explicitly select another checkout.

## Inspect machine defaults

```console
$ waldo config get
$ waldo lookaside status
```

By default, managed models live in `~/.waldo/models`, verified retained objects
in `~/.waldo/cache`, and temporary recovery/download state below the operating
system's user-scoped temporary directory. The cache is bounded to 20 GiB.

## Structured output

Place the global option before the command:

```console
$ waldo --json index summary science
```

Stable result JSON is written to standard output. Progress remains on standard
error, allowing automation to capture the result without losing visibility.
