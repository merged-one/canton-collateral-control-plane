# ADR 0005: Use JSON And JSON Schema For CPL v0.1

- Status: Accepted
- Date: 2026-03-28

## Context

The repository architecture already treats the Collateral Policy Language as a boundary artifact shared by policy evaluation, optimization, workflow execution, reporting, and conformance tooling. That boundary now needs a concrete first format.

The format must be:

- machine-readable and strongly validated
- deterministic across tooling
- strict enough to reject undeclared extensions
- expressive enough for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style controls
- durable enough to version independently from the policy content carried inside it

## Decision

The repository will use JSON plus JSON Schema Draft 2020-12 as the canonical `CPL v0.1` format.

Specific decisions:

1. The canonical policy artifact is a JSON document validated against `schema/cpl.schema.json`.
2. `cplVersion` identifies the language version, while `policyVersion` identifies the authored policy content version.
3. The schema will reject undeclared properties by using `additionalProperties: false` throughout the document.
4. Market-practice variants are represented through one shared top-level model plus profile-specific values, not through separate incompatible schemas.
5. The repository will publish validating example policies for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style usage.
6. The first validation toolchain will be a pinned repo-local CLI validator exposed through `make validate-cpl`.

## Consequences

Positive:

- future engines and workflows can consume a single strict package shape
- validation can run before business logic exists
- policy authors can distinguish language evolution from policy revision
- market-practice diversity is expressed through policy data, not fragmented formats

Tradeoffs:

- JSON is less author-friendly than YAML for manual editing
- some semantic checks still require later engine logic because JSON Schema is structural
- strict rejection of unknown fields means extensions must be planned and versioned intentionally

These tradeoffs are accepted because the repository prioritizes deterministic interfaces and auditability over informal convenience.
