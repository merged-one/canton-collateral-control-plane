# Prompt 16 Execution Report

## Scope

Wire the confidential margin-call demo through the pinned Quickstart LocalNet and the reference token adapter so one operator command now chains policy evaluation, optimization, Quickstart workflow preparation, adapter execution, and final execution reporting without fabricating success on blocked paths.

## Chained Artifacts

The Quickstart-backed positive path is designed to generate and link:

- one `PolicyEvaluationReport`
- one `OptimizationReport`
- one Quickstart workflow input artifact
- one Quickstart workflow result artifact
- one Quickstart scenario seed receipt
- one adapter execution report
- one provider-visible adapter status artifact
- one final `ExecutionReport` plus Markdown summary and timeline

The negative Quickstart paths are designed to prove:

- policy-blocked scenarios stop before workflow and adapter execution
- workflow-rejected scenarios emit workflow evidence plus provider-visible adapter status evidence showing no downstream movement

## Commands

```sh
make docs-lint
git diff --check
make demo-margin-call
make demo-margin-call-quickstart
```

Additional command-level checks executed during implementation:

```sh
sh -n scripts/localnet-run-margin-call-workflow.sh
sh -n scripts/localnet-run-token-adapter.sh
sh -n scripts/localnet-seed-demo.sh
sh -n scripts/localnet-status-control-plane.sh
python3 -m py_compile app/orchestration/margin_call_demo.py app/orchestration/cli.py
make daml-build
```

## Results

- `make demo-margin-call` passed and regenerated `reports/generated/margin-call-demo-execution-report.json` plus the supporting Markdown and workflow artifacts for the IDE-ledger comparison path.
- the first `make demo-margin-call-quickstart` attempt failed for a real Quickstart reason before the orchestration layer completed:
  - the running participant had already vetted `canton-collateral-control-plane v0.1.5`
  - the modified DAR produced a different package hash under the same package version
  - Quickstart returned HTTP `400` with code `KNOWN_PACKAGE_VERSION`
  - the fix was to bump the shared Daml package version from `0.1.5` to `0.1.6` so the updated Control Plane DAR could be deployed cleanly
- the rerun of `make demo-margin-call-quickstart` passed, validated `reports/generated/margin-call-quickstart-execution-report.json` against `reports/schemas/execution-report.schema.json`, and wrote execution id `exr-9bc26ea5d960c241` at `2026-03-29T23:32:01Z`.
- the Quickstart deployment receipt now proves `.daml/dist-quickstart/canton-collateral-control-plane-0.1.6.dar` with package id `ae41ef524a90248a1d0e48368a15dadda5347f8af32fb4e173cfcaab157380c7` was installed into the pinned `app-provider` and `app-user` participants.
- the positive Quickstart margin-call path produced and linked these subordinate artifacts:
  - `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`
  - `reports/generated/positive-margin-call-quickstart-optimization-report.json`
  - `reports/generated/positive-margin-call-quickstart-workflow-input.json`
  - `reports/generated/positive-margin-call-quickstart-workflow-result.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`
- the positive Quickstart workflow artifact proves:
  - margin-call state `Closed`
  - posting state `PendingSettlement` before adapter confirmation
  - workflow gate `PREPARE_FOR_ADAPTER`
  - settlement instruction `quickstart-demo-posting-correlation-101-instruction`
  - settlement-instruction state `PendingSettlement`
  - selected lots `quickstart-demo-lot-101`, `quickstart-demo-lot-102`, `quickstart-demo-lot-103`, and `quickstart-demo-lot-104`
- the positive adapter execution artifact proves:
  - receipt `quickstart-demo-margin-101-reference-token-receipt`
  - receipt status `EXECUTED`
  - instruction `quickstart-demo-posting-correlation-101-instruction`
  - four real movements into `secured-account-quickstart-demo-101` for lots `quickstart-demo-lot-101`, `quickstart-demo-lot-102`, `quickstart-demo-lot-103`, and `quickstart-demo-lot-104`
  - posting state `Closed` after workflow confirmation
  - settlement instruction state `Settled` after workflow confirmation
  - four pledged encumbrances and two provider-visible workflow execution reports after confirmation
- the negative ineligible Quickstart scenario blocked at `POLICY_EVALUATION` and emitted no optimization, workflow, seed, or adapter artifacts.
- the negative workflow-rejected Quickstart scenario produced and linked:
  - `reports/generated/negative-workflow-rejected-quickstart-policy-evaluation-report.json`
  - `reports/generated/negative-workflow-rejected-quickstart-optimization-report.json`
  - `reports/generated/negative-workflow-rejected-quickstart-workflow-input.json`
  - `reports/generated/negative-workflow-rejected-quickstart-workflow-result.json`
  - `reports/generated/negative-workflow-rejected-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/negative-workflow-rejected-quickstart/localnet-reference-token-adapter-status.json`
- the negative workflow artifact proves the secured party rejected the posting with:
  - workflow gate `REJECT_BY_SECURED_PARTY`
  - posting state `Rejected`
  - no settlement instruction id
  - observed reason code `WORKFLOW_REJECTED`
- the blocked adapter-status artifact proves no downstream data-plane movement occurred on that rejected path:
  - posting state `Rejected`
  - settlement-instruction state `null`
  - provider-visible adapter receipt count `0`
  - provider-visible reference-token-holding count `0`
  - provider-visible encumbrance count `0`
- `make docs-lint` passed after the new Quickstart margin-call docs, ADR, tracker, runbook, and evidence updates landed.
- `git diff --check` passed with no whitespace or patch-format issues.

## Remaining Gaps

- substitution and return do not yet run through the same Quickstart-backed workflow-plus-adapter chain
- the current execution-report and adapter-status surfaces still use the workflow-party and provider-visible baseline rather than role-scoped disclosure profiles
- the reference token adapter remains a narrow posting-focused reference path rather than a production custodian or issuer integration
