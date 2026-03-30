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
| E-0062 | ADRs | [docs/adrs/0015-quickstart-demo-foundation.md](../adrs/0015-quickstart-demo-foundation.md) | pinned Quickstart demo foundation and overlay-first LocalNet decision |
| E-0063 | Code | [infra/quickstart/bootstrap-localnet.sh](../../infra/quickstart/bootstrap-localnet.sh) | pinned upstream CN Quickstart bootstrap and `.env.local` overlay writer |
| E-0064 | Code | [scripts/run-localnet-smoke.sh](../../scripts/run-localnet-smoke.sh) | upstream Docker preflight plus compose-config smoke for the pinned Quickstart stack |
| E-0065 | Specs | [docs/integration/LOCALNET_DEMO_PLAN.md](../integration/LOCALNET_DEMO_PLAN.md) | staged path from the current Quickstart foundation to a real confidential collateral demo |
| E-0066 | Specs | [docs/integration/ASSET_ADAPTER_PLAN.md](../integration/ASSET_ADAPTER_PLAN.md) | staged path from normalized inventory inputs to live token-standard-style asset adapters |
| E-0067 | Code | [infra/quickstart/overlay](../../infra/quickstart/overlay) | pinned upstream metadata and overlay profiles for Quickstart LocalNet staging |
| E-0068 | Demo artifacts | [docs/evidence/prompt-08-execution-report.md](./prompt-08-execution-report.md) | reproducible Prompt 8 execution record for the Quickstart LocalNet foundation |
| E-0069 | ADRs | [docs/adrs/0011-margin-call-demo-shape.md](../adrs/0011-margin-call-demo-shape.md) | first end-to-end margin-call demo shape and execution-report decision |
| E-0070 | Code | [app/orchestration](../../app/orchestration) | orchestration layer for the end-to-end margin-call, return, and substitution demos plus report generation |
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
| E-0084 | ADRs | [docs/adrs/0013-return-and-release-control.md](../adrs/0013-return-and-release-control.md) | retained-set return control, replay safety, and return-report decision |
| E-0085 | Specs | [docs/specs/RETURN_REPORT_SPEC.md](../specs/RETURN_REPORT_SPEC.md) | normative contract and scope notes for the first end-to-end `ReturnReport` |
| E-0086 | Code | [reports/schemas/return-report.schema.json](../../reports/schemas/return-report.schema.json) | canonical machine-readable schema for the first return execution artifact |
| E-0087 | Code | [examples/demo-scenarios/return](../../examples/demo-scenarios/return) | reproducible positive and negative demo inputs for the return scenario runner |
| E-0088 | Demo artifacts | [reports/generated/return-demo-report.json](../../reports/generated/return-demo-report.json) | real end-to-end return artifact from `make demo-return` |
| E-0089 | Operational runbooks | [docs/runbooks/RETURN_DEMO_RUNBOOK.md](../runbooks/RETURN_DEMO_RUNBOOK.md) | operator procedure for the end-to-end return demo |
| E-0090 | Demo artifacts | [docs/evidence/prompt-11-execution-report.md](./prompt-11-execution-report.md) | reproducible Prompt 11 execution record for the first end-to-end return prototype |
| E-0091 | ADRs | [docs/adrs/0014-conformance-and-demo-package.md](../adrs/0014-conformance-and-demo-package.md) | aggregate conformance-suite and final demo-pack packaging decision |
| E-0092 | Tests | [docs/testing/CONFORMANCE_SUITE.md](../testing/CONFORMANCE_SUITE.md) | aggregate invariant-verification scope, command surface, and operator checks |
| E-0093 | Tests | [test/conformance/test_conformance.py](../../test/conformance/test_conformance.py) | executable assertions over the generated conformance-suite report |
| E-0094 | Operational runbooks | [docs/runbooks/FINAL_DEMO_RUNBOOK.md](../runbooks/FINAL_DEMO_RUNBOOK.md) | operator procedure for the final packaged confidential workflow demonstration |
| E-0095 | Specs | [docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md](../integration/THIRD_PARTY_INTEGRATION_GUIDE.md) | boundary-level integration contract guidance for venues, financing apps, token issuers, custodians, and future Canton projects |
| E-0096 | Demo artifacts | [docs/evidence/DEMO_ARTIFACT_INDEX.md](./DEMO_ARTIFACT_INDEX.md) | reviewer-facing index for the generated demo package and supporting artifacts |
| E-0097 | Demo artifacts | [reports/generated/conformance-suite-report.json](../../reports/generated/conformance-suite-report.json) | real Quickstart-backed aggregate invariant pass/fail output from `make test-conformance` |
| E-0098 | Demo artifacts | [reports/generated/final-demo-pack.json](../../reports/generated/final-demo-pack.json) | real Quickstart-centered final packaged prototype evidence index from `make demo-all` |
| E-0099 | Demo artifacts | [docs/evidence/prompt-12-execution-report.md](./prompt-12-execution-report.md) | reproducible Prompt 12 execution record for the conformance suite and final demo pack |
| E-0100 | Tests | [test/conformance/test_conformance_checks.py](../../test/conformance/test_conformance_checks.py) | isolated unit assertions over conformance helper rules so report-level and rule-level regressions can fail independently |
| E-0101 | Code | [testsupport/fixture_builders.py](../../testsupport/fixture_builders.py) | shared deterministic fixture builders for the Python policy-engine and optimizer suites |
| E-0102 | Code | [scripts/verify-portable.sh](../../scripts/verify-portable.sh) | Docker-free portable verification loop that preserves the full Quickstart smoke gate as a separate superset |
| E-0103 | ADRs | [docs/adrs/0016-quickstart-runtime-bridge.md](../adrs/0016-quickstart-runtime-bridge.md) | explicit dual-runtime bridge decision between the repo host toolchain and the pinned Quickstart runtime line |
| E-0104 | Code | [scripts/build-quickstart-dar.sh](../../scripts/build-quickstart-dar.sh) | containerized Daml `3.4.10` plus Java `21` bridge that builds a Quickstart-compatible Control Plane DAR from the shared source tree |
| E-0105 | Code | [scripts/localnet-deploy-dar.sh](../../scripts/localnet-deploy-dar.sh) | pinned Quickstart package-install command that uploads the Control Plane DAR through the upstream onboarding container |
| E-0106 | Demo artifacts | [docs/evidence/prompt-13-execution-report.md](./prompt-13-execution-report.md) | reproducible Prompt 13 execution record for the Quickstart runtime bridge and package deployment proof |
| E-0107 | ADRs | [docs/adrs/0017-quickstart-confidential-seed.md](../adrs/0017-quickstart-confidential-seed.md) | overlay-first decision for starting Quickstart, seeding one confidential scenario, and querying provider-visible status without forking upstream |
| E-0108 | Code | [infra/quickstart/overlay/control-plane-compose.yaml](../../infra/quickstart/overlay/control-plane-compose.yaml) | repo-owned compose override that isolates the Control Plane LocalNet stack by container name while preserving upstream compose files |
| E-0109 | Code | [daml/CantonCollateral/QuickstartSeed.daml](../../daml/CantonCollateral/QuickstartSeed.daml) | multi-participant Daml Script layer for Quickstart seeding and provider-visible status queries |
| E-0110 | Code | [scripts/localnet-control-plane-common.sh](../../scripts/localnet-control-plane-common.sh) | shared Quickstart control-plane runtime, auth-export, participant-config, and artifact helper functions |
| E-0111 | Code | [scripts/run-quickstart-daml-script.sh](../../scripts/run-quickstart-daml-script.sh) | containerized Daml Script runner that executes the shared Quickstart seed or status scripts against the pinned runtime line |
| E-0112 | Code | [scripts/localnet-start-control-plane.sh](../../scripts/localnet-start-control-plane.sh) | isolated Quickstart overlay startup and Control Plane package deployment command |
| E-0113 | Code | [scripts/localnet-seed-demo.sh](../../scripts/localnet-seed-demo.sh) | default confidential-scenario seeding command for the Quickstart LocalNet |
| E-0114 | Code | [scripts/localnet-status-control-plane.sh](../../scripts/localnet-status-control-plane.sh) | provider-visible Quickstart status query and Markdown summary generator |
| E-0115 | Code | [infra/quickstart/scenarios/confidential-margin-scenario.json](../../infra/quickstart/scenarios/confidential-margin-scenario.json) | declared default Quickstart seed manifest for one confidential margin-style collateral scenario |
| E-0116 | Operational runbooks | [docs/runbooks/LOCALNET_CONTROL_PLANE_RUNBOOK.md](../runbooks/LOCALNET_CONTROL_PLANE_RUNBOOK.md) | bootstrap, start, deploy, seed, inspect, teardown, and failure-handling guide for the Quickstart-backed Control Plane scenario |
| E-0117 | Demo artifacts | [reports/generated/localnet-control-plane-deployment-receipt.json](../../reports/generated/localnet-control-plane-deployment-receipt.json) | machine-readable proof that the Control Plane DAR was deployed into the pinned Quickstart participants |
| E-0118 | Demo artifacts | [reports/generated/localnet-control-plane-seed-receipt.json](../../reports/generated/localnet-control-plane-seed-receipt.json) | machine-readable proof that the default confidential scenario was seeded on Quickstart with ledger-returned contract identifiers |
| E-0119 | Demo artifacts | [reports/generated/localnet-control-plane-status.json](../../reports/generated/localnet-control-plane-status.json) | machine-readable provider-visible Quickstart ledger snapshot for the seeded scenario |
| E-0120 | Demo artifacts | [docs/evidence/prompt-14-execution-report.md](./prompt-14-execution-report.md) | reproducible Prompt 14 execution record for the Quickstart overlay start, seed, and status proof |
| E-0121 | ADRs | [docs/adrs/0018-reference-token-adapter-path.md](../adrs/0018-reference-token-adapter-path.md) | decision for the first narrow Quickstart-backed reference token adapter boundary |
| E-0122 | Code | [daml/CantonCollateral/ReferenceToken.daml](../../daml/CantonCollateral/ReferenceToken.daml) | reference token holding and adapter receipt contracts that model the asset-side reference path |
| E-0123 | Code | [daml/CantonCollateral/QuickstartAdapter.daml](../../daml/CantonCollateral/QuickstartAdapter.daml) | Quickstart-backed Daml Script layer that consumes workflow settlement outputs and drives the reference token adapter path |
| E-0124 | Code | [scripts/localnet-run-token-adapter.sh](../../scripts/localnet-run-token-adapter.sh) | reproducible operator command for adapter execution and artifact generation on the running Quickstart LocalNet |
| E-0125 | Code | [scripts/localnet-adapter-status.sh](../../scripts/localnet-adapter-status.sh) | reproducible provider-visible adapter status query and summary generation command |
| E-0126 | Code | [reports/schemas/adapter-execution-report.schema.json](../../reports/schemas/adapter-execution-report.schema.json) | canonical machine-readable schema for the Quickstart reference token adapter execution artifact |
| E-0127 | Demo artifacts | [reports/generated/localnet-reference-token-adapter-execution-report.json](../../reports/generated/localnet-reference-token-adapter-execution-report.json) | real Quickstart-backed adapter execution artifact proving settlement-instruction consumption and token-style movement |
| E-0128 | Demo artifacts | [reports/generated/localnet-reference-token-adapter-status.json](../../reports/generated/localnet-reference-token-adapter-status.json) | real provider-visible adapter status artifact showing holdings, encumbrances, execution report count, and adapter receipt count after execution |
| E-0129 | Demo artifacts | [docs/evidence/prompt-15-execution-report.md](./prompt-15-execution-report.md) | reproducible Prompt 15 execution record for the first Quickstart-backed reference token adapter path |
| E-0130 | ADRs | [docs/adrs/0019-quickstart-margin-call-demo-orchestration.md](../adrs/0019-quickstart-margin-call-demo-orchestration.md) | decision for the Quickstart-backed margin-call orchestration path and workflow-to-adapter handoff discipline |
| E-0131 | Code | [daml/CantonCollateral/QuickstartMarginCall.daml](../../daml/CantonCollateral/QuickstartMarginCall.daml) | Quickstart-backed Daml Script layer that advances seeded margin-call workflow state to the adapter handoff point or a deterministic workflow gate |
| E-0132 | Code | [scripts/localnet-run-margin-call-workflow.sh](../../scripts/localnet-run-margin-call-workflow.sh) | reproducible operator command for Quickstart margin-call workflow preparation and artifact generation |
| E-0133 | Code | [examples/demo-scenarios/margin-call/quickstart-demo-config.json](../../examples/demo-scenarios/margin-call/quickstart-demo-config.json) | declared positive and negative Quickstart-backed margin-call scenarios including workflow-gate and adapter expectations |
| E-0134 | Demo artifacts | [docs/evidence/prompt-16-execution-report.md](./prompt-16-execution-report.md) | reproducible Prompt 16 execution record for the Quickstart-backed end-to-end margin-call chain |
| E-0135 | Demo artifacts | [reports/generated/margin-call-quickstart-execution-report.json](../../reports/generated/margin-call-quickstart-execution-report.json) | real Quickstart-backed end-to-end margin-call execution artifact chaining policy, optimization, workflow, adapter, and blocked-path evidence |
| E-0136 | ADRs | [docs/adrs/0020-quickstart-substitution-demo-orchestration.md](../adrs/0020-quickstart-substitution-demo-orchestration.md) | decision for the Quickstart-backed substitution orchestration path and workflow-to-adapter atomicity discipline |
| E-0137 | Code | [daml/CantonCollateral/QuickstartSubstitution.daml](../../daml/CantonCollateral/QuickstartSubstitution.daml) | Quickstart-backed Daml Script layer that seeds confidential substitution scenarios, advances substitution workflow state, and exposes substitution-specific adapter and status queries |
| E-0138 | Code | [scripts/localnet-seed-substitution-demo.sh](../../scripts/localnet-seed-substitution-demo.sh) | reproducible operator command for seeding scenario-scoped Quickstart substitution state and emitting a seed receipt |
| E-0139 | Code | [scripts/localnet-run-substitution-workflow.sh](../../scripts/localnet-run-substitution-workflow.sh) | reproducible operator command for advancing the Quickstart substitution workflow to settlement preparation or a deterministic blocked state |
| E-0140 | Code | [scripts/localnet-run-substitution-token-adapter.sh](../../scripts/localnet-run-substitution-token-adapter.sh) | reproducible operator command for driving the reference token replacement or release path from a real substitution settlement instruction |
| E-0141 | Code | [scripts/localnet-substitution-status.sh](../../scripts/localnet-substitution-status.sh) | reproducible provider-visible substitution status query covering holdings, encumbrances, workflow status, and adapter receipts |
| E-0142 | Code | [examples/demo-scenarios/substitution/quickstart-demo-config.json](../../examples/demo-scenarios/substitution/quickstart-demo-config.json) | declared positive and negative Quickstart-backed substitution scenarios including policy-blocked and partial-substitution-blocked expectations |
| E-0143 | Code | [infra/quickstart/scenarios/confidential-substitution-demo-positive-scenario.json](../../infra/quickstart/scenarios/confidential-substitution-demo-positive-scenario.json) | declared Quickstart seed manifest for the positive confidential substitution scenario, paired with the blocked partial-substitution manifest in the same directory |
| E-0144 | Demo artifacts | [docs/evidence/prompt-17-execution-report.md](./prompt-17-execution-report.md) | reproducible Prompt 17 execution record for the Quickstart-backed end-to-end substitution chain |
| E-0145 | Demo artifacts | [reports/generated/substitution-quickstart-report.json](../../reports/generated/substitution-quickstart-report.json) | real Quickstart-backed end-to-end substitution execution artifact proving atomic replacement on the positive path and blocked partial substitution with no adapter side effects |
| E-0146 | ADRs | [docs/adrs/0021-quickstart-return-demo-orchestration.md](../adrs/0021-quickstart-return-demo-orchestration.md) | decision for the Quickstart-backed return orchestration path and workflow-to-adapter replay-safety discipline |
| E-0147 | Code | [daml/CantonCollateral/QuickstartReturn.daml](../../daml/CantonCollateral/QuickstartReturn.daml) | Quickstart-backed Daml Script layer that seeds confidential return scenarios, advances return workflow state, drives replay-safe adapter confirmation, and exposes provider-visible return status |
| E-0148 | Code | [scripts/localnet-seed-return-demo.sh](../../scripts/localnet-seed-return-demo.sh) | reproducible operator command for seeding scenario-scoped Quickstart return state and emitting a seed receipt |
| E-0149 | Code | [scripts/localnet-run-return-workflow.sh](../../scripts/localnet-run-return-workflow.sh) | reproducible operator command for advancing the Quickstart return workflow to settlement preparation or a deterministic blocked state |
| E-0150 | Code | [scripts/localnet-run-return-token-adapter.sh](../../scripts/localnet-run-return-token-adapter.sh) | reproducible operator command for driving the reference token release path from a real return settlement instruction |
| E-0151 | Code | [scripts/localnet-return-status.sh](../../scripts/localnet-return-status.sh) | reproducible provider-visible return status query covering holdings, encumbrances, workflow status, and adapter receipts |
| E-0152 | Code | [examples/demo-scenarios/return/quickstart-demo-config.json](../../examples/demo-scenarios/return/quickstart-demo-config.json) | declared positive and negative Quickstart-backed return scenarios including approval-gated release, replay blocking, and stale-coverage expectations |
| E-0153 | Code | [infra/quickstart/scenarios/confidential-return-demo-positive-scenario.json](../../infra/quickstart/scenarios/confidential-return-demo-positive-scenario.json) | declared Quickstart seed manifest for the positive confidential return scenario, paired with the unauthorized, replay, and stale-coverage manifests in the same directory |
| E-0154 | Demo artifacts | [docs/evidence/prompt-18-execution-report.md](./prompt-18-execution-report.md) | reproducible Prompt 18 execution record for the Quickstart-backed end-to-end return chain |
| E-0155 | Demo artifacts | [reports/generated/return-quickstart-report.json](../../reports/generated/return-quickstart-report.json) | real Quickstart-backed end-to-end return execution artifact proving approval-gated release, replay-safe return handling, and blocked unauthorized release with no adapter side effects |
| E-0156 | ADRs | [docs/adrs/0022-quickstart-conformance-and-demo-package.md](../adrs/0022-quickstart-conformance-and-demo-package.md) | decision to center conformance and final demo packaging on Quickstart deployment, reference-adapter proof, and runtime-backed demo evidence |
| E-0157 | Specs | [docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md](./PROPOSAL_READINESS_ASSESSMENT.md) | explicit reviewer-facing assessment of what is real on Quickstart, what machine-readable artifacts prove, and what remains staged |
| E-0158 | Demo artifacts | [docs/evidence/prompt-19-execution-report.md](./prompt-19-execution-report.md) | reproducible Prompt 19 execution record for the Quickstart-centered conformance and final demo package rebuild |
| E-0159 | ADRs | [docs/adrs/0023-proposal-submission-wrapper.md](../adrs/0023-proposal-submission-wrapper.md) | decision to add a reviewer-facing proposal-submission wrapper around the runtime-backed final demo pack |
| E-0160 | Code | [app/orchestration/proposal_submission_pack.py](../../app/orchestration/proposal_submission_pack.py) | proposal-submission manifest generator that derives reviewer-facing packaging from the generated final demo pack |
| E-0161 | Specs | [docs/evidence/REVIEWER_START_HERE.md](./REVIEWER_START_HERE.md) | shortest reviewer path from repo entrypoint to generated proposal evidence |
| E-0162 | Specs | [docs/evidence/PROPOSAL_SUBMISSION_MEMO.md](./PROPOSAL_SUBMISSION_MEMO.md) | concise reviewer memo stating what is real, what proves it, and what remains staged |
| E-0163 | Demo artifacts | [docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md](./PROPOSAL_WALKTHROUGH_SCRIPT.md) | repo-tracked walkthrough script for reviewer replay or live presentation |
| E-0165 | Demo artifacts | [reports/generated/proposal-submission-manifest.json](../../reports/generated/proposal-submission-manifest.json) | machine-readable reviewer-facing wrapper over the Quickstart-backed proposal proof set |
| E-0166 | Demo artifacts | [docs/evidence/prompt-20-execution-report.md](./prompt-20-execution-report.md) | reproducible Prompt 20 execution record for the proposal-submission package and reviewer kit |

## Coverage Notes

- The `Code` category now includes the first Daml workflow skeleton package in addition to schema, bootstrap, and toolchain artifacts.
- The `Code` category now also includes the Quickstart seed or status Daml Script layer plus the overlay-specific startup, auth, and status scripts that turn package deployment into a seeded LocalNet scenario.
- The architecture, CPL, policy-engine, optimizer, Daml-boundary, Quickstart-foundation, Quickstart workflow-orchestration layers, reference-adapter path, and Quickstart-centered conformance or packaging surfaces now provide executable evidence, though broader adapter coverage and workflow-coupled reference-data evidence are still pending.
- The `Demo artifacts` category now includes the end-to-end margin-call, return, and substitution reports plus their supporting policy, optimization, workflow, conformance, final demo-pack, readiness-assessment, and prompt evidence artifacts, the Quickstart-backed package deployment proof, one concrete reference token adapter proof path, the first Quickstart-backed end-to-end margin-call chain evidence, the first Quickstart-backed atomic substitution evidence chain, and the first Quickstart-backed replay-safe return evidence chain.
- The `Demo artifacts` category now also includes a reviewer-facing proposal-submission manifest plus a repo-tracked walkthrough script that stay pinned to the generated Quickstart proof set.
- The evidence set now records the rename to "Canton Collateral Control Plane" as a semantic clarification of the same subsystem stack rather than a new product direction.
- The evidence set now includes an explicit third-party integration guide, a reviewer-facing demo artifact index, and a reviewer start or memo surface so future Canton projects and proposal reviewers can consume the prototype through declared interfaces instead of reverse-engineering incidental file shapes.
- Economic rationale is now architecture-, control-, and optimization-objective-oriented rather than calibration-backed.
- The test evidence set now distinguishes shared deterministic fixture builders, isolated conformance-helper checks, and portable versus Docker-backed verification command surfaces.
