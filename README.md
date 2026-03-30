# Canton Collateral Control Plane

## What this prototype is

This repository is a documentation-first prototype for the Canton Collateral Control Plane, a reusable collateral control plane for Canton-native secured-finance workflows. It coordinates shared control logic for:

- collateral eligibility evaluation
- haircut and lendable-value calculation
- concentration-limit monitoring
- encumbrance and release control
- substitution and allocation
- pre-positioning and mobilization
- atomic collateral movement across workflows
- machine-readable collateral decision and execution reporting

The intended runtime shape is a Quickstart-based LocalNet with token-standard-style assets, reference Daml workflows, and auditable reports that can be checked against invariants, evidence, and tests.

Historical alias note:
The former name "Canton Collateral Policy & Optimization Engine" is retained only as a deprecated historical alias for continuity in older records. `C-COPE` should not be used in new documentation; use "Canton Collateral Control Plane" or "the Control Plane" instead.

Current framing note:
This repository now reflects the development-fund proposal dated 2026-03-28. The rename to "Canton Collateral Control Plane" is semantic, not directional: the current policy, optimization, workflow, conformance, and reporting subsystems remain intact and are now described more precisely as parts of one shared control plane. If the proposal changes later, repository-level assumptions should be revised through the mission-control process and ADRs.

## Reviewer Start

If you are reviewing the proposal package rather than contributing code, start here:

- [docs/evidence/REVIEWER_START_HERE.md](./docs/evidence/REVIEWER_START_HERE.md)
- [docs/evidence/PROPOSAL_SUBMISSION_MEMO.md](./docs/evidence/PROPOSAL_SUBMISSION_MEMO.md)
- `make proposal-package`

## Why documentation-first

Collateral policy, control, substitution, allocation, and release handling are safety-critical. Before business logic exists, this repository establishes the operating rules needed to build the prototype safely:

- requirements must trace to invariants, evidence, and tests
- significant design choices must be captured as ADRs
- changes must leave behind reproducible commands
- demos must be reproducible and must not contain fake success artifacts

This order of work is deliberate. The Control Plane spans policy, optimization, workflow, conformance, and reporting layers across multiple future apps, so undocumented assumptions would create defects at the shared control boundary, not just in one app.

## Control Plane Vs Data Plane

The architecture is intentionally split between the shared collateral control plane and the data-plane surfaces it evaluates, drives, or reports on.

| Plane | Includes |
| --- | --- |
| Control plane | `CPL`, eligibility evaluation, haircuting and lendable value, encumbrance and release control, concentration logic, optimization, substitution orchestration, conformance, and reporting |
| Data plane | token-standard-style assets, Daml Finance-style assets, ledger state and contract instances, settlement and DvP rails, and the Quickstart or LocalNet execution environment |

The workflow library remains a control-plane subsystem, while the resulting ledger state and contract instances it commits are part of the data plane. This distinction keeps authoritative execution state separate from policy authoring, optimization objectives, and evidence generation.

## Control-Plane Subsystems

The target architecture follows the proposal-aligned subsystem stack while preserving explicit reporting and evidence boundaries:

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
6. Reporting and Evidence Layer
   Machine-readable decision and execution reporting plus mission-control traceability artifacts.

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
- initial deterministic `CPL v0.1` policy engine and machine-readable policy evaluation report contract
- initial deterministic optimization engine and machine-readable optimization report contract
- first end-to-end margin-call demo command with a machine-readable execution report, Markdown summary, and timeline artifacts
- first Quickstart-backed end-to-end margin-call demo command with a machine-readable execution report, Markdown summary, timeline artifacts, and subordinate workflow plus adapter artifacts
- first end-to-end return demo command with a machine-readable return report, Markdown summary, and timeline artifacts
- first Quickstart-backed end-to-end return demo command with a machine-readable return report, Markdown summary, timeline artifacts, and subordinate workflow plus adapter artifacts
- first end-to-end substitution demo command with a machine-readable substitution report, Markdown summary, and timeline artifacts
- aggregate conformance-suite command with explicit invariant pass or fail output across the three confidential workflow demos
- final demo-pack command with machine-readable artifact indexing and third-party integration guidance
- proposal submission package command with a machine-readable reviewer-facing manifest, summary, memo, and walkthrough surfaces
- pinned runtime foundation for Daml-centric workflow modeling and local verification
- pinned Quickstart-based LocalNet bootstrap and compose-config smoke foundation that preserves upstream CN Quickstart workflows as closely as practical
- containerized Quickstart runtime bridge plus real Quickstart start, deploy, seed, and status commands for the Control Plane DAR and seeded scenario
- first Quickstart-backed reference token adapter path with a machine-readable adapter execution report and provider-visible adapter status artifacts
- first Daml domain model and lifecycle skeletons for obligations, posting, substitution, return, settlement intent, and execution reporting
- executable Daml script checks for margin call, posting, substitution, and return skeletons
- implementation-ready planning for CPL, policy-engine, optimization, workflow, and conformance phases
- reusable framing for margin, repo, securities-lending, treasury, and collateral-mobility workflows

## Non-Goals

Current non-goals:

- becoming a CCP, custodian, central-bank facility, price-oracle business, or legal-document platform
- replacing venue-specific, repo-specific, or derivatives-specific applications
- production-ready economic calibration
- production-grade live integrations with custodians, CCPs, central-bank systems, or external pricing stacks
- Quickstart-backed adapter coverage beyond the current seeded scenario plus narrow reference token posting path in the pinned LocalNet
- generic external integration buses or production custodian abstractions
- UI development
- performance tuning
- live funding-curve optimization, workflow-coupled reservation, settlement-window enforcement, and production-grade collateral business logic in this phase

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
make localnet-bootstrap
make localnet-smoke
make localnet-build-dar
make localnet-deploy-dar
make localnet-start-control-plane
make localnet-seed-demo
make localnet-status-control-plane
make localnet-run-token-adapter
make localnet-adapter-status
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-policy-engine
make test-optimizer
make daml-build
make daml-test
make demo-run
make demo-margin-call
make demo-margin-call-quickstart
make demo-return
make demo-return-quickstart
make demo-substitution
make demo-substitution-quickstart
make test-conformance
make demo-all
make proposal-package
make status
make docs-lint
make verify-portable
make verify
```

`make localnet-bootstrap` now stages a pinned upstream CN Quickstart checkout and writes a repo-owned `.env.local` overlay without forking upstream files. `make localnet-smoke` reuses upstream Docker preflight checks and validates the composed Quickstart LocalNet configuration. `make localnet-build-dar` builds the Control Plane DAR against the pinned Quickstart runtime line through a containerized Daml `3.4.10` plus Java `21` bridge. `make localnet-deploy-dar` rebuilds that DAR and installs it into the running Quickstart app-provider and app-user participants through the upstream onboarding container. `make localnet-start-control-plane` starts the repo-owned isolated Quickstart overlay, deploys the Control Plane DAR, and writes deployment receipts. `make localnet-seed-demo` allocates the required parties and users, seeds one confidential margin-style collateral scenario on Quickstart, and writes contract receipts. `make localnet-status-control-plane` queries the running LocalNet from the provider-visible view and writes machine-readable plus Markdown status snapshots. `make localnet-run-token-adapter` consumes the seeded `SettlementInstruction`, performs the reference token movement on Quickstart, confirms workflow settlement, and emits a schema-valid adapter execution report. `make localnet-adapter-status` refreshes the provider-visible adapter receipt and holding surface. `make demo-run` exercises a real Daml workflow smoke script over the initial obligation, posting, substitution, and return skeletons. `make demo-margin-call` evaluates positive and negative margin-call scenarios, passes the positive recommendation into a Daml Script workflow path, and emits a schema-valid `ExecutionReport` plus Markdown summary and timeline artifacts on the IDE ledger. `make demo-margin-call-quickstart` runs the Quickstart-backed margin-call chain end to end across policy evaluation, optimization, Quickstart workflow preparation, reference token adapter execution, and final execution reporting. `make demo-return` evaluates the currently encumbered set, derives the returned lots from a deterministic retained-set recommendation, enforces approvals plus replay-safe release control on the Daml boundary, and emits a schema-valid `ReturnReport` plus Markdown summary and timeline artifacts. `make demo-return-quickstart` now runs the Quickstart-backed return chain end to end across retained-set selection, Quickstart workflow execution, reference token adapter release, provider-visible status refresh, approval-gated release proof, and replay-safe duplicate-request blocking. `make demo-substitution` starts from already encumbered collateral, evaluates substitution-specific positive and negative scenarios, enforces approvals plus atomicity on the Daml boundary, and emits a schema-valid `SubstitutionReport` plus Markdown summary and timeline artifacts. `make demo-substitution-quickstart` now runs the Quickstart-backed substitution chain end to end across policy evaluation, replacement selection, Quickstart substitution workflow execution, reference token adapter release plus replacement movement, provider-visible status refresh, and final substitution reporting. `make test-conformance` now refreshes Quickstart deployment evidence, validates one concrete reference token adapter proof path, and validates the three Quickstart-backed confidential workflow demo artifact chains before emitting aggregate invariant pass or fail output. `make demo-all` now packages those runtime-backed artifacts, the conformance output, the readiness assessment, and the integration-guide references into one final machine-readable demo pack. `make proposal-package` now wraps that runtime-backed package with a reviewer start path, proposal memo, walkthrough materials, and one machine-readable proposal-submission manifest. `make daml-test` runs the script-level lifecycle checks individually. `make policy-eval` validates a real policy input, evaluates normalized inventory, and emits a schema-valid `PolicyEvaluationReport`. `make optimize` validates a real policy input, optimizes against normalized inventory plus obligation inputs, and emits a schema-valid `OptimizationReport`. `make verify-portable` runs the full repository verification loop through the proposal submission package without the Docker-dependent Quickstart smoke gate. `make verify` remains the full superset and adds `make localnet-smoke` on top of the portable checks.

Current CPL artifacts:

- [docs/specs/CPL_SPEC_v0_1.md](./docs/specs/CPL_SPEC_v0_1.md)
- [docs/specs/CPL_EXAMPLES.md](./docs/specs/CPL_EXAMPLES.md)
- [schema/cpl.schema.json](./schema/cpl.schema.json)
- [docs/testing/CPL_VALIDATION_TEST_PLAN.md](./docs/testing/CPL_VALIDATION_TEST_PLAN.md)
- [docs/setup/LOCAL_DEV_SETUP.md](./docs/setup/LOCAL_DEV_SETUP.md)
- [docs/setup/DEPENDENCY_POLICY.md](./docs/setup/DEPENDENCY_POLICY.md)

Current policy-engine artifacts:

- [docs/specs/POLICY_EVALUATION_REPORT_SPEC.md](./docs/specs/POLICY_EVALUATION_REPORT_SPEC.md)
- [reports/schemas/policy-evaluation-report.schema.json](./reports/schemas/policy-evaluation-report.schema.json)
- [docs/testing/POLICY_ENGINE_TEST_PLAN.md](./docs/testing/POLICY_ENGINE_TEST_PLAN.md)
- [examples/inventory/central-bank-eligible-inventory.json](./examples/inventory/central-bank-eligible-inventory.json)
- [reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json](./reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json)

Current optimization artifacts:

- [docs/specs/OPTIMIZATION_REPORT_SPEC.md](./docs/specs/OPTIMIZATION_REPORT_SPEC.md)
- [reports/schemas/optimization-report.schema.json](./reports/schemas/optimization-report.schema.json)
- [docs/testing/OPTIMIZER_TEST_PLAN.md](./docs/testing/OPTIMIZER_TEST_PLAN.md)
- [docs/economic/OPTIMIZATION_OBJECTIVES.md](./docs/economic/OPTIMIZATION_OBJECTIVES.md)
- [examples/obligations/central-bank-window-call.json](./examples/obligations/central-bank-window-call.json)
- [reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json](./reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json)

Current execution-report artifacts:

- [docs/specs/EXECUTION_REPORT_SPEC.md](./docs/specs/EXECUTION_REPORT_SPEC.md)
- [reports/schemas/execution-report.schema.json](./reports/schemas/execution-report.schema.json)
- [docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md](./docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md)
- [examples/demo-scenarios/margin-call/demo-config.json](./examples/demo-scenarios/margin-call/demo-config.json)
- [examples/demo-scenarios/margin-call/quickstart-demo-config.json](./examples/demo-scenarios/margin-call/quickstart-demo-config.json)
- [reports/generated/margin-call-demo-execution-report.json](./reports/generated/margin-call-demo-execution-report.json)
- [reports/generated/margin-call-demo-summary.md](./reports/generated/margin-call-demo-summary.md)
- [reports/generated/margin-call-demo-timeline.md](./reports/generated/margin-call-demo-timeline.md)
- [reports/generated/margin-call-quickstart-execution-report.json](./reports/generated/margin-call-quickstart-execution-report.json)
- [reports/generated/margin-call-quickstart-summary.md](./reports/generated/margin-call-quickstart-summary.md)
- [reports/generated/margin-call-quickstart-timeline.md](./reports/generated/margin-call-quickstart-timeline.md)

Current substitution-report artifacts:

- [docs/specs/SUBSTITUTION_REPORT_SPEC.md](./docs/specs/SUBSTITUTION_REPORT_SPEC.md)
- [reports/schemas/substitution-report.schema.json](./reports/schemas/substitution-report.schema.json)
- [docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md](./docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md)
- [examples/demo-scenarios/substitution/demo-config.json](./examples/demo-scenarios/substitution/demo-config.json)
- [examples/demo-scenarios/substitution/quickstart-demo-config.json](./examples/demo-scenarios/substitution/quickstart-demo-config.json)
- [reports/generated/substitution-demo-report.json](./reports/generated/substitution-demo-report.json)
- [reports/generated/substitution-demo-summary.md](./reports/generated/substitution-demo-summary.md)
- [reports/generated/substitution-quickstart-report.json](./reports/generated/substitution-quickstart-report.json)
- [reports/generated/substitution-quickstart-summary.md](./reports/generated/substitution-quickstart-summary.md)
- [reports/generated/substitution-quickstart-timeline.md](./reports/generated/substitution-quickstart-timeline.md)
- [reports/generated/substitution-demo-timeline.md](./reports/generated/substitution-demo-timeline.md)

Current return-report artifacts:

- [docs/specs/RETURN_REPORT_SPEC.md](./docs/specs/RETURN_REPORT_SPEC.md)
- [reports/schemas/return-report.schema.json](./reports/schemas/return-report.schema.json)
- [docs/runbooks/RETURN_DEMO_RUNBOOK.md](./docs/runbooks/RETURN_DEMO_RUNBOOK.md)
- [examples/demo-scenarios/return/demo-config.json](./examples/demo-scenarios/return/demo-config.json)
- [examples/demo-scenarios/return/quickstart-demo-config.json](./examples/demo-scenarios/return/quickstart-demo-config.json)
- [reports/generated/return-demo-report.json](./reports/generated/return-demo-report.json)
- [reports/generated/return-demo-summary.md](./reports/generated/return-demo-summary.md)
- [reports/generated/return-demo-timeline.md](./reports/generated/return-demo-timeline.md)
- [reports/generated/return-quickstart-report.json](./reports/generated/return-quickstart-report.json)
- [reports/generated/return-quickstart-summary.md](./reports/generated/return-quickstart-summary.md)
- [reports/generated/return-quickstart-timeline.md](./reports/generated/return-quickstart-timeline.md)

Current conformance artifacts:

- [docs/testing/CONFORMANCE_SUITE.md](./docs/testing/CONFORMANCE_SUITE.md)
- [test/conformance/test_conformance.py](./test/conformance/test_conformance.py)
- [reports/generated/conformance-suite-report.json](./reports/generated/conformance-suite-report.json)
- [reports/generated/conformance-suite-summary.md](./reports/generated/conformance-suite-summary.md)

Current final demo-pack artifacts:

- [docs/runbooks/FINAL_DEMO_RUNBOOK.md](./docs/runbooks/FINAL_DEMO_RUNBOOK.md)
- [docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md](./docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md)
- [docs/evidence/DEMO_ARTIFACT_INDEX.md](./docs/evidence/DEMO_ARTIFACT_INDEX.md)
- [reports/generated/final-demo-pack.json](./reports/generated/final-demo-pack.json)
- [reports/generated/final-demo-pack-summary.md](./reports/generated/final-demo-pack-summary.md)

## Upcoming Phases

- Phase 0: documentation and mission-control spine
- Milestone 1 / Phase 1: Collateral Policy Language and formal model
- Milestone 2 / Phase 2: Policy engine and asset adapters
- Milestone 3 / Phase 3: Optimization and substitution engine
- Milestone 4 / Phase 4: Atomic collateral workflows and conformance suite
- Milestone 5 / Phase 5: Public release, demo environment, and adoption package
