# ADR 0002: Adopt The C-COPE Solution Shape From The Proposal

- Status: Accepted
- Date: 2026-03-28

## Context

The development-fund proposal dated 2026-03-28 adds materially sharper framing than the repository's initial bootstrap documents. It describes the project as a neutral collateral control plane for Canton rather than only as a narrow margin-workflow prototype, and it introduces a five-layer reference architecture:

1. Collateral Policy Language
2. Policy Engine
3. Optimization Engine
4. Workflow Library
5. Conformance Suite

The proposal also expands the intended workflow scope to include variation margin, initial margin, bilateral collateralization, repo, securities lending, treasury optimization, collateral recall, and close-out.

Without explicitly adopting or rejecting that framing, the repository would risk drifting between a small proof of concept and a broader reusable infrastructure target.

## Decision

The repository will use the proposal's C-COPE framing as its current architecture and roadmap basis.

This means:

1. The project is treated as a neutral collateral control-plane reference stack, not as a single app or venue.
2. The repository roadmap will align to the five-layer solution shape from the proposal.
3. Machine-readable reports remain a distinct concern that spans the policy, optimization, workflow, and conformance layers.
4. Milestones, invariants, and integration surfaces should reflect reuse across multiple Canton application types.
5. If the external proposal changes later, repository assumptions must be updated through ADRs and mission-control documents instead of informal edits.

## Consequences

Positive:

- clearer scope for future CPL, optimizer, workflow, and conformance work
- better alignment between repo documentation and expected fundable deliverables
- earlier visibility into cross-workflow reuse, adapter requirements, and negative-path testing

Tradeoffs:

- broader architecture increases documentation scope before implementation begins
- more care is required to avoid overcommitting to proposal details that may still evolve
- milestone planning must be kept distinguishable from completed implementation

These tradeoffs are acceptable because the proposal provides materially better structure than the generic bootstrap docs, and the ADR process gives the repo a clean way to absorb later changes.
