# Data Flow

## Common Inputs

Every workflow in the Control Plane is anchored to the same control inputs, while the data plane supplies the relevant holdings, committed contract state, and settlement execution surfaces:

- a versioned `PolicyPackage`
- an immutable `ValuationSnapshot`
- current `CollateralInventoryLot` and `EncumbranceState` facts
- explicit actor approvals and control rights
- a correlation identifier that ties decision outputs to committed workflow state

## Flow 1: Policy Publication

| Step | Actor Or Component | Output |
| --- | --- | --- |
| 1 | policy administrator authors or amends a policy profile | draft policy package |
| 2 | policy registry validates schedule completeness and version metadata | validated package candidate |
| 3 | authorized approver publishes the package | effective `PolicyPackage` and schedule IDs |
| 4 | reporter records the publication event | evidence link for later workflow traceability |

## Flow 2: Margin Call Issuance

| Step | Actor Or Component | Output |
| --- | --- | --- |
| 1 | secured party or call manager requests coverage calculation | evaluation request |
| 2 | reference data adapter freezes prices, FX, and inventory facts | `ValuationSnapshot` |
| 3 | policy evaluation engine computes required coverage and shortfall status | `PolicyDecisionReport` |
| 4 | workflow orchestrator creates a `CallObligation` on Canton | committed obligation state |
| 5 | reporting service emits issuance evidence tied to the obligation and snapshot IDs | `ExecutionReport` |

## Flow 3: Collateral Posting

| Step | Actor Or Component | Output |
| --- | --- | --- |
| 1 | pledgor or operator selects candidate inventory or requests optimization | posting request |
| 2 | policy evaluation engine checks each candidate lot for eligibility, haircut, and concentration impact | feasible candidate set |
| 3 | optimization engine ranks the feasible set if optimization is enabled | `OptimizationProposal` |
| 4 | workflow orchestrator submits Daml choices to reserve and pledge the selected lots | committed encumbrance state |
| 5 | workflow package creates `SettlementInstruction` records for control or delivery actions | settlement instructions |
| 6 | reporting service derives the posting execution report from committed events | `ExecutionReport` |

## Flow 4: Substitution Request And Approval

| Step | Actor Or Component | Output |
| --- | --- | --- |
| 1 | pledgor submits a `SubstitutionRequest` naming lots to release and proposed replacements | submitted request |
| 2 | policy evaluation engine re-checks replacement feasibility against current exposure and concentration headroom | substitution decision report |
| 3 | optimization engine may propose a better replacement set within the same policy boundary | ranked alternatives |
| 4 | secured party and custodian control role review the request | approval or rejection record |
| 5 | workflow package atomically releases replaced encumbrances and applies new ones | updated encumbrance and settlement state |
| 6 | reporting service emits a substitution execution report | `ExecutionReport` |

## Flow 5: Return Request And Release Settlement

| Step | Actor Or Component | Output |
| --- | --- | --- |
| 1 | pledgor or secured party identifies excess coverage and creates a `ReturnRequest` | submitted request |
| 2 | policy evaluation engine confirms post-return coverage and control conditions | return decision report |
| 3 | approval roles authorize the release if required by policy | approval record |
| 4 | workflow package moves the affected lots from pledged to pending-release and then to released | committed release state |
| 5 | settlement instructions direct the custodian or asset adapter to return control | `SettlementInstruction` |
| 6 | reporting service emits the release-and-return execution report | `ExecutionReport` |

## Flow 6: Exception Path

| Trigger | Workflow Handling | Report Requirement |
| --- | --- | --- |
| ineligible collateral | reject posting or substitution before encumbrance changes commit | include explicit rule failure and affected lot IDs |
| concentration breach | hold request in exception or reject it depending on policy | include breached bucket, threshold, and attempted state |
| missing approval | keep workflow pending or expired; never auto-approve | include missing role and deadline state |
| settlement failure | keep original encumbrance authoritative until a compensating path is committed | include settlement leg status and remediation state |
| stale snapshot or policy version mismatch | fail fast and require re-evaluation | include the stale reference identifiers |

## Flow 7: Expiry Path

| Artifact | Expiry Condition | Required Outcome |
| --- | --- | --- |
| `CallObligation` | due time passes before sufficient coverage is committed | obligation moves to expired or exception state with explicit shortfall record |
| `SubstitutionRequest` | approvals or settlement do not complete before expiry window | request expires without implicit release of existing collateral |
| `ReturnRequest` | approval or settlement window closes | request expires and collateral remains encumbered until a new authorized request is submitted |
| `SettlementInstruction` | external settlement deadline passes | workflow remains in exception until reconciled or canceled by explicit action |

## Data Lineage Rules

- Every execution flow must reference the exact policy version used.
- Every eligibility or haircut decision must reference a valuation snapshot identifier.
- Every optimization proposal must carry the policy decision report identifier it depends on.
- Every execution report must reference the committed workflow objects, not just the submitted request.
- Every exception or expiry outcome must be reported explicitly; silent timeouts are not valid behavior.
