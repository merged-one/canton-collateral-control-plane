# ADR 0009: Rename The Repository To Canton Collateral Control Plane

- Status: Accepted
- Date: 2026-03-28

## Context

The repository already contains the right subsystem boundaries for a Canton-native collateral prototype: `CPL`, deterministic policy evaluation, optimization, Daml workflow orchestration, conformance, and reporting. The earlier name "Canton Collateral Policy & Optimization Engine" over-emphasized only two of those subsystems and suggested a narrower product shape than the repository actually documents and implements.

The architecture also already decomposes naturally into:

- a control plane that defines rules, evaluates feasibility, orchestrates workflow intent, and produces conformance and reporting outputs
- a data plane that holds or moves asset facts, ledger state, settlement state, and runtime execution surfaces

The old shorthand `C-COPE` is also no longer desirable. It is not descriptive enough for new documentation, and alternate acronyms such as `CCCP` or `CCP` would create market-structure ambiguity in a repository that explicitly models CCP-style controls without becoming a CCP.

## Decision

The repository adopts the following naming and architecture rules:

1. The active user-facing name is "Canton Collateral Control Plane".
2. The rename is semantic, not directional. It does not change the mission, scope, milestone ordering, or subsystem set already present in the repository.
3. The former name "Canton Collateral Policy & Optimization Engine" is retained only as a deprecated historical alias where continuity is useful in older records.
4. New documentation should use "Canton Collateral Control Plane" or "the Control Plane". The repository should not adopt new shorthand such as `CCCP`, `CCP`, or a replacement acronym.
5. The control plane includes:
   - `CPL`
   - eligibility evaluation
   - haircuting and lendable-value calculation
   - encumbrance and release control
   - concentration logic
   - optimization
   - substitution orchestration
   - conformance and reporting
6. The data plane includes:
   - token-standard-style assets
   - Daml Finance-style assets
   - ledger state and contract instances
   - settlement and DvP rails
   - Quickstart or LocalNet execution environment
7. Existing subsystem names remain valid. Directory names, module names, and package boundaries should be preserved unless a later ADR justifies additional churn.

## Consequences

Positive:

- the repository name now matches the implemented and planned subsystem stack
- future prompts can continue building policy, optimization, workflow, conformance, and reporting work without a naming-induced architecture mismatch
- control semantics stay explicitly separate from asset, ledger, settlement, and runtime execution surfaces
- contributor guidance is clearer about which historical name is still acceptable only for continuity notes

Tradeoffs:

- some historical records must carry alias notes so the rename does not erase prior evidence
- safe in-repo metadata such as DAR naming may change even though directory and module names mostly remain stable
- documentation updates are required across README, mission-control, glossary, architecture, and integration surfaces

These tradeoffs are accepted because the repository already behaves like a collateral control plane, and the rename clarifies that existing reality without redirecting the project.
