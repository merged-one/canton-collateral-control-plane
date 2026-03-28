# ADR 0008: Implement A Deterministic CPL v0.1 Policy Evaluation Engine

- Status: Accepted
- Date: 2026-03-28

## Context

The repository already has a strict `CPL v0.1` schema, market-practice example policies, and Daml workflow skeletons, but it still lacks an executable policy engine. Without one, policy semantics stop at documentation and schema validation, which is insufficient for the milestone's determinism, explainability, and conformance goals.

The first engine needs to:

- load a real `CPL v0.1` policy file without hidden field conventions
- load a candidate collateral inventory set
- evaluate eligibility, haircut, lendable value, concentration, control, and wrong-way-risk behavior deterministically
- emit a machine-readable report contract suitable for future workflow and optimization consumers
- make negative paths explicit rather than implicit

## Decision

The repository will implement the first off-ledger policy engine as a small Python standard-library service under `app/policy-engine/`, with a report contract under `reports/schemas/`.

Specific decisions:

1. The engine consumes the published `CPL v0.1` JSON policy shape directly and uses the repo's existing schema-validation command before evaluation.
2. Candidate inventory input is a normalized JSON document with explicit exposure-counterparty context and monetary values already expressed in one `valuationCurrency`.
3. The engine remains side-effect free: policy plus inventory produces a deterministic `PolicyEvaluationReport`, with no workflow mutation and no hidden external calls.
4. Haircut semantics follow the `CPL v0.1` spec exactly: highest matching base haircut wins, and currency mismatch adds the matching pair override or default mismatch haircut.
5. Lendable value is rounded to cents with the policy's configured rounding mode.
6. Concentration limits are evaluated after non-concentration `REJECT` reasons are applied, so bucket math reflects the surviving candidate set rather than obviously ineligible lots.
7. `JURISDICTION` concentration bucketing uses `issuanceJurisdiction` in `v0.1`.
8. The report identifier is derived from a stable hash of canonicalized inputs rather than a runtime timestamp.
9. Settlement windows, expiry timers, substitution-right evaluation, and release-path logic remain outside this first engine boundary.

## Consequences

Positive:

- the repository now has a real executable path from policy package to deterministic decision report
- failure attribution is machine-readable at both lot and portfolio levels
- report generation stays separate from workflow state mutation, preserving the architecture boundary
- later optimizers and workflow orchestrators can consume a stable report contract rather than re-implementing policy rules

Tradeoffs:

- the first inventory input contract is intentionally normalized and does not yet include an external FX adapter or reference-data schema
- temporal settlement-window checks are deferred even though the policy schema already carries those fields
- the first engine is deterministic and conservative, but not yet calibrated for performance or live integration

These tradeoffs are accepted because the repository needs a strict, reproducible decision path before it adds asset adapters, reference-data contracts, or workflow-coupled evaluation behavior.
