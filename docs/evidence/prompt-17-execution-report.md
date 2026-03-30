# Prompt 17 Execution Report

## Scope

Wire the confidential substitution demo through the pinned Quickstart LocalNet and the reference token adapter so one operator command now chains policy evaluation, optimization, Quickstart substitution workflow execution, adapter-driven replacement or release, and final substitution reporting without fabricating success on blocked paths.

## Chained Artifacts

The Quickstart-backed positive path is designed to generate and link:

- one `PolicyEvaluationReport`
- one `OptimizationReport`
- one Quickstart workflow input artifact
- one Quickstart workflow result artifact
- one Quickstart scenario seed receipt
- one substitution adapter execution report
- one provider-visible substitution status artifact
- one final `SubstitutionReport` plus Markdown summary and timeline

The negative Quickstart paths are designed to prove:

- policy-blocked scenarios stop before workflow and adapter execution
- workflow-blocked partial substitution scenarios emit workflow evidence plus provider-visible status evidence showing no release, no replacement movement, and no adapter receipt

## Commands

```sh
make docs-lint
git diff --check
make demo-substitution
make localnet-deploy-dar
make demo-substitution-quickstart
```

Additional command-level checks executed during implementation:

```sh
sh -n scripts/localnet-seed-substitution-demo.sh
sh -n scripts/localnet-run-substitution-workflow.sh
sh -n scripts/localnet-run-substitution-token-adapter.sh
sh -n scripts/localnet-substitution-status.sh
python3 -m py_compile app/orchestration/substitution_demo.py app/orchestration/substitution_cli.py
make daml-build
```

## Results

- `make demo-substitution` passed and regenerated `reports/generated/substitution-demo-report.json` plus the supporting Markdown and workflow artifacts for the IDE-ledger comparison path.
- the first Quickstart redeploy attempt surfaced a real Quickstart package-version conflict:
  - the running participant had already vetted `canton-collateral-control-plane v0.1.7`
  - the modified DAR produced a different package hash under the same package version
  - Quickstart returned HTTP `400` with code `KNOWN_PACKAGE_VERSION`
  - the fix was to bump the shared Daml package version from `0.1.7` to `0.1.8` so the updated Control Plane DAR could be deployed cleanly
- `make localnet-deploy-dar` then passed and the deployment receipt now proves `/Users/charlesdusek/Code/canton-collateral-control-plane/.daml/dist-quickstart/canton-collateral-control-plane-0.1.8.dar` with package id `e7c7bb46feecee544cdefbb58661bfc1563eea27dde48dcba85830b62549a0a4` was installed into the pinned `app-provider` and `app-user` participants.
- `make demo-substitution-quickstart` passed, validated `reports/generated/substitution-quickstart-report.json` against `reports/schemas/substitution-report.schema.json`, and wrote the final Quickstart-backed substitution report at `2026-03-30T03:03:13Z` with `demo.command` set to `make demo-substitution-quickstart`.
- the positive Quickstart substitution path produced and linked these subordinate artifacts:
  - `reports/generated/positive-substitution-quickstart-policy-evaluation-report.json`
  - `reports/generated/positive-substitution-quickstart-optimization-report.json`
  - `reports/generated/positive-substitution-quickstart-workflow-input.json`
  - `reports/generated/positive-substitution-quickstart-workflow-result.json`
  - `reports/generated/positive-substitution-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`
  - `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json`
- the positive Quickstart substitution report proves atomic replacement for incumbent lots `quickstart-sub-current-eib-521` and `quickstart-sub-current-kfw-521` with approved replacement lots `quickstart-sub-repl-fannie-521` and `quickstart-sub-repl-ust-521`:
  - `atomicityEvidence.proofStatus` is `ATOMICALLY_COMMITTED`
  - adapter release actions exactly match the incumbent encumbered set
  - adapter replacement actions exactly match the approved replacement set
  - final released lots exactly match the incumbent set
  - final active encumbered lots exactly match the replacement set
  - provider-visible current holdings show the incumbent lots returned to `provider-account-substitution-521`
  - provider-visible replacement holdings show the replacement lots settled into `secured-account-substitution-521`
  - provider-visible adapter receipt count is `1`
- the positive substitution adapter execution artifact proves:
  - receipt `positive-substitution-quickstart-reference-token-substitution-receipt`
  - receipt status `EXECUTED`
  - instruction `quickstart-substitution-correlation-521-instruction`
  - two release movements back to `provider-account-substitution-521`
  - two replacement movements into `secured-account-substitution-521`
  - workflow confirmation with substitution state `Closed` and settlement-instruction state `Settled`
- the negative ineligible Quickstart scenario blocked at `POLICY_EVALUATION` and emitted no workflow, seed, or adapter artifacts.
- the negative partial-substitution Quickstart scenario produced and linked:
  - `reports/generated/negative-partial-substitution-quickstart-policy-evaluation-report.json`
  - `reports/generated/negative-partial-substitution-quickstart-optimization-report.json`
  - `reports/generated/negative-partial-substitution-quickstart-workflow-input.json`
  - `reports/generated/negative-partial-substitution-quickstart-workflow-result.json`
  - `reports/generated/negative-partial-substitution-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/negative-partial-substitution-quickstart/localnet-substitution-status.json`
- the blocked partial-substitution evidence proves no side effects committed for the incumbent lots `quickstart-sub-current-eib-621` and `quickstart-sub-current-kfw-621`:
  - `atomicityEvidence.proofStatus` is `BLOCKED_NO_SIDE_EFFECTS`
  - `blockedPhase` is `WORKFLOW`
  - adapter release actions and replacement actions are both empty
  - final released lots are empty
  - final active encumbered lots remain the incumbent set
  - provider-visible replacement holdings are empty
  - provider-visible adapter receipt count is `0`
  - provider-visible status still shows substitution state `Approved` with no settlement instruction and the incumbent holdings retained in `secured-account-substitution-621`
- `make docs-lint` passed after the ADR, tracker, runbook, spec, invariant, risk, threat-model, and command-surface updates landed.
- `git diff --check` passed with no whitespace or patch-format issues.

## Remaining Gaps

- the return path does not yet run through the same Quickstart-backed workflow-plus-adapter chain
- the current report and status surfaces still use the workflow-party and provider-visible baseline rather than role-scoped disclosure profiles
- the reference token adapter remains a narrow reference path rather than a production custodian, issuer, or tri-party integration
