# Collateral Policy Language (CPL) v0.1

## Status

- Version: `0.1.0`
- Repository phase: Milestone 1 / Phase 1
- Canonical schema: [schema/cpl.schema.json](../../schema/cpl.schema.json)
- Validation command: `make validate-cpl`

## Purpose

`CPL v0.1` is the repository's first machine-readable contract for collateral policy. It defines how a future policy engine, optimizer, workflow package, and report generator will consume the same policy artifact without hidden conventions.

`CPL v0.1` covers:

- policy identity and versioning
- effective times and authoring metadata
- eligibility filters for asset class, issue type, issuer, custodian, and jurisdiction
- haircut schedules and currency mismatch haircuts
- concentration limits
- encumbrance and segregation controls
- substitution rights
- settlement currency constraints, settlement windows, and expiries
- wrong-way-risk exclusions

`CPL v0.1` does not yet model valuation snapshots, workflow state, legal-document prose, optimization objectives, or executed decision reports. Those remain separate interfaces.

## Format And Normative Rules

The canonical interchange format is JSON validated against [schema/cpl.schema.json](../../schema/cpl.schema.json), using JSON Schema Draft 2020-12.

Normative authoring rules:

1. `cplVersion` identifies the language version and is fixed to `0.1.0` for this release.
2. `policyVersion` identifies the content version of one policy and uses semantic versioning.
3. Unknown properties are invalid. The schema uses `additionalProperties: false` throughout to prevent silent extension and parser drift.
4. Percentages used in concentration thresholds and free-allocation fields are decimal ratios. Example: `0.25` means `25%`.
5. Haircuts are expressed in basis points. Example: `250` means `2.50%`.
6. Currency codes use ISO-style three-letter uppercase strings. Jurisdictions use two-letter uppercase codes.
7. Time windows use explicit UTC offsets plus an IANA time-zone label for operator readability.

## Top-Level Model

| Section | Purpose | Required |
| --- | --- | --- |
| `cplVersion` | Declares the language version. | Yes |
| `policyId` | Stable policy identifier. | Yes |
| `policyVersion` | Content version for this policy. | Yes |
| `profile` | Intended market profile such as `central_bank` or `ccp`. | Yes |
| `metadata` | Authoring, ownership, approval, and tagging fields. | Yes |
| `effectivePeriod` | Policy activation interval. | Yes |
| `eligibility` | Static eligibility filters. | Yes |
| `haircuts` | Valuation basis, rounding, base haircuts, mismatch haircuts. | Yes |
| `concentrationLimits` | Portfolio and operational concentration caps. | Yes |
| `controlRequirements` | Encumbrance and segregation controls. | Yes |
| `substitutionRights` | Rights and approvals for collateral substitution. | Yes |
| `settlement` | Currency constraints, windows, and expiries. | Yes |
| `wrongWayRiskExclusions` | Explicit exclusions or escalation rules. | Yes |

## Section Semantics

### Metadata And Effective Period

`metadata` carries descriptive and governance fields. It is not optional commentary. Future loaders should treat it as part of the authoritative package for audit and explainability.

`effectivePeriod` defines the policy interval. `effectiveFrom` is inclusive. `effectiveUntil`, when present, is exclusive. A future policy engine must reject evaluation outside that interval rather than silently falling back to stale policy.

### Eligibility

An asset is eligible only if all of the following hold:

1. its asset class is in `eligibleAssetClasses`
2. its issue type is in `eligibleIssueTypes`
3. it satisfies `issuerFilters`
4. it satisfies `custodianFilters`
5. it satisfies `jurisdictionFilters`
6. it satisfies settlement currency rules
7. it does not trip a wrong-way-risk exclusion with `REJECT`

`issuerFilters`, `custodianFilters`, and `jurisdictionFilters` are intentionally separate. This mirrors real operating practice where issuer risk, custody control, and jurisdictional eligibility are distinct decision axes.

### Haircuts

`haircuts.schedule` is a list of selector-based haircut rules. A rule matches when every selector field present in that rule matches the asset and context.

Normative evaluation rule:

- if no haircut rule matches, the asset is ineligible
- if multiple haircut rules match, the evaluator must apply the highest `haircutBps`

This conservative fallback makes overlapping schedules deterministic until later phases add stronger authoring diagnostics.

`currencyMismatch.defaultHaircutBps` applies when collateral currency differs from settlement currency and `allowCollateralCurrencyMismatch` is `true`. A matching pair override replaces the default mismatch haircut for that currency pair.

### Concentration Limits

Each concentration limit applies independently. All applicable limits must pass.

`threshold.metric` distinguishes ratio-style caps from absolute-value caps:

- `PERCENT_OF_COLLATERAL_VALUE`
- `PERCENT_OF_LENDABLE_VALUE`
- `ABSOLUTE_MARKET_VALUE`

`breachAction` is part of the policy contract. It tells downstream systems whether a breach should reject immediately, escalate, or route to review.

### Control Requirements

`controlRequirements.encumbrance` addresses whether the asset must be free, whether reuse is allowed, and how much of the asset must remain unallocated.

`controlRequirements.segregation` describes required custody separation. `required: false` forces `segregationType: NONE`. Any segregated posture must name a non-`NONE` type.

### Substitution Rights

`substitutionRights` encodes whether substitution is allowed at all and, if it is, what approvals, notice, inventory-control mode, and replacement coverage rule apply.

Normative substitution rule:

- a substitution request is acceptable only if the replacement set still passes eligibility, haircut, concentration, control, and settlement checks after removing the outgoing collateral

### Settlement

`settlement.currencyConstraints` defines which settlement currencies are admissible and whether collateral-currency mismatch is allowed.

`settlementWindows` define when instructions may settle. A future workflow layer should treat actions outside the window according to `cutoffAction`, not according to local operator guesswork.

`expiry` distinguishes business-process validity from policy validity. Policy validity lives in `effectivePeriod`; instruction and call validity live in `settlement.expiry`.

### Wrong-Way Risk Exclusions

Wrong-way risk is explicit, not implicit. Every exclusion has an `action` and a machine-readable type. `CPL v0.1` supports:

- issuer equals exposure counterparty
- issuer in counterparty group
- issuer country equals exposure country
- custom issuer list
- custom jurisdiction list

This separation is deliberate. Later phases can add richer exposure graphs without changing the contract shape for common control cases.

## Market-Practice Mapping

### Central-Bank Style

Central-bank collateral frameworks typically separate eligibility, custody control, haircuting, and operating windows. `CPL v0.1` maps that by:

- using explicit issuer, custodian, and jurisdiction filters instead of one opaque eligibility list
- supporting maturity- and rating-sensitive haircut schedules
- modeling restricted custody and segregation requirements
- encoding operator-style settlement windows and controlled substitution

### Tri-Party Style

Tri-party utilities manage inventory, selection, and substitution operationally, but within a pre-agreed rule set. `CPL v0.1` maps that by:

- allowing custody/account filters to point at tri-party agents
- separating policy eligibility from inventory-control mode
- making substitution rights, notice, same-day settlement, and agent control explicit
- supporting concentration caps and same-day operational windows

### CCP Style

CCPs generally apply conservative haircuts, strict concentration limits, and strong operational controls. `CPL v0.1` maps that by:

- allowing multiple concurrent concentration limits by issuer, currency, and jurisdiction
- supporting conservative mismatch haircuts and strict breach actions
- capturing segregated custody requirements and CCP-controlled substitution
- making expiry and operating windows explicit for margin processing

### Bilateral CSA Style

Bilateral CSAs are negotiated and operational rather than centrally administered, but still require explicit currencies, haircuts, and substitution rights. `CPL v0.1` maps that by:

- allowing negotiated settlement currencies and mismatch haircuts
- permitting non-segregated structures where the legal arrangement allows them
- requiring explicit consent settings for substitution
- encoding wrong-way-risk deny lists for counterparty-issued paper

## Validation And Conformance

The first repository validation surface is schema-level, not engine-level.

Run:

```sh
make validate-cpl
```

The validation target:

- checks the schema against its metaschema
- validates the four published example policies
- exercises generated negative cases so the schema must reject missing required fields and unknown properties

## Known Limits In v0.1

`CPL v0.1` intentionally leaves some semantic checks to later phases:

- the schema does not compare whether `effectiveUntil` is later than `effectiveFrom`
- the schema does not encode rating-order arithmetic beyond enumerated rating labels
- the schema does not enforce cross-file uniqueness for `policyId`
- the schema does not yet model valuation freshness, legal thresholds, FX source lineage, or workflow approvals

Those limits are acceptable for `v0.1` because the immediate goal is to freeze a durable policy package shape for later policy-engine and workflow work.
