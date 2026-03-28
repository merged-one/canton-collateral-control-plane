# Runbooks

Runbooks turn design intent into operator steps. They should contain real commands, expected outputs, and failure handling. Placeholder success narratives are not acceptable.

## Planned Runbooks

- LocalNet bootstrap
- policy load and validation
- margin call scenario execution
- collateral substitution scenario
- collateral return scenario
- release verification and evidence collection

## Current State

The repository now includes:

- [docs/setup/LOCAL_DEV_SETUP.md](../setup/LOCAL_DEV_SETUP.md) for pinned local bootstrap and verification
- [infra/quickstart/README.md](../../infra/quickstart/README.md) for the pinned Quickstart LocalNet bootstrap and smoke layer
- [docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md](./MARGIN_CALL_DEMO_RUNBOOK.md) for the first end-to-end margin-call demo
- [docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md](./SUBSTITUTION_DEMO_RUNBOOK.md) for the first end-to-end substitution demo
- `make localnet-bootstrap` for staging the pinned upstream CN Quickstart checkout and overlay
- `make localnet-smoke` for Docker preflight plus compose-config validation of the pinned Quickstart stack
- `make validate-cpl` for schema-validating published policy artifacts
- `make policy-eval` for generating a real `PolicyEvaluationReport`
- `make optimize` for generating a real `OptimizationReport`
- `make demo-run` for a Daml runtime-foundation smoke scenario
- `make demo-margin-call` for the first end-to-end margin-call operator demo
- `make demo-substitution` for the first end-to-end substitution operator demo

Future workflow additions should continue to add or update at least one runbook and one reproducible command.
