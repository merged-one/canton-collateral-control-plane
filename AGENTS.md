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

- This repository is in a documentation-and-controls plus runtime-foundation phase.
- Collateral business logic is still intentionally absent.
- Reproducible control commands now include `make bootstrap`, `make validate-cpl`, `make daml-build`, `make demo-run`, `make status`, and `make verify`.
