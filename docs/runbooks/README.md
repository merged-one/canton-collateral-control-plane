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
- [infra/quickstart/README.md](../../infra/quickstart/README.md) for the pinned Quickstart LocalNet bootstrap, isolated overlay, DAR-build, deployment, and seeded-scenario layer
- [docs/runbooks/LOCALNET_CONTROL_PLANE_RUNBOOK.md](./LOCALNET_CONTROL_PLANE_RUNBOOK.md) for bootstrap, start, deploy, seed, reference-token-adapter execution, inspect, and teardown of the Quickstart-backed Control Plane scenario
- [docs/runbooks/FINAL_DEMO_RUNBOOK.md](./FINAL_DEMO_RUNBOOK.md) for the final packaged confidential workflow demo
- [docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md](./MARGIN_CALL_DEMO_RUNBOOK.md) for the first end-to-end margin-call demo
- [docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md](./SUBSTITUTION_DEMO_RUNBOOK.md) for the first end-to-end substitution demo
- [docs/runbooks/RETURN_DEMO_RUNBOOK.md](./RETURN_DEMO_RUNBOOK.md) for the first end-to-end return demo
- `make localnet-bootstrap` for staging the pinned upstream CN Quickstart checkout and overlay
- `make localnet-smoke` for Docker preflight plus compose-config validation of the pinned Quickstart stack
- `make localnet-build-dar` for the Quickstart-compatible Control Plane DAR build
- `make localnet-deploy-dar` for package installation into a running pinned Quickstart LocalNet
- `make localnet-start-control-plane` for starting the isolated overlay runtime and deploying the Control Plane DAR
- `make localnet-seed-demo` for seeding the default confidential Quickstart scenario and writing contract receipts
- `make localnet-status-control-plane` for generating the provider-visible Quickstart status snapshot
- `make localnet-run-token-adapter` for executing the reference token adapter path and writing machine-readable adapter evidence
- `make localnet-adapter-status` for refreshing the provider-visible adapter status surface
- `make validate-cpl` for schema-validating published policy artifacts
- `make policy-eval` for generating a real `PolicyEvaluationReport`
- `make optimize` for generating a real `OptimizationReport`
- `make demo-run` for a Daml runtime-foundation smoke scenario
- `make demo-margin-call` for the first end-to-end margin-call operator demo
- `make demo-return` for the first end-to-end return operator demo
- `make demo-return-quickstart` for the Quickstart-backed end-to-end return operator demo
- `make demo-substitution` for the first end-to-end substitution operator demo
- `make test-conformance` for the aggregate invariant-verification package
- `make demo-all` for the final packaged prototype demonstration
- `make proposal-package` for the reviewer-facing proposal submission wrapper around the final demo pack

Future workflow additions should continue to add or update at least one runbook and one reproducible command.
