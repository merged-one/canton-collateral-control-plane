# Roadmap

This roadmap currently reflects the 2026-03-28 development-fund proposal. If the proposal changes, update this roadmap through the mission-control process and ADRs.

The roadmap describes the build-out of the Control Plane subsystems plus the adjacent data-plane integrations they depend on. The rename to "Canton Collateral Control Plane" is a clarification of the existing architecture, not a change in business direction.

Current staging note:
The repository now has a pinned Quickstart bootstrap and compose-preflight foundation plus a first IDE-ledger-backed end-to-end margin-call demo, but the remaining roadmap still applies because the Control Plane DAR is not yet deployed into Quickstart and no live asset adapter exists yet.

## Phase 0: Mission Control Spine

Objective:
Establish repository governance, control documents, and traceability before adding business logic.

Exit criteria:

- core documentation spine exists
- ADR baseline exists
- invariant, risk, and evidence registries exist
- lightweight verification commands succeed

## Milestone 1 / Phase 1: Collateral Policy Language, Formal Model, And Runtime Foundation

Objective:
Define the reusable Collateral Policy Language and formal model that future control-plane subsystems and data-plane adapters will consume.

Expected outputs:

- `CPL v0.1` specification
- schema for eligibility, haircuts, concentration limits, encumbrance state, substitution rights, and release control
- formal invariant catalog
- architecture and data-model documentation
- sample policy profiles for bilateral, tri-party, CCP-style, and central-bank-style usage
- pinned local Daml and Java runtime foundation with reproducible bootstrap and smoke-run commands

Acceptance focus:

- at least 12 named invariants
- at least one traceability example from spec to scenario
- policy profiles published for the four target usage patterns

## Milestone 2 / Phase 2: Policy Engine And Asset Adapters

Objective:
Build the deterministic policy engine and the first data-plane asset adapters against the pinned LocalNet and asset standards.

Expected outputs:

- deterministic policy engine
- haircut and lendable-value calculator
- concentration-limit evaluator
- token-standard-style asset adapter
- reference adapters for Quickstart-based assets and Daml Finance-style assets
- machine-readable policy evaluation reports

Acceptance focus:

- eligibility and lendable value are reproducible
- policy failures are explained explicitly
- token-standard-style assets can be evaluated by the engine

## Milestone 3 / Phase 3: Optimization And Substitution Engine

Objective:
Add deterministic optimization and substitution logic on top of the policy layer.

Expected outputs:

- best-to-post and cheapest-to-deliver optimizer
- substitution engine
- pre-positioned versus mobilizable inventory logic
- concentration-aware multi-obligation allocation
- deterministic explanation traces for optimizer decisions

Acceptance focus:

- optimizer outputs are deterministic under documented assumptions
- substitution respects policy, encumbrance state, and concentration limits
- explanation traces justify asset choices

## Milestone 4 / Phase 4: Atomic Collateral Workflows And Conformance Suite

Objective:
Implement the first end-to-end Daml workflow library and prove it with a conformance suite.

Expected outputs:

- Daml workflows for margin call, margin return, substitution, and close-out transfer
- atomic multi-leg execution against a real Canton reference environment
- conformance suite and invariant reports
- negative-path scenarios for ineligible assets, expired calls, insufficient lendable value, concentration breaches, unauthorized release, and replayed instructions

Acceptance focus:

- end-to-end workflows execute on a real Canton-based environment
- atomicity holds across supported legs
- negative paths fail cleanly and reproducibly
- invariant reports are generated from real execution

## Milestone 5 / Phase 5: Public Release, Demo Environment, And Adoption Package

Objective:
Package the reference stack for external adopters with a runnable demo and integration guidance.

Expected outputs:

- public release
- Quickstart-based demo environment
- maintainer, operator, and integration documentation
- reference machine-readable and human-readable reports
- recorded walkthrough
- adoption guidance for venues, custodians, financing apps, treasury desks, and collateral-service providers

Acceptance focus:

- a third party can run the demo from documented commands
- at least two sample policy profiles and two sample execution reports are published
- integration guidance is concrete enough for external adopters
