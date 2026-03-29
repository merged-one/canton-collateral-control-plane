import tempfile
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "app/orchestration"))

from conformance_suite import (  # noqa: E402
    _check_atomic_substitution_when_required,
    _check_audit_trail_completeness,
    _check_authorization_and_role_control,
    _check_no_double_encumbrance,
    _check_report_fidelity,
    _check_replay_safety,
)


def _control_check(check_id: str) -> dict:
    return {"checkId": check_id}


def _execution_report(summary: str = "Committed collateral workflow.") -> dict:
    return {
        "reportId": "exec-001",
        "workflowType": "COLLATERAL_WORKFLOW",
        "outcome": "COMMITTED",
        "eventIds": ["evt-001"],
        "summary": summary,
    }


def _workflow_step() -> dict:
    return {
        "step": 1,
        "actor": "Operator",
        "phase": "WORKFLOW",
        "state": "Committed",
        "detail": "Recorded a deterministic workflow step.",
    }


def _margin_workflow(**overrides) -> dict:
    workflow = {
        "encumberedLotIds": ["lot-margin-1"],
        "executionReportCount": 1,
        "executionReports": [_execution_report()],
        "steps": [_workflow_step()],
        "controlChecks": [],
    }
    workflow.update(overrides)
    return workflow


def _substitution_workflow(**overrides) -> dict:
    workflow = {
        "substitutionState": "Settled",
        "activeEncumberedLotIds": ["lot-new-1"],
        "releasedLotIds": ["lot-old-1"],
        "atomicityOutcome": "COMMITTED_ATOMICALLY",
        "executionReportCount": 1,
        "executionReports": [_execution_report()],
        "steps": [_workflow_step()],
        "controlChecks": [],
    }
    workflow.update(overrides)
    return workflow


def _return_workflow(**overrides) -> dict:
    workflow = {
        "returnState": "Closed",
        "currentEncumberedLotIds": ["lot-ret-1", "lot-ret-2"],
        "returnedLotIds": ["lot-ret-1"],
        "remainingEncumberedLotIds": ["lot-ret-2"],
        "returnRequestId": "return-req-001",
        "executionReportCount": 1,
        "executionReports": [_execution_report()],
        "steps": [_workflow_step()],
        "controlChecks": [],
    }
    workflow.update(overrides)
    return workflow


def _scenario(
    *,
    scenario_id: str,
    mode: str,
    workflow: dict | None,
    workflow_result_path: str,
    current_posted_lot_ids: list[str] | None = None,
    selected_lot_ids: list[str] | None = None,
    policy_evaluation_report_path: str | None = None,
    optimization_report_path: str | None = None,
    workflow_input_path: str | None = None,
) -> dict:
    return {
        "scenarioId": scenario_id,
        "mode": mode,
        "currentPostedLotIds": [] if current_posted_lot_ids is None else current_posted_lot_ids,
        "selectedLotIds": [] if selected_lot_ids is None else selected_lot_ids,
        "policyEvaluationReportPath": policy_evaluation_report_path,
        "optimizationReportPath": optimization_report_path,
        "workflowInputPath": workflow_input_path,
        "workflowResultPath": workflow_result_path,
        "workflow": workflow,
    }


def _timeline_entry(scenario_id: str, phase: str = "WORKFLOW") -> dict:
    return {
        "scenarioId": scenario_id,
        "phase": phase,
        "status": "COMPLETED",
        "detail": "Timeline entry recorded for the scenario.",
    }


def _demo_report(
    *,
    report_type: str,
    report_artifact_key: str,
    report_path: str,
    summary_path: str,
    timeline_path: str,
    scenarios: list[dict],
    timeline: list[dict],
    invariant_checks: list[dict] | None = None,
) -> dict:
    positive_count = sum(1 for scenario in scenarios if scenario["mode"] == "POSITIVE")
    negative_count = sum(1 for scenario in scenarios if scenario["mode"] == "NEGATIVE")
    return {
        "reportType": report_type,
        "demo": {
            "demoId": f"{report_type.lower()}-demo",
            "command": f"make {report_type.lower()}",
            "scenarioCount": len(scenarios),
            "positiveScenarioCount": positive_count,
            "negativeScenarioCount": negative_count,
        },
        "artifacts": {
            report_artifact_key: report_path,
            "markdownSummaryPath": summary_path,
            "timelinePath": timeline_path,
        },
        "scenarios": scenarios,
        "invariantChecks": (
            [{"checkId": "TEST-ONLY", "status": "PASS"}]
            if invariant_checks is None
            else invariant_checks
        ),
        "timeline": timeline,
    }


class ConformanceCheckUnitTest(unittest.TestCase):
    maxDiff = None

    def test_authorization_and_role_control_passes_for_blocked_release_evidence(self) -> None:
        substitution_report = _demo_report(
            report_type="SubstitutionReport",
            report_artifact_key="substitutionReportPath",
            report_path="reports/generated/substitution-demo-report.json",
            summary_path="reports/generated/substitution-demo-summary.md",
            timeline_path="reports/generated/substitution-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="negative-unauthorized-release",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/negative-unauthorized-release-workflow-result.json",
                    workflow=_substitution_workflow(
                        substitutionState="PendingSettlement",
                        activeEncumberedLotIds=["lot-old-1"],
                        releasedLotIds=[],
                        executionReportCount=0,
                        executionReports=[],
                        controlChecks=[
                            _control_check("APPROVAL_GATE_BLOCKED"),
                            _control_check("UNAUTHORIZED_RELEASE_BLOCKED"),
                        ],
                    ),
                )
            ],
            timeline=[],
        )
        return_report = _demo_report(
            report_type="ReturnReport",
            report_artifact_key="returnReportPath",
            report_path="reports/generated/return-demo-report.json",
            summary_path="reports/generated/return-demo-summary.md",
            timeline_path="reports/generated/return-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="negative-unauthorized-return",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-ret-1"],
                    workflow_result_path="reports/generated/negative-unauthorized-return-workflow-result.json",
                    workflow=_return_workflow(
                        returnState="PendingSettlement",
                        currentEncumberedLotIds=["lot-ret-1"],
                        returnedLotIds=[],
                        remainingEncumberedLotIds=["lot-ret-1"],
                        executionReportCount=0,
                        executionReports=[],
                        controlChecks=[
                            _control_check("APPROVAL_GATE_BLOCKED"),
                            _control_check("UNAUTHORIZED_RETURN_BLOCKED"),
                        ],
                    ),
                )
            ],
            timeline=[],
        )

        result = _check_authorization_and_role_control(
            substitution_report=substitution_report,
            return_report=return_report,
        )

        self.assertEqual(result["status"], "PASS")

    def test_no_double_encumbrance_fails_when_return_reuses_the_same_lot(self) -> None:
        margin_call_report = _demo_report(
            report_type="ExecutionReport",
            report_artifact_key="executionReportPath",
            report_path="reports/generated/margin-call-demo-execution-report.json",
            summary_path="reports/generated/margin-call-demo-summary.md",
            timeline_path="reports/generated/margin-call-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="positive-margin-call",
                    mode="POSITIVE",
                    selected_lot_ids=["lot-margin-1"],
                    workflow_result_path="reports/generated/positive-margin-call-workflow-result.json",
                    workflow=_margin_workflow(encumberedLotIds=["lot-margin-1"]),
                )
            ],
            timeline=[_timeline_entry("positive-margin-call")],
        )
        substitution_report = _demo_report(
            report_type="SubstitutionReport",
            report_artifact_key="substitutionReportPath",
            report_path="reports/generated/substitution-demo-report.json",
            summary_path="reports/generated/substitution-demo-summary.md",
            timeline_path="reports/generated/substitution-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="positive-substitution",
                    mode="POSITIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/positive-substitution-workflow-result.json",
                    workflow=_substitution_workflow(),
                ),
                _scenario(
                    scenario_id="negative-unauthorized-release",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/negative-unauthorized-release-workflow-result.json",
                    workflow=_substitution_workflow(
                        substitutionState="PendingSettlement",
                        activeEncumberedLotIds=["lot-old-1"],
                        releasedLotIds=[],
                        executionReportCount=0,
                        executionReports=[],
                    ),
                ),
            ],
            timeline=[_timeline_entry("positive-substitution")],
        )
        return_report = _demo_report(
            report_type="ReturnReport",
            report_artifact_key="returnReportPath",
            report_path="reports/generated/return-demo-report.json",
            summary_path="reports/generated/return-demo-summary.md",
            timeline_path="reports/generated/return-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="positive-return",
                    mode="POSITIVE",
                    current_posted_lot_ids=["lot-ret-1", "lot-ret-2"],
                    workflow_result_path="reports/generated/positive-return-workflow-result.json",
                    workflow=_return_workflow(
                        currentEncumberedLotIds=["lot-ret-1", "lot-ret-2"],
                        returnedLotIds=["lot-ret-1"],
                        remainingEncumberedLotIds=["lot-ret-1"],
                    ),
                ),
                _scenario(
                    scenario_id="negative-unauthorized-return",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-ret-1", "lot-ret-2"],
                    workflow_result_path="reports/generated/negative-unauthorized-return-workflow-result.json",
                    workflow=_return_workflow(
                        returnState="PendingSettlement",
                        returnedLotIds=[],
                        remainingEncumberedLotIds=["lot-ret-1", "lot-ret-2"],
                        executionReportCount=0,
                        executionReports=[],
                    ),
                ),
            ],
            timeline=[_timeline_entry("positive-return")],
        )

        result = _check_no_double_encumbrance(
            margin_call_report=margin_call_report,
            substitution_report=substitution_report,
            return_report=return_report,
        )

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("reused a lot", result["detail"])

    def test_atomic_substitution_when_required_fails_when_partial_flow_releases_collateral(self) -> None:
        substitution_report = _demo_report(
            report_type="SubstitutionReport",
            report_artifact_key="substitutionReportPath",
            report_path="reports/generated/substitution-demo-report.json",
            summary_path="reports/generated/substitution-demo-summary.md",
            timeline_path="reports/generated/substitution-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="positive-substitution",
                    mode="POSITIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/positive-substitution-workflow-result.json",
                    workflow=_substitution_workflow(),
                ),
                _scenario(
                    scenario_id="negative-partial-substitution",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/negative-partial-substitution-workflow-result.json",
                    workflow=_substitution_workflow(
                        substitutionState="Approved",
                        activeEncumberedLotIds=["lot-old-1"],
                        releasedLotIds=["lot-old-1"],
                        atomicityOutcome="BLOCKED_ATOMICALLY",
                        executionReportCount=0,
                        executionReports=[],
                        controlChecks=[_control_check("PARTIAL_SUBSTITUTION_BLOCKED")],
                    ),
                ),
                _scenario(
                    scenario_id="negative-unauthorized-release",
                    mode="NEGATIVE",
                    current_posted_lot_ids=["lot-old-1"],
                    workflow_result_path="reports/generated/negative-unauthorized-release-workflow-result.json",
                    workflow=_substitution_workflow(
                        substitutionState="PendingSettlement",
                        activeEncumberedLotIds=["lot-old-1"],
                        releasedLotIds=[],
                        atomicityOutcome="BLOCKED_ATOMICALLY",
                        executionReportCount=0,
                        executionReports=[],
                    ),
                ),
            ],
            timeline=[_timeline_entry("positive-substitution")],
        )

        result = _check_atomic_substitution_when_required(
            substitution_report=substitution_report
        )

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("released collateral", result["detail"])

    def test_replay_safety_fails_without_replay_blocking_control(self) -> None:
        return_report = _demo_report(
            report_type="ReturnReport",
            report_artifact_key="returnReportPath",
            report_path="reports/generated/return-demo-report.json",
            summary_path="reports/generated/return-demo-summary.md",
            timeline_path="reports/generated/return-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="negative-replayed-return-instruction",
                    mode="NEGATIVE",
                    workflow_result_path="reports/generated/negative-replayed-return-instruction-workflow-result.json",
                    workflow=_return_workflow(controlChecks=[]),
                )
            ],
            timeline=[],
        )

        result = _check_replay_safety(return_report=return_report)

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("replay-blocking control check", result["detail"])

    def test_report_fidelity_fails_when_a_scenario_references_a_missing_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            self._write_artifact(repo_root, "reports/generated/demo-report.json")
            self._write_artifact(repo_root, "reports/generated/demo-summary.md", "# summary\n")
            self._write_artifact(repo_root, "reports/generated/demo-timeline.md", "# timeline\n")
            self._write_artifact(repo_root, "reports/generated/policy-report.json")
            self._write_artifact(repo_root, "reports/generated/optimizer-report.json")
            self._write_artifact(repo_root, "reports/generated/workflow-input.json")

            demo_report = _demo_report(
                report_type="ExecutionReport",
                report_artifact_key="executionReportPath",
                report_path="reports/generated/demo-report.json",
                summary_path="reports/generated/demo-summary.md",
                timeline_path="reports/generated/demo-timeline.md",
                scenarios=[
                    _scenario(
                        scenario_id="positive-margin-call",
                        mode="POSITIVE",
                        workflow_result_path="reports/generated/missing-workflow-result.json",
                        workflow=_margin_workflow(),
                        selected_lot_ids=["lot-margin-1"],
                        policy_evaluation_report_path="reports/generated/policy-report.json",
                        optimization_report_path="reports/generated/optimizer-report.json",
                        workflow_input_path="reports/generated/workflow-input.json",
                    )
                ],
                timeline=[_timeline_entry("positive-margin-call")],
            )

            result = _check_report_fidelity(
                demo_reports=[demo_report],
                repo_root=repo_root,
            )

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("missing workflowResultPath", result["detail"])

    def test_audit_trail_completeness_fails_without_execution_report_summary(self) -> None:
        demo_report = _demo_report(
            report_type="ExecutionReport",
            report_artifact_key="executionReportPath",
            report_path="reports/generated/margin-call-demo-execution-report.json",
            summary_path="reports/generated/margin-call-demo-summary.md",
            timeline_path="reports/generated/margin-call-demo-timeline.md",
            scenarios=[
                _scenario(
                    scenario_id="positive-margin-call",
                    mode="POSITIVE",
                    selected_lot_ids=["lot-margin-1"],
                    workflow_result_path="reports/generated/positive-margin-call-workflow-result.json",
                    workflow=_margin_workflow(
                        executionReports=[_execution_report(summary="")],
                    ),
                )
            ],
            timeline=[_timeline_entry("positive-margin-call")],
        )

        result = _check_audit_trail_completeness(demo_reports=[demo_report])

        self.assertEqual(result["status"], "FAIL")
        self.assertIn("missing summary", result["detail"])

    @staticmethod
    def _write_artifact(repo_root: Path, relative_path: str, contents: str = "{}\n") -> None:
        path = repo_root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
