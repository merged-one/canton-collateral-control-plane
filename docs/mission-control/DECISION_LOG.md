# Decision Log

This log captures concise decision records. Significant architectural or operating decisions must also have ADRs in [docs/adrs/](../adrs/).

| ID | Date | Decision | Status | Evidence |
| --- | --- | --- | --- | --- |
| D-0001 | 2026-03-28 | Establish a documentation-first control spine before adding business logic. | Accepted | [ADR 0001](../adrs/0001-repo-principles.md) |
| D-0002 | 2026-03-28 | Treat policy, optimization, workflow execution, and reporting as separate concerns from the first implementation phase onward. | Accepted | [ADR 0001](../adrs/0001-repo-principles.md) |
| D-0003 | 2026-03-28 | Use `make docs-lint`, `make status`, and `make verify` as the baseline repository control loop until pinned implementation tooling exists. | Accepted | [../../Makefile](../../Makefile), [../evidence/prompt-01-execution-report.md](../evidence/prompt-01-execution-report.md) |
| D-0004 | 2026-03-28 | Establish six explicit system boundaries: policy language, policy evaluation, optimization, workflow execution, reporting, and runtime infrastructure. | Accepted | [ADR 0002](../adrs/0002-system-boundaries.md) |
| D-0005 | 2026-03-28 | Keep policy evaluation deterministic, optimization advisory, and workflow state authoritative on Canton. | Accepted | [ADR 0003](../adrs/0003-policy-optimization-workflow-separation.md) |
| D-0006 | 2026-03-28 | Treat reports and execution evidence as state-derived outputs rather than operator-authored summaries. | Accepted | [ADR 0004](../adrs/0004-report-fidelity-and-evidence.md) |
| D-0007 | 2026-03-28 | Publish `CPL v0.1` as strict JSON validated by JSON Schema, with separate language-version and policy-version fields. | Accepted | [ADR 0005](../adrs/0005-cpl-format-and-versioning.md) |
| D-0008 | 2026-03-28 | Adopt a pinned repo-local Daml runtime foundation with checksum-verified bootstrap, a minimal executable package, and a stable build/demo command surface. | Accepted | [ADR 0006](../adrs/0006-runtime-foundation.md) |
| D-0009 | 2026-03-28 | Split the first Daml workflow package into explicit role, inventory, encumbrance, obligation, settlement, and report boundaries rather than one opaque contract set. | Accepted | [ADR 0007](../adrs/0007-daml-contract-boundaries.md) |
| D-0010 | 2026-03-28 | Implement the first deterministic `CPL v0.1` policy evaluation engine as a small off-ledger Python service with a separate machine-readable `PolicyEvaluationReport` contract. | Accepted | [ADR 0008](../adrs/0008-policy-evaluation-engine.md) |
