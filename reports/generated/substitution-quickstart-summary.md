# Substitution Demo Summary

- Report ID: `srr-a8a9d213c0f6408a`
- Runtime mode: `QUICKSTART`
- Command: `make demo-substitution-quickstart`
- Manifest: `examples/demo-scenarios/substitution/quickstart-demo-config.json`
- Report artifact: `reports/generated/substitution-quickstart-report.json`

## Scenario Outcomes

| Scenario | Mode | Result | Blocked Phase | Adapter Outcome | Summary |
| --- | --- | --- | --- | --- | --- |
| positive-substitution-quickstart | POSITIVE | SUCCESS | - | EXECUTED | Quickstart preserved the incumbent encumbrance set until the full replacement scope was approved, the adapter released quickstart-sub-current-eib-521, quickstart-sub-current-kfw-521 and moved quickstart-sub-repl-fannie-521, quickstart-sub-repl-ust-521, and Canton closed the substitution atomically. |
| negative-replacement-becomes-ineligible-quickstart | NEGATIVE | EXPECTED_FAILURE | POLICY_EVALUATION | NOT_REQUESTED | Policy evaluation blocked the replacement inventory with decision REJECT and reason codes ASSET_CLASS_NOT_ELIGIBLE, HAIRCUT_RULE_NOT_FOUND, ISSUER_NOT_ON_ALLOW_LIST, ISSUER_RATING_BELOW_MINIMUM, ISSUER_TYPE_NOT_ALLOWED, ISSUE_TYPE_NOT_ELIGIBLE. |
| negative-partial-substitution-quickstart | NEGATIVE | EXPECTED_FAILURE | WORKFLOW | BLOCKED | Quickstart blocked the partial substitution before settlement commit, the incumbent encumbrance set remained quickstart-sub-current-eib-621, quickstart-sub-current-kfw-621, and the adapter surface remained at 0 receipts. |

## Invariant Checks

| Invariant | Status | Evidence | Note |
| --- | --- | --- | --- |
| PDR-001 | PASS | `reports/generated/positive-substitution-quickstart-policy-evaluation-report.json` | The positive Quickstart substitution path used a generated policy-evaluation report derived from declared inputs. |
| ALLOC-001 | PASS | `reports/generated/positive-substitution-quickstart-optimization-report.json` | The optimizer produced a deterministic replacement recommendation that matched the declared Quickstart substitution seed scope. |
| WF-001 | PASS | `reports/generated/positive-substitution-quickstart/localnet-control-plane-seed-receipt.json`, `reports/generated/positive-substitution-quickstart-workflow-result.json` | The Quickstart substitution workflow remained authoritative for incumbent scope, approvals, settlement intent, and final atomic closure. |
| ADAPT-001 | PASS | `reports/generated/positive-substitution-quickstart-workflow-result.json`, `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`, `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json` | The reference token adapter consumed the Quickstart substitution handoff artifact, executed incumbent release plus replacement movement, and emitted auditable receipts without bypassing workflow authority. |
| ATOM-001 | PASS | `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`, `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json`, `reports/generated/negative-partial-substitution-quickstart-workflow-result.json`, `reports/generated/negative-partial-substitution-quickstart/localnet-substitution-status.json` | The positive Quickstart path committed the full release-and-replacement scope atomically, and the blocked partial path preserved the incumbent encumbrance and holding state without adapter side effects. |
| REPT-001 | PASS | `reports/generated/positive-substitution-quickstart-policy-evaluation-report.json`, `reports/generated/positive-substitution-quickstart-optimization-report.json`, `reports/generated/positive-substitution-quickstart-workflow-result.json`, `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`, `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json` | The Quickstart substitution report references real policy, optimization, workflow, adapter, and status artifacts rather than operator-authored summaries. |
| EXCP-001 | PASS | `reports/generated/negative-replacement-becomes-ineligible-quickstart-policy-evaluation-report.json`, `reports/generated/negative-partial-substitution-quickstart-policy-evaluation-report.json`, `reports/generated/negative-partial-substitution-quickstart-workflow-result.json`, `reports/generated/negative-partial-substitution-quickstart/localnet-substitution-status.json` | The negative Quickstart substitution scenarios failed deterministically for policy ineligibility and blocked partial substitution without fabricating downstream adapter success. |
