# Local Development Setup

## Purpose

Bootstrap a pinned local toolchain that can compile the repository's Daml package, validate `CPL v0.1`, evaluate the first policy-engine path, and execute the initial Daml workflow smoke scenario from a clean checkout.

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
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
make daml-build
make daml-test
make demo-run
make verify
```

What each command does:

- `make status`: show pinned versus installed tool versions, scaffold presence, and git state
- `make validate-cpl`: validate `CPL v0.1` schema and the published example policies
- `make policy-eval`: validate a policy input, evaluate candidate inventory, and validate the generated `PolicyEvaluationReport`
- `make test-policy-engine`: run deterministic policy-engine tests and regenerate the committed example report artifact
- `make daml-build`: compile the repository's Daml package into `.daml/dist/`
- `make daml-test`: run the Daml lifecycle scripts for margin call, posting, substitution, and return skeletons
- `make demo-run`: execute the aggregate `Bootstrap:workflowSmokeTest` Daml script
- `make verify`: run the full verification loop across docs, CPL validation, policy-engine tests, Daml build, Daml tests, and smoke execution

## Runtime Layout

- `.runtime/bin/`: repo-local `daml`, `daml-helper`, `java`, and `javac` entry points
- `.runtime/tools/`: extracted pinned SDK and JDK archives
- `.runtime/downloads/`: cached upstream tarballs
- `.venv/`: pinned schema-validation tooling
- `.daml/dist/`: generated DAR artifacts from `make daml-build`

## Notes

- The current repository now includes an initial deterministic policy engine and initial Daml workflow skeletons, but it still does not implement optimization, live asset adapters, or settlement-window enforcement.
- Future Quickstart or Canton overlay assets should land under `infra/`, not inside the Daml or app package trees.
- If the toolchain needs to be rebuilt from scratch, run `make clean-runtime` and then `make bootstrap`.
