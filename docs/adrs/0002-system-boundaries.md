# ADR 0002: Establish System Boundaries For The Canton-Native Control Plane

- Status: Accepted
- Date: 2026-03-28

## Context

The repository already adopted a neutral collateral control-plane framing on Canton. The next missing step is a precise system-boundary definition. Without that boundary work, policy rules, optimization logic, Daml workflow behavior, reporting, and LocalNet infrastructure could blur together in a way that would make later implementation hard to reason about and hard to defend.

The architecture must also remain compatible with the intended Quickstart-based LocalNet and future token-standard-style asset integrations without turning the repository into a monolithic application.

## Decision

The control-plane architecture is split into six explicit boundaries:

1. Collateral Policy Language and schedules
2. Policy evaluation engine
3. Optimization engine
4. Daml workflow contracts and orchestration
5. Reporting and evidence generation
6. Demo and runtime infrastructure

The following rules apply:

- policy packages are versioned and reusable across workflows
- policy evaluation is deterministic and side-effect free with respect to business state
- optimization proposals are advisory and never authoritative on their own
- Canton workflow state is authoritative for obligations, encumbrances, approvals, and settlement progression
- reports are derived from committed state and immutable references
- LocalNet or demo infrastructure may host the system but may not change control-plane semantics

## Consequences

Positive:

- implementation prompts can target a specific layer without redefining the whole system
- policy, workflow, and reporting interfaces can evolve with clearer contracts
- runtime topology decisions can change without rewriting the domain model

Tradeoffs:

- more interfaces must be documented before code exists
- the architecture requires stricter versioning and traceability discipline
- some convenience shortcuts common in prototypes are ruled out

Those tradeoffs are accepted because the domain is safety-critical and the repository is intended to guide reusable implementation, not only a one-off demo.
