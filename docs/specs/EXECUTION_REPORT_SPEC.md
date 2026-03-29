# Execution Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/execution-report.schema.json](../../reports/schemas/execution-report.schema.json)
- Primary commands:
  - `make demo-margin-call`
  - `make demo-margin-call-quickstart`

## Purpose

`ExecutionReport` is the first machine-readable operator-facing contract that ties together:

- the policy-evaluation artifact for one candidate collateral set
- the optimization artifact for one margin obligation
- the committed workflow result for the positive posting path
- the Quickstart adapter result and adapter-status evidence when the runtime mode executes a real data-plane action
- negative-path evidence for blocked scenarios in the same demo run

The contract exists to prove that the Canton Collateral Control Plane can now generate auditable end-to-end demo evidence without inventing workflow success, adapter success, or hidden relationships between policy, optimization, workflow, and execution artifacts.

Substitution now uses a separate [SUBSTITUTION_REPORT_SPEC.md](./SUBSTITUTION_REPORT_SPEC.md) contract so the margin-call `ExecutionReport` does not absorb substitution-specific approval and atomicity semantics.

## Inputs

The current execution-report path consumes one manifest under `examples/demo-scenarios/margin-call/` and resolves:

1. one `CPL v0.1` policy file per scenario
2. one normalized inventory snapshot per scenario
3. one normalized obligation input when optimization is required
4. one runtime-specific workflow request for the positive workflow path
5. one Quickstart seed manifest when the runtime mode is `QUICKSTART`

The manifest also defines:

- which scenarios should run optimization
- which scenario should run the workflow path
- which scenario should run the adapter path
- expected policy, optimization, workflow, and adapter outcomes
- workflow metadata such as correlation ID, due time, source account, and destination account for IDE-ledger mode
- Quickstart workflow gates and seed manifests for Quickstart mode

## Deterministic Rules

The report depends on these rules:

1. Every scenario runs policy evaluation first.
2. Optimization runs only for scenarios marked `runOptimization = true`.
3. Workflow execution runs only for scenarios marked `runWorkflow = true` and only after the scenario has produced a valid optimizer recommendation.
4. The workflow layer receives the optimizer-selected lots through an explicit workflow-input artifact; it does not infer inventory selection independently.
5. In `QUICKSTART` mode, scenario seeding runs before workflow execution and the adapter runs only when the scenario is marked `runAdapter = true`, the workflow gate is `PREPARE_FOR_ADAPTER`, and the workflow result exposes a real settlement instruction.
6. Negative scenarios do not fabricate workflow or adapter artifacts when upstream policy, optimization, or workflow gating blocks execution.
7. The top-level `executionId` is a stable hash of the manifest content, runtime mode, and scenario results used to build the report.

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `ExecutionReport`. |
| `reportVersion` | Fixed to `0.1.0`. |
| `executionId` | Deterministic hash-based identifier for one demo run. |
| `generatedAt` | UTC timestamp when the orchestration wrote the report. |
| `overallStatus` | `PASS` or `FAIL` for the full demo run. |
| `demo` | Command, runtime mode, manifest path, output directory, primary policy artifact, and scenario counts. |
| `artifacts` | Paths to the JSON execution report, Markdown summary, and Markdown timeline. |
| `scenarios` | Per-scenario results including policy, optimization, workflow, and reason-code outcomes. |
| `timeline` | Ordered execution-phase entries across the demo run. |
| `invariantChecks` | Pass/fail entries that map the demo outputs back to repository invariants. |

## Scenario Semantics

Each scenario object records:

- whether the scenario is `POSITIVE` or `NEGATIVE`
- the operator-readable description and summary
- observed versus expected reason codes
- references to the generated policy-evaluation, optimization, workflow, seed, and adapter artifacts
- the policy decision, optimization status, recommended action, and selected lot IDs
- the workflow result for the positive path when present
- the blocked phase and adapter outcome when the runtime is `QUICKSTART`

Positive IDE-ledger scenarios emit:

- one policy-evaluation report
- one optimization report
- one Daml workflow result JSON artifact
- one closed margin-call path and one closed posting path in the Daml result

Positive Quickstart scenarios emit:

- one policy-evaluation report
- one optimization report
- one Quickstart workflow result JSON artifact that stops at the adapter handoff point
- one Quickstart seed receipt scoped to the scenario runtime directory
- one adapter execution report plus one provider-visible adapter status artifact
- one final execution report that references all subordinate artifacts

Negative scenarios emit:

- one policy-evaluation report for all negative cases
- one optimization report only when the scenario needs to prove a downstream block rather than an immediate policy block
- no workflow artifact when the scenario is blocked before posting
- no adapter execution artifact when the scenario is blocked before workflow or when workflow gating rejects the posting
- a provider-visible adapter status artifact only when the Quickstart negative path must prove no downstream movement occurred

## Timeline Semantics

`timeline` records the real execution phases in order:

- `POLICY_EVALUATION`
- `OPTIMIZATION`
- `QUICKSTART_SEED`
- `WORKFLOW`
- `ADAPTER`

The Markdown timeline derived from the report also includes the ordered step list returned by the positive workflow path. `QUICKSTART_SEED` and `ADAPTER` appear only for `QUICKSTART` runs, and `ADAPTER` may be marked `SKIPPED` when the workflow is intentionally blocked before the adapter boundary.

## Current Scope And Limits

The current `ExecutionReport` contract covers:

- the IDE-ledger and Quickstart-backed end-to-end margin-call demo paths
- one real positive posting path on the IDE ledger
- one real positive Quickstart workflow-plus-adapter path
- negative paths that block before workflow execution or at the Quickstart workflow gate without fabricating adapter success
- invariant pass/fail evidence references
- operator-facing Markdown summary and timeline artifacts

The current contract does not yet cover:

- return-specific and substitution-specific workflow reporting, which now live in `ReturnReport` and `SubstitutionReport`
- role-scoped disclosure profiles
- substitution or return execution on Quickstart
- substitution or return adapter evidence
- multi-obligation workflow bundles
- external audit packaging beyond repo-local artifacts

Those remain future work for workflow disclosure profiles, broader Quickstart runtime coverage, and the broader conformance suite.
