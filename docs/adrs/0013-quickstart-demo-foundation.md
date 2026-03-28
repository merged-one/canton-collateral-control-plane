# ADR 0013: Establish A Pinned Quickstart Demo Foundation

- Status: Accepted
- Date: 2026-03-28

## Context

The repository now has a pinned repo-local Daml runtime foundation, an initial workflow skeleton, a deterministic policy engine, and a deterministic optimizer. It still lacks a credible Quickstart-backed LocalNet path for later confidential collateral demos.

The upstream CN Quickstart currently exposes a modular `quickstart/` project with a `Makefile`-driven workflow, Docker Compose layering, `.env.local` profile configuration, and a documented development path centered on `make setup`, `make build`, `make start`, and `make status`. As of 2026-03-28, the repo pin chosen for this foundation is commit `fe56d460af650b71b8e20098b3e76693397a8bf9`, whose upstream `.env` records `DAML_RUNTIME_VERSION=3.4.10`, `SPLICE_VERSION=0.5.3`, and `JAVA_VERSION=21-jdk`.

That upstream runtime line does not yet match this repository's current Daml SDK `2.10.4` package boundary. The foundation therefore needs to get the repo closer to a real LocalNet demo without pretending that the package bridge or asset-adapter integration is already solved.

## Decision

The repository will adopt a pinned, overlay-first Quickstart demo foundation.

Specific decisions:

1. The Quickstart LocalNet source will be staged as a detached upstream checkout under `.runtime/localnet/cn-quickstart`, pinned by full commit SHA in `infra/quickstart/overlay/upstream-pin.env`.
2. Repo-owned runtime customization will use `.env.local` overlay templates and adjacent scripts before any upstream fork is considered.
3. The repository will expose `make localnet-bootstrap` to stage the pinned checkout and write `.env.local`, and `make localnet-smoke` to run upstream Docker preflight plus `docker compose ... config`.
4. The LocalNet startup workflow will stay with upstream Quickstart commands: `make check-docker`, `make build`, `make start`, and `make status` from the staged `quickstart/` directory.
5. The repository will not claim Control Plane DAR deployment, seed data, token movement, or asset-adapter execution until the Daml runtime bridge and adapter contracts are pinned explicitly.
6. Any future Quickstart fork remains exceptional and must satisfy the existing overlay-first criteria documented in the integration plans.

## Consequences

Positive:

- the repo now has a real, pinned Quickstart foundation instead of only prose plans
- the runtime delta from upstream is narrow and reviewable
- operator guidance can point to exact commands and an exact upstream commit
- later demo prompts can focus on package bridge, seed data, and adapters rather than starting from scratch

Tradeoffs:

- `make verify` now includes a network-backed Quickstart preflight in addition to the repo-local bootstrap and Daml checks
- the LocalNet foundation stops at compose validation rather than full start or DAR deployment
- the repo now carries an explicit version-skew risk between its current Daml package and the pinned Quickstart runtime line

These tradeoffs are accepted because the repository needs a credible, upstream-aligned LocalNet foundation now, but it must not fabricate a confidential collateral demo before the runtime bridge and asset interfaces are real.
