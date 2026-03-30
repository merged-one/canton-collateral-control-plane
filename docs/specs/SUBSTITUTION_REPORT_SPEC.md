# Substitution Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/substitution-report.schema.json](../../reports/schemas/substitution-report.schema.json)
- Primary commands:
  - `make demo-substitution`
  - `make demo-substitution-quickstart`

## Purpose

`SubstitutionReport` is the operator-facing machine-readable contract for end-to-end collateral substitution in the Control Plane. It ties together:

- the policy-evaluation artifact for each substitution scenario
- the optimization artifact for each scenario that seeks a replacement set
- the workflow result when the scenario crosses the Daml or Quickstart workflow boundary
- adapter execution and provider-visible status artifacts when the positive path continues into the Quickstart reference token adapter
- explicit atomicity evidence for both committed and blocked substitution paths

## Runtime Modes

The report now supports two runtime surfaces:

- `IDE_LEDGER` for `make demo-substitution`
- `QUICKSTART` for `make demo-substitution-quickstart`

The Quickstart mode adds:

- a scenario-scoped Quickstart seed receipt
- a real Quickstart workflow result with settlement-instruction visibility
- a substitution adapter execution report for the positive path
- a provider-visible Quickstart substitution status artifact for positive and blocked workflow paths
- `atomicityEvidence` that proves either atomic release-and-replacement commitment or blocked no-side-effects behavior

## Inputs

The current report path consumes one manifest under `examples/demo-scenarios/substitution/` and resolves:

1. one `CPL v0.1` policy file per scenario
2. one normalized inventory snapshot per scenario
3. one normalized obligation input when optimization is required
4. one workflow request payload when workflow execution is required
5. for Quickstart scenarios, one scenario-scoped LocalNet seed manifest that declares:
   - `scenarioId`
   - `obligationId`
   - `correlationId`
   - `policyVersion`
   - `snapshotId`
   - `decisionReference`
   - operator and custodian identity hints
   - incumbent encumbered lots
   - approved replacement lots

Substitution obligations may include a `substitutionRequest` block with:

- `requestId`
- `mustReplaceLotIds`
- `atomicityRequired`

## Deterministic Rules

The report depends on these rules:

1. every scenario runs policy evaluation first
2. optimization runs only when `runOptimization = true`
3. workflow execution runs only when `runWorkflow = true`
4. Quickstart adapter execution runs only when `runAdapter = true` and only after the Quickstart workflow result exposes a real pending-settlement instruction
5. the optimizer must treat `mustReplaceLotIds` as a hard release scope and reject portfolios that retain those lots
6. the workflow request must carry both the incumbent encumbered lots and the optimizer-selected replacement lots; the workflow and adapter do not re-select inventory independently
7. blocked Quickstart workflow paths must emit no adapter receipt and no replacement holding side effects
8. the top-level `substitutionReportId` is a stable hash of the manifest content plus the scenario results used to build the report

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `SubstitutionReport`. |
| `reportVersion` | Fixed to `0.1.0`. |
| `substitutionReportId` | Deterministic hash-based identifier for one substitution demo run. |
| `generatedAt` | UTC timestamp when the orchestration wrote the report. |
| `overallStatus` | `PASS` or `FAIL` for the full demo run. |
| `demo` | Command, runtime mode, manifest path, output directory, and scenario counts. |
| `artifacts` | Paths to the JSON substitution report, Markdown summary, and Markdown timeline. |
| `scenarios` | Per-scenario results including policy, optimization, workflow, adapter, blocked-phase, and atomicity-evidence outcomes. |
| `timeline` | Ordered execution-phase entries across the demo run. |
| `invariantChecks` | Pass or fail entries mapping the demo outputs back to repository invariants. |

## Scenario Semantics

Each scenario object records:

- whether the scenario is `POSITIVE` or `NEGATIVE`
- the operator-readable description and summary
- observed versus expected reason codes
- references to generated policy, optimization, workflow-input, workflow-result, and Quickstart-local artifacts
- the policy decision, optimization status, recommended action, incumbent lot set, and replacement lot set
- `workflowRuntime`, `blockedPhase`, and `adapterOutcome`
- `atomicityEvidence` when the scenario exercises Quickstart workflow or adapter behavior

Quickstart substitution scenarios additionally record:

- `quickstartSeedReceiptPath`
- `adapterExecutionReportPath`
- `adapterStatusPath`

## Workflow Result Semantics

When present, `workflow` records:

- `substitutionState`
- `securedPartyApproval` and `custodianApproval`
- `settlementInstructionId` and `settlementInstructionState` where applicable
- `currentEncumberedLotIds`, `releasedLotIds`, `replacementLotIds`, and `activeEncumberedLotIds`
- `atomicityOutcome`
- `executionReports` and `executionReportCount`
- `controlChecks`
- ordered workflow `steps`

In Quickstart mode, `workflowGate` distinguishes:

- `PREPARE_FOR_ADAPTER` for the positive handoff into the adapter
- `ATTEMPT_PARTIAL_SETTLEMENT` for the blocked partial-substitution path

## Atomicity Evidence Semantics

`atomicityEvidence` is the report-level proof surface for Quickstart-backed substitution semantics. It records:

- `proofStatus`
- `incumbentEncumberedLotIds`
- `approvedReplacementLotIds`
- `adapterActionReleaseLotIds`
- `adapterActionReplacementLotIds`
- `finalReleasedLotIds`
- `finalActiveEncumberedLotIds`
- `providerVisibleCurrentHoldingLotIds`
- `providerVisibleReplacementHoldingLotIds`
- `providerVisibleAdapterReceiptCount`
- `note`

The current proof statuses are:

- `ATOMICALLY_COMMITTED` for the positive Quickstart path
- `BLOCKED_NO_SIDE_EFFECTS` for the blocked partial-substitution path
- `IDE_LEDGER_WORKFLOW_ONLY` for the original IDE-ledger workflow path

## Timeline Semantics

`timeline` records real execution phases in order:

- `POLICY_EVALUATION`
- `OPTIMIZATION`
- `QUICKSTART_SEED`
- `WORKFLOW`
- `ADAPTER`

The Markdown timeline derived from the report keeps the same order and points at the generated JSON artifacts for each phase.

## Current Scope And Limits

The current contract covers:

- the original IDE-ledger substitution prototype
- one real Quickstart-backed positive atomic replacement path
- one Quickstart policy-blocked negative path
- one Quickstart blocked partial-substitution path
- workflow-to-adapter evidence that the adapter consumed the real Quickstart handoff artifact
- provider-visible post-substitution and blocked-path status evidence

The current contract does not yet cover:

- Quickstart-backed return execution
- role-scoped substitution-report disclosure profiles
- production custodian or issuer adapter integrations
- multi-obligation substitution bundles
- settlement-window enforcement beyond the current workflow scaffolding
