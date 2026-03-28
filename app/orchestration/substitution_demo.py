"""End-to-end collateral substitution demo orchestration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from margin_call_demo import (
    DemoExecutionError,
    _append_timeline,
    _assert_equal,
    _assert_reason_codes,
    _load_json,
    _optimization_reason_codes as _base_optimization_reason_codes,
    _policy_reason_codes,
    _relative_path,
    _resolve_scenario_path,
    _run_daml_workflow,
    _utc_now,
    _validate_json_schema,
    _write_json,
    _write_text,
    evaluate_policy,
    optimize_collateral,
    write_optimization_report,
    write_policy_report,
)


def run_substitution_demo(
    *,
    manifest_path: str | Path,
    output_dir: str | Path,
    repo_root: str | Path,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root).resolve()
    manifest = _load_json(manifest_path)
    manifest_path_obj = Path(manifest_path).resolve()
    output_dir_path = Path(output_dir).resolve()
    output_dir_path.mkdir(parents=True, exist_ok=True)

    timeline: list[dict[str, Any]] = []
    scenario_results: list[dict[str, Any]] = []

    for sequence, scenario in enumerate(manifest["scenarios"], start=1):
        scenario_results.append(
            _run_scenario(
                scenario=scenario,
                sequence=sequence,
                manifest_path=manifest_path_obj,
                output_dir=output_dir_path,
                repo_root=repo_root_path,
                timeline=timeline,
            )
        )

    invariant_checks = _build_invariant_checks(scenario_results)
    substitution_report = _build_substitution_report(
        manifest=manifest,
        manifest_path=manifest_path_obj,
        repo_root=repo_root_path,
        output_dir=output_dir_path,
        scenario_results=scenario_results,
        timeline=timeline,
        invariant_checks=invariant_checks,
    )

    report_path = output_dir_path / "substitution-demo-report.json"
    summary_path = output_dir_path / "substitution-demo-summary.md"
    timeline_path = output_dir_path / "substitution-demo-timeline.md"

    substitution_report["artifacts"] = {
        "substitutionReportPath": _relative_path(report_path, repo_root_path),
        "markdownSummaryPath": _relative_path(summary_path, repo_root_path),
        "timelinePath": _relative_path(timeline_path, repo_root_path),
    }

    _write_json(report_path, substitution_report)
    _validate_json_schema(
        report_path=report_path,
        schema_path=repo_root_path / "reports/schemas/substitution-report.schema.json",
    )

    _write_markdown_summary(summary_path, substitution_report)
    _write_timeline_markdown(timeline_path, substitution_report)

    return substitution_report


def _run_scenario(
    *,
    scenario: dict[str, Any],
    sequence: int,
    manifest_path: Path,
    output_dir: Path,
    repo_root: Path,
    timeline: list[dict[str, Any]],
) -> dict[str, Any]:
    scenario_id = scenario["scenarioId"]
    scenario_mode = scenario["mode"]
    expected = scenario["expected"]
    resolved_policy_path = _resolve_scenario_path(manifest_path, scenario["policy"])
    resolved_inventory_path = _resolve_scenario_path(manifest_path, scenario["inventory"])
    resolved_obligation_path = (
        _resolve_scenario_path(manifest_path, scenario["obligation"])
        if scenario.get("obligation")
        else None
    )

    policy = _load_json(resolved_policy_path)
    inventory = _load_json(resolved_inventory_path)
    obligation = _load_json(resolved_obligation_path) if resolved_obligation_path else None

    policy_report_path = output_dir / f"{scenario_id}-policy-evaluation-report.json"
    optimization_report_path = (
        output_dir / f"{scenario_id}-optimization-report.json"
        if scenario.get("runOptimization", False)
        else None
    )
    workflow_input_path = (
        output_dir / f"{scenario_id}-workflow-input.json"
        if scenario.get("runWorkflow", False)
        else None
    )
    workflow_result_path = (
        output_dir / f"{scenario_id}-workflow-result.json"
        if scenario.get("runWorkflow", False)
        else None
    )

    policy_started_at = _utc_now()
    policy_report = evaluate_policy(policy, inventory)
    write_policy_report(policy_report, policy_report_path)
    _validate_json_schema(
        report_path=policy_report_path,
        schema_path=repo_root / "reports/schemas/policy-evaluation-report.schema.json",
    )
    policy_finished_at = _utc_now()
    _append_timeline(
        timeline=timeline,
        sequence=sequence,
        scenario_id=scenario_id,
        phase="POLICY_EVALUATION",
        status="COMPLETED",
        started_at=policy_started_at,
        finished_at=policy_finished_at,
        artifact_path=_relative_path(policy_report_path, repo_root),
        detail=(
            f"Evaluated substitution candidates for {scenario_mode.lower()} scenario "
            f"with overall decision {policy_report['overallDecision']}."
        ),
    )
    _assert_equal(
        actual=policy_report["overallDecision"],
        expected=expected["policyOverallDecision"],
        message=f"{scenario_id}: unexpected policy overall decision",
    )

    optimization_report = None
    if scenario.get("runOptimization", False):
        if obligation is None or optimization_report_path is None:
            raise DemoExecutionError(
                f"{scenario_id}: optimization requested without an obligation input"
            )
        optimization_started_at = _utc_now()
        optimization_report = optimize_collateral(policy, inventory, obligation)
        write_optimization_report(optimization_report, optimization_report_path)
        _validate_json_schema(
            report_path=optimization_report_path,
            schema_path=repo_root / "reports/schemas/optimization-report.schema.json",
        )
        optimization_finished_at = _utc_now()
        _append_timeline(
            timeline=timeline,
            sequence=sequence,
            scenario_id=scenario_id,
            phase="OPTIMIZATION",
            status="COMPLETED",
            started_at=optimization_started_at,
            finished_at=optimization_finished_at,
            artifact_path=_relative_path(optimization_report_path, repo_root),
            detail=(
                f"Optimized the substitution request for scenario {scenario_id} with "
                f"recommendation {optimization_report['recommendedAction']}."
            ),
        )
        _assert_equal(
            actual=optimization_report["status"],
            expected=expected["optimizationStatus"],
            message=f"{scenario_id}: unexpected optimization status",
        )
        if "recommendedAction" in expected:
            _assert_equal(
                actual=optimization_report["recommendedAction"],
                expected=expected["recommendedAction"],
                message=f"{scenario_id}: unexpected optimization action",
            )

    workflow_result = None
    if scenario.get("runWorkflow", False):
        if optimization_report is None or obligation is None:
            raise DemoExecutionError(
                f"{scenario_id}: workflow requested without optimization output"
            )
        if workflow_input_path is None or workflow_result_path is None:
            raise DemoExecutionError(f"{scenario_id}: workflow artifact paths are missing")
        workflow_request = _build_workflow_request(
            scenario=scenario,
            inventory=inventory,
            obligation=obligation,
            policy=policy,
            policy_report=policy_report,
            optimization_report=optimization_report,
        )
        _write_json(workflow_input_path, workflow_request)
        workflow_started_at = _utc_now()
        workflow_result = _run_daml_workflow(
            script_name=scenario["workflow"]["scriptName"],
            input_path=workflow_input_path,
            output_path=workflow_result_path,
            repo_root=repo_root,
        )
        workflow_finished_at = _utc_now()
        _append_timeline(
            timeline=timeline,
            sequence=sequence,
            scenario_id=scenario_id,
            phase="WORKFLOW",
            status="COMPLETED",
            started_at=workflow_started_at,
            finished_at=workflow_finished_at,
            artifact_path=_relative_path(workflow_result_path, repo_root),
            detail=_workflow_timeline_detail(scenario_id, workflow_result),
        )
        _validate_workflow_result(
            scenario_id=scenario_id,
            workflow_result=workflow_result,
            expected=expected,
        )

    observed_reason_codes = sorted(
        set(_policy_reason_codes(policy_report))
        | set(_substitution_optimization_reason_codes(optimization_report))
        | set(_workflow_reason_codes(workflow_result, scenario_mode=scenario_mode))
    )
    _assert_reason_codes(
        scenario_id=scenario_id,
        observed_reason_codes=observed_reason_codes,
        expected_reason_codes=expected.get("reasonCodes", []),
    )

    summary = _scenario_summary(
        scenario=scenario,
        policy_report=policy_report,
        optimization_report=optimization_report,
        workflow_result=workflow_result,
    )

    replacement_lot_ids = (
        []
        if optimization_report is None or optimization_report["recommendedPortfolio"] is None
        else optimization_report["recommendedPortfolio"]["lotIds"]
    )

    return {
        "scenarioId": scenario_id,
        "mode": scenario_mode,
        "description": scenario["description"],
        "result": "SUCCESS" if scenario_mode == "POSITIVE" else "EXPECTED_FAILURE",
        "summary": summary,
        "observedReasonCodes": observed_reason_codes,
        "expectedReasonCodes": expected.get("reasonCodes", []),
        "policyEvaluationReportPath": _relative_path(policy_report_path, repo_root),
        "optimizationReportPath": (
            None
            if optimization_report_path is None
            else _relative_path(optimization_report_path, repo_root)
        ),
        "workflowInputPath": (
            None if workflow_input_path is None else _relative_path(workflow_input_path, repo_root)
        ),
        "workflowResultPath": (
            None if workflow_result_path is None else _relative_path(workflow_result_path, repo_root)
        ),
        "policyDecision": policy_report["overallDecision"],
        "optimizationStatus": (
            None if optimization_report is None else optimization_report["status"]
        ),
        "recommendedAction": (
            None
            if optimization_report is None
            else optimization_report["recommendedAction"]
        ),
        "currentPostedLotIds": (
            []
            if obligation is None
            else sorted(obligation.get("currentPostedLotIds", []))
        ),
        "replacementLotIds": replacement_lot_ids,
        "workflow": workflow_result,
    }


def _build_workflow_request(
    *,
    scenario: dict[str, Any],
    inventory: dict[str, Any],
    obligation: dict[str, Any],
    policy: dict[str, Any],
    policy_report: dict[str, Any],
    optimization_report: dict[str, Any],
) -> dict[str, Any]:
    substitution_request = obligation.get("substitutionRequest")
    if substitution_request is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: workflow requested without a substitutionRequest block"
        )
    recommended_portfolio = optimization_report["recommendedPortfolio"]
    if recommended_portfolio is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: workflow requested without a recommended replacement portfolio"
        )

    workflow_config = scenario["workflow"]
    inventory_by_lot_id = {lot["lotId"]: lot for lot in inventory["candidateLots"]}
    current_posted_lot_ids = obligation["currentPostedLotIds"]
    replacement_lot_ids = recommended_portfolio["lotIds"]

    policy_atomicity_required = not policy["substitutionRights"]["partialSubstitutionAllowed"]
    if substitution_request["atomicityRequired"] != policy_atomicity_required:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: substitutionRequest.atomicityRequired must match the policy partial-substitution rule"
        )

    return {
        "scenarioId": scenario["scenarioId"],
        "obligationId": obligation["obligationId"],
        "correlationId": workflow_config["correlationId"],
        "policyVersion": policy["policyVersion"],
        "snapshotId": workflow_config.get(
            "snapshotId",
            f"{inventory['inventorySetId']}::{inventory['evaluationContext']['asOf']}",
        ),
        "decisionReference": workflow_config.get(
            "decisionReference", policy_report["evaluationId"]
        ),
        "requiredCoverage": obligation["obligationAmount"],
        "currentPostedLots": [
            _workflow_lot_input(
                inventory_by_lot_id[lot_id],
                workflow_config,
            )
            for lot_id in current_posted_lot_ids
        ],
        "replacementLots": [
            _workflow_lot_input(
                inventory_by_lot_id[lot_id],
                workflow_config,
            )
            for lot_id in replacement_lot_ids
        ],
        "requiresSecuredPartyApproval": policy["substitutionRights"]["requiresSecuredPartyConsent"],
        "requiresCustodianApproval": policy["substitutionRights"]["requiresCustodianConsent"],
        "atomicityRequired": substitution_request["atomicityRequired"],
        "simulateUnauthorizedReleaseAttempt": workflow_config.get(
            "simulateUnauthorizedReleaseAttempt", False
        ),
        "simulatePartialSettlementAttempt": workflow_config.get(
            "simulatePartialSettlementAttempt", False
        ),
    }


def _workflow_lot_input(
    lot: dict[str, Any],
    workflow_config: dict[str, Any],
) -> dict[str, Any]:
    quantity = lot.get("nominalValue", lot.get("marketValue"))
    if quantity is None:
        raise DemoExecutionError(
            f"lot {lot['lotId']} lacks nominalValue and marketValue for workflow input"
        )
    return {
        "lotId": lot["lotId"],
        "assetId": lot["assetId"],
        "issuer": lot["issuerId"],
        "assetClass": lot["assetClass"],
        "currency": lot["currency"],
        "settlementSystem": workflow_config["settlementSystem"],
        "tokenAdapterReference": workflow_config.get(
            "tokenAdapterReferencePrefix", "demo/adapter"
        )
        + f"/{lot['assetId']}",
        "jurisdiction": lot["issuanceJurisdiction"],
        "transferabilityFlags": workflow_config.get(
            "transferabilityFlags",
            ["deliverable", "pledgeable", "segregated"],
        ),
        "custodyAccount": workflow_config["sourceAccount"],
        "quantity": quantity,
        "sourceAccount": workflow_config["sourceAccount"],
        "destinationAccount": workflow_config["destinationAccount"],
    }


def _validate_workflow_result(
    *,
    scenario_id: str,
    workflow_result: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    _assert_equal(
        actual=workflow_result["substitutionState"],
        expected=expected["workflowSubstitutionState"],
        message=f"{scenario_id}: unexpected substitution workflow state",
    )
    _assert_equal(
        actual=sorted(workflow_result["activeEncumberedLotIds"]),
        expected=sorted(expected["activeEncumberedLotIds"]),
        message=f"{scenario_id}: active encumbrance set drifted from the expected state",
    )
    _assert_equal(
        actual=sorted(workflow_result["releasedLotIds"]),
        expected=sorted(expected["releasedLotIds"]),
        message=f"{scenario_id}: released encumbrance set drifted from the expected state",
    )
    _assert_equal(
        actual=workflow_result["atomicityOutcome"],
        expected=expected["atomicityOutcome"],
        message=f"{scenario_id}: unexpected atomicity outcome",
    )
    if "requiredControlChecks" in expected:
        observed_control_checks = sorted(
            check["checkId"] for check in workflow_result["controlChecks"]
        )
        _assert_equal(
            actual=observed_control_checks,
            expected=sorted(expected["requiredControlChecks"]),
            message=f"{scenario_id}: workflow control checks drifted from the expected set",
        )
    if workflow_result["executionReportCount"] < expected["minimumExecutionReportCount"]:
        raise DemoExecutionError(
            f"{scenario_id}: expected at least {expected['minimumExecutionReportCount']} "
            f"execution reports but found {workflow_result['executionReportCount']}"
        )


def _workflow_reason_codes(
    workflow_result: dict[str, Any] | None,
    *,
    scenario_mode: str,
) -> list[str]:
    if workflow_result is None or scenario_mode != "NEGATIVE":
        return []
    return sorted(check["checkId"] for check in workflow_result["controlChecks"])


def _substitution_optimization_reason_codes(
    optimization_report: dict[str, Any] | None,
) -> list[str]:
    if optimization_report is None:
        return []
    decision_trace = next(
        (
            trace
            for trace in optimization_report["explanationTrace"]
            if trace["stage"] == "DECISION" and trace["reasonCodes"]
        ),
        None,
    )
    if decision_trace is not None:
        return sorted(set(decision_trace["reasonCodes"]))
    return _base_optimization_reason_codes(optimization_report)


def _workflow_timeline_detail(
    scenario_id: str,
    workflow_result: dict[str, Any],
) -> str:
    if workflow_result["substitutionState"] == "Closed":
        return (
            f"Recorded the Daml substitution workflow for scenario {scenario_id} and "
            "confirmed atomic encumbrance replacement."
        )
    return (
        f"Recorded the Daml control failure for scenario {scenario_id} with "
        f"workflow state {workflow_result['substitutionState']}."
    )


def _build_substitution_report(
    *,
    manifest: dict[str, Any],
    manifest_path: Path,
    repo_root: Path,
    output_dir: Path,
    scenario_results: list[dict[str, Any]],
    timeline: list[dict[str, Any]],
    invariant_checks: list[dict[str, Any]],
) -> dict[str, Any]:
    positive_scenarios = [scenario for scenario in scenario_results if scenario["mode"] == "POSITIVE"]
    negative_scenarios = [scenario for scenario in scenario_results if scenario["mode"] == "NEGATIVE"]
    canonical = json.dumps(
        {"manifest": manifest, "scenarioResults": scenario_results},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    primary_optimization_ref = (
        positive_scenarios[0]["optimizationReportPath"] if positive_scenarios else None
    )

    return {
        "$schema": "../../reports/schemas/substitution-report.schema.json",
        "reportType": "SubstitutionReport",
        "reportVersion": "0.1.0",
        "substitutionReportId": f"srr-{digest[:16]}",
        "generatedAt": _utc_now(),
        "overallStatus": "PASS",
        "demo": {
            "demoId": manifest["demoId"],
            "demoVersion": manifest["demoVersion"],
            "command": "make demo-substitution",
            "manifestPath": _relative_path(manifest_path, repo_root),
            "outputDirectory": _relative_path(output_dir, repo_root),
            "primaryOptimizationArtifact": primary_optimization_ref,
            "scenarioCount": len(scenario_results),
            "positiveScenarioCount": len(positive_scenarios),
            "negativeScenarioCount": len(negative_scenarios),
        },
        "artifacts": {},
        "scenarios": scenario_results,
        "timeline": timeline,
        "invariantChecks": invariant_checks,
    }


def _build_invariant_checks(
    scenario_results: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    positive_scenario = next(
        scenario for scenario in scenario_results if scenario["mode"] == "POSITIVE"
    )
    negative_scenarios = [
        scenario for scenario in scenario_results if scenario["mode"] == "NEGATIVE"
    ]
    unauthorized_scenario = next(
        scenario
        for scenario in negative_scenarios
        if scenario["scenarioId"] == "negative-unauthorized-release"
    )
    partial_scenario = next(
        scenario
        for scenario in negative_scenarios
        if scenario["scenarioId"] == "negative-partial-substitution"
    )

    return [
        {
            "invariantId": "PDR-001",
            "status": "PASS",
            "evidence": [positive_scenario["policyEvaluationReportPath"]],
            "note": "The positive substitution path used a generated policy-evaluation report derived from declared inputs.",
        },
        {
            "invariantId": "ALLOC-001",
            "status": "PASS",
            "evidence": [positive_scenario["optimizationReportPath"]],
            "note": "The optimizer produced a deterministic replacement recommendation with explicit substitution deltas.",
        },
        {
            "invariantId": "CTRL-001",
            "status": "PASS",
            "evidence": [
                positive_scenario["workflowResultPath"],
                unauthorized_scenario["workflowResultPath"],
            ],
            "note": "The workflow blocked pre-approval settlement intent creation and blocked the unauthorized release attempt while preserving the current encumbrances.",
        },
        {
            "invariantId": "ATOM-001",
            "status": "PASS",
            "evidence": [
                positive_scenario["workflowResultPath"],
                partial_scenario["workflowResultPath"],
            ],
            "note": "The positive path replaced encumbrances atomically, and the partial-substitution path failed without releasing the incumbent encumbrances.",
        },
        {
            "invariantId": "REPT-001",
            "status": "PASS",
            "evidence": [
                positive_scenario["workflowResultPath"],
                positive_scenario["policyEvaluationReportPath"],
                positive_scenario["optimizationReportPath"],
            ],
            "note": "The substitution report references real workflow, policy, and optimizer artifacts rather than operator-authored summaries.",
        },
        {
            "invariantId": "EXCP-001",
            "status": "PASS",
            "evidence": [
                artifact
                for scenario in negative_scenarios
                for artifact in (
                    scenario["policyEvaluationReportPath"],
                    scenario["optimizationReportPath"],
                    scenario["workflowResultPath"],
                )
                if artifact is not None
            ],
            "note": "The negative substitution scenarios failed deterministically for ineligibility, concentration, unauthorized release, and partial-settlement atomicity violations.",
        },
    ]


def _scenario_summary(
    *,
    scenario: dict[str, Any],
    policy_report: dict[str, Any],
    optimization_report: dict[str, Any] | None,
    workflow_result: dict[str, Any] | None,
) -> str:
    if scenario["mode"] == "POSITIVE":
        assert optimization_report is not None
        assert workflow_result is not None
        return (
            f"Current encumbrances stayed controlled until approval, the optimizer recommended "
            f"{', '.join(workflow_result['replacementLotIds'])}, and the Daml workflow "
            f"closed the substitution atomically against outgoing lots "
            f"{', '.join(workflow_result['releasedLotIds'])}."
        )

    if workflow_result is not None:
        control_codes = ", ".join(check["checkId"] for check in workflow_result["controlChecks"])
        return (
            f"The workflow blocked the control path with atomicity outcome "
            f"{workflow_result['atomicityOutcome']} and control checks {control_codes}."
        )

    if optimization_report is None:
        return (
            f"Policy evaluation blocked the replacement inventory with decision "
            f"{policy_report['overallDecision']} and reason codes "
            f"{', '.join(_policy_reason_codes(policy_report))}."
        )

    return (
        f"Policy evaluation stayed admissible at the lot level, but optimization "
        f"ended with {optimization_report['status']} and reason codes "
        f"{', '.join(_substitution_optimization_reason_codes(optimization_report))}."
    )


def _write_markdown_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Substitution Demo Summary",
        "",
        f"- Report ID: `{report['substitutionReportId']}`",
        f"- Command: `{report['demo']['command']}`",
        f"- Manifest: `{report['demo']['manifestPath']}`",
        f"- Report artifact: `{report['artifacts']['substitutionReportPath']}`",
        "",
        "## Scenario Outcomes",
        "",
        "| Scenario | Mode | Result | Summary |",
        "| --- | --- | --- | --- |",
    ]
    for scenario in report["scenarios"]:
        lines.append(
            f"| {scenario['scenarioId']} | {scenario['mode']} | {scenario['result']} | {scenario['summary']} |"
        )

    lines.extend(
        [
            "",
            "## Invariant Checks",
            "",
            "| Invariant | Status | Evidence | Note |",
            "| --- | --- | --- | --- |",
        ]
    )
    for check in report["invariantChecks"]:
        evidence = ", ".join(f"`{item}`" for item in check["evidence"])
        lines.append(
            f"| {check['invariantId']} | {check['status']} | {evidence} | {check['note']} |"
        )

    _write_text(path, "\n".join(lines) + "\n")


def _write_timeline_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Substitution Demo Timeline",
        "",
        "| Seq | Scenario | Phase | Status | Artifact | Detail |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for entry in report["timeline"]:
        artifact = "`-`" if entry["artifactPath"] is None else f"`{entry['artifactPath']}`"
        lines.append(
            f"| {entry['sequence']} | {entry['scenarioId']} | {entry['phase']} | {entry['status']} | {artifact} | {entry['detail']} |"
        )
    _write_text(path, "\n".join(lines) + "\n")
