"""End-to-end margin-call demo orchestration."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


APP_DIR = Path(__file__).resolve().parents[1]
POLICY_ENGINE_DIR = APP_DIR / "policy-engine"
OPTIMIZER_DIR = APP_DIR / "optimizer"
REPO_ROOT_DIR = APP_DIR.parent
QUICKSTART_RUNTIME_DIR = REPO_ROOT_DIR / ".runtime" / "localnet"
QUICKSTART_DEFAULT_WORKDIR = QUICKSTART_RUNTIME_DIR / "cn-quickstart"
QUICKSTART_CONTROL_PLANE_STATE_ROOT = QUICKSTART_RUNTIME_DIR / "control-plane"

for module_dir in (POLICY_ENGINE_DIR, OPTIMIZER_DIR):
    if str(module_dir) not in sys.path:
        sys.path.insert(0, str(module_dir))

from evaluator import evaluate_policy, load_json as load_input_json, write_report as write_policy_report  # noqa: E402
from optimizer import optimize_collateral, write_report as write_optimization_report  # noqa: E402


RUNTIME_IDE_LEDGER = "IDE_LEDGER"
RUNTIME_QUICKSTART = "QUICKSTART"
BLOCKING_POLICY = "POLICY_EVALUATION"
BLOCKING_OPTIMIZATION = "OPTIMIZATION"
BLOCKING_WORKFLOW = "WORKFLOW"
BLOCKING_ADAPTER = "ADAPTER"
ADAPTER_EXECUTED = "EXECUTED"
ADAPTER_BLOCKED = "BLOCKED"
ADAPTER_NOT_REQUESTED = "NOT_REQUESTED"


class DemoExecutionError(RuntimeError):
    """Raised when the demo cannot produce a trustworthy execution report."""


def run_margin_call_demo(
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
        raise DemoExecutionError(f"unsupported margin-call runtime mode {runtime_mode!r}")

    report_stem = report_basename or _default_report_basename(normalized_runtime_mode)
    command = command_name or _default_command_name(normalized_runtime_mode)

    timeline: list[dict[str, Any]] = []
    scenario_results: list[dict[str, Any]] = []

    scenario_entries = manifest["scenarios"]
    for sequence, scenario in enumerate(scenario_entries, start=1):
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
    execution_report = _build_execution_report(
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

    execution_report_path = output_dir_path / f"{report_stem}-execution-report.json"
    summary_path = output_dir_path / f"{report_stem}-summary.md"
    timeline_path = output_dir_path / f"{report_stem}-timeline.md"

    execution_report["artifacts"] = {
        "executionReportPath": _relative_path(execution_report_path, repo_root_path),
        "markdownSummaryPath": _relative_path(summary_path, repo_root_path),
        "timelinePath": _relative_path(timeline_path, repo_root_path),
    }

    _write_json(execution_report_path, execution_report)
    _validate_json_schema(
        report_path=execution_report_path,
        schema_path=repo_root_path / "reports/schemas/execution-report.schema.json",
    )

    _write_markdown_summary(summary_path, execution_report)
    _write_timeline_markdown(timeline_path, execution_report)

    return execution_report


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
            f"Evaluated candidate inventory for {scenario_mode.lower()} scenario "
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
                f"Optimized collateral for scenario {scenario_id} with "
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
                detail=(
                    f"Recorded the Daml margin-call and posting path for scenario "
                    f"{scenario_id}."
                ),
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
                    f"Seeded or reused the declared Quickstart scenario for {scenario_id} "
                    f"before workflow execution."
                ),
            )

            seed_receipt = _load_json(quickstart_seed_receipt_path)
            workflow_request = _build_quickstart_workflow_request(
                scenario=scenario,
                obligation=obligation,
                optimization_report=optimization_report,
                seed_receipt=seed_receipt,
            )
            _write_json(workflow_input_path, workflow_request)

            workflow_started_at = _utc_now()
            workflow_result = _run_quickstart_margin_call_workflow(
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
                detail=(
                    f"Advanced the Quickstart margin-call workflow for scenario "
                    f"{scenario_id} through gate {workflow_request['workflowGate']}."
                ),
            )
            _validate_quickstart_workflow_result(
                scenario_id=scenario_id,
                workflow_result=workflow_result,
                expected=expected,
            )

            if scenario.get("runAdapter", False):
                adapter_started_at = _utc_now()
                adapter_execution_report_path = _run_quickstart_token_adapter(
                    repo_root=repo_root,
                    scenario_artifact_dir=quickstart_artifact_dir,
                    scenario_state_dir=quickstart_state_dir,
                )
                adapter_finished_at = _utc_now()
                adapter_status_path = quickstart_artifact_dir / "localnet-reference-token-adapter-status.json"
                adapter_report = _load_json(adapter_execution_report_path)
                adapter_status = _load_json(adapter_status_path)
                _validate_json_schema(
                    report_path=adapter_execution_report_path,
                    schema_path=repo_root / "reports/schemas/adapter-execution-report.schema.json",
                )
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
                        f"Executed the reference token adapter for scenario {scenario_id} "
                        f"and confirmed workflow settlement on Quickstart."
                    ),
                )
                _validate_adapter_result(
                    scenario_id=scenario_id,
                    adapter_report=adapter_report,
                    adapter_status=adapter_status,
                    expected=expected,
                )
            else:
                adapter_status_started_at = _utc_now()
                adapter_status_path = _run_quickstart_adapter_status(
                    repo_root=repo_root,
                    scenario_artifact_dir=quickstart_artifact_dir,
                    scenario_state_dir=quickstart_state_dir,
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
                        f"the workflow ended in posting state {workflow_result['postingState']}."
                    ),
                )
                _validate_adapter_blocked_status(
                    scenario_id=scenario_id,
                    adapter_status=adapter_status,
                    expected=expected,
                )

    observed_reason_codes = sorted(
        set(_policy_reason_codes(policy_report))
        | set(_optimization_reason_codes(optimization_report))
        | set(_workflow_reason_codes(workflow_result))
    )
    _assert_reason_codes(
        scenario_id=scenario_id,
        observed_reason_codes=observed_reason_codes,
        expected_reason_codes=expected.get("reasonCodes", []),
    )

    result_kind = "SUCCESS" if scenario_mode == "POSITIVE" else "EXPECTED_FAILURE"
    summary = _scenario_summary(
        scenario=scenario,
        policy_report=policy_report,
        optimization_report=optimization_report,
        workflow_result=workflow_result,
        adapter_report=adapter_report,
        adapter_status=adapter_status,
    )

    scenario_result = {
        "scenarioId": scenario_id,
        "mode": scenario_mode,
        "description": scenario["description"],
        "result": result_kind,
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
        "workflowRuntime": (
            None if workflow_result is None else runtime_mode
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
        "selectedLotIds": (
            []
            if optimization_report is None or optimization_report["recommendedPortfolio"] is None
            else optimization_report["recommendedPortfolio"]["lotIds"]
        ),
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
        "workflow": workflow_result,
    }
    return scenario_result


def _build_execution_report(
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
    primary_policy_ref = (
        positive_scenarios[0]["policyEvaluationReportPath"] if positive_scenarios else None
    )

    return {
        "$schema": "../../reports/schemas/execution-report.schema.json",
        "reportType": "ExecutionReport",
        "reportVersion": "0.1.0",
        "executionId": f"exr-{digest[:16]}",
        "generatedAt": _utc_now(),
        "overallStatus": "PASS",
        "demo": {
            "demoId": manifest["demoId"],
            "demoVersion": manifest["demoVersion"],
            "runtimeMode": runtime_mode,
            "command": command_name,
            "manifestPath": _relative_path(manifest_path, repo_root),
            "outputDirectory": _relative_path(output_dir, repo_root),
            "primaryPolicyEvaluationArtifact": primary_policy_ref,
            "scenarioCount": len(scenario_results),
            "positiveScenarioCount": len(positive_scenarios),
            "negativeScenarioCount": len(negative_scenarios),
        },
        "artifacts": {},
        "scenarios": scenario_results,
        "timeline": timeline,
        "invariantChecks": invariant_checks,
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
    recommended_portfolio = optimization_report["recommendedPortfolio"]
    if recommended_portfolio is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: workflow requested without a recommended portfolio"
        )

    inventory_by_lot_id = {lot["lotId"]: lot for lot in inventory["candidateLots"]}
    workflow_config = scenario["workflow"]
    selected_lot_inputs = []
    for lot_id in recommended_portfolio["lotIds"]:
        lot = inventory_by_lot_id[lot_id]
        quantity = lot.get("nominalValue", lot.get("marketValue"))
        if quantity is None:
            raise DemoExecutionError(
                f"{scenario['scenarioId']}: lot {lot_id} lacks nominalValue and marketValue"
            )
        selected_lot_inputs.append(
            {
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
        "dueAt": workflow_config["dueAt"],
        "selectedLots": selected_lot_inputs,
    }


def _build_quickstart_workflow_request(
    *,
    scenario: dict[str, Any],
    obligation: dict[str, Any],
    optimization_report: dict[str, Any],
    seed_receipt: dict[str, Any],
) -> dict[str, Any]:
    recommended_portfolio = optimization_report["recommendedPortfolio"]
    if recommended_portfolio is None:
        raise DemoExecutionError(
            f"{scenario['scenarioId']}: Quickstart workflow requested without a recommended portfolio"
        )

    selected_lot_ids = recommended_portfolio["lotIds"]
    seeded_lot_ids = [lot["lotId"] for lot in seed_receipt["inventoryLots"]]
    _assert_equal(
        actual=sorted(selected_lot_ids),
        expected=sorted(seeded_lot_ids),
        message=(
            f"{scenario['scenarioId']}: optimizer-selected lots drifted from the declared "
            "Quickstart seed scenario"
        ),
    )
    _assert_equal(
        actual=obligation["obligationId"],
        expected=seed_receipt["obligationId"],
        message=f"{scenario['scenarioId']}: obligation id drifted from the Quickstart seed receipt",
    )

    return {
        "scenarioId": scenario["scenarioId"],
        "obligationId": seed_receipt["obligationId"],
        "postingId": seed_receipt["postingId"],
        "providerParty": seed_receipt["providerParty"],
        "securedParty": seed_receipt["securedParty"],
        "custodianParty": seed_receipt["custodianParty"],
        "selectedLotIds": selected_lot_ids,
        "workflowGate": scenario["workflowGate"],
    }


def _run_daml_workflow(
    *,
    script_name: str,
    input_path: Path,
    output_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    daml_bin = os.environ.get("DAML_BIN")
    if not daml_bin:
        raise DemoExecutionError(
            "DAML_BIN is not set; run the demo through the Makefile after bootstrap"
        )

    dar_file = _find_dar(repo_root)
    command = [
        daml_bin,
        "script",
        "--dar",
        str(dar_file),
        "--script-name",
        script_name,
        "--input-file",
        str(input_path),
        "--output-file",
        str(output_path),
        "--ide-ledger",
    ]
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise DemoExecutionError(
            "daml workflow execution failed:\n"
            + completed.stdout
            + completed.stderr
        )
    return _load_json(output_path)


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
        command=[str(repo_root / "scripts/localnet-seed-demo.sh")],
        env=env,
        cwd=repo_root,
        error_label="localnet-seed-demo",
    )
    receipt_path = scenario_artifact_dir / "localnet-control-plane-seed-receipt.json"
    if not receipt_path.is_file():
        raise DemoExecutionError(
            f"localnet-seed-demo did not produce {receipt_path.relative_to(repo_root).as_posix()}"
        )
    return receipt_path


def _run_quickstart_margin_call_workflow(
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
            str(repo_root / "scripts/localnet-run-margin-call-workflow.sh"),
            "--input-file",
            str(workflow_input_path),
            "--output-file",
            str(workflow_result_path),
        ],
        env=env,
        cwd=repo_root,
        error_label="localnet-run-margin-call-workflow",
    )
    return _load_json(workflow_result_path)


def _run_quickstart_adapter_status(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
) -> Path:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=None,
    )
    _run_command(
        command=[str(repo_root / "scripts/localnet-adapter-status.sh")],
        env=env,
        cwd=repo_root,
        error_label="localnet-adapter-status",
    )
    status_path = scenario_artifact_dir / "localnet-reference-token-adapter-status.json"
    if not status_path.is_file():
        raise DemoExecutionError(
            f"localnet-adapter-status did not produce {status_path.relative_to(repo_root).as_posix()}"
        )
    return status_path


def _run_quickstart_token_adapter(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
) -> Path:
    env = _localnet_env(
        repo_root=repo_root,
        scenario_artifact_dir=scenario_artifact_dir,
        scenario_state_dir=scenario_state_dir,
        quickstart_manifest_path=None,
    )
    _run_command(
        command=[str(repo_root / "scripts/localnet-run-token-adapter.sh")],
        env=env,
        cwd=repo_root,
        error_label="localnet-run-token-adapter",
    )
    report_path = scenario_artifact_dir / "localnet-reference-token-adapter-execution-report.json"
    if not report_path.is_file():
        raise DemoExecutionError(
            "localnet-run-token-adapter did not produce "
            + report_path.relative_to(repo_root).as_posix()
        )
    return report_path


def _localnet_env(
    *,
    repo_root: Path,
    scenario_artifact_dir: Path,
    scenario_state_dir: Path,
    quickstart_manifest_path: Path | None,
) -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("LOCALNET_WORKDIR", str(QUICKSTART_DEFAULT_WORKDIR))
    env.setdefault("LOCALNET_PROFILE", "lean")
    env.setdefault("LOCALNET_PARTY_HINT", "canton-collateral-1")
    env["LOCALNET_CONTROL_PLANE_OUTPUT_DIR"] = str(scenario_artifact_dir)
    env["LOCALNET_CONTROL_PLANE_STATE_DIR"] = str(scenario_state_dir)
    if quickstart_manifest_path is not None:
        env["LOCALNET_SCENARIO_MANIFEST"] = str(quickstart_manifest_path)
    return env


def _run_command(
    *,
    command: list[str],
    env: dict[str, str],
    cwd: Path,
    error_label: str,
) -> None:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    if completed.returncode != 0:
        raise DemoExecutionError(
            f"{error_label} failed:\n{completed.stdout}{completed.stderr}"
        )


def _default_command_name(runtime_mode: str) -> str:
    if runtime_mode == RUNTIME_QUICKSTART:
        return "make demo-margin-call-quickstart"
    return "make demo-margin-call"


def _default_report_basename(runtime_mode: str) -> str:
    if runtime_mode == RUNTIME_QUICKSTART:
        return "margin-call-quickstart"
    return "margin-call-demo"


def _find_dar(repo_root: Path) -> Path:
    dar_files = sorted((repo_root / ".daml/dist").glob("*.dar"))
    if not dar_files:
        raise DemoExecutionError("No DAR file found under .daml/dist; run daml-build first")
    return dar_files[0]


def _validate_ide_workflow_result(
    *,
    scenario_id: str,
    workflow_result: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    _assert_equal(
        actual=workflow_result["marginCallState"],
        expected=expected["workflowMarginCallState"],
        message=f"{scenario_id}: unexpected margin call workflow state",
    )
    _assert_equal(
        actual=workflow_result["postingState"],
        expected=expected["workflowPostingState"],
        message=f"{scenario_id}: unexpected posting workflow state",
    )
    _assert_equal(
        actual=sorted(workflow_result["selectedLotIds"]),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: workflow selected lots drifted from the expected allocation",
    )
    _assert_equal(
        actual=sorted(workflow_result["encumberedLotIds"]),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: workflow encumbered lots drifted from the expected allocation",
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
        actual=workflow_result["marginCallState"],
        expected=expected["workflowMarginCallState"],
        message=f"{scenario_id}: unexpected Quickstart margin-call state",
    )
    _assert_equal(
        actual=workflow_result["postingState"],
        expected=expected["workflowPostingState"],
        message=f"{scenario_id}: unexpected Quickstart posting state",
    )
    _assert_equal(
        actual=workflow_result["workflowGate"],
        expected=expected["workflowGate"],
        message=f"{scenario_id}: unexpected Quickstart workflow gate outcome",
    )
    _assert_equal(
        actual=sorted(workflow_result["selectedLotIds"]),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: Quickstart workflow selected lots drifted from the optimizer recommendation",
    )
    _assert_equal(
        actual=workflow_result.get("settlementInstructionState"),
        expected=expected.get("workflowSettlementInstructionState"),
        message=f"{scenario_id}: unexpected settlement instruction state",
    )
    if workflow_result["executionReportCount"] < expected["minimumExecutionReportCount"]:
        raise DemoExecutionError(
            f"{scenario_id}: expected at least {expected['minimumExecutionReportCount']} "
            f"Quickstart execution reports but found {workflow_result['executionReportCount']}"
        )


def _validate_adapter_result(
    *,
    scenario_id: str,
    adapter_report: dict[str, Any],
    adapter_status: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    movement_lot_ids = [
        movement["lotId"] for movement in adapter_report["adapterReceipt"]["movements"]
    ]
    encumbered_lot_ids = [
        encumbrance["lotId"] for encumbrance in adapter_report["encumbranceContextAfter"]
    ]
    _assert_equal(
        actual=adapter_report["workflowConfirmation"]["postingStateAfterConfirmation"],
        expected=expected["adapterPostingStateAfterConfirmation"],
        message=f"{scenario_id}: unexpected posting state after adapter confirmation",
    )
    _assert_equal(
        actual=adapter_report["workflowConfirmation"]["settledInstructionState"],
        expected=expected["adapterSettledInstructionState"],
        message=f"{scenario_id}: unexpected settled instruction state after adapter confirmation",
    )
    _assert_equal(
        actual=adapter_report["adapterReceipt"]["status"],
        expected=expected["adapterReceiptStatus"],
        message=f"{scenario_id}: unexpected adapter receipt status",
    )
    _assert_equal(
        actual=sorted(movement_lot_ids),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: adapter moved an unexpected lot set",
    )
    _assert_equal(
        actual=len(adapter_report["adapterReceipt"]["movements"]),
        expected=expected["adapterMovementCount"],
        message=f"{scenario_id}: unexpected adapter movement count",
    )
    _assert_equal(
        actual=sorted(encumbered_lot_ids),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: adapter-created encumbrances drifted from the expected lot set",
    )
    _assert_equal(
        actual=adapter_status["postingState"],
        expected=expected["adapterPostingStateAfterConfirmation"],
        message=f"{scenario_id}: provider-visible posting state drifted from the adapter report",
    )
    _assert_equal(
        actual=adapter_status["settlementInstructionState"],
        expected=expected["adapterSettledInstructionState"],
        message=f"{scenario_id}: provider-visible settlement instruction state drifted from the adapter report",
    )
    _assert_equal(
        actual=len(adapter_status["providerVisibleAdapterReceipts"]),
        expected=1,
        message=f"{scenario_id}: expected exactly one provider-visible adapter receipt",
    )
    _assert_equal(
        actual=sorted(
            holding["lotId"] for holding in adapter_status["providerVisibleReferenceTokenHoldings"]
        ),
        expected=sorted(expected["selectedLotIds"]),
        message=f"{scenario_id}: provider-visible reference token holdings drifted from the expected lot set",
    )


def _validate_adapter_blocked_status(
    *,
    scenario_id: str,
    adapter_status: dict[str, Any],
    expected: dict[str, Any],
) -> None:
    _assert_equal(
        actual=adapter_status["postingState"],
        expected=expected["adapterBlockedPostingState"],
        message=f"{scenario_id}: unexpected posting state for blocked adapter path",
    )
    _assert_equal(
        actual=len(adapter_status["providerVisibleAdapterReceipts"]),
        expected=0,
        message=f"{scenario_id}: adapter receipts were emitted even though the path was blocked",
    )
    _assert_equal(
        actual=len(adapter_status["providerVisibleReferenceTokenHoldings"]),
        expected=0,
        message=f"{scenario_id}: adapter holdings were created even though the path was blocked",
    )
    _assert_equal(
        actual=adapter_status["providerVisibleEncumbranceCount"],
        expected=0,
        message=f"{scenario_id}: encumbrances were created even though the adapter path was blocked",
    )


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
    negative_evidence = _compact_paths(
        path
        for scenario in negative_scenarios
        for path in (
            scenario["policyEvaluationReportPath"],
            scenario["workflowResultPath"],
            scenario["adapterStatusPath"],
        )
    )

    if runtime_mode == RUNTIME_QUICKSTART:
        return [
            {
                "invariantId": "PDR-001",
                "status": "PASS",
                "evidence": [positive_scenario["policyEvaluationReportPath"]],
                "note": "The positive Quickstart path policy report was generated from declared policy and inventory inputs.",
            },
            {
                "invariantId": "ALLOC-001",
                "status": "PASS",
                "evidence": [positive_scenario["optimizationReportPath"]],
                "note": "The optimizer produced a deterministic selected-lot recommendation that matched the declared Quickstart seed scenario.",
            },
            {
                "invariantId": "WF-001",
                "status": "PASS",
                "evidence": _compact_paths(
                    [
                        positive_scenario["quickstartSeedReceiptPath"],
                        positive_scenario["workflowResultPath"],
                        positive_scenario["adapterExecutionReportPath"],
                    ]
                ),
                "note": "The Quickstart-backed workflow issued the call, prepared the settlement instruction, and then closed the posting path only through Canton workflow confirmation.",
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
                "note": "The reference token adapter consumed the Quickstart workflow handoff artifact, executed the asset-side move, and emitted auditable receipts without bypassing workflow authority.",
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
                "note": "The Quickstart execution report references real policy, optimization, workflow, and adapter artifacts rather than operator-authored placeholders.",
            },
            {
                "invariantId": "EXCP-001",
                "status": "PASS",
                "evidence": negative_evidence,
                "note": "The negative Quickstart scenarios blocked either before workflow execution or at workflow gating and did not fabricate downstream adapter success.",
            },
        ]

    return [
        {
            "invariantId": "PDR-001",
            "status": "PASS",
            "evidence": [positive_scenario["policyEvaluationReportPath"]],
            "note": "The positive path policy report was generated from declared policy and inventory inputs.",
        },
        {
            "invariantId": "ALLOC-001",
            "status": "PASS",
            "evidence": [positive_scenario["optimizationReportPath"]],
            "note": "The optimizer produced a deterministic selected-lot recommendation with an explanation trace.",
        },
        {
            "invariantId": "WF-001",
            "status": "PASS",
            "evidence": [positive_scenario["workflowResultPath"]],
            "note": "The Daml workflow closed the margin-call issuance and collateral-posting path through committed choices.",
        },
        {
            "invariantId": "REPT-001",
            "status": "PASS",
            "evidence": [
                positive_scenario["workflowResultPath"],
                positive_scenario["policyEvaluationReportPath"],
                positive_scenario["optimizationReportPath"],
            ],
            "note": "The execution report references real workflow, policy, and optimization artifacts rather than operator-authored placeholders.",
        },
        {
            "invariantId": "EXCP-001",
            "status": "PASS",
            "evidence": [scenario["policyEvaluationReportPath"] for scenario in negative_scenarios],
            "note": "The negative scenarios fail with explicit reason codes for ineligible collateral, insufficient lendable value, and an expired policy window.",
        },
    ]


def _scenario_summary(
    *,
    scenario: dict[str, Any],
    policy_report: dict[str, Any],
    optimization_report: dict[str, Any] | None,
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
    adapter_status: dict[str, Any] | None,
) -> str:
    if scenario["mode"] == "POSITIVE":
        assert optimization_report is not None
        assert workflow_result is not None
        if adapter_report is not None:
            return (
                f"Policy accepted the candidate set, the optimizer recommended "
                f"{optimization_report['recommendedAction']}, the Quickstart workflow issued "
                f"the call and prepared a settlement instruction, and the reference token "
                f"adapter settled lots {', '.join(workflow_result['selectedLotIds'])}."
            )
        return (
            f"Policy accepted the candidate set, the optimizer recommended "
            f"{optimization_report['recommendedAction']}, and the Daml workflow "
            f"closed the margin-call and posting path for lots "
            f"{', '.join(workflow_result['selectedLotIds'])}."
        )

    if workflow_result is not None:
        return (
            f"Policy and optimization stayed admissible, but the Quickstart workflow "
            f"blocked the path in posting state {workflow_result['postingState']} and the "
            f"adapter surface remained at {len(adapter_status['providerVisibleAdapterReceipts']) if adapter_status else 0} receipts."
        )

    if optimization_report is None:
        return (
            f"Policy evaluation blocked the scenario with decision "
            f"{policy_report['overallDecision']} and reason codes "
            f"{', '.join(_policy_reason_codes(policy_report))}."
        )

    return (
        f"Policy evaluation stayed admissible at the lot level, but optimization "
        f"ended with {optimization_report['status']} and reason codes "
        f"{', '.join(_optimization_reason_codes(optimization_report))}."
    )


def _policy_reason_codes(policy_report: dict[str, Any]) -> list[str]:
    reason_codes = {
        reason["code"] for reason in policy_report["portfolioReasons"] if reason is not None
    }
    for asset in policy_report["assetResults"]:
        reason_codes.update(reason["code"] for reason in asset["reasons"])
    return sorted(reason_codes)


def _optimization_reason_codes(optimization_report: dict[str, Any] | None) -> list[str]:
    if optimization_report is None:
        return []
    recommended_portfolio = optimization_report["recommendedPortfolio"]
    if recommended_portfolio is not None:
        return sorted(recommended_portfolio["blockingReasonCodes"])
    current_portfolio = optimization_report["currentPortfolio"]
    if current_portfolio is not None:
        return sorted(current_portfolio["blockingReasonCodes"])
    decision_trace = next(
        (
            trace
            for trace in optimization_report["explanationTrace"]
            if trace["stage"] == "DECISION"
        ),
        None,
    )
    if decision_trace and decision_trace["reasonCodes"]:
        return sorted(set(decision_trace["reasonCodes"]))

    trace_reason_codes = sorted(
        set(
            code
            for trace in optimization_report["explanationTrace"]
            for code in trace["reasonCodes"]
        )
    )
    if "INSUFFICIENT_LENDABLE_VALUE" in trace_reason_codes:
        return ["INSUFFICIENT_LENDABLE_VALUE"]
    return trace_reason_codes


def _workflow_reason_codes(workflow_result: dict[str, Any] | None) -> list[str]:
    if workflow_result is None:
        return []
    if workflow_result.get("postingState") == "Rejected":
        return ["WORKFLOW_REJECTED"]
    return []


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
    if optimization_report is not None and optimization_report["status"] != "OPTIMAL":
        return BLOCKING_OPTIMIZATION
    if workflow_result is not None and workflow_result["postingState"] != "PendingSettlement":
        return BLOCKING_WORKFLOW
    if workflow_result is not None and adapter_report is None:
        return BLOCKING_ADAPTER
    return None


def _adapter_outcome(
    *,
    workflow_result: dict[str, Any] | None,
    adapter_report: dict[str, Any] | None,
) -> str | None:
    if workflow_result is None:
        return None
    if adapter_report is not None:
        return ADAPTER_EXECUTED
    if workflow_result.get("postingState") != "PendingSettlement":
        return ADAPTER_BLOCKED
    return ADAPTER_NOT_REQUESTED


def _append_timeline(
    *,
    timeline: list[dict[str, Any]],
    sequence: int,
    scenario_id: str,
    phase: str,
    status: str,
    started_at: str,
    finished_at: str,
    artifact_path: str | None,
    detail: str,
) -> None:
    timeline.append(
        {
            "sequence": len(timeline) + 1,
            "scenarioSequence": sequence,
            "scenarioId": scenario_id,
            "phase": phase,
            "status": status,
            "startedAt": started_at,
            "finishedAt": finished_at,
            "artifactPath": artifact_path,
            "detail": detail,
        }
    )


def _write_markdown_summary(path: Path, execution_report: dict[str, Any]) -> None:
    lines = [
        "# Margin Call Demo Summary",
        "",
        "## Overview",
        "",
        f"- Execution report: `{execution_report['artifacts']['executionReportPath']}`",
        f"- Runtime mode: `{execution_report['demo']['runtimeMode']}`",
        f"- Scenario count: `{execution_report['demo']['scenarioCount']}`",
        f"- Primary policy evaluation artifact: `{execution_report['demo']['primaryPolicyEvaluationArtifact']}`",
        "",
        "## Scenario Results",
        "",
        "| Scenario | Mode | Result | Summary |",
        "| --- | --- | --- | --- |",
    ]

    for scenario in execution_report["scenarios"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    scenario["scenarioId"],
                    scenario["mode"],
                    scenario["result"],
                    scenario["summary"],
                ]
            )
            + " |"
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

    for invariant in execution_report["invariantChecks"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    invariant["invariantId"],
                    invariant["status"],
                    ", ".join(f"`{item}`" for item in invariant["evidence"]),
                    invariant["note"],
                ]
            )
            + " |"
        )

    positive_scenario = next(
        scenario for scenario in execution_report["scenarios"] if scenario["mode"] == "POSITIVE"
    )
    lines.extend(
        [
            "",
            "## Positive Path",
            "",
            f"- Recommended action: `{positive_scenario['recommendedAction']}`",
            f"- Selected lots: `{', '.join(positive_scenario['selectedLotIds'])}`",
            f"- Workflow result artifact: `{positive_scenario['workflowResultPath']}`",
        ]
    )
    if positive_scenario["adapterExecutionReportPath"] is not None:
        lines.append(
            f"- Adapter result artifact: `{positive_scenario['adapterExecutionReportPath']}`"
        )
    if positive_scenario["adapterStatusPath"] is not None:
        lines.append(f"- Adapter status artifact: `{positive_scenario['adapterStatusPath']}`")
    if positive_scenario["quickstartSeedReceiptPath"] is not None:
        lines.append(
            f"- Quickstart seed receipt: `{positive_scenario['quickstartSeedReceiptPath']}`"
        )
    lines.append("")

    _write_text(path, "\n".join(lines) + "\n")


def _write_timeline_markdown(path: Path, execution_report: dict[str, Any]) -> None:
    lines = [
        "# Margin Call Demo Timeline",
        "",
        "## Execution Phases",
        "",
        "| Seq | Scenario | Phase | Status | Artifact | Detail |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for event in execution_report["timeline"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(event["sequence"]),
                    event["scenarioId"],
                    event["phase"],
                    event["status"],
                    "" if event["artifactPath"] is None else f"`{event['artifactPath']}`",
                    event["detail"],
                ]
            )
            + " |"
        )

    positive_scenario = next(
        scenario for scenario in execution_report["scenarios"] if scenario["mode"] == "POSITIVE"
    )
    workflow = positive_scenario["workflow"]
    if workflow is not None:
        lines.extend(
            [
                "",
                "## Positive Workflow Steps",
                "",
                "| Step | Phase | Actor | State | Detail |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for step in workflow["steps"]:
            lines.append(
                "| "
                + " | ".join(
                    [
                        str(step["step"]),
                        step["phase"],
                        step["actor"],
                        step["state"],
                        step["detail"],
                    ]
                )
                + " |"
            )

    _write_text(path, "\n".join(lines) + "\n")


def _validate_json_schema(*, report_path: Path, schema_path: Path) -> None:
    check_jsonschema_bin = os.environ.get("CHECK_JSONSCHEMA_BIN")
    if not check_jsonschema_bin:
        raise DemoExecutionError(
            "CHECK_JSONSCHEMA_BIN is not set; run the demo through the Makefile after bootstrap"
        )
    completed = subprocess.run(
        [check_jsonschema_bin, "--schemafile", str(schema_path), str(report_path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise DemoExecutionError(
            f"schema validation failed for {report_path}:\n"
            + completed.stdout
            + completed.stderr
        )


def _assert_equal(*, actual: Any, expected: Any, message: str) -> None:
    if actual != expected:
        raise DemoExecutionError(f"{message}: expected {expected!r}, found {actual!r}")


def _assert_reason_codes(
    *,
    scenario_id: str,
    observed_reason_codes: list[str],
    expected_reason_codes: list[str],
) -> None:
    missing_codes = sorted(set(expected_reason_codes) - set(observed_reason_codes))
    if missing_codes:
        raise DemoExecutionError(
            f"{scenario_id}: expected reason codes were not observed: {', '.join(missing_codes)}"
        )


def _compact_paths(paths: list[str | None] | Any) -> list[str]:
    if not isinstance(paths, list):
        paths = list(paths)
    return [path for path in paths if path is not None]


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve_scenario_path(manifest_path: Path, relative_path: str) -> Path:
    return (manifest_path.parent / relative_path).resolve()


def _relative_path(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root).as_posix()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)
        handle.write("\n")


def _write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


def _load_json(path: str | Path) -> dict[str, Any]:
    return load_input_json(path)
