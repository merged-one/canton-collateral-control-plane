# Final Demo Runbook

## Purpose

Run the proposal-ready prototype package for the Canton Collateral Control Plane and verify that one reproducible command produces:

- Quickstart deployment evidence
- one concrete reference token adapter proof path
- confidential margin-call evidence on Quickstart
- confidential collateral-substitution evidence on Quickstart
- confidential margin-return evidence on Quickstart
- aggregate invariant pass or fail output across those real runtime paths
- machine-readable artifact indexing plus explicit real-versus-staged readiness notes

If you need the reviewer-facing submission wrapper on top of this runtime package, run `make proposal-package` after `make demo-all` or just run `make proposal-package` directly.

## Preconditions

- run from the repository root
- local bootstrap completed with `make bootstrap`
- Docker and the pinned Quickstart LocalNet prerequisites are available
- the repo-local Daml toolchain is available under `.runtime/`
- no local scenario, policy, or report-schema edits are pending unless intentionally under test

## Primary Command

```sh
make demo-all
```

This command:

1. runs `make test-conformance`
2. starts or reuses the pinned Quickstart deployment
3. validates one concrete reference token adapter proof path
4. validates the confidential margin-call, substitution, and return Quickstart demo artifact chains as part of the conformance suite
5. generates aggregate invariant pass or fail output
6. writes `reports/generated/final-demo-pack.json`
7. writes `reports/generated/final-demo-pack-summary.md`

The reviewer-facing wrapper command is:

```sh
make proposal-package
```

That command reruns `make demo-all` as needed and then writes:

- `reports/generated/proposal-submission-manifest.json`
- `reports/generated/proposal-submission-summary.md`

## Expected Artifacts

After a successful run, confirm that these files exist:

- `reports/generated/final-demo-pack.json`
- `reports/generated/final-demo-pack-summary.md`
- `reports/generated/conformance-suite-report.json`
- `reports/generated/conformance-suite-summary.md`
- `reports/generated/localnet-control-plane-deployment-receipt.json`
- `reports/generated/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/localnet-reference-token-adapter-status.json`
- `reports/generated/margin-call-quickstart-execution-report.json`
- `reports/generated/substitution-quickstart-report.json`
- `reports/generated/return-quickstart-report.json`

The operator package also depends on these repository documents:

- `docs/evidence/DEMO_ARTIFACT_INDEX.md`
- `docs/evidence/REVIEWER_START_HERE.md`
- `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md`
- `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md`
- `docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md`
- `docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md`
- `docs/testing/CONFORMANCE_SUITE.md`

## Operator Checks

Check the final pack:

```sh
jq '{demoPackId, overallStatus, runtimeEvidence: {deploymentReceiptPath: .runtimeEvidence.deploymentReceiptPath, referenceAdapterExecutionReportPath: .runtimeEvidence.referenceAdapterExecutionReportPath}, commandSurface, demoFlows: [.demoFlows[] | {demoType, runtimeMode, command, comparisonCommand, reportPath}], readiness}' reports/generated/final-demo-pack.json
```

Check the conformance output:

```sh
jq '{suiteId, overallStatus, checks: [.checks[] | {checkId, status}]}' reports/generated/conformance-suite-report.json
```

Check the readiness assessment:

```sh
sed -n '1,260p' docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md
```

Check the human-readable package summary:

```sh
sed -n '1,260p' reports/generated/final-demo-pack-summary.md
```

Check the reviewer-facing wrapper summary:

```sh
sed -n '1,260p' reports/generated/proposal-submission-summary.md
```

## Failure Handling

If `make demo-all` fails:

1. inspect `reports/generated/conformance-suite-summary.md` if it exists
2. identify whether the failure came from:
   - Quickstart deployment evidence
   - the concrete reference token adapter proof
   - one of the three Quickstart-backed confidential workflow demos
   - the aggregate conformance checks
   - the final demo-pack indexing step
3. re-run the lower-level command that failed:

```sh
make localnet-start-control-plane
make localnet-run-token-adapter
make localnet-adapter-status
make demo-margin-call-quickstart
make demo-substitution-quickstart
make demo-return-quickstart
make test-conformance
```

4. if the failure is in the final pack only, inspect the referenced artifact paths in:

```sh
sed -n '1,260p' reports/generated/conformance-suite-report.json
sed -n '1,260p' reports/generated/final-demo-pack.json
```

5. if the failure is runtime-related, confirm the Quickstart surfaces still look healthy:

```sh
make localnet-start-control-plane
make localnet-status-control-plane
```

## Recovery Notes

- `make demo-all` is idempotent with respect to the generated files under `reports/generated/`
- the package now centers the real Quickstart deployment plus reference-adapter-backed execution story; the IDE-ledger demo commands remain comparison surfaces only
- the final demo pack remains the runtime evidence bundle, while `make proposal-package` is the reviewer-facing submission wrapper
- `make verify` remains the full repository validation loop
