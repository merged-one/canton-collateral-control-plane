# ADR 0023: Add A Proposal Submission Wrapper Around The Final Demo Pack

- Status: Accepted
- Date: 2026-03-30

## Context

ADR 0022 made the conformance suite and final demo pack Quickstart-first. That closed the runtime-proof gap, but it still left one reviewer-consumption gap:

- technical reviewers still had to discover the correct review order across the repo by hand
- the final demo pack remained a runtime evidence index, not a submission-specific reviewer bundle
- memo and walkthrough materials could drift from the generated proof set unless they were pinned to one machine-readable wrapper
- the repository needs an external-review surface without changing the existing `FinalDemoPack`, conformance, workflow, or adapter report contracts

This task prepares the repo for proposal submission rather than for a new runtime capability milestone.

## Decision

The repository will add a separate proposal-submission wrapper instead of overloading `make demo-all`.

The concrete shape is:

1. `make proposal-package` wraps `make demo-all` and writes:
   - `reports/generated/proposal-submission-manifest.json`
   - `reports/generated/proposal-submission-summary.md`
2. The proposal-submission wrapper consumes the generated final demo pack, conformance output, and reviewer-facing docs:
   - reviewer start path
   - proposal submission memo
   - walkthrough script
3. Reviewer-facing claims must remain derived from generated evidence:
   - Quickstart deployment proof
   - one concrete reference token adapter proof path
   - the three Quickstart-backed confidential workflow demos
   - the aggregate conformance report
4. The final demo pack stays stable as the runtime evidence package:
   - the proposal wrapper is a reviewer-consumption layer
   - it does not redefine workflow, adapter, conformance, or final-pack contracts
5. The walkthrough remains repo-tracked documentation only:
   - the repo stores one walkthrough script
   - the proposal package does not depend on any out-of-repo media asset

## Rejected Alternatives

### Alternative 1: Expand the final demo pack itself until it becomes the reviewer memo, walkthrough script, and submission bundle

Rejected because it would blur runtime evidence and reviewer guidance into one contract.

- `make demo-all` should stay focused on runtime-backed packaging
- reviewer memo and walkthrough materials change at a different cadence than workflow proof artifacts
- one overloaded package would make claim-traceability harder rather than easier

### Alternative 2: Add only static docs and skip a machine-readable proposal wrapper

Rejected because that would reintroduce narrative drift.

- reviewers would still have to reconstruct the exact proof order by hand
- the memo could age away from the current final demo pack and conformance IDs
- the repo would lose a deterministic top-level command for proposal packaging

## Consequences

Positive:

- reviewers now get a deterministic `make proposal-package` entry point
- the repo can separate runtime proof from reviewer guidance without weakening evidence discipline
- proposal claims now have one machine-readable wrapper tied to the actual generated proof set

Tradeoffs:

- the repo now carries another generated package layer on top of `make demo-all`
- there is no out-of-repo media dependency in the submission package
- proposal packaging now needs its own docs, tests, and mission-control updates in addition to the runtime package

These tradeoffs are accepted because proposal reviewers need a faster, safer review path than the raw runtime package alone provides.
