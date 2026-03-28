# Integration Surfaces

This document identifies the major system boundaries the Canton Collateral Control Plane is expected to expose or depend on. All surfaces are planned; none are implemented yet.

## Planned Surfaces

| Surface | Purpose | Notes |
| --- | --- | --- |
| Canton Quickstart LocalNet | Host confidential multi-party workflow execution. | Version and topology to be pinned in a future ADR. |
| Token-standard-style asset adapter | Represent collateral assets, control state, and encumbrance state in a reusable way. | Must support deterministic eligibility and control semantics. |
| Daml Finance-style asset adapter | Provide a second reference integration path for existing Canton-oriented asset models. | Exact scope remains to be pinned after dependency review. |
| CPL input surface | Accept versioned eligibility, haircut, concentration, wrong-way-risk, control, substitution-right, and settlement-window rules. | Must be portable across multiple workflow types. |
| Reference data inputs | Provide valuation, FX, custodian, jurisdiction, and static reference data. | Must be versioned, attributable, and auditable. |
| Optimization boundary | Produce best-to-post, cheapest-to-deliver, substitution, and concentration-aware allocation decisions. | Must remain separate from policy authoring and workflow settlement. |
| Workflow library boundary | Execute margin call, substitution, return, delivery, and close-out flows atomically. | Must preserve confidentiality, authorization, and replay safety. |
| Consumer application boundary | Allow financing apps, derivatives apps, tokenized-asset platforms, stablecoin rails, and custodial workflows to call into the control plane. | The Control Plane should be reusable infrastructure, not a single venue app. |
| Report and scenario-runner surface | Emit machine-readable decision and execution reports and drive conformance scenarios. | Must satisfy report-fidelity and exception-path invariants. |

## Mapping To Established Practice

- Central-bank style collateral frameworks motivate the split between policy, valuation, control, and settlement.
- Tri-party workflows motivate explicit selection, substitution, pre-positioning, and operational coordination boundaries.
- CCP-style control motivates concentration-sensitive policy evaluation and conservative haircut application.

## Near-Term Follow-Up

- pin the LocalNet distribution
- wire CPL evaluation to the published schema and policy-profile examples
- define the first decision-report and execution-report contracts
- define the initial asset-adapter contracts
