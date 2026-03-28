# Threat Model

## Scope

The future system will manage confidential collateral policy, inventory, valuation, workflow, and reporting state across multiple parties. This document records the threat posture implied by the architecture package and the design areas that must remain visible as implementation begins.

The current repository state now includes an initial off-ledger policy evaluation engine, an initial off-ledger optimizer, initial Daml workflow templates for obligations, posting, substitution, return, settlement intent, and execution reporting, a first end-to-end margin-call demo runner plus execution-report contract, and a pinned Quickstart bootstrap and compose-preflight layer. Those surfaces make privacy, determinism, and authority boundaries concrete, but they are still a skeleton layer rather than a full disclosure-profile, replay-hardening, or adapter-integrated implementation.

## Protected Assets

- confidential policy and position data
- policy version and effective-window data
- inventory-lot and custody-account facts
- authorization decisions and role assignments
- valuation inputs and haircut parameters
- policy evaluation reports and machine-readable failure reasons
- optimization reports, substitution deltas, and explanation traces
- margin-call demo manifests and workflow-input payloads
- encumbrance state
- settlement instructions and control acknowledgments
- execution reports and audit evidence
- pinned Quickstart overlay configuration and upstream commit metadata

## Threat Actors

- unauthorized internal user
- authorized user exceeding their role
- compromised integration endpoint
- compromised adjacent service
- operator error during substitution or release
- external observer attempting to infer confidential state

## Core Threats

| Threat | Why It Matters | Initial Control Direction |
| --- | --- | --- |
| Broken authorization or role separation | Users could approve or release collateral outside policy. | Explicit role model, auditable authorization checks, contract-specific controllers, and invariant tracking. |
| Confidentiality leakage | Sensitive counterparty or position information could escape intended visibility. | Privacy-preserving workflow boundaries, explicit observer lists, and minimal reporting disclosure. |
| Over-broad contract visibility | Parties could see obligations, inventory, or settlement data unrelated to their role. | Narrow signatory and observer sets, separate request and settlement templates, role-specific report profiles. |
| Replay or duplicate execution | Repeated events could create duplicate pledges or releases. | Idempotent command design and replay-focused tests. |
| Optimizer or reporter treated as authority | Off-ledger services could become hidden sources of truth. | Keep workflow state authoritative on Canton and derive reports from committed state only. |
| Hidden optimizer objective drift or non-deterministic tie handling | Similar requests could yield different substitutions or recommendations that operators cannot defend. | Publish the objective in ADRs and report contracts, keep search order deterministic, and retain explanation traces plus no-churn handling for equal economics. |
| Non-atomic substitution or return | Coverage could be lost during workflow transitions. | Treat atomic workflow completion as a blocking invariant. |
| Report tampering or drift | Operators could rely on incorrect evidence. | State-derived report generation, schema validation, and report-fidelity checks. |
| Scenario-manifest drift | The operator demo could silently stop representing the documented margin-call shape. | Keep scenario inputs versioned in-repo, validate expected outcomes inside the orchestration layer, and fail closed when they drift. |
| Policy-evaluation report over-disclosure | Off-ledger reports could leak more inventory or counterparty detail than a consumer needs. | Keep report schemas explicit, add role-scoped disclosure profiles later, and avoid hidden joins to external reference data. |
| Optimization-report over-disclosure | Advisory optimization output could reveal more inventory detail or operational preference than a consumer needs. | Keep the optimization report schema explicit, defer role-scoped report profiles, and preserve workflow authority boundaries. |
| Schema downgrade or undeclared extension | Consumers could derive different results from materially different policy documents. | Pin `cplVersion`, reject unknown fields, and validate policy documents before load. |
| Tool-download tampering or drift | A compromised or drifting bootstrap source could change local behavior invisibly. | Pin download URLs and SHA-256 checksums and install runtime tools repo-locally. |
| Runtime overlay drift | Demo or LocalNet shortcuts could alter behavior relative to the documented architecture. | Separate runtime concerns from business semantics and keep overlay changes explicit. |
| Quickstart runtime-version skew | Operators could treat the pinned LocalNet foundation as deployable even when the repo DAR is not yet compatible with the pinned Quickstart runtime line. | Record the version gap explicitly, stop automation at compose validation, and gate package deployment behind a separate bridge decision. |
| Environment drift | The system could become impossible to reproduce or validate consistently. | Pinned dependencies, checksum-verified bootstrap commands, and release evidence. |

## Trust Boundaries

- policy authoring and registry versus workflow execution
- policy evaluation versus optimization proposal generation
- published CPL schema versus runtime policy ingestion
- optimization proposal generation versus settlement authority
- workflow request contracts versus settlement instructions versus execution-report contracts
- confidential ledger state versus report-generation views
- LocalNet overlay and adjacent services versus upstream Quickstart base
- business roles versus demo and runtime operators

## Open Questions

- which Quickstart topology extensions can be expressed purely through overlays?
- what minimum report profiles satisfy auditability without over-disclosure?
- what freshness and provenance guarantees must a valuation snapshot prove?
- which asset-control semantics belong in the adapter layer versus the workflow package?
- which Daml runtime bridge will let the repo DAR be deployed into the pinned Quickstart LocalNet without losing reproducibility?
- when should future workflow-coupled optimization respect operational churn budgets or consent costs in addition to the current deterministic economic proxy objective?
- how should the current workflow-party execution reports be transformed into narrower operator, auditor, or external-integration views?
- how should future consumers reject or negotiate policies that require a newer `cplVersion` than they support?
