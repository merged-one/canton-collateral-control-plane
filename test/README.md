# Test Surface

This directory contains deterministic policy-engine, optimizer, and conformance tests. Shared Python fixture builders that keep the unit suites aligned live under `testsupport/`.

Current contents:

- `test/conformance/` for the aggregate conformance suite, including both generated-report assertions and isolated helper-check unit tests
- `test/policy-engine/` for the `CPL v0.1` policy engine scenario suite
- `test/optimizer/` for deterministic best-to-post, substitution, concentration, and no-solution scenarios
- `testsupport/` for shared deterministic Python fixture builders used across the policy-engine and optimizer suites
- `make demo-margin-call` as the current executable conformance path for end-to-end positive and negative margin-call scenarios
- `make demo-substitution` as the executable conformance path for end-to-end positive and negative substitution scenarios
- `make test-conformance` as the aggregate invariant-verification path across margin call, substitution, and return

Expected future contents:

- Daml package tests
- policy-engine determinism tests
- optimizer determinism tests
- report-contract validation tests
- conformance scenarios against LocalNet or an equivalent pinned runtime
