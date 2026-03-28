# Collateral Domain Model

## Domain Scope

The domain model describes the reusable concepts the control plane must understand regardless of whether the workflow is bilateral margin, tri-party collateral management, or CCP-style control. It is intentionally neutral with respect to asset venue, custody provider, and product type.

## Domain Partitions

| Partition | Purpose |
| --- | --- |
| reference and identity | define assets, issuers, custody locations, and counterparties |
| policy and schedule | define reusable rules for eligibility, haircuts, concentration, control, and timing |
| inventory and encumbrance | describe what collateral exists, where it sits, and what portion is committed |
| workflow and settlement | describe obligations, requests, approvals, and instructions |
| reporting and evidence | describe what happened and how it can be reconstructed |

## Core Concepts

| Concept | Kind | Definition | Key Fields | Relationship Notes |
| --- | --- | --- | --- | --- |
| `CollateralAsset` | reference entity | canonical definition of an asset type that may be pledged or delivered as collateral | `asset_id`, issuer, asset class, currency, settlement system, token adapter reference, jurisdiction, transferability flags | one asset may appear in many inventory lots and valuation snapshots |
| `CollateralInventoryLot` | operational entity | a specific position or lot owned or controlled by a provider and available for potential collateral use | `lot_id`, `asset_id`, owner party, custodian, account, quantity, availability window, provenance, control method | smallest unit the Control Plane uses for selection, encumbrance, substitution, and return |
| `EncumbranceState` | operational entity | authoritative statement of how much of a lot is free, reserved, pledged, pending release, or released | `encumbrance_id`, `lot_id`, obligation reference, state, quantity, effective time | derived and committed through workflow state; prevents double-encumbrance |
| `EligibilitySchedule` | policy entity | versioned schedule defining whether an asset is acceptable under specified conditions | schedule ID, effective time range, allowed and disallowed buckets, control conditions, settlement windows | referenced by a policy package; evaluated against asset facts and workflow context |
| `HaircutSchedule` | policy entity | versioned schedule that maps asset and context buckets to haircut percentages and rounding rules | schedule ID, valuation basis, haircut percent, rounding rule, stress bucket | used by the policy engine to compute lendable value |
| `ConcentrationLimitRule` | policy entity | versioned cap on exposure to a bucket such as issuer, asset class, currency, jurisdiction, or custodian | rule ID, bucket definition, threshold metric, breach handling mode | evaluated using current and proposed encumbrance state |
| `CallObligation` | workflow entity | requirement for a provider to post or maintain collateral against an exposure | obligation ID, secured party, provider, required coverage, due time, policy version, status | may be satisfied by one or more settlement instructions and encumbrances |
| `SubstitutionRequest` | workflow entity | request to replace currently posted collateral with alternate collateral while preserving coverage | request ID, obligation ID, released lot set, replacement lot set, expiry time, approval state | must reference both current encumbrances and proposed replacements |
| `ReturnRequest` | workflow entity | request to release excess or no-longer-required collateral back to the provider | request ID, obligation ID, lot set, requested quantity, reason, expiry time | evaluated against post-return coverage and release rights |
| `SecuredParty` | actor role | counterparty or control beneficiary entitled to receive or control collateral | party ID, legal entity reference, approval rights, report profile | usually the beneficiary of a call obligation |
| `Pledgor` or `CollateralProvider` | actor role | party that owns or controls eligible collateral and may post, substitute, or request return | party ID, custody relationships, optimization preferences, authorization set | owns inventory lots and initiates many workflow actions |
| `Custodian` or `ControlRole` | actor role | party responsible for settlement, control acknowledgment, or release execution | party ID, custody account references, control scope, approval rights | may need visibility only to settlement and control data, not full exposure context |
| `ValuationSnapshot` | immutable record | frozen set of prices, FX rates, issuer attributes, and contextual facts used in a decision | snapshot ID, as-of time, source references, price set, FX set, static data digest | every policy decision and report should reference a snapshot ID |
| `SettlementInstruction` | workflow entity | explicit instruction to move collateral, change control, or release collateral | instruction ID, source and destination account or party, quantity, timing window, status | generated by workflow state and consumed by custodian or asset adapters |
| `ExecutionReport` | reporting entity | machine-readable record of what committed, under which inputs, and with which outcome | report ID, correlation ID, workflow type, policy version, snapshot ID, event list, outcome | derived from committed state and used for audit, operations, and external integration |

## Supporting Concepts

| Concept | Purpose |
| --- | --- |
| `PolicyPackage` | groups the active eligibility, haircut, concentration, control, and settlement schedules used together |
| `PolicyDecisionReport` | captures the deterministic eligibility and lendable-value result for a specific workflow context |
| `OptimizationProposal` | captures ranked feasible candidates and explanation traces |
| `ApprovalRecord` | records which role approved, rejected, or let a request expire |
| `ExceptionRecord` | captures why a workflow moved to an exception path and what remediation is required |

## Relationship Rules

- a `CollateralAsset` may back many `CollateralInventoryLot` records, but each lot keeps its own custody and provenance facts
- a `CollateralInventoryLot` may participate in multiple obligations only up to its unencumbered quantity
- an `EncumbranceState` always points to both a lot and an obligation or request context
- a `CallObligation` references exactly one policy version, though that version may itself contain multiple schedules
- a `SubstitutionRequest` and a `ReturnRequest` must not implicitly change encumbrance state until the workflow layer commits the change
- an `ExecutionReport` is valid only if it can be traced to committed workflow objects and immutable inputs

## Canonical State Questions

The domain model is structured so implementation can answer the following questions without ambiguity:

- what collateral exists and where is it controlled?
- how much of each lot is free versus committed?
- under which policy version and snapshot was a decision made?
- which party initiated, approved, or rejected a workflow step?
- what settlement action was instructed and did it complete?
- what report proves the committed outcome?
