# Dependency Policy

## Goal

Keep the prototype's runtime and verification surface reproducible, easy to audit, and conservative enough for later Canton adoption work.

## Pinned Dependencies

| Dependency | Pinned Version | Source Of Truth | Why It Is Pinned |
| --- | --- | --- | --- |
| Daml SDK 2.10.4 | `2.10.4` | [daml.yaml](../../daml.yaml), [scripts/toolchain.env](../../scripts/toolchain.env) | canonical workflow-modeling toolchain for the repository's Daml package |
| Canton open-source 2.10.4 | `2.10.4` | [scripts/toolchain.env](../../scripts/toolchain.env) | runtime compatibility baseline aligned with the Daml SDK release |
| Temurin JDK 17.0.18+8 | `17.0.18+8` | [scripts/toolchain.env](../../scripts/toolchain.env), [`.tool-versions`](../../.tool-versions) | stable LTS Java baseline for Daml and Canton tooling |
| Python | `3.14.3` | [`.tool-versions`](../../.tool-versions) | recommended local version for repeatable bootstrap and schema validation |
| `check-jsonschema` | `0.37.1` | [requirements-cpl-validation.txt](../../requirements-cpl-validation.txt) | strict pinned validator for `CPL v0.1` inputs and `PolicyEvaluationReport` schema checks |

## Installation Policy

- bootstrap from official upstream release archives, not ad hoc mirrors
- verify all downloaded archives with pinned SHA-256 checksums
- install runtime tools under repo-local `.runtime/` rather than relying on mutable global installations
- keep Python validation tooling in repo-local `.venv/`
- avoid adding service runtimes or package managers until a concrete repository need exists

## Service-Layer Policy

The repository may add off-ledger services only for:

- policy evaluation
- optimization orchestration
- report generation
- integration helpers

Those services must remain small and non-authoritative. Daml remains the intended authority for workflow state and transitions.

## Update Rules

1. Change pins through an ADR or an ADR-backed tracker update.
2. Update `daml.yaml`, `scripts/toolchain.env`, `.tool-versions`, and setup docs together when a pinned tool changes.
3. Keep the Makefile command surface stable unless there is a concrete need to change it.
4. Re-run `make bootstrap`, `make daml-build`, `make demo-run`, and `make verify` after any dependency change.

## Deferred Dependencies

These remain intentionally deferred until later phases:

- Quickstart overlay selection and packaging details
- additional report-schema validation tooling beyond `check-jsonschema`
- integration-service frameworks
- any optimizer-specific solver libraries
