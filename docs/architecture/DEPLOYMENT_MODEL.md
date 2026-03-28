# Deployment Model

## Target Prototype Shape

The prototype is intended to run on a Quickstart-based LocalNet with C-COPE components added through overlays and adjacent services. The control plane should remain deployable without forking upstream Quickstart internals unless an extension point is missing and an ADR explicitly authorizes the fork.

## Deployment Units

| Deployment Unit | Role In The Prototype | Preferred Placement |
| --- | --- | --- |
| Quickstart domain, sequencer, and mediator services | provide the base Canton network for local development and scenario execution | upstream Quickstart base |
| participant for pledgor roles | hosts parties that own eligible inventory and initiate posting, substitution, and return requests | LocalNet overlay |
| participant for secured-party roles | hosts parties that issue calls, approve substitutions, and receive collateral control rights | LocalNet overlay |
| participant for custodian or control roles | hosts parties that acknowledge control, delivery, release, and return instructions | LocalNet overlay |
| C-COPE Daml package | defines obligation, encumbrance, approval, and settlement contracts | deployed on LocalNet participants |
| policy registry service | publishes and serves policy packages outside the ledger | adjacent service |
| reference data and valuation service | creates immutable valuation snapshots from market and static data | adjacent service |
| optimization service | ranks feasible candidate lots using policy-constrained inputs | adjacent service |
| reporting and evidence service | derives execution reports from committed workflow state and referenced snapshots | adjacent service |
| integration gateway | presents stable APIs to external apps and local test harnesses | adjacent service |

## State Placement

| State Type | Preferred Location | Reason |
| --- | --- | --- |
| obligations, encumbrances, approvals, settlement state | Canton ledger | authoritative multi-party workflow state belongs on the ledger |
| policy packages and schedule history | policy registry | versioned policy management should stay independent of workflow deployment |
| valuation snapshots | snapshot store | snapshots must be immutable and re-usable across reports |
| optimization proposals | optimizer or workflow reference store | proposals are advisory and may be regenerated |
| execution reports and prompt evidence | reporting store and repository docs | reports are derived outputs that need durable traceability |
| LocalNet bootstrap config | overlay files in the repo | runtime concerns must stay separate from domain logic |

## Environment Layers

### Documentation layer

- repository ADRs, architecture docs, invariants, and evidence records
- pinned bootstrap, Daml scaffold, and verification commands for the runtime foundation
- no executable collateral business logic in this phase

### LocalNet development layer

- upstream Quickstart bundle
- overlay participants, parties, and package deployment
- adjacent services running with local configuration

### Shared demo layer

- the same logical separation as LocalNet development
- reproducible bootstrap and scenario commands
- no demo-only semantics or hard-coded success data

### Future pilot layer

- separate organizations or participants per institution
- stronger secret management and environment isolation
- the same policy, workflow, reporting, and evidence contracts

## Operational Principles

- keep upstream Quickstart artifacts vendored or referenced as-is where possible
- express repo-specific topology through overlays, not edits to upstream defaults
- deploy C-COPE services beside Canton, not inside Canton internals
- treat observability as a runtime concern; it must not become a hidden source of truth
- isolate demo bootstrap data from production-intended schema or contract design

## Upgrade And Change Rules

1. Pin the Quickstart version before implementation work starts.
2. Pin Daml package and service versions per release.
3. Change the LocalNet topology through overlay files or deployment manifests first.
4. Fork upstream Quickstart only when an overlay cannot express the needed extension, and record that decision in an ADR.
5. Keep rollback possible by versioning policy packages, Daml packages, and overlay configuration independently.
