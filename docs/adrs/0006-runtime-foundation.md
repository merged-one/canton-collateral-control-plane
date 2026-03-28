# ADR 0006: Establish A Pinned Daml Runtime Foundation

- Status: Accepted
- Date: 2026-03-28

## Context

The repository now has a formal CPL contract and a documentation backbone, but it still lacks an executable foundation that future prompts can compile and extend directly. The next phase needs a real package layout and a stable command surface without prematurely adding collateral business logic.

The runtime foundation must:

- use Daml as the canonical workflow-modeling technology
- keep the off-ledger service layer narrow and non-authoritative
- install reproducibly from pinned versions
- work from a clean checkout with explicit commands
- prove real compilation and execution without fabricating workflow outputs

## Decision

The repository will adopt a pinned repo-local runtime foundation centered on Daml.

Specific decisions:

1. Daml SDK `2.10.4` is the canonical workflow-modeling toolchain for this repository.
2. Temurin JDK `17.0.18+8` is the pinned Java baseline for local Daml and Canton tooling.
3. Bootstrap installs the Daml SDK and JDK under repo-local `.runtime/` and installs CPL validation tooling into repo-local `.venv/`.
4. The default command surface is `make bootstrap`, `make status`, `make validate-cpl`, `make daml-build`, `make demo-run`, and `make verify`.
5. The committed Daml package remains intentionally minimal and exists only to prove compile-and-run readiness; collateral policy, optimization, and settlement business semantics are deferred.
6. Any future off-ledger service code must live under `app/` and remain limited to policy evaluation, optimization orchestration, report generation, or integration helpers.

## Consequences

Positive:

- future prompts can add Daml packages and helper services without restructuring the repository
- contributors can bootstrap a clean machine without guessing global tool versions
- the command surface now proves real compilation and script execution rather than documentation-only readiness
- toolchain provenance is explicit and checksum-verified

Tradeoffs:

- bootstrap downloads are larger than the earlier docs-only baseline
- the repo now owns local tool-install logic that must stay aligned with upstream releases
- the minimal Daml package is execution infrastructure, not business value on its own

These tradeoffs are accepted because the repository needs a real, reproducible technical starting point before higher-risk collateral workflows are implemented.
