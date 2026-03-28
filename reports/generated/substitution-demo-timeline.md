# Substitution Demo Timeline

| Seq | Scenario | Phase | Status | Artifact | Detail |
| --- | --- | --- | --- | --- | --- |
| 1 | positive-substitution | POLICY_EVALUATION | COMPLETED | `reports/generated/positive-substitution-policy-evaluation-report.json` | Evaluated substitution candidates for positive scenario with overall decision ACCEPT. |
| 2 | positive-substitution | OPTIMIZATION | COMPLETED | `reports/generated/positive-substitution-optimization-report.json` | Optimized the substitution request for scenario positive-substitution with recommendation SUBSTITUTE. |
| 3 | positive-substitution | WORKFLOW | COMPLETED | `reports/generated/positive-substitution-workflow-result.json` | Recorded the Daml substitution workflow for scenario positive-substitution and confirmed atomic encumbrance replacement. |
| 4 | negative-replacement-becomes-ineligible | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-replacement-becomes-ineligible-policy-evaluation-report.json` | Evaluated substitution candidates for negative scenario with overall decision REJECT. |
| 5 | negative-concentration-breach | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-concentration-breach-policy-evaluation-report.json` | Evaluated substitution candidates for negative scenario with overall decision ACCEPT. |
| 6 | negative-concentration-breach | OPTIMIZATION | COMPLETED | `reports/generated/negative-concentration-breach-optimization-report.json` | Optimized the substitution request for scenario negative-concentration-breach with recommendation NO_SOLUTION. |
| 7 | negative-unauthorized-release | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-unauthorized-release-policy-evaluation-report.json` | Evaluated substitution candidates for negative scenario with overall decision ACCEPT. |
| 8 | negative-unauthorized-release | OPTIMIZATION | COMPLETED | `reports/generated/negative-unauthorized-release-optimization-report.json` | Optimized the substitution request for scenario negative-unauthorized-release with recommendation SUBSTITUTE. |
| 9 | negative-unauthorized-release | WORKFLOW | COMPLETED | `reports/generated/negative-unauthorized-release-workflow-result.json` | Recorded the Daml control failure for scenario negative-unauthorized-release with workflow state PendingSettlement. |
| 10 | negative-partial-substitution | POLICY_EVALUATION | COMPLETED | `reports/generated/negative-partial-substitution-policy-evaluation-report.json` | Evaluated substitution candidates for negative scenario with overall decision ACCEPT. |
| 11 | negative-partial-substitution | OPTIMIZATION | COMPLETED | `reports/generated/negative-partial-substitution-optimization-report.json` | Optimized the substitution request for scenario negative-partial-substitution with recommendation SUBSTITUTE. |
| 12 | negative-partial-substitution | WORKFLOW | COMPLETED | `reports/generated/negative-partial-substitution-workflow-result.json` | Recorded the Daml control failure for scenario negative-partial-substitution with workflow state Approved. |
