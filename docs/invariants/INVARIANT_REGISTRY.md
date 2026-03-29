# Invariant Registry

This registry defines system properties that future code, reports, and tests must preserve. Each future implementation change should link affected invariants to evidence and verification.

## Taxonomy

- authorization and role control
- architecture separation
- adapter-boundary discipline
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
- upstream overlay discipline
- toolchain reproducibility
- auditability

## Proposal-Aligned Starter Invariants

| ID | Theme | Invariant Statement | Planned Evidence |
| --- | --- | --- | --- |
| AUTH-001 | Authorization and role control | Only authorized roles may create, approve, amend, or release collateral policy and workflow actions, and every authorization decision must be attributable to an identity and role. | ADR 0007, Daml role and workflow modules, Daml script authorization tests, `make test-conformance`, conformance report, execution reports |
| ARCH-001 | Architecture separation | Control-plane artifacts such as policy packages, policy decisions, optimization proposals, workflow-library outputs, conformance outputs, and execution reports must remain versioned artifacts with explicit boundaries; data-plane asset state, ledger state, settlement rails, and runtime infrastructure must stay explicit adjacent surfaces rather than hidden extensions of the control plane. | architecture docs, ADR 0003, ADR 0007, ADR 0010, Daml mapping |
| ADAPT-001 | Adapter-boundary discipline | Asset adapters may consume `SettlementInstruction` and related control contracts, execute asset-side actions, and emit machine-readable receipts, but they must not reinterpret policy, bypass workflow approvals, or authoritatively mutate obligation, encumbrance, or settlement workflow state off-ledger. | ADR 0018, ADR 0019, `daml/CantonCollateral/ReferenceToken.daml`, `daml/CantonCollateral/QuickstartAdapter.daml`, `daml/CantonCollateral/QuickstartMarginCall.daml`, `make localnet-run-token-adapter`, `make localnet-adapter-status`, `make demo-margin-call-quickstart`, adapter execution report, Prompt 15 evidence, Prompt 16 evidence |
| CPL-001 | Schema-version discipline | Every CPL policy package must declare both `cplVersion` and `policyVersion`, and loaders must reject undeclared fields rather than inferring hidden semantics from unknown data. | CPL spec, schema, ADR 0005, validation command |
| ELIG-001 | Eligibility determinism | Given the same policy version, asset facts, valuation inputs, and concentration state, eligibility evaluation must produce the same decision and explanation every time. | decision procedure spec, deterministic tests, `make test-conformance`, conformance determinism artifact, execution reports |
| HAIR-001 | Haircut and lendable-value correctness | Lendable value must equal the policy-defined valuation basis adjusted by the policy-defined haircut and rounding rules, with no hidden adjustments. | valuation formulas, test vectors, report fields, `make test-conformance`, conformance haircut artifact |
| CONC-001 | Concentration-limit enforcement | Allocation, substitution, and release decisions must reject or flag states that exceed the policy-defined concentration limits for issuer, asset class, currency, jurisdiction, or other configured buckets. | policy profiles, concentration tests, decision reports |
| CTRL-001 | Encumbrance and release control | If a policy or control state requires secured-party or pledgee approval for release, the release path must remain blocked until that approval is present and attributable. | Daml workflow modules, Daml test plan, authorization tests, `make demo-return`, `make demo-substitution`, return and substitution reports |
| ENC-001 | No double-encumbrance | A collateral position or lot must not be concurrently committed to overlapping obligations beyond its available encumberable amount. | encumbrance template, Daml lifecycle scripts, replay and concurrency tests, `make test-conformance`, conformance report |
| TIME-001 | Policy timing and expiry | Policy applicability, settlement windows, and operational expiry must be represented explicitly, and evaluators must not silently treat stale or out-of-window instructions as valid. | CPL spec, schema, validation plan, temporal scenario tests |
| ALLOC-001 | Substitution and allocation explainability | Given identical inputs and documented optimization settings, allocation or substitution output must be deterministic and accompanied by explanation traces showing why selected assets were chosen over alternatives. | ADR 0009, optimizer spec, deterministic tests, optimization reports, substitution reports |
| ATOM-001 | Atomic substitution and return | Collateral substitution and collateral return must complete atomically so that exposure coverage is not broken by intermediate visible states. | ADR 0007, ADR 0012, ADR 0013, substitution and return workflow templates, Daml lifecycle scripts, `make demo-return`, `make demo-substitution`, `make test-conformance`, conformance report, future Canton proof artifacts |
| ATOM-002 | Atomic settlement across legs | For supported multi-leg delivery or close-out flows, settlement must either complete across all required legs or fail without a partially committed exposure-changing state. | multi-leg workflow tests, conformance reports, execution evidence |
| PRIV-001 | Privacy-preserving visibility | Each role may see only the contracts, fields, and reports required for its responsibility, and cross-party visibility must be explicit rather than implied by shared infrastructure. | privacy model, ADR 0007, Daml mapping, stakeholder and disclosure-profile tests, `daml/CantonCollateral/QuickstartSeed.daml`, `make localnet-status-control-plane`, Quickstart status snapshot |
| PDR-001 | Policy decision report fidelity | Every machine-readable policy evaluation report must be derived deterministically from one declared policy version and one declared inventory snapshot, with explicit asset-level and portfolio-level reasons for rejection, escalation, or review. | policy evaluation report schema, ADR 0008, policy-engine tests, generated policy reports |
| REPT-001 | Report fidelity | Every machine-readable execution report, return report, or substitution report must correspond exactly to committed workflow state and must not invent or omit materially relevant actions. | execution, return, and substitution report schemas and specs, Daml workflow result, Quickstart workflow result, adapter execution report, `make demo-margin-call`, `make demo-margin-call-quickstart`, `make demo-return`, `make demo-substitution`, `make test-conformance`, `make demo-all`, conformance report, final demo pack, demo evidence |
| VAL-001 | Valuation snapshot lineage | Every policy decision and execution report must reference an immutable valuation snapshot or explicitly record why no snapshot was required. | `PolicyContext` in Daml workflows, decision reports, execution reports |
| WWR-001 | Wrong-way-risk explicitness | Wrong-way-risk exclusions must be machine-readable, attributable to a named rule, and enforced before an asset is accepted into eligible collateral. | CPL schema, example policies, negative-path scenarios |
| REPL-001 | Replay safety | Retried or replayed messages, commands, or events must not create duplicate pledges, duplicate releases, or inconsistent reports. | idempotency design, replay-safe request identifiers, Daml replay tests, `make demo-return`, `make test-conformance`, conformance report, event-correlation evidence |
| WF-001 | Workflow authority | Obligation, encumbrance, approval, and settlement state may change only through committed workflow transitions on Canton; off-ledger services may propose or report changes but may not authoritatively apply them. | `daml/CantonCollateral/*.daml`, ADR 0007, ADR 0019, Daml test plan, execution evidence, `make localnet-seed-demo`, `make localnet-run-margin-call-workflow`, `make demo-margin-call-quickstart`, Quickstart seed receipt |
| RUNTIME-001 | Runtime and demo separation | LocalNet overlays, demo bootstrap data, and runtime services must not alter policy semantics, bypass approvals, or fabricate successful reports. | deployment model, ADR 0015, ADR 0016, ADR 0017, ADR 0019, Quickstart README, LocalNet control-plane runbook, `make localnet-smoke`, `make localnet-build-dar`, `make localnet-deploy-dar`, `make localnet-start-control-plane`, `make localnet-seed-demo`, `make localnet-status-control-plane`, `make demo-margin-call`, `make demo-margin-call-quickstart`, `make demo-return`, `make demo-substitution`, `make demo-all`, prompt evidence |
| UPSTR-001 | Upstream overlay discipline | Quickstart-based LocalNet integration must pin an upstream source revision and prefer overlays or adjacent scripts over forks unless an ADR records why a fork is unavoidable. | ADR 0015, ADR 0017, `infra/quickstart/overlay/`, `infra/quickstart/overlay/control-plane-compose.yaml`, `make localnet-bootstrap`, `make localnet-smoke`, `make localnet-start-control-plane`, LocalNet demo plan |
| TOOL-001 | Toolchain reproducibility | Build, validation, and smoke-run commands must resolve to pinned Daml, Java, validation-tool, and Quickstart versions that are documented, checksum-verified or commit-pinned where downloaded, reproducible from a clean checkout, and explicitly tiered so portable verification does not silently depend on optional Docker-backed runtime checks. | dependency policy, bootstrap script, Quickstart bootstrap script, Quickstart DAR bridge script, Quickstart Daml Script runner, `scripts/verify-portable.sh`, `make verify-portable`, `make verify`, `make daml-build`, `make daml-test`, `make demo-run`, `make localnet-smoke`, `make localnet-build-dar`, `make localnet-deploy-dar`, `make localnet-start-control-plane`, `make localnet-seed-demo`, `make localnet-status-control-plane`, verification commands |
| AUD-001 | Auditability | Every material state transition must be traceable to inputs, policy version, actors, timestamps, and resulting state changes without requiring hidden manual reconstruction. | execution report template, Daml mapping, lifecycle scripts, `make test-conformance`, conformance report, `make demo-all`, final demo pack, prompt execution evidence |
| EXCP-001 | Exception-path determinism | Negative-path scenarios such as expired calls, insufficient lendable value, concentration breaches, unauthorized release attempts, or stale-snapshot failures must fail reproducibly with explicit reasons rather than implicit or silent failure modes. | conformance suite, negative-path scenarios, decision reports |

## Notes

- The registry now carries 24 named invariants spanning schema discipline, timing, wrong-way risk, policy-report fidelity, explicit control-plane versus data-plane architecture, privacy, workflow authority, runtime discipline, upstream overlay discipline, and toolchain reproducibility in addition to the original control properties.
- The first Daml workflow skeleton now adds concrete contract, report, and script hooks for authorization, workflow authority, atomicity, report fidelity, and auditability invariants.
- The first policy engine now adds executable evidence for deterministic eligibility, haircut, concentration, and failure-attribution invariants through schema-valid reports and scenario tests.
- The first optimizer now adds executable evidence for allocation explainability, concentration-aware best-to-post behavior, substitution economics, and clean no-solution handling through schema-valid reports and scenario tests.
- The first end-to-end margin-call demo now adds executable evidence that policy, optimization, workflow, and execution-report artifacts can be linked through one reproducible command without fabricating success on blocked paths.
- The first end-to-end return demo now adds executable evidence that retained-set selection, approval-gated release, replay blocking, and encumbrance-state integrity can be linked through one reproducible command without fabricating success on blocked paths.
- The first end-to-end substitution demo now adds executable evidence that encumbered-collateral replacement, approval-gated release, atomic all-or-nothing settlement, and substitution-report fidelity can be linked through one reproducible command without fabricating success on blocked paths.
- The Quickstart foundation and runtime bridge now add executable evidence that upstream pinning, overlay discipline, containerized cross-version DAR builds, and package deployment commands are explicit rather than hidden inside undocumented environment drift.
- The seeded Quickstart scenario now adds executable evidence that repo-owned overlays can allocate parties, seed real contract state, and query provider-visible status on LocalNet without inventing synthetic success artifacts.
- The Quickstart-backed reference token adapter now adds executable evidence that a narrow data-plane adapter can consume workflow settlement intent, perform token-style movement, emit a machine-readable receipt, and still leave workflow authority and encumbrance creation on Canton.
- The Quickstart-backed margin-call demo now adds executable evidence that policy, optimization, Quickstart workflow preparation, adapter execution, and final execution reporting can be chained together without fabricating downstream success on blocked paths.
- The aggregate conformance suite now adds executable evidence that authorization, determinism, haircut arithmetic, replay safety, no double-encumbrance, report fidelity, and audit completeness are visible in one machine-readable package rather than only across separate demos.
- The verification surface now distinguishes portable repository validation from Docker-backed Quickstart smoke validation so toolchain regressions and environment-service failures remain separately attributable.
- Future invariant updates should extend the current Daml-script, policy-engine, optimizer, conformance, and demo-pack evidence into expiry, privacy-profile, and workflow-coupled concentration scenarios.
