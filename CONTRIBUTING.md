# Contributing

## Workflow

This repository is documentation-first. Contributors should build or change the control spine before they add implementation details.

Start every task with:

```sh
make status
```

After a fresh clone or when the local toolchain is missing, run:

```sh
make bootstrap
```

Then follow this sequence:

1. Read [AGENTS.md](./AGENTS.md) and [docs/mission-control/MASTER_TRACKER.md](./docs/mission-control/MASTER_TRACKER.md).
2. Add a pre-change entry to [docs/mission-control/WORKLOG.md](./docs/mission-control/WORKLOG.md).
3. Make the smallest coherent change that advances the current phase.
4. Update ADRs, invariants, evidence, risks, and runbooks as required by the change.
5. Run verification commands.
6. Add a post-change worklog entry with outcomes, commands, and next steps.

## Required Artifacts

When relevant, each contribution must leave behind:

- a reproducible command
- links to updated invariants and evidence
- an ADR for significant design changes
- security, risk, or operational notes when the change touches those concerns

## Guardrails

- Do not add fake demo outputs or placeholder success artifacts.
- Do not merge unpinned or non-reproducible tool choices without documenting the rationale.
- Do not couple policy logic, optimization, workflow orchestration, and reporting into one opaque module.
- Treat confidentiality, control, atomicity, and auditability as first-order requirements.

## Verification

Current baseline verification:

```sh
make bootstrap
make localnet-bootstrap
make localnet-smoke
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
make demo-return-quickstart
make demo-substitution
make demo-substitution-quickstart
make test-conformance
make demo-all
make proposal-package
make docs-lint
make verify-portable
make verify
```

The bootstrap installs the pinned repo-local Daml and Java toolchain under `.runtime/` and keeps CPL validation isolated in `.venv/`. `make localnet-bootstrap` stages the pinned upstream CN Quickstart checkout under `.runtime/localnet/`, `make localnet-smoke` validates the upstream compose topology, `make localnet-build-dar` builds the Control Plane DAR against the pinned Quickstart runtime line through the documented containerized bridge, and `make localnet-deploy-dar` installs that DAR into a running pinned Quickstart stack. `make localnet-start-control-plane` brings up the repo-owned isolated Quickstart overlay and writes a deployment receipt. `make localnet-seed-demo` seeds the default confidential collateral scenario and writes ledger-returned contract identifiers. `make localnet-status-control-plane` captures the provider-visible Quickstart status surface. `make localnet-run-token-adapter` executes the first reference token adapter path and writes adapter execution evidence. `make localnet-adapter-status` refreshes the provider-visible adapter status surface. `make demo-margin-call` remains the IDE-ledger end-to-end operator demo for margin-call posting. `make demo-margin-call-quickstart` now runs the Quickstart-backed margin-call chain end to end across policy evaluation, optimization, workflow preparation, adapter execution, and final execution reporting. `make demo-return` proves retained-set-driven collateral return, approval enforcement, replay blocking, and release-state integrity. `make demo-return-quickstart` now proves the Quickstart-backed return chain across retained-set selection, workflow execution, adapter-driven release, provider-visible status refresh, approval-gated release, and replay-safe duplicate-request blocking. `make demo-substitution` proves encumbered-collateral replacement, approval enforcement, and atomic substitution failure handling. `make demo-substitution-quickstart` now proves the Quickstart-backed substitution chain across policy evaluation, optimization, workflow execution, adapter-driven incumbent release plus replacement movement, and final substitution reporting. `make test-conformance` now refreshes Quickstart deployment evidence, validates one concrete reference token adapter proof path, and validates the three Quickstart-backed confidential workflow demo artifact chains before emitting aggregate invariant output. `make demo-all` now packages those runtime-backed artifacts into the final reviewer-facing demo bundle with explicit real-versus-staged readiness notes. `make proposal-package` now wraps that bundle with a proposal-submission manifest, reviewer memo, and walkthrough materials pinned to the generated evidence. `make verify-portable` is the baseline verification loop through the proposal package, while `make verify` adds the Quickstart smoke gate. The policy engine and optimizer stay stdlib-only and validate their generated report artifacts against the committed report schemas.
