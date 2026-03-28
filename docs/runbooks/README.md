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

No executable workflow runbooks exist yet because business logic is intentionally absent. The repository now includes one operator-facing control command, `make validate-cpl`, for schema-validating published policy artifacts. When implementation begins, each major workflow should add or update at least one runbook and one reproducible command.
