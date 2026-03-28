# Margin Call Demo Runbook

## Purpose

Run the first end-to-end margin-call prototype and verify that the repository generates real execution artifacts from policy, optimization, and Daml workflow execution.

## Preconditions

- run from the repository root
- local bootstrap completed with `make bootstrap`
- the repo-local Daml toolchain is available under `.runtime/`
- no local policy or demo input edits are pending unless intentionally under test

## Primary Command

```sh
make demo-margin-call
```

This command:

1. compiles the Daml package through `make daml-build`
2. evaluates the positive and negative scenario bundles under `examples/demo-scenarios/margin-call/`
3. runs the positive Daml workflow path with optimizer-selected lots
4. validates the generated `ExecutionReport` against `reports/schemas/execution-report.schema.json`
5. writes JSON and Markdown artifacts under `reports/generated/`

## Expected Artifacts

After a successful run, confirm that these files exist:

- `reports/generated/margin-call-demo-execution-report.json`
- `reports/generated/margin-call-demo-summary.md`
- `reports/generated/margin-call-demo-timeline.md`
- `reports/generated/positive-margin-call-policy-evaluation-report.json`
- `reports/generated/positive-margin-call-optimization-report.json`
- `reports/generated/positive-margin-call-workflow-input.json`
- `reports/generated/positive-margin-call-workflow-result.json`

The same run also refreshes the negative-path artifacts:

- `reports/generated/negative-ineligible-asset-policy-evaluation-report.json`
- `reports/generated/negative-insufficient-lendable-value-policy-evaluation-report.json`
- `reports/generated/negative-insufficient-lendable-value-optimization-report.json`
- `reports/generated/negative-expired-policy-window-policy-evaluation-report.json`

## Operator Checks

Check the execution report:

```sh
jq '{executionId, overallStatus, demo, scenarios: [.scenarios[] | {scenarioId, mode, result, policyDecision, optimizationStatus, recommendedAction}]}' reports/generated/margin-call-demo-execution-report.json
```

Check the positive workflow result:

```sh
jq '{marginCallState, postingState, selectedLotIds, encumberedLotIds, executionReportCount}' reports/generated/positive-margin-call-workflow-result.json
```

Check the Markdown summary:

```sh
sed -n '1,220p' reports/generated/margin-call-demo-summary.md
```

## Failure Handling

If `make demo-margin-call` fails:

1. inspect the reported scenario name and failure reason
2. open the generated scenario artifact under `reports/generated/` if one was written before the failure
3. run the component commands directly if needed:

```sh
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/demo-scenarios/margin-call/positive-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/demo-scenarios/margin-call/positive-inventory.json OBLIGATION=examples/demo-scenarios/margin-call/positive-obligation.json
```

4. if the failure comes from Daml workflow execution, confirm the package still builds:

```sh
make daml-build
make daml-test
```

5. if schema validation fails, inspect the relevant generated JSON file and compare it against:

- `reports/schemas/policy-evaluation-report.schema.json`
- `reports/schemas/optimization-report.schema.json`
- `reports/schemas/execution-report.schema.json`

## Recovery Notes

- The run is idempotent with respect to generated artifacts under `reports/generated/`; re-running the command replaces the prior demo outputs.
- The demo currently uses the Daml IDE ledger, not the pinned Quickstart LocalNet.
- The positive workflow path proves the margin-call and posting sequence only. It does not yet prove Quickstart deployment, asset-adapter execution, or role-scoped report disclosure.
