# Master Tracker

Last Updated: 2026-03-28
Current Phase: Milestone 1 / Phase 1 - CPL, Formal Model, And Runtime Foundation

## Mission

Stand up a documentation-first C-COPE repository: a neutral Canton collateral control-plane prototype that can safely evolve into reusable policy, optimization, workflow, and reporting components for margin, repo, securities-lending, treasury, collateral mobility, and close-out workflows.

## Scope

- define repository governance, change control, and contribution rules
- establish proposal-aligned architecture, invariant, risk, evidence, and testing scaffolding
- prepare for a pinned Quickstart-based LocalNet, token-standard-style asset model, and Daml workflow baseline
- shape the repo around a reusable collateral policy language, optimizer, workflow library, and conformance suite
- provide an auditable control spine for future implementation phases

## Non-Goals

- shipping production business logic in this phase
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

Milestone 1 / Phase 1 establishes the first formal policy package for the repository. The expected output is a durable `CPL v0.1` contract with machine-readable schema validation, example policy profiles, and enough versioning discipline to support later engine and workflow work without hidden policy semantics.

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

## Next 5 Tasks

1. Specify machine-readable `PolicyDecisionReport` and `ExecutionReport` contracts plus disclosure profiles.
2. Pin the target Quickstart release and overlay strategy that will sit on top of the current Daml and Canton baseline.
3. Define the first Daml package boundary for obligations, encumbrance, substitution, return, and settlement instructions beyond the runtime-foundation smoke package.
4. Define versioned reference-data contracts for valuation, FX, custodian, and issuer facts consumed by CPL evaluation.
5. Expand the conformance-suite matrix to cover negative, temporal, privacy, atomicity, and runtime-bootstrap scenarios against the new foundation.

## Blockers

- No current blocker for continued specification work.
- Policy-engine and workflow implementation should not start until the target Quickstart overlay and asset interface versions are pinned on top of the current Daml and Canton baseline.
- Economic calibration is intentionally deferred until reference-data contracts and report contracts are specified.
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
- report schema validation tooling
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
- [ ] executable demo artifacts
- [ ] implementation-linked tests

## Demo Checklist

- [ ] reproducible LocalNet startup command
- [ ] reproducible seed-data or bootstrap command
- [ ] sample policy load command
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
