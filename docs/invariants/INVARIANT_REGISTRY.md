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
- policy-decision-report fidelity
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
| AUTH-001 | Authorization and role control | Only authorized roles may create, approve, amend, or release collateral policy and workflow actions, and every authorization decision must be attributable to an identity and role. | ADR 0007, Daml role and workflow modules, Daml script authorization tests, execution reports |
| ARCH-001 | Architecture separation | Control-plane artifacts such as policy packages, policy decisions, optimization proposals, workflow-library outputs, conformance outputs, and execution reports must remain versioned artifacts with explicit boundaries; data-plane asset state, ledger state, settlement rails, and runtime infrastructure must stay explicit adjacent surfaces rather than hidden extensions of the control plane. | architecture docs, ADR 0003, ADR 0007, ADR 0009, Daml mapping |
| CPL-001 | Schema-version discipline | Every CPL policy package must declare both `cplVersion` and `policyVersion`, and loaders must reject undeclared fields rather than inferring hidden semantics from unknown data. | CPL spec, schema, ADR 0005, validation command |
| ELIG-001 | Eligibility determinism | Given the same policy version, asset facts, valuation inputs, and concentration state, eligibility evaluation must produce the same decision and explanation every time. | decision procedure spec, deterministic tests, execution reports |
| HAIR-001 | Haircut and lendable-value correctness | Lendable value must equal the policy-defined valuation basis adjusted by the policy-defined haircut and rounding rules, with no hidden adjustments. | valuation formulas, test vectors, report fields |
| CONC-001 | Concentration-limit enforcement | Allocation, substitution, and release decisions must reject or flag states that exceed the policy-defined concentration limits for issuer, asset class, currency, jurisdiction, or other configured buckets. | policy profiles, concentration tests, decision reports |
| CTRL-001 | Encumbrance and release control | If a policy or control state requires secured-party or pledgee approval for release, the release path must remain blocked until that approval is present and attributable. | Daml workflow modules, Daml test plan, authorization tests, execution reports |
| ENC-001 | No double-encumbrance | A collateral position or lot must not be concurrently committed to overlapping obligations beyond its available encumberable amount. | encumbrance template, Daml lifecycle scripts, replay and concurrency tests |
| TIME-001 | Policy timing and expiry | Policy applicability, settlement windows, and operational expiry must be represented explicitly, and evaluators must not silently treat stale or out-of-window instructions as valid. | CPL spec, schema, validation plan, temporal scenario tests |
| ALLOC-001 | Substitution and allocation explainability | Given identical inputs and documented optimization settings, allocation or substitution output must be deterministic and accompanied by explanation traces showing why selected assets were chosen over alternatives. | optimizer spec, deterministic tests, explanation reports |
| ATOM-001 | Atomic substitution and return | Collateral substitution and collateral return must complete atomically so that exposure coverage is not broken by intermediate visible states. | ADR 0007, substitution and return workflow templates, Daml lifecycle scripts, future Canton proof artifacts |
| ATOM-002 | Atomic settlement across legs | For supported multi-leg delivery or close-out flows, settlement must either complete across all required legs or fail without a partially committed exposure-changing state. | multi-leg workflow tests, conformance reports, execution evidence |
| PRIV-001 | Privacy-preserving visibility | Each role may see only the contracts, fields, and reports required for its responsibility, and cross-party visibility must be explicit rather than implied by shared infrastructure. | privacy model, ADR 0007, Daml mapping, stakeholder and disclosure-profile tests |
| PDR-001 | Policy decision report fidelity | Every machine-readable policy evaluation report must be derived deterministically from one declared policy version and one declared inventory snapshot, with explicit asset-level and portfolio-level reasons for rejection, escalation, or review. | policy evaluation report schema, ADR 0008, policy-engine tests, generated policy reports |
| REPT-001 | Report fidelity | Every machine-readable execution report must correspond exactly to committed workflow state and must not invent or omit materially relevant actions. | execution report template, Daml mapping, Daml lifecycle scripts, demo evidence |
| VAL-001 | Valuation snapshot lineage | Every policy decision and execution report must reference an immutable valuation snapshot or explicitly record why no snapshot was required. | `PolicyContext` in Daml workflows, decision reports, execution reports |
| WWR-001 | Wrong-way-risk explicitness | Wrong-way-risk exclusions must be machine-readable, attributable to a named rule, and enforced before an asset is accepted into eligible collateral. | CPL schema, example policies, negative-path scenarios |
| REPL-001 | Replay safety | Retried or replayed messages, commands, or events must not create duplicate pledges, duplicate releases, or inconsistent reports. | idempotency design, replay tests, event-correlation evidence |
| WF-001 | Workflow authority | Obligation, encumbrance, approval, and settlement state may change only through committed workflow transitions on Canton; off-ledger services may propose or report changes but may not authoritatively apply them. | `daml/CantonCollateral/*.daml`, ADR 0007, Daml test plan, execution evidence |
| RUNTIME-001 | Runtime and demo separation | LocalNet overlays, demo bootstrap data, and runtime services must not alter policy semantics, bypass approvals, or fabricate successful reports. | deployment model, runbooks, demo evidence |
| TOOL-001 | Toolchain reproducibility | Build, validation, and smoke-run commands must resolve to pinned Daml, Java, and validation-tool versions that are documented, checksum-verified where downloaded, and reproducible from a clean checkout. | dependency policy, bootstrap script, `make daml-build`, `make daml-test`, `make demo-run`, verification commands |
| AUD-001 | Auditability | Every material state transition must be traceable to inputs, policy version, actors, timestamps, and resulting state changes without requiring hidden manual reconstruction. | execution report template, Daml mapping, lifecycle scripts, prompt execution evidence |
| EXCP-001 | Exception-path determinism | Negative-path scenarios such as expired calls, insufficient lendable value, concentration breaches, unauthorized release attempts, or stale-snapshot failures must fail reproducibly with explicit reasons rather than implicit or silent failure modes. | conformance suite, negative-path scenarios, decision reports |

## Notes

- The registry now carries 23 named invariants spanning schema discipline, timing, wrong-way risk, policy-report fidelity, explicit control-plane versus data-plane architecture, privacy, workflow authority, runtime discipline, and toolchain reproducibility in addition to the original control properties.
- The first Daml workflow skeleton now adds concrete contract, report, and script hooks for authorization, workflow authority, atomicity, report fidelity, and auditability invariants.
- The first policy engine now adds executable evidence for deterministic eligibility, haircut, concentration, and failure-attribution invariants through schema-valid reports and scenario tests.
- Future invariant updates should extend the current Daml-script and policy-engine evidence into replay, expiry, privacy-profile, and workflow-coupled concentration scenarios.
