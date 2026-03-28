# ADR 0012: Enforce Atomic Substitution Scope And Control Checks

- Status: Accepted
- Date: 2026-03-28

## Context

The repository now has a deterministic optimizer, initial substitution templates on the Daml boundary, and one end-to-end margin-call demo. It still lacks a real substitution prototype that proves the following together:

- the starting collateral set is already encumbered
- a substitution request can require release of specific pledged lots
- the optimizer can recommend a valid replacement set under the declared policy
- secured-party and custodian approvals remain explicit control gates
- the replacement either commits as one full scope change or does not release the incumbent encumbrances at all
- operator evidence ties policy, optimization, workflow, and failure reasons into one machine-readable artifact

Without an explicit decision here, the prototype would be vulnerable to three failure modes:

- an optimizer recommendation could keep one of the lots that the request required to be replaced
- workflow execution could accept a partial replacement set after approval even when policy and request semantics require all-or-nothing substitution
- reporting could flatten policy, control, and workflow evidence into one opaque success or failure summary

## Decision

The repository will implement the first substitution prototype as a scope-bound, approval-gated, atomic replacement flow with a separate substitution-report contract.

Specific decisions:

1. Substitution obligations may include a `substitutionRequest` block that declares `requestId`, `mustReplaceLotIds`, and `atomicityRequired`.
2. The optimizer must treat `mustReplaceLotIds` as a hard constraint and reject any candidate portfolio that retains one of those lots.
3. If a valid replacement set exists, the optimizer may still recommend `SUBSTITUTE` even when the current posted set is economically better, because the request scope requires release of declared encumbrances rather than a pure economic rebalance.
4. Workflow execution must keep secured-party and custodian approvals explicit and attributable before settlement intent can be created or confirmed.
5. When `atomicityRequired = true`, the Daml substitution workflow must reject settlement scope drift, including partial replacement attempts that omit approved replacement lots.
6. Unauthorized release or settlement confirmation attempts must fail closed and preserve the incumbent encumbered lot set.
7. Operator-facing substitution evidence will be published as a separate machine-readable `SubstitutionReport` contract rather than overloading the margin-call `ExecutionReport`.
8. The first operator command for this path is `make demo-substitution`, backed by real policy, optimization, Daml workflow, and Markdown summary artifacts.

## Consequences

Positive:

- the prototype now proves substitution-specific control semantics rather than implying them from the margin-call path
- optimizer, workflow, and report contracts share one explicit replacement scope
- negative-path evidence becomes deterministic for ineligibility, concentration breach, unauthorized release, and partial-settlement atomicity violations
- the repository gains a real substitution demo without pretending Quickstart-backed deployment is complete

Tradeoffs:

- the first substitution workflow still runs on the Daml IDE ledger rather than the pinned Quickstart LocalNet
- the substitution report is an operator-facing aggregate contract, not yet a role-scoped disclosure profile
- the optimizer remains advisory and off-ledger, so workflow authority still depends on the Daml boundary to enforce approvals and settlement scope

These tradeoffs are accepted because the repository needs a real substitution prototype now, but it must not hide the split between advisory optimization, authoritative workflow execution, and operator-facing evidence.
