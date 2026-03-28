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

At this phase, the repository only supports lightweight documentation checks:

```sh
make docs-lint
make verify
```

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
- negative paths for ineligible assets, expired calls, insufficient lendable value, concentration breaches, unauthorized release, and replayed instructions

## Traceability Expectations

- every new feature updates the invariant registry
- every invariant gains at least one planned or implemented verification hook
- every demo artifact must point back to the code path and command that generated it
- milestone planning should distinguish between specification-only evidence and executed conformance evidence
