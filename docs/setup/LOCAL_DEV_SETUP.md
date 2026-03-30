# Local Development Setup

## Purpose

Bootstrap a pinned local toolchain that can compile the repository's Daml package, validate `CPL v0.1`, evaluate the first policy-engine path, optimize the first collateral-allocation path, execute the initial Daml workflow smoke scenario, run the first end-to-end margin-call, Quickstart-backed margin-call, return, and substitution demos from a clean checkout, stage the pinned Quickstart-based LocalNet foundation, and start, deploy, seed, inspect, or execute a Quickstart-compatible Control Plane scenario.

## Supported Bootstrap Platforms

- macOS on Apple Silicon (`Darwin-arm64`)
- Linux on `x86_64`

The bootstrap is intentionally repo-local. It installs the Daml SDK and JDK under `.runtime/` and keeps Python validation tooling in `.venv/`.

The Quickstart bridge is intentionally split from that host-native toolchain. The repo keeps Daml SDK `2.10.4` plus JDK `17` for the existing IDE-ledger workflow surface, while Quickstart-compatible DAR builds run in Docker on Daml SDK `3.4.10` plus Java `21`.

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
make localnet-build-dar
make localnet-deploy-dar
make localnet-start-control-plane
make localnet-seed-demo
make localnet-status-control-plane
make localnet-run-token-adapter
make localnet-adapter-status
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-policy-engine
make test-optimizer
make daml-build
make daml-test
make demo-run
make demo-margin-call
make demo-margin-call-quickstart
make demo-return
make demo-substitution
make demo-substitution-quickstart
make test-conformance
make demo-all
make verify-portable
make verify
```

What each command does:

- `make status`: show pinned versus installed tool versions, scaffold presence, and git state
- `make localnet-bootstrap`: stage the pinned upstream CN Quickstart checkout and write `quickstart/.env.local` from the repo overlay
- `make localnet-smoke`: run upstream Docker preflight checks and validate the composed Quickstart LocalNet configuration
- `make localnet-build-dar`: build the Control Plane DAR against the pinned Quickstart runtime line through the containerized Daml `3.4.10` plus Java `21` bridge and write package metadata under `.daml/dist-quickstart/`
- `make localnet-deploy-dar`: rebuild the Quickstart-compatible DAR and upload it into a running pinned Quickstart LocalNet through the upstream onboarding container and participant package APIs
- `make localnet-start-control-plane`: start the isolated repo-owned Quickstart overlay, deploy the Control Plane DAR, and write deployment evidence under `reports/generated/`
- `make localnet-seed-demo`: allocate or reuse the scenario parties and users, seed the default confidential margin-style scenario on Quickstart, and write the seed receipt plus status snapshots under `reports/generated/`
- `make localnet-status-control-plane`: query the seeded scenario from the provider-visible Quickstart view and rewrite the machine-readable plus Markdown status artifacts under `reports/generated/`
- `make localnet-run-token-adapter`: consume the seeded settlement instruction, execute the reference token adapter path on Quickstart, validate the generated adapter execution report, and refresh adapter status artifacts under `reports/generated/`
- `make localnet-adapter-status`: query the provider-visible adapter receipt and reference-token-holding surface and rewrite the machine-readable plus Markdown adapter status artifacts under `reports/generated/`
- `make validate-cpl`: validate `CPL v0.1` schema and the published example policies
- `make policy-eval`: validate a policy input, evaluate candidate inventory, and validate the generated `PolicyEvaluationReport`
- `make optimize`: validate a policy input, optimize against inventory plus obligation inputs, and validate the generated `OptimizationReport`
- `make test-policy-engine`: run deterministic policy-engine tests and regenerate the committed example report artifact
- `make test-optimizer`: run deterministic optimizer tests and regenerate the committed optimization report artifact
- `make daml-build`: compile the repository's Daml package into `.daml/dist/`
- `make daml-test`: run the Daml lifecycle scripts for margin call, posting, substitution, and return skeletons
- `make demo-run`: execute the aggregate `Bootstrap:workflowSmokeTest` Daml script
- `make demo-margin-call`: run the IDE-ledger positive and negative end-to-end margin-call scenarios and emit execution-report artifacts
- `make demo-margin-call-quickstart`: start or reuse the Quickstart overlay, evaluate the Quickstart-backed positive and negative margin-call scenarios, hand the positive workflow result to the reference token adapter, and emit chained execution-report artifacts
- `make demo-return`: run the first positive and negative end-to-end return scenarios and emit return-report artifacts
- `make demo-substitution`: run the first positive and negative end-to-end substitution scenarios and emit substitution-report artifacts
- `make demo-substitution-quickstart`: start or reuse the Quickstart overlay, evaluate the Quickstart-backed positive and negative substitution scenarios, hand the positive workflow result to the substitution adapter path, and emit chained substitution-report artifacts
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
- `.daml/dist-quickstart/`: generated Quickstart-compatible DAR artifact plus package metadata from `make localnet-build-dar`

## Notes

- The current repository now includes an initial deterministic policy engine, an initial deterministic optimizer, initial Daml workflow skeletons, end-to-end margin-call, return, and substitution demos, an aggregate conformance suite, and a final demo pack, but it still does not implement live asset adapters, settlement-window enforcement, or workflow-coupled optimization reservation.
- The Quickstart LocalNet foundation now stages a real upstream checkout, validates its compose topology, starts an isolated repo-owned Quickstart overlay, deploys the Control Plane DAR, seeds one confidential collateral scenario with ledger-returned contract identifiers, executes Quickstart-backed margin-call and substitution workflow-preparation paths, and executes reference token adapter posting plus substitution paths, but it still does not provide return-adapter coverage, production-grade asset adapters, settlement-window enforcement, or workflow-coupled optimizer reservation.
- `make localnet-build-dar` and `make localnet-deploy-dar` require Docker because the Quickstart-compatible DAR is built inside a Linux container even on Apple Silicon hosts.
- Future Quickstart or Canton overlay assets should land under `infra/`, not inside the Daml or app package trees.
- If the toolchain needs to be rebuilt from scratch, run `make clean-runtime` and then `make bootstrap`.
