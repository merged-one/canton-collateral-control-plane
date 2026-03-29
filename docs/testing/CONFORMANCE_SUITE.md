# Conformance Suite

## Purpose

The conformance suite turns the three confidential workflow demos into one explicit invariant-verification surface for the Canton Collateral Control Plane.

It does not replace the underlying demo commands. It executes them, aggregates their evidence, and emits one machine-readable pass or fail report that a reviewer can inspect without guessing which scenario proved which property.

## Primary Command

```sh
make test-conformance
```

This command:

1. rebuilds the Daml package through `make daml-build`
2. re-runs the confidential margin-call, collateral substitution, and margin-return demos
3. generates supporting policy-evaluation evidence for determinism and haircut checks
4. emits `reports/generated/conformance-suite-report.json`
5. emits `reports/generated/conformance-suite-summary.md`
6. runs `test/conformance/test_conformance.py` against the generated suite report
7. runs `test/conformance/test_conformance_checks.py` so key helper checks can fail independently of the aggregate scenario rerun

## Required Coverage

The current suite covers the minimum prototype control set required by the proposal:

| Check ID | Invariants | What It Proves | Primary Evidence |
| --- | --- | --- | --- |
| `AUTHORIZATION_AND_ROLE_CONTROL` | `AUTH-001`, `CTRL-001`, `WF-001` | unauthorized substitution or return release attempts remain blocked until the correct approvals and roles are present | negative substitution and return workflow results |
| `ELIGIBILITY_DETERMINISM` | `ELIG-001`, `PDR-001` | repeating the same policy evaluation with identical inputs produces the same machine-readable result | `reports/generated/conformance-eligibility-determinism-policy-evaluation-report.json` |
| `HAIRCUT_CORRECTNESS` | `HAIR-001` | valuation basis, haircut basis points, and lendable value arithmetic remain explicit and reproducible | `reports/generated/conformance-haircut-policy-evaluation-report.json` |
| `NO_DOUBLE_ENCUMBRANCE` | `ENC-001`, `CTRL-001` | posting, substitution, and return flows preserve disjoint encumbrance sets and block overlapping state changes | positive and blocked workflow result artifacts |
| `ATOMIC_SUBSTITUTION_WHEN_REQUIRED` | `ATOM-001`, `CTRL-001` | full replacement either commits atomically or leaves the incumbent set untouched | positive substitution plus blocked partial and unauthorized substitution results |
| `REPLAY_SAFETY` | `REPL-001` | a replayed return instruction is rejected without duplicating release behavior | replay return workflow result |
| `REPORT_FIDELITY` | `REPT-001`, `PDR-001` | machine-readable reports point to real generated artifacts and keep scenario, workflow, and artifact counts aligned | top-level demo reports and referenced scenario artifacts |
| `AUDIT_TRAIL_COMPLETENESS` | `AUD-001` | positive workflow paths expose steps, execution-report events, and timelines that can be audited without hidden reconstruction | top-level demo reports, workflow results, and timelines |

## Generated Outputs

After a successful run, the conformance suite refreshes at least these artifacts:

- `reports/generated/conformance-suite-report.json`
- `reports/generated/conformance-suite-summary.md`
- `reports/generated/conformance-eligibility-determinism-policy-evaluation-report.json`
- `reports/generated/conformance-haircut-policy-evaluation-report.json`
- `reports/generated/margin-call-demo-execution-report.json`
- `reports/generated/substitution-demo-report.json`
- `reports/generated/return-demo-report.json`

## Operator Checks

Check the suite outcome:

```sh
jq '{suiteId, overallStatus, coverage, checks: [.checks[] | {checkId, status, invariantIds}]}' reports/generated/conformance-suite-report.json
```

Check the Markdown summary:

```sh
sed -n '1,260p' reports/generated/conformance-suite-summary.md
```

Check the supporting haircut vector:

```sh
jq '{overallDecision, assetResults: [.assetResults[] | {lotId, valuationBasisValue, baseHaircutBps, totalHaircutBps, lendableValue}]}' reports/generated/conformance-haircut-policy-evaluation-report.json
```

## Failure Handling

If `make test-conformance` fails:

1. inspect `reports/generated/conformance-suite-summary.md` if it was written
2. identify the failing `checkId` and its referenced artifacts
3. re-run the affected lower-level command if needed:

```sh
make demo-margin-call
make demo-substitution
make demo-return
```

4. if the failure is in determinism or haircut evidence, compare the supporting policy-evaluation artifacts directly:

```sh
sed -n '1,220p' reports/generated/conformance-eligibility-determinism-policy-evaluation-report.json
sed -n '1,220p' reports/generated/conformance-haircut-policy-evaluation-report.json
```

5. if the failure points at workflow evidence, confirm the package still builds and the Daml lifecycle tests still pass:

```sh
make daml-build
make daml-test
```

## Notes

- `make test-conformance` is the prototype's aggregated invariant gate, not a replacement for `make test-policy-engine`, `make test-optimizer`, or `make daml-test`
- the conformance test package now includes both generated-report assertions and isolated helper-check unit tests so report-shape and rule regressions do not have to surface through the same failure mode
- the conformance suite still uses the Daml IDE ledger for workflow execution because the Quickstart runtime bridge remains a separate follow-on task
- the current suite is intentionally evidence-first: it checks the machine-readable artifacts that proposal reviewers will actually inspect
