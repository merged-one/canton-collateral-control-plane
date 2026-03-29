# Local Development Setup

## Purpose

Bootstrap a pinned local toolchain that can compile the repository's Daml package, validate `CPL v0.1`, evaluate the first policy-engine path, optimize the first collateral-allocation path, execute the initial Daml workflow smoke scenario, run the first end-to-end margin-call, return, and substitution demos from a clean checkout, and stage the first pinned Quickstart-based LocalNet foundation.

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
- Docker plus Docker Compose for the Quickstart LocalNet foundation commands and the full `make verify` target; `make verify-portable` does not require Docker

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
make localnet-bootstrap
make localnet-smoke
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-policy-engine
make test-optimizer
make daml-build
make daml-test
make demo-run
make demo-margin-call
make demo-return
make demo-substitution
make test-conformance
make demo-all
make verify-portable
make verify
```

What each command does:

- `make status`: show pinned versus installed tool versions, scaffold presence, and git state
- `make localnet-bootstrap`: stage the pinned upstream CN Quickstart checkout and write `quickstart/.env.local` from the repo overlay
- `make localnet-smoke`: run upstream Docker preflight checks and validate the composed Quickstart LocalNet configuration
- `make validate-cpl`: validate `CPL v0.1` schema and the published example policies
- `make policy-eval`: validate a policy input, evaluate candidate inventory, and validate the generated `PolicyEvaluationReport`
- `make optimize`: validate a policy input, optimize against inventory plus obligation inputs, and validate the generated `OptimizationReport`
- `make test-policy-engine`: run deterministic policy-engine tests and regenerate the committed example report artifact
- `make test-optimizer`: run deterministic optimizer tests and regenerate the committed optimization report artifact
- `make daml-build`: compile the repository's Daml package into `.daml/dist/`
- `make daml-test`: run the Daml lifecycle scripts for margin call, posting, substitution, and return skeletons
- `make demo-run`: execute the aggregate `Bootstrap:workflowSmokeTest` Daml script
- `make demo-margin-call`: run the first positive and negative end-to-end margin-call scenarios and emit execution-report artifacts
- `make demo-return`: run the first positive and negative end-to-end return scenarios and emit return-report artifacts
- `make demo-substitution`: run the first positive and negative end-to-end substitution scenarios and emit substitution-report artifacts
- `make test-conformance`: run the aggregate conformance suite and emit explicit invariant pass/fail output across the three confidential workflow demos
- `make demo-all`: build the final demo pack from the aggregate conformance output
- `make verify-portable`: run the full verification loop across docs, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml tests, aggregate conformance, and final demo packaging without requiring Docker
- `make verify`: run the full verification loop and then add the Quickstart LocalNet smoke execution on top of `make verify-portable`

## Runtime Layout

- `.runtime/bin/`: repo-local `daml`, `daml-helper`, `java`, and `javac` entry points
- `.runtime/tools/`: extracted pinned SDK and JDK archives
- `.runtime/downloads/`: cached upstream tarballs
- `.runtime/localnet/`: pinned upstream CN Quickstart checkout plus generated `.env.local`
- `.venv/`: pinned schema-validation tooling
- `.daml/dist/`: generated DAR artifacts from `make daml-build`

## Notes

- The current repository now includes an initial deterministic policy engine, an initial deterministic optimizer, initial Daml workflow skeletons, end-to-end margin-call, return, and substitution demos, an aggregate conformance suite, and a final demo pack, but it still does not implement live asset adapters, settlement-window enforcement, or workflow-coupled optimization reservation.
- The Quickstart LocalNet foundation now stages a real upstream checkout and validates its compose topology, but it does not yet build the upstream stack automatically or deploy the repository's DAR into it.
- Future Quickstart or Canton overlay assets should land under `infra/`, not inside the Daml or app package trees.
- If the toolchain needs to be rebuilt from scratch, run `make clean-runtime` and then `make bootstrap`.
