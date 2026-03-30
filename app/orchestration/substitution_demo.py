"""End-to-end collateral substitution demo orchestration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from margin_call_demo import (
    ADAPTER_BLOCKED,
    ADAPTER_EXECUTED,
    ADAPTER_NOT_REQUESTED,
    BLOCKING_ADAPTER,
    BLOCKING_OPTIMIZATION,
    BLOCKING_POLICY,
    BLOCKING_WORKFLOW,
    QUICKSTART_CONTROL_PLANE_STATE_ROOT,
    RUNTIME_IDE_LEDGER,
    RUNTIME_QUICKSTART,
    DemoExecutionError,
    _append_timeline,
    _assert_equal,
    _assert_reason_codes,
    _compact_paths,
    _load_json,
    _localnet_env,
    _optimization_reason_codes as _base_optimization_reason_codes,
    _policy_reason_codes,
    _relative_path,
    _resolve_scenario_path,
    _run_command,
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
    runtime_mode: str = RUNTIME_IDE_LEDGER,
    report_basename: str | None = None,
    command_name: str | None = None,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root).resolve()
    manifest = _load_json(manifest_path)
    manifest_path_obj = Path(manifest_path).resolve()
    output_dir_path = Path(output_dir).resolve()
    output_dir_path.mkdir(parents=True, exist_ok=True)

    normalized_runtime_mode = runtime_mode.upper()
    if normalized_runtime_mode not in {RUNTIME_IDE_LEDGER, RUNTIME_QUICKSTART}:
        raise DemoExecutionError(f"unsupported substitution runtime mode {runtime_mode!r}")

    report_stem = report_basename or _default_report_basename(normalized_runtime_mode)
    command = command_name or _default_command_name(normalized_runtime_mode)

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
                runtime_mode=normalized_runtime_mode,
                timeline=timeline,
            )
        )

    invariant_checks = _build_invariant_checks(
        scenario_results=scenario_results,
        runtime_mode=normalized_runtime_mode,
    )
    substitution_report = _build_substitution_report(
        manifest=manifest,
        manifest_path=manifest_path_obj,
        repo_root=repo_root_path,
        output_dir=output_dir_path,
        scenario_results=scenario_results,
        timeline=timeline,
        invariant_checks=invariant_checks,
        runtime_mode=normalized_runtime_mode,
        command_name=command,
    )

    report_path = output_dir_path / f"{report_stem}-report.json"
    summary_path = output_dir_path / f"{report_stem}-summary.md"
    timeline_path = output_dir_path / f"{report_stem}-timeline.md"

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
    runtime_mode: str,
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
    quickstart_seed_receipt_path: Path | None = None
    adapter_execution_report_path: Path | None = None
    adapter_status_path: Path | None = None

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
    adapter_report = None
    adapter_status = None

    if scenario.get("runWorkflow", False):
        if optimization_report is None or obligation is None:
            raise DemoExecutionError(
                f"{scenario_id}: workflow requested without optimization output"
            )
        if workflow_input_path is None or workflow_result_path is None:
            raise DemoExecutionError(f"{scenario_id}: workflow artifact paths are missing")

        if runtime_mode == RUNTIME_IDE_LEDGER:
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
                detail=_ide_workflow_timeline_detail(scenario_id, workflow_result),
            )
            _validate_ide_workflow_result(
                scenario_id=scenario_id,
                workflow_result=workflow_result,
                expected=expected,
            )
        else:
            quickstart_artifact_dir = output_dir / scenario_id
            quickstart_state_dir = QUICKSTART_CONTROL_PLANE_STATE_ROOT / scenario_id
            quickstart_artifact_dir.mkdir(parents=True, exist_ok=True)
            quickstart_state_dir.mkdir(parents=True, exist_ok=True)
            quickstart_manifest_path = _resolve_scenario_path(
                manifest_path,
                scenario["quickstartScenarioManifest"],
            )

            seed_started_at = _utc_now()
            quickstart_seed_receipt_path = _run_quickstart_seed(
                repo_root=repo_root,
                scenario_artifact_dir=quickstart_artifact_dir,
                scenario_state_dir=quickstart_state_dir,
                quickstart_manifest_path=quickstart_manifest_path,
            )
            seed_finished_at = _utc_now()
            _append_timeline(
                timeline=timeline,
                sequence=sequence,
                scenario_id=scenario_id,
                phase="QUICKSTART_SEED",
                status="COMPLETED",
                started_at=seed_started_at,
                finished_at=seed_finished_at,
                artifact_path=_relative_path(quickstart_seed_receipt_path, repo_root),
                detail=(
                    f"Seeded or reused the declared Quickstart substitution scenario for "
                    f"{scenario_id} before workflow execution."
                ),
            )

            seed_receipt = _load_json(quickstart_seed_receipt_path)
            workflow_request = _build_quickstart_workflow_request(
                scenario=scenario,
                obligation=obligation,
                policy=policy,
                optimization_report=optimization_report,
                seed_receipt=seed_receipt,
            )
            _write_json(workflow_input_path, workflow_request)

            workflow_started_at = _utc_now()
            workflow_result = _run_quickstart_workflow(
                repo_root=repo_root,
                scenario_artifact_dir=quickstart_artifact_dir,
                scenario_state_dir=quickstart_state_dir,
                workflow_input_path=workflow_input_path,
                workflow_result_path=workflow_result_path,
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
                detail=_quickstart_workflow_timeline_detail(scenario_id, workflow_result),
            )
            _validate_quickstart_workflow_result(
                scenario_id=scenario_id,
                workflow_result=workflow_result,
                expected=expected,
            )

            status_output_path = quickstart_artifact_dir / "localnet-substitution-status.json"
            if scenario.get("runAdapter", False):
                adapter_input_path = quickstart_state_dir / "substitution-adapter-input.json"
                adapter_execution_report_path = (
                    quickstart_artifact_dir
                    / "localnet-substitution-adapter-execution-report.json"
                )
                adapter_request = _build_quickstart_adapter_input(
                    seed_receipt=seed_receipt,
                    workflow_result=workflow_result,
                )
                _write_json(adapter_input_path, adapter_request)
                adapter_started_at = _utc_now()
                _run_quickstart_adapter(
                    repo_root=repo_root,
                    scenario_artifact_dir=quickstart_artifact_dir,
                    scenario_state_dir=quickstart_state_dir,
                    adapter_input_path=adapter_input_path,
                    adapter_output_path=adapter_execution_report_path,
                )
                adapter_finished_at = _utc_now()
                adapter_status_path = _run_quickstart_status(
                    repo_root=repo_root,
                    scenario_artifact_dir=quickstart_artifact_dir,
                    scenario_state_dir=quickstart_state_dir,
                    status_output_path=status_output_path,
                )
                adapter_report = _load_json(adapter_execution_report_path)
                adapter_status = _load_json(adapter_status_path)
                _append_timeline(
                    timeline=timeline,
                    sequence=sequence,
                    scenario_id=scenario_id,
                    phase="ADAPTER",
                    status="COMPLETED",
                    started_at=adapter_started_at,
                    finished_at=adapter_finished_at,
                    artifact_path=_relative_path(adapter_execution_report_path, repo_root),
                    detail=(
                        f"Executed the reference token adapter for scenario {scenario_id}, "
                        "released the incumbent holdings, moved the replacement holdings, "
                        "and confirmed substitution settlement on Quickstart."
                    ),
                )
                _validate_quickstart_adapter_result(
                    scenario_id=scenario_id,
                    adapter_report=adapter_report,
                    adapter_status=adapter_status,
                    expected=expected,
                )
            else:
                adapter_status_started_at = _utc_now()
                adapter_status_path = _run_quickstart_status(
                    repo_root=repo_root,
                    scenario_artifact_dir=quickstart_artifact_dir,
                    scenario_state_dir=quickstart_state_dir,
                    status_output_path=status_output_path,
                )
                adapter_status_finished_at = _utc_now()
                adapter_status = _load_json(adapter_status_path)
                _append_timeline(
                    timeline=timeline,
                    sequence=sequence,
                    scenario_id=scenario_id,
                    phase="ADAPTER",
                    status="SKIPPED",
                    started_at=adapter_status_started_at,
                    finished_at=adapter_status_finished_at,
                    artifact_path=_relative_path(adapter_status_path, repo_root),
                    detail=(
                        f"Did not invoke the adapter for scenario {scenario_id} because "
                        "the substitution workflow blocked before a committed replacement handoff."
                    ),
                )
                _validate_quickstart_blocked_status(
                    scenario_id=scenario_id,
                    adapter_status=adapter_status,
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

    replacement_lot_ids = (
        []
        if optimization_report is None or optimization_report["recommendedPortfolio"] is None
        else optimization_report["recommendedPortfolio"]["lotIds"]
    )
    atomicity_evidence = _build_atomicity_evidence(
        runtime_mode=runtime_mode,
        scenario_mode=scenario_mode,
        current_posted_lot_ids=(
            [] if obligation is None else sorted(obligation.get("currentPostedLotIds", []))
        ),
        replacement_lot_ids=replacement_lot_ids,
        workflow_result=workflow_result,
        adapter_report=adapter_report,
        adapter_status=adapter_status,
    )

    return {
        "scenarioId": scenario_id,
        "mode": scenario_mode,
        "description": scenario["description"],
        "result": "SUCCESS" if scenario_mode == "POSITIVE" else "EXPECTED_FAILURE",
        "summary": _scenario_summary(
            scenario=scenario,
            runtime_mode=runtime_mode,
            policy_report=policy_report,
            optimization_report=optimization_report,
            workflow_result=workflow_result,
            adapter_report=adapter_report,
            adapter_status=adapter_status,
        ),
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
        "quickstartSeedReceiptPath": (
            None
            if quickstart_seed_receipt_path is None
            else _relative_path(quickstart_seed_receipt_path, repo_root)
        ),
        "adapterExecutionReportPath": (
            None
            if adapter_execution_report_path is None
            else _relative_path(adapter_execution_report_path, repo_root)
        ),
        "adapterStatusPath": (
            None if adapter_status_path is None else _relative_path(adapter_status_path, repo_root)
        ),
        "workflowRuntime": None if workflow_result is None else runtime_mode,
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
        "blockedPhase": _blocked_phase(
            scenario_mode=scenario_mode,
            policy_report=policy_report,
            optimization_report=optimization_report,
            workflow_result=workflow_result,
            adapter_report=adapter_report,
        ),
        "adapterOutcome": _adapter_outcome(
            workflow_result=workflow_result,
            adapter_report=adapter_report,
        ),
        "atomicityEvidence": atomicity_evidence,
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


def _build_quickstart_workflow_request(
    *,
    scenario: dict[str, Any],
    obligation: dict[str, Any],
    policy: dict[str, Any],
    optimization_report: dict[str, Any],
    seed_receipt: dict[str, Any],
) -> dict[str, Any]:
    substitution_request = obligation.get("substitutionRequest")
    if substitution_request is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: Quickstart workflow requested without a substitutionRequest block"
        )
    recommended_portfolio = optimization_report["recommendedPortfolio"]
    if recommended_portfolio is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: Quickstart workflow requested without a recommended replacement portfolio"
        )

    selected_replacement_lot_ids = recommended_portfolio["lotIds"]
    seeded_replacement_lot_ids = [lot["lotId"] for lot in seed_receipt["replacementLots"]]
    _assert_equal(
        actual=sorted(selected_replacement_lot_ids),
        expected=sorted(seeded_replacement_lot_ids),
        message=(
            f"{scenario['scenarioId']}: optimizer-selected replacement lots drifted from "
            "the declared Quickstart substitution seed scenario"
        ),
    )
    _assert_equal(
        actual=sorted(obligation["currentPostedLotIds"]),
        expected=sorted(lot["lotId"] for lot in seed_receipt["currentEncumberedLots"]),
        message=(
            f"{scenario['scenarioId']}: incumbent lot scope drifted from the declared "
            "Quickstart substitution seed scenario"
        ),
    )
    _assert_equal(
        actual=obligation["obligationId"],
        expected=seed_receipt["obligationId"],
        message=f"{scenario['scenarioId']}: obligation id drifted from the Quickstart seed receipt",
    )

    policy_atomicity_required = not policy["substitutionRights"]["partialSubstitutionAllowed"]
    _assert_equal(
        actual=substitution_request["atomicityRequired"],
        expected=policy_atomicity_required,
        message=(
            f"{scenario['scenarioId']}: substitutionRequest.atomicityRequired must match "
            "the policy partial-substitution rule"
        ),
    )

    replacement_lots_by_id = {
        lot["lotId"]: lot for lot in seed_receipt["replacementLots"]
    }
    replacement_lots = [replacement_lots_by_id[lot_id] for lot_id in selected_replacement_lot_ids]

    return {
        "scenarioId": scenario["scenarioId"],
        "obligationId": seed_receipt["obligationId"],
        "correlationId": seed_receipt["correlationId"],
        "policyVersion": seed_receipt["policyVersion"],
        "snapshotId": seed_receipt["snapshotId"],
        "decisionReference": seed_receipt["decisionReference"],
        "providerParty": seed_receipt["providerParty"],
        "securedParty": seed_receipt["securedParty"],
        "custodianParty": seed_receipt["custodianParty"],
        "currentEncumberedLotIds": obligation["currentPostedLotIds"],
        "replacementLots": replacement_lots,
        "requiresSecuredPartyApproval": policy["substitutionRights"]["requiresSecuredPartyConsent"],
        "requiresCustodianApproval": policy["substitutionRights"]["requiresCustodianConsent"],
        "atomicityRequired": substitution_request["atomicityRequired"],
        "workflowGate": scenario["workflowGate"],
    }


def _build_quickstart_adapter_input(
    *,
    seed_receipt: dict[str, Any],
    workflow_result: dict[str, Any],
) -> dict[str, Any]:
    settlement_instruction_id = workflow_result.get("settlementInstructionId")
    if settlement_instruction_id is None:
        raise DemoExecutionError(
            f"{workflow_result['scenarioId']}: Quickstart adapter requested without a settlement instruction"
        )

    return {
        "scenarioId": workflow_result["scenarioId"],
        "obligationId": seed_receipt["obligationId"],
        "providerParty": seed_receipt["providerParty"],
        "securedParty": seed_receipt["securedParty"],
        "custodianParty": seed_receipt["custodianParty"],
        "settlementInstructionId": settlement_instruction_id,
        "currentEncumberedLots": seed_receipt["currentEncumberedLots"],
        "replacementLots": seed_receipt["replacementLots"],
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


def _validate_ide_workflow_result(
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


def _validate_quickstart_workflow_result(
    *,
    scenario_id: str,
    workflow_result: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    _assert_equal(
        actual=workflow_result["substitutionState"],
        expected=expected["workflowSubstitutionState"],
        message=f"{scenario_id}: unexpected Quickstart substitution state",
    )
    _assert_equal(
        actual=workflow_result["workflowGate"],
        expected=expected["workflowGate"],
        message=f"{scenario_id}: unexpected Quickstart substitution workflow gate",
    )
    _assert_equal(
        actual=workflow_result.get("settlementInstructionState"),
        expected=expected.get("workflowSettlementInstructionState"),
        message=f"{scenario_id}: unexpected Quickstart substitution instruction state",
    )
    _assert_equal(
        actual=sorted(workflow_result["activeEncumberedLotIds"]),
        expected=sorted(expected["activeEncumberedLotIds"]),
        message=f"{scenario_id}: Quickstart active encumbrance set drifted from the expected state",
    )
    _assert_equal(
        actual=sorted(workflow_result["releasedLotIds"]),
        expected=sorted(expected["releasedLotIds"]),
        message=f"{scenario_id}: Quickstart released encumbrance set drifted from the expected state",
    )
    _assert_equal(
        actual=workflow_result["atomicityOutcome"],
        expected=expected["atomicityOutcome"],
        message=f"{scenario_id}: unexpected Quickstart atomicity outcome",
    )
    if "requiredControlChecks" in expected:
        observed_control_checks = sorted(
            check["checkId"] for check in workflow_result["controlChecks"]
        )
        _assert_equal(
            actual=observed_control_checks,
            expected=sorted(expected["requiredControlChecks"]),
            message=f"{scenario_id}: Quickstart workflow control checks drifted from the expected set",
        )
    if workflow_result["executionReportCount"] < expected["minimumExecutionReportCount"]:
        raise DemoExecutionError(
            f"{scenario_id}: expected at least {expected['minimumExecutionReportCount']} "
            f"Quickstart execution reports but found {workflow_result['executionReportCount']}"
        )


def _validate_quickstart_adapter_result(
    *,
    scenario_id: str,
    adapter_report: dict[str, Any],
    adapter_status: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    release_lot_ids = [
        movement["lotId"] for movement in adapter_report["adapterActions"]["releaseMovements"]
    ]
    replacement_lot_ids = [
        movement["lotId"]
        for movement in adapter_report["adapterActions"]["replacementMovements"]
    ]
    _assert_equal(
        actual=adapter_report["adapterActions"]["adapterReceipt"]["status"],
        expected=expected["adapterReceiptStatus"],
        message=f"{scenario_id}: unexpected substitution adapter receipt status",
    )
    _assert_equal(
        actual=sorted(release_lot_ids),
        expected=sorted(expected["adapterReleaseLotIds"]),
        message=f"{scenario_id}: incumbent release scope drifted from the expected adapter path",
    )
    _assert_equal(
        actual=sorted(replacement_lot_ids),
        expected=sorted(expected["adapterReplacementLotIds"]),
        message=f"{scenario_id}: replacement move scope drifted from the expected adapter path",
    )
    _assert_equal(
        actual=adapter_report["workflowConfirmation"]["substitutionStateAfterConfirmation"],
        expected=expected["adapterSubstitutionStateAfterConfirmation"],
        message=f"{scenario_id}: unexpected substitution state after adapter confirmation",
    )
    _assert_equal(
        actual=adapter_report["workflowConfirmation"]["settledInstructionState"],
        expected=expected["adapterSettledInstructionState"],
        message=f"{scenario_id}: unexpected substitution instruction state after adapter confirmation",
    )
    _assert_equal(
        actual=sorted(adapter_report["workflowConfirmation"]["activeEncumberedLotIds"]),
        expected=sorted(expected["finalActiveEncumberedLotIds"]),
        message=f"{scenario_id}: final active encumbrance set drifted from the expected post-substitution state",
    )
    _assert_equal(
        actual=sorted(adapter_report["workflowConfirmation"]["releasedLotIds"]),
        expected=sorted(expected["finalReleasedLotIds"]),
        message=f"{scenario_id}: final released encumbrance set drifted from the expected post-substitution state",
    )
    _assert_equal(
        actual=adapter_status["substitutionState"],
        expected=expected["adapterSubstitutionStateAfterConfirmation"],
        message=f"{scenario_id}: provider-visible substitution state drifted from the adapter report",
    )
    _assert_equal(
        actual=adapter_status["settlementInstructionState"],
        expected=expected["adapterSettledInstructionState"],
        message=f"{scenario_id}: provider-visible instruction state drifted from the adapter report",
    )
    _assert_equal(
        actual=sorted(
            _encumbrance_lot_ids_with_status(
                adapter_status["providerVisibleEncumbrances"],
                "EncumbrancePledged",
            )
        ),
        expected=sorted(expected["finalActiveEncumberedLotIds"]),
        message=f"{scenario_id}: provider-visible active encumbrances drifted from the expected post-substitution set",
    )
    _assert_equal(
        actual=sorted(
            _encumbrance_lot_ids_with_status(
                adapter_status["providerVisibleEncumbrances"],
                "EncumbranceReleased",
            )
        ),
        expected=sorted(expected["finalReleasedLotIds"]),
        message=f"{scenario_id}: provider-visible released encumbrances drifted from the expected post-substitution set",
    )
    _assert_equal(
        actual=len(adapter_status["providerVisibleAdapterReceipts"]),
        expected=1,
        message=f"{scenario_id}: expected exactly one provider-visible substitution adapter receipt",
    )
    _assert_equal(
        actual=sorted(
            holding["lotId"] for holding in adapter_status["providerVisibleCurrentLotHoldings"]
        ),
        expected=sorted(expected["finalCurrentHoldingLotIds"]),
        message=f"{scenario_id}: provider-visible incumbent holding set drifted from the expected post-substitution state",
    )
    _assert_equal(
        actual=sorted(
            holding["lotId"]
            for holding in adapter_status["providerVisibleReplacementLotHoldings"]
        ),
        expected=sorted(expected["finalReplacementHoldingLotIds"]),
        message=f"{scenario_id}: provider-visible replacement holding set drifted from the expected post-substitution state",
    )


def _validate_quickstart_blocked_status(
    *,
    scenario_id: str,
    adapter_status: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    _assert_equal(
        actual=adapter_status["substitutionState"],
        expected=expected["blockedSubstitutionState"],
        message=f"{scenario_id}: unexpected substitution state for blocked Quickstart path",
    )
    _assert_equal(
        actual=sorted(
            _encumbrance_lot_ids_with_status(
                adapter_status["providerVisibleEncumbrances"],
                "EncumbrancePledged",
            )
        ),
        expected=sorted(expected["blockedActiveEncumberedLotIds"]),
        message=f"{scenario_id}: blocked path changed the active encumbrance set unexpectedly",
    )
    _assert_equal(
        actual=sorted(
            _encumbrance_lot_ids_with_status(
                adapter_status["providerVisibleEncumbrances"],
                "EncumbranceReleased",
            )
        ),
        expected=sorted(expected["blockedReleasedLotIds"]),
        message=f"{scenario_id}: blocked path released encumbrances unexpectedly",
    )
    _assert_equal(
        actual=sorted(
            holding["lotId"] for holding in adapter_status["providerVisibleCurrentLotHoldings"]
        ),
        expected=sorted(expected["blockedCurrentHoldingLotIds"]),
        message=f"{scenario_id}: blocked path changed the incumbent holding set unexpectedly",
    )
    _assert_equal(
        actual=sorted(
            holding["lotId"]
            for holding in adapter_status["providerVisibleReplacementLotHoldings"]
        ),
        expected=sorted(expected["blockedReplacementHoldingLotIds"]),
        message=f"{scenario_id}: blocked path created replacement holdings unexpectedly",
    )
    _assert_equal(
        actual=len(adapter_status["providerVisibleAdapterReceipts"]),
        expected=0,
        message=f"{scenario_id}: adapter receipts were emitted even though the substitution was blocked",
    )


def _run_quickstart_seed(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
    quickstart_manifest_path: Path,
) -> Path:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=quickstart_manifest_path,
    )
    _run_command(
        command=[str(repo_root / "scripts/localnet-seed-substitution-demo.sh")],
        env=env,
        cwd=repo_root,
        error_label="localnet-seed-substitution-demo",
    )
    receipt_path = scenario_artifact_dir / "localnet-control-plane-seed-receipt.json"
    if not receipt_path.is_file():
        raise DemoExecutionError(
            "localnet-seed-substitution-demo did not produce "
            + receipt_path.relative_to(repo_root).as_posix()
        )
    return receipt_path


def _run_quickstart_workflow(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
    workflow_input_path: Path,
    workflow_result_path: Path,
) -> dict[str, Any]:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=None,
    )
    _run_command(
        command=[
            str(repo_root / "scripts/localnet-run-substitution-workflow.sh"),
            "--input-file",
            str(workflow_input_path),
            "--output-file",
            str(workflow_result_path),
        ],
        env=env,
        cwd=repo_root,
        error_label="localnet-run-substitution-workflow",
    )
    return _load_json(workflow_result_path)


def _run_quickstart_adapter(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
    adapter_input_path: Path,
    adapter_output_path: Path,
) -> None:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=None,
    )
    _run_command(
        command=[
            str(repo_root / "scripts/localnet-run-substitution-token-adapter.sh"),
            "--input-file",
            str(adapter_input_path),
            "--output-file",
            str(adapter_output_path),
        ],
        env=env,
        cwd=repo_root,
        error_label="localnet-run-substitution-token-adapter",
    )


def _run_quickstart_status(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
    status_output_path: Path,
) -> Path:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=None,
    )
    _run_command(
        command=[
            str(repo_root / "scripts/localnet-substitution-status.sh"),
            "--output-file",
            str(status_output_path),
        ],
        env=env,
        cwd=repo_root,
        error_label="localnet-substitution-status",
    )
    if not status_output_path.is_file():
        raise DemoExecutionError(
            "localnet-substitution-status did not produce "
            + status_output_path.relative_to(repo_root).as_posix()
        )
    return status_output_path


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


def _ide_workflow_timeline_detail(
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


def _quickstart_workflow_timeline_detail(
    scenario_id: str,
    workflow_result: dict[str, Any],
) -> str:
    if workflow_result["substitutionState"] == "PendingSettlement":
        return (
            f"Prepared the Quickstart substitution workflow for scenario {scenario_id} "
            "and exposed the full replacement instruction to the adapter."
        )
    return (
        f"Recorded the Quickstart substitution control failure for scenario {scenario_id} "
        f"with workflow state {workflow_result['substitutionState']}."
    )


def _blocked_phase(
    *,
    scenario_mode: str,
    policy_report: dict[str, Any],
    optimization_report: dict[str, Any] | None,
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
) -> str | None:
    if scenario_mode != "NEGATIVE":
        return None
    if policy_report["overallDecision"] != "ACCEPT":
        return BLOCKING_POLICY
    if optimization_report is None or optimization_report["status"] != "OPTIMAL":
        return BLOCKING_OPTIMIZATION
    if workflow_result is None or adapter_report is None:
        return BLOCKING_WORKFLOW
    return BLOCKING_ADAPTER


def _adapter_outcome(
    *,
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
) -> str | None:
    if workflow_result is None:
        return ADAPTER_NOT_REQUESTED
    if adapter_report is not None:
        return ADAPTER_EXECUTED
    return ADAPTER_BLOCKED


def _encumbrance_lot_ids_with_status(
    encumbrances: list[dict[str, Any]],
    status: str,
) -> list[str]:
    return sorted(
        encumbrance["lotId"]
        for encumbrance in encumbrances
        if encumbrance["status"] == status
    )


def _build_atomicity_evidence(
    *,
    runtime_mode: str,
    scenario_mode: str,
    current_posted_lot_ids: list[str],
    replacement_lot_ids: list[str],
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
    adapter_status: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if runtime_mode == RUNTIME_QUICKSTART:
        if adapter_report is not None and adapter_status is not None:
            return {
                "proofStatus": "ATOMICALLY_COMMITTED",
                "incumbentEncumberedLotIds": current_posted_lot_ids,
                "approvedReplacementLotIds": replacement_lot_ids,
                "adapterActionReleaseLotIds": sorted(
                    movement["lotId"]
                    for movement in adapter_report["adapterActions"]["releaseMovements"]
                ),
                "adapterActionReplacementLotIds": sorted(
                    movement["lotId"]
                    for movement in adapter_report["adapterActions"]["replacementMovements"]
                ),
                "finalReleasedLotIds": sorted(
                    adapter_report["workflowConfirmation"]["releasedLotIds"]
                ),
                "finalActiveEncumberedLotIds": sorted(
                    adapter_report["workflowConfirmation"]["activeEncumberedLotIds"]
                ),
                "providerVisibleCurrentHoldingLotIds": sorted(
                    holding["lotId"]
                    for holding in adapter_status["providerVisibleCurrentLotHoldings"]
                ),
                "providerVisibleReplacementHoldingLotIds": sorted(
                    holding["lotId"]
                    for holding in adapter_status["providerVisibleReplacementLotHoldings"]
                ),
                "providerVisibleAdapterReceiptCount": len(
                    adapter_status["providerVisibleAdapterReceipts"]
                ),
                "note": (
                    "The adapter moved the full incumbent release scope and the full "
                    "replacement scope, then Canton confirmed substitution settlement "
                    "with released incumbent encumbrances and newly pledged replacement encumbrances."
                ),
            }
        if workflow_result is not None and adapter_status is not None and scenario_mode == "NEGATIVE":
            return {
                "proofStatus": "BLOCKED_NO_SIDE_EFFECTS",
                "incumbentEncumberedLotIds": current_posted_lot_ids,
                "approvedReplacementLotIds": replacement_lot_ids,
                "adapterActionReleaseLotIds": [],
                "adapterActionReplacementLotIds": [],
                "finalReleasedLotIds": _encumbrance_lot_ids_with_status(
                    adapter_status["providerVisibleEncumbrances"],
                    "EncumbranceReleased",
                ),
                "finalActiveEncumberedLotIds": _encumbrance_lot_ids_with_status(
                    adapter_status["providerVisibleEncumbrances"],
                    "EncumbrancePledged",
                ),
                "providerVisibleCurrentHoldingLotIds": sorted(
                    holding["lotId"]
                    for holding in adapter_status["providerVisibleCurrentLotHoldings"]
                ),
                "providerVisibleReplacementHoldingLotIds": sorted(
                    holding["lotId"]
                    for holding in adapter_status["providerVisibleReplacementLotHoldings"]
                ),
                "providerVisibleAdapterReceiptCount": len(
                    adapter_status["providerVisibleAdapterReceipts"]
                ),
                "note": (
                    "Quickstart blocked the partial substitution before any adapter "
                    "receipt or replacement movement could commit, and the incumbent "
                    "encumbrance and holding set remained intact."
                ),
            }
        return None

    if workflow_result is None:
        return None
    return {
        "proofStatus": "IDE_LEDGER_WORKFLOW_ONLY",
        "incumbentEncumberedLotIds": current_posted_lot_ids,
        "approvedReplacementLotIds": replacement_lot_ids,
        "adapterActionReleaseLotIds": [],
        "adapterActionReplacementLotIds": [],
        "finalReleasedLotIds": sorted(workflow_result["releasedLotIds"]),
        "finalActiveEncumberedLotIds": sorted(workflow_result["activeEncumberedLotIds"]),
        "providerVisibleCurrentHoldingLotIds": [],
        "providerVisibleReplacementHoldingLotIds": [],
        "providerVisibleAdapterReceiptCount": None,
        "note": (
            "The IDE-ledger path proves workflow-scoped atomic substitution, but it does "
            "not execute the Quickstart adapter release-plus-replacement path."
        ),
    }


def _build_substitution_report(
    *,
    manifest: dict[str, Any],
    manifest_path: Path,
    repo_root: Path,
    output_dir: Path,
    scenario_results: list[dict[str, Any]],
    timeline: list[dict[str, Any]],
    invariant_checks: list[dict[str, Any]],
    runtime_mode: str,
    command_name: str,
) -> dict[str, Any]:
    positive_scenarios = [scenario for scenario in scenario_results if scenario["mode"] == "POSITIVE"]
    negative_scenarios = [scenario for scenario in scenario_results if scenario["mode"] == "NEGATIVE"]
    canonical = json.dumps(
        {
            "manifest": manifest,
            "runtimeMode": runtime_mode,
            "scenarioResults": scenario_results,
        },
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
            "runtimeMode": runtime_mode,
            "command": command_name,
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
    *,
    scenario_results: list[dict[str, Any]],
    runtime_mode: str,
) -> list[dict[str, Any]]:
    positive_scenario = next(
        scenario for scenario in scenario_results if scenario["mode"] == "POSITIVE"
    )
    negative_scenarios = [
        scenario for scenario in scenario_results if scenario["mode"] == "NEGATIVE"
    ]

    if runtime_mode == RUNTIME_QUICKSTART:
        partial_scenario = next(
            scenario
            for scenario in negative_scenarios
            if scenario["scenarioId"] == "negative-partial-substitution-quickstart"
        )
        negative_evidence = _compact_paths(
            path
            for scenario in negative_scenarios
            for path in (
                scenario["policyEvaluationReportPath"],
                scenario["workflowResultPath"],
                scenario["adapterStatusPath"],
            )
        )
        return [
            {
                "invariantId": "PDR-001",
                "status": "PASS",
                "evidence": [positive_scenario["policyEvaluationReportPath"]],
                "note": "The positive Quickstart substitution path used a generated policy-evaluation report derived from declared inputs.",
            },
            {
                "invariantId": "ALLOC-001",
                "status": "PASS",
                "evidence": [positive_scenario["optimizationReportPath"]],
                "note": "The optimizer produced a deterministic replacement recommendation that matched the declared Quickstart substitution seed scope.",
            },
            {
                "invariantId": "WF-001",
                "status": "PASS",
                "evidence": _compact_paths(
                    [
                        positive_scenario["quickstartSeedReceiptPath"],
                        positive_scenario["workflowResultPath"],
                    ]
                ),
                "note": "The Quickstart substitution workflow remained authoritative for incumbent scope, approvals, settlement intent, and final atomic closure.",
            },
            {
                "invariantId": "ADAPT-001",
                "status": "PASS",
                "evidence": _compact_paths(
                    [
                        positive_scenario["workflowResultPath"],
                        positive_scenario["adapterExecutionReportPath"],
                        positive_scenario["adapterStatusPath"],
                    ]
                ),
                "note": "The reference token adapter consumed the Quickstart substitution handoff artifact, executed incumbent release plus replacement movement, and emitted auditable receipts without bypassing workflow authority.",
            },
            {
                "invariantId": "ATOM-001",
                "status": "PASS",
                "evidence": _compact_paths(
                    [
                        positive_scenario["adapterExecutionReportPath"],
                        positive_scenario["adapterStatusPath"],
                        partial_scenario["workflowResultPath"],
                        partial_scenario["adapterStatusPath"],
                    ]
                ),
                "note": "The positive Quickstart path committed the full release-and-replacement scope atomically, and the blocked partial path preserved the incumbent encumbrance and holding state without adapter side effects.",
            },
            {
                "invariantId": "REPT-001",
                "status": "PASS",
                "evidence": _compact_paths(
                    [
                        positive_scenario["policyEvaluationReportPath"],
                        positive_scenario["optimizationReportPath"],
                        positive_scenario["workflowResultPath"],
                        positive_scenario["adapterExecutionReportPath"],
                        positive_scenario["adapterStatusPath"],
                    ]
                ),
                "note": "The Quickstart substitution report references real policy, optimization, workflow, adapter, and status artifacts rather than operator-authored summaries.",
            },
            {
                "invariantId": "EXCP-001",
                "status": "PASS",
                "evidence": negative_evidence,
                "note": "The negative Quickstart substitution scenarios failed deterministically for policy ineligibility and blocked partial substitution without fabricating downstream adapter success.",
            },
        ]

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
            "evidence": _compact_paths(
                [
                    positive_scenario["workflowResultPath"],
                    next(
                        scenario["workflowResultPath"]
                        for scenario in negative_scenarios
                        if scenario["scenarioId"] == "negative-unauthorized-release"
                    ),
                ]
            ),
            "note": "The workflow blocked pre-approval settlement intent creation and blocked the unauthorized release attempt while preserving the current encumbrances.",
        },
        {
            "invariantId": "ATOM-001",
            "status": "PASS",
            "evidence": _compact_paths(
                [
                    positive_scenario["workflowResultPath"],
                    next(
                        scenario["workflowResultPath"]
                        for scenario in negative_scenarios
                        if scenario["scenarioId"] == "negative-partial-substitution"
                    ),
                ]
            ),
            "note": "The positive path replaced encumbrances atomically, and the partial-substitution path failed without releasing the incumbent encumbrances.",
        },
        {
            "invariantId": "REPT-001",
            "status": "PASS",
            "evidence": _compact_paths(
                [
                    positive_scenario["workflowResultPath"],
                    positive_scenario["policyEvaluationReportPath"],
                    positive_scenario["optimizationReportPath"],
                ]
            ),
            "note": "The substitution report references real workflow, policy, and optimizer artifacts rather than operator-authored summaries.",
        },
        {
            "invariantId": "EXCP-001",
            "status": "PASS",
            "evidence": _compact_paths(
                artifact
                for scenario in negative_scenarios
                for artifact in (
                    scenario["policyEvaluationReportPath"],
                    scenario["optimizationReportPath"],
                    scenario["workflowResultPath"],
                )
            ),
            "note": "The negative substitution scenarios failed deterministically for ineligibility, concentration, unauthorized release, and partial-settlement atomicity violations.",
        },
    ]


def _scenario_summary(
    *,
    scenario: dict[str, Any],
    runtime_mode: str,
    policy_report: dict[str, Any],
    optimization_report: dict[str, Any] | None,
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
    adapter_status: dict[str, Any] | None,
) -> str:
    if scenario["mode"] == "POSITIVE":
        assert workflow_result is not None
        if runtime_mode == RUNTIME_QUICKSTART:
            assert adapter_report is not None
            return (
                "Quickstart preserved the incumbent encumbrance set until the full "
                "replacement scope was approved, the adapter released "
                + ", ".join(sorted(m["lotId"] for m in adapter_report["adapterActions"]["releaseMovements"]))
                + " and moved "
                + ", ".join(sorted(m["lotId"] for m in adapter_report["adapterActions"]["replacementMovements"]))
                + ", and Canton closed the substitution atomically."
            )
        assert optimization_report is not None
        return (
            f"Current encumbrances stayed controlled until approval, the optimizer recommended "
            f"{', '.join(workflow_result['replacementLotIds'])}, and the Daml workflow "
            f"closed the substitution atomically against outgoing lots "
            f"{', '.join(workflow_result['releasedLotIds'])}."
        )

    if workflow_result is not None and adapter_status is not None and runtime_mode == RUNTIME_QUICKSTART:
        return (
            "Quickstart blocked the partial substitution before settlement commit, the "
            "incumbent encumbrance set remained "
            + ", ".join(sorted(_encumbrance_lot_ids_with_status(adapter_status["providerVisibleEncumbrances"], "EncumbrancePledged")))
            + ", and the adapter surface remained at "
            + str(len(adapter_status["providerVisibleAdapterReceipts"]))
            + " receipts."
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


def _default_command_name(runtime_mode: str) -> str:
    if runtime_mode == RUNTIME_QUICKSTART:
        return "make demo-substitution-quickstart"
    return "make demo-substitution"


def _default_report_basename(runtime_mode: str) -> str:
    if runtime_mode == RUNTIME_QUICKSTART:
        return "substitution-quickstart"
    return "substitution-demo"


def _write_markdown_summary(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Substitution Demo Summary",
        "",
        f"- Report ID: `{report['substitutionReportId']}`",
        f"- Runtime mode: `{report['demo']['runtimeMode']}`",
        f"- Command: `{report['demo']['command']}`",
        f"- Manifest: `{report['demo']['manifestPath']}`",
        f"- Report artifact: `{report['artifacts']['substitutionReportPath']}`",
        "",
        "## Scenario Outcomes",
        "",
        "| Scenario | Mode | Result | Blocked Phase | Adapter Outcome | Summary |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for scenario in report["scenarios"]:
        lines.append(
            f"| {scenario['scenarioId']} | {scenario['mode']} | {scenario['result']} | "
            f"{scenario['blockedPhase'] or '-'} | {scenario['adapterOutcome'] or '-'} | {scenario['summary']} |"
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
