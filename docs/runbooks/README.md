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

Collateral workflow runbooks do not exist yet because business logic is intentionally absent. The repository now includes:

- [docs/setup/LOCAL_DEV_SETUP.md](../setup/LOCAL_DEV_SETUP.md) for pinned local bootstrap and verification
- `make validate-cpl` for schema-validating published policy artifacts
- `make demo-run` for a Daml runtime-foundation smoke scenario

When workflow implementation begins, each major workflow should add or update at least one runbook and one reproducible command.
