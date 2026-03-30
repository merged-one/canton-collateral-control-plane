# Proposal Readiness Assessment

## Purpose

This assessment states what the Canton Collateral Control Plane now proves on the pinned Quickstart runtime, what is backed by machine-readable evidence, what remains prototype scope, and what changed versus the earlier IDE-ledger-only prototype posture.

## What Is Real On Quickstart

The repository now proves these runtime-backed surfaces:

- the Control Plane DAR can be deployed into the pinned Quickstart `app-provider` and `app-user` participants
- one concrete reference token adapter path can consume a real `SettlementInstruction`, move `ReferenceTokenHolding`, emit a receipt, and expose provider-visible post-execution status
- confidential margin call runs end to end on Quickstart across policy evaluation, optimization, workflow preparation, adapter execution, and final execution reporting
- confidential substitution runs end to end on Quickstart across policy evaluation, replacement selection, workflow execution, adapter-driven incumbent release plus replacement movement, and final substitution reporting
- confidential return runs end to end on Quickstart across retained-set determination, workflow execution, adapter-driven release, provider-visible status refresh, approval-gated release proof, and replay-safe duplicate handling
- aggregate invariant evidence and final package indexing now consume those runtime-backed paths directly

## What Is Proven By Machine-Readable Evidence

The following artifacts are the primary machine-readable proof set:

- `reports/generated/localnet-control-plane-deployment-receipt.json`
- `reports/generated/localnet-reference-token-adapter-execution-report.json`
- `reports/generated/localnet-reference-token-adapter-status.json`
- `reports/generated/margin-call-quickstart-execution-report.json`
- `reports/generated/substitution-quickstart-report.json`
- `reports/generated/return-quickstart-report.json`
- `reports/generated/conformance-suite-report.json`
- `reports/generated/final-demo-pack.json`

Those artifacts prove, at minimum:

- pinned Quickstart commit and deployed package identity
- one concrete adapter receipt and provider-visible status path
- positive and blocked negative runtime scenarios for margin call, substitution, and return
- aggregate invariant pass or fail output across the runtime-backed path
- explicit indexing of the runtime evidence and the remaining staged boundary

## What Remains Prototype-Only

The current repository still does not prove:

- production-grade custodian, issuer, or settlement-network adapters beyond the narrow reference token path
- role-scoped disclosure profiles beyond the current workflow-party and provider-visible baseline
- workflow-coupled optimizer reservation and consent semantics
- production settlement-window enforcement, retry, and recovery semantics
- reference-data contracts for valuation, FX, issuer, and counterparty facts
- broader collateral business logic hardening beyond the current deterministic prototype scope

These items should be treated as staged roadmap scope, not as implied current capability.

## Technical Delta From The Earlier IDE-Ledger-Only Prototype

A fund reviewer should see four concrete changes:

1. The primary proof surface is no longer the IDE-ledger comparison path. The package now centers Quickstart deployment plus runtime-backed workflow and adapter evidence.
2. The repository now proves one concrete adapter seam with real machine-readable receipts and provider-visible status rather than stopping at workflow preparation.
3. The conformance suite now validates runtime-backed artifacts from Quickstart deployment, adapter execution, and the three confidential Quickstart demo flows.
4. The final demo pack now states explicitly what is real versus what remains staged, reducing the risk of over-reading the prototype as a production integration surface.

## Reviewer Recommendation

Reviewers should inspect the runtime artifacts in this order:

1. `reports/generated/proposal-submission-manifest.json`
2. `reports/generated/localnet-control-plane-deployment-receipt.json`
3. `reports/generated/localnet-reference-token-adapter-execution-report.json`
4. `reports/generated/localnet-reference-token-adapter-status.json`
5. `reports/generated/margin-call-quickstart-execution-report.json`
6. `reports/generated/substitution-quickstart-report.json`
7. `reports/generated/return-quickstart-report.json`
8. `reports/generated/conformance-suite-report.json`
9. `reports/generated/final-demo-pack.json`

That sequence shows the reviewer wrapper first, then the Quickstart deployment surface, the standalone adapter seam, the three workflow types, and finally the aggregate runtime package that ties them together.
