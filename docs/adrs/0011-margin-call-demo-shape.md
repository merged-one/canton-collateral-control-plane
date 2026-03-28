# ADR 0011: Establish The First End-To-End Margin Call Demo Shape

- Status: Accepted
- Date: 2026-03-28

## Context

The repository now has a deterministic policy engine, a deterministic optimizer, initial Daml workflow templates for obligation and posting flows, and a pinned Quickstart foundation. It still lacks one reproducible command that ties those layers into a single auditable margin-call outcome.

Without an explicit demo shape, the repository would remain vulnerable to two bad outcomes:

- a demo could stitch together policy, optimization, workflow, and reporting outputs informally and drift away from the real executable path
- an execution report could remain underdefined, forcing operators or reviewers to guess how policy artifacts, optimization artifacts, and Daml workflow evidence are linked

The first end-to-end prototype must therefore prove real technical progress without pretending the full Quickstart-backed confidential-collateral environment is already complete.

## Decision

The repository will implement the first end-to-end margin-call demo as an orchestration-layer scenario runner backed by real policy, optimization, and Daml execution artifacts.

Specific decisions:

1. The primary operator command is `make demo-margin-call`.
2. Demo inputs live under `examples/demo-scenarios/margin-call/` as a manifest plus scenario-specific policy, inventory, and obligation files.
3. The orchestration layer under `app/orchestration/` runs the policy engine first, then the optimizer, and only then invokes a parameterized Daml Script for the positive workflow path.
4. The Daml Script consumes the optimizer-selected lot set through JSON input and records the secured-party margin-call issuance plus the provider posting path on the Daml workflow boundary.
5. The operator-facing `ExecutionReport` is a separate machine-readable report contract under `reports/schemas/execution-report.schema.json`; it references the generated policy-evaluation, optimization, and workflow artifacts rather than replacing them.
6. The first demo publishes one positive margin-call path plus negative-path coverage for ineligible collateral, insufficient lendable value, and an expired policy window.
7. Negative scenarios stop before Daml workflow execution when policy or optimization outcomes make a posting path invalid; the demo must not fabricate a workflow success artifact for blocked cases.
8. The first execution report is an operator-facing aggregate artifact, not yet a role-scoped disclosure profile; narrower report views remain future work.

## Consequences

Positive:

- the repository now has a real end-to-end margin-call command rather than adjacent building blocks only
- execution reporting gains a concrete schema, spec, and runbook
- the positive flow proves that optimizer-selected inventory can be bound to the Daml posting path without collapsing workflow authority into the off-ledger layer
- negative-path evidence becomes reproducible rather than anecdotal

Tradeoffs:

- the first demo runs on the Daml IDE ledger rather than the pinned Quickstart LocalNet because the runtime bridge remains unresolved
- the orchestration-layer execution report is broader than the future role-scoped disclosure profiles
- the Daml posting path records selected lots and committed workflow transitions, but valuation and concentration authority remain off-ledger in the policy and optimization artifacts

These tradeoffs are accepted because the repository needs a real end-to-end prototype now, but it must not claim a Quickstart-backed confidential-collateral deployment or hide the boundary between advisory computation and authoritative workflow state.
