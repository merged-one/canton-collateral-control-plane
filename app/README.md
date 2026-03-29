# App Surface

The `app/` tree contains the prototype's small off-ledger service layer.

Current contents:

- `app/policy-engine/` for the deterministic `CPL v0.1` policy evaluation engine and CLI
- `app/optimizer/` for the deterministic best-to-post and substitution optimizer plus CLI
- `app/orchestration/` for the IDE-ledger and Quickstart-backed end-to-end margin-call, return, and substitution scenario runners, the aggregate conformance suite, and the final demo-pack generation paths

Allowed scope:

- policy evaluation helpers
- optimization orchestration
- report generation
- integration helpers

Not allowed:

- authoritative workflow state
- hidden policy semantics
- fabricated reports or demo-only shortcuts

Current boundary note:
The policy engine and optimizer may evaluate policy, rank feasible collateral sets, and produce reports, but Canton remains the intended authority for workflow state and transitions.
