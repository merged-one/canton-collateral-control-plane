# Invariant Registry

This registry defines system properties that future code, reports, and tests must preserve. Each future implementation change should link affected invariants to evidence and verification.

## Taxonomy

- authorization and role control
- architecture separation
- schema-version discipline
- eligibility determinism
- haircut and lendable-value correctness
- concentration-limit enforcement
- encumbrance and release control
- no double-encumbrance
- policy timing and expiry
- substitution and allocation explainability
- atomic substitution and return
- atomic settlement across legs
- privacy-preserving visibility
- report fidelity
- valuation snapshot lineage
- replay safety
- workflow authority
- runtime and demo separation
- toolchain reproducibility
- auditability

## Proposal-Aligned Starter Invariants

| ID | Theme | Invariant Statement | Planned Evidence |
| --- | --- | --- | --- |
| AUTH-001 | Authorization and role control | Only authorized roles may create, approve, amend, or release collateral policy and workflow actions, and every authorization decision must be attributable to an identity and role. | policy schema, access-control tests, audit records |
| ARCH-001 | Architecture separation | Policy packages, policy decisions, optimization proposals, workflow state, and execution reports must remain versioned artifacts with explicit boundaries; no downstream layer may silently mutate an upstream layer's authoritative record. | architecture docs, ADRs, interface contracts |
| CPL-001 | Schema-version discipline | Every CPL policy package must declare both `cplVersion` and `policyVersion`, and loaders must reject undeclared fields rather than inferring hidden semantics from unknown data. | CPL spec, schema, ADR 0005, validation command |
| ELIG-001 | Eligibility determinism | Given the same policy version, asset facts, valuation inputs, and concentration state, eligibility evaluation must produce the same decision and explanation every time. | decision procedure spec, deterministic tests, execution reports |
| HAIR-001 | Haircut and lendable-value correctness | Lendable value must equal the policy-defined valuation basis adjusted by the policy-defined haircut and rounding rules, with no hidden adjustments. | valuation formulas, test vectors, report fields |
| CONC-001 | Concentration-limit enforcement | Allocation, substitution, and release decisions must reject or flag states that exceed the policy-defined concentration limits for issuer, asset class, currency, jurisdiction, or other configured buckets. | policy profiles, concentration tests, decision reports |
| CTRL-001 | Encumbrance and release control | If a policy or control state requires secured-party or pledgee approval for release, the release path must remain blocked until that approval is present and attributable. | workflow specs, authorization tests, audit records |
| ENC-001 | No double-encumbrance | A collateral position or lot must not be concurrently committed to overlapping obligations beyond its available encumberable amount. | state model, concurrency tests, ledger evidence |
| TIME-001 | Policy timing and expiry | Policy applicability, settlement windows, and operational expiry must be represented explicitly, and evaluators must not silently treat stale or out-of-window instructions as valid. | CPL spec, schema, validation plan, temporal scenario tests |
| ALLOC-001 | Substitution and allocation explainability | Given identical inputs and documented optimization settings, allocation or substitution output must be deterministic and accompanied by explanation traces showing why selected assets were chosen over alternatives. | optimizer spec, deterministic tests, explanation reports |
| ATOM-001 | Atomic substitution and return | Collateral substitution and collateral return must complete atomically so that exposure coverage is not broken by intermediate visible states. | workflow spec, transactional tests, Canton proof artifacts |
| ATOM-002 | Atomic settlement across legs | For supported multi-leg delivery or close-out flows, settlement must either complete across all required legs or fail without a partially committed exposure-changing state. | multi-leg workflow tests, conformance reports, execution evidence |
| PRIV-001 | Privacy-preserving visibility | Each role may see only the contracts, fields, and reports required for its responsibility, and cross-party visibility must be explicit rather than implied by shared infrastructure. | privacy model, access-control tests, report-profile review |
| REPT-001 | Report fidelity | Every machine-readable execution report must correspond exactly to committed workflow state and must not invent or omit materially relevant actions. | report schema, state-to-report checks, demo evidence |
| VAL-001 | Valuation snapshot lineage | Every policy decision and execution report must reference an immutable valuation snapshot or explicitly record why no snapshot was required. | valuation snapshot contract, decision reports, execution reports |
| WWR-001 | Wrong-way-risk explicitness | Wrong-way-risk exclusions must be machine-readable, attributable to a named rule, and enforced before an asset is accepted into eligible collateral. | CPL schema, example policies, negative-path scenarios |
| REPL-001 | Replay safety | Retried or replayed messages, commands, or events must not create duplicate pledges, duplicate releases, or inconsistent reports. | idempotency design, replay tests, event-correlation evidence |
| WF-001 | Workflow authority | Obligation, encumbrance, approval, and settlement state may change only through committed workflow transitions on Canton; off-ledger services may propose or report changes but may not authoritatively apply them. | Daml workflow spec, integration tests, execution evidence |
| RUNTIME-001 | Runtime and demo separation | LocalNet overlays, demo bootstrap data, and runtime services must not alter policy semantics, bypass approvals, or fabricate successful reports. | deployment model, runbooks, demo evidence |
| TOOL-001 | Toolchain reproducibility | Build, validation, and smoke-run commands must resolve to pinned Daml, Java, and validation-tool versions that are documented, checksum-verified where downloaded, and reproducible from a clean checkout. | dependency policy, bootstrap script, setup docs, verification commands |
| AUD-001 | Auditability | Every material state transition must be traceable to inputs, policy version, actors, timestamps, and resulting state changes without requiring hidden manual reconstruction. | audit log design, report schema, operational runbooks |
| EXCP-001 | Exception-path determinism | Negative-path scenarios such as expired calls, insufficient lendable value, concentration breaches, unauthorized release attempts, or stale-snapshot failures must fail reproducibly with explicit reasons rather than implicit or silent failure modes. | conformance suite, negative-path scenarios, decision reports |

## Notes

- The registry now carries 22 named invariants spanning schema discipline, timing, wrong-way risk, architecture, privacy, workflow authority, runtime discipline, and toolchain reproducibility in addition to the original control properties.
- These invariants are still intentionally technology-agnostic at the repository-bootstrap stage, but the architecture package narrows their intended implementation boundaries.
- Future invariants should add explicit links to tests and evidence entries once implementation begins.
