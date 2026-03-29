# Policy Evaluation Report Specification

## Status

- Report version: `0.1.0`
- Canonical schema: [reports/schemas/policy-evaluation-report.schema.json](../../reports/schemas/policy-evaluation-report.schema.json)
- Primary command: `make policy-eval POLICY=... INVENTORY=...`

## Purpose

`PolicyEvaluationReport` is the first machine-readable output contract for the repository's off-ledger policy engine. It captures deterministic eligibility, haircut, lendable-value, concentration, control, and wrong-way-risk outcomes for one candidate collateral inventory set evaluated against one `CPL v0.1` policy.

The report exists to support:

- operator review of candidate collateral sets
- downstream optimization and workflow orchestration
- Quickstart-backed margin-call orchestration that must carry one declared policy decision artifact into workflow and adapter reporting
- schema-valid evidence for deterministic negative and positive paths
- invariant traceability for eligibility, haircut, concentration, and failure attribution

## Inputs

The current engine consumes:

1. a policy JSON file that conforms to [schema/cpl.schema.json](../../schema/cpl.schema.json)
2. a candidate inventory JSON file with:
   - top-level `inventorySetId`, `inventoryVersion`, `evaluationContext`, and `candidateLots`
   - normalized monetary values in one `valuationCurrency`
   - one target `settlementCurrency`
   - exposure-counterparty facts used for self-issued, counterparty-issued, and wrong-way-risk checks

Current inventory assumptions:

- `marketValue`, `nominalValue`, and `outstandingPrincipal` are already normalized into `evaluationContext.valuationCurrency`
- the engine does not perform FX conversion inside the report path
- absolute concentration thresholds must use the same currency as `valuationCurrency`

## Deterministic Rules

The report contract depends on these evaluation rules:

1. Input lots are evaluated in sorted `lotId` order.
2. Haircut rule matching uses the published CPL selector semantics: every selector field present in a rule must match.
3. If multiple haircut rules match, the engine applies the highest `haircutBps`.
4. If collateral currency differs from settlement currency, the engine adds the matching pair override or the policy default mismatch haircut.
5. Lendable value is rounded to cents using the policy's `haircuts.roundingMode`.
6. Concentration limits are evaluated on the subset of lots that survived non-concentration `REJECT` reasons.
7. `evaluationId` is a stable hash of the canonicalized policy and inventory inputs; the engine does not inject wall-clock timestamps into the report.

## Top-Level Structure

| Field | Meaning |
| --- | --- |
| `reportType` | Fixed to `PolicyEvaluationReport`. |
| `reportVersion` | Fixed to `0.1.0` for this contract. |
| `evaluationId` | Deterministic hash-based identifier for one policy-plus-inventory evaluation. |
| `overallDecision` | One of `ACCEPT`, `REJECT`, `ESCALATE`, or `REVIEW`. |
| `policy` | Policy identity, version, language version, and profile. |
| `inventory` | Inventory-set identity, version, `asOf`, settlement currency, valuation currency, and lot count. |
| `summary` | Stable counts and aggregate values for the evaluated set. |
| `portfolioReasons` | Machine-readable reasons that apply at the report or portfolio level. |
| `assetResults` | Per-lot eligibility, haircut, lendable-value, and reason details. |
| `concentrationResults` | Per-limit, per-bucket concentration observations and any breach reason. |

## Decisions And Reasons

### Overall decision

The report-level outcome is derived conservatively:

- any `REJECT` reason yields `overallDecision = REJECT`
- otherwise, any `ESCALATE` reason yields `overallDecision = ESCALATE`
- otherwise, any `REVIEW` reason yields `overallDecision = REVIEW`
- otherwise, the report is `ACCEPT`

### Asset decision

Each asset result uses:

- `ELIGIBLE`
- `INELIGIBLE`
- `ESCALATE`
- `REVIEW`

### Reason model

Every reason contains:

- a stable `code`
- a `category`
- a severity of `REJECT`, `ESCALATE`, or `REVIEW`
- a human-readable `message`
- a `policyPath`

Optional fields such as `policyRuleId`, `relatedLotIds`, `bucket`, `observedValue`, `thresholdValue`, and `currency` make failure attribution machine-readable without requiring the consumer to parse free-form text.

## Monetary And Concentration Semantics

- `marketValue`, `valuationBasisValue`, and `lendableValue` are expressed in `inventory.valuationCurrency`
- `baseHaircutBps`, `currencyMismatchHaircutBps`, and `totalHaircutBps` are basis-point integers
- `bucketValue` and `denominatorValue` in `concentrationResults` use the metric required by the policy threshold
- `observedRatio` is populated only for percentage thresholds

Current `JURISDICTION` concentration bucketing uses `issuanceJurisdiction`. This is an explicit `v0.1` engine decision and is recorded in ADR 0008 rather than left implicit.

## Current Scope And Limits

The current engine covers:

- eligibility filters
- haircuts and lendable value
- settlement-currency mismatch checks
- concentration limits
- encumbrance and segregation controls
- wrong-way-risk exclusions

The current engine does not yet evaluate:

- settlement-window timing
- workflow expiry handling
- substitution-right logic
- release-path logic tied to live encumbrance state
- FX conversion beyond normalized valuation inputs

Those remain separate concerns for later workflow, reference-data, and conformance phases. The current Quickstart-backed margin-call demo therefore treats `PolicyEvaluationReport` as a declared subordinate artifact rather than as a source of hidden runtime authority.
