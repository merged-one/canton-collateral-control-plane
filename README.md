# Canton Collateral Policy Optimization Engine (C-COPE)

## What this prototype is

This repository is a documentation-first prototype for C-COPE, an open-source reference standard and execution engine for collateral policy and optimization on Canton. The target system is a reusable collateral control plane for:

- collateral eligibility evaluation
- haircut and lendable-value calculation
- concentration-limit monitoring
- encumbrance and release control
- substitution and allocation
- pre-positioning and mobilization
- atomic collateral movement across workflows
- machine-readable collateral decision and execution reporting

The intended runtime shape is a Quickstart-based LocalNet with token-standard-style assets, reference Daml workflows, and auditable reports that can be checked against invariants, evidence, and tests.

Current framing note:
This repository now reflects the development-fund proposal dated 2026-03-28. If the proposal changes later, repository-level assumptions should be revised through the mission-control process and ADRs.

## Why documentation-first

Collateral policy, control, substitution, allocation, and release handling are safety-critical. Before business logic exists, this repository establishes the operating rules needed to build the prototype safely:

- requirements must trace to invariants, evidence, and tests
- significant design choices must be captured as ADRs
- changes must leave behind reproducible commands
- demos must be reproducible and must not contain fake success artifacts

This order of work is deliberate. C-COPE spans policy, optimization, workflow, and reporting layers across multiple future apps, so undocumented assumptions would create defects at the control-plane boundary, not just in one app.

## Target High-Level Architecture

The target architecture follows the five-layer reference stack from the proposal while preserving explicit reporting and evidence boundaries:

1. Collateral Policy Language (CPL)
   Versioned policy schema for eligibility, haircuting, concentration, control, substitution rights, and settlement conditions.
2. Policy Engine
   Deterministic evaluation of eligibility, lendable value, policy failures, and release conditions.
3. Optimization Engine
   Best-to-post, cheapest-to-deliver, substitution, and concentration-aware allocation with explanation traces.
4. Workflow Library
   Reference Daml workflows for margin call, delivery, substitution, return, close-out, and exception handling.
5. Conformance Suite
   Invariant catalog, scenario runner, and report-validation layer that proves actual behavior and report fidelity.

Machine-readable reporting remains a separate concern across the policy, optimization, workflow, and conformance layers. Reports should explain both why a decision was made and what actually executed.

This maps to established practice:

- central-bank collateral frameworks separate eligibility, valuation, haircuting, control, pre-positioning, and settlement concerns
- tri-party collateral utilities manage selection, valuation, substitution, and operational coordination
- CCP-style controls apply conservative haircuts, concentration limits, and explicit exception handling
- Canton provides privacy-preserving, party-specific, atomic workflows across multiple parties and applications

## Scope

Current scope:

- repository governance and operating rules
- mission-control documents and decision tracking
- proposal-aligned architecture, milestone, invariant, and evidence structure
- `CPL v0.1` prose specification, JSON Schema, validation plan, and example policy set
- pinned runtime foundation for Daml-centric workflow modeling and local verification
- implementation-ready planning for CPL, policy-engine, optimization, workflow, and conformance phases
- reusable framing for margin, repo, securities-lending, treasury, and collateral-mobility workflows

## Non-Goals

Current non-goals:

- becoming a CCP, custodian, central-bank facility, price-oracle business, or legal-document platform
- replacing venue-specific, repo-specific, or derivatives-specific applications
- production-ready economic calibration
- live integrations with custodians, CCPs, central-bank systems, or external pricing stacks
- UI development
- performance tuning
- implementation of collateral business logic in this phase

## Mission Control

Mission control is the repository's operating spine. Start here:

- [AGENTS.md](./AGENTS.md)
- [docs/mission-control/MASTER_TRACKER.md](./docs/mission-control/MASTER_TRACKER.md)
- [docs/mission-control/WORKLOG.md](./docs/mission-control/WORKLOG.md)
- [docs/invariants/INVARIANT_REGISTRY.md](./docs/invariants/INVARIANT_REGISTRY.md)
- [docs/evidence/EVIDENCE_MANIFEST.md](./docs/evidence/EVIDENCE_MANIFEST.md)

Working rules:

- read `AGENTS.md` and `MASTER_TRACKER.md` before making changes
- update `WORKLOG.md` before and after each task
- update invariants and evidence for every new feature
- record significant design choices as ADRs

Reproducible commands today:

```sh
make bootstrap
make validate-cpl
make daml-build
make demo-run
make status
make docs-lint
make verify
```

`make demo-run` currently exercises a minimal Daml runtime-foundation smoke test. It proves the pinned toolchain and package layout work without claiming collateral workflow semantics yet.

Current CPL artifacts:

- [docs/specs/CPL_SPEC_v0_1.md](./docs/specs/CPL_SPEC_v0_1.md)
- [docs/specs/CPL_EXAMPLES.md](./docs/specs/CPL_EXAMPLES.md)
- [schema/cpl.schema.json](./schema/cpl.schema.json)
- [docs/testing/CPL_VALIDATION_TEST_PLAN.md](./docs/testing/CPL_VALIDATION_TEST_PLAN.md)
- [docs/setup/LOCAL_DEV_SETUP.md](./docs/setup/LOCAL_DEV_SETUP.md)
- [docs/setup/DEPENDENCY_POLICY.md](./docs/setup/DEPENDENCY_POLICY.md)

## Upcoming Phases

- Phase 0: documentation and mission-control spine
- Milestone 1 / Phase 1: Collateral Policy Language and formal model
- Milestone 2 / Phase 2: Policy engine and asset adapters
- Milestone 3 / Phase 3: Optimization and substitution engine
- Milestone 4 / Phase 4: Atomic collateral workflows and conformance suite
- Milestone 5 / Phase 5: Public release, demo environment, and adoption package
