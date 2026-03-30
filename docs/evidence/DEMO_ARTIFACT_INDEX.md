# Demo Artifact Index

## Purpose

This index identifies the real artifact bundle produced by the proposal-ready demo surface. It is the reviewer-facing map from commands to generated evidence and now centers the Quickstart-backed runtime path rather than the older IDE-ledger comparison flow.

## Primary Commands

```sh
make test-conformance
make demo-all
make proposal-package
```

## Aggregate Artifacts

| Artifact | Type | Produced By | Purpose |
| --- | --- | --- | --- |
| `reports/generated/conformance-suite-report.json` | JSON | `make test-conformance` | machine-readable invariant pass or fail output across the Quickstart-backed margin-call, substitution, and return demos plus runtime evidence |
| `reports/generated/conformance-suite-summary.md` | Markdown | `make test-conformance` | human-readable summary of the aggregate conformance checks |
| `reports/generated/conformance-eligibility-determinism-policy-evaluation-report.json` | JSON | `make test-conformance` | supporting determinism evidence for repeated policy evaluation |
| `reports/generated/conformance-haircut-policy-evaluation-report.json` | JSON | `make test-conformance` | supporting haircut-vector evidence for lendable-value arithmetic |
| `reports/generated/final-demo-pack.json` | JSON | `make demo-all` | machine-readable package index for the Quickstart-backed final prototype demonstration |
| `reports/generated/final-demo-pack-summary.md` | Markdown | `make demo-all` | operator and reviewer summary of the final prototype package |
| `reports/generated/proposal-submission-manifest.json` | JSON | `make proposal-package` | machine-readable reviewer-facing wrapper that freezes the current Quickstart proof set, reviewer docs, and proposal claim boundary |
| `reports/generated/proposal-submission-summary.md` | Markdown | `make proposal-package` | short reviewer summary for proposal submission built from the generated runtime evidence |

## Quickstart Runtime Foundation Artifacts

| Artifact | Type | Produced By | Purpose |
| --- | --- | --- | --- |
| `reports/generated/localnet-control-plane-deployment-receipt.json` | JSON | `make localnet-start-control-plane` and `make test-conformance` | machine-readable proof that the Control Plane DAR was deployed into the pinned Quickstart participants |
| `reports/generated/localnet-control-plane-deployment-summary.md` | Markdown | `make localnet-start-control-plane` and `make test-conformance` | human-readable deployment summary for the pinned Quickstart surface |
| `reports/generated/localnet-reference-token-adapter-execution-report.json` | JSON | `make localnet-run-token-adapter` and validated by `make test-conformance` | proof of one concrete reference token adapter posting path |
| `reports/generated/localnet-reference-token-adapter-status.json` | JSON | `make localnet-adapter-status` and validated by `make test-conformance` | provider-visible status evidence for one concrete reference token adapter path |

## Confidential Workflow Demo Artifacts

### Margin Call On Quickstart

- `reports/generated/margin-call-quickstart-execution-report.json`
- `reports/generated/margin-call-quickstart-summary.md`
- `reports/generated/margin-call-quickstart-timeline.md`
- `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`
- `reports/generated/positive-margin-call-quickstart-optimization-report.json`
- `reports/generated/positive-margin-call-quickstart-workflow-input.json`
- `reports/generated/positive-margin-call-quickstart-workflow-result.json`
- `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`

### Collateral Substitution On Quickstart

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
- blocked-path substitution policy, workflow, and status artifacts for replacement ineligibility and partial-substitution rejection

### Margin Return On Quickstart

- `reports/generated/return-quickstart-report.json`
- `reports/generated/return-quickstart-summary.md`
- `reports/generated/return-quickstart-timeline.md`
- `reports/generated/positive-return-quickstart-policy-evaluation-report.json`
- `reports/generated/positive-return-quickstart-optimization-report.json`
- `reports/generated/positive-return-quickstart-workflow-input.json`
- `reports/generated/positive-return-quickstart-workflow-result.json`
- `reports/generated/positive-return-quickstart/localnet-control-plane-seed-receipt.json`
- `reports/generated/positive-return-quickstart/localnet-return-adapter-execution-report.json`
- `reports/generated/positive-return-quickstart/localnet-return-status.json`
- blocked-path return policy, workflow, adapter, and status artifacts for unauthorized release, replay-safe duplicate handling, and obligation-state mismatch

## Supporting Documentation

The final demo package should be read together with:

- `docs/evidence/REVIEWER_START_HERE.md`
- `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md`
- `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md`
- `docs/testing/CONFORMANCE_SUITE.md`
- `docs/runbooks/FINAL_DEMO_RUNBOOK.md`
- `docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md`
- `docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md`
- `docs/evidence/prompt-19-execution-report.md`

## Reviewer Workflow

1. run `make proposal-package`
2. inspect `reports/generated/proposal-submission-manifest.json`
3. inspect `reports/generated/final-demo-pack.json`
4. inspect `reports/generated/conformance-suite-report.json`
5. inspect the Quickstart deployment receipt and concrete reference adapter proof artifacts
6. inspect the three Quickstart-backed confidential workflow reports
7. inspect the readiness assessment, reviewer memo, integration guide, and this artifact index

The package is only valid if the machine-readable artifacts, Markdown summaries, and documented command surface all line up with one another and the real-versus-staged boundary remains explicit.
