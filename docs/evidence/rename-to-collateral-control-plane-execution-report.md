# Rename To Canton Collateral Control Plane Execution Report

## Summary Of Rename Changes

The repository's active user-facing identity is now "Canton Collateral Control Plane". The rename is semantic, not directional: the existing `CPL`, policy engine, optimization engine, workflow library, conformance suite, and reporting or evidence layer remain intact and are now described explicitly as subsystems of one shared control plane.

The documentation now distinguishes the control plane from the data plane. Control-plane responsibilities cover policy authoring, eligibility and haircut evaluation, concentration and release control, optimization, substitution orchestration, conformance, and reporting. Data-plane responsibilities cover token-standard-style assets, Daml Finance-style assets, committed ledger state and contract instances, settlement and DvP rails, and the Quickstart or LocalNet execution environment.

The former name "Canton Collateral Policy & Optimization Engine" is retained only as a deprecated historical alias where continuity helps. `C-COPE` is deprecated and should not be used going forward. No new acronym such as `CCCP` or `CCP` was introduced.

## Files Changed

- `AGENTS.md`
- `Makefile`
- `README.md`
- `daml.yaml`
- `docs/adrs/0002-system-boundaries.md`
- `docs/adrs/0009-rename-to-canton-collateral-control-plane.md`
- `docs/adrs/README.md`
- `docs/architecture/COMPONENTS.md`
- `docs/architecture/DATA_FLOW.md`
- `docs/architecture/DEPLOYMENT_MODEL.md`
- `docs/architecture/OVERVIEW.md`
- `docs/architecture/PRIVACY_MODEL.md`
- `docs/domain/COLLATERAL_DOMAIN_MODEL.md`
- `docs/domain/GLOSSARY.md`
- `docs/evidence/EVIDENCE_MANIFEST.md`
- `docs/evidence/prompt-04-execution-report.md`
- `docs/evidence/prompt-05-execution-report.md`
- `docs/evidence/rename-to-collateral-control-plane-execution-report.md`
- `docs/integration/INTEGRATION_SURFACES.md`
- `docs/integration/QUICKSTART_INTEGRATION_PLAN.md`
- `docs/integration/TOKEN_STANDARD_ALIGNMENT.md`
- `docs/invariants/INVARIANT_REGISTRY.md`
- `docs/mission-control/DECISION_LOG.md`
- `docs/mission-control/MASTER_TRACKER.md`
- `docs/mission-control/ROADMAP.md`
- `docs/mission-control/WORKLOG.md`
- `docs/risks/RISK_REGISTER.md`

## Checks Run

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

## Checks Passed

- `make bootstrap`
- `make status`
- `make validate-cpl`
- `make test-policy-engine`
- `make daml-build`
- `make daml-test`
- `make demo-run`
- `make docs-lint`
- `make verify`
- `python3 -m compileall app/policy-engine test/policy-engine`

## Checks Failed

- none

## Compatibility Notes

- The former name "Canton Collateral Policy & Optimization Engine" is preserved only as a deprecated historical alias in continuity notes.
- `CPL`, the policy engine, optimization engine, workflow library, conformance suite, and reporting or evidence layer were not renamed or flattened.
- Directory names and module names were preserved to avoid unnecessary churn for future prompts.
- Safe in-repo metadata was updated: the Daml package now builds as `.daml/dist/canton-collateral-control-plane-0.1.0.dar`.
- No dedicated formatter or static type-check target is currently configured in the repository; the existing lint, schema-validation, unit-test, Daml-test, demo, and full verify loop remain the executable control surface.

## Residual Risks

- Historical references outside this repository may still use the deprecated former name until downstream docs are updated.
- The repository still lacks a dedicated formatter and static type-check toolchain, so documentation discipline and executable verification remain the primary safeguards for this rename.
- Quickstart-backed data-plane integration remains future work, so the control-plane versus data-plane split is documented and verified structurally rather than against a full external settlement path.

## Exact Next Recommended Step

Continue with Prompt 6
