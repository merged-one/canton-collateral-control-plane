# Repository Instructions

## Mandatory Startup Sequence

Before making any change in this repository:

1. Read this file.
2. Read [docs/mission-control/MASTER_TRACKER.md](./docs/mission-control/MASTER_TRACKER.md).
3. Read any more-specific `AGENTS.md` files in subdirectories you touch.
4. Update [docs/mission-control/WORKLOG.md](./docs/mission-control/WORKLOG.md) with a pre-change entry.

## Operating Rules

- Always read `AGENTS.md` and `docs/mission-control/MASTER_TRACKER.md` before making changes.
- Always update `WORKLOG.md` before and after changes.
- Every new feature must update `docs/invariants/INVARIANT_REGISTRY.md` and `docs/evidence/EVIDENCE_MANIFEST.md`.
- Every significant design decision must use an ADR in `docs/adrs/`.
- No fake demo outputs, reports, or placeholder success artifacts may appear in the main execution path.
- Prefer pinned dependencies, deterministic builds, reproducible demos, and explicit commands.
- Treat collateral policy, control, substitution, and release handling as safety-critical.
- Separate policy, optimization, workflow execution, and reporting concerns.
- Document how the system maps to central-bank style collateral frameworks, tri-party substitution workflows, and CCP-style concentration control.
- Use "Canton Collateral Control Plane" or "the Control Plane" in new documentation. The former name "Canton Collateral Policy & Optimization Engine" and `C-COPE` are deprecated historical aliases only.
- Every task must leave behind at least one reproducible command.

## Change Expectations

- Documentation-first is the default until the tracker explicitly authorizes the next implementation phase.
- If a change affects behavior, add or update the corresponding invariant entry.
- If a change affects risk, update the risk register and threat model as needed.
- If a change affects operations, update runbooks or note why a runbook is still pending.
- If a change affects interfaces or architecture, add an ADR or explicitly explain why one is not needed.

## Definition Of Done

A task is not done until all applicable items are complete:

- scope reflected in mission-control documents
- worklog updated before and after the task
- invariants and evidence updated where applicable
- reproducible commands recorded
- relevant checks executed and results captured
- no unrelated business logic or placeholder artifacts introduced

## Current Repo Posture

- This repository is in a documentation-and-controls, runtime-foundation, initial policy-engine, initial optimization-engine, and initial Daml workflow-skeleton phase.
- The first Daml contract boundary now exists for obligations, posting, substitution, return, settlement intent, and execution reporting.
- A first deterministic `CPL v0.1` policy evaluation engine now exists for eligibility, haircut, lendable-value, concentration, control, and wrong-way-risk reporting against normalized inventory inputs.
- A first deterministic optimizer now exists for best-to-post, substitution recommendation, concentration-aware allocation, and explanation-trace reporting against normalized obligation inputs.
- A first end-to-end margin-call demo now exists under `make demo-margin-call`, generating a machine-readable execution report plus Markdown summary and timeline artifacts from real policy, optimization, and Daml workflow execution.
- A first Quickstart-backed end-to-end margin-call demo now exists under `make demo-margin-call-quickstart`, generating a machine-readable execution report plus Markdown summary and timeline artifacts from real policy, optimization, Quickstart workflow execution, and reference token adapter execution.
- A first end-to-end return demo now exists under `make demo-return`, generating a machine-readable return report plus Markdown summary and timeline artifacts from real policy, optimization, and Daml workflow execution.
- A first Quickstart-backed end-to-end return demo now exists under `make demo-return-quickstart`, generating a machine-readable return report plus Markdown summary and timeline artifacts from real policy, optimization, Quickstart workflow execution, reference token adapter release execution, and provider-visible status evidence.
- A first end-to-end substitution demo now exists under `make demo-substitution`, generating a machine-readable substitution report plus Markdown summary and timeline artifacts from real policy, optimization, and Daml workflow execution.
- A first Quickstart-backed end-to-end substitution demo now exists under `make demo-substitution-quickstart`, generating a machine-readable substitution report plus Markdown summary and timeline artifacts from real policy, optimization, Quickstart workflow execution, reference token adapter replacement or release execution, and provider-visible status evidence.
- A first aggregate conformance suite now exists under `make test-conformance`, refreshing Quickstart deployment evidence, one standalone reference token adapter path, and explicit invariant pass/fail output across the Quickstart-backed margin-call, substitution, and return demos plus supporting determinism and haircut evidence.
- A first final demo pack now exists under `make demo-all`, generating a machine-readable package index plus Markdown summary for the Quickstart-backed confidential workflow demo surface with explicit real-versus-staged readiness notes.
- A first proposal submission package now exists under `make proposal-package`, generating a machine-readable proposal manifest plus Markdown summary that wrap the Quickstart-backed final demo pack with reviewer-start, memo, and walkthrough surfaces.
- A pinned CN Quickstart bootstrap, containerized Quickstart-DAR bridge build, isolated overlay start path, package-deployment command, seeded confidential collateral scenario, Quickstart status-evidence surface, and first reference token adapter path now exist under `infra/quickstart/` plus `scripts/`.
- Production-grade asset adapters, settlement-window enforcement, workflow-coupled optimizer reservation, and production-grade collateral business logic remain intentionally absent.
- Reproducible control commands now include `make bootstrap`, `make localnet-bootstrap`, `make localnet-smoke`, `make localnet-build-dar`, `make localnet-deploy-dar`, `make localnet-start-control-plane`, `make localnet-seed-demo`, `make localnet-status-control-plane`, `make localnet-run-token-adapter`, `make localnet-adapter-status`, `make validate-cpl`, `make policy-eval`, `make optimize`, `make test-policy-engine`, `make test-optimizer`, `make test-conformance`, `make daml-build`, `make daml-test`, `make demo-run`, `make demo-margin-call`, `make demo-margin-call-quickstart`, `make demo-return`, `make demo-return-quickstart`, `make demo-substitution`, `make demo-substitution-quickstart`, `make demo-all`, `make proposal-package`, `make status`, `make verify-portable`, and `make verify`.
