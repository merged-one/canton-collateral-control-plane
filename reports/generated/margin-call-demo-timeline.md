# Margin Call Demo Timeline

## Execution Phases

| Seq | Scenario | Phase | Status | Artifact | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | positive-margin-call | POLICY_EVALUATION | COMPLETED | `reports/generated/positive-margin-call-policy-evaluation-report.json` | Evaluated candidate inventory for positive scenario with overall decision ACCEPT. |
| 2 | positive-margin-call | OPTIMIZATION | COMPLETED | `reports/generated/positive-margin-call-optimization-report.json` | Optimized collateral for scenario positive-margin-call with recommendation POST_NEW_SET. |
| 3 | positive-margin-call | WORKFLOW | COMPLETED | `reports/generated/positive-margin-call-workflow-result.json` | Recorded the Daml margin-call and posting path for scenario positive-margin-call. |
| 4 | negative-ineligible-asset | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-ineligible-asset-policy-evaluation-report.json` | Evaluated candidate inventory for negative scenario with overall decision REJECT. |
| 5 | negative-insufficient-lendable-value | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-insufficient-lendable-value-policy-evaluation-report.json` | Evaluated candidate inventory for negative scenario with overall decision ACCEPT. |
| 6 | negative-insufficient-lendable-value | OPTIMIZATION | COMPLETED | `reports/generated/negative-insufficient-lendable-value-optimization-report.json` | Optimized collateral for scenario negative-insufficient-lendable-value with recommendation NO_SOLUTION. |
| 7 | negative-expired-policy-window | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-expired-policy-window-policy-evaluation-report.json` | Evaluated candidate inventory for negative scenario with overall decision REJECT. |

## Positive Workflow Steps

| Step | Phase | Actor | State | Detail |
| --- | --- | --- | --- | --- |
| 1 | MARGIN_CALL | secured-party | Draft | secured party created the draft call obligation |
| 2 | MARGIN_CALL | secured-party | UnderEvaluation | secured party started obligation evaluation |
| 3 | MARGIN_CALL | secured-party | Submitted | secured party confirmed the shortfall against the selected policy snapshot |
| 4 | MARGIN_CALL | secured-party | Closed | secured party issued the margin call without additional approval |
| 5 | POSTING | provider | Draft | provider staged eligible collateral inventory for the posting intent |
| 6 | POSTING | provider | Submitted | provider submitted the collateral posting intent |
| 7 | POSTING | provider | UnderEvaluation | provider moved the posting intent into evaluation |
| 8 | POSTING | provider | PendingApproval | provider recorded a feasible posting path |
| 9 | POSTING | secured-party | PendingApproval | secured party approved the posting path |
| 10 | POSTING | custodian | PendingSettlement | custodian approved the posting path and a settlement instruction was created |
| 11 | POSTING | custodian | Closed | custodian confirmed settlement and the encumbrances were committed |
