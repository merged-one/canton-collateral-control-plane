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
| E-0001 | Specs | [README.md](../../README.md) | proposal-aligned repository mission and architecture summary |
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
| E-0036 | Code | [daml/Bootstrap.daml](../../daml/Bootstrap.daml) | minimal executable Daml smoke scenario proving compile-and-run readiness |
| E-0037 | Operational runbooks | [docs/setup/LOCAL_DEV_SETUP.md](../setup/LOCAL_DEV_SETUP.md) | reproducible local bootstrap and command guide |
| E-0038 | Specs | [docs/setup/DEPENDENCY_POLICY.md](../setup/DEPENDENCY_POLICY.md) | pinned dependency and service-layer policy |
| E-0039 | Demo artifacts | [docs/evidence/prompt-04-execution-report.md](./prompt-04-execution-report.md) | reproducible Prompt 4 execution record for the runtime foundation |

## Coverage Notes

- The `Code` category now includes schema, bootstrap, toolchain, and minimal Daml foundation artifacts, but still no collateral business logic.
- The architecture and CPL packages now provide stronger design evidence, but not executable workflow evidence.
- The `Demo artifacts` category now includes a runtime-foundation smoke-run record, but still not end-to-end collateral workflow runs.
- Economic rationale is currently architecture-, control-, and market-practice-oriented rather than calibration-backed.
