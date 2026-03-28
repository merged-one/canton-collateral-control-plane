# Daml Test Plan

## Purpose

This plan defines the first executable checks for the Daml package boundary under `daml/CantonCollateral/`.

## Reproducible Commands

```sh
make daml-build
make daml-test
make demo-run
make demo-margin-call
make demo-substitution
```

## Script Coverage

| Script | Scope | Invariants touched |
| --- | --- | --- |
| `CantonCollateral.Test:marginCallLifecycleTest` | margin call creation, approval gating, execution-report emission | `AUTH-001`, `WF-001`, `REPT-001`, `AUD-001` |
| `CantonCollateral.Test:postingAndSubstitutionLifecycleTest` | posting intent, approval routing, settlement, substitution approval, substitution rejection, encumbrance replacement | `CTRL-001`, `ENC-001`, `ATOM-001`, `WF-001`, `REPT-001` |
| `CantonCollateral.Test:returnLifecycleTest` | return request approval and settlement-confirmed release path | `CTRL-001`, `ATOM-001`, `WF-001`, `REPT-001` |
| `CantonCollateral.Demo:marginCallDemoWorkflow` | parameterized positive margin-call issuance and posting path driven by optimizer-selected lots | `WF-001`, `REPT-001`, `AUD-001` |
| `CantonCollateral.Demo:substitutionDemoWorkflow` | parameterized substitution path from existing encumbrances through approval-gated atomic replacement or deterministic control failure | `CTRL-001`, `ATOM-001`, `WF-001`, `REPT-001`, `EXCP-001` |
| `Bootstrap:workflowSmokeTest` | aggregate smoke run over the three lifecycle scripts | command-surface validation and operator reproducibility |

## Positive Paths

- margin call creation reaches `Closed` only after issuance or explicit approval
- posting creates an explicit `SettlementInstruction` before encumbrances are committed
- substitution archives released encumbrances and creates replacement encumbrances only when settlement is confirmed
- return workflow releases encumbrances only after return settlement confirmation
- the end-to-end margin-call demo passes optimizer-selected lots into a Daml Script and records both the issued call and the settled posting path
- the end-to-end substitution demo starts from currently encumbered lots, applies optimizer-selected replacements, and records only a fully approved atomic replacement path as committed

## Negative Paths

- posting can be rejected by secured party or custodian before settlement
- substitution can be rejected without mutating the currently pledged encumbrance set
- settlement exception choices keep the workflow in `ExceptionOpen` rather than fabricating success
- `make demo-margin-call` now covers the operator-facing negative paths for ineligible collateral, insufficient lendable value, and an expired policy window before the Daml workflow step is invoked
- `make demo-substitution` now covers operator-facing negative paths for replacement ineligibility, concentration-blocked replacement, unauthorized release attempts, and attempted partial settlement when atomicity is required

## Current Limits

- the scripts use pinned policy references, not a live policy engine
- the parameterized margin-call demo uses the Daml IDE ledger rather than the pinned Quickstart LocalNet
- privacy is checked structurally through stakeholder choices and query scope, not yet through a full disclosure-profile suite
- replay, Daml-enforced expiry, and fuller concentration-limit workflow coverage remain future work
