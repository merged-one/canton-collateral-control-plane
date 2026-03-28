# Substitution Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/substitution-report.schema.json](../../reports/schemas/substitution-report.schema.json)
- Primary command: `make demo-substitution`

## Purpose

`SubstitutionReport` is the first machine-readable operator-facing contract for end-to-end collateral substitution in the Control Plane. It ties together:

- the policy-evaluation artifact for each substitution scenario
- the optimization artifact for each scenario that seeks a replacement set
- the committed or blocked Daml substitution workflow result when workflow execution is required
- invariant-linked negative-path evidence for ineligibility, concentration failure, unauthorized release, and partial-settlement atomicity violations

The contract exists so operators and reviewers can verify that the repository now proves real encumbered-collateral replacement behavior without guessing how policy, optimization, approvals, and workflow outcomes relate.

## Inputs

The current substitution-report path consumes one manifest under `examples/demo-scenarios/substitution/` and resolves:

1. one `CPL v0.1` policy file per scenario
2. one normalized inventory snapshot per scenario
3. one normalized obligation input when optimization is required
4. one parameterized Daml Script request when workflow execution is required

Substitution obligations may also include a `substitutionRequest` block with:

- `requestId`
- `mustReplaceLotIds`
- `atomicityRequired`

The manifest additionally defines:

- which scenarios should run optimization
- which scenarios should invoke the Daml substitution workflow path
- expected policy, optimization, workflow, and reason-code outcomes
- workflow metadata such as correlation ID, source and destination accounts, settlement system, and simulated control-failure flags

## Deterministic Rules

The report depends on these rules:

1. Every scenario runs policy evaluation first.
2. Optimization runs only for scenarios marked `runOptimization = true`.
3. Daml workflow execution runs only for scenarios marked `runWorkflow = true` and only after optimization has produced a valid replacement set.
4. The optimizer must treat `mustReplaceLotIds` as a hard release scope and reject candidate portfolios that retain those lots.
5. The workflow request carries both the incumbent encumbered lots and the optimizer-selected replacement lots; the Daml layer does not re-select inventory independently.
6. `substitutionRequest.atomicityRequired` must match the policy's `partialSubstitutionAllowed` rule as inverted into workflow semantics.
7. Negative workflow scenarios must fail closed: incumbent encumbrances remain active, and the report records explicit control-check reason codes.
8. The top-level `substitutionReportId` is a stable hash of the manifest content plus the scenario results used to build the report.

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `SubstitutionReport`. |
| `reportVersion` | Fixed to `0.1.0`. |
| `substitutionReportId` | Deterministic hash-based identifier for one substitution demo run. |
| `generatedAt` | UTC timestamp when the orchestration wrote the report. |
| `overallStatus` | `PASS` or `FAIL` for the full demo run. |
| `demo` | Command, manifest path, output directory, primary optimization artifact, and scenario counts. |
| `artifacts` | Paths to the JSON substitution report, Markdown summary, and Markdown timeline. |
| `scenarios` | Per-scenario results including policy, optimization, workflow, and reason-code outcomes. |
| `timeline` | Ordered execution-phase entries across the demo run. |
| `invariantChecks` | Pass/fail entries mapping the demo outputs back to repository invariants. |

## Scenario Semantics

Each scenario object records:

- whether the scenario is `POSITIVE` or `NEGATIVE`
- the operator-readable description and summary
- observed versus expected reason codes
- references to the generated policy-evaluation, optimization, workflow-input, and workflow-result artifacts
- the policy decision, optimization status, recommended action, and incumbent versus replacement lot sets
- the Daml workflow result when workflow execution is present

Positive scenarios currently emit:

- one policy-evaluation report
- one optimization report
- one workflow-input JSON artifact
- one Daml workflow-result JSON artifact
- one closed substitution path with released incumbent encumbrances and active replacement encumbrances

Negative scenarios currently emit:

- one policy-evaluation report for every negative case
- one optimization report only when the scenario proves a concentration or workflow-control outcome
- one workflow-input and workflow-result JSON artifact only when the scenario must prove an authorization or atomicity failure on the Daml boundary

## Workflow Result Semantics

When present, `workflow` records:

- `substitutionState`
- `securedPartyApproval` and `custodianApproval`
- `currentEncumberedLotIds`, `releasedLotIds`, `replacementLotIds`, and `activeEncumberedLotIds`
- `atomicityOutcome`
- `executionReports` and `executionReportCount`
- `controlChecks`
- ordered workflow `steps`

These fields exist so a consumer can distinguish:

- a committed atomic replacement
- a blocked pre-approval settlement attempt
- an unauthorized release attempt
- a rejected partial-settlement attempt when atomicity is required

## Timeline Semantics

`timeline` records real execution phases in order:

- `POLICY_EVALUATION`
- `OPTIMIZATION`
- `WORKFLOW`

The Markdown timeline derived from the report keeps the same order and points at the generated JSON artifacts for each phase.

## Current Scope And Limits

The current `SubstitutionReport` contract covers:

- the first end-to-end substitution demo path
- one real positive atomic replacement path
- four real negative substitution paths
- invariant-linked evidence references
- operator-facing Markdown summary and timeline artifacts

The current contract does not yet cover:

- role-scoped disclosure profiles
- Quickstart-backed workflow execution
- live asset-adapter evidence
- multi-obligation or chained substitution bundles
- external audit packaging beyond repo-local artifacts

Those remain future work for workflow disclosure profiles, Quickstart deployment, and the broader conformance suite.
