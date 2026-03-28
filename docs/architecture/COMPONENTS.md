# Components

## Component Inventory

| Component | Responsibility | Key Inputs | Key Outputs | Persistence |
| --- | --- | --- | --- | --- |
| Policy authoring and registry | author, validate, version, and publish policy packages and schedules | policy drafts, profile templates, approval metadata | effective policy package, schedule identifiers | policy registry store |
| Reference data and valuation adapter | normalize asset facts, prices, FX rates, issuer data, and custody metadata into immutable snapshots | market data, static reference data, custody facts | valuation snapshot, normalized asset facts | snapshot store |
| Policy evaluation engine | evaluate eligibility, haircut schedule, concentration limits, encumbrance availability, and release rules deterministically | policy package, valuation snapshot, inventory facts, obligation context | policy decision report with explanations | reproducible decision cache optional |
| Optimization engine | produce candidate posting and substitution plans under policy-feasible constraints | policy decision report, inventory availability, objective settings, operational constraints | optimization proposal and ranking trace | proposal cache optional |
| Daml workflow package | encode obligations, encumbrance records, approvals, settlement instructions, and lifecycle transitions | approved actions, party identities, policy references | authoritative ledger state | Canton ledger |
| Workflow orchestrator | translate integration requests into Daml choices and correlate multi-step workflow progress | API requests, optimization references, party approvals | submitted commands, workflow correlation state | orchestrator store optional |
| Reporting and evidence service | generate execution reports, audit views, and traceability links from committed state | Canton events, decision reports, snapshot metadata | execution report, evidence references | report store |
| Integration gateway | expose stable interfaces to external apps and adapters without leaking internal template layout | consumer requests, auth context | API responses, request IDs, status views | gateway logs |
| Demo and runtime overlay | start LocalNet, deploy packages, wire adjacent services, and expose reproducible operator commands | pinned Quickstart distribution, overlay config, container images | runnable prototype environment | environment config |

## Dependency Rules

1. Policy authoring and registry may be read by the evaluation engine, optimizer, reporter, and workflow orchestrator, but workflow state must not mutate policy definitions.
2. The policy evaluation engine depends on policy and snapshot inputs only; it must remain side-effect free from a business perspective.
3. The optimization engine may consume policy decisions and inventory state, but it may not bypass the policy engine or commit encumbrances.
4. The Daml workflow package is the only component allowed to change obligation, approval, encumbrance, and settlement state.
5. The reporting and evidence service reads committed state and immutable references; it does not act as a hidden orchestrator.
6. Demo infrastructure may host components and seed data, but it may not alter domain semantics or fabricate successful outcomes.

## Canonical Interfaces

| Interface | Producer | Consumer | Purpose |
| --- | --- | --- | --- |
| `PolicyPackage` | policy registry | evaluation engine, optimizer, workflow orchestrator, reporter | share the versioned rules and schedule identifiers used by a workflow |
| `ValuationSnapshot` | reference data adapter | evaluation engine, reporter | freeze market and reference inputs for reproducible decisions |
| `PolicyDecisionReport` | evaluation engine | optimizer, workflow orchestrator, reporter | explain eligibility, haircuts, concentration checks, and release constraints |
| `OptimizationProposal` | optimization engine | workflow orchestrator, reporter | propose ranked posting or substitution candidates |
| `SettlementInstruction` | workflow package and orchestrator | custodian role, reporter, external adapters | direct delivery, control, release, or return actions |
| `ExecutionReport` | reporting service | operators, auditors, external consumers | describe what actually committed and why |

## Responsibilities By Concern

### Policy layer

- defines reusable schedules and profiles
- does not know workflow contract IDs
- does not store counterparty-specific runtime state

### Decision layer

- computes deterministic decisions from explicit inputs
- produces rejection reasons and explanation traces
- does not choose business objectives on its own

### Optimization layer

- ranks feasible assets and substitutions
- treats policy rejections as hard constraints
- does not issue approvals or alter ledger state

### Workflow layer

- owns lifecycle transitions and atomic settlement behavior
- captures party approvals and control checks
- does not embed schedule math directly in templates unless cached as referenced output

### Reporting layer

- renders state and evidence after commit
- supports machine-readable execution output
- does not hide missing data with inferred or invented fields

### Runtime layer

- packages and deploys the prototype
- keeps upstream Quickstart separable from Control Plane overlays
- remains replaceable without changing domain documents

## Failure Containment

| Failure | Containment Rule |
| --- | --- |
| invalid policy package | reject at publication time; do not let workflow depend on it |
| stale valuation snapshot | fail evaluation or mark results unusable; do not silently recompute with hidden data |
| optimizer failure | preserve workflow safety by falling back to manual or deterministic non-optimized submission |
| settlement or custodian failure | keep workflow in an exception state rather than partially releasing encumbrance |
| reporting failure | workflow state remains authoritative; reports can be regenerated from committed state |
| LocalNet bootstrap failure | treat as environment failure only; do not mutate policy or workflow semantics to compensate |
