# Substitution Demo Runbook

## Purpose

Run the Control Plane substitution demos and verify that the repository generates real substitution artifacts from policy evaluation, optimization, workflow execution, adapter execution where applicable, and final reporting.

## Preconditions

- run from the repository root
- `make bootstrap` completed
- Docker available for the Quickstart-backed path
- no unintended local scenario or policy edits are pending

## Primary Commands

IDE-ledger comparison path:

```sh
make demo-substitution
```

Quickstart-backed end-to-end path:

```sh
make demo-substitution-quickstart
```

`make demo-substitution` keeps the first substitution prototype on the Daml IDE ledger. `make demo-substitution-quickstart` starts or reuses the pinned Quickstart overlay, deploys the current Control Plane DAR, evaluates substitution scenarios, prepares the positive substitution on Quickstart, invokes the reference token adapter for incumbent release plus replacement movement, refreshes provider-visible status, validates the generated `SubstitutionReport`, and writes JSON plus Markdown artifacts under `reports/generated/`.

## Expected Quickstart Artifacts

After `make demo-substitution-quickstart` succeeds, confirm these files exist:

- `reports/generated/substitution-quickstart-report.json`
- `reports/generated/substitution-quickstart-summary.md`
- `reports/generated/substitution-quickstart-timeline.md`
- `reports/generated/positive-substitution-quickstart-policy-evaluation-report.json`
- `reports/generated/positive-substitution-quickstart-optimization-report.json`
- `reports/generated/positive-substitution-quickstart-workflow-input.json`
- `reports/generated/positive-substitution-quickstart-workflow-result.json`
- `reports/generated/positive-substitution-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`
- `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json`
- `reports/generated/negative-replacement-becomes-ineligible-quickstart-policy-evaluation-report.json`
- `reports/generated/negative-partial-substitution-quickstart-policy-evaluation-report.json`
- `reports/generated/negative-partial-substitution-quickstart-optimization-report.json`
- `reports/generated/negative-partial-substitution-quickstart-workflow-input.json`
- `reports/generated/negative-partial-substitution-quickstart-workflow-result.json`
- `reports/generated/negative-partial-substitution-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/negative-partial-substitution-quickstart/localnet-substitution-status.json`

## Operator Checks

Inspect the Quickstart substitution report:

```sh
jq '{substitutionReportId, overallStatus, demo, scenarios: [.scenarios[] | {scenarioId, mode, result, workflowRuntime, adapterOutcome, blockedPhase, atomicityEvidence}]}' reports/generated/substitution-quickstart-report.json
```

Inspect the positive workflow handoff before adapter confirmation:

```sh
jq '{substitutionState, settlementInstructionId, settlementInstructionState, currentEncumberedLotIds, replacementLotIds, activeEncumberedLotIds, atomicityOutcome, controlChecks}' reports/generated/positive-substitution-quickstart-workflow-result.json
```

Inspect the positive adapter execution proof:

```sh
jq '{incumbentEncumberedLotIds, approvedReplacementLotIds, adapterActions, workflowConfirmation}' reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json
```

Inspect the provider-visible positive post-substitution state:

```sh
jq '{substitutionState, settlementInstructionState, providerVisibleEncumbrances, providerVisibleCurrentLotHoldings, providerVisibleReplacementLotHoldings, providerVisibleAdapterReceipts}' reports/generated/positive-substitution-quickstart/localnet-substitution-status.json
```

Inspect the blocked partial-substitution status proof:

```sh
jq '{substitutionState, settlementInstructionState, providerVisibleEncumbrances, providerVisibleCurrentLotHoldings, providerVisibleReplacementLotHoldings, providerVisibleAdapterReceipts}' reports/generated/negative-partial-substitution-quickstart/localnet-substitution-status.json
```

## Failure Handling

If `make demo-substitution-quickstart` fails:

1. inspect the reported scenario and phase in `reports/generated/substitution-quickstart-report.json` if it was written
2. inspect the scenario-local artifacts under `reports/generated/positive-substitution-quickstart/` or `reports/generated/negative-partial-substitution-quickstart/`
3. confirm the Quickstart surface is healthy:

```sh
make localnet-start-control-plane
make localnet-status-control-plane
```

4. rerun the substitution-specific Quickstart helpers directly if needed:

```sh
sh -n scripts/localnet-seed-substitution-demo.sh
sh -n scripts/localnet-run-substitution-workflow.sh
sh -n scripts/localnet-run-substitution-token-adapter.sh
sh -n scripts/localnet-substitution-status.sh
make localnet-deploy-dar
```

5. if the failure is isolated to policy or optimization, rerun the off-ledger steps directly:

```sh
make policy-eval POLICY=examples/demo-scenarios/substitution/substitution-policy.json INVENTORY=examples/demo-scenarios/substitution/quickstart-positive-inventory.json
make optimize POLICY=examples/demo-scenarios/substitution/substitution-policy.json INVENTORY=examples/demo-scenarios/substitution/quickstart-positive-inventory.json OBLIGATION=examples/demo-scenarios/substitution/quickstart-positive-obligation.json
```

## Recovery Notes

- `make demo-substitution` remains the IDE-ledger comparison path and does not exercise Quickstart or the adapter boundary.
- `make demo-substitution-quickstart` now proves one real positive atomic replacement path and one real blocked partial-substitution path on Quickstart.
- the current Quickstart substitution path still uses the narrow reference token adapter rather than a production custodian or issuer integration.
- margin return remains outside the Quickstart-backed adapter chain and is still pending equivalent runtime coverage.
