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
| E-0003 | ADRs | [docs/adrs/0002-c-cope-solution-shape.md](../adrs/0002-c-cope-solution-shape.md) | proposal-aligned solution framing and milestone basis |
| E-0004 | Specs | [docs/mission-control/ROADMAP.md](../mission-control/ROADMAP.md) | roadmap aligned to the current proposal milestone structure |
| E-0005 | Specs | [docs/invariants/INVARIANT_REGISTRY.md](../invariants/INVARIANT_REGISTRY.md) | expanded invariant taxonomy and control properties |
| E-0006 | Specs | [docs/risks/RISK_REGISTER.md](../risks/RISK_REGISTER.md) | initial operational and architectural risk set |
| E-0007 | Security review | [docs/security/THREAT_MODEL.md](../security/THREAT_MODEL.md) | initial threat model skeleton |
| E-0008 | Tests | [docs/testing/TEST_STRATEGY.md](../testing/TEST_STRATEGY.md) | verification approach, conformance direction, and traceability expectations |
| E-0009 | Operational runbooks | [docs/runbooks/README.md](../runbooks/README.md) | runbook inventory and expectations |
| E-0010 | Demo artifacts | [docs/evidence/prompt-01-execution-report.md](./prompt-01-execution-report.md) | reproducible Prompt 1 execution record for the documentation spine |
| E-0011 | Code | [Makefile](../../Makefile) | baseline reproducible verification commands for the repo spine |
| E-0012 | Economic rationale | [docs/adrs/0002-c-cope-solution-shape.md](../adrs/0002-c-cope-solution-shape.md) | rationale for the neutral collateral control-plane framing on Canton |

## Coverage Notes

- The `Code` category is intentionally minimal because no business logic exists yet.
- The `Demo artifacts` category currently contains execution evidence for repository setup only, not workflow demos.
- Economic rationale is currently captured as architectural and ADR evidence rather than implementation-backed calibration evidence.
