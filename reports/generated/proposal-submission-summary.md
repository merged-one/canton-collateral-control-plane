# Proposal Submission Summary

- Submission ID: `psp-8bc396964860907b`
- Command: `make proposal-package`
- Overall status: `PASS`
- Source commit: `a6b6a9cce50ad1e9c73c95eef10dd0fd386e620b`
- Worktree status at package build: `DIRTY`
- Final demo pack ID: `fdp-ad4246d5144c77eb`
- Conformance suite ID: `csr-d7e4b4c29646d5d4`
- Quickstart commit: `fe56d460af650b71b8e20098b3e76693397a8bf9`
- Deployed package ID: `2535dc1e6f8ab629482bc6c186334df1c79ab0fe5c59302d7bcb20f5a7c139fb`

## Reviewer Journey

| Step | Label | Path | Purpose |
| --- | --- | --- | --- |
| 1 | Reviewer start | `docs/evidence/REVIEWER_START_HERE.md` | Start with the shortest orientation path and the exact command surface. |
| 2 | Reviewer memo | `docs/evidence/PROPOSAL_SUBMISSION_MEMO.md` | Read the runtime-backed claims, staged scope, and technical delta in one place. |
| 3 | Quickstart deployment | `reports/generated/localnet-control-plane-deployment-receipt.json` | Confirm the pinned Quickstart commit, deployed DAR, and package identity. |
| 4 | Reference adapter | `reports/generated/localnet-reference-token-adapter-execution-report.json` | Verify the concrete settlement-instruction-to-adapter proof path. |
| 5 | Adapter status | `reports/generated/localnet-reference-token-adapter-status.json` | Confirm the provider-visible post-execution state after the adapter path ran. |
| 6 | Conformance | `reports/generated/conformance-suite-report.json` | Confirm the aggregate invariant pass or fail output for the Quickstart-backed proof set. |
| 7 | Quickstart demos | `reports/generated/final-demo-pack.json` | Use the final demo pack after conformance to inspect the margin-call, substitution, and return runtime paths together. |
| 8 | Walkthrough | `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md` | Use the repo-tracked walkthrough script for reviewer replay or live presentation. |

## Frozen Runtime Proof

- Runtime mode: `QUICKSTART`
- Reference adapter receipt status: `EXECUTED`
- Adapter movement lots: `quickstart-reference-token-lot-007, quickstart-reference-token-lot-008`

| Demo | Report ID | Command | Report |
| --- | --- | --- | --- |
| CONFIDENTIAL_MARGIN_CALL | `exr-9bc26ea5d960c241` | `make demo-margin-call-quickstart` | `reports/generated/margin-call-quickstart-execution-report.json` |
| CONFIDENTIAL_COLLATERAL_SUBSTITUTION | `srr-a8a9d213c0f6408a` | `make demo-substitution-quickstart` | `reports/generated/substitution-quickstart-report.json` |
| CONFIDENTIAL_MARGIN_RETURN | `rrr-163cdd5d84a09b71` | `make demo-return-quickstart` | `reports/generated/return-quickstart-report.json` |

## Real Vs Staged

### Real On Quickstart

- Pinned Quickstart deployment and DAR installation into app-provider and app-user participants.
- One concrete reference token adapter posting path with machine-readable execution and status evidence.
- Quickstart-backed confidential margin call, substitution, and return demo flows with real workflow-to-adapter handoff evidence.
- Aggregate invariant evidence across those runtime-backed demo paths through make test-conformance and make demo-all.

### Do Not Infer

- The reference token adapter path is not a generalized production custodian, issuer, or settlement-network integration surface.
- The current workflow-party and provider-visible evidence surfaces do not yet prove broader role-scoped disclosure profiles.
- Workflow-coupled optimizer reservation, settlement-window enforcement, retry and recovery semantics, and reference-data contracts remain staged roadmap scope.

## Walkthrough Package

- Walkthrough script: `docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md`
- Commands shown: `make proposal-package`
- Artifact order count: `10`

