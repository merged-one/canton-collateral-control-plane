# ADR 0020: Orchestrate The Substitution Demo Through Quickstart Workflow Handoff And Reference Token Adapter

- Status: Accepted
- Date: 2026-03-30

## Context

ADR 0012 established the first substitution prototype on the IDE ledger with explicit replacement scope, approval gates, and atomic all-or-nothing settlement semantics. ADR 0018 established the first narrow Quickstart-backed reference token adapter path. Prompt 16 then bound the margin-call chain through Quickstart, but substitution still stopped before the real runtime and adapter surface.

That left four material gaps:

- `make demo-substitution` still stopped on the IDE ledger
- the Quickstart seed, workflow, adapter, and provider-visible status surfaces were disconnected from the substitution demo command
- the substitution report could not yet prove atomic incumbent release plus replacement movement on the real runtime path
- blocked partial substitution could not yet prove that no adapter receipt or partial side effect committed on Quickstart

Prompt 17 requires the repository to close those gaps without bypassing workflow authority and without fabricating positive-path success.

## Decision

Implement a dedicated Quickstart runtime mode for the substitution orchestration layer and bind it to scenario-scoped Quickstart seed, workflow, substitution-adapter, and provider-visible status commands.

The concrete shape is:

1. The substitution orchestration layer gains an explicit runtime choice:
   - `IDE_LEDGER` remains the existing comparison path
   - `QUICKSTART` becomes a first-class execution mode for the end-to-end confidential substitution demo
2. Quickstart substitution scenarios become scenario-scoped runtime inputs:
   - each workflow-bearing Quickstart scenario declares its own seed manifest
   - orchestration writes scenario-scoped state and artifact directories
   - positive and blocked partial-substitution paths can be tied back to one declared incumbent set, one declared replacement set, and one observed runtime surface
3. Workflow execution stays authoritative on Canton:
   - a new `CantonCollateral.QuickstartSubstitution` Daml Script layer advances the seeded substitution through real workflow states
   - the positive path exposes a real pending-settlement `SettlementInstruction` for the adapter
   - the blocked negative path proves the workflow rejected a partial replacement attempt before settlement intent could commit
4. Adapter execution remains strictly downstream of workflow state:
   - orchestration invokes the substitution adapter only when the Quickstart workflow result proves the positive pending-settlement handoff
   - the adapter consumes the full incumbent-release scope and the full replacement scope declared by workflow state
   - workflow confirmation of substitution closure remains on Canton after the adapter moves the reference token holdings
5. `SubstitutionReport` expands to carry the full Quickstart chain:
   - policy-evaluation artifact
   - optimization artifact
   - Quickstart workflow result artifact
   - Quickstart seed receipt
   - substitution adapter execution report
   - provider-visible substitution status artifact
   - report-level atomicity proof for committed and blocked paths

## Rejected Alternatives

### Alternative 1: Keep substitution on the IDE ledger and document the Quickstart commands separately

Rejected because it would preserve the evidence gap between the operator demo and the real runtime path.

- the substitution report would still stop before the real adapter path
- reviewers would need to correlate separate commands manually
- Prompt 17 explicitly requires one real chained Quickstart substitution command

### Alternative 2: Invoke the substitution adapter directly from optimization output

Rejected because it would bypass workflow authority.

- the optimizer is advisory only
- the adapter must consume workflow-declared release and replacement scope, not re-derive it from off-ledger output
- skipping the workflow handoff would break the control-plane versus data-plane split defended by ADR 0003 and ADR 0018

### Alternative 3: Treat blocked partial substitution as a workflow-only negative path without provider-visible adapter-status evidence

Rejected because it would weaken the no-side-effects proof.

- reviewers need to see that incumbent encumbrances and holdings remained intact
- adapter receipt count `0` is part of the acceptance criteria
- the report must prove both the blocked decision and the absence of downstream adapter mutation

## Consequences

Positive:

- the repository now has one real Quickstart-backed end-to-end substitution command rather than disconnected seed, workflow, and adapter fragments
- `SubstitutionReport` can now prove both committed atomic replacement and blocked partial substitution on the real runtime path
- the adapter boundary is reused for substitution without collapsing workflow authority into the data-plane layer

Tradeoffs:

- the Quickstart substitution path adds runtime-specific state, manifest, and artifact complexity
- the first Quickstart-backed substitution chain still uses the narrow reference token adapter rather than a production custodian integration
- Quickstart-backed return execution remains a separate follow-on task

These tradeoffs are accepted because the repository needed one real Quickstart-backed substitution chain now, and Prompt 17 required proof of both atomic positive-path replacement and blocked partial substitution without waiting for broader return or disclosure-profile work.
