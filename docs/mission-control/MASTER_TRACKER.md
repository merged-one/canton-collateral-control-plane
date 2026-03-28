# Master Tracker

Last Updated: 2026-03-28
Current Phase: Milestone 4 / Phase 4 - Initial Margin Call Demo And Execution Reporting

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

Milestone 4 / Phase 4 now establishes the first executable bridge from policy evaluation and optimization into an authoritative Daml workflow path. The expected output is a reproducible margin-call demo that consumes declared scenario inputs, emits a machine-readable `ExecutionReport`, and proves one positive posting path plus explicit negative-path evidence without pretending the full Quickstart deployment is complete.

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
- repo-local bootstrap, status, build, demo, and verify commands published under `Makefile` and `scripts/`
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
- LocalNet startup, Control Plane DAR deployment, token-standard-style assets, and confidential collateral seed data remain staged follow-on work because the current repo Daml package (`2.10.4`) is not yet bridged to the pinned Quickstart runtime line (`3.4.10`)

Prompt 9 status:

- first end-to-end margin-call demo added under `app/orchestration/` and `examples/demo-scenarios/margin-call/`
- `make demo-margin-call` now evaluates positive and negative margin-call scenarios, runs the positive Daml workflow path, and emits a machine-readable `ExecutionReport` plus Markdown summary and timeline artifacts
- the demo now covers negative paths for ineligible collateral, insufficient lendable value, and an expired policy window without fabricating workflow success on blocked cases
- the prototype still runs the positive workflow path on the Daml IDE ledger; Quickstart-backed package deployment and role-scoped report disclosure remain staged follow-on work

## Next 5 Tasks

1. Close the Daml runtime bridge required to deploy the Control Plane DAR into the pinned Quickstart LocalNet.
2. Specify role-scoped `ExecutionReport` disclosure profiles beyond the current operator-facing demo aggregate and workflow-party report baseline.
3. Define versioned reference-data contracts for valuation, FX, custodian, issuer, and counterparty facts consumed by policy evaluation.
4. Define the first workflow-coupled optimizer reservation and consent interface without collapsing Canton authority.
5. Define the first asset-adapter interface that will consume `SettlementInstruction` and `EncumbranceState` contracts without collapsing workflow authority.

## Blockers

- There is no current blocker for continued documentation, policy-engine, optimizer, and report-contract work.
- Full Quickstart-backed workflow deployment is blocked on the current runtime-version bridge between the repo Daml package (`2.10.4`) and the pinned upstream Quickstart runtime line (`3.4.10`).
- Live asset-adapter and workflow-coupled implementation beyond the current off-ledger engines and Daml skeletons should not proceed until the LocalNet package-deployment path and asset interface versions are pinned explicitly.
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
- [x] Prompt 9 execution report

## Demo Checklist

- [x] reproducible LocalNet startup command
- [x] reproducible seed-data or bootstrap command
- [x] sample policy load command
- [x] machine-readable optimization report generated by real optimization execution
- [x] machine-readable execution report generated by real workflow execution
- [x] operator-facing demo runbook
- [ ] end-to-end substitution or return demo command

## Release Checklist

- [ ] all scope changes mapped to ADRs or explicitly noted as ADR-not-required
- [ ] invariants linked to tests and evidence
- [ ] threat model and risk register reviewed
- [ ] dependency versions pinned
- [ ] demo commands reproducible from a clean checkout
- [ ] no fake artifacts in the release path
- [ ] clean worktree at release cut

## Integration Goals

- model central-bank-style collateral frameworks with explicit eligibility, haircut, control, and settlement separation
- support tri-party-style collateral selection, valuation, and substitution workflows
- encode CCP-style concentration and haircut controls conservatively and transparently
- preserve confidentiality while enabling multi-party atomic workflows on Canton
- support reuse across financing apps, derivatives apps, tokenized-asset platforms, stablecoin rails, and custodial workflows
- emit reports that external review tooling can validate without guessing hidden state
- keep third-party integration possible through stable policy, asset, workflow, and reporting interfaces
