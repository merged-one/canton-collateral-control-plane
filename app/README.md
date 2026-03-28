# App Surface

The `app/` tree contains the prototype's small off-ledger service layer.

Current contents:

- `app/policy-engine/` for the deterministic `CPL v0.1` policy evaluation engine and CLI

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
The policy engine may evaluate policy and produce reports, but Canton remains the intended authority for workflow state and transitions.
