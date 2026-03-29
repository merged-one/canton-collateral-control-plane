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
make demo-substitution
make test-conformance
make demo-all
make docs-lint
make verify-portable
make verify
```

`CPL v0.1` schema coverage and the initial negative cases are documented in [CPL_VALIDATION_TEST_PLAN.md](./CPL_VALIDATION_TEST_PLAN.md). The policy-engine scenario coverage is documented in [POLICY_ENGINE_TEST_PLAN.md](./POLICY_ENGINE_TEST_PLAN.md). The optimizer scenario coverage is documented in [OPTIMIZER_TEST_PLAN.md](./OPTIMIZER_TEST_PLAN.md). The Daml workflow skeleton coverage is documented in [DAML_TEST_PLAN.md](./DAML_TEST_PLAN.md). The aggregate conformance suite is documented in [CONFORMANCE_SUITE.md](./CONFORMANCE_SUITE.md). The Quickstart LocalNet foundation now adds a pinned upstream checkout, compose-preflight smoke, isolated overlay start, seeded-scenario command surface, provider-visible Quickstart status evidence, a Quickstart-backed margin-call workflow handoff surface, and the first Quickstart-backed reference token adapter execution artifact. The Python unit suites now share deterministic fixture builders, and the conformance layer now includes isolated helper tests in addition to the generated-suite assertions. The current repository now proves deterministic policy evaluation, deterministic collateral optimization, basic workflow lifecycle execution, end-to-end margin-call, return, and substitution demos with explicit negative paths, aggregate invariant pass/fail output, the first real Quickstart-seeded collateral scenario, one real Quickstart-backed end-to-end margin-call chain, and one real Quickstart-backed adapter path.

## Verification Tiers

- `make verify-portable` is the baseline repository gate for environments that can run the pinned Python and Daml toolchain but do not have Docker available.
- `make verify` is the full superset and adds `make localnet-smoke` so the pinned Quickstart compose surface remains an explicit environment-dependent gate.
- `make localnet-start-control-plane`, `make localnet-seed-demo`, `make localnet-status-control-plane`, `make localnet-run-token-adapter`, `make localnet-adapter-status`, and `make demo-margin-call-quickstart` are operator-facing Quickstart checks that currently sit outside the default verify targets because they require a running Docker stack, Quickstart auth wiring, and a seeded or reseeded LocalNet.

## Current Conformance Scope

The current conformance suite now covers:

- authorization and role control
- eligibility determinism
- haircut conservation and lendable-value correctness
- concentration-limit enforcement
- no double encumbrance
- atomic substitution and atomic settlement across legs
- return release-condition validation and retained-coverage safety
- replay safety
- report fidelity
- audit trail completeness
- negative paths for ineligible assets, expired calls, insufficient lendable value, concentration breaches, Quickstart workflow rejection without adapter movement, unauthorized release, replayed return instructions, stale obligation-state mismatches, attempted partial substitution under atomicity, and replayed instructions

## Traceability Expectations

- every new feature updates the invariant registry
- every invariant gains at least one planned or implemented verification hook
- every demo artifact must point back to the code path and command that generated it
- milestone planning should distinguish between specification-only evidence and executed conformance evidence
