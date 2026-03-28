# Worklog

This log is append-oriented. Every task should record intent before changes and outcomes after changes.

## 2026-03-28 - Prompt 1 - Pre-Change

Intent:
Create the repository's mission-control and documentation spine without adding business logic.

Starting state:

- repository contains only `.git`
- no operating instructions or architecture documents exist yet

Planned commands:

```sh
make status
make docs-lint
make verify
git status --short --branch
```

Expected artifacts:

- repository operating instructions
- mission-control tracker, roadmap, worklog, and decision log
- starter ADR, invariants, risks, evidence, security, testing, and change-control documents

## 2026-03-28 - Prompt 1 - Post-Change

Outcome:
Created the repository's initial mission-control spine and kept the repo documentation-only.

Completed artifacts:

- root operating documents: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, `.gitignore`, `Makefile`
- mission-control documents under `docs/mission-control/`
- starter ADR, invariants, risks, evidence, integration, domain, testing, security, runbook, and change-control documents
- prompt execution report in `docs/evidence/prompt-01-execution-report.md`

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed
- `make status` reported Phase 0 and the expected untracked documentation tree before commit
- `make verify` passed and confirmed the repository remains documentation-only

Next step:
Pin the target Quickstart or LocalNet and document the first interface and dependency ADRs before adding business logic.

## 2026-03-28 - Proposal Alignment - Pre-Change

Intent:
Use the development-fund proposal as a stronger framing input for repository architecture, scope, milestones, and invariant planning.

Starting state:

- repository has a generic mission-control spine
- proposal introduces a concrete control-plane framing, five-layer reference stack, milestone plan, and broader workflow scope

Planned commands:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Expected artifacts:

- updated repo framing and roadmap aligned to the proposal
- expanded invariant and integration documentation
- ADR and decision-log updates where the proposal changes repository-level architecture assumptions

## 2026-03-28 - Proposal Alignment - Post-Change

Outcome:
Aligned the repository docs to the 2026-03-28 development-fund proposal and made the control-plane framing explicit without adding business logic.

Completed artifacts:

- proposal-aligned repository framing in `README.md` and `docs/mission-control/MASTER_TRACKER.md`
- milestone structure updated in `docs/mission-control/ROADMAP.md`
- initial architectural ADR later refined into `docs/adrs/0002-system-boundaries.md`, `docs/adrs/0003-policy-optimization-workflow-separation.md`, and `docs/adrs/0004-report-fidelity-and-evidence.md`
- expanded invariant, integration, glossary, testing, evidence, and risk documents
- decision log updated to reflect the adopted solution shape

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed after the proposal-alignment updates
- `make status` continued to report `Current Phase: Phase 0 - Mission Control Spine`
- `make verify` passed and confirmed the repository remains documentation-only

Next step:
Translate the proposal's Milestone 1 into concrete repository artifacts: `CPL v0.1`, policy profiles, and the first dependency and interface ADRs.

## 2026-03-28 - Prompt 2 - Pre-Change

Intent:
Design the repository's technical architecture and domain model for a Canton-native collateral control plane, with explicit separation between policy language, policy evaluation, optimization, Daml workflow orchestration, reporting/evidence, and demo/runtime infrastructure.

Risks addressed:

- ambiguous system boundaries could let policy, optimization, workflow, and reporting concerns bleed together
- privacy and report-fidelity assumptions could stay implicit instead of being pinned to Canton-native boundaries
- future implementation prompts could diverge without a shared lifecycle model, domain vocabulary, and integration plan

Affected files:

- `docs/architecture/OVERVIEW.md`
- `docs/architecture/COMPONENTS.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/DEPLOYMENT_MODEL.md`
- `docs/architecture/PRIVACY_MODEL.md`
- `docs/adrs/0002-system-boundaries.md`
- `docs/adrs/0003-policy-optimization-workflow-separation.md`
- `docs/adrs/0004-report-fidelity-and-evidence.md`
- `docs/domain/COLLATERAL_DOMAIN_MODEL.md`
- `docs/domain/ACTORS_AND_ROLES.md`
- `docs/domain/LIFECYCLE_STATES.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-02-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `docs/adrs/README.md`
- `Makefile`

Acceptance criteria:

- the repository has a crisp technical architecture for a Canton-native collateral control plane
- domain concepts and lifecycle states are unambiguous
- future implementation prompts have enough guidance to stay coherent
- the design clearly supports future third-party integration

Planned commands:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 2 - Post-Change

Outcome:
Published the repository's first full architecture and domain package for a Canton-native collateral control plane, with explicit separation between policy language, policy evaluation, optimization, Daml workflow orchestration, reporting and evidence, and demo/runtime infrastructure.

Completed artifacts:

- architecture overview, component, data-flow, deployment, and privacy documents under `docs/architecture/`
- new ADR set in `docs/adrs/0002-system-boundaries.md`, `docs/adrs/0003-policy-optimization-workflow-separation.md`, and `docs/adrs/0004-report-fidelity-and-evidence.md`
- domain model, actors-and-roles, and lifecycle-state documents under `docs/domain/`
- Quickstart integration and token-standard alignment guidance under `docs/integration/`
- mission-control, invariant, risk, threat, evidence, and validation updates aligned to the new architecture package
- prompt execution record in `docs/evidence/prompt-02-execution-report.md`

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed
- `make status` passed and continued to report `Current Phase: Phase 0 - Mission Control Spine`
- `make verify` passed and confirmed the repository remains documentation-only
- architecture and domain guidance now cover system boundaries, privacy, lifecycle transitions, and future third-party integration assumptions

Next step:
Pin the Quickstart and asset-adapter dependency set, then formalize the first `CPL v0.1`, policy decision report, execution report, and Daml package contracts against the documented architecture.

## 2026-03-28 - Prompt 3 - Pre-Change

Intent:
Design and publish the first `CPL v0.1` package as a prose specification plus a machine-readable schema, supported by validating example policies, a minimal durable validation toolchain, and mission-control traceability updates.

Risks addressed:

- the repository currently describes CPL conceptually but does not yet expose a versioned machine-readable contract
- policy coverage could remain too weak for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style controls
- schema drift or weak validation could undermine later deterministic policy-engine work
- operators would lack a reproducible command to prove example policies conform to the published schema

Affected files:

- `README.md`
- `Makefile`
- `requirements-cpl-validation.txt`
- `docs/specs/CPL_SPEC_v0_1.md`
- `docs/specs/CPL_EXAMPLES.md`
- `schema/cpl.schema.json`
- `examples/policies/central-bank-style-policy.json`
- `examples/policies/tri-party-style-policy.json`
- `examples/policies/ccp-style-policy.json`
- `examples/policies/bilateral-csa-style-policy.json`
- `docs/adrs/0005-cpl-format-and-versioning.md`
- `docs/adrs/README.md`
- `docs/testing/CPL_VALIDATION_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-03-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `docs/runbooks/README.md`

Acceptance criteria:

- `CPL v0.1` exists as both prose spec and machine-readable schema
- the four example policy files validate successfully
- the schema is strong enough to support later policy-engine work without relying on hidden conventions
- central-bank, tri-party, CCP, and bilateral market-practice mappings are documented clearly
- the repository exposes at least one reproducible validation command such as `make validate-cpl`

Planned commands:

```sh
make validate-cpl
make docs-lint
make status
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 3 - Post-Change

Outcome:
Published the first formal `CPL v0.1` package for the repository, including a normative specification, strict JSON Schema, four validating market-profile examples, a pinned validation toolchain, and the required mission-control traceability updates.

Completed artifacts:

- `CPL v0.1` prose specification and example guide under `docs/specs/`
- machine-readable schema in `schema/cpl.schema.json`
- validating example policies for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style usage under `examples/policies/`
- ADR 0005 for CPL format and versioning plus a dedicated CPL validation test plan
- `make validate-cpl` and the pinned validator dependency in `requirements-cpl-validation.txt`
- README, tracker, decision log, invariant, risk, threat, runbook, evidence, and prompt-execution updates aligned to the new CPL surface

Commands run:

```sh
make validate-cpl
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make validate-cpl` passed and confirmed the schema validates against its metaschema, the four example policies validate successfully, and generated negative cases fail as expected
- `make docs-lint` passed
- `make status` passed and reported `Current Phase: Milestone 1 / Phase 1 - CPL And Formal Model`
- `make verify` passed and now includes the CPL schema validation loop in the baseline repository controls
- the repository remains free of business logic while now exposing a durable machine-readable policy contract

Next step:
Define machine-readable `PolicyDecisionReport` and `ExecutionReport` contracts, then pin the Quickstart and asset-adapter dependencies that will consume `CPL v0.1`.

## 2026-03-28 - Prompt 4 - Pre-Change

Intent:
Establish a runnable technical foundation for the prototype with a pinned Daml-centric toolchain, reproducible bootstrap and verification scripts, and directory/package scaffolding that future implementation prompts can extend without restructuring the repository.

Risks addressed:

- dependency drift could block later Daml and Canton work or make local reproduction inconsistent
- the repo's current `verify` contract rejects all implementation files and therefore no longer matches the next prototype phase
- future prompts could start adding workflow, integration, and reporting code without a stable package layout or operator command surface
- service-layer scope could sprawl unless the runtime foundation keeps policy, workflow, reporting, and integration concerns explicitly separated

Affected files:

- `daml.yaml`
- `.tool-versions`
- `Makefile`
- `scripts/bootstrap.sh`
- `scripts/verify.sh`
- `scripts/dev-status.sh`
- `docs/setup/LOCAL_DEV_SETUP.md`
- `docs/setup/DEPENDENCY_POLICY.md`
- `docs/adrs/0006-runtime-foundation.md`
- `docs/adrs/README.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-04-execution-report.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/runbooks/README.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `README.md`
- `daml/`
- `app/`
- `reports/`
- `test/`
- `examples/`
- `infra/`

Acceptance criteria:

- the repo exposes a real runtime and build foundation rooted in Daml for workflow modeling
- bootstrap, status, verify, CPL validation, future Daml build, and future demo commands are reproducible and documented
- pinned dependencies are justified, locally installable, and visible in both code and docs
- future prompts can add Daml packages and small helper services without restructuring the repo
- mission-control, invariant, ADR, and evidence documents reflect the new foundation phase

Planned commands:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 4 - Post-Change

Outcome:
Established the repository's first runnable technical foundation with a pinned Daml-centric toolchain, repo-local bootstrap, a minimal executable Daml package, and a reproducible command surface for setup, build, smoke execution, and verification.

Completed artifacts:

- pinned toolchain files: `daml.yaml`, `.tool-versions`, and `scripts/toolchain.env`
- repo-local bootstrap and control scripts in `scripts/bootstrap.sh`, `scripts/dev-status.sh`, and `scripts/verify.sh`
- minimal executable Daml package in `daml/Foundation.daml` and `daml/Bootstrap.daml`
- reserved repository surfaces for future services, reports, tests, examples, and infrastructure under `app/`, `reports/`, `test/`, `examples/`, and `infra/`
- setup documentation in `docs/setup/LOCAL_DEV_SETUP.md` and `docs/setup/DEPENDENCY_POLICY.md`
- ADR 0006 plus mission-control, invariant, evidence, risk, threat, runbook, and README updates aligned to the new runtime phase
- prompt execution record in `docs/evidence/prompt-04-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make demo-run
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed and installed the pinned repo-local Daml SDK `2.10.4`, Temurin JDK `17.0.18+8`, and validation tooling
- `make status` passed and reported the new runtime-foundation phase, pinned toolchain, installed toolchain, and scaffold directories
- `make validate-cpl` passed and preserved the earlier schema-validation baseline
- `make daml-build` passed and produced the repository DAR artifact under `.daml/dist/`
- `make demo-run` passed and executed the `Bootstrap:foundationSmokeTest` Daml script against the IDE ledger
- `make verify` passed and now covers docs linting, CPL validation, Daml build, and Daml smoke execution in one command
- the repo now has executable runtime scaffolding without yet adding collateral business logic

Next step:
Define the first machine-readable `PolicyDecisionReport` and `ExecutionReport` contracts, then expand the Daml package boundary from the runtime-foundation smoke package into obligation, encumbrance, substitution, return, and settlement contracts.

## 2026-03-28 - Prompt 5 - Pre-Change

Intent:
Implement the first Daml domain model and workflow skeletons for confidential collateral control, including obligation, inventory, encumbrance, substitution, return, settlement, and execution-report surfaces that preserve policy and optimization separation.

Risks addressed:

- privacy boundaries could erode if workflow templates expose more than the required role-specific state
- substitution or return flows could accidentally encode non-atomic or implicitly successful paths
- the first Daml package boundary could collapse policy, workflow, settlement, and reporting concerns into one opaque contract set
- report and state vocabularies could drift from the documented lifecycle model and invariants if they are not pinned together now

Affected files:

- `daml.yaml`
- `Makefile`
- `daml/Bootstrap.daml`
- `daml/CantonCollateral/*.daml`
- `docs/domain/DAML_MAPPING.md`
- `docs/adrs/0007-daml-contract-boundaries.md`
- `docs/testing/DAML_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-05-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `README.md`
- `scripts/dev-status.sh`
- `scripts/verify.sh`

Acceptance criteria:

- Daml modules for roles, assets, lots, encumbrance, obligations, substitution, return, settlement, and execution reporting compile under the pinned SDK
- the repository contains contract-level lifecycle skeletons for margin call creation, posting intent, substitution, approval or rejection, return request, and release or return settlement intent
- the design preserves role separation, privacy intent, and policy-versus-workflow separation
- reproducible build and script execution commands cover the new Daml package and tests

Planned commands:

```sh
make bootstrap
make daml-build
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 5 - Post-Change

Outcome:
Implemented the repository's first real Daml workflow package for confidential collateral control, including contract boundaries for obligations, posting intent, substitution, return, settlement instruction, encumbrance state, and execution reporting, then verified the package with executable Daml lifecycle scripts.

Completed artifacts:

- initial Daml workflow modules under `daml/CantonCollateral/` for shared types, roles, assets, inventory, encumbrance, obligations, posting, substitution, return, settlement, reporting, and tests
- updated `daml/Bootstrap.daml`, `daml.yaml`, `Makefile`, and verification scripts so the new Daml package builds, tests, and smoke-runs from the pinned toolchain
- new contract-boundary ADR in `docs/adrs/0007-daml-contract-boundaries.md`
- new domain-to-Daml mapping in `docs/domain/DAML_MAPPING.md`
- new Daml lifecycle test plan in `docs/testing/DAML_TEST_PLAN.md`
- mission-control, invariant, evidence, risk, security, setup, and contribution docs updated to reflect the first workflow skeleton package
- prompt execution record in `docs/evidence/prompt-05-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make daml-test
make demo-run
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported `Current Phase: Milestone 1 / Phase 1 - CPL, Formal Model, Runtime Foundation, And Initial Daml Workflow Skeletons`
- `make validate-cpl` passed
- `make daml-build` passed and produced the repository DAR artifact under `.daml/dist/`
- `make daml-test` passed and executed the three lifecycle scripts
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make verify` passed and exercised docs linting, CPL validation, Daml build, Daml lifecycle tests, and the workflow smoke run
- `git status --short --branch` showed only the expected task-related changes before commit

Next step:
Define the first machine-readable `PolicyDecisionReport` contract and role-scoped `ExecutionReport` disclosure profiles, then pin the Quickstart overlay and asset-adapter interfaces that will consume the current Daml settlement and encumbrance contracts.

## 2026-03-28 - Prompt 6 - Pre-Change

Intent:
Implement the repository's first real `CPL v0.1` policy evaluation engine, including deterministic eligibility, haircut, lendable-value, concentration, control, and wrong-way-risk checks backed by the published schema and a machine-readable report contract.

Risks addressed:

- the repository currently has a strict CPL schema but no executable evaluator, so policy semantics still stop at documentation
- ad hoc evaluation logic could drift from the published `CPL v0.1` schema and market-practice examples
- report outputs could become non-deterministic or lose explicit machine-readable failure attribution
- concentration, encumbrance, settlement-currency, and wrong-way-risk controls could remain untested in real inventory scenarios

Affected files:

- `Makefile`
- `README.md`
- `app/policy-engine/*`
- `examples/inventory/*`
- `reports/schemas/policy-evaluation-report.schema.json`
- `reports/generated/*`
- `docs/specs/POLICY_EVALUATION_REPORT_SPEC.md`
- `docs/testing/POLICY_ENGINE_TEST_PLAN.md`
- `docs/adrs/0008-policy-evaluation-engine.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-06-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/testing/TEST_STRATEGY.md`
- `test/policy-engine/*`

Acceptance criteria:

- the policy engine loads a real `CPL v0.1` policy file and candidate inventory set from disk
- eligibility, haircut, lendable value, concentration, encumbrance, settlement-currency, and wrong-way-risk outcomes are derived from the published schema fields rather than ad hoc flags
- failure attribution is explicit, deterministic, and machine-readable at both asset and portfolio levels
- reproducible commands exist for policy evaluation and policy-engine tests
- at least one real policy-evaluation report artifact is generated and linked into mission-control evidence

Planned commands:

```sh
make bootstrap
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 6 - Post-Change

Outcome:
Implemented the repository's first real `CPL v0.1` policy evaluation engine, added the first machine-readable `PolicyEvaluationReport` contract, generated a real report artifact from the command surface, and verified the new engine alongside the existing Daml workflow baseline.

Completed artifacts:

- deterministic policy-engine source under `app/policy-engine/` for policy loading, inventory loading, eligibility checks, haircut and lendable-value calculation, concentration evaluation, wrong-way-risk handling, and report generation
- normalized example inventory input under `examples/inventory/central-bank-eligible-inventory.json`
- canonical report schema under `reports/schemas/policy-evaluation-report.schema.json`
- real generated report artifact under `reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json`
- report specification in `docs/specs/POLICY_EVALUATION_REPORT_SPEC.md`
- new design decision in `docs/adrs/0008-policy-evaluation-engine.md`
- policy-engine test plan in `docs/testing/POLICY_ENGINE_TEST_PLAN.md`
- deterministic policy-engine scenario tests under `test/policy-engine/`
- updated command surface in `Makefile`, `scripts/dev-status.sh`, and `scripts/verify.sh`
- mission-control, invariant, evidence, risk, security, setup, and repository-surface docs updated to reflect the new engine package
- prompt execution record in `docs/evidence/prompt-06-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
make daml-test
make demo-run
make docs-lint
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported `Current Phase: Milestone 2 / Phase 2 - Initial Policy Engine, Report Contracts, And Daml Workflow Skeletons`
- `make validate-cpl` passed
- `make policy-eval ...` passed, generated the schema-valid example policy-evaluation report artifact, and validated it against `reports/schemas/policy-evaluation-report.schema.json`
- `make test-policy-engine` passed and executed the eight deterministic scenario tests for eligibility, issuer rejection, haircut application, currency mismatch haircuts, concentration breaches, wrong-way-risk exclusions, encumbrance failures, and repeatability
- `make daml-test` passed and preserved the existing workflow lifecycle-script baseline
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make docs-lint` passed after the policy-engine, tracker, ADR, spec, test-plan, and evidence updates
- `make verify` passed and exercised docs linting, CPL validation, policy-engine tests, Daml build, Daml lifecycle tests, and the workflow smoke run
- `git status --short --branch` showed only the expected task-related changes before commit

Next step:
Define pinned reference-data contracts for valuation, FX, issuer, and counterparty facts, then add role-scoped `ExecutionReport` disclosure profiles and the first asset-adapter interface on top of the new policy-engine and Daml package surfaces.

## 2026-03-28 - Rename To Canton Collateral Control Plane - Pre-Change

Intent:
Rename the repository's user-facing identity from "Canton Collateral Policy & Optimization Engine" / "C-COPE" to "Canton Collateral Control Plane" without changing the mission, implementation sequencing, or subsystem boundaries, and make the control-plane versus data-plane architecture explicit across the primary documentation surfaces.

Risks addressed:

- the current project name over-emphasizes two subsystems and obscures that policy, optimization, workflow orchestration, conformance, and reporting already operate as one control plane
- the old acronym can create market-structure ambiguity and distract from the intended architecture
- rename churn could accidentally flatten subsystem boundaries, misstate historical evidence, or break future prompts and reproducible commands
- build metadata and generated-artifact naming could drift from the new identity unless updated consistently and verified

Affected files:

- `README.md`
- `AGENTS.md`
- `Makefile`
- `daml.yaml`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/WORKLOG.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/architecture/OVERVIEW.md`
- `docs/architecture/COMPONENTS.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/DEPLOYMENT_MODEL.md`
- `docs/architecture/PRIVACY_MODEL.md`
- `docs/domain/GLOSSARY.md`
- `docs/domain/COLLATERAL_DOMAIN_MODEL.md`
- `docs/integration/INTEGRATION_SURFACES.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/adrs/README.md`
- `docs/adrs/0002-system-boundaries.md`
- `docs/adrs/0009-rename-to-canton-collateral-control-plane.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-04-execution-report.md`
- `docs/evidence/prompt-05-execution-report.md`
- `docs/evidence/rename-to-collateral-control-plane-execution-report.md`
- `docs/risks/RISK_REGISTER.md`

Acceptance criteria:

- the repository presents itself as "Canton Collateral Control Plane" on primary identity surfaces
- the former name is retained only as a deprecated historical alias where continuity helps
- README, architecture docs, glossary, and ADRs distinguish control-plane responsibilities from the data plane
- subsystem names remain intact for `CPL`, policy evaluation, optimization, workflow, conformance, and reporting
- in-repo metadata and DAR naming are updated where safe without unnecessary directory or module churn
- mission-control, invariants, evidence, and ADR records reflect the rename
- relevant checks run successfully and no existing code or tests are broken

Planned commands:

```sh
make bootstrap
make docs-lint
make validate-cpl
make test-policy-engine
make daml-build
make daml-test
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Rename To Canton Collateral Control Plane - Post-Change

Outcome:
Renamed the repository's primary user-facing identity to "Canton Collateral Control Plane", clarified the control-plane versus data-plane architecture across the core documentation surfaces, preserved the prior name only as a deprecated historical alias, and updated safe in-repo metadata so the Daml build artifact now carries the new control-plane name.

Completed artifacts:

- renamed primary identity surfaces in `README.md`, `AGENTS.md`, `docs/mission-control/`, and the glossary
- added explicit control-plane versus data-plane architecture guidance in `README.md`, `docs/architecture/OVERVIEW.md`, `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`, and `docs/domain/GLOSSARY.md`
- updated build metadata in `daml.yaml` so the DAR now builds as `canton-collateral-control-plane-0.1.0.dar`
- recorded the rename decision in `docs/adrs/0009-rename-to-canton-collateral-control-plane.md` and linked it through the decision log, invariant registry, risk register, and evidence manifest
- updated continuity and evidence records in `docs/evidence/`, including this rename execution report
- preserved subsystem names and existing code layout for `CPL`, policy evaluation, optimization, workflow, conformance, and reporting surfaces

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make test-policy-engine
make daml-build
make daml-test
make demo-run
make docs-lint
make verify
python3 -m compileall app/policy-engine test/policy-engine
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported the current Milestone 2 / Phase 2 state plus the renamed Daml package metadata
- `make validate-cpl` passed
- `make test-policy-engine` passed and preserved the eight deterministic Python scenario tests plus report generation
- `make daml-build` passed and produced `.daml/dist/canton-collateral-control-plane-0.1.0.dar`
- `make daml-test` passed and preserved the Daml lifecycle-script baseline
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make docs-lint` passed after the rename ADR, execution report, tracker, and architecture updates were added to the required documentation set
- `make verify` passed and re-executed the repository lint, validation, policy-engine, Daml build, Daml lifecycle, and workflow smoke checks in one command
- `python3 -m compileall app/policy-engine test/policy-engine` passed as an extra Python syntax sanity check
- no dedicated formatter or static type-check target is currently configured in the repository; the available executable lint and verification loop passed cleanly
- `git status --short --branch` showed only the expected rename-related modifications before commit

Next step:
Continue with the Prompt 6 follow-on work by defining pinned reference-data contracts, role-scoped `ExecutionReport` disclosure profiles, and the first asset-adapter interface on top of the current policy-engine and Daml package surfaces.
