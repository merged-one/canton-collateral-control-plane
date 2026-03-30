# Substitution Demo Summary

- Report ID: `srr-41979123ad810f49`
- Runtime mode: `IDE_LEDGER`
- Command: `make demo-substitution`
- Manifest: `examples/demo-scenarios/substitution/demo-config.json`
- Report artifact: `reports/generated/substitution-demo-report.json`

## Scenario Outcomes

| Scenario | Mode | Result | Blocked Phase | Adapter Outcome | Summary |
| --- | --- | --- | --- | --- | --- |
| positive-substitution | POSITIVE | SUCCESS | - | BLOCKED | Current encumbrances stayed controlled until approval, the optimizer recommended sub-repl-fannie, sub-repl-ust, and the Daml workflow closed the substitution atomically against outgoing lots sub-current-kfw, sub-current-eib. |
| negative-replacement-becomes-ineligible | NEGATIVE | EXPECTED_FAILURE | POLICY_EVALUATION | NOT_REQUESTED | Policy evaluation blocked the replacement inventory with decision REJECT and reason codes ASSET_CLASS_NOT_ELIGIBLE, HAIRCUT_RULE_NOT_FOUND, ISSUER_NOT_ON_ALLOW_LIST, ISSUER_RATING_BELOW_MINIMUM, ISSUER_TYPE_NOT_ALLOWED, ISSUE_TYPE_NOT_ELIGIBLE. |
| negative-concentration-breach | NEGATIVE | EXPECTED_FAILURE | OPTIMIZATION | NOT_REQUESTED | Policy evaluation stayed admissible at the lot level, but optimization ended with NO_SOLUTION and reason codes CONCENTRATION_LIMIT_BREACH, INSUFFICIENT_LENDABLE_VALUE. |
| negative-unauthorized-release | NEGATIVE | EXPECTED_FAILURE | WORKFLOW | BLOCKED | The workflow blocked the control path with atomicity outcome BLOCKED_ATOMICALLY and control checks APPROVAL_GATE_BLOCKED, UNAUTHORIZED_RELEASE_BLOCKED. |
| negative-partial-substitution | NEGATIVE | EXPECTED_FAILURE | WORKFLOW | BLOCKED | The workflow blocked the control path with atomicity outcome BLOCKED_ATOMICALLY and control checks APPROVAL_GATE_BLOCKED, PARTIAL_SUBSTITUTION_BLOCKED. |

## Invariant Checks

| Invariant | Status | Evidence | Note |
| --- | --- | --- | --- |
| PDR-001 | PASS | `reports/generated/positive-substitution-policy-evaluation-report.json` | The positive substitution path used a generated policy-evaluation report derived from declared inputs. |
| ALLOC-001 | PASS | `reports/generated/positive-substitution-optimization-report.json` | The optimizer produced a deterministic replacement recommendation with explicit substitution deltas. |
| CTRL-001 | PASS | `reports/generated/positive-substitution-workflow-result.json`, `reports/generated/negative-unauthorized-release-workflow-result.json` | The workflow blocked pre-approval settlement intent creation and blocked the unauthorized release attempt while preserving the current encumbrances. |
| ATOM-001 | PASS | `reports/generated/positive-substitution-workflow-result.json`, `reports/generated/negative-partial-substitution-workflow-result.json` | The positive path replaced encumbrances atomically, and the partial-substitution path failed without releasing the incumbent encumbrances. |
| REPT-001 | PASS | `reports/generated/positive-substitution-workflow-result.json`, `reports/generated/positive-substitution-policy-evaluation-report.json`, `reports/generated/positive-substitution-optimization-report.json` | The substitution report references real workflow, policy, and optimizer artifacts rather than operator-authored summaries. |
| EXCP-001 | PASS | `reports/generated/negative-replacement-becomes-ineligible-policy-evaluation-report.json`, `reports/generated/negative-concentration-breach-policy-evaluation-report.json`, `reports/generated/negative-concentration-breach-optimization-report.json`, `reports/generated/negative-unauthorized-release-policy-evaluation-report.json`, `reports/generated/negative-unauthorized-release-optimization-report.json`, `reports/generated/negative-unauthorized-release-workflow-result.json`, `reports/generated/negative-partial-substitution-policy-evaluation-report.json`, `reports/generated/negative-partial-substitution-optimization-report.json`, `reports/generated/negative-partial-substitution-workflow-result.json` | The negative substitution scenarios failed deterministically for ineligibility, concentration, unauthorized release, and partial-settlement atomicity violations. |
