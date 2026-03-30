# Reviewer Start Here

Use this path if you want the shortest technically correct review of the Canton Collateral Control Plane proposal package.

## Primary Command

```sh
make proposal-package
```

That command refreshes the Quickstart-backed runtime proof through `make demo-all` and then writes:

- `reports/generated/proposal-submission-manifest.json`
- `reports/generated/proposal-submission-summary.md`

## Review Order

1. Read `reports/generated/proposal-submission-summary.md`.
2. Read `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md`.
3. Confirm the Quickstart deployment and adapter seam:
   - `reports/generated/localnet-control-plane-deployment-receipt.json`
   - `reports/generated/localnet-reference-token-adapter-execution-report.json`
   - `reports/generated/localnet-reference-token-adapter-status.json`
4. Inspect the three Quickstart workflow reports:
   - `reports/generated/margin-call-quickstart-execution-report.json`
   - `reports/generated/substitution-quickstart-report.json`
   - `reports/generated/return-quickstart-report.json`
5. Inspect `reports/generated/conformance-suite-report.json`.
6. Inspect `reports/generated/final-demo-pack.json`.
7. Use `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md` if you want the same story as a walkthrough script for reviewer replay or live presentation.

## Review Boundary

The package proves one Quickstart-backed deployment, one concrete reference token adapter path, and three Quickstart-backed confidential workflow demos. It does not prove production-grade custodian integrations, role-scoped disclosure profiles, workflow-coupled reservation, settlement-window enforcement, or broader reference-data contracts.
