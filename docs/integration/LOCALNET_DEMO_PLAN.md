# LocalNet Demo Plan

## Objective

Turn the current repository into a real confidential-collateral demo on top of an upstream CN Quickstart LocalNet without collapsing policy, optimization, workflow authority, or reporting boundaries.

## Current Implemented Layer

The repository now implements Stage 0, Stage 1, Stage 2, Stage 3, and the posting-focused portion of Stage 4:

- pinned upstream CN Quickstart checkout at commit `fe56d460af650b71b8e20098b3e76693397a8bf9`
- repo-owned `.env.local` overlay profiles under `infra/quickstart/overlay/`
- reproducible bootstrap through `make localnet-bootstrap`
- reproducible compose-preflight smoke through `make localnet-smoke`
- reproducible Quickstart-compatible DAR build through `make localnet-build-dar`
- reproducible package installation into a running pinned Quickstart LocalNet through `make localnet-deploy-dar`
- reproducible isolated overlay start through `make localnet-start-control-plane`
- reproducible scenario seeding through `make localnet-seed-demo`
- reproducible Quickstart status evidence through `make localnet-status-control-plane`
- reproducible Quickstart margin-call workflow handoff through `make localnet-run-margin-call-workflow`
- reproducible Quickstart-backed reference token adapter execution through `make localnet-run-token-adapter`
- reproducible Quickstart-backed end-to-end margin-call orchestration through `make demo-margin-call-quickstart`
- documented operator path that can still stay with upstream `make check-docker`, `make build`, `make start`, and `make status` when direct upstream debugging is needed

This prompt does not yet:

- execute substitution or return through the same Quickstart-backed chain
- expose role-scoped report profiles on top of the current workflow-party and provider-visible baseline
- provide broader custodian or issuer adapters beyond the reference token posting path

## Staged Delivery

### Stage 0: Pinned Foundation

Status: implemented in this prompt

- pin one upstream Quickstart commit and record the observed upstream runtime versions
- keep the upstream tree detached and unmodified
- express repo intent through `.env.local` overlays and adjacent scripts
- validate the composed stack before claiming a runnable confidential demo

### Stage 1: Upstream LocalNet Bring-Up

Status: implemented through a repo-owned overlay wrapper while the upstream path remains available for debugging

- run `make check-docker`, `make build`, `make start`, and `make status` inside the staged upstream `quickstart/` directory
- verify the LocalNet validators and supporting services are healthy
- preserve upstream logs, Daml Shell, and observability workflows so later debugging stays aligned with the Quickstart ecosystem

### Stage 2: Control Plane Package Bridge

Status: implemented

- keep the repo-default host toolchain on Daml `2.10.4` while building Quickstart-compatible DARs through a containerized Daml `3.4.10` plus Java `21` bridge
- preserve one shared Control Plane Daml source tree rather than splitting into host-only and Quickstart-only package variants
- upload the Control Plane DAR into the running app-provider and app-user participants through the upstream onboarding container

### Stage 3: Confidential Collateral Seed Scenario

Status: implemented through seeded state plus posting-focused workflow execution

- seed a minimal but real scenario covering collateral provider, secured party, custodian, and optional operator roles
- load one obligation, provider inventory provenance, and one posting intent without bypassing workflow authority
- capture ledger-returned contract identifiers and provider-visible status from committed Canton state
- emit the first Quickstart-backed `ExecutionReport` and settlement-intent trace for the margin-call posting path
- prove a blocked workflow gate that does not trigger adapter movement

### Stage 4: Cross-App Demo Extensions

Status: reference posting-path implementation complete; broader extensions deferred

- attach one token-standard-style issuer or wallet path
- attach one custodian or control adapter path
- optionally expose venue or financing-app callbacks once settlement instruction contracts are pinned

## Assumptions, Mocked Surfaces, And Deferrals

| Area | Assumed Or Mocked | Why |
| --- | --- | --- |
| Quickstart topology | upstream CN Quickstart modular Docker Compose stack | stay close to supported workflows and reduce repo-owned runtime code |
| Auth path | OAuth2 remains the default overlay choice | keeps the future confidential demo close to the upstream security posture |
| Observability | optional in `lean`, enabled in `faithful` | preserve a lightweight preflight while keeping a higher-fidelity path available |
| LocalNet start | real repo-owned wrapper over the upstream compose stack | keeps upstream runtime ownership explicit while giving the repository a reproducible startup command |
| Control Plane package load | real | the repo now builds and uploads a Quickstart-compatible DAR through the documented bridge |
| Confidential seed state | real | the repo now allocates scenario roles, seeds real contracts, and captures provider-visible status on Quickstart |
| Asset movement | real for the reference token posting path, deferred for broader flows | the repository now proves one narrow adapter path without claiming a complete custodian or issuer integration surface |

## Integration Hooks For Other Canton Projects

| Integrator | Future Hook |
| --- | --- |
| venues | consume approved `SettlementInstruction` artifacts and return venue-specific execution status callbacks |
| financing apps | call policy evaluation, optimization, and workflow proposal boundaries without owning settlement authority |
| token issuers | expose token, balance, control, and transfer surfaces through the planned asset-adapter contract |
| custodians | map custody-account control, hold, and release semantics into `EncumbranceState` and settlement callback updates |
| margining applications | drive obligation issuance and workflow consent while reusing the shared policy and optimization layers |

## Reproducible Commands

From the repository root:

```sh
make localnet-bootstrap
make localnet-smoke
make localnet-build-dar
make localnet-deploy-dar
make localnet-start-control-plane
make localnet-seed-demo
make localnet-status-control-plane
make localnet-run-margin-call-workflow
make localnet-run-token-adapter
make localnet-adapter-status
make demo-margin-call-quickstart
```

From the staged upstream checkout after bootstrap:

```sh
cd .runtime/localnet/cn-quickstart/quickstart
make check-docker
make build
make start
make status
```

## Exit Criteria For A Real Confidential Demo

- the upstream Quickstart stack starts reproducibly from the pinned checkout
- the Control Plane DAR is deployed through a documented version-bridge path
- at least one confidential collateral scenario is seeded and inspectable on Quickstart
- at least one token-standard-style asset path can be loaded through a real adapter
- at least one collateral posting or substitution scenario emits a real machine-readable `ExecutionReport`
- at least one negative path proves the adapter does not move collateral when policy or workflow gates fail
- all assumptions, mocks, and deferred surfaces remain explicit in operator documentation
