# Local Development Setup

## Purpose

Bootstrap a pinned local toolchain that can compile the repository's Daml package, validate `CPL v0.1`, and execute the runtime-foundation smoke scenario from a clean checkout.

## Supported Bootstrap Platforms

- macOS on Apple Silicon (`Darwin-arm64`)
- Linux on `x86_64`

The bootstrap is intentionally repo-local. It installs the Daml SDK and JDK under `.runtime/` and keeps Python validation tooling in `.venv/`.

## Prerequisites

- `curl`
- `tar`
- `git`
- `make`
- `python3`
- `rg`
- either `shasum` or `sha256sum`

## Bootstrap

From the repository root:

```sh
make bootstrap
```

This command:

1. downloads the pinned Daml SDK and Temurin JDK archives from their official release sources
2. verifies the download checksums
3. installs the tools under `.runtime/`
4. creates `.venv/` and installs the pinned CPL validation dependency

## Daily Commands

```sh
make status
make validate-cpl
make daml-build
make demo-run
make verify
```

What each command does:

- `make status`: show pinned versus installed tool versions, scaffold presence, and git state
- `make validate-cpl`: validate `CPL v0.1` schema and the published example policies
- `make daml-build`: compile the repository's Daml package into `.daml/dist/`
- `make demo-run`: execute the minimal `Bootstrap:foundationSmokeTest` Daml script
- `make verify`: run the full runtime-foundation verification loop

## Runtime Layout

- `.runtime/bin/`: repo-local `daml`, `daml-helper`, `java`, and `javac` entry points
- `.runtime/tools/`: extracted pinned SDK and JDK archives
- `.runtime/downloads/`: cached upstream tarballs
- `.venv/`: pinned schema-validation tooling
- `.daml/dist/`: generated DAR artifacts from `make daml-build`

## Notes

- The current Daml package is intentionally minimal. It proves compilation and execution only; it does not implement collateral policy or settlement behavior.
- Future Quickstart or Canton overlay assets should land under `infra/`, not inside the Daml or app package trees.
- If the toolchain needs to be rebuilt from scratch, run `make clean-runtime` and then `make bootstrap`.
