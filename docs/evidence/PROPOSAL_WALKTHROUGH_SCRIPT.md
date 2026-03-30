# Proposal Walkthrough Script

Target duration: 8-10 minutes.

This script is the repo-tracked reviewer walkthrough and live-demo script. Use the exact commit and artifact ids from `reports/generated/proposal-submission-manifest.json`.

## 1. Repo Posture

State that the Canton Collateral Control Plane is still a prototype, but it is no longer an IDE-ledger-only prototype. The current repo proves a Quickstart-backed deployment, one concrete adapter seam, three Quickstart-backed confidential workflow demos, and aggregate invariant evidence over those runtime-backed paths.

Show:

- `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md`
- `docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md`

## 2. One-Command Proof Path

Run:

```sh
make proposal-package
```

State that this command wraps `make demo-all`, which in turn wraps `make test-conformance`, so the reviewer package is anchored to the real Quickstart-backed runtime proof rather than a parallel narrative path.

Show:

- `reports/generated/proposal-submission-summary.md`
- `reports/generated/proposal-submission-manifest.json`

## 3. Concrete Adapter Seam

Explain that the reference token adapter consumes a real `SettlementInstruction`, moves the reference-token lots, emits a receipt, and returns control to Canton. The adapter does not decide policy, approvals, eligibility, or workflow state.

Show:

- `reports/generated/localnet-control-plane-deployment-receipt.json`
- `reports/generated/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/localnet-reference-token-adapter-status.json`

## 4. Quickstart Workflow Demos

Walk through the three confidential flows in this order:

1. margin call on Quickstart
2. substitution on Quickstart
3. return on Quickstart

For each flow, point out the positive runtime path, at least one blocked negative path, and the explicit note about what remains staged.

Show:

- `reports/generated/margin-call-quickstart-execution-report.json`
- `reports/generated/substitution-quickstart-report.json`
- `reports/generated/return-quickstart-report.json`

## 5. Aggregate Conformance Output

Explain that the conformance suite is now Quickstart-first and validates deployment proof, the reference adapter seam, and the three workflow reports together instead of treating Quickstart as sidecar evidence.

Show:

- `reports/generated/conformance-suite-report.json`
- `reports/generated/conformance-suite-summary.md`

## 6. Prototype Boundary And Close

End with the explicit boundary:

- real now: Quickstart deployment, one concrete adapter path, three Quickstart-backed workflows, aggregate invariant evidence
- still staged: production adapters, role-scoped disclosure profiles, workflow-coupled reservation, settlement-window semantics, reference-data contracts

Close by pointing the reviewer back to:

- `reports/generated/final-demo-pack.json`
- `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md`
- `docs/evidence/REVIEWER_START_HERE.md`
