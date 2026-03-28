# Margin Call Demo Summary

## Overview

- Execution report: `reports/generated/margin-call-demo-execution-report.json`
- Scenario count: `4`
- Primary policy evaluation artifact: `reports/generated/positive-margin-call-policy-evaluation-report.json`

## Scenario Results

| Scenario | Mode | Result | Summary |
| --- | --- | --- | --- |
| positive-margin-call | POSITIVE | SUCCESS | Policy accepted the candidate set, the optimizer recommended POST_NEW_SET, and the Daml workflow closed the margin-call and posting path for lots mc-lot-001, mc-lot-002, mc-lot-003, mc-lot-004. |
| negative-ineligible-asset | NEGATIVE | EXPECTED_FAILURE | Policy evaluation blocked the scenario with decision REJECT and reason codes ASSET_CLASS_NOT_ELIGIBLE, HAIRCUT_RULE_NOT_FOUND, ISSUER_NOT_ON_ALLOW_LIST, ISSUER_RATING_BELOW_MINIMUM, ISSUER_TYPE_NOT_ALLOWED, ISSUE_TYPE_NOT_ELIGIBLE. |
| negative-insufficient-lendable-value | NEGATIVE | EXPECTED_FAILURE | Policy evaluation stayed admissible at the lot level, but optimization ended with NO_SOLUTION and reason codes INSUFFICIENT_LENDABLE_VALUE. |
| negative-expired-policy-window | NEGATIVE | EXPECTED_FAILURE | Policy evaluation blocked the scenario with decision REJECT and reason codes POLICY_NOT_EFFECTIVE. |

## Invariant Checks

| Invariant | Status | Evidence | Note |
| --- | --- | --- | --- |
| PDR-001 | PASS | `reports/generated/positive-margin-call-policy-evaluation-report.json` | The positive path policy report was generated from declared policy and inventory inputs. |
| ALLOC-001 | PASS | `reports/generated/positive-margin-call-optimization-report.json` | The optimizer produced a deterministic selected-lot recommendation with an explanation trace. |
| WF-001 | PASS | `reports/generated/positive-margin-call-workflow-result.json` | The Daml workflow closed the margin-call issuance and collateral-posting path through committed choices. |
| REPT-001 | PASS | `reports/generated/positive-margin-call-workflow-result.json`, `reports/generated/positive-margin-call-policy-evaluation-report.json`, `reports/generated/positive-margin-call-optimization-report.json` | The execution report references real workflow, policy, and optimization artifacts rather than operator-authored placeholders. |
| EXCP-001 | PASS | `reports/generated/negative-ineligible-asset-policy-evaluation-report.json`, `reports/generated/negative-insufficient-lendable-value-policy-evaluation-report.json`, `reports/generated/negative-expired-policy-window-policy-evaluation-report.json` | The negative scenarios fail with explicit reason codes for ineligible collateral, insufficient lendable value, and an expired policy window. |

## Positive Workflow Path

- Recommended action: `POST_NEW_SET`
- Selected lots: `mc-lot-001, mc-lot-002, mc-lot-003, mc-lot-004`
- Workflow result artifact: `reports/generated/positive-margin-call-workflow-result.json`

