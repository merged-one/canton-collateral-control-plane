# Master Tracker

Last Updated: 2026-03-29
Current Phase: Milestone 5 / Phase 5 - Final Conformance And Demo Package

## Mission

Stand up a documentation-first Canton Collateral Control Plane repository: a neutral Canton collateral control-plane prototype that can safely evolve into reusable policy, optimization, workflow, conformance, and reporting components for margin, repo, securities-lending, treasury, collateral mobility, and close-out workflows.

Repository identity note:
The repository's active user-facing name is "Canton Collateral Control Plane". The former name "Canton Collateral Policy & Optimization Engine" is retained only as a deprecated historical alias for continuity in older records, and `C-COPE` should not be used in new documentation.

## Scope

- define repository governance, change control, and contribution rules
- establish proposal-aligned architecture, invariant, risk, evidence, and testing scaffolding
- prepare for a pinned Quickstart-based LocalNet, token-standard-style asset model, and Daml workflow baseline
- shape the repo around a reusable collateral policy language, optimizer, workflow library, and conformance suite
- provide an auditable control spine for future implementation phases

## Non-Goals

- shipping production-grade business logic in this phase
- claiming validated economics or regulatory compliance
- integrating with live custodians, CCPs, or central-bank platforms
- becoming a venue, CCP, custodian, price-oracle business, or legal-document system
- generating demo outputs without executable backing

## Architectural Pillars

1. Neutral collateral control-plane design reusable across multiple Canton apps.
2. Versioned Collateral Policy Language for eligibility, haircuting, concentration, control, and substitution rights.
3. Deterministic policy evaluation and optimization with explanation traces.
4. Atomic multi-party workflow execution and control semantics on Canton.
5. Conformance, reporting, and auditability as first-class outputs.
6. Documentation, evidence, and test traceability from the start.

## Current Phase

Milestone 5 / Phase 5 now packages the existing policy, optimization, workflow, reporting, and first data-plane reference-adapter layers into one reproducible proposal-ready surface. The expected output is a reproducible conformance suite and final demo pack plus one concrete Quickstart-backed workflow-execution and adapter path that consume declared scenario inputs, emit machine-readable evidence, prove positive plus negative paths, expose invariant pass or fail output, and document the third-party integration boundary without pretending production-grade external integration is complete.

Prompt 1 status:

- documentation spine created
- baseline verification commands added
- repository remains intentionally free of business logic pending pinned dependency and interface decisions

Proposal alignment status:

- repository framing updated to the current control-plane model
- roadmap now mirrors the proposal milestone structure
- invariants expanded toward the proposal's conformance-suite acceptance criteria
- future proposal changes should be incorporated through ADRs rather than informal drift

Repository identity status:

- rename clarified that policy, optimization, workflow orchestration, conformance, and reporting are subsystems of one shared collateral control plane
- control-plane responsibilities remain distinct from data-plane assets, ledger state, settlement rails, and LocalNet execution
- subsystem names remain intact; only user-facing identity and safe in-repo metadata were updated

Prompt 2 status:

- architecture boundaries defined for policy, evaluation, optimization, workflow, reporting, and runtime infrastructure
- collateral domain model, actor model, and lifecycle states documented
- Quickstart integration and token-standard alignment assumptions documented for future implementation
- repository remains documentation-only pending pinned dependencies, schema design, and package boundaries

Prompt 3 status:

- `CPL v0.1` prose specification published under `docs/specs/`
- machine-readable JSON Schema published at `schema/cpl.schema.json`
- example central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style policies published and validated
- `make validate-cpl` added as a reproducible repository control command
- repository remains implementation-light: policy engine, optimization engine, workflow packages, and report schemas are still pending

Prompt 4 status:

- Daml runtime foundation pinned to Daml SDK `2.10.4`, Canton `2.10.4`, and Temurin JDK `17.0.18+8`
- repo-local bootstrap, status, build, demo, portable-verify, and full-verify commands published under `Makefile` and `scripts/`
- minimal executable Daml package added under `daml/` to prove compile-and-run readiness without collateral business logic
- future service-layer code now has reserved `app/`, `reports/`, `test/`, `examples/`, and `infra/` surfaces

Prompt 5 status:

- first Daml contract boundary added under `daml/CantonCollateral/` for roles, assets, inventory, encumbrance, obligations, posting, substitution, return, settlement instructions, and execution reporting
- lifecycle skeletons now cover margin call issuance, collateral posting intent, substitution approval and rejection, margin return request, and settlement confirmation or exception paths
- `make daml-test` and `Bootstrap:workflowSmokeTest` now provide executable lifecycle checks against the pinned SDK
- policy evaluation, optimization, report disclosure profiles, and external asset-adapter integrations remain separate future layers

Prompt 6 status:

- first deterministic `CPL v0.1` policy evaluation engine added under `app/policy-engine/`
- engine now evaluates eligibility, haircut, lendable value, concentration, encumbrance, segregation, settlement-currency mismatch, and wrong-way-risk outcomes against normalized candidate inventory
- machine-readable `PolicyEvaluationReport` contract published under `reports/schemas/` with spec, ADR, test plan, and generated example artifact
- `make policy-eval` and `make test-policy-engine` now provide reproducible policy-engine evaluation and test commands
- role-scoped `ExecutionReport` disclosure profiles, live asset adapters, and reference-data contracts remain future layers

Prompt 7 status:

- first deterministic optimizer added under `app/optimizer/` for best-to-post selection, substitution recommendation, concentration-aware allocation, and deterministic explanation traces
- machine-readable `OptimizationReport` contract published under `reports/schemas/` with spec, ADR, economic rationale, test plan, and generated example artifact
- `make optimize` and `make test-optimizer` now provide reproducible optimization and optimizer-test commands
- optimization remains advisory and off-ledger; workflow reservation, consent, and settlement authority remain future Canton-layer work

Prompt 8 status:

- pinned CN Quickstart LocalNet foundation added under `infra/quickstart/` with commit-based upstream pinning, overlay profiles, and operator documentation
- `make localnet-bootstrap` now stages the upstream checkout and writes a repo-owned `.env.local` overlay without modifying tracked upstream files
- `make localnet-smoke` now reuses upstream Docker preflight checks and validates the composed Quickstart stack as the earliest real runnable LocalNet layer
- LocalNet startup, token-standard-style assets, and confidential collateral seed data remain staged follow-on work; the later runtime bridge work now closes the Control Plane DAR build and install path without forking upstream Quickstart

Prompt 9 status:

- first end-to-end margin-call demo added under `app/orchestration/` and `examples/demo-scenarios/margin-call/`
- `make demo-margin-call` now evaluates positive and negative margin-call scenarios, runs the positive Daml workflow path, and emits a machine-readable `ExecutionReport` plus Markdown summary and timeline artifacts
- the demo now covers negative paths for ineligible collateral, insufficient lendable value, and an expired policy window without fabricating workflow success on blocked cases
- the prototype still runs the positive workflow path on the Daml IDE ledger; Quickstart-backed package deployment and role-scoped report disclosure remain staged follow-on work

Prompt 10 status:

- first end-to-end substitution prototype added under `app/orchestration/` and `examples/demo-scenarios/substitution/`
- `make demo-substitution` now starts from existing encumbered collateral, runs substitution-specific positive and negative scenarios, invokes a parameterized Daml substitution workflow path, and emits a machine-readable `SubstitutionReport` plus Markdown summary and timeline artifacts
- the prototype now proves optimizer-scoped replacement, approval-gated release, unauthorized-release blocking, and atomic all-or-nothing substitution handling without fabricating success on blocked cases
- the substitution workflow still runs on the Daml IDE ledger; Quickstart-backed deployment and role-scoped report disclosure remain staged follow-on work

Prompt 11 status:

- first end-to-end return prototype added under `app/orchestration/` and `examples/demo-scenarios/return/`
- `make demo-return` now starts from existing encumbered collateral, runs retained-set optimization to derive the released lots, invokes a parameterized Daml return workflow path, and emits a machine-readable `ReturnReport` plus Markdown summary and timeline artifacts
- the prototype now proves approval-gated release, replay-safe return identifiers, obligation-state mismatch blocking, and settlement-driven encumbrance release without fabricating success on blocked cases
- the return workflow still runs on the Daml IDE ledger; Quickstart-backed deployment, role-scoped report disclosure, and first-class CPL return-right clauses remain staged follow-on work

Prompt 12 status:

- aggregate conformance suite added under `app/orchestration/` and `test/conformance/`
- `make test-conformance` now re-runs the confidential margin-call, substitution, and return demos, emits a machine-readable `ConformanceSuiteReport`, and proves authorization, determinism, haircut correctness, no double-encumbrance, atomic substitution, replay safety, report fidelity, and audit completeness
- `make demo-all` now packages the confidential workflow demos, conformance output, artifact index, and third-party integration guidance into one machine-readable final demo pack plus Markdown summary
- the Python test harness now includes shared deterministic fixture builders, isolated conformance-helper unit tests, and a Docker-free `make verify-portable` path while `make verify` remains the full Quickstart-aware superset
- the final package still runs its end-to-end workflow demos on the Daml IDE ledger even though the Control Plane DAR can now be built and installed into Quickstart; Quickstart-backed workflow execution remains the next runtime task

Prompt 13 status:

- ADR 0016 now chooses a dual-runtime bridge: the repo keeps host-native Daml SDK `2.10.4` plus JDK `17` for the existing IDE-ledger workflow surface while Quickstart-compatible DAR builds run in Docker on Daml SDK `3.4.10` plus Java `21`
- `make localnet-build-dar` now produces a Quickstart-compatible Control Plane DAR plus package-id metadata from the shared Daml source tree without repinning upstream Quickstart
- `make localnet-deploy-dar` now validates the pinned upstream checkout, rebuilds the Quickstart-compatible DAR, and uploads it through the upstream onboarding container into the running app-provider and app-user participants
- the Daml package now compiles on both runtime lines through explicit source compatibility updates, including a keyless `ReturnRequestRegistry` replay guard and template-specific query helpers
- Quickstart-backed workflow execution, confidential collateral seed data, role-scoped report disclosure, and live asset adapters remain staged follow-on work

Prompt 14 status:

- ADR 0017 now chooses a repo-owned overlay seed strategy that starts the pinned Quickstart stack, allocates the needed parties and users, seeds one confidential collateral scenario, and emits status evidence without forking upstream Quickstart
- `make localnet-start-control-plane` now starts or reuses an isolated Quickstart overlay on the dedicated `quickstart-control-plane` network, deploys `canton-collateral-control-plane-0.1.1.dar`, and writes a machine-readable deployment receipt plus Markdown summary
- `make localnet-seed-demo` now seeds one real Quickstart scenario with provider, secured-party, custodian, and operator roles plus one margin-style obligation, two provider inventory lots, and one posting intent through the shared Daml package
- `make localnet-status-control-plane` now queries the seeded Quickstart state from the provider-visible view and writes a machine-readable ledger snapshot plus Markdown status summary
- the Quickstart scenario now exists as real LocalNet ledger state, but full Quickstart-backed workflow execution, role-scoped report disclosure, and live asset adapters remain staged follow-on work

Prompt 15 status:

- ADR 0018 now chooses a narrow Quickstart-backed reference token adapter path that consumes Control Plane settlement and control artifacts without collapsing workflow authority into the adapter
- `make localnet-run-token-adapter` now consumes the seeded posting flow, performs a real token-style movement on `ReferenceTokenHolding`, confirms workflow settlement, and writes a schema-valid machine-readable adapter execution report plus Markdown summary
- `make localnet-adapter-status` now queries the provider-visible post-execution state and writes a machine-readable adapter status snapshot plus Markdown summary
- the repository now has one real, documented data-plane adapter path on Quickstart, but broader substitution or return adapters, production-grade custodian integrations, settlement-window enforcement, and role-scoped report disclosure remain staged follow-on work

Prompt 16 status:

- ADR 0019 now chooses a Quickstart-backed margin-call orchestration path that reseeds scenario-scoped state, advances the posting flow to the adapter handoff point on-ledger, invokes the reference token adapter only from the real workflow result, and folds all subordinate artifacts into one machine-readable execution report
- `make demo-margin-call-quickstart` now starts or reuses the pinned Quickstart overlay, evaluates the positive and negative Quickstart margin-call scenarios, runs the positive workflow-preparation plus adapter chain, and emits a schema-valid `ExecutionReport` plus Markdown summary and timeline artifacts
- the positive Quickstart path now links policy evaluation, optimization, workflow preparation, adapter execution, and final execution reporting through generated artifacts rather than operator-authored summaries
- the negative Quickstart paths now prove both policy-blocked and workflow-rejected cases without fabricating downstream adapter success
- substitution and return still remain on the IDE-ledger workflow path, and role-scoped report disclosure, production-grade custodian integrations, and settlement-window enforcement remain staged follow-on work

## Next 5 Tasks

1. Specify role-scoped `ExecutionReport`, `ReturnReport`, `SubstitutionReport`, and adapter-receipt disclosure profiles beyond the current workflow-party and provider-visible baseline.
2. Define versioned reference-data contracts for valuation, FX, custodian, issuer, and counterparty facts consumed by policy evaluation.
3. Define the first workflow-coupled optimizer reservation and consent interface, including substitution-scope and return-release carriage, without collapsing Canton authority.
4. Extend the reference token adapter path beyond posting into substitution and return handling, including explicit release or replacement confirmation carriage.
5. Define replay, retry, failure-recovery, and settlement-window semantics for future production-grade asset adapters without weakening the current control-plane boundary.

## Blockers

- There is no current blocker for continued documentation, policy-engine, optimizer, and report-contract work.
- There is no current blocker preventing Control Plane DAR build, package installation, seeded confidential-scenario creation, Quickstart-backed margin-call workflow execution, or the first Quickstart-backed reference token adapter execution in the pinned Quickstart LocalNet; the remaining gated work is broader adapter coverage, role-scoped reporting, reference-data contracts, and workflow-coupled reservation on top of that baseline.
- Production-grade asset-adapter and workflow-coupled implementation beyond the current reference adapter, off-ledger engines, and Daml workflow package should not proceed until the seeded LocalNet package surface and asset interface versions are pinned explicitly.
- Economic calibration beyond the current deterministic proxy objective is intentionally deferred until reference-data contracts and richer report contracts are specified.
- The current roadmap reflects the 2026-03-28 proposal and may need ADR-backed revision if the proposal changes materially.

## Dependency List

Current repo dependencies:

- Git
- `curl`
- `make`
- POSIX shell
- `tar`
- `python3`
- `rg` for lightweight verification
- Docker
- Docker Compose
- repo-local `.runtime` bootstrap for pinned Daml and Java tooling
- repo-local `.venv` bootstrap for pinned schema validation
- Temurin JDK `17.0.18+8`
- Daml SDK `2.10.4`
- Canton `2.10.4` as the current runtime compatibility baseline
- containerized Quickstart DAR build image `ubuntu:24.04`
- Quickstart bridge Daml SDK `3.4.10`
- Quickstart bridge Java `21`
- `check-jsonschema==0.37.1` via `requirements-cpl-validation.txt`
- pinned CN Quickstart commit `fe56d460af650b71b8e20098b3e76693397a8bf9`
- upstream Quickstart runtime metadata `DAML_RUNTIME_VERSION=3.4.10`, `SPLICE_VERSION=0.5.3`, and `JAVA_VERSION=21-jdk`

Target dependencies to pin in future ADRs:

- token-standard-style asset libraries or templates
- Daml Finance-style reference assets or adapters where applicable
- scenario-runner or conformance harness tooling
- deterministic developer environment bootstrap tooling

## Evidence Checklist

- [x] repository operating instructions
- [x] master tracker and roadmap
- [x] starter ADR set
- [x] architecture-boundary ADR set
- [x] invariant registry skeleton
- [x] risk register skeleton
- [x] evidence manifest categories
- [x] threat model skeleton
- [x] Prompt 1 execution report
- [x] architecture and domain package
- [x] Quickstart integration and token-alignment guidance
- [x] `CPL v0.1` prose spec and schema
- [x] schema validation toolchain and example policy set
- [x] Prompt 3 execution report
- [x] pinned dependency ADRs
- [x] initial Daml workflow skeleton package
- [x] initial policy evaluation report contract
- [x] initial deterministic policy evaluation engine
- [x] initial optimization report contract
- [x] initial deterministic optimizer
- [x] pinned Quickstart LocalNet bootstrap and smoke foundation
- [x] staged asset-adapter integration plan
- [x] executable demo artifacts
- [x] implementation-linked tests
- [x] Prompt 7 execution report
- [x] Prompt 8 execution report
- [x] first machine-readable end-to-end execution report contract
- [x] first end-to-end margin-call demo artifacts
- [x] first machine-readable end-to-end return report contract
- [x] first end-to-end return demo artifacts
- [x] first machine-readable end-to-end substitution report contract
- [x] first end-to-end substitution demo artifacts
- [x] Prompt 9 execution report
- [x] Prompt 10 execution report
- [x] Prompt 11 execution report
- [x] aggregate conformance suite
- [x] final demo pack
- [x] third-party integration guide
- [x] Prompt 12 execution report
- [x] Quickstart runtime bridge ADR and deployment command surface
- [x] Prompt 13 execution report
- [x] Quickstart seeded-scenario ADR, runbook, and evidence surface
- [x] Prompt 14 execution report
- [x] first Quickstart-backed reference token adapter path
- [x] machine-readable adapter execution report schema and generated artifact
- [x] Prompt 15 execution report
- [x] Quickstart-backed margin-call orchestration and execution-report expansion
- [x] Prompt 16 execution report

## Demo Checklist

- [x] reproducible LocalNet startup command
- [x] reproducible seed-data or bootstrap command
- [x] reproducible Quickstart control-plane start command
- [x] reproducible Quickstart scenario status command
- [x] reproducible Quickstart workflow-preparation command
- [x] reproducible Quickstart reference token adapter command
- [x] reproducible Quickstart adapter status command
- [x] reproducible Quickstart margin-call demo command
- [x] sample policy load command
- [x] machine-readable optimization report generated by real optimization execution
- [x] machine-readable execution report generated by real workflow execution
- [x] machine-readable adapter execution report generated by real adapter execution
- [x] operator-facing demo runbook
- [x] end-to-end return demo command
- [x] end-to-end substitution demo command
- [x] aggregate conformance-suite command
- [x] final demo-pack command
- [x] invariant pass/fail output
- [x] demo artifact index
- [x] third-party integration guide
- [x] reproducible Quickstart package-deployment command

## Release Checklist

- [x] all scope changes mapped to ADRs or explicitly noted as ADR-not-required
- [x] invariants linked to tests and evidence
- [x] threat model and risk register reviewed
- [x] dependency versions pinned
- [x] demo commands reproducible from a clean checkout
- [x] no fake artifacts in the release path
- [x] clean worktree at release cut

## Integration Goals

- model central-bank-style collateral frameworks with explicit eligibility, haircut, control, and settlement separation
- support tri-party-style collateral selection, valuation, and substitution workflows
- encode CCP-style concentration and haircut controls conservatively and transparently
- preserve confidentiality while enabling multi-party atomic workflows on Canton
- support reuse across financing apps, derivatives apps, tokenized-asset platforms, stablecoin rails, and custodial workflows
- emit reports that external review tooling can validate without guessing hidden state
- keep third-party integration possible through stable policy, asset, workflow, and reporting interfaces
