# Proposal Submission Memo

Use `reports/generated/proposal-submission-manifest.json` for the exact commit, artifact ids, and proof ordering from the current submission run.

## What Is Real Now

The repository now proves a pinned Quickstart-backed Control Plane deployment, one concrete reference token adapter path, confidential margin call on Quickstart, confidential substitution on Quickstart, confidential return on Quickstart, and aggregate invariant output across those runtime-backed paths.

## What Machine Evidence Proves It

The primary machine-readable proof set is:

1. `reports/generated/localnet-control-plane-deployment-receipt.json`
2. `reports/generated/localnet-reference-token-adapter-execution-report.json`
3. `reports/generated/localnet-reference-token-adapter-status.json`
4. `reports/generated/margin-call-quickstart-execution-report.json`
5. `reports/generated/substitution-quickstart-report.json`
6. `reports/generated/return-quickstart-report.json`
7. `reports/generated/conformance-suite-report.json`
8. `reports/generated/final-demo-pack.json`
9. `reports/generated/proposal-submission-manifest.json`

## What Remains Prototype-Only

The repository still does not prove production-grade custodian, issuer, or settlement-network adapters beyond the narrow reference-token path; broader role-scoped disclosure profiles; workflow-coupled optimizer reservation and consent semantics; production settlement-window enforcement, retry, or recovery semantics; or richer reference-data contracts for valuation, FX, issuer, and counterparty facts.

Do not infer that the reference token adapter path is already a general production integration surface, that provider-visible proof implies final reviewer disclosure design, or that the current Quickstart runtime package already closes the remaining operational hardening work.

## What Changed Versus The Earlier IDE-Ledger-Only Prototype

The primary proof surface is no longer the IDE-ledger demo chain. Reviewers can now inspect a real Quickstart deployment, a real settlement-instruction-to-adapter seam, three Quickstart-backed confidential workflow reports, and one aggregate conformance report that validates runtime-backed artifacts rather than narrative-only or IDE-ledger-only flow packaging.

## How To Review The Package In 10-15 Minutes

Run `make proposal-package`, read `reports/generated/proposal-submission-summary.md`, then confirm the deployment receipt, adapter execution report, adapter status report, the three Quickstart workflow reports, `reports/generated/conformance-suite-report.json`, and finally `reports/generated/final-demo-pack.json`. Use `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md` if you want the same sequence as a walkthrough script for reviewer replay or live presentation.
