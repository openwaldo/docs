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

## Get the public index

```console
$ git clone https://github.com/openwaldo/waldo-index.git
$ waldo config set index "$PWD/waldo-index"
$ waldo index summary
```

An explicit filesystem path always discovers its enclosing checkout. A logical
path such as `science/plos` uses the checkout containing the current directory,
then the configured `index` path.

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

