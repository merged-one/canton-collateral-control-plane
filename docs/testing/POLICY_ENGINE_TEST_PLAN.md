# Policy Engine Test Plan

## Purpose

This plan defines the first executable verification surface for the `CPL v0.1` policy engine and its `PolicyEvaluationReport` contract.

## Toolchain

- runtime: repo-local Python `3.14.3` recommendation from [docs/setup/DEPENDENCY_POLICY.md](../setup/DEPENDENCY_POLICY.md)
- test runner: Python standard-library `unittest`
- report validation tool: `check-jsonschema==0.37.1`
- commands:
  - `make policy-eval POLICY=... INVENTORY=...`
  - `make test-policy-engine`

## Test Scope

| Test ID | Scenario | Expected Result |
| --- | --- | --- |
| `PE-001` | Eligible asset under a real `CPL v0.1` policy. | Asset is `ELIGIBLE`; report `overallDecision` is `ACCEPT`. |
| `PE-002` | Ineligible issuer under issuer allow-list controls. | Asset is `INELIGIBLE` with explicit issuer failure attribution. |
| `PE-003` | Haircut application under residual-maturity selectors and valuation-basis logic. | Base haircut and lendable value match the policy schedule deterministically. |
| `PE-004` | Currency mismatch haircut with pair override. | Base haircut plus mismatch haircut are additive and explicit in the report. |
| `PE-005` | Concentration limit breach. | Report includes per-bucket concentration evidence and the breached lots get machine-readable reasons. |
| `PE-006` | Wrong-way-risk exclusion. | Asset is rejected or escalated according to the named exclusion rule. |
| `PE-007` | Encumbrance restriction failure. | Asset is `INELIGIBLE` with explicit control-failure attribution. |
| `PE-008` | Deterministic rerun of the same policy and inventory input. | Entire report is byte-stable in structure and values, including `evaluationId`. |
| `PE-009` | Generated report artifact validation against the canonical report schema. | Pass |

## Reproducible Commands

Primary commands:

```sh
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
```

Repository verification loop:

```sh
make docs-lint
make validate-cpl
make test-policy-engine
make verify
```

## Invariant Coverage

The policy-engine test surface directly supports:

- `ELIG-001` eligibility determinism
- `HAIR-001` haircut and lendable-value correctness
- `CONC-001` concentration-limit enforcement
- `WWR-001` wrong-way-risk explicitness
- `EXCP-001` exception-path determinism
- `PDR-001` policy decision report fidelity

## Current Gaps

This plan does not yet prove:

- settlement-window or expiry behavior
- substitution or return-path evaluation
- external FX conversion or valuation-reference lineage beyond normalized input
- role-scoped execution-report disclosure profiles
- asset-adapter integration against a live Canton environment

Those remain later milestone surfaces and should be added through conformance and workflow plans rather than folded implicitly into the current engine tests.
