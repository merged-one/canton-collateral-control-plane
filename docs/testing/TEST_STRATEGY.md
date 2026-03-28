# Test Strategy

## Purpose

Testing in this repository exists to prove invariants, not just to increase coverage numbers. Each meaningful feature should map to explicit invariants and reproducible checks.

## Test Layers

1. Document checks
   Verify required control documents, sections, and cross-links exist.
2. Schema and contract tests
   Validate CPL, asset-adapter, and report structures once they exist.
3. Determinism tests
   Check policy evaluation, haircuting, concentration, and optimization reproducibility.
4. Workflow tests
   Check atomicity, authorization, substitution, return, close-out, and replay behavior.
5. Security tests
   Check access control, confidentiality boundaries, and integrity assumptions.
6. Conformance-suite scenarios
   Check negative paths, invariant reports, and scenario-runner outputs against documented expectations.
7. Demo verification
   Check that operator-facing demo flows are backed by real commands and generated artifacts.

## Current Baseline

At this phase, the repository supports documentation checks, schema validation, deterministic policy-engine tests, and executable Daml workflow checks:

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
make demo-substitution
make docs-lint
make verify
```

`CPL v0.1` schema coverage and the initial negative cases are documented in [CPL_VALIDATION_TEST_PLAN.md](./CPL_VALIDATION_TEST_PLAN.md). The policy-engine scenario coverage is documented in [POLICY_ENGINE_TEST_PLAN.md](./POLICY_ENGINE_TEST_PLAN.md). The optimizer scenario coverage is documented in [OPTIMIZER_TEST_PLAN.md](./OPTIMIZER_TEST_PLAN.md). The Daml workflow skeleton coverage is documented in [DAML_TEST_PLAN.md](./DAML_TEST_PLAN.md). The Quickstart LocalNet foundation now adds a pinned upstream checkout plus a compose-preflight smoke check. The current repository now proves deterministic policy evaluation, deterministic collateral optimization, basic workflow lifecycle execution, the first end-to-end margin-call and substitution demos with explicit negative paths, and the earliest real LocalNet bootstrap layer.

## Proposal-Aligned Conformance Direction

The proposal implies a conformance suite that should eventually cover at least:

- eligibility determinism
- haircut conservation and lendable-value correctness
- concentration-limit enforcement
- no double encumbrance
- authorization and secured-party control
- atomic substitution and atomic settlement across legs
- replay safety
- report fidelity
- negative paths for ineligible assets, expired calls, insufficient lendable value, concentration breaches, unauthorized release, attempted partial substitution under atomicity, and replayed instructions

## Traceability Expectations

- every new feature updates the invariant registry
- every invariant gains at least one planned or implemented verification hook
- every demo artifact must point back to the code path and command that generated it
- milestone planning should distinguish between specification-only evidence and executed conformance evidence
