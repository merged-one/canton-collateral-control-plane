# Margin Call Demo Timeline

## Execution Phases

| Seq | Scenario | Phase | Status | Artifact | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | positive-margin-call-quickstart | POLICY_EVALUATION | COMPLETED | `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json` | Evaluated candidate inventory for positive scenario with overall decision ACCEPT. |
| 2 | positive-margin-call-quickstart | OPTIMIZATION | COMPLETED | `reports/generated/positive-margin-call-quickstart-optimization-report.json` | Optimized collateral for scenario positive-margin-call-quickstart with recommendation POST_NEW_SET. |
| 3 | positive-margin-call-quickstart | QUICKSTART_SEED | COMPLETED | `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json` | Seeded or reused the declared Quickstart scenario for positive-margin-call-quickstart before workflow execution. |
| 4 | positive-margin-call-quickstart | WORKFLOW | COMPLETED | `reports/generated/positive-margin-call-quickstart-workflow-result.json` | Advanced the Quickstart margin-call workflow for scenario positive-margin-call-quickstart through gate PREPARE_FOR_ADAPTER. |
| 5 | positive-margin-call-quickstart | ADAPTER | COMPLETED | `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json` | Executed the reference token adapter for scenario positive-margin-call-quickstart and confirmed workflow settlement on Quickstart. |
| 6 | negative-ineligible-asset-quickstart | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-ineligible-asset-quickstart-policy-evaluation-report.json` | Evaluated candidate inventory for negative scenario with overall decision REJECT. |
| 7 | negative-workflow-rejected-quickstart | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-workflow-rejected-quickstart-policy-evaluation-report.json` | Evaluated candidate inventory for negative scenario with overall decision ACCEPT. |
| 8 | negative-workflow-rejected-quickstart | OPTIMIZATION | COMPLETED | `reports/generated/negative-workflow-rejected-quickstart-optimization-report.json` | Optimized collateral for scenario negative-workflow-rejected-quickstart with recommendation POST_NEW_SET. |
| 9 | negative-workflow-rejected-quickstart | QUICKSTART_SEED | COMPLETED | `reports/generated/negative-workflow-rejected-quickstart/localnet-control-plane-seed-receipt.json` | Seeded or reused the declared Quickstart scenario for negative-workflow-rejected-quickstart before workflow execution. |
| 10 | negative-workflow-rejected-quickstart | WORKFLOW | COMPLETED | `reports/generated/negative-workflow-rejected-quickstart-workflow-result.json` | Advanced the Quickstart margin-call workflow for scenario negative-workflow-rejected-quickstart through gate REJECT_BY_SECURED_PARTY. |
| 11 | negative-workflow-rejected-quickstart | ADAPTER | SKIPPED | `reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json` | Did not invoke the adapter for scenario negative-workflow-rejected-quickstart because the workflow ended in posting state Rejected. |

## Positive Workflow Steps

| Step | Phase | Actor | State | Detail |
| --- | --- | --- | --- | --- |
| 1 | MARGIN_CALL | secured-party | Closed | secured party issued the seeded Quickstart margin call without additional approval |
| 2 | POSTING | provider | UnderEvaluation | provider started posting evaluation on Quickstart |
| 3 | POSTING | provider | PendingApproval | provider recorded a feasible posting path on Quickstart |
| 4 | POSTING | secured-party | PendingApproval | secured party approved the Quickstart posting path |
| 5 | POSTING | custodian | PendingSettlement | custodian approved the Quickstart posting path and exposed the settlement instruction |
