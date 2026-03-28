# Optimizer Test Plan

## Purpose

This plan records the deterministic test coverage required for the first optimizer implementation under `app/optimizer/`.

## Scope

The first optimizer test suite must prove:

- best-to-post selection under a published policy and obligation amount
- concentration-aware portfolio selection
- substitution recommendation against an existing posted set
- forced replacement of declared encumbered lots when a substitution request scopes the release set
- clean no-solution handling
- deterministic repeatability for identical inputs

## Commands

```sh
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-optimizer
```

## Scenario Coverage

1. Cheapest eligible asset wins when unconstrained.
   Use a relaxed concentration configuration and show the optimizer prefers the lower-cost compliant asset.
2. Concentration rule changes the allocation.
   Use a portfolio where the lowest-cost same-issuer solution is blocked and a diversified set becomes optimal.
3. Substitution improves the objective while preserving compliance.
   Start from a feasible current posted set and show the optimizer recommends a lower-cost replacement.
4. Request-scoped substitution can force release of incumbent lots.
   Start from a current posted set that remains feasible, declare `mustReplaceLotIds`, and show the optimizer recommends a valid replacement set instead of keeping the incumbent set.
5. No solution case is handled cleanly.
   Show the optimizer emits `NO_SOLUTION` with explicit blocking reason codes instead of raising an unstructured error.
6. Determinism.
   Run the same optimization twice and require byte-equivalent report objects before serialization.

## Validation Expectations

- `make test-optimizer` must run the Python unit suite under `test/optimizer/`
- the target must regenerate at least one committed optimization report artifact through the real CLI path
- the generated report must validate against [reports/schemas/optimization-report.schema.json](../../reports/schemas/optimization-report.schema.json)
- substitution-request fields such as `mustReplaceLotIds` and `atomicityRequired` must appear in the machine-readable report when present on the obligation input
- policy-engine tests remain in place because optimizer correctness depends on stable policy semantics

## Deferred Coverage

The following remain future work:

- larger search-space and performance characterization
- workflow-coupled substitution consent and settlement windows
- replay and concurrency behavior once optimization proposals are bound to Canton workflow state
- reference-data driven objective terms such as funding spread, repo specialness, or custody cost
