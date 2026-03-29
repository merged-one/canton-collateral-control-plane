# Margin Call Demo Summary

## Overview

- Execution report: `reports/generated/margin-call-quickstart-execution-report.json`
- Runtime mode: `QUICKSTART`
- Scenario count: `3`
- Primary policy evaluation artifact: `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`

## Scenario Results

| Scenario | Mode | Result | Summary |
| --- | --- | --- | --- |
| positive-margin-call-quickstart | POSITIVE | SUCCESS | Policy accepted the candidate set, the optimizer recommended POST_NEW_SET, the Quickstart workflow issued the call and prepared a settlement instruction, and the reference token adapter settled lots quickstart-demo-lot-101, quickstart-demo-lot-102, quickstart-demo-lot-103, quickstart-demo-lot-104. |
| negative-ineligible-asset-quickstart | NEGATIVE | EXPECTED_FAILURE | Policy evaluation blocked the scenario with decision REJECT and reason codes ASSET_CLASS_NOT_ELIGIBLE, HAIRCUT_RULE_NOT_FOUND, ISSUER_NOT_ON_ALLOW_LIST, ISSUER_RATING_BELOW_MINIMUM, ISSUER_TYPE_NOT_ALLOWED, ISSUE_TYPE_NOT_ELIGIBLE. |
| negative-workflow-rejected-quickstart | NEGATIVE | EXPECTED_FAILURE | Policy and optimization stayed admissible, but the Quickstart workflow blocked the path in posting state Rejected and the adapter surface remained at 0 receipts. |

## Invariant Checks

| Invariant | Status | Evidence | Note |
| --- | --- | --- | --- |
| PDR-001 | PASS | `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json` | The positive Quickstart path policy report was generated from declared policy and inventory inputs. |
| ALLOC-001 | PASS | `reports/generated/positive-margin-call-quickstart-optimization-report.json` | The optimizer produced a deterministic selected-lot recommendation that matched the declared Quickstart seed scenario. |
| WF-001 | PASS | `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`, `reports/generated/positive-margin-call-quickstart-workflow-result.json`, `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json` | The Quickstart-backed workflow issued the call, prepared the settlement instruction, and then closed the posting path only through Canton workflow confirmation. |
| ADAPT-001 | PASS | `reports/generated/positive-margin-call-quickstart-workflow-result.json`, `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`, `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json` | The reference token adapter consumed the Quickstart workflow handoff artifact, executed the asset-side move, and emitted auditable receipts without bypassing workflow authority. |
| REPT-001 | PASS | `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`, `reports/generated/positive-margin-call-quickstart-optimization-report.json`, `reports/generated/positive-margin-call-quickstart-workflow-result.json`, `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`, `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json` | The Quickstart execution report references real policy, optimization, workflow, and adapter artifacts rather than operator-authored placeholders. |
| EXCP-001 | PASS | `reports/generated/negative-ineligible-asset-quickstart-policy-evaluation-report.json`, `reports/generated/negative-workflow-rejected-quickstart-policy-evaluation-report.json`, `reports/generated/negative-workflow-rejected-quickstart-workflow-result.json`, `reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json` | The negative Quickstart scenarios blocked either before workflow execution or at workflow gating and did not fabricate downstream adapter success. |

## Positive Path

- Recommended action: `POST_NEW_SET`
- Selected lots: `quickstart-demo-lot-101, quickstart-demo-lot-102, quickstart-demo-lot-103, quickstart-demo-lot-104`
- Workflow result artifact: `reports/generated/positive-margin-call-quickstart-workflow-result.json`
- Adapter result artifact: `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
- Adapter status artifact: `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`
- Quickstart seed receipt: `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`

