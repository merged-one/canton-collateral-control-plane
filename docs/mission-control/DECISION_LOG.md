# Decision Log

This log captures concise decision records. Significant architectural or operating decisions must also have ADRs in [docs/adrs/](../adrs/).

| ID | Date | Decision | Status | Evidence |
| --- | --- | --- | --- | --- |
| D-0001 | 2026-03-28 | Establish a documentation-first control spine before adding business logic. | Accepted | [ADR 0001](../adrs/0001-repo-principles.md) |
| D-0002 | 2026-03-28 | Treat policy, optimization, workflow execution, and reporting as separate concerns from the first implementation phase onward. | Accepted | [ADR 0001](../adrs/0001-repo-principles.md) |
| D-0003 | 2026-03-28 | Use `make docs-lint`, `make status`, and `make verify` as the baseline repository control loop until pinned implementation tooling exists. | Accepted | [../../Makefile](../../Makefile), [../evidence/prompt-01-execution-report.md](../evidence/prompt-01-execution-report.md) |
| D-0004 | 2026-03-28 | Adopt the proposal's C-COPE naming and five-layer solution shape as the repository's current architectural framing. | Accepted | [ADR 0002](../adrs/0002-c-cope-solution-shape.md) |
