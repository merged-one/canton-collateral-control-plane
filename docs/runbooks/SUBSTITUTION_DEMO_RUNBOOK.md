# Substitution Demo Runbook

## Purpose

Run the first end-to-end substitution prototype and verify that the repository generates real substitution artifacts from policy, optimization, and Daml workflow execution.

## Preconditions

- run from the repository root
- local bootstrap completed with `make bootstrap`
- the repo-local Daml toolchain is available under `.runtime/`
- no local policy or demo input edits are pending unless intentionally under test

## Primary Command

```sh
make demo-substitution
```

This command:

1. compiles the Daml package through `make daml-build`
2. evaluates the positive and negative substitution bundles under `examples/demo-scenarios/substitution/`
3. runs optimizer selection for the scenarios that need replacement recommendations
4. invokes the Daml substitution workflow path for the positive path plus the workflow-control negative paths
5. validates the generated `SubstitutionReport` against `reports/schemas/substitution-report.schema.json`
6. writes JSON and Markdown artifacts under `reports/generated/`

## Expected Artifacts

After a successful run, confirm that these files exist:

- `reports/generated/substitution-demo-report.json`
- `reports/generated/substitution-demo-summary.md`
- `reports/generated/substitution-demo-timeline.md`
- `reports/generated/positive-substitution-policy-evaluation-report.json`
- `reports/generated/positive-substitution-optimization-report.json`
- `reports/generated/positive-substitution-workflow-input.json`
- `reports/generated/positive-substitution-workflow-result.json`

The same run also refreshes the negative-path artifacts:

- `reports/generated/negative-replacement-becomes-ineligible-policy-evaluation-report.json`
- `reports/generated/negative-concentration-breach-policy-evaluation-report.json`
- `reports/generated/negative-concentration-breach-optimization-report.json`
- `reports/generated/negative-unauthorized-release-policy-evaluation-report.json`
- `reports/generated/negative-unauthorized-release-optimization-report.json`
- `reports/generated/negative-unauthorized-release-workflow-input.json`
- `reports/generated/negative-unauthorized-release-workflow-result.json`
- `reports/generated/negative-partial-substitution-policy-evaluation-report.json`
- `reports/generated/negative-partial-substitution-optimization-report.json`
- `reports/generated/negative-partial-substitution-workflow-input.json`
- `reports/generated/negative-partial-substitution-workflow-result.json`

## Operator Checks

Check the substitution report:

```sh
jq '{substitutionReportId, overallStatus, demo, scenarios: [.scenarios[] | {scenarioId, mode, result, policyDecision, optimizationStatus, recommendedAction, observedReasonCodes}]}' reports/generated/substitution-demo-report.json
```

Check the positive workflow result:

```sh
jq '{substitutionState, currentEncumberedLotIds, releasedLotIds, replacementLotIds, activeEncumberedLotIds, atomicityOutcome, executionReportCount}' reports/generated/positive-substitution-workflow-result.json
```

Check the Markdown summary:

```sh
sed -n '1,220p' reports/generated/substitution-demo-summary.md
```

## Failure Handling

If `make demo-substitution` fails:

1. inspect the reported scenario name and failure reason
2. open the generated scenario artifact under `reports/generated/` if one was written before the failure
3. run the component commands directly if needed:

```sh
make policy-eval POLICY=examples/demo-scenarios/substitution/substitution-policy.json INVENTORY=examples/demo-scenarios/substitution/positive-inventory.json
make optimize POLICY=examples/demo-scenarios/substitution/substitution-policy.json INVENTORY=examples/demo-scenarios/substitution/positive-inventory.json OBLIGATION=examples/demo-scenarios/substitution/positive-obligation.json
```

4. if the failure comes from Daml workflow execution, confirm the package still builds and the lifecycle tests still pass:

```sh
make daml-build
make daml-test
```

5. if schema validation fails, inspect the relevant generated JSON file and compare it against:

- `reports/schemas/policy-evaluation-report.schema.json`
- `reports/schemas/optimization-report.schema.json`
- `reports/schemas/substitution-report.schema.json`

## Recovery Notes

- The run is idempotent with respect to generated artifacts under `reports/generated/`; re-running the command replaces the prior substitution outputs.
- The demo currently uses the Daml IDE ledger, not the pinned Quickstart LocalNet.
- The positive workflow path proves encumbered-collateral replacement, approval gating, and atomicity only. It does not yet prove Quickstart deployment, asset-adapter execution, or role-scoped report disclosure.
