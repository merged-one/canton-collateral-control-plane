# CPL Validation Test Plan

## Purpose

This plan defines the first executable validation surface for `CPL v0.1`. The goal is to prove that the published schema is real, strict, and usable by later policy-engine work.

## Toolchain

- validator package: `check-jsonschema==0.37.1`
- pin file: [requirements-cpl-validation.txt](../../requirements-cpl-validation.txt)
- runtime location: repo-local `.venv/`
- operator command: `make validate-cpl`

The Make target bootstraps the validator into `.venv/` when missing, validates the schema itself, validates the published example policies, and runs negative checks.

## Test Scope

| Test ID | Scope | Expected Result |
| --- | --- | --- |
| `CPL-VAL-001` | Validate `schema/cpl.schema.json` against the JSON Schema metaschema. | Pass |
| `CPL-VAL-002` | Validate [examples/policies/central-bank-style-policy.json](../../examples/policies/central-bank-style-policy.json). | Pass |
| `CPL-VAL-003` | Validate [examples/policies/tri-party-style-policy.json](../../examples/policies/tri-party-style-policy.json). | Pass |
| `CPL-VAL-004` | Validate [examples/policies/ccp-style-policy.json](../../examples/policies/ccp-style-policy.json). | Pass |
| `CPL-VAL-005` | Validate [examples/policies/bilateral-csa-style-policy.json](../../examples/policies/bilateral-csa-style-policy.json). | Pass |
| `CPL-VAL-006` | Validate a generated negative case missing `policyId`. | Fail validation |
| `CPL-VAL-007` | Validate a generated negative case with an unknown top-level property. | Fail validation |

## Reproducible Commands

Primary command:

```sh
make validate-cpl
```

Full repository control loop:

```sh
make docs-lint
make status
make verify
```

## Invariant Coverage

The initial validation plan supports these invariants directly:

- schema-valid policy packages declare explicit policy identity, versioning, and timing fields
- eligibility controls are machine-readable rather than hidden prose
- concentration limits and wrong-way-risk exclusions are explicit fields rather than implied side rules
- settlement windows, expiry, and substitution controls are encoded in the same authoritative package

## Known Gaps

The schema validator is structural, not economic. `CPL v0.1` validation does not yet prove:

- rating ordering beyond enumerated labels
- cross-file uniqueness for policy identifiers
- temporal ordering such as `effectiveUntil > effectiveFrom`
- concentration behavior against live inventory
- substitution behavior against actual workflow state

Those checks belong in later policy-engine, conformance-suite, and workflow tests. For `v0.1`, the objective is to lock a strict package shape and validate example artifacts reproducibly.
