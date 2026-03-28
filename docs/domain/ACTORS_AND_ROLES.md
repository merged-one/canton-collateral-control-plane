# Actors And Roles

## Primary Roles

| Role | Primary Responsibility | Can Initiate | Must Approve | Cannot Unilaterally Do |
| --- | --- | --- | --- | --- |
| `Pledgor` or `CollateralProvider` | provide eligible inventory and satisfy obligations | posting requests, substitution requests, return requests | approvals only where the provider's consent is required | declare collateral released without workflow commitment |
| `SecuredParty` | hold exposure, issue calls, and control release rights | margin call issuance, approval or rejection of substitution or return | approval when release or substitution rights require it | inspect unrelated provider inventory or rewrite policy schedules |
| `Custodian` or `ControlRole` | acknowledge control, settlement, release, and return execution | settlement acknowledgments, control confirmations, exception escalation | approval when control transfer is a policy condition | alter obligations, valuations, or optimizer objectives |
| `PolicyAdministrator` | author, validate, and publish policy packages | policy publication and retirement | policy approvals according to governance | settle collateral or override workflow state |
| `ValuationOperator` | publish trusted valuation snapshots and reference-data normalization results | snapshot creation | none unless policy requires a valuation attestation | approve substitution or release solely by controlling prices |
| `OptimizationOperator` | run deterministic candidate ranking under configured objectives | optimization requests | none | mark ineligible collateral as feasible or commit encumbrance |
| `WorkflowOrchestrator` | submit Daml choices and correlate multi-step workflow progress | workflow commands on behalf of authorized parties | none as a business approver | impersonate approval roles or author policy |
| `ReportingOperator` | generate execution reports and audit packages | report generation requests | none | invent committed events or repair missing state by guesswork |
| `Auditor` | review attributable evidence and invariant coverage | evidence review | none | alter workflow, policy, or runtime state |
| `DemoOrRuntimeOperator` | deploy and monitor the LocalNet and adjacent services | bootstrap, health checks, shutdown, upgrades | environment changes only | override business approvals or gain default visibility into confidential workflow state |
| `ExternalIntegratingApplication` | submit scoped requests and consume scoped reports | API requests defined by the gateway | none | assume direct access to internal contracts or hidden topology details |

## Separation Of Duties

- policy administration is separate from policy consumption
- optimization is separate from settlement authority
- workflow orchestration is separate from business approval
- reporting is separate from execution authority
- demo and runtime operations are separate from confidential business roles

## Approval Expectations By Workflow

| Workflow | Required Roles |
| --- | --- |
| margin call issuance | secured party or delegated call manager |
| collateral posting | provider initiation plus any secured-party or custodian approvals required by policy |
| substitution request | provider initiation, secured-party approval when rights require it, custodian approval when control changes are required |
| return request | provider or secured-party initiation depending on the release reason, plus all policy-required release approvers |
| release and return settlement | custodian or control role acknowledgment when collateral movement or release occurs |
| exception handling | operational owner plus the roles needed to remediate the failed path |

## Role-Specific Constraints

- A `PolicyAdministrator` may publish a schedule but may not back-date workflow outcomes by changing policy history.
- An `OptimizationOperator` may propose an alternate lot set but may not turn a rejected policy decision into an approved one.
- A `Custodian` sees the data needed to execute or reject a settlement instruction, not the full economic rationale unless the workflow requires it.
- A `ReportingOperator` may emit multiple disclosure profiles of the same execution report, but all must derive from the same committed source state.
- A `DemoOrRuntimeOperator` may restart services or redeploy overlays, but must not become a hidden business super-user.
