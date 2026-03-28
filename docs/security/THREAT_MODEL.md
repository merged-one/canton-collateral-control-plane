# Threat Model

## Scope

The future system will manage confidential collateral policy, inventory, valuation, workflow, and reporting state across multiple parties. This document records the threat posture implied by the architecture package and the design areas that must remain visible as implementation begins.

## Protected Assets

- confidential policy and position data
- policy version and effective-window data
- inventory-lot and custody-account facts
- authorization decisions and role assignments
- valuation inputs and haircut parameters
- encumbrance state
- settlement instructions and control acknowledgments
- execution reports and audit evidence

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
| Broken authorization or role separation | Users could approve or release collateral outside policy. | Explicit role model, auditable authorization checks, invariant tracking. |
| Confidentiality leakage | Sensitive counterparty or position information could escape intended visibility. | Privacy-preserving workflow boundaries and minimal reporting disclosure. |
| Over-broad contract visibility | Parties could see obligations, inventory, or settlement data unrelated to their role. | Narrow signatory and observer sets, separate templates, role-specific report profiles. |
| Replay or duplicate execution | Repeated events could create duplicate pledges or releases. | Idempotent command design and replay-focused tests. |
| Optimizer or reporter treated as authority | Off-ledger services could become hidden sources of truth. | Keep workflow state authoritative on Canton and derive reports from committed state only. |
| Non-atomic substitution or return | Coverage could be lost during workflow transitions. | Treat atomic workflow completion as a blocking invariant. |
| Report tampering or drift | Operators could rely on incorrect evidence. | State-derived report generation and report-fidelity checks. |
| Schema downgrade or undeclared extension | Consumers could derive different results from materially different policy documents. | Pin `cplVersion`, reject unknown fields, and validate policy documents before load. |
| Runtime overlay drift | Demo or LocalNet shortcuts could alter behavior relative to the documented architecture. | Separate runtime concerns from business semantics and keep overlay changes explicit. |
| Environment drift | The system could become impossible to reproduce or validate consistently. | Pinned dependencies, explicit bootstrap commands, and release evidence. |

## Trust Boundaries

- policy authoring and registry versus workflow execution
- policy evaluation versus optimization proposal generation
- published CPL schema versus runtime policy ingestion
- optimization proposal generation versus settlement authority
- confidential ledger state versus report-generation views
- LocalNet overlay and adjacent services versus upstream Quickstart base
- business roles versus demo and runtime operators

## Open Questions

- which Quickstart topology extensions can be expressed purely through overlays?
- what minimum report profiles satisfy auditability without over-disclosure?
- what freshness and provenance guarantees must a valuation snapshot prove?
- which asset-control semantics belong in the adapter layer versus the workflow package?
- how should future consumers reject or negotiate policies that require a newer `cplVersion` than they support?
