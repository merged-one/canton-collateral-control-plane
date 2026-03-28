# Execution Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/execution-report.schema.json](../../reports/schemas/execution-report.schema.json)
- Primary command: `make demo-margin-call`

## Purpose

`ExecutionReport` is the first machine-readable operator-facing contract that ties together:

- the policy-evaluation artifact for one candidate collateral set
- the optimization artifact for one margin obligation
- the committed Daml workflow result for the positive posting path
- negative-path evidence for blocked scenarios in the same demo run

The contract exists to prove that the Canton Collateral Control Plane can now generate auditable end-to-end demo evidence without inventing workflow success or hiding the relationship between policy, optimization, and execution artifacts.

Substitution now uses a separate [SUBSTITUTION_REPORT_SPEC.md](./SUBSTITUTION_REPORT_SPEC.md) contract so the margin-call `ExecutionReport` does not absorb substitution-specific approval and atomicity semantics.

## Inputs

The current execution-report path consumes one manifest under `examples/demo-scenarios/margin-call/` and resolves:

1. one `CPL v0.1` policy file per scenario
2. one normalized inventory snapshot per scenario
3. one normalized obligation input when optimization is required
4. one parameterized Daml Script request for the positive workflow path

The manifest also defines:

- which scenarios should run optimization
- which scenario should run the Daml workflow path
- expected policy, optimization, and workflow outcomes
- workflow metadata such as correlation ID, due time, source account, and destination account

## Deterministic Rules

The report depends on these rules:

1. Every scenario runs policy evaluation first.
2. Optimization runs only for scenarios marked `runOptimization = true`.
3. Daml workflow execution runs only for scenarios marked `runWorkflow = true` and only after the positive scenario has produced a valid optimizer recommendation.
4. The positive Daml Script receives the optimizer-selected lots through `--input-file`; the workflow layer does not infer inventory selection independently.
5. Negative scenarios do not fabricate workflow artifacts when the policy or optimization layers block execution.
6. The top-level `executionId` is a stable hash of the manifest content plus the scenario results used to build the report.

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `ExecutionReport`. |
| `reportVersion` | Fixed to `0.1.0`. |
| `executionId` | Deterministic hash-based identifier for one demo run. |
| `generatedAt` | UTC timestamp when the orchestration wrote the report. |
| `overallStatus` | `PASS` or `FAIL` for the full demo run. |
| `demo` | Command, manifest path, output directory, primary policy artifact, and scenario counts. |
| `artifacts` | Paths to the JSON execution report, Markdown summary, and Markdown timeline. |
| `scenarios` | Per-scenario results including policy, optimization, workflow, and reason-code outcomes. |
| `timeline` | Ordered execution-phase entries across the demo run. |
| `invariantChecks` | Pass/fail entries that map the demo outputs back to repository invariants. |

## Scenario Semantics

Each scenario object records:

- whether the scenario is `POSITIVE` or `NEGATIVE`
- the operator-readable description and summary
- observed versus expected reason codes
- references to the generated policy-evaluation, optimization, and workflow artifacts
- the policy decision, optimization status, recommended action, and selected lot IDs
- the Daml workflow result for the positive path when present

Positive scenarios currently emit:

- one policy-evaluation report
- one optimization report
- one Daml workflow result JSON artifact
- one closed margin-call path and one closed posting path in the Daml result

Negative scenarios currently emit:

- one policy-evaluation report for all negative cases
- one optimization report only when the scenario needs to prove insufficient lendable value
- no Daml workflow artifact when the scenario is blocked before posting

## Timeline Semantics

`timeline` records the real execution phases in order:

- `POLICY_EVALUATION`
- `OPTIMIZATION`
- `WORKFLOW`

The Markdown timeline derived from the report also includes the ordered step list returned by the positive Daml Script.

## Current Scope And Limits

The current `ExecutionReport` contract covers:

- the first end-to-end margin-call demo path
- one real positive posting path
- three real negative paths
- invariant pass/fail evidence references
- operator-facing Markdown summary and timeline artifacts

The current contract does not yet cover:

- substitution-specific workflow reporting, which now lives in `SubstitutionReport`
- role-scoped disclosure profiles
- Quickstart-backed workflow execution
- live asset-adapter evidence
- multi-obligation workflow bundles
- external audit packaging beyond repo-local artifacts

Those remain future work for workflow disclosure profiles, Quickstart deployment, and the broader conformance suite.
