# Worklog

This log is append-oriented. Every task should record intent before changes and outcomes after changes.

## 2026-03-29 - Prompt 17 Quickstart Substitution Adapter End-To-End - Pre-Change

Intent:
Upgrade the confidential substitution demo so the positive path executes end to end through policy evaluation, optimization, Quickstart-backed substitution workflow execution, the reference token adapter replacement and release path, and final substitution reporting, while at least one negative path proves no partial substitution or unintended adapter side effects can commit.

Task summary:

- refactor the substitution orchestration into an explicit Quickstart mode that can prepare scenario-scoped LocalNet state, run the declared positive substitution path against the deployed Control Plane package, invoke the token-adapter-driven replacement or release handoff, and collect subordinate artifacts into one machine-readable substitution report
- add or update a reproducible `make demo-substitution-quickstart` command that ensures the LocalNet and package prerequisites are ready, runs the positive and negative Quickstart substitution scenarios, and fails nonzero on genuine workflow or adapter failure
- expand substitution artifact generation so the report explicitly captures the incumbent encumbered set, replacement set, adapter actions, final post-substitution state, and all-or-nothing atomicity evidence on the real executed path
- prove at least one blocked negative path where partial substitution is rejected, the incumbent encumbrance set remains intact, and adapter-side effects do not commit
- update tracker, invariants, evidence, runbooks, specs, setup, and ADR surfaces as needed so the new Quickstart substitution posture and the remaining return-gap boundary are explicit

Expected affected files:

- `Makefile`
- `app/orchestration/substitution_demo.py`
- `app/orchestration/substitution_cli.py`
- `app/orchestration/cli.py` if the shared command surface needs updating
- new or updated Quickstart substitution helpers under `scripts/`
- relevant Daml modules under `daml/CantonCollateral/` for Quickstart substitution workflow preparation and adapter-backed replacement evidence
- substitution scenario manifests under `examples/demo-scenarios/substitution/`
- `reports/schemas/substitution-report.schema.json` if the report contract needs to expand for Quickstart workflow and adapter evidence
- generated substitution artifacts under `reports/generated/`
- `docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md`
- `docs/specs/SUBSTITUTION_REPORT_SPEC.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-17-execution-report.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/WORKLOG.md`
- the next ADR only if the Quickstart substitution handoff materially changes the current design boundary

Risk assessment:

- the substitution report could overclaim atomic replacement if it stitches together stale workflow or adapter artifacts rather than artifacts produced by the same Quickstart run
- the adapter extension could drift past the current boundary discipline if it starts selecting inventory or mutating obligation semantics instead of consuming workflow-declared replacement and release scope
- the negative-path evidence could be misleading if a blocked substitution still leaves adapter receipts, holdings, or partial encumbrance changes visible after failure
- the Quickstart substitution path could accidentally depend on hidden seeded state rather than scenario-scoped manifests and explicit reproducible commands

Acceptance criteria:

- `make demo-substitution-quickstart` exists, is documented, and fails nonzero on real Quickstart, workflow, or adapter failure
- the positive substitution path now runs through real Quickstart-backed workflow execution and the reference token adapter rather than stopping at the IDE ledger
- the generated substitution report explicitly proves incumbent scope, replacement scope, adapter actions, final post-substitution state, and atomic all-or-nothing replacement on the executed path
- at least one negative scenario proves no partial substitution, no incumbent release drift, and no unintended adapter side effects on the blocked path
- relevant checks, docs, invariants, evidence, and generated artifacts are updated and captured

## 2026-03-30 - Prompt 17 Quickstart Substitution Adapter End-To-End - Post-Change

Outcome:
Upgraded the confidential substitution demo so the Quickstart-backed path now runs end to end through policy evaluation, optimization, Quickstart substitution workflow execution, the reference token adapter replacement or release path, and final substitution reporting, with negative paths that prove no partial substitution or unintended adapter side effects commit.

Completed changes:

- added the Quickstart runtime mode and substitution report-contract expansion in `app/orchestration/substitution_demo.py`, `app/orchestration/substitution_cli.py`, and `reports/schemas/substitution-report.schema.json`
- added the Quickstart substitution workflow and status layer with `daml/CantonCollateral/QuickstartSubstitution.daml`, `scripts/localnet-seed-substitution-demo.sh`, `scripts/localnet-run-substitution-workflow.sh`, `scripts/localnet-run-substitution-token-adapter.sh`, and `scripts/localnet-substitution-status.sh`
- added dedicated Quickstart substitution scenario manifests and declared LocalNet seed manifests for:
  - one positive Quickstart-backed atomic substitution path
  - one policy-blocked negative path
  - one workflow-blocked partial substitution path that proves no release, no replacement movement, and no adapter receipt commit
- updated `make demo-substitution-quickstart` so it starts or reuses the LocalNet, deploys the Control Plane DAR when needed, runs the Quickstart-backed positive and negative substitution scenarios, validates the generated substitution report, and fails nonzero on genuine runtime failure
- expanded the generated artifact surface so the Quickstart substitution report now references real policy, optimization, workflow, seed, adapter, and blocked-path status artifacts and records `atomicityEvidence` for both committed and blocked outcomes
- added ADR 0020 and aligned tracker, runbooks, specs, setup, testing, invariants, risks, threat model, evidence, README, and command-surface docs with the new Quickstart-backed substitution chain
- bumped the shared Daml package version from `0.1.7` to `0.1.8` after the first Quickstart redeploy surfaced a real `KNOWN_PACKAGE_VERSION` conflict on the running participant

Commands run:

```sh
sh -n scripts/localnet-seed-substitution-demo.sh
sh -n scripts/localnet-run-substitution-workflow.sh
sh -n scripts/localnet-run-substitution-token-adapter.sh
sh -n scripts/localnet-substitution-status.sh
python3 -m py_compile app/orchestration/substitution_demo.py app/orchestration/substitution_cli.py
make daml-build
make demo-substitution
make localnet-deploy-dar
make demo-substitution-quickstart
make docs-lint
git diff --check
```

Results:

- the shell syntax checks passed for the new Quickstart substitution workflow, seed, adapter, and status scripts
- the Python bytecode check passed for the substitution orchestration and CLI modules
- `make daml-build` passed, and the first Quickstart redeploy attempt surfaced a real `KNOWN_PACKAGE_VERSION` conflict on package version `0.1.7`, proving the runtime path fails nonzero on package drift instead of fabricating success
- after bumping the shared package version to `0.1.8`, `make localnet-deploy-dar` passed and the deployment receipt now records `.daml/dist-quickstart/canton-collateral-control-plane-0.1.8.dar` with package id `e7c7bb46feecee544cdefbb58661bfc1563eea27dde48dcba85830b62549a0a4`
- `make demo-substitution` passed and regenerated `reports/generated/substitution-demo-report.json` plus supporting IDE-ledger artifacts for the comparison path
- `make demo-substitution-quickstart` passed and validated `reports/generated/substitution-quickstart-report.json`, `reports/generated/substitution-quickstart-summary.md`, and `reports/generated/substitution-quickstart-timeline.md`
- the positive Quickstart scenario produced and linked:
  - `reports/generated/positive-substitution-quickstart-policy-evaluation-report.json`
  - `reports/generated/positive-substitution-quickstart-optimization-report.json`
  - `reports/generated/positive-substitution-quickstart-workflow-input.json`
  - `reports/generated/positive-substitution-quickstart-workflow-result.json`
  - `reports/generated/positive-substitution-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/positive-substitution-quickstart/localnet-substitution-adapter-execution-report.json`
  - `reports/generated/positive-substitution-quickstart/localnet-substitution-status.json`
- the positive Quickstart report proves `ATOMICALLY_COMMITTED` replacement for incumbent lots `quickstart-sub-current-eib-521` and `quickstart-sub-current-kfw-521` with approved replacement lots `quickstart-sub-repl-fannie-521` and `quickstart-sub-repl-ust-521`, and the provider-visible status artifact proves:
  - substitution state `Closed`
  - settlement instruction state `Settled`
  - one adapter receipt
  - incumbent holdings released back to `provider-account-substitution-521`
  - replacement holdings settled into `secured-account-substitution-521`
- the blocked partial Quickstart scenario produced policy, optimization, workflow, seed, and status artifacts but no adapter execution report, and the blocked-path evidence proves `BLOCKED_NO_SIDE_EFFECTS` for incumbent lots `quickstart-sub-current-eib-621` and `quickstart-sub-current-kfw-621` with:
  - no adapter release actions
  - no adapter replacement actions
  - no released lots
  - no replacement holdings
  - zero adapter receipts
  - incumbent holdings still retained in `secured-account-substitution-621`
- the final accepted Quickstart scenario ids are the fresh `521` positive path and `621` blocked partial path, which avoid stale-state reuse from earlier debug runs
- `make docs-lint` passed after the new Quickstart substitution docs, ADR, tracker, runbook, and evidence updates landed
- `git diff --check` passed with no whitespace or patch-format issues

Next step:
Extend the same Quickstart-backed workflow-plus-adapter discipline to the return path so margin return or release can produce real adapter-backed proof of release semantics rather than stopping at the current workflow skeleton.

## 2026-03-29 - Prompt 16 Quickstart Margin-Call End-To-End - Pre-Change

Intent:
Upgrade the confidential margin-call demo so the positive path executes end to end through policy evaluation, optimization, Quickstart-backed workflow execution, the reference token adapter, and final execution reporting, while negative paths continue to block cleanly without fabricated downstream success.

Task summary:

- refactor the existing margin-call orchestration into an explicit Quickstart mode that can prepare the LocalNet, run the declared positive path against the deployed Control Plane package, invoke the reference token adapter, and collect subordinate artifact paths into one machine-readable execution report
- add or update a reproducible `make demo-margin-call-quickstart` command that ensures the LocalNet and package prerequisites are ready, runs the positive end-to-end path, and fails nonzero on genuine workflow or adapter failure
- expand margin-call artifact generation so the execution report references real policy, optimization, workflow, and adapter artifacts and so at least one negative scenario proves the adapter does not run when policy or workflow gating blocks execution
- update tracker, invariants, evidence, runbooks, specs, setup, and any required architecture or ADR surfaces so the new Quickstart-backed margin-call posture and remaining substitution and return gaps are explicit

Expected affected files:

- `Makefile`
- `app/orchestration/margin_call_demo.py`
- `app/orchestration/cli.py`
- new or updated Quickstart orchestration helpers under `scripts/`
- generated margin-call artifacts under `reports/generated/`
- `reports/schemas/execution-report.schema.json` if the expanded artifact linkage requires contract updates
- `infra/quickstart/scenarios/confidential-margin-scenario.json` only if the seeded scenario needs additional workflow handoff metadata
- relevant Daml modules under `daml/CantonCollateral/` only if Quickstart workflow execution or reporting helpers need to expose a real margin-call result surface separate from the standalone adapter path
- `docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md`
- `docs/integration/LOCALNET_DEMO_PLAN.md`
- `docs/specs/EXECUTION_REPORT_SPEC.md`
- `docs/specs/POLICY_EVALUATION_REPORT_SPEC.md`
- `docs/specs/OPTIMIZATION_REPORT_SPEC.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-16-execution-report.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/WORKLOG.md`
- additional docs only where needed to keep the new Quickstart margin-call command and artifact surfaces consistent

Risk assessment:

- the orchestration could accidentally claim Quickstart-backed workflow or adapter success by reusing stale seeded or adapter artifacts instead of tying the report to the current run
- negative-path handling could become misleading if the adapter surface is invoked or reported after a policy, optimization, or workflow gate has already failed
- Quickstart preparation logic could become too implicit if the new command silently depends on external state without making deployment, seeding, and adapter prerequisites reproducible
- a widened execution report contract could weaken report fidelity if subordinate artifact references are optional or no longer align with the actual positive and negative path results

Acceptance criteria:

- `make demo-margin-call-quickstart` exists, is documented, and fails nonzero on real Quickstart, workflow, or adapter failure
- the positive margin-call path now runs through real Quickstart-backed workflow execution and the reference token adapter rather than stopping at the IDE ledger
- the generated execution report references real policy, optimization, workflow, and adapter artifacts produced by the same run
- at least one negative scenario proves no adapter movement occurs when policy or workflow gating fails and the report reflects the blocked path accurately
- relevant checks, docs, invariants, and evidence are updated and captured

## 2026-03-29 - Prompt 16 Quickstart Margin-Call End-To-End - Post-Change

Outcome:
Upgraded the confidential margin-call demo so the Quickstart-backed path now runs end to end through policy evaluation, optimization, Quickstart workflow preparation, the reference token adapter, and final execution reporting, with negative paths that block cleanly and do not fabricate adapter success.

Completed changes:

- added the Quickstart runtime mode and report-contract expansion in `app/orchestration/margin_call_demo.py`, `app/orchestration/cli.py`, and `reports/schemas/execution-report.schema.json`
- added the Quickstart workflow-preparation layer with `daml/CantonCollateral/QuickstartMarginCall.daml` and `scripts/localnet-run-margin-call-workflow.sh`
- added dedicated Quickstart margin-call scenario manifests and declared LocalNet seed manifests for:
  - one positive Quickstart-backed end-to-end margin-call path
  - one policy-blocked negative path
  - one workflow-rejected negative path that proves no adapter movement occurs
- updated `make demo-margin-call-quickstart` so it starts or reuses the LocalNet, deploys the Control Plane DAR when needed, runs the Quickstart-backed positive and negative margin-call scenarios, validates the generated execution report, and fails nonzero on genuine runtime failure
- expanded the generated artifact surface so the Quickstart execution report now references real policy, optimization, workflow, seed, adapter, and blocked-path status artifacts
- added ADR 0019 and aligned tracker, runbooks, specs, setup, testing, invariants, risks, threat model, evidence, README, and command-surface docs with the new Quickstart-backed margin-call chain
- bumped the shared Daml package version from `0.1.5` to `0.1.6` after the first Quickstart rerun surfaced a real `KNOWN_PACKAGE_VERSION` conflict on the running participant

Commands run:

```sh
sh -n scripts/localnet-run-margin-call-workflow.sh
sh -n scripts/localnet-run-token-adapter.sh
sh -n scripts/localnet-seed-demo.sh
sh -n scripts/localnet-status-control-plane.sh
python3 -m py_compile app/orchestration/margin_call_demo.py app/orchestration/cli.py
make daml-build
make demo-margin-call
make demo-margin-call-quickstart
make docs-lint
git diff --check
```

Results:

- the shell syntax checks passed for the new Quickstart workflow-preparation script and the related seed, status, and adapter scripts
- the Python bytecode check passed for the margin-call orchestration and CLI modules
- `make daml-build` passed and built the shared Control Plane DAR before the Quickstart package-version bump and again through the Quickstart runtime bridge after the bump
- the first `make demo-margin-call-quickstart` attempt failed with Quickstart HTTP `400` code `KNOWN_PACKAGE_VERSION`, proving the new command fails nonzero on a real package-deployment conflict instead of fabricating success
- after bumping the shared Daml package version to `0.1.6`, `make demo-margin-call` passed and regenerated `reports/generated/margin-call-demo-execution-report.json` plus supporting IDE-ledger artifacts
- after the package-version fix, `make demo-margin-call-quickstart` passed and validated `reports/generated/margin-call-quickstart-execution-report.json` with execution id `exr-9bc26ea5d960c241`
- the Quickstart deployment receipt now records `.daml/dist-quickstart/canton-collateral-control-plane-0.1.6.dar` with package id `ae41ef524a90248a1d0e48368a15dadda5347f8af32fb4e173cfcaab157380c7`
- the positive Quickstart scenario produced and linked:
  - `reports/generated/positive-margin-call-quickstart-policy-evaluation-report.json`
  - `reports/generated/positive-margin-call-quickstart-optimization-report.json`
  - `reports/generated/positive-margin-call-quickstart-workflow-input.json`
  - `reports/generated/positive-margin-call-quickstart-workflow-result.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-control-plane-seed-receipt.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-execution-report.json`
  - `reports/generated/positive-margin-call-quickstart/localnet-reference-token-adapter-status.json`
- the positive Quickstart workflow result proved:
  - margin-call state `Closed`
  - posting state `PendingSettlement` before adapter confirmation
  - workflow gate `PREPARE_FOR_ADAPTER`
  - settlement instruction `quickstart-demo-posting-correlation-101-instruction`
  - selected lots `quickstart-demo-lot-101`, `quickstart-demo-lot-102`, `quickstart-demo-lot-103`, and `quickstart-demo-lot-104`
- the positive adapter execution report proved:
  - receipt `quickstart-demo-margin-101-reference-token-receipt`
  - receipt status `EXECUTED`
  - four real lot movements into `secured-account-quickstart-demo-101`
  - posting state `Closed` after workflow confirmation
  - settlement instruction state `Settled` after workflow confirmation
  - four pledged encumbrances after confirmation
- the negative ineligible Quickstart scenario blocked at `POLICY_EVALUATION` and emitted no workflow or adapter artifacts
- the negative workflow-rejected Quickstart scenario produced policy, optimization, workflow, seed, and blocked adapter-status artifacts but no adapter execution report, and the blocked adapter-status artifact proved:
  - posting state `Rejected`
  - provider-visible adapter receipt count `0`
  - provider-visible holding count `0`
  - provider-visible encumbrance count `0`
- `make docs-lint` passed after the ADR, tracker, runbook, spec, evidence, and command-surface updates
- `git diff --check` passed with no whitespace or patch-format issues

Next step:
Extend the same Quickstart-backed workflow-plus-adapter discipline to substitution and return, then narrow the current workflow-party and provider-visible report surfaces into explicit role-scoped disclosure profiles.

## 2026-03-29 - Prompt 15 Reference Token Adapter Path - Pre-Change

Intent:
Implement the first concrete Quickstart-backed reference token adapter path so the Control Plane can hand a real `SettlementInstruction` and related control state to a narrow data-plane adapter that performs a minimal token-style movement and emits machine-readable execution evidence.

Task summary:

- define the first stable reference token adapter boundary for settlement-instruction consumption, asset and lot identity mapping, account references, release or replacement confirmation carriage, and adapter receipt output
- implement the smallest real Quickstart-backed adapter path that reads Control Plane workflow outputs, performs a token-style movement or encumbrance-state transition, and emits a machine-readable adapter execution artifact
- add reproducible operator commands for running the adapter and inspecting adapter status without collapsing policy, optimization, workflow authority, or report generation into the adapter layer
- update ADRs, mission-control documents, invariants, evidence, architecture, integration, runbook, and glossary surfaces so the adapter boundary and residual non-goals are explicit

Expected affected files:

- `Makefile`
- new or updated adapter scripts under `scripts/`
- `daml/CantonCollateral/` modules for the reference token adapter path and any supporting Quickstart script hooks
- `reports/schemas/adapter-execution-report.schema.json`
- generated adapter artifacts under `reports/generated/`
- `docs/adrs/` with the next sequential ADR number because ADR `0017` is already assigned to the Quickstart confidential-seed decision
- `docs/integration/ASSET_ADAPTER_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md`
- `docs/domain/DAML_MAPPING.md`
- relevant architecture, runbook, glossary, mission-control, invariant, evidence, risk, and setup docs required to keep the new command and boundary surfaces consistent
- `docs/evidence/prompt-15-execution-report.md`
- `docs/mission-control/WORKLOG.md`

Risk assessment:

- the adapter could accidentally collapse workflow authority into the data-plane path if it directly reinterprets approval or policy semantics instead of only consuming declared settlement and control contracts
- a Quickstart-backed reference token move may require additional seed state or participant visibility that, if modeled poorly, could weaken the confidentiality or role-boundary demonstration
- an adapter receipt that is not keyed tightly enough to workflow, instruction, lot, and external action identifiers would weaken auditability and downstream execution reporting
- the first implementation must stay explicitly reference-grade; if it drifts toward a generic external integration bus or production custodian abstraction, the repo would overclaim the current milestone

Acceptance criteria:

- one documented reference token adapter path exists and is clearly data-plane scoped relative to Control Plane authority
- `make localnet-run-token-adapter` and `make localnet-adapter-status` exist, are documented, and fail clearly when Quickstart prerequisites are missing
- the adapter produces a real machine-readable artifact from actual execution against the seeded Quickstart-backed environment
- invariants, evidence, ADRs, tracker, and runbooks consistently describe what the adapter consumes, what it emits, and what remains intentionally out of scope
- relevant build, schema, Daml, docs, and Quickstart-backed adapter checks are executed and captured in evidence

## 2026-03-29 - Prompt 15 Reference Token Adapter Path - Post-Change

Outcome:
Implemented the first real Quickstart-backed reference token adapter path so the Control Plane can hand settlement and encumbrance workflow outputs to a narrow data-plane adapter that performs a minimal token-style collateral movement, confirms settlement closure, and emits machine-readable adapter evidence.

Completed changes:

- added the first stable reference token adapter boundary with `daml/CantonCollateral/ReferenceToken.daml` and `daml/CantonCollateral/QuickstartAdapter.daml`, including settlement-instruction consumption, lot and asset mapping, account references, adapter receipt output, and machine-readable status surfaces
- extended `daml/CantonCollateral/Settlement.daml` so a `SettlementInstruction` carries `allocationsInScope`, letting the adapter consume the workflow-declared lot set without reinterpreting policy
- updated `daml/CantonCollateral/QuickstartSeed.daml` and the confidential Quickstart scenario manifest so the seeded scenario can reuse the hosted secured-party identity as the Quickstart custodian and support a real adapter action path against the running LocalNet
- added the reproducible operator command surface:
  - `make localnet-run-token-adapter`
  - `make localnet-adapter-status`
- added adapter helper scripts plus adapter artifacts and schema:
  - `scripts/localnet-run-token-adapter.sh`
  - `scripts/localnet-adapter-status.sh`
  - `reports/schemas/adapter-execution-report.schema.json`
  - `reports/generated/localnet-reference-token-adapter-execution-report.json`
  - `reports/generated/localnet-reference-token-adapter-summary.md`
  - `reports/generated/localnet-reference-token-adapter-status.json`
  - `reports/generated/localnet-reference-token-adapter-status-summary.md`
- added ADR 0018 and aligned architecture, integration, runbook, glossary, mission-control, invariant, evidence, setup, risk, and threat-model documentation with the new reference adapter boundary and its explicit non-goals

Architecture and ADR note:

- ADR 0018 was added because Prompt 15 introduces the first durable asset-side adapter boundary: the Control Plane still owns policy, optimization, workflow authority, and reporting, while the reference adapter only consumes declared settlement and control contracts and emits execution receipts plus status evidence

Commands run:

```sh
sh -n scripts/localnet-control-plane-common.sh
sh -n scripts/localnet-seed-demo.sh
sh -n scripts/localnet-status-control-plane.sh
sh -n scripts/localnet-run-token-adapter.sh
sh -n scripts/localnet-adapter-status.sh
make daml-build
make localnet-deploy-dar
make localnet-run-token-adapter
make localnet-adapter-status
make docs-lint
git diff --check
git status --short --branch
```

Results:

- `make localnet-deploy-dar` passed and deployed `.daml/dist-quickstart/canton-collateral-control-plane-0.1.5.dar` with package id `7fb85f0678a49f3a07f3e4bf7233aeec7bbfbdce53f1bddd58d97d24b86b7ee6`
- the Quickstart-backed adapter execution passed against seeded scenario `quickstart-reference-token-margin-004` and produced `reports/generated/localnet-reference-token-adapter-execution-report.json` plus the matching Markdown summary
- the execution report captured one settled instruction `quickstart-reference-token-posting-correlation-004-instruction`, one adapter receipt `quickstart-reference-token-margin-004-reference-token-receipt`, and one external transfer id `quickstart-reference-token-posting-correlation-004-instruction-reference-token-transfer`
- the adapter moved two lots into the secured holding reference:
  - `quickstart-reference-token-lot-007` for `60.0` of `us-tbill-2029-01`
  - `quickstart-reference-token-lot-008` for `40.0` of `us-tbill-2030-03`
- the workflow-confirmation portion of the adapter evidence showed posting state progression `Submitted -> PendingSettlement -> Closed`, settlement-instruction state `Settled`, provider-visible encumbrance count `2`, and provider-visible execution-report count `1`
- the refreshed adapter status command passed and confirmed provider-visible post-execution state with `2` reference-token holdings in `secured-account-001`, `2` encumbrances, `1` execution report, and `1` adapter receipt
- the adapter execution artifact validated against `reports/schemas/adapter-execution-report.schema.json`
- `make docs-lint` passed after the ADR, docs, runbook, command-surface, invariant, and evidence updates were added
- `git diff --check` passed with no whitespace or malformed patch issues

Residual risks and follow-up:

- the reference token adapter remains intentionally Quickstart-scoped and reference-grade; it does not yet model real custodian connectivity, settlement windows, reservation coordination, or production reconciliation behavior
- the adapter currently backfills reference-token holdings from provider inventory during execution, so pre-execution holdings are absent from the initial adapter report even though post-execution holdings and receipts are real and provider-visible
- future adapter paths must preserve the same boundary discipline and avoid reintroducing policy interpretation or workflow authority into the data-plane layer

## 2026-03-29 - Prompt 14 Quickstart Seeded Confidential Scenario - Pre-Change

Intent:
Extend the pinned Quickstart foundation from package deployment only to a real seeded Control Plane scenario by adding repo-owned overlay bootstrap, start, seed, and status commands plus explicit Quickstart-backed evidence artifacts.

Task summary:

- add an overlay-first Quickstart control-plane layer that can start the pinned LocalNet, deploy the Control Plane package, allocate the scenario parties and roles, and seed one confidential margin-style collateral scenario
- capture machine-readable and human-readable evidence proving the seeded contracts and scenario metadata live on Quickstart rather than only on the IDE ledger
- update runbooks, tracker, roadmap, decision log, invariants, risks, threat model, evidence manifest, and worklog so the new command surface and residual gaps are explicit

Expected affected files:

- `Makefile`
- `scripts/localnet-deploy-dar.sh`
- new Quickstart control-plane scripts under `scripts/`
- new Quickstart scenario inputs and evidence directories under `infra/quickstart/`
- `daml/CantonCollateral/` only if a shared seed or status helper is required
- `infra/quickstart/README.md`
- `docs/integration/LOCALNET_DEMO_PLAN.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/runbooks/LOCALNET_CONTROL_PLANE_RUNBOOK.md`
- `docs/runbooks/README.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-14-execution-report.md`
- `docs/mission-control/WORKLOG.md`
- additional documentation only where required to keep the command surface, evidence surface, and runbooks consistent

Risk assessment:

- Quickstart auth, participant-user, or onboarding assumptions could differ between the pinned stack and the repo-owned seed flow, which would block seeding even though DAR deployment already works
- allocating parties or scenario users incorrectly could weaken the confidentiality demonstration by collapsing roles onto one participant or by granting broader rights than intended
- a seed flow that only records local assumptions instead of ledger-returned identifiers would fail the requirement to prove the scenario exists on Quickstart
- live asset adapters remain absent, so the seeded scenario must stay explicit about what is real ledger state versus what is still deferred adapter execution

Acceptance criteria:

- `make localnet-start-control-plane`, `make localnet-seed-demo`, and `make localnet-status-control-plane` exist, are documented, and fail clearly when prerequisites are missing
- the Control Plane DAR is deployed into the pinned Quickstart environment and one confidential collateral scenario is seeded there with explicit parties and contract identifiers
- machine-readable and human-readable Quickstart evidence artifacts are generated from the real seed and status flow
- the new LocalNet control-plane runbook documents bootstrap, start, deploy, seed, inspect, teardown, and common failures
- tracker, roadmap, decision log, invariants, risks, threat model, evidence manifest, and worklog all reflect the new seeded Quickstart posture and the remaining adapter gap

## 2026-03-29 - Prompt 14 Quickstart Seeded Confidential Scenario - Post-Change

Outcome:
Extended the pinned Quickstart foundation from package deployment only to a real seeded Quickstart scenario by adding an isolated overlay start path, a multi-participant Daml Script seed and status layer, operator runbooks, and machine-readable deployment plus seed plus status evidence.

Completed changes:

- added the repo-owned Quickstart control-plane command surface:
  - `make localnet-start-control-plane`
  - `make localnet-seed-demo`
  - `make localnet-status-control-plane`
- added the overlay runtime assets needed to keep the LocalNet isolated and upstream-preserving, including `infra/quickstart/overlay/control-plane-compose.yaml`, dedicated port suffixes in the overlay profiles, the shared helper shell library, and the containerized Quickstart Daml Script runner
- added `daml/CantonCollateral/QuickstartSeed.daml` plus `infra/quickstart/scenarios/confidential-margin-scenario.json` so the Quickstart path can allocate the required parties and users, seed one confidential margin-style obligation, provider inventory set, and posting intent, and query provider-visible ledger state from the running LocalNet
- generated real Quickstart evidence artifacts:
  - `reports/generated/localnet-control-plane-deployment-receipt.json`
  - `reports/generated/localnet-control-plane-deployment-summary.md`
  - `reports/generated/localnet-control-plane-seed-receipt.json`
  - `reports/generated/localnet-control-plane-status.json`
  - `reports/generated/localnet-control-plane-status-summary.md`
- added ADR 0017, the LocalNet control-plane runbook, the Prompt 14 execution report, and aligned the tracker, roadmap, decision log, invariant registry, evidence manifest, risk register, threat model, README surfaces, and operator setup docs with the seeded Quickstart posture

Architecture and ADR note:

- ADR 0017 was added because Prompt 14 introduces a new durable operating boundary: the Control Plane now starts, seeds, and queries the pinned Quickstart LocalNet through repo-owned overlays and Daml Script instead of stopping at package upload only

Commands run:

```sh
sh -n scripts/localnet-control-plane-common.sh
sh -n scripts/run-quickstart-daml-script.sh
sh -n scripts/localnet-start-control-plane.sh
sh -n scripts/localnet-seed-demo.sh
sh -n scripts/localnet-status-control-plane.sh
sh -n scripts/localnet-deploy-dar.sh
sh -n scripts/run-localnet-smoke.sh
make daml-build
make localnet-build-dar
make localnet-start-control-plane
make localnet-seed-demo
make localnet-status-control-plane
make docs-lint
git diff --check
git status --short --branch
```

Results:

- the Quickstart overlay start command passed and deployed package id `829c57ff1186dd09d4e3e232f2ac08c447de2bfe7c7f3b0cc3bf433fb3190f63` from `.daml/dist-quickstart/canton-collateral-control-plane-0.1.1.dar` into the pinned Quickstart participants through onboarding container `control-plane-splice-onboarding`
- the seed command passed and created the default scenario `quickstart-confidential-margin-001` with:
  - provider party `app_user_canton-collateral-1::122029d17b90ca982c572b237f30895dd12b8db8582d623e473ed8059ce3e4185d0a`
  - secured party `app_provider_canton-collateral-1::12208903631325bcb3f6a87594729003aa53482189f278200572cb23b01e795a5afc`
  - custodian party `controlplane-custodian-1::12208903631325bcb3f6a87594729003aa53482189f278200572cb23b01e795a5afc`
  - operator party `controlplane-operator-1::12208903631325bcb3f6a87594729003aa53482189f278200572cb23b01e795a5afc`
  - obligation `quickstart-margin-obligation-001`
  - posting intent `quickstart-margin-posting-001`
  - inventory lots `quickstart-us-tbill-lot-001` and `quickstart-us-tbill-lot-002`
- the refreshed status command passed and confirmed the provider-visible Quickstart view sees `1` obligation, `2` inventory lots, and `1` posting intent for the seeded scenario, while execution-report and encumbrance counts remain `0`
- `make docs-lint` passed after the seeded Quickstart command, runbook, ADR, tracker, invariant, and evidence surfaces were added
- `git diff --check` passed with no whitespace or malformed patch issues

Residual risks and follow-up:

- the seeded Quickstart surface still stops at seeded ledger state rather than a full Quickstart-backed workflow execution report
- live asset adapters, settlement-window enforcement, workflow-coupled optimizer reservation, and production-grade collateral business logic remain intentionally absent
- future Daml changes must continue to preserve compatibility across the host-native `2.10.4` path and the containerized Quickstart `3.4.10` path

## 2026-03-29 - Prompt 13 Quickstart Runtime Bridge - Pre-Change

Intent:
Choose and implement the smallest credible runtime-bridge strategy that lets the Canton Collateral Control Plane DAR build and attempt deployment into the pinned upstream Quickstart LocalNet instead of leaving the Quickstart path blocked at version mismatch.

Task summary:

- determine whether the correct bridge is a repo Daml upgrade, a dual-runtime bridge, or a Quickstart re-pin
- implement the chosen runtime strategy across toolchain pins, bootstrap scripts, and deployment command surface
- add an ADR, operator evidence, and mission-control updates so the Quickstart deployment path is explicit, reproducible, and no longer documented only as an unresolved blocker

Expected affected files:

- `daml.yaml`
- `Makefile`
- `scripts/toolchain.env`
- `scripts/bootstrap.sh`
- `scripts/dev-status.sh`
- `infra/quickstart/bootstrap-localnet.sh`
- `infra/quickstart/README.md`
- `docs/adrs/0016-quickstart-runtime-bridge.md`
- `docs/setup/DEPENDENCY_POLICY.md`
- `docs/setup/LOCAL_DEV_SETUP.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-13-execution-report.md`
- `docs/mission-control/WORKLOG.md`
- additional repo-surface documentation updated only where required to keep the command surface and tracker consistent

Risk assessment:

- upgrading the repo Daml line could break existing IDE-ledger workflow scripts or require a Java baseline change that ripples through bootstrap and verification
- introducing a dual-runtime path could make the repo harder to reproduce if the bootstrap, status, and docs do not make the split explicit and deterministic
- re-pinning Quickstart to an older runtime could move the repo away from the current upstream LocalNet direction and weaken the existing overlay-first foundation
- deployment into Quickstart may still be environment-sensitive if Docker or the upstream stack is not fully built and running, so failure handling and evidence need to stay explicit

Acceptance criteria:

- one explicit runtime strategy is chosen and justified in a new ADR
- the Control Plane DAR builds under the chosen strategy
- the repository exposes a real deployment-oriented Quickstart command that checks readiness and fails clearly
- dependency, setup, Quickstart, tracker, and evidence docs consistently reflect the chosen strategy
- execution evidence records the exact commands run, what passed or failed, and the remaining residual risks

## 2026-03-29 - Prompt 13 Quickstart Runtime Bridge - Post-Change

Outcome:
Closed the Quickstart runtime bridge through an ADR-backed dual-runtime strategy that keeps the repo-default host toolchain on Daml `2.10.4` plus JDK `17` while building and deploying Quickstart-compatible DARs in Docker on Daml `3.4.10` plus Java `21`.

Completed changes:

- added ADR 0016 and aligned the tracker, roadmap, decision log, dependency policy, local setup guide, Quickstart integration docs, evidence manifest, risk register, threat model, runbook index, README surfaces, and Prompt 13 execution evidence around the explicit dual-runtime bridge decision
- added `scripts/build-quickstart-dar.sh`, `scripts/localnet-deploy-dar.sh`, `make localnet-build-dar`, and `make localnet-deploy-dar` so the Control Plane DAR can be built against the pinned Quickstart runtime line and installed into a running pinned Quickstart LocalNet
- updated `scripts/bootstrap.sh`, `scripts/dev-status.sh`, `scripts/toolchain.env`, and `infra/quickstart/bootstrap-localnet.sh` so the host-native versus Quickstart-bridge split is visible to operators
- updated the Daml source to compile on both runtime lines by replacing the return replay key path with `ReturnRequestRegistry` and by switching the shared Daml Script contract-query helpers to template-specific variants
- verified the bridge against a live pinned Quickstart LocalNet by building the upstream Quickstart licensing DAR in Docker, bringing up the upstream runtime slice with Keycloak enabled, and uploading the Control Plane DAR into the app-provider and app-user participants

Architecture and ADR note:

- ADR 0016 was added because the runtime-bridge choice changes how the repository builds, deploys, and documents Daml packages against the pinned Quickstart runtime line

Commands run:

```sh
make localnet-bootstrap
make daml-build
make daml-test
make localnet-build-dar
cd .runtime/localnet/cn-quickstart/quickstart && make check-docker
cd .runtime/localnet/cn-quickstart/quickstart && . /Users/charlesdusek/Code/canton-collateral-control-plane/.runtime/env.sh && make build
. ./scripts/toolchain.env && docker run --rm -i -v "$PWD/.runtime/localnet/cn-quickstart/quickstart:/workspace" -w /workspace/daml/licensing -e QUICKSTART_DAML_SDK_VERSION="$QUICKSTART_DAML_SDK_VERSION" -e QUICKSTART_DAML_SDK_LINUX_AARCH64_ARCHIVE="$QUICKSTART_DAML_SDK_LINUX_AARCH64_ARCHIVE" -e QUICKSTART_DAML_SDK_LINUX_AARCH64_URL="$QUICKSTART_DAML_SDK_LINUX_AARCH64_URL" -e QUICKSTART_DAML_SDK_LINUX_AARCH64_SHA256="$QUICKSTART_DAML_SDK_LINUX_AARCH64_SHA256" ubuntu:24.04 /bin/sh <<'EOF'
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update >/dev/null
apt-get install -y ca-certificates curl gzip openjdk-21-jdk-headless tar >/dev/null
curl -fsSL "$QUICKSTART_DAML_SDK_LINUX_AARCH64_URL" -o "/tmp/$QUICKSTART_DAML_SDK_LINUX_AARCH64_ARCHIVE"
echo "$QUICKSTART_DAML_SDK_LINUX_AARCH64_SHA256  /tmp/$QUICKSTART_DAML_SDK_LINUX_AARCH64_ARCHIVE" | sha256sum -c - >/dev/null
tar -xzf "/tmp/$QUICKSTART_DAML_SDK_LINUX_AARCH64_ARCHIVE" -C /tmp
sdk_dir="/tmp/sdk-$QUICKSTART_DAML_SDK_VERSION"
export PATH="$sdk_dir/daml:$sdk_dir/daml-helper:$PATH"
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-arm64
export DAML_HOME=/tmp/daml-home
mkdir -p "$DAML_HOME/sdk" "$DAML_HOME/bin"
ln -s "$sdk_dir" "$DAML_HOME/sdk/$QUICKSTART_DAML_SDK_VERSION"
ln -s "$sdk_dir/daml/daml" "$DAML_HOME/bin/daml"
cat > "$DAML_HOME/daml-config.yaml" <<CFG
update-check: never
auto-install: false
CFG
daml build --project-root /workspace/daml/licensing
EOF
cd .runtime/localnet/cn-quickstart/quickstart && export MODULES_DIR="$PWD/docker/modules" LOCALNET_DIR="$PWD/docker/modules/localnet" LOCALNET_ENV_DIR="$PWD/docker/modules/localnet/env" IMAGE_TAG="$(sed -n 's/^SPLICE_VERSION=//p' .env)" && docker compose --profile app-provider --profile app-user --profile sv --profile swagger-ui --profile pqs-app-provider --profile keycloak -f compose.yaml -f "$LOCALNET_DIR/compose.yaml" -f "$MODULES_DIR/keycloak/compose.yaml" -f "$MODULES_DIR/splice-onboarding/compose.yaml" -f "$MODULES_DIR/pqs/compose.yaml" --env-file .env --env-file .env.local --env-file "$LOCALNET_DIR/compose.env" --env-file "$LOCALNET_ENV_DIR/common.env" --env-file "$MODULES_DIR/keycloak/compose.env" --env-file "$MODULES_DIR/pqs/compose.env" up -d --build keycloak nginx-keycloak canton splice splice-onboarding
make localnet-deploy-dar
make docs-lint
make verify-portable
make verify
git diff --check
git status --short --branch
```

Results:

- `make daml-build`, `make daml-test`, `make localnet-build-dar`, `make localnet-deploy-dar`, `make docs-lint`, `make verify-portable`, `make verify`, and `git diff --check` all passed
- the first host-side upstream `make build` attempt failed at Quickstart's Daml `3.4.10` verification step, which confirmed that the repo should keep the host-native `2.10.4` path and use the documented containerized bridge for Quickstart-compatible DAR production instead
- the first deployment attempts surfaced and then resolved repo-owned bridge issues in the container stdin wiring, env sourcing, and metadata path normalization before the final Quickstart upload succeeded
- the final `make localnet-deploy-dar` execution uploaded the Control Plane DAR into both pinned Quickstart participants and confirmed package presence by package id `fc0d45f0d0ee032245807bdeba0be201d3c5c9518fa150cf804985440b05efe8`

Residual risks and follow-up:

- the bridge remains dual-runtime, so future Daml source changes must continue to be checked on both the host-native and Quickstart-compatible build paths
- the package is now installable into Quickstart, but seeded Quickstart-backed workflow execution, role-scoped report disclosure, and live asset adapters remain future work

## 2026-03-29 - Test Harness Enhancements - Pre-Change

Intent:
Implement the highest-value test-structure improvements identified in the prior analysis by extracting shared Python test fixtures, adding isolated conformance-check tests, and separating always-portable verification from Docker-backed LocalNet smoke validation.

Starting state:

- worktree is dirty from the prior successful verification run because `WORKLOG.md` and several generated report artifacts were refreshed with current timestamps
- the current test surface passes, but conformance helper logic is only lightly isolated, policy-engine and optimizer tests duplicate fixture mutation code, and `make verify` is environment-sensitive because it always includes `make localnet-smoke`

Expected focus areas:

- reduce duplicated scenario setup across `test/policy-engine/` and `test/optimizer/`
- test conformance helper behavior directly without always depending on a full aggregate rerun
- preserve the existing full verification path while introducing a portable verification path that does not require Docker
- update invariants, evidence, and operator-facing documentation to reflect the improved test harness

Planned commands:

```sh
make test-policy-engine
make test-optimizer
make test-conformance
make docs-lint
make verify-portable
make verify
git diff --check
git status --short --branch
```

## 2026-03-29 - Test Harness Enhancements - Post-Change

Outcome:
Implemented the highest-value test-harness improvements by introducing a shared deterministic Python fixture-builder module, adding isolated conformance-helper unit tests, and separating Docker-free repository verification from the full Quickstart-aware verification path.

Completed changes:

- added `testsupport/fixture_builders.py` and refactored the policy-engine plus optimizer suites to consume shared deterministic fixtures instead of duplicating JSON loading and concentration-relaxation setup
- added `test/conformance/test_conformance_checks.py` so authorization, no-double-encumbrance, atomic substitution, replay-safety, report-fidelity, and audit-trail helper logic can fail independently of a full aggregate rerun
- added `scripts/verify-portable.sh` plus `make verify-portable` as the Docker-free baseline verification loop
- updated `scripts/verify.sh` so `make verify` now composes `make verify-portable` and `make localnet-smoke` instead of duplicating the command sequence
- aligned README, contributing, local setup, test strategy, conformance, invariant, evidence, tracker, AGENTS, and final-demo-pack command-surface documentation to the new verification tiers and test-harness structure

Architecture and ADR note:

- no ADR was added because the change refines the existing test harness and command surface within the current architecture rather than introducing a new architectural boundary or subsystem contract

Commands run:

```sh
chmod +x scripts/verify-portable.sh
make test-policy-engine
make test-optimizer
make test-conformance
make docs-lint
make verify-portable
make verify
git diff --check
git status --short --branch
```

Results:

- `make test-policy-engine` passed with 8 tests after the shared fixture refactor
- `make test-optimizer` passed with 7 tests after the shared fixture refactor
- `make test-conformance` passed with 11 tests, reflecting the original generated-suite assertions plus the new isolated helper-check unit tests
- `make docs-lint` passed with the new `make verify-portable` documentation requirements
- `make verify-portable` passed as the Docker-free baseline verification loop
- `make verify` passed as the full superset, including the pinned Quickstart compose-config smoke validation
- `git diff --check` passed with no whitespace or patch-format issues
- `git status --short --branch` now shows the expected source, documentation, and regenerated artifact updates from the successful verification run

Next step:
Consider whether the generated report artifacts should move to deterministic timestamps or a check-only comparison mode so successful verification loops stop dirtying the worktree when no semantic behavior changed.

## 2026-03-29 - Test Stabilization And Analysis - Pre-Change

Intent:
Run the repository's full test and verification surface, iterate on any failures until all checks are green, and then perform a detailed analysis of the current test structure with concrete enhancement recommendations.

Starting state:

- worktree is clean on `main`
- the repository's documented verification surface includes policy-engine, optimizer, Daml, conformance, demo-pack, documentation, and aggregate verify targets

Expected focus areas:

- diagnose and fix any regressions that block the documented test commands from passing
- preserve deterministic behavior and existing evidence generation semantics while repairing failures
- assess layering, duplication, gaps, fixture reuse, and traceability across the current test surface after the suite is green

Planned commands:

```sh
make test-policy-engine
make test-optimizer
make daml-test
make test-conformance
make demo-all
make docs-lint
make verify
git diff --check
git status --short --branch
```

## 2026-03-29 - Test Stabilization And Analysis - Post-Change

Outcome:
Executed the repository's documented verification surface end to end, confirmed that the policy-engine, optimizer, Daml workflow, conformance, demo-pack, documentation, and aggregate verification targets all pass, and completed a follow-on analysis of the current test structure and upgrade opportunities.

Observed issue and resolution:

- `make verify` initially failed in the `localnet-smoke` leg because the Docker daemon was not running
- confirmed the failure with `docker info` and the upstream Quickstart `make check-docker` gate
- started Docker Desktop locally, re-ran `make localnet-smoke`, and then re-ran `make verify` successfully
- no repository source-code or business-logic fix was required; the failure was environmental and the repo-side smoke gate behaved correctly

Commands run:

```sh
make test-policy-engine
make test-optimizer
make daml-test
make test-conformance
make demo-all
make docs-lint
make verify
make localnet-smoke
docker info
git diff --check
git status --short --branch
```

Results:

- `make test-policy-engine` passed with 8 unit tests plus report-schema validation
- `make test-optimizer` passed with 7 unit tests plus report-schema validation
- `make daml-test` passed and the three lifecycle scripts completed successfully on the IDE ledger
- `make test-conformance` passed and regenerated the aggregate conformance report plus supporting evidence
- `make demo-all` passed and regenerated the final demo pack
- `make docs-lint` passed
- `make verify` passed after Docker Desktop was started, including the pinned Quickstart compose-config smoke path
- `git diff --check` passed with no whitespace or patch-format issues
- `git status --short --branch` shows the worklog update plus refreshed generated report artifacts with current timestamps from the successful verification run

Follow-up analysis focus:

- the current suite is strong on deterministic scenario assertions and evidence-backed demo verification
- the next highest-value improvements are fixture extraction, more isolated conformance-check tests, portable versus Docker-backed verification tiers, and a strategy for timestamped generated artifacts that currently dirty the worktree on successful reruns

Next step:
Convert the current evidence-first test surface into a more maintainable harness by extracting shared builders, adding isolated tests for conformance-check helpers and report contracts, and separating always-portable verification from environment-dependent LocalNet smoke validation.

## 2026-03-28 - Prompt 12 - Pre-Change

Intent:
Build the conformance suite and final end-to-end demo pack for the Canton Collateral Control Plane prototype by unifying the existing confidential margin-call, substitution, and return flows into a reproducible, proposal-ready verification and evidence surface.

Risks addressed:

- the current prototype demonstrates individual flows, but lacks a single conformance harness that proves role control, determinism, replay safety, audit completeness, and report fidelity across the full demo surface
- reviewers could mistake generated artifacts for narrative-only examples unless the repository adds a single deterministic `make demo-all` path and explicit machine-readable evidence indexing
- future Canton projects, venues, custodians, financing applications, and token issuers still need a clearer integration contract boundary to understand how to consume policy, workflow, report, and evidence outputs safely
- release confidence would remain incomplete unless the final demo package is tied to invariant checking, mission-control updates, reproducible commands, and a full repository verification pass

Affected files:

- `Makefile`
- `README.md`
- `test/conformance/`
- `app/orchestration/`
- `scripts/`
- `reports/generated/`
- `docs/testing/CONFORMANCE_SUITE.md`
- `docs/runbooks/FINAL_DEMO_RUNBOOK.md`
- `docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md`
- `docs/evidence/DEMO_ARTIFACT_INDEX.md`
- `docs/evidence/prompt-12-execution-report.md`
- `docs/adrs/0014-conformance-and-demo-package.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/WORKLOG.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`

Acceptance criteria:

- the repository exposes a reproducible conformance suite with a real `make test-conformance` command covering authorization and role control, eligibility determinism, haircut correctness, no double-encumbrance, atomic substitution when required, replay safety, report fidelity, and audit trail completeness
- the repository exposes a real `make demo-all` command that produces JSON and Markdown artifacts for confidential margin call, substitution, and return flows plus invariant pass/fail output
- the final demo pack indexes real artifacts and documents how third parties integrate with the Control Plane through stable policy, workflow, reporting, and evidence surfaces
- mission-control, ADR, invariant, evidence, risk, threat, runbook, and README surfaces reflect the final packaged prototype
- the full verification path is executed, changes are committed, and the worktree is left clean

Planned commands:

```sh
make demo-all
make test-conformance
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git diff --check
git status --short --branch
```

## 2026-03-28 - Prompt 12 - Post-Change

Outcome:
Packaged the existing confidential margin-call, collateral-substitution, and margin-return prototypes into one proposal-ready conformance suite and final demo pack by adding aggregate orchestration, explicit invariant pass/fail output, a final artifact index, and a documented third-party integration boundary for the Canton Collateral Control Plane.

Completed artifacts:

- new aggregate conformance runner plus CLI under `app/orchestration/` with a real `make test-conformance` command
- new final demo-pack generator plus CLI under `app/orchestration/` with a real `make demo-all` command
- new aggregate conformance test surface under `test/conformance/`
- new operator and reviewer docs under `docs/testing/CONFORMANCE_SUITE.md`, `docs/runbooks/FINAL_DEMO_RUNBOOK.md`, `docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md`, and `docs/evidence/DEMO_ARTIFACT_INDEX.md`
- new ADR under `docs/adrs/0014-conformance-and-demo-package.md` plus Quickstart ADR renumbered to `docs/adrs/0015-quickstart-demo-foundation.md`
- regenerated real demo evidence under `reports/generated/` including the conformance suite report, final demo pack, and refreshed margin-call, substitution, and return artifacts
- mission-control, invariant, evidence, risk, threat, README, contributing, setup, and status surfaces aligned to the final packaged prototype
- prompt execution evidence under `docs/evidence/prompt-12-execution-report.md`

Commands run:

```sh
make demo-all
make test-conformance
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git diff --check
git status --short --branch
```

Results:

- `make demo-all` passed and generated `reports/generated/final-demo-pack.json` plus `reports/generated/final-demo-pack-summary.md`
- `make test-conformance` passed and generated `reports/generated/conformance-suite-report.json`, `reports/generated/conformance-suite-summary.md`, and the supporting determinism and haircut evidence artifacts
- `make test-policy-engine` passed and regenerated the committed baseline `PolicyEvaluationReport` artifact
- `make test-optimizer` passed and regenerated the committed baseline `OptimizationReport` artifact
- `make daml-test` passed and preserved the Daml lifecycle-script baseline for margin call, substitution, and return workflows
- `make docs-lint` passed after the new conformance, demo-pack, integration, runbook, ADR, tracker, and evidence surfaces were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, the aggregate conformance suite, the final demo pack, and the pinned Quickstart compose-preflight smoke path in one reproducible loop
- `git diff --check` passed with no whitespace or patch-format issues
- `git status --short --branch` before commit showed only the expected Prompt 12 code, documentation, ADR, mission-control, and generated-artifact changes

Next step:
Bridge the repo Daml package into the pinned Quickstart runtime line, then define role-scoped disclosure profiles, versioned reference-data contracts, and workflow-coupled reservation plus consent interfaces on top of the now-packaged prototype.

## 2026-03-28 - Prompt 1 - Pre-Change

Intent:
Create the repository's mission-control and documentation spine without adding business logic.

Starting state:

- repository contains only `.git`
- no operating instructions or architecture documents exist yet

Planned commands:

```sh
make status
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 11 - Pre-Change

Intent:
Implement the first end-to-end confidential margin return and release prototype for the Canton Collateral Control Plane, including a real `make demo-return` command, Daml workflow support for return and release control, operator documentation, machine-readable return reporting, and deterministic negative-path evidence.

Risks addressed:

- return and release handling are safety-critical, and the current prototype does not yet prove authorization-gated collateral release
- encumbrance state could drift if the return workflow does not reconcile requested amounts, released lots, and post-release obligation state deterministically
- replayed return instructions or unauthorized release attempts could appear to succeed unless the workflow and demo artifacts make the control failures explicit
- proposal and demo reviewers need machine-readable evidence that the Control Plane enforces secured-party control, authorization, and release-state integrity without relying on narrative-only summaries

Affected files:

- `Makefile`
- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `app/README.md`
- `app/orchestration/return_cli.py`
- `app/orchestration/return_demo.py`
- `daml/Bootstrap.daml`
- `daml/CantonCollateral/Return.daml`
- `daml/CantonCollateral/Test.daml`
- `examples/README.md`
- `examples/demo-scenarios/return/`
- `reports/README.md`
- `reports/generated/`
- `reports/schemas/return-report.schema.json`
- `docs/specs/RETURN_REPORT_SPEC.md`
- `docs/runbooks/RETURN_DEMO_RUNBOOK.md`
- `docs/testing/DAML_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/runbooks/README.md`
- `docs/adrs/README.md`
- `docs/adrs/0013-return-and-release-control.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-11-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`

Acceptance criteria:

- the prototype demonstrates a real positive return workflow from declared scenario inputs through Daml execution
- authorization, secured-party control, replay protection, and obligation-state checks are explicit in the workflow and report artifacts
- return execution updates encumbrance state deterministically and emits a machine-readable return report plus operator-facing Markdown artifacts
- negative-path scenarios cover unauthorized release, replayed return instruction, and obligation-versus-request amount mismatch without fabricating success
- mission-control, invariants, evidence, ADR, runbook, and reproducible command surfaces are updated for proposal and demo use
- relevant commands are run, the changes are committed, and the worktree is left clean

Planned commands:

```sh
make demo-return
make daml-test
make test-policy-engine
make test-optimizer
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 11 - Post-Change

Outcome:
Implemented the repository's first end-to-end confidential return and release prototype by tightening the Daml return workflow, adding a retained-set-based return orchestration layer, publishing a machine-readable `ReturnReport` contract, generating real positive and negative return artifacts, and aligning the mission-control, ADR, runbook, and evidence surfaces to the new control model.

Completed artifacts:

- new return orchestration surface under `app/orchestration/` with a real `make demo-return` command
- expanded Daml return workflow, parameterized return demo script, and lifecycle tests under `daml/CantonCollateral/`
- new return scenario bundle under `examples/demo-scenarios/return/`
- new return-report schema and specification under `reports/schemas/return-report.schema.json` and `docs/specs/RETURN_REPORT_SPEC.md`
- new operator runbook under `docs/runbooks/RETURN_DEMO_RUNBOOK.md`
- new ADR under `docs/adrs/0013-return-and-release-control.md` plus renumbered Quickstart ADR under `docs/adrs/0015-quickstart-demo-foundation.md`
- regenerated real demo artifacts under `reports/generated/` including the return report, Markdown summary, timeline, positive workflow result, and the negative-path policy, optimization, and workflow artifacts
- mission-control, invariant, risk, threat, README, setup, testing, evidence, and command-surface updates aligned to the new prototype
- prompt execution evidence under `docs/evidence/prompt-11-execution-report.md`

Commands run:

```sh
make status
make demo-return
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git diff --check
git status --short --branch
```

Results:

- `make status` passed and reported `Current Phase: Milestone 4 / Phase 4 - Initial Margin Call, Return, And Substitution Demo Reporting`
- `make demo-return` passed and generated `reports/generated/return-demo-report.json` plus the supporting JSON and Markdown artifacts for one positive and three negative scenarios
- `make test-policy-engine` passed and regenerated the committed baseline `PolicyEvaluationReport` artifact
- `make test-optimizer` passed and regenerated the committed baseline `OptimizationReport` artifact
- `make daml-test` passed and extended the Daml lifecycle-script baseline for return replay blocking, unauthorized release prevention, and obligation-state mismatch handling
- `make docs-lint` passed after the new return docs, ADR, runbook, tracker, and evidence surfaces were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, all three end-to-end demos, and the Quickstart compose-preflight smoke path
- `git diff --check` passed with no whitespace or patch-format issues
- `git status --short --branch` before commit showed only the expected Prompt 11 code, documentation, schema, example, generated-artifact, and ADR-renumbering changes

Next step:
Bridge the repo Daml package into the pinned Quickstart runtime line, then define role-scoped execution, return, and substitution report profiles plus workflow-coupled reservation and consent interfaces on top of the current demo set.

Expected artifacts:

- repository operating instructions
- mission-control tracker, roadmap, worklog, and decision log
- starter ADR, invariants, risks, evidence, security, testing, and change-control documents

## 2026-03-28 - Prompt 1 - Post-Change

Outcome:
Created the repository's initial mission-control spine and kept the repo documentation-only.

Completed artifacts:

- root operating documents: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CODEOWNERS`, `.gitignore`, `Makefile`
- mission-control documents under `docs/mission-control/`
- starter ADR, invariants, risks, evidence, integration, domain, testing, security, runbook, and change-control documents
- prompt execution report in `docs/evidence/prompt-01-execution-report.md`

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed
- `make status` reported Phase 0 and the expected untracked documentation tree before commit
- `make verify` passed and confirmed the repository remains documentation-only

Next step:
Pin the target Quickstart or LocalNet and document the first interface and dependency ADRs before adding business logic.

## 2026-03-28 - Proposal Alignment - Pre-Change

Intent:
Use the development-fund proposal as a stronger framing input for repository architecture, scope, milestones, and invariant planning.

Starting state:

- repository has a generic mission-control spine
- proposal introduces a concrete control-plane framing, five-layer reference stack, milestone plan, and broader workflow scope

Planned commands:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Expected artifacts:

- updated repo framing and roadmap aligned to the proposal
- expanded invariant and integration documentation
- ADR and decision-log updates where the proposal changes repository-level architecture assumptions

## 2026-03-28 - Proposal Alignment - Post-Change

Outcome:
Aligned the repository docs to the 2026-03-28 development-fund proposal and made the control-plane framing explicit without adding business logic.

Completed artifacts:

- proposal-aligned repository framing in `README.md` and `docs/mission-control/MASTER_TRACKER.md`
- milestone structure updated in `docs/mission-control/ROADMAP.md`
- initial architectural ADR later refined into `docs/adrs/0002-system-boundaries.md`, `docs/adrs/0003-policy-optimization-workflow-separation.md`, and `docs/adrs/0004-report-fidelity-and-evidence.md`
- expanded invariant, integration, glossary, testing, evidence, and risk documents
- decision log updated to reflect the adopted solution shape

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed after the proposal-alignment updates
- `make status` continued to report `Current Phase: Phase 0 - Mission Control Spine`
- `make verify` passed and confirmed the repository remains documentation-only

Next step:
Translate the proposal's Milestone 1 into concrete repository artifacts: `CPL v0.1`, policy profiles, and the first dependency and interface ADRs.

## 2026-03-28 - Prompt 2 - Pre-Change

Intent:
Design the repository's technical architecture and domain model for a Canton-native collateral control plane, with explicit separation between policy language, policy evaluation, optimization, Daml workflow orchestration, reporting/evidence, and demo/runtime infrastructure.

Risks addressed:

- ambiguous system boundaries could let policy, optimization, workflow, and reporting concerns bleed together
- privacy and report-fidelity assumptions could stay implicit instead of being pinned to Canton-native boundaries
- future implementation prompts could diverge without a shared lifecycle model, domain vocabulary, and integration plan

Affected files:

- `docs/architecture/OVERVIEW.md`
- `docs/architecture/COMPONENTS.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/DEPLOYMENT_MODEL.md`
- `docs/architecture/PRIVACY_MODEL.md`
- `docs/adrs/0002-system-boundaries.md`
- `docs/adrs/0003-policy-optimization-workflow-separation.md`
- `docs/adrs/0004-report-fidelity-and-evidence.md`
- `docs/domain/COLLATERAL_DOMAIN_MODEL.md`
- `docs/domain/ACTORS_AND_ROLES.md`
- `docs/domain/LIFECYCLE_STATES.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-02-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `docs/adrs/README.md`
- `Makefile`

Acceptance criteria:

- the repository has a crisp technical architecture for a Canton-native collateral control plane
- domain concepts and lifecycle states are unambiguous
- future implementation prompts have enough guidance to stay coherent
- the design clearly supports future third-party integration

Planned commands:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 2 - Post-Change

Outcome:
Published the repository's first full architecture and domain package for a Canton-native collateral control plane, with explicit separation between policy language, policy evaluation, optimization, Daml workflow orchestration, reporting and evidence, and demo/runtime infrastructure.

Completed artifacts:

- architecture overview, component, data-flow, deployment, and privacy documents under `docs/architecture/`
- new ADR set in `docs/adrs/0002-system-boundaries.md`, `docs/adrs/0003-policy-optimization-workflow-separation.md`, and `docs/adrs/0004-report-fidelity-and-evidence.md`
- domain model, actors-and-roles, and lifecycle-state documents under `docs/domain/`
- Quickstart integration and token-standard alignment guidance under `docs/integration/`
- mission-control, invariant, risk, threat, evidence, and validation updates aligned to the new architecture package
- prompt execution record in `docs/evidence/prompt-02-execution-report.md`

Commands run:

```sh
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make docs-lint` passed
- `make status` passed and continued to report `Current Phase: Phase 0 - Mission Control Spine`
- `make verify` passed and confirmed the repository remains documentation-only
- architecture and domain guidance now cover system boundaries, privacy, lifecycle transitions, and future third-party integration assumptions

Next step:
Pin the Quickstart and asset-adapter dependency set, then formalize the first `CPL v0.1`, policy decision report, execution report, and Daml package contracts against the documented architecture.

## 2026-03-28 - Prompt 3 - Pre-Change

Intent:
Design and publish the first `CPL v0.1` package as a prose specification plus a machine-readable schema, supported by validating example policies, a minimal durable validation toolchain, and mission-control traceability updates.

Risks addressed:

- the repository currently describes CPL conceptually but does not yet expose a versioned machine-readable contract
- policy coverage could remain too weak for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style controls
- schema drift or weak validation could undermine later deterministic policy-engine work
- operators would lack a reproducible command to prove example policies conform to the published schema

Affected files:

- `README.md`
- `Makefile`
- `requirements-cpl-validation.txt`
- `docs/specs/CPL_SPEC_v0_1.md`
- `docs/specs/CPL_EXAMPLES.md`
- `schema/cpl.schema.json`
- `examples/policies/central-bank-style-policy.json`
- `examples/policies/tri-party-style-policy.json`
- `examples/policies/ccp-style-policy.json`
- `examples/policies/bilateral-csa-style-policy.json`
- `docs/adrs/0005-cpl-format-and-versioning.md`
- `docs/adrs/README.md`
- `docs/testing/CPL_VALIDATION_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-03-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `docs/runbooks/README.md`

Acceptance criteria:

- `CPL v0.1` exists as both prose spec and machine-readable schema
- the four example policy files validate successfully
- the schema is strong enough to support later policy-engine work without relying on hidden conventions
- central-bank, tri-party, CCP, and bilateral market-practice mappings are documented clearly
- the repository exposes at least one reproducible validation command such as `make validate-cpl`

Planned commands:

```sh
make validate-cpl
make docs-lint
make status
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 3 - Post-Change

Outcome:
Published the first formal `CPL v0.1` package for the repository, including a normative specification, strict JSON Schema, four validating market-profile examples, a pinned validation toolchain, and the required mission-control traceability updates.

Completed artifacts:

- `CPL v0.1` prose specification and example guide under `docs/specs/`
- machine-readable schema in `schema/cpl.schema.json`
- validating example policies for central-bank-style, tri-party-style, CCP-style, and bilateral CSA-style usage under `examples/policies/`
- ADR 0005 for CPL format and versioning plus a dedicated CPL validation test plan
- `make validate-cpl` and the pinned validator dependency in `requirements-cpl-validation.txt`
- README, tracker, decision log, invariant, risk, threat, runbook, evidence, and prompt-execution updates aligned to the new CPL surface

Commands run:

```sh
make validate-cpl
make docs-lint
make status
make verify
git status --short --branch
```

Results:

- `make validate-cpl` passed and confirmed the schema validates against its metaschema, the four example policies validate successfully, and generated negative cases fail as expected
- `make docs-lint` passed
- `make status` passed and reported `Current Phase: Milestone 1 / Phase 1 - CPL And Formal Model`
- `make verify` passed and now includes the CPL schema validation loop in the baseline repository controls
- the repository remains free of business logic while now exposing a durable machine-readable policy contract

Next step:
Define machine-readable `PolicyDecisionReport` and `ExecutionReport` contracts, then pin the Quickstart and asset-adapter dependencies that will consume `CPL v0.1`.

## 2026-03-28 - Prompt 4 - Pre-Change

Intent:
Establish a runnable technical foundation for the prototype with a pinned Daml-centric toolchain, reproducible bootstrap and verification scripts, and directory/package scaffolding that future implementation prompts can extend without restructuring the repository.

Risks addressed:

- dependency drift could block later Daml and Canton work or make local reproduction inconsistent
- the repo's current `verify` contract rejects all implementation files and therefore no longer matches the next prototype phase
- future prompts could start adding workflow, integration, and reporting code without a stable package layout or operator command surface
- service-layer scope could sprawl unless the runtime foundation keeps policy, workflow, reporting, and integration concerns explicitly separated

Affected files:

- `daml.yaml`
- `.tool-versions`
- `Makefile`
- `scripts/bootstrap.sh`
- `scripts/verify.sh`
- `scripts/dev-status.sh`
- `docs/setup/LOCAL_DEV_SETUP.md`
- `docs/setup/DEPENDENCY_POLICY.md`
- `docs/adrs/0006-runtime-foundation.md`
- `docs/adrs/README.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-04-execution-report.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/runbooks/README.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `README.md`
- `daml/`
- `app/`
- `reports/`
- `test/`
- `examples/`
- `infra/`

Acceptance criteria:

- the repo exposes a real runtime and build foundation rooted in Daml for workflow modeling
- bootstrap, status, verify, CPL validation, future Daml build, and future demo commands are reproducible and documented
- pinned dependencies are justified, locally installable, and visible in both code and docs
- future prompts can add Daml packages and small helper services without restructuring the repo
- mission-control, invariant, ADR, and evidence documents reflect the new foundation phase

Planned commands:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 4 - Post-Change

Outcome:
Established the repository's first runnable technical foundation with a pinned Daml-centric toolchain, repo-local bootstrap, a minimal executable Daml package, and a reproducible command surface for setup, build, smoke execution, and verification.

Completed artifacts:

- pinned toolchain files: `daml.yaml`, `.tool-versions`, and `scripts/toolchain.env`
- repo-local bootstrap and control scripts in `scripts/bootstrap.sh`, `scripts/dev-status.sh`, and `scripts/verify.sh`
- minimal executable Daml package in `daml/Foundation.daml` and `daml/Bootstrap.daml`
- reserved repository surfaces for future services, reports, tests, examples, and infrastructure under `app/`, `reports/`, `test/`, `examples/`, and `infra/`
- setup documentation in `docs/setup/LOCAL_DEV_SETUP.md` and `docs/setup/DEPENDENCY_POLICY.md`
- ADR 0006 plus mission-control, invariant, evidence, risk, threat, runbook, and README updates aligned to the new runtime phase
- prompt execution record in `docs/evidence/prompt-04-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make demo-run
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed and installed the pinned repo-local Daml SDK `2.10.4`, Temurin JDK `17.0.18+8`, and validation tooling
- `make status` passed and reported the new runtime-foundation phase, pinned toolchain, installed toolchain, and scaffold directories
- `make validate-cpl` passed and preserved the earlier schema-validation baseline
- `make daml-build` passed and produced the repository DAR artifact under `.daml/dist/`
- `make demo-run` passed and executed the `Bootstrap:foundationSmokeTest` Daml script against the IDE ledger
- `make verify` passed and now covers docs linting, CPL validation, Daml build, and Daml smoke execution in one command
- the repo now has executable runtime scaffolding without yet adding collateral business logic

Next step:
Define the first machine-readable `PolicyDecisionReport` and `ExecutionReport` contracts, then expand the Daml package boundary from the runtime-foundation smoke package into obligation, encumbrance, substitution, return, and settlement contracts.

## 2026-03-28 - Prompt 5 - Pre-Change

Intent:
Implement the first Daml domain model and workflow skeletons for confidential collateral control, including obligation, inventory, encumbrance, substitution, return, settlement, and execution-report surfaces that preserve policy and optimization separation.

Risks addressed:

- privacy boundaries could erode if workflow templates expose more than the required role-specific state
- substitution or return flows could accidentally encode non-atomic or implicitly successful paths
- the first Daml package boundary could collapse policy, workflow, settlement, and reporting concerns into one opaque contract set
- report and state vocabularies could drift from the documented lifecycle model and invariants if they are not pinned together now

Affected files:

- `daml.yaml`
- `Makefile`
- `daml/Bootstrap.daml`
- `daml/CantonCollateral/*.daml`
- `docs/domain/DAML_MAPPING.md`
- `docs/adrs/0007-daml-contract-boundaries.md`
- `docs/testing/DAML_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-05-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `README.md`
- `scripts/dev-status.sh`
- `scripts/verify.sh`

Acceptance criteria:

- Daml modules for roles, assets, lots, encumbrance, obligations, substitution, return, settlement, and execution reporting compile under the pinned SDK
- the repository contains contract-level lifecycle skeletons for margin call creation, posting intent, substitution, approval or rejection, return request, and release or return settlement intent
- the design preserves role separation, privacy intent, and policy-versus-workflow separation
- reproducible build and script execution commands cover the new Daml package and tests

Planned commands:

```sh
make bootstrap
make daml-build
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 5 - Post-Change

Outcome:
Implemented the repository's first real Daml workflow package for confidential collateral control, including contract boundaries for obligations, posting intent, substitution, return, settlement instruction, encumbrance state, and execution reporting, then verified the package with executable Daml lifecycle scripts.

Completed artifacts:

- initial Daml workflow modules under `daml/CantonCollateral/` for shared types, roles, assets, inventory, encumbrance, obligations, posting, substitution, return, settlement, reporting, and tests
- updated `daml/Bootstrap.daml`, `daml.yaml`, `Makefile`, and verification scripts so the new Daml package builds, tests, and smoke-runs from the pinned toolchain
- new contract-boundary ADR in `docs/adrs/0007-daml-contract-boundaries.md`
- new domain-to-Daml mapping in `docs/domain/DAML_MAPPING.md`
- new Daml lifecycle test plan in `docs/testing/DAML_TEST_PLAN.md`
- mission-control, invariant, evidence, risk, security, setup, and contribution docs updated to reflect the first workflow skeleton package
- prompt execution record in `docs/evidence/prompt-05-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make daml-build
make daml-test
make demo-run
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported `Current Phase: Milestone 1 / Phase 1 - CPL, Formal Model, Runtime Foundation, And Initial Daml Workflow Skeletons`
- `make validate-cpl` passed
- `make daml-build` passed and produced the repository DAR artifact under `.daml/dist/`
- `make daml-test` passed and executed the three lifecycle scripts
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make verify` passed and exercised docs linting, CPL validation, Daml build, Daml lifecycle tests, and the workflow smoke run
- `git status --short --branch` showed only the expected task-related changes before commit

Next step:
Define the first machine-readable `PolicyDecisionReport` contract and role-scoped `ExecutionReport` disclosure profiles, then pin the Quickstart overlay and asset-adapter interfaces that will consume the current Daml settlement and encumbrance contracts.

## 2026-03-28 - Prompt 6 - Pre-Change

Intent:
Implement the repository's first real `CPL v0.1` policy evaluation engine, including deterministic eligibility, haircut, lendable-value, concentration, control, and wrong-way-risk checks backed by the published schema and a machine-readable report contract.

Risks addressed:

- the repository currently has a strict CPL schema but no executable evaluator, so policy semantics still stop at documentation
- ad hoc evaluation logic could drift from the published `CPL v0.1` schema and market-practice examples
- report outputs could become non-deterministic or lose explicit machine-readable failure attribution
- concentration, encumbrance, settlement-currency, and wrong-way-risk controls could remain untested in real inventory scenarios

Affected files:

- `Makefile`
- `README.md`
- `app/policy-engine/*`
- `examples/inventory/*`
- `reports/schemas/policy-evaluation-report.schema.json`
- `reports/generated/*`
- `docs/specs/POLICY_EVALUATION_REPORT_SPEC.md`
- `docs/testing/POLICY_ENGINE_TEST_PLAN.md`
- `docs/adrs/0008-policy-evaluation-engine.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-06-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/testing/TEST_STRATEGY.md`
- `test/policy-engine/*`

Acceptance criteria:

- the policy engine loads a real `CPL v0.1` policy file and candidate inventory set from disk
- eligibility, haircut, lendable value, concentration, encumbrance, settlement-currency, and wrong-way-risk outcomes are derived from the published schema fields rather than ad hoc flags
- failure attribution is explicit, deterministic, and machine-readable at both asset and portfolio levels
- reproducible commands exist for policy evaluation and policy-engine tests
- at least one real policy-evaluation report artifact is generated and linked into mission-control evidence

Planned commands:

```sh
make bootstrap
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 6 - Post-Change

Outcome:
Implemented the repository's first real `CPL v0.1` policy evaluation engine, added the first machine-readable `PolicyEvaluationReport` contract, generated a real report artifact from the command surface, and verified the new engine alongside the existing Daml workflow baseline.

Completed artifacts:

- deterministic policy-engine source under `app/policy-engine/` for policy loading, inventory loading, eligibility checks, haircut and lendable-value calculation, concentration evaluation, wrong-way-risk handling, and report generation
- normalized example inventory input under `examples/inventory/central-bank-eligible-inventory.json`
- canonical report schema under `reports/schemas/policy-evaluation-report.schema.json`
- real generated report artifact under `reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json`
- report specification in `docs/specs/POLICY_EVALUATION_REPORT_SPEC.md`
- new design decision in `docs/adrs/0008-policy-evaluation-engine.md`
- policy-engine test plan in `docs/testing/POLICY_ENGINE_TEST_PLAN.md`
- deterministic policy-engine scenario tests under `test/policy-engine/`
- updated command surface in `Makefile`, `scripts/dev-status.sh`, and `scripts/verify.sh`
- mission-control, invariant, evidence, risk, security, setup, and repository-surface docs updated to reflect the new engine package
- prompt execution record in `docs/evidence/prompt-06-execution-report.md`

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json
make test-policy-engine
make daml-test
make demo-run
make docs-lint
make verify
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported `Current Phase: Milestone 2 / Phase 2 - Initial Policy Engine, Report Contracts, And Daml Workflow Skeletons`
- `make validate-cpl` passed
- `make policy-eval ...` passed, generated the schema-valid example policy-evaluation report artifact, and validated it against `reports/schemas/policy-evaluation-report.schema.json`
- `make test-policy-engine` passed and executed the eight deterministic scenario tests for eligibility, issuer rejection, haircut application, currency mismatch haircuts, concentration breaches, wrong-way-risk exclusions, encumbrance failures, and repeatability
- `make daml-test` passed and preserved the existing workflow lifecycle-script baseline
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make docs-lint` passed after the policy-engine, tracker, ADR, spec, test-plan, and evidence updates
- `make verify` passed and exercised docs linting, CPL validation, policy-engine tests, Daml build, Daml lifecycle tests, and the workflow smoke run
- `git status --short --branch` showed only the expected task-related changes before commit

Next step:
Define pinned reference-data contracts for valuation, FX, issuer, and counterparty facts, then add role-scoped `ExecutionReport` disclosure profiles and the first asset-adapter interface on top of the new policy-engine and Daml package surfaces.

## 2026-03-28 - Rename To Canton Collateral Control Plane - Pre-Change

Intent:
Rename the repository's user-facing identity from "Canton Collateral Policy & Optimization Engine" / "C-COPE" to "Canton Collateral Control Plane" without changing the mission, implementation sequencing, or subsystem boundaries, and make the control-plane versus data-plane architecture explicit across the primary documentation surfaces.

Risks addressed:

- the current project name over-emphasizes two subsystems and obscures that policy, optimization, workflow orchestration, conformance, and reporting already operate as one control plane
- the old acronym can create market-structure ambiguity and distract from the intended architecture
- rename churn could accidentally flatten subsystem boundaries, misstate historical evidence, or break future prompts and reproducible commands
- build metadata and generated-artifact naming could drift from the new identity unless updated consistently and verified

Affected files:

- `README.md`
- `AGENTS.md`
- `Makefile`
- `daml.yaml`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/WORKLOG.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/architecture/OVERVIEW.md`
- `docs/architecture/COMPONENTS.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/DEPLOYMENT_MODEL.md`
- `docs/architecture/PRIVACY_MODEL.md`
- `docs/domain/GLOSSARY.md`
- `docs/domain/COLLATERAL_DOMAIN_MODEL.md`
- `docs/integration/INTEGRATION_SURFACES.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/adrs/README.md`
- `docs/adrs/0002-system-boundaries.md`
- `docs/adrs/0010-rename-to-canton-collateral-control-plane.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-04-execution-report.md`
- `docs/evidence/prompt-05-execution-report.md`
- `docs/evidence/rename-to-collateral-control-plane-execution-report.md`
- `docs/risks/RISK_REGISTER.md`

Acceptance criteria:

- the repository presents itself as "Canton Collateral Control Plane" on primary identity surfaces
- the former name is retained only as a deprecated historical alias where continuity helps
- README, architecture docs, glossary, and ADRs distinguish control-plane responsibilities from the data plane
- subsystem names remain intact for `CPL`, policy evaluation, optimization, workflow, conformance, and reporting
- in-repo metadata and DAR naming are updated where safe without unnecessary directory or module churn
- mission-control, invariants, evidence, and ADR records reflect the rename
- relevant checks run successfully and no existing code or tests are broken

Planned commands:

```sh
make bootstrap
make docs-lint
make validate-cpl
make test-policy-engine
make daml-build
make daml-test
make demo-run
make verify
git status --short --branch
```

## 2026-03-28 - Rename To Canton Collateral Control Plane - Post-Change

Outcome:
Renamed the repository's primary user-facing identity to "Canton Collateral Control Plane", clarified the control-plane versus data-plane architecture across the core documentation surfaces, preserved the prior name only as a deprecated historical alias, and updated safe in-repo metadata so the Daml build artifact now carries the new control-plane name.

Completed artifacts:

- renamed primary identity surfaces in `README.md`, `AGENTS.md`, `docs/mission-control/`, and the glossary
- added explicit control-plane versus data-plane architecture guidance in `README.md`, `docs/architecture/OVERVIEW.md`, `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`, and `docs/domain/GLOSSARY.md`
- updated build metadata in `daml.yaml` so the DAR now builds as `canton-collateral-control-plane-0.1.0.dar`
- recorded the rename decision in `docs/adrs/0010-rename-to-canton-collateral-control-plane.md` and linked it through the decision log, invariant registry, risk register, and evidence manifest
- updated continuity and evidence records in `docs/evidence/`, including this rename execution report
- preserved subsystem names and existing code layout for `CPL`, policy evaluation, optimization, workflow, conformance, and reporting surfaces

Commands run:

```sh
make bootstrap
make status
make validate-cpl
make test-policy-engine
make daml-build
make daml-test
make demo-run
make docs-lint
make verify
python3 -m compileall app/policy-engine test/policy-engine
git status --short --branch
```

Results:

- `make bootstrap` passed
- `make status` passed and reported the current Milestone 2 / Phase 2 state plus the renamed Daml package metadata
- `make validate-cpl` passed
- `make test-policy-engine` passed and preserved the eight deterministic Python scenario tests plus report generation
- `make daml-build` passed and produced `.daml/dist/canton-collateral-control-plane-0.1.0.dar`
- `make daml-test` passed and preserved the Daml lifecycle-script baseline
- `make demo-run` passed and executed `Bootstrap:workflowSmokeTest`
- `make docs-lint` passed after the rename ADR, execution report, tracker, and architecture updates were added to the required documentation set
- `make verify` passed and re-executed the repository lint, validation, policy-engine, Daml build, Daml lifecycle, and workflow smoke checks in one command
- `python3 -m compileall app/policy-engine test/policy-engine` passed as an extra Python syntax sanity check
- no dedicated formatter or static type-check target is currently configured in the repository; the available executable lint and verification loop passed cleanly
- `git status --short --branch` showed only the expected rename-related modifications before commit

Next step:
Continue with the Prompt 6 follow-on work by defining pinned reference-data contracts, role-scoped `ExecutionReport` disclosure profiles, and the first asset-adapter interface on top of the current policy-engine and Daml package surfaces.

## 2026-03-28 - Prompt 7 - Pre-Change

Intent:
Implement the repository's first deterministic collateral optimization engine for best-to-post allocation and substitution recommendation, with explicit separation from workflow execution and machine-readable optimization reporting.

Risks addressed:

- the repository currently stops at policy evaluation, so posting decisions remain undocumented, untested, and operationally ambiguous
- optimization logic could accidentally collapse policy evaluation, report generation, and workflow execution into one layer unless the boundary is made explicit in code and ADRs
- non-deterministic tie-breaking or unstable explanation ordering would undermine operational review, legal review, and reproducible testing
- concentration-aware allocation and substitution logic could drift from institutional collateral practice if objective semantics are not documented alongside the implementation
- report and evidence artifacts could remain incomplete unless the optimizer produces a schema-valid machine-readable output and the mission-control surfaces are updated in the same change

Affected files:

- `Makefile`
- `README.md`
- `app/README.md`
- `app/optimizer/`
- `examples/README.md`
- `examples/inventory/central-bank-eligible-inventory.json`
- `examples/obligations/*.json`
- `reports/README.md`
- `reports/generated/`
- `reports/schemas/optimization-report.schema.json`
- `docs/specs/OPTIMIZATION_REPORT_SPEC.md`
- `docs/economic/OPTIMIZATION_OBJECTIVES.md`
- `docs/testing/OPTIMIZER_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/adrs/0009-optimization-objective-and-determinism.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-07-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`
- `test/optimizer/`

Acceptance criteria:

- a real deterministic optimizer exists under `app/optimizer/` and remains separate from workflow execution concerns
- the optimizer supports best-to-post selection under a policy and obligation amount
- the optimizer recommends compliant substitutions when an existing posted set can be improved
- concentration-aware allocation changes outcomes when policy concentration limits bind
- machine-readable optimization reports include deterministic explanation traces and validate against the published schema
- reproducible commands exist for `make optimize` and `make test-optimizer`
- optimizer documentation, ADRs, invariants, evidence, and mission-control records are updated consistently
- at least one generated optimization report artifact is produced from executable code, relevant checks pass, the changes are committed, and the worktree is left clean

Planned commands:

```sh
make optimize POLICY=... INVENTORY=... OBLIGATION=...
make test-optimizer
make test-policy-engine
make validate-cpl
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 7 - Post-Change

Outcome:
Implemented the repository's first deterministic collateral optimizer under `app/optimizer/`, added a machine-readable `OptimizationReport` contract plus generated artifact, documented the objective and determinism rules, and preserved the separation between optimization advice and authoritative Canton workflow execution.

Completed artifacts:

- optimizer implementation and CLI under `app/optimizer/`
- reusable non-concentration screening and report-finalization split inside `app/policy-engine/evaluator.py`
- example obligation inputs under `examples/obligations/`
- optimization report schema and generated artifact under `reports/schemas/` and `reports/generated/`
- optimization report spec, economic rationale, optimizer test plan, and ADR under `docs/specs/`, `docs/economic/`, `docs/testing/`, and `docs/adrs/`
- mission-control, invariant, evidence, risk, threat, runbook, setup, and command-surface updates for the new optimizer milestone
- prompt execution evidence in `docs/evidence/prompt-07-execution-report.md`
- deterministic optimizer scenario suite under `test/optimizer/`

Commands run:

```sh
make status
make validate-cpl
make optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json
make test-policy-engine
make test-optimizer
make docs-lint
make verify
git status --short --branch
```

Results:

- `make status` passed and reported `Current Phase: Milestone 3 / Phase 3 - Initial Optimization And Substitution Engine`
- `make validate-cpl` passed
- `make optimize ...` passed and regenerated `reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json`
- `make test-policy-engine` passed and preserved the existing deterministic policy-engine baseline
- `make test-optimizer` passed and executed the five new deterministic optimizer scenario tests plus report validation
- `make docs-lint` passed after the optimizer schema, ADR, spec, economic note, test plan, tracker, and evidence updates were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, and the workflow smoke run
- the Daml helper emitted an informational notice that SDK `3.4.11` exists upstream; the repository remains intentionally pinned to `2.10.4`
- `git status --short --branch` showed only the expected task-related changes before commit

Next step:
Define reference-data contracts and workflow-coupled reservation or consent interfaces so future optimizer recommendations can be bound to Canton execution without losing the current deterministic advisory boundary.

## 2026-03-28 - Prompt 8 - Pre-Change

Intent:
Create the first credible Quickstart-based LocalNet demo foundation for the Canton Collateral Control Plane, with a pinned upstream bootstrap path, an overlay surface that avoids unnecessary forks, and explicit staged planning for later token-standard-style asset integration.

Risks addressed:

- the repository currently stops at IDE-ledger Daml smoke tests, leaving the Quickstart-backed LocalNet path unpinned and operationally ambiguous
- an eager LocalNet integration could fork upstream CN Quickstart too early or hide environment authority inside repo-specific runtime shortcuts
- token-standard-style asset integration assumptions could remain implicit, making later venue, custodian, issuer, and financing-app integration harder to defend
- a partial runtime layer could be mistaken for a real confidential collateral demo unless mocked and deferred surfaces are stated explicitly

Affected files:

- `Makefile`
- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `infra/README.md`
- `infra/quickstart/README.md`
- `infra/quickstart/bootstrap-localnet.sh`
- `infra/quickstart/overlay/`
- `scripts/run-localnet-smoke.sh`
- `scripts/dev-status.sh`
- `docs/setup/LOCAL_DEV_SETUP.md`
- `docs/runbooks/README.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/integration/LOCALNET_DEMO_PLAN.md`
- `docs/integration/ASSET_ADAPTER_PLAN.md`
- `docs/integration/INTEGRATION_SURFACES.md`
- `docs/adrs/README.md`
- `docs/adrs/0015-quickstart-demo-foundation.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-08-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`

Acceptance criteria:

- the repo exposes a credible, documented Quickstart-based LocalNet demo foundation without pretending the full confidential collateral demo is finished
- the LocalNet bootstrap and smoke commands are reproducible, pinned, and stay as close as practical to upstream CN Quickstart workflows
- assumptions, mocks, and deferred integration surfaces are explicit for asset issuers, custodians, venues, financing apps, and margining applications
- mission-control, invariant, evidence, and ADR traces are updated consistently
- the implemented commands are run where feasible, the changes are committed, and the worktree is left clean

Planned commands:

```sh
make localnet-bootstrap
make localnet-smoke
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 8 - Post-Change

Outcome:
Established the repository's first credible Quickstart-based LocalNet demo foundation by pinning an upstream CN Quickstart checkout, adding an overlay-first bootstrap and smoke path, documenting the staged route to live asset integration, and preserving a clear stop line before any fake confidential-collateral demo claims.

Completed artifacts:

- pinned Quickstart bootstrap, overlay metadata, and profile templates under `infra/quickstart/`
- reproducible Quickstart smoke script under `scripts/run-localnet-smoke.sh`
- new LocalNet and asset-adapter plans under `docs/integration/`
- new Quickstart foundation ADR under `docs/adrs/0015-quickstart-demo-foundation.md`
- README, setup, runbook, dependency, test-strategy, invariant, evidence, risk, security, roadmap, tracker, and decision-log updates for the new LocalNet layer
- prompt execution evidence in `docs/evidence/prompt-08-execution-report.md`

Commands run:

```sh
chmod +x infra/quickstart/bootstrap-localnet.sh scripts/run-localnet-smoke.sh
sh -n infra/quickstart/bootstrap-localnet.sh scripts/run-localnet-smoke.sh scripts/dev-status.sh scripts/verify.sh
make status
make localnet-bootstrap
make localnet-smoke
make docs-lint
make verify
git status --short --branch
```

Results:

- `sh -n ...` passed for the new and updated shell scripts
- `make status` passed and reported the Quickstart pin plus the staged overlay values once the bootstrap finished
- `make localnet-bootstrap` passed and staged the pinned CN Quickstart checkout at commit `fe56d460af650b71b8e20098b3e76693397a8bf9`
- `make localnet-smoke` passed after switching to the upstream `compose-config` target and validated the composed Quickstart stack without claiming the LocalNet was running
- `make docs-lint` passed after the Quickstart foundation docs, ADR, integration plans, and prompt evidence were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, workflow smoke execution, and the new Quickstart LocalNet smoke check
- the Daml helper again emitted an informational notice that SDK `3.4.11` exists upstream; the repository remains intentionally pinned to `2.10.4`
- `git status --short --branch` before commit showed only the expected Prompt 8 changes

Next step:
Resolve the Daml runtime bridge needed to deploy the Control Plane DAR into the pinned Quickstart LocalNet, then add the first real asset-adapter and seeded confidential collateral scenario on top of that bridge.

## 2026-03-28 - Prompt 9 - Pre-Change

Intent:
Implement the first end-to-end confidential margin call prototype for the Canton Collateral Control Plane, with a real demo command that evaluates candidate collateral, records a valid posting path through the existing Daml workflow boundary, emits a machine-readable execution report, and captures operator-facing evidence plus negative-path coverage.

Risks addressed:

- the repository currently has separate policy-evaluation, optimization, and Daml workflow building blocks but no single reproducible command that ties them into one auditable margin-call path
- a demo could fabricate workflow success or summarize outcomes without grounding them in real policy and Daml execution
- negative-path behavior for ineligible collateral, insufficient lendable value, and stale obligations or policy windows could remain undocumented or untested
- execution reporting could stay underspecified, leaving artifact consumers to guess how policy, optimization, and workflow evidence connect

Affected files:

- `Makefile`
- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `app/README.md`
- `app/orchestration/`
- `daml/Bootstrap.daml`
- `daml/CantonCollateral/`
- `examples/README.md`
- `examples/demo-scenarios/margin-call/`
- `reports/README.md`
- `reports/schemas/execution-report.schema.json`
- `reports/generated/`
- `test/README.md`
- `test/orchestration/`
- `docs/specs/EXECUTION_REPORT_SPEC.md`
- `docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md`
- `docs/testing/DAML_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/adrs/README.md`
- `docs/adrs/0011-margin-call-demo-shape.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-09-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`

Acceptance criteria:

- a real `make demo-margin-call` command exists and runs from a clean checkout
- the demo generates real JSON and Markdown execution artifacts from actual policy, optimization, and Daml workflow execution
- the positive path shows margin-call issuance, eligible collateral selection or assignment, policy evaluation, and a recorded posting path
- negative-path coverage exists for ineligible collateral, insufficient lendable value, and an expired obligation or policy window
- mission-control, ADR, invariant, evidence, and runbook surfaces reflect the new prototype
- relevant commands are run, the changes are committed, and the worktree is left clean

Planned commands:

```sh
make demo-margin-call
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 9 - Post-Change

Outcome:
Implemented the repository's first end-to-end margin-call prototype by adding a manifest-driven orchestration layer, a parameterized Daml demo workflow path, a machine-readable `ExecutionReport` contract, real positive and negative demo scenarios, and operator-facing summary and timeline artifacts generated from actual execution.

Completed artifacts:

- new orchestration surface under `app/orchestration/` with a real `make demo-margin-call` command
- new parameterized Daml demo script under `daml/CantonCollateral/Demo.daml`
- new margin-call scenario bundle under `examples/demo-scenarios/margin-call/`
- new execution-report schema and specification under `reports/schemas/execution-report.schema.json` and `docs/specs/EXECUTION_REPORT_SPEC.md`
- new operator runbook under `docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md`
- new ADR under `docs/adrs/0011-margin-call-demo-shape.md` plus renumbered Quickstart ADR under `docs/adrs/0015-quickstart-demo-foundation.md`
- regenerated real demo artifacts under `reports/generated/` including the execution report, Markdown summary, timeline, positive workflow result, and negative-path artifacts
- mission-control, invariant, risk, threat, README, setup, testing, evidence, and command-surface updates aligned to the new prototype
- prompt execution evidence under `docs/evidence/prompt-09-execution-report.md`

Commands run:

```sh
make status
make demo-margin-call
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git status --short --branch
```

## 2026-03-28 - Prompt 10 - Post-Change

Outcome:
Implemented the repository's first end-to-end substitution prototype by extending the optimizer for scoped substitution requests, adding a parameterized Daml substitution demo workflow, publishing a machine-readable `SubstitutionReport` contract, generating real positive and negative substitution artifacts, and aligning the mission-control, ADR, runbook, and evidence surfaces to the new control model.

Completed artifacts:

- scoped substitution-request support in `app/optimizer/` plus deterministic optimizer tests for forced incumbent replacement and clean no-solution handling
- new substitution orchestration surface under `app/orchestration/` with a real `make demo-substitution` command
- expanded Daml substitution workflow, demo script, and lifecycle tests under `daml/CantonCollateral/`
- new substitution scenario bundle under `examples/demo-scenarios/substitution/`
- new substitution-report schema and specification under `reports/schemas/substitution-report.schema.json` and `docs/specs/SUBSTITUTION_REPORT_SPEC.md`
- new operator runbook under `docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md`
- new ADR under `docs/adrs/0012-substitution-atomicity.md` plus renumbered Quickstart ADR under `docs/adrs/0015-quickstart-demo-foundation.md`
- regenerated real demo artifacts under `reports/generated/` including the substitution report, Markdown summary, timeline, positive workflow result, and negative-path policy, optimization, and workflow artifacts
- mission-control, invariant, risk, threat, README, setup, testing, evidence, and command-surface updates aligned to the new prototype
- prompt execution evidence under `docs/evidence/prompt-10-execution-report.md`

Commands run:

```sh
make status
make demo-substitution
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git diff --check
git status --short --branch
```

Results:

- `make status` passed and reported `Current Phase: Milestone 4 / Phase 4 - Initial Margin Call And Substitution Demo Reporting`
- `make demo-substitution` passed and generated `reports/generated/substitution-demo-report.json` plus the supporting JSON and Markdown artifacts for one positive and four negative scenarios
- `make test-policy-engine` passed and regenerated the committed baseline `PolicyEvaluationReport` artifact
- `make test-optimizer` passed and regenerated the committed baseline `OptimizationReport` artifact with the substitution-request contract extensions intact
- `make daml-test` passed and preserved the Daml lifecycle-script baseline for margin call, posting, substitution, and return flows
- `make docs-lint` passed after the new substitution docs, ADR, runbook, tracker, and evidence surfaces were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, both end-to-end demos, and the Quickstart compose-preflight smoke path
- `git diff --check` passed with no whitespace or patch-format issues
- `git status --short --branch` before commit showed only the expected Prompt 10 changes, including the new substitution artifacts and the ADR renumber from Quickstart `0012` to `0013`

Next step:
Bridge the repo Daml package into the pinned Quickstart runtime line, then define role-scoped execution and substitution report profiles plus workflow-coupled reservation and consent interfaces on top of the new end-to-end demo paths.

Results:

- `make status` passed and reported `Current Phase: Milestone 4 / Phase 4 - Initial Margin Call Demo And Execution Reporting`
- `make demo-margin-call` passed and generated `reports/generated/margin-call-demo-execution-report.json` plus the supporting Markdown and workflow artifacts
- `make test-policy-engine` passed and regenerated the committed policy-evaluation artifact
- `make test-optimizer` passed and regenerated the committed optimization artifact
- `make daml-test` passed and preserved the lifecycle-script baseline
- `make docs-lint` passed after the new orchestration, schema, runbook, ADR, and evidence surfaces were added to the required documentation set
- `make verify` passed and re-ran docs linting, CPL validation, policy-engine tests, optimizer tests, Daml build, Daml lifecycle tests, the new end-to-end demo command, and the Quickstart compose-preflight smoke check
- the Daml helper again emitted informational notices that SDK `3.4.11` exists upstream; the repository remains intentionally pinned to `2.10.4`
- `git status --short --branch` before commit showed only the expected Prompt 9 changes, including the intentional ADR renumbering from Quickstart `0011` to `0012`

Next step:
Bridge the repo Daml package into the pinned Quickstart runtime line, then add role-scoped execution-report disclosure profiles and workflow-coupled reservation or consent controls on top of the new end-to-end demo path.

## 2026-03-28 - Prompt 10 - Pre-Change

Intent:
Implement the first confidential collateral substitution prototype for the Canton Collateral Control Plane, with deterministic positive and negative substitution scenarios, workflow-enforced approvals and atomicity, real optimizer-orchestrator integration, and machine-readable substitution reporting.

Risks addressed:

- the repository currently proves a margin-call posting path but does not yet expose a real end-to-end substitution demo that starts from encumbered collateral and shows replacement under policy
- substitution control semantics could remain implicit, especially around approval enforcement, unauthorized release prevention, and atomic all-or-nothing replacement behavior
- the optimizer currently recommends substitutions off-ledger, but the orchestration and Daml workflow layers do not yet prove that a recommended replacement set can be executed atomically or fail deterministically
- reporting consumers currently lack a substitution-specific machine-readable contract that ties policy, optimization, approval, workflow, and failure evidence together

Affected files:

- `Makefile`
- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `app/README.md`
- `app/optimizer/`
- `app/orchestration/`
- `daml/Bootstrap.daml`
- `daml/CantonCollateral/`
- `examples/README.md`
- `examples/demo-scenarios/substitution/`
- `reports/README.md`
- `reports/generated/`
- `reports/schemas/`
- `test/README.md`
- `test/optimizer/`
- `docs/specs/SUBSTITUTION_REPORT_SPEC.md`
- `docs/specs/EXECUTION_REPORT_SPEC.md`
- `docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md`
- `docs/testing/DAML_TEST_PLAN.md`
- `docs/testing/OPTIMIZER_TEST_PLAN.md`
- `docs/testing/TEST_STRATEGY.md`
- `docs/adrs/README.md`
- `docs/adrs/0012-substitution-atomicity.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/WORKLOG.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-10-execution-report.md`
- `docs/risks/RISK_REGISTER.md`
- `docs/security/THREAT_MODEL.md`

Acceptance criteria:

- a real `make demo-substitution` command exists and runs from a clean checkout
- the demo starts from existing encumbered collateral, initiates a substitution request, enforces the required approvals, and executes the replacement atomically or fails atomically
- the optimizer-orchestrator path produces a valid replacement set under the declared policy and emits explicit deterministic failures for the negative scenarios
- real JSON and Markdown substitution artifacts are generated from actual policy, optimization, and Daml workflow execution
- mission-control, ADR, invariant, evidence, runbook, and report-spec surfaces reflect the substitution prototype
- relevant commands are run, the changes are committed, and the worktree is left clean

Planned commands:

```sh
make demo-substitution
make test-policy-engine
make test-optimizer
make daml-test
make docs-lint
make verify
git status --short --branch
```
