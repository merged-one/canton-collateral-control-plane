# ADR 0004: Make Report Fidelity And Evidence First-Class Outputs

- Status: Accepted
- Date: 2026-03-28

## Context

The repository already prohibits fake demo artifacts and placeholder success paths. That rule needs a concrete architectural consequence: reports and evidence must come from committed workflow state and immutable inputs rather than from simulations, ad hoc operator notes, or manually reconstructed spreadsheets.

Collateral workflows are operationally sensitive. A report that does not match ledger state, policy inputs, or approvals is worse than no report because it creates false confidence.

## Decision

The system will treat report fidelity and evidence as first-class outputs:

1. Every execution report must be derived from committed workflow state plus referenced policy, valuation, and decision inputs.
2. Every material workflow transition must be attributable to actors, timestamps, policy versions, and correlation identifiers.
3. Demo evidence must record the commands run and the checks observed; it must not invent success artifacts.
4. Report generation is downstream of execution and must not become a hidden workflow controller.
5. Redacted or audience-specific report profiles are allowed, but each must still be traceable to the same committed source state.

## Consequences

Positive:

- operators and reviewers can trust reports as evidence rather than marketing output
- conformance tests can validate report fields against committed state
- audit and privacy reviews can reason about disclosure as a designed interface

Tradeoffs:

- report schemas and lineage fields must be designed earlier than many prototypes would prefer
- execution evidence adds documentation overhead to every meaningful task
- some operational views must be generated in multiple disclosure profiles instead of one universal report

These tradeoffs are accepted because the prototype is intended to be defensible and reproducible, not merely illustrative.
