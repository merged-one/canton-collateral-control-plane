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
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-policy-engine
make test-optimizer
make daml-build
make daml-test
make demo-run
make demo-margin-call
make docs-lint
make verify
```

The bootstrap installs the pinned repo-local Daml and Java toolchain under `.runtime/` and keeps CPL validation isolated in `.venv/`. `make localnet-bootstrap` stages the pinned upstream CN Quickstart checkout under `.runtime/localnet/`, and `make localnet-smoke` validates the upstream compose topology without pretending the Control Plane DAR is already deployed. `make demo-margin-call` now provides the first end-to-end operator demo and validates its generated execution report against the committed schema. The policy engine and optimizer stay stdlib-only and validate their generated report artifacts against the committed report schemas.
