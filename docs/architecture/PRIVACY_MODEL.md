# Privacy Model

## Privacy Objective

The control plane must let multiple parties coordinate collateral workflows without exposing unnecessary inventory, policy, or optimization details. Canton is used because workflow state can be shared only with the parties that need it, while still supporting atomic multi-party execution.

## Data Classes

| Data Class | Examples | Default Visibility |
| --- | --- | --- |
| policy definitions | eligibility schedules, haircut schedules, concentration rules, release conditions | policy administrators and authorized services |
| valuation inputs | price source, FX rate, issuer attributes, as-of time | evaluation service, authorized reporters, parties entitled to the resulting decision |
| inventory facts | lot identifiers, custody account, quantity, settlement constraints | owning pledgor, authorized custodian role, evaluation and optimization services within scope |
| workflow state | call obligations, approvals, encumbrance records, settlement instructions | only workflow parties that are signatories or explicit observers |
| optimization rationale | ranking scores, objective settings, rejected alternatives | authorized operators and parties entitled to the proposal |
| execution reports | committed outcomes, referenced inputs, exception status | authorized operators, auditors, and workflow participants according to report profile |

## Role Visibility Matrix

| Role | Must Be Able To See | Must Not Be Able To See |
| --- | --- | --- |
| pledgor or collateral provider | its own lots, its own obligations, its own substitution and return requests, settlement instructions that affect its collateral | unrelated counterparties' inventory, unrelated obligations, other parties' optimization candidates |
| secured party | obligations owed to it, posted collateral covering those obligations, approval and release events affecting its control rights | provider inventory not relevant to its obligations, other secured parties' exposures |
| custodian or control role | settlement instructions, control-account details, approval state required to move or release collateral | unrelated pricing inputs, unrelated bilateral exposure data, optimizer cost models not needed for settlement |
| policy administrator | policy packages, profile templates, publication approvals, validation results | runtime positions or bilateral exposure unless separately authorized |
| valuation or reference-data operator | asset facts and market inputs required to create snapshots | workflow details not required for valuation production |
| optimization operator | scoped inventory facts, policy-feasible candidates, objective settings, concentration bucket state | unrelated counterparty positions, policy packages outside assigned scope |
| reporting operator or auditor | committed workflow state and referenced inputs needed for an approved report profile | hidden inventory or valuation fields outside the approved report scope |
| demo or runtime operator | service health, deployment status, redacted logs, bootstrap configuration | raw confidential workflow payloads unless also acting under an authorized business role |
| external integrating application | only the requests, responses, and reports explicitly delegated to that app | internal ledger topology, unrelated contracts, hidden optimization traces |

## Canton Mapping

### Contract visibility

- Daml contracts are visible only to their signatories and explicit observers.
- C-COPE should use narrow observer sets instead of broad shared contracts.
- Separate templates should be used when different roles need different subsets of information.

### Party and participant boundaries

- each institution-facing role should map to a distinct Canton party
- participants host only the parties they are allowed to act for
- LocalNet may co-host multiple parties for convenience, but document-level authority must still assume role separation

### Workflow patterns

- `CallObligation` contracts should be visible to the secured party and the relevant pledgor, with custodian visibility added only when control or settlement action is required
- `SettlementInstruction` contracts should expose only the fields needed to execute the movement or control action
- `ExecutionReport` generation should read committed state and publish role-specific report views instead of one global report object containing every field

### Avoided anti-patterns

- no global inventory ledger visible to all counterparties
- no report generation that depends on ad hoc privileged database joins unavailable to the parties named in the report
- no optimizer service that can inspect all inventory across institutions by default
- no demo operator access path that bypasses party-level visibility rules

## Report Disclosure Profiles

| Report Profile | Intended Audience | Allowed Content |
| --- | --- | --- |
| participant execution report | pledgor, secured party, custodian | workflow objects relevant to that transaction, referenced policy version, snapshot ID, settlement status |
| operator report | internal authorized operator | correlation IDs, processing timestamps, exception states, service version metadata |
| audit report | authorized reviewer | signed or attributable record of inputs, approvals, outcomes, and invariant coverage |
| external integration report | downstream application | minimal data needed to reconcile an API request with the resulting workflow outcome |

## Privacy Invariants

- a role sees only the contracts and report fields required for its responsibility
- workflow reports are derived from visible and authorized state, not from a shadow data lake
- optimization traces are shared only within the scope that produced them
- control and settlement roles see operational instructions without inheriting unrelated economic detail
