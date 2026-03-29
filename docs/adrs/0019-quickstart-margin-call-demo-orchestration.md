# ADR 0019: Orchestrate The Margin-Call Demo Through Quickstart Workflow Handoff And Reference Token Adapter

- Status: Accepted
- Date: 2026-03-29

## Context

ADR 0017 established a real confidential Quickstart scenario with seeded obligations, inventory lots, role registrations, and posting intent state. ADR 0018 established a narrow Quickstart-backed reference token adapter that can consume a real `SettlementInstruction` and emit execution evidence without collapsing workflow authority into the adapter.

That still left one material gap in the demo surface:

- `make demo-margin-call` still stopped on the IDE ledger
- the existing Quickstart seed and adapter commands were disconnected from the policy and optimization demo chain
- the execution report could not yet prove one end-to-end path across policy evaluation, optimization, Quickstart workflow preparation, adapter execution, and final reporting
- negative Quickstart paths did not yet prove that blocked policy or workflow states prevent downstream adapter movement

Prompt 16 requires the repository to close that gap without fabricating success and without bypassing workflow authority.

## Decision

Implement a dedicated Quickstart runtime mode for the margin-call orchestration layer and bind it to a scenario-scoped workflow-preparation command plus the existing reference token adapter command.

The concrete shape is:

1. The margin-call orchestration layer gains an explicit runtime choice:
   - `IDE_LEDGER` remains the existing comparison path
   - `QUICKSTART` becomes a first-class execution mode for the end-to-end confidential margin-call demo
2. Quickstart scenarios are reseeded per workflow-bearing scenario:
   - each Quickstart workflow scenario declares its own seed manifest
   - orchestration writes scenario-scoped state and artifact directories
   - the run does not depend on a stale previously seeded posting state
3. Workflow preparation stays authoritative on Canton:
   - a new `CantonCollateral.QuickstartMarginCall` Daml Script advances the seeded margin-call and posting intent through the real workflow states
   - the script either exposes a real `SettlementInstruction` for adapter consumption or records a deterministic workflow rejection
   - the workflow result is written as a machine-readable artifact and becomes the only allowed handoff into the adapter layer
4. Adapter execution remains downstream of workflow state:
   - orchestration invokes the reference token adapter only when the Quickstart workflow result proves the positive handoff state
   - blocked policy or workflow paths do not fabricate adapter execution
   - the workflow-rejected negative path still captures provider-visible adapter status evidence to prove that no movement occurred
5. `ExecutionReport` expands to carry the full chain:
   - policy evaluation artifact
   - optimization artifact
   - Quickstart workflow result artifact
   - adapter execution and adapter status artifacts where applicable
   - blocked-phase and adapter-outcome metadata for negative Quickstart paths

## Rejected Alternatives

### Alternative 1: Keep `make demo-margin-call` on the IDE ledger and document the Quickstart commands separately

Rejected because it would preserve an evidence gap between the operator demo and the Quickstart runtime surface.

- the execution report would still stop short of the real LocalNet
- reviewers would need to correlate separate commands manually
- Prompt 16 explicitly requires one real chained command

### Alternative 2: Invoke the adapter directly from optimization output

Rejected because it would bypass workflow authority.

- the optimizer is advisory only
- the adapter must consume workflow outputs, not off-ledger portfolio recommendations
- skipping the workflow handoff would break the control-plane versus data-plane split defended by ADR 0003 and ADR 0018

### Alternative 3: Reuse one global seeded Quickstart scenario for every positive or negative case

Rejected because it would weaken determinism and negative-path attribution.

- a stale posting or settlement state could leak across scenarios
- workflow rejection evidence would become harder to attribute cleanly
- per-scenario reseeding keeps the execution report tied to one declared manifest and one observed runtime state

## Consequences

Positive:

- the repository now has one real Quickstart-backed end-to-end margin-call command rather than separate seed, workflow, and adapter fragments
- `ExecutionReport` can now reference real subordinate artifacts from every layer of the positive chain
- blocked Quickstart paths now prove no downstream adapter movement occurs when policy or workflow gates fail

Tradeoffs:

- the Quickstart orchestration path adds runtime-specific complexity and scenario-scoped artifact directories
- the first Quickstart-backed end-to-end chain is still posting-focused and margin-call-specific
- substitution and return remain on the IDE-ledger path until equivalent Quickstart workflow-plus-adapter handoffs are implemented

These tradeoffs are accepted because the repository needed one real chained Quickstart execution surface more than it needed a broader but unproven generalization.
