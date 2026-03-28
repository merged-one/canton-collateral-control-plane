# Master Tracker

Last Updated: 2026-03-28
Current Phase: Milestone 2 / Phase 2 - Initial Policy Engine, Report Contracts, And Daml Workflow Skeletons

## Mission

Stand up a documentation-first C-COPE repository: a neutral Canton collateral control-plane prototype that can safely evolve into reusable policy, optimization, workflow, and reporting components for margin, repo, securities-lending, treasury, collateral mobility, and close-out workflows.

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

Milestone 2 / Phase 2 establishes the first executable policy-decision path for the repository. The expected output is a deterministic off-ledger engine that consumes `CPL v0.1`, evaluates normalized candidate inventory, emits a machine-readable `PolicyEvaluationReport`, and stays separate from authoritative workflow state on Canton.

Prompt 1 status:

- documentation spine created
- baseline verification commands added
- repository remains intentionally free of business logic pending pinned dependency and interface decisions

Proposal alignment status:

- repository framing updated to the C-COPE control-plane model
- roadmap now mirrors the proposal milestone structure
- invariants expanded toward the proposal's conformance-suite acceptance criteria
- future proposal changes should be incorporated through ADRs rather than informal drift

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
- optimization, role-scoped `ExecutionReport` disclosure profiles, live asset adapters, and reference-data contracts remain future layers

## Next 5 Tasks

1. Define versioned reference-data contracts for valuation, FX, custodian, issuer, and counterparty facts consumed by policy evaluation.
2. Specify role-scoped `ExecutionReport` disclosure profiles beyond the current workflow-party report baseline.
3. Pin the target Quickstart release and overlay strategy that will sit on top of the current Daml and Canton baseline.
4. Expand the conformance-suite matrix to cover temporal, privacy, replay, substitution, and release scenarios on top of the new policy-engine and Daml package surfaces.
5. Define the first asset-adapter interface that will consume `SettlementInstruction` and `EncumbranceState` contracts without collapsing workflow authority.

## Blockers

- No current blocker for continued policy-engine and report-contract work.
- Live asset-adapter and workflow-coupled implementation beyond the current engine and Daml skeletons should not proceed until the target Quickstart overlay and asset interface versions are pinned on top of the current Daml and Canton baseline.
- Economic calibration is intentionally deferred until reference-data contracts and richer report contracts are specified.
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
- repo-local `.runtime` bootstrap for pinned Daml and Java tooling
- repo-local `.venv` bootstrap for pinned schema validation
- Temurin JDK `17.0.18+8`
- Daml SDK `2.10.4`
- Canton `2.10.4` as the current runtime compatibility baseline
- `check-jsonschema==0.37.1` via `requirements-cpl-validation.txt`

Target dependencies to pin in future ADRs:

- Canton Quickstart or equivalent LocalNet bundle
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
- [x] executable demo artifacts
- [x] implementation-linked tests

## Demo Checklist

- [ ] reproducible LocalNet startup command
- [ ] reproducible seed-data or bootstrap command
- [x] sample policy load command
- [ ] end-to-end substitution or return demo command
- [ ] machine-readable execution report generated by real workflow execution
- [ ] operator-facing demo runbook

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
