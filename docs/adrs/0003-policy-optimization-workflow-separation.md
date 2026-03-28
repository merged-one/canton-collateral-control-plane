# ADR 0003: Separate Policy Evaluation, Optimization, And Workflow Execution

- Status: Accepted
- Date: 2026-03-28

## Context

Collateral systems often fail architecturally when policy rules, allocation heuristics, and settlement mechanics are mixed into one service or one contract model. In a Canton-native design, this is especially risky because:

- policy decisions should be reproducible from explicit inputs
- optimization objectives may change without changing legal or operational policy
- workflow state must stay authoritative on-ledger
- substitution and return flows require atomic execution even when optimization is optional

If these concerns are not separated now, later implementation could entangle policy math with Daml contracts or let optimizer output act as hidden authority.

## Decision

The system will enforce the following separation:

1. The policy evaluation engine determines feasibility, haircut-adjusted value, concentration impact, and release eligibility from explicit inputs.
2. The optimization engine consumes only policy-feasible inputs and produces ranked proposals with explanation traces.
3. The workflow layer commits obligations, approvals, encumbrances, substitutions, returns, and settlement instructions on Canton.
4. Workflow execution may reference a policy decision report or optimization proposal, but those artifacts remain externally versioned inputs rather than hidden embedded logic.
5. A workflow must remain safe even if optimization is disabled or unavailable.

## Consequences

Positive:

- deterministic policy tests can be built independently of workflow tests
- optimization can evolve or be replaced without changing authoritative ledger state
- operators can distinguish hard policy rejection from soft objective preference

Tradeoffs:

- more explicit correlation identifiers and report references are needed
- some data must be passed between services rather than recomputed informally
- Daml templates may need careful design to avoid copying large decision payloads

These tradeoffs are accepted because separation is the only credible way to preserve determinism, explainability, and atomicity together.
