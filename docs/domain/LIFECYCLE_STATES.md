# Lifecycle States

## Shared State Vocabulary

| State | Meaning |
| --- | --- |
| `Draft` | created but not yet submitted into a workflow |
| `Submitted` | formally requested and awaiting evaluation or routing |
| `UnderEvaluation` | policy and data checks are running against explicit inputs |
| `PendingApproval` | all hard checks passed, but required role approvals are outstanding |
| `Approved` | required approvals are present and the workflow may proceed to settlement |
| `Rejected` | the request failed due to policy, authorization, or business rejection |
| `PendingSettlement` | settlement or control movement has been instructed but not yet confirmed |
| `Settled` | the instructed movement or control change has committed successfully |
| `ExceptionOpen` | a failure or mismatch requires remediation before closure |
| `Expired` | the allowed time window ended before successful completion |
| `Closed` | the workflow reached its terminal state with an attributable outcome |

## Workflow 1: Margin Call Issuance

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `Draft` | `UnderEvaluation` | secured party requests call calculation | policy version and snapshot inputs are present |
| `UnderEvaluation` | `Submitted` | shortfall is confirmed | decision report identifies required coverage |
| `Submitted` | `PendingApproval` | internal review or call governance requires approval | approval policy applies |
| `Submitted` | `Closed` | no extra approval is required and call is issued immediately | attributable issuer identity is present |
| `PendingApproval` | `Closed` | required issuer approval is recorded | obligation is committed on Canton |
| `Submitted` or `PendingApproval` | `Expired` | due or issuance window passes without valid issue | expiry timestamp reached |

## Workflow 2: Collateral Posting

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `Draft` | `Submitted` | provider nominates lots or requests optimizer assistance | target obligation exists |
| `Submitted` | `UnderEvaluation` | policy checks start | policy version, snapshot, and lot facts are pinned |
| `UnderEvaluation` | `PendingApproval` | lots are feasible and approval is required | hard policy checks pass |
| `UnderEvaluation` | `PendingSettlement` | lots are feasible and no extra approval is required | hard policy checks pass |
| `PendingApproval` | `PendingSettlement` | all required approvals are recorded | control rights satisfied |
| `PendingSettlement` | `Settled` | settlement and encumbrance commit atomically | Daml workflow and settlement instruction succeed |
| `Settled` | `Closed` | posting execution report is emitted | committed state is reported |
| any non-terminal state | `Rejected` | infeasibility or unauthorized action is detected | explicit rejection reason recorded |
| `PendingSettlement` | `ExceptionOpen` | settlement fails after approval | remediation path required |

## Workflow 3: Substitution Request

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `Draft` | `Submitted` | provider requests replacement of posted collateral | referenced lots are currently encumbered |
| `Submitted` | `UnderEvaluation` | replacement feasibility checks start | proposed replacement set is explicit |
| `UnderEvaluation` | `PendingApproval` | replacement is feasible but approvals are required | coverage remains intact after substitution |
| `UnderEvaluation` | `PendingSettlement` | replacement is feasible and approval set is already satisfied | control conditions met |
| `PendingApproval` | `Approved` | secured party and custodian approvals are complete | all required roles have acted |
| `Approved` | `PendingSettlement` | orchestrator submits atomic swap choices | workflow correlation ID assigned |
| `PendingSettlement` | `Settled` | old encumbrance is released only as new encumbrance commits | atomic workflow succeeds |
| `Settled` | `Closed` | substitution execution report is emitted | report fidelity check passes |
| any non-terminal state | `Rejected` | replacement is ineligible, unauthorized, or concentration-breaching | explicit decision trace exists |
| any non-terminal state | `Expired` | approval or settlement window closes | expiry timestamp reached |

## Workflow 4: Substitution Approval

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `PendingApproval` | `Approved` | all required approval records are present | each approval is attributable to the correct role |
| `PendingApproval` | `Rejected` | an approver rejects the request | rejection rationale recorded |
| `PendingApproval` | `Expired` | approval deadline passes | no implicit approval |

## Workflow 5: Return Request

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `Draft` | `Submitted` | provider or secured party requests a release | obligation and requested lots are referenced |
| `Submitted` | `UnderEvaluation` | post-return coverage is tested | policy version and snapshot are current |
| `UnderEvaluation` | `PendingApproval` | return is feasible and release approvals are required | post-return state remains compliant |
| `UnderEvaluation` | `PendingSettlement` | return is feasible and no additional approval is required | control conditions already satisfied |
| `PendingApproval` | `Approved` | required release approvals are present | rights and deadlines satisfied |
| `Approved` | `PendingSettlement` | workflow submits release and return instructions | correlation ID assigned |
| `PendingSettlement` | `Settled` | release and return commit successfully | settlement succeeds |
| `Settled` | `Closed` | return execution report is emitted | report derived from committed state |
| any non-terminal state | `Rejected` | return would break coverage or violate control rights | explicit rejection reason recorded |
| any non-terminal state | `Expired` | release window closes | collateral remains encumbered |

## Workflow 6: Release And Return Settlement

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| `Approved` | `PendingSettlement` | release and movement instructions are sent | all authorizations are present |
| `PendingSettlement` | `Settled` | custodian confirms release or movement | instruction status is successful |
| `PendingSettlement` | `ExceptionOpen` | custodian rejects or times out | original encumbrance remains authoritative until remediated |
| `Settled` | `Closed` | final report and reconciliation complete | committed state and report agree |

## Workflow 7: Exception Path

| From | To | Trigger | Guard |
| --- | --- | --- | --- |
| any active state | `ExceptionOpen` | settlement failure, stale data, conflicting encumbrance, or mismatched approval | explicit exception record created |
| `ExceptionOpen` | `UnderEvaluation` | remediation requires fresh feasibility checks | updated snapshot or request data provided |
| `ExceptionOpen` | `Rejected` | remediation proves impossible | attributable failure reason recorded |
| `ExceptionOpen` | `Closed` | compensating workflow or manual resolution commits | outcome documented in execution report |

## Workflow 8: Expiry Path

| Artifact | Non-Terminal States Subject To Expiry | Expiry Outcome |
| --- | --- | --- |
| `CallObligation` | `Submitted`, `PendingApproval` | move to `Expired` with explicit uncovered amount |
| `SubstitutionRequest` | `Submitted`, `UnderEvaluation`, `PendingApproval`, `Approved`, `PendingSettlement` | move to `Expired`; existing collateral stays in force |
| `ReturnRequest` | `Submitted`, `UnderEvaluation`, `PendingApproval`, `Approved`, `PendingSettlement` | move to `Expired`; no release occurs |
| `SettlementInstruction` | `PendingSettlement` | move to `ExceptionOpen` or terminal failure depending on workflow policy |

## Lifecycle Guarantees

- no release or substitution takes effect without a committed workflow transition
- expiry never implies silent approval or implicit settlement
- exception handling must preserve attributable state rather than resetting history
- terminal reports are produced only after the terminal state is committed
