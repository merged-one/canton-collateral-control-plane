# Optimization Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/optimization-report.schema.json](../../reports/schemas/optimization-report.schema.json)
- Primary command: `make optimize POLICY=... INVENTORY=... OBLIGATION=...`

## Purpose

`OptimizationReport` is the first machine-readable output contract for the Control Plane's optimization layer. It records how the optimizer screened candidate lots, evaluated concentration-aware portfolios, ranked feasible allocations, and chose either a new post set, a substitution recommendation, or a clean no-solution result.

The report exists to support:

- operator review of best-to-post and substitution decisions
- workflow-layer consumption of advisory optimization output without collapsing authority boundaries
- Quickstart-backed margin-call orchestration that must hand an explicit selected-lot set into the workflow-preparation and adapter chain
- legal, audit, and control review of deterministic explanation traces
- reproducible negative-path evidence for shortfall and concentration-blocked scenarios

## Inputs

The current optimizer consumes:

1. a policy JSON file that conforms to [schema/cpl.schema.json](../../schema/cpl.schema.json)
2. a normalized inventory JSON file in the same shape used by the policy engine
3. an obligation JSON file with:
   - `obligationId`
   - `obligationVersion`
   - `asOf`
   - `settlementCurrency`
   - `coverageMetric`
   - `obligationAmount`
   - optional `currentPostedLotIds`
   - optional `substitutionRequest` with `requestId`, `mustReplaceLotIds`, and `atomicityRequired`

Current obligation assumptions:

- `coverageMetric` must be `LENDABLE_VALUE`
- `obligationAmount` is already normalized into the inventory valuation and settlement currency basis
- `obligation.asOf` must match `inventory.evaluationContext.asOf`
- `obligation.settlementCurrency` must match `inventory.evaluationContext.settlementCurrency`

## Deterministic Rules

The contract depends on these optimizer rules:

1. Candidate lots are screened in sorted `lotId` order using the policy engine's non-concentration checks.
2. Portfolio search considers only lots that are individually admissible on those non-concentration checks.
3. Candidate subsets are enumerated deterministically by subset size and then by sorted `lotId`.
4. A feasible portfolio must both cover the obligation amount and yield `overallDecision = ACCEPT` after concentration checks are applied.
5. The lexicographic objective is:
   - minimize posted market value
   - then minimize haircut cost
   - then minimize excess coverage
   - then minimize lot count
   - then use sorted lot IDs only as a deterministic tie-break
6. If a current posted set exists and is economically equal to the best alternative on the first four objective dimensions, the optimizer keeps the current set to avoid unnecessary churn.
7. If `substitutionRequest.mustReplaceLotIds` is present, candidate subsets that retain one of those lots are invalid even when the incumbent set remains feasible.
8. If a valid replacement set exists for a scoped substitution request, the optimizer may still recommend `SUBSTITUTE` rather than `KEEP_CURRENT_POSTED_SET` because the request requires release of named incumbent lots.
9. `optimizationId` is a stable hash of canonicalized policy, inventory, and obligation inputs; the engine does not inject wall-clock timestamps.

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `OptimizationReport`. |
| `reportVersion` | Fixed to `0.1.0`. |
| `optimizationId` | Deterministic hash-based identifier for one optimization request. |
| `status` | `OPTIMAL` or `NO_SOLUTION`. |
| `recommendedAction` | `POST_NEW_SET`, `SUBSTITUTE`, `KEEP_CURRENT_POSTED_SET`, or `NO_SOLUTION`. |
| `objective` | Published ranking sequence used by the optimizer. |
| `policy` | Policy identity and profile. |
| `inventory` | Inventory snapshot identity and currencies. |
| `obligation` | Obligation identity, coverage metric, requested amount, current posted set if supplied, and substitution-request scope if supplied. |
| `candidateUniverse` | Candidate-screening counts plus per-lot admissibility summaries. |
| `currentPortfolio` | Optional evaluation of the currently posted set. |
| `recommendedPortfolio` | The selected portfolio when a feasible recommendation exists. |
| `substitutionRecommendation` | Machine-readable add/remove deltas between the current and recommended sets, including scoped-release metadata when present. |
| `explanationTrace` | Ordered search and decision trace entries. |

## Portfolio Semantics

Each portfolio object includes:

- `policyEvaluationId` to correlate back to the underlying policy-decision logic
- `policyDecision` so a consumer can distinguish hard policy failure from pure shortfall
- `allocatedMarketValue`, `allocatedLendableValue`, `shortfallAmount`, `excessAmount`, and `haircutCostAmount`
- `objectiveVector` so ranking is machine-readable
- `blockingReasonCodes` for non-feasible sets
- `selectedLots` and `concentrationResults` for direct review

`shortfallAmount` and `excessAmount` are always explicit. The optimizer does not infer feasibility from a missing field.

## Explanation Trace Semantics

Each explanation trace entry includes:

- a stable `step` number
- a `stage` of `SCREENING`, `CURRENT_PORTFOLIO`, `SEARCH`, or `DECISION`
- an `outcome`
- a short human-readable `message`
- optional `lotIds`, `reasonCodes`, `coverageAmount`, and `objectiveSnapshot`

The trace is intentionally deterministic and append-only for one request. Consumers should not treat it as free-form debug output.

## Substitution Request Semantics

When `obligation.substitutionRequest` is present:

- `mustReplaceLotIds` identifies incumbent lots that must not remain in the recommended set
- `atomicityRequired` captures whether downstream workflow execution must reject partial replacement scope
- `substitutionRecommendation` includes `requestId`, `atomicityRequired`, `mustReplaceLotIds`, and `retainedLotIds`
- `NO_SOLUTION` may occur even when the incumbent current portfolio remains feasible, because the substitution request can force release of encumbered lots that leave no compliant replacement set

## Current Scope And Limits

The current optimizer covers:

- best-to-post lot-set selection
- substitution recommendation against an existing posted set
- concentration-aware allocation
- deterministic explanation traces
- explicit no-solution reporting

The current optimizer does not yet cover:

- live pricing curves or repo specialness inputs
- partial-lot splitting
- workflow-coupled reservation or settlement sequencing
- consent, notice-period, or settlement-window enforcement in the search objective
- production-scale optimization heuristics beyond the current deterministic exhaustive subset search

Those remain future layers for reference-data contracts, workflow execution, and conformance expansion. The current Quickstart-backed margin-call demo therefore consumes `OptimizationReport` as an advisory but explicit handoff artifact rather than as a hidden selection shortcut.
