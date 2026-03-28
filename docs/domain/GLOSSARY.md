# Glossary

| Term | Meaning In This Repository |
| --- | --- |
| Canton Collateral Control Plane | The current user-facing name for the repository and the umbrella architecture that coordinates policy, optimization, workflow orchestration, conformance, and reporting. |
| C-COPE (deprecated) | Historical alias for the former repository name "Canton Collateral Policy & Optimization Engine". Retained only for continuity in older records; new docs should use "Canton Collateral Control Plane" or "the Control Plane". |
| Control plane | The subsystem set that authors policy, evaluates eligibility, computes haircuts and lendable value, manages concentration and release logic, orchestrates workflows, runs conformance checks, and generates reports. |
| Data plane | The asset, ledger, settlement, and runtime surfaces the control plane evaluates or drives, including token-standard-style assets, Daml Finance-style assets, contract state on Canton, DvP rails, and LocalNet execution. |
| Canton | The distributed application platform targeted for confidential, atomic multi-party workflow execution. |
| LocalNet | A local development deployment based on Canton Quickstart or equivalent tooling. |
| CPL | Collateral Policy Language, the versioned machine-readable schema for collateral-policy rules. |
| Collateral policy | Versioned rules governing asset eligibility, haircuting, concentration, control, and release conditions. |
| Eligibility | The determination that an asset may be used under a specific policy and current portfolio state. |
| Haircut | A policy-defined reduction applied to valuation when computing lendable value. |
| Lendable value | The value recognized for collateral coverage after haircuting and policy adjustments. |
| Concentration limit | A policy-defined cap on exposure to a bucket such as issuer, asset class, currency, jurisdiction, or custodian. |
| Encumbrance | The portion of an asset or position committed to satisfy an obligation. |
| Pre-positioning | Operationally preparing eligible collateral inventory in advance so it can be mobilized quickly when needed. |
| Best-to-post | An optimization objective that prefers the most efficient assets to satisfy a collateral obligation under policy constraints. |
| Cheapest-to-deliver | An optimization objective that minimizes delivery cost or opportunity cost subject to policy constraints. |
| Substitution | Replacement of posted collateral with alternate eligible collateral while preserving required coverage. |
| Margin return | Release of excess collateral once coverage and control conditions permit it. |
| Close-out | The transfer, seizure, or unwind workflow that applies after default or a termination event under documented rights. |
| Policy profile | A reusable policy configuration pattern, such as bilateral, tri-party, CCP-style, or central-bank-style. |
| Conformance suite | The scenario runner, tests, and invariant reports used to prove that implemented behavior matches the documented control plane. |
| Execution report | A machine-readable report describing what workflow steps executed, under which policy version, and with what outcome. |
| Evidence | Reproducible artifacts supporting claims about design, implementation, tests, operations, or security. |
| ADR | Architecture Decision Record capturing a durable design or operating decision. |
