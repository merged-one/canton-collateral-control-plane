# Margin Call Demo Runbook

## Purpose

Run the Quickstart-backed end-to-end margin-call demo and verify that the repository generates real execution artifacts from policy, optimization, Quickstart workflow execution, reference-token adapter execution, and final execution reporting.

## Preconditions

- run from the repository root
- local bootstrap completed with `make bootstrap`
- Docker and the pinned Quickstart LocalNet prerequisites are available
- the repo-local Daml toolchain is available under `.runtime/`
- no local policy or demo input edits are pending unless intentionally under test

## Primary Command

```sh
make demo-margin-call-quickstart
```

This command:

1. starts or reuses the Quickstart LocalNet through `make localnet-start-control-plane`
2. evaluates the Quickstart positive and negative scenario bundle under `examples/demo-scenarios/margin-call/quickstart-demo-config.json`
3. reseeds one scenario-scoped Quickstart ledger state for each workflow-bearing scenario
4. runs the positive Quickstart workflow path with optimizer-selected lots and hands the resulting settlement instruction to the reference token adapter
5. proves a negative workflow-rejection path that emits no adapter receipt, holding, or encumbrance movement
6. validates the generated `ExecutionReport` against `reports/schemas/execution-report.schema.json`
7. writes JSON and Markdown artifacts under `reports/generated/`

`make demo-margin-call` remains available as the IDE-ledger comparison path, but the Quickstart command is now the primary operator runbook for the confidential margin-call chain.

## Expected Artifacts

After a successful run, confirm that these files exist:

- `reports/generated/margin-call-demo-execution-report.json`
- `reports/generated/margin-call-quickstart-summary.md`
- `reports/generated/margin-call-quickstart-timeline.md`
- `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`
- `reports/generated/positive-margin-call-quickstart-optimization-report.json`
- `reports/generated/positive-margin-call-quickstart-workflow-input.json`
- `reports/generated/positive-margin-call-quickstart-workflow-result.json`
- `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`

The same run also refreshes the negative-path artifacts:

- `reports/generated/negative-ineligible-asset-quickstart-policy-evaluation-report.json`
- `reports/generated/negative-workflow-rejected-quickstart-policy-evaluation-report.json`
- `reports/generated/negative-workflow-rejected-quickstart-optimization-report.json`
- `reports/generated/negative-workflow-rejected-quickstart-workflow-input.json`
- `reports/generated/negative-workflow-rejected-quickstart-workflow-result.json`
- `reports/generated/negative-workflow-rejected-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json`

## Operator Checks

Check the execution report:

```sh
jq '{executionId, overallStatus, demo: {command, runtimeMode}, scenarios: [.scenarios[] | {scenarioId, mode, result, blockedPhase, adapterOutcome, workflowArtifactPath, adapterExecutionReportPath, adapterStatusPath}]}' reports/generated/margin-call-quickstart-execution-report.json
```

Check the positive workflow result:

```sh
jq '{marginCallState, postingState, workflowGate, settlementInstructionId, settlementInstructionState, selectedLotIds, encumberedLotIds, executionReportCount}' reports/generated/positive-margin-call-quickstart-workflow-result.json
```

Check the positive adapter result:

```sh
jq '{reportId, adapterReceipt: {status, movementLotIds: [.adapterReceipt.movements[].lotId]}, workflowConfirmation: {postingStateAfterConfirmation, settledInstructionState}}' reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json
```

Check the blocked negative adapter status:

```sh
jq '{postingState, settlementInstructionState, providerVisibleEncumbranceCount, providerVisibleAdapterReceipts: (.providerVisibleAdapterReceipts | length), providerVisibleReferenceTokenHoldings: (.providerVisibleReferenceTokenHoldings | length)}' reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json
```

Check the Markdown summary:

```sh
sed -n '1,240p' reports/generated/margin-call-quickstart-summary.md
```

## Failure Handling

If `make demo-margin-call-quickstart` fails:

1. inspect the reported scenario name and failure reason
2. open the generated scenario artifact under `reports/generated/` if one was written before the failure
3. confirm the Quickstart overlay is still healthy:

```sh
make localnet-start-control-plane
make localnet-status-control-plane
```

4. run the component commands directly if needed:

```sh
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/demo-scenarios/margin-call/quickstart-positive-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/demo-scenarios/margin-call/quickstart-positive-inventory.json OBLIGATION=examples/demo-scenarios/margin-call/quickstart-positive-obligation.json
```

5. if the failure comes from Quickstart workflow execution, inspect:

- `reports/generated/<scenario-id>/localnet-control-plane-seed-receipt.json`
- `reports/generated/<scenario-id>-workflow-input.json`
- `reports/generated/<scenario-id>-workflow-result.json`

6. if the failure comes from adapter execution or blocked-path assertions, inspect:

- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`
- `reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json`

7. if the failure comes from Daml build or workflow execution, confirm the package still builds:

```sh
make daml-build
make daml-test
```

8. if schema validation fails, inspect the relevant generated JSON file and compare it against:

- `reports/schemas/policy-evaluation-report.schema.json`
- `reports/schemas/optimization-report.schema.json`
- `reports/schemas/execution-report.schema.json`
- `reports/schemas/adapter-execution-report.schema.json`

## Recovery Notes

- The run is idempotent with respect to generated artifacts under `reports/generated/`; re-running the command replaces the prior demo outputs.
- The Quickstart run reseeds scenario-scoped state directories under `.runtime/localnet/control-plane/` and rewrites scenario-scoped artifacts under `reports/generated/<scenario-id>/`.
- The positive Quickstart path now proves policy evaluation, optimization, workflow preparation, adapter execution, and final execution reporting on the pinned LocalNet.
- `make demo-margin-call` remains the IDE-ledger comparison path.
- Substitution and return still do not execute through this Quickstart-backed chain, and role-scoped report disclosure remains future work.
