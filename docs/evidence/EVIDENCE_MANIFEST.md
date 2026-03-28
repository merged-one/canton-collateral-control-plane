# Evidence Manifest

This manifest defines the evidence categories required to defend changes in this repository. Evidence should be concrete, reproducible, and linked to invariants where possible.

## Evidence Categories

| Category | Purpose | Typical Contents |
| --- | --- | --- |
| Specs | Capture intended behavior and interface expectations. | architecture notes, schema docs, workflow specs |
| ADRs | Record durable design decisions and rationale. | numbered ADRs and status changes |
| Code | Preserve the implemented logic that realizes documented behavior. | versioned source, configs, scripts, lockfiles |
| Tests | Show executable verification of behavior and invariants. | unit, integration, replay, property, and scenario tests |
| Demo artifacts | Show reproducible operator-facing demonstrations backed by real execution. | commands, transcripts, generated reports, screenshots when warranted |
| Economic rationale | Explain why policy, haircut, concentration, and optimization choices are defensible. | calibration notes, assumptions, references, model commentary |
| Security review | Show confidentiality, authorization, replay, and integrity concerns were reviewed. | threat model updates, review notes, findings, mitigations |
| Operational runbooks | Show how an operator can run, verify, and recover the system safely. | bootstrap, incident, demo, release, and rollback runbooks |

## Current Evidence Inventory

| ID | Category | Artifact | Notes |
| --- | --- | --- | --- |
| E-0001 | Specs | [README.md](../../README.md) | current repository mission, historical-alias note, and control-plane versus data-plane summary |
| E-0002 | ADRs | [docs/adrs/0001-repo-principles.md](../adrs/0001-repo-principles.md) | repository principles and safety posture |
| E-0003 | ADRs | [docs/adrs/0002-system-boundaries.md](../adrs/0002-system-boundaries.md) | system-boundary definition for the control-plane architecture |
| E-0004 | Specs | [docs/mission-control/ROADMAP.md](../mission-control/ROADMAP.md) | roadmap aligned to the current proposal milestone structure |
| E-0005 | Specs | [docs/invariants/INVARIANT_REGISTRY.md](../invariants/INVARIANT_REGISTRY.md) | expanded invariant taxonomy and control properties |
| E-0006 | Specs | [docs/risks/RISK_REGISTER.md](../risks/RISK_REGISTER.md) | operational and architectural risk set |
| E-0007 | Security review | [docs/security/THREAT_MODEL.md](../security/THREAT_MODEL.md) | threat model reflecting architecture, privacy, and runtime boundaries |
| E-0008 | Tests | [docs/testing/TEST_STRATEGY.md](../testing/TEST_STRATEGY.md) | verification approach, conformance direction, and traceability expectations |
| E-0009 | Operational runbooks | [docs/runbooks/README.md](../runbooks/README.md) | runbook inventory and expectations |
| E-0010 | Demo artifacts | [docs/evidence/prompt-01-execution-report.md](./prompt-01-execution-report.md) | reproducible Prompt 1 execution record for the documentation spine |
| E-0011 | Code | [Makefile](../../Makefile) | reproducible verification commands and documentation presence checks |
| E-0012 | Economic rationale | [docs/architecture/OVERVIEW.md](../architecture/OVERVIEW.md) | rationale for the reusable Canton-native collateral control plane and boundary split |
| E-0013 | Specs | [docs/architecture/COMPONENTS.md](../architecture/COMPONENTS.md) | component responsibilities, interfaces, and dependency rules |
| E-0014 | Specs | [docs/architecture/DATA_FLOW.md](../architecture/DATA_FLOW.md) | lifecycle-aligned data flows for call, posting, substitution, return, exception, and expiry paths |
| E-0015 | Specs | [docs/architecture/DEPLOYMENT_MODEL.md](../architecture/DEPLOYMENT_MODEL.md) | Quickstart-based LocalNet deployment boundaries and runtime layering |
| E-0016 | Security review | [docs/architecture/PRIVACY_MODEL.md](../architecture/PRIVACY_MODEL.md) | role visibility model and Canton privacy mapping |
| E-0017 | ADRs | [docs/adrs/0003-policy-optimization-workflow-separation.md](../adrs/0003-policy-optimization-workflow-separation.md) | policy, optimization, and workflow separation decision |
| E-0018 | ADRs | [docs/adrs/0004-report-fidelity-and-evidence.md](../adrs/0004-report-fidelity-and-evidence.md) | report fidelity and evidence-generation decision |
| E-0019 | Specs | [docs/domain/COLLATERAL_DOMAIN_MODEL.md](../domain/COLLATERAL_DOMAIN_MODEL.md) | canonical collateral entities, roles, and relationships |
| E-0020 | Specs | [docs/domain/ACTORS_AND_ROLES.md](../domain/ACTORS_AND_ROLES.md) | actor separation of duties and approval expectations |
| E-0021 | Specs | [docs/domain/LIFECYCLE_STATES.md](../domain/LIFECYCLE_STATES.md) | workflow states and transition guards |
| E-0022 | Specs | [docs/integration/QUICKSTART_INTEGRATION_PLAN.md](../integration/QUICKSTART_INTEGRATION_PLAN.md) | LocalNet integration plan with overlays and adjacent services |
| E-0023 | Specs | [docs/integration/TOKEN_STANDARD_ALIGNMENT.md](../integration/TOKEN_STANDARD_ALIGNMENT.md) | asset representation and future Canton integration boundaries |
| E-0024 | Demo artifacts | [docs/evidence/prompt-02-execution-report.md](./prompt-02-execution-report.md) | reproducible Prompt 2 execution record for the architecture and domain package |
| E-0025 | Specs | [docs/specs/CPL_SPEC_v0_1.md](../specs/CPL_SPEC_v0_1.md) | normative `CPL v0.1` format, semantics, and market-practice mapping |
| E-0026 | Code | [schema/cpl.schema.json](../../schema/cpl.schema.json) | machine-readable `CPL v0.1` schema with strict field validation |
| E-0027 | Specs | [docs/specs/CPL_EXAMPLES.md](../specs/CPL_EXAMPLES.md) | explanation of the central-bank-style, tri-party-style, CCP-style, and bilateral examples |
| E-0028 | ADRs | [docs/adrs/0005-cpl-format-and-versioning.md](../adrs/0005-cpl-format-and-versioning.md) | canonical format, versioning, and validation decision for `CPL v0.1` |
| E-0029 | Tests | [docs/testing/CPL_VALIDATION_TEST_PLAN.md](../testing/CPL_VALIDATION_TEST_PLAN.md) | first executable validation scope for schema, positive examples, and negative cases |
| E-0030 | Code | [requirements-cpl-validation.txt](../../requirements-cpl-validation.txt) | pinned validation dependency for the repo-local CPL validation toolchain |
| E-0031 | Demo artifacts | [docs/evidence/prompt-03-execution-report.md](./prompt-03-execution-report.md) | reproducible Prompt 3 execution record for the CPL specification and schema package |
| E-0032 | ADRs | [docs/adrs/0006-runtime-foundation.md](../adrs/0006-runtime-foundation.md) | pinned Daml-centric runtime-foundation decision |
| E-0033 | Code | [daml.yaml](../../daml.yaml) | pinned Daml project definition and init script |
| E-0034 | Code | [scripts/toolchain.env](../../scripts/toolchain.env) | shared version pins, download URLs, and checksums for the runtime bootstrap |
| E-0035 | Code | [scripts/bootstrap.sh](../../scripts/bootstrap.sh) | repo-local checksum-verified toolchain bootstrap |
| E-0036 | Code | [daml/Bootstrap.daml](../../daml/Bootstrap.daml) | aggregate executable Daml workflow smoke scenario over the initial lifecycle scripts |
| E-0037 | Operational runbooks | [docs/setup/LOCAL_DEV_SETUP.md](../setup/LOCAL_DEV_SETUP.md) | reproducible local bootstrap and command guide |
| E-0038 | Specs | [docs/setup/DEPENDENCY_POLICY.md](../setup/DEPENDENCY_POLICY.md) | pinned dependency and service-layer policy |
| E-0039 | Demo artifacts | [docs/evidence/prompt-04-execution-report.md](./prompt-04-execution-report.md) | reproducible Prompt 4 execution record for the runtime foundation |
| E-0040 | Specs | [docs/domain/DAML_MAPPING.md](../domain/DAML_MAPPING.md) | domain-to-Daml mapping for the first workflow package boundary |
| E-0041 | ADRs | [docs/adrs/0007-daml-contract-boundaries.md](../adrs/0007-daml-contract-boundaries.md) | contract-boundary decision for the first Daml workflow package |
| E-0042 | Code | [daml/CantonCollateral](../../daml/CantonCollateral) | initial Daml workflow modules for roles, inventory, encumbrance, obligations, posting, substitution, return, settlement, and reports |
| E-0043 | Tests | [docs/testing/DAML_TEST_PLAN.md](../testing/DAML_TEST_PLAN.md) | executable Daml script coverage for the first lifecycle skeletons |
| E-0044 | Demo artifacts | [docs/evidence/prompt-05-execution-report.md](./prompt-05-execution-report.md) | reproducible Prompt 5 execution record for the first Daml workflow skeleton package |
| E-0045 | ADRs | [docs/adrs/0008-policy-evaluation-engine.md](../adrs/0008-policy-evaluation-engine.md) | first deterministic off-ledger policy-engine and report-contract decision |
| E-0046 | Code | [app/policy-engine](../../app/policy-engine) | deterministic `CPL v0.1` policy-engine implementation and CLI |
| E-0047 | Specs | [docs/specs/POLICY_EVALUATION_REPORT_SPEC.md](../specs/POLICY_EVALUATION_REPORT_SPEC.md) | normative report contract, deterministic rules, and scope notes for `PolicyEvaluationReport` |
| E-0048 | Code | [reports/schemas/policy-evaluation-report.schema.json](../../reports/schemas/policy-evaluation-report.schema.json) | canonical machine-readable schema for `PolicyEvaluationReport` |
| E-0049 | Tests | [docs/testing/POLICY_ENGINE_TEST_PLAN.md](../testing/POLICY_ENGINE_TEST_PLAN.md) | scenario coverage for eligibility, haircuts, concentration, wrong-way risk, control failures, and determinism |
| E-0050 | Demo artifacts | [reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json](../../reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json) | real generated policy-evaluation artifact from `make policy-eval` |
| E-0051 | Demo artifacts | [docs/evidence/prompt-06-execution-report.md](./prompt-06-execution-report.md) | reproducible Prompt 6 execution record for the first policy-engine package |
| E-0052 | ADRs | [docs/adrs/0010-rename-to-canton-collateral-control-plane.md](../adrs/0010-rename-to-canton-collateral-control-plane.md) | repository-identity rename plus control-plane versus data-plane clarification |
| E-0053 | Demo artifacts | [docs/evidence/rename-to-collateral-control-plane-execution-report.md](./rename-to-collateral-control-plane-execution-report.md) | reproducible execution record for the repository rename and metadata update |
| E-0054 | ADRs | [docs/adrs/0009-optimization-objective-and-determinism.md](../adrs/0009-optimization-objective-and-determinism.md) | first optimizer objective, deterministic search, and no-churn substitution decision |
| E-0055 | Code | [app/optimizer](../../app/optimizer) | deterministic optimizer implementation and CLI |
| E-0056 | Specs | [docs/specs/OPTIMIZATION_REPORT_SPEC.md](../specs/OPTIMIZATION_REPORT_SPEC.md) | normative report contract, deterministic search rules, and scope notes for `OptimizationReport` |
| E-0057 | Code | [reports/schemas/optimization-report.schema.json](../../reports/schemas/optimization-report.schema.json) | canonical machine-readable schema for `OptimizationReport` |
| E-0058 | Tests | [docs/testing/OPTIMIZER_TEST_PLAN.md](../testing/OPTIMIZER_TEST_PLAN.md) | scenario coverage for best-to-post, concentration-aware allocation, substitution, no-solution handling, and determinism |
| E-0059 | Economic rationale | [docs/economic/OPTIMIZATION_OBJECTIVES.md](../economic/OPTIMIZATION_OBJECTIVES.md) | institutional rationale for best-to-post, concentration control, substitution economics, and deterministic explainability |
| E-0060 | Demo artifacts | [reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json](../../reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json) | real generated optimization artifact from `make optimize` |
| E-0061 | Demo artifacts | [docs/evidence/prompt-07-execution-report.md](./prompt-07-execution-report.md) | reproducible Prompt 7 execution record for the first optimizer package |
| E-0062 | ADRs | [docs/adrs/0013-quickstart-demo-foundation.md](../adrs/0013-quickstart-demo-foundation.md) | pinned Quickstart demo foundation and overlay-first LocalNet decision |
| E-0063 | Code | [infra/quickstart/bootstrap-localnet.sh](../../infra/quickstart/bootstrap-localnet.sh) | pinned upstream CN Quickstart bootstrap and `.env.local` overlay writer |
| E-0064 | Code | [scripts/run-localnet-smoke.sh](../../scripts/run-localnet-smoke.sh) | upstream Docker preflight plus compose-config smoke for the pinned Quickstart stack |
| E-0065 | Specs | [docs/integration/LOCALNET_DEMO_PLAN.md](../integration/LOCALNET_DEMO_PLAN.md) | staged path from the current Quickstart foundation to a real confidential collateral demo |
| E-0066 | Specs | [docs/integration/ASSET_ADAPTER_PLAN.md](../integration/ASSET_ADAPTER_PLAN.md) | staged path from normalized inventory inputs to live token-standard-style asset adapters |
| E-0067 | Code | [infra/quickstart/overlay](../../infra/quickstart/overlay) | pinned upstream metadata and overlay profiles for Quickstart LocalNet staging |
| E-0068 | Demo artifacts | [docs/evidence/prompt-08-execution-report.md](./prompt-08-execution-report.md) | reproducible Prompt 8 execution record for the Quickstart LocalNet foundation |
| E-0069 | ADRs | [docs/adrs/0011-margin-call-demo-shape.md](../adrs/0011-margin-call-demo-shape.md) | first end-to-end margin-call demo shape and execution-report decision |
| E-0070 | Code | [app/orchestration](../../app/orchestration) | orchestration layer for the end-to-end margin-call and substitution demos plus report generation |
| E-0071 | Specs | [docs/specs/EXECUTION_REPORT_SPEC.md](../specs/EXECUTION_REPORT_SPEC.md) | normative contract and scope notes for the first end-to-end `ExecutionReport` |
| E-0072 | Code | [reports/schemas/execution-report.schema.json](../../reports/schemas/execution-report.schema.json) | canonical machine-readable schema for the first end-to-end execution artifact |
| E-0073 | Code | [examples/demo-scenarios/margin-call](../../examples/demo-scenarios/margin-call) | reproducible positive and negative demo inputs for the margin-call scenario runner |
| E-0074 | Demo artifacts | [reports/generated/margin-call-demo-execution-report.json](../../reports/generated/margin-call-demo-execution-report.json) | real end-to-end execution artifact from `make demo-margin-call` |
| E-0075 | Operational runbooks | [docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md](../runbooks/MARGIN_CALL_DEMO_RUNBOOK.md) | operator procedure for the end-to-end margin-call demo |
| E-0076 | Demo artifacts | [docs/evidence/prompt-09-execution-report.md](./prompt-09-execution-report.md) | reproducible Prompt 9 execution record for the first end-to-end margin-call prototype |
| E-0077 | ADRs | [docs/adrs/0012-substitution-atomicity.md](../adrs/0012-substitution-atomicity.md) | substitution-scope, approval-gate, and atomicity decision for the first end-to-end substitution prototype |
| E-0078 | Specs | [docs/specs/SUBSTITUTION_REPORT_SPEC.md](../specs/SUBSTITUTION_REPORT_SPEC.md) | normative contract and scope notes for the first end-to-end `SubstitutionReport` |
| E-0079 | Code | [reports/schemas/substitution-report.schema.json](../../reports/schemas/substitution-report.schema.json) | canonical machine-readable schema for the first substitution execution artifact |
| E-0080 | Code | [examples/demo-scenarios/substitution](../../examples/demo-scenarios/substitution) | reproducible positive and negative demo inputs for the substitution scenario runner |
| E-0081 | Demo artifacts | [reports/generated/substitution-demo-report.json](../../reports/generated/substitution-demo-report.json) | real end-to-end substitution artifact from `make demo-substitution` |
| E-0082 | Operational runbooks | [docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md](../runbooks/SUBSTITUTION_DEMO_RUNBOOK.md) | operator procedure for the end-to-end substitution demo |
| E-0083 | Demo artifacts | [docs/evidence/prompt-10-execution-report.md](./prompt-10-execution-report.md) | reproducible Prompt 10 execution record for the first end-to-end substitution prototype |

## Coverage Notes

- The `Code` category now includes the first Daml workflow skeleton package in addition to schema, bootstrap, and toolchain artifacts.
- The architecture, CPL, policy-engine, optimizer, Daml-boundary, and Quickstart-foundation packages now provide executable evidence, though adapter integration and workflow-coupled reference-data evidence are still pending.
- The `Demo artifacts` category now includes the first end-to-end margin-call and substitution reports plus their supporting policy, optimization, workflow, and prompt evidence artifacts, but still not a Quickstart-backed deployment proof.
- The evidence set now records the rename to "Canton Collateral Control Plane" as a semantic clarification of the same subsystem stack rather than a new product direction.
- Economic rationale is now architecture-, control-, and optimization-objective-oriented rather than calibration-backed.
