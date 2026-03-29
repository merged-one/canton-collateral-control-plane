"""Build the final end-to-end demo pack from the conformance suite output."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from margin_call_demo import DemoExecutionError, _load_json, _relative_path, _utc_now, _write_json, _write_text


def build_final_demo_pack(
    *,
    conformance_report_path: str | Path,
    output_dir: str | Path,
    repo_root: str | Path,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root).resolve()
    output_dir_path = Path(output_dir).resolve()
    output_dir_path.mkdir(parents=True, exist_ok=True)

    conformance_report = _load_json(_resolve_path(repo_root_path, conformance_report_path))
    if conformance_report["overallStatus"] != "PASS":
        raise DemoExecutionError(
            "The conformance suite must pass before the final demo pack can be built."
        )

    demo_reports = [
        _load_json(repo_root_path / demo_report["reportPath"])
        for demo_report in conformance_report["demoReports"]
    ]

    final_pack_path = output_dir_path / "final-demo-pack.json"
    summary_path = output_dir_path / "final-demo-pack-summary.md"
    machine_readable_artifacts = _machine_readable_artifacts(
        repo_root=repo_root_path,
        conformance_report=conformance_report,
        demo_reports=demo_reports,
    )
    human_readable_artifacts = _human_readable_artifacts(
        conformance_report=conformance_report,
        demo_reports=demo_reports,
    )
    integration_surfaces = _integration_surfaces()

    pack = {
        "reportType": "FinalDemoPack",
        "reportVersion": "0.1.0",
        "demoPackId": _demo_pack_id(
            conformance_report=conformance_report,
            demo_reports=demo_reports,
            integration_surfaces=integration_surfaces,
        ),
        "generatedAt": _utc_now(),
        "overallStatus": "PASS",
        "command": "make demo-all",
        "artifacts": {
            "finalDemoPackPath": _relative_path(final_pack_path, repo_root_path),
            "markdownSummaryPath": _relative_path(summary_path, repo_root_path),
            "conformanceReportPath": conformance_report["artifacts"]["conformanceReportPath"],
            "conformanceSummaryPath": conformance_report["artifacts"]["markdownSummaryPath"],
            "demoArtifactIndexPath": "docs/evidence/DEMO_ARTIFACT_INDEX.md",
            "integrationGuidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
            "runbookPath": "docs/runbooks/FINAL_DEMO_RUNBOOK.md",
        },
        "commandSurface": [
            "make demo-margin-call",
            "make demo-substitution",
            "make demo-return",
            "make test-conformance",
            "make demo-all",
            "make verify-portable",
            "make verify",
        ],
        "demoFlows": [
            _demo_flow_entry(demo_report_entry, report)
            for demo_report_entry, report in zip(
                conformance_report["demoReports"], demo_reports, strict=True
            )
        ],
        "invariantOutput": {
            "checkCount": conformance_report["coverage"]["completedCheckCount"],
            "passedCheckCount": conformance_report["coverage"]["passedCheckCount"],
            "failedCheckCount": conformance_report["coverage"]["failedCheckCount"],
            "conformanceChecks": conformance_report["checks"],
        },
        "machineReadableArtifacts": machine_readable_artifacts,
        "humanReadableArtifacts": human_readable_artifacts,
        "integrationSurfaces": integration_surfaces,
    }

    pack["machineReadableArtifacts"] = sorted(
        set(pack["machineReadableArtifacts"])
        | {_relative_path(final_pack_path, repo_root_path)}
    )
    pack["humanReadableArtifacts"] = sorted(
        set(pack["humanReadableArtifacts"])
        | {_relative_path(summary_path, repo_root_path)}
    )

    _write_json(final_pack_path, pack)
    _write_text(summary_path, _render_final_demo_summary(pack))
    return pack


def _demo_flow_entry(demo_report_entry: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    return {
        "demoType": demo_report_entry["demoType"],
        "reportType": demo_report_entry["reportType"],
        "command": demo_report_entry["command"],
        "overallStatus": report["overallStatus"],
        "reportPath": demo_report_entry["reportPath"],
        "summaryPath": demo_report_entry["summaryPath"],
        "timelinePath": demo_report_entry["timelinePath"],
        "positiveScenarioIds": demo_report_entry["positiveScenarioIds"],
        "negativeScenarioIds": demo_report_entry["negativeScenarioIds"],
    }


def _machine_readable_artifacts(
    *,
    repo_root: Path,
    conformance_report: dict[str, Any],
    demo_reports: list[dict[str, Any]],
) -> list[str]:
    artifacts = {
        conformance_report["artifacts"]["conformanceReportPath"],
        conformance_report["artifacts"]["eligibilityDeterminismArtifactPath"],
        conformance_report["artifacts"]["haircutVectorArtifactPath"],
    }

    for demo_report in demo_reports:
        for value in demo_report["artifacts"].values():
            if value is not None and value.endswith(".json"):
                artifacts.add(value)
        for scenario in demo_report["scenarios"]:
            for field in (
                "policyEvaluationReportPath",
                "optimizationReportPath",
                "workflowInputPath",
                "workflowResultPath",
            ):
                value = scenario[field]
                if value is not None:
                    artifacts.add(value)

    for artifact in sorted(artifacts):
        if not (repo_root / artifact).is_file():
            raise DemoExecutionError(
                f"Final demo pack references a missing machine-readable artifact: {artifact}"
            )

    return sorted(artifacts)


def _human_readable_artifacts(
    *,
    conformance_report: dict[str, Any],
    demo_reports: list[dict[str, Any]],
) -> list[str]:
    artifacts = {
        conformance_report["artifacts"]["markdownSummaryPath"],
        "docs/evidence/DEMO_ARTIFACT_INDEX.md",
        "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
        "docs/runbooks/FINAL_DEMO_RUNBOOK.md",
    }

    for demo_report in demo_reports:
        for value in demo_report["artifacts"].values():
            if value is not None and value.endswith(".md"):
                artifacts.add(value)

    return sorted(artifacts)


def _integration_surfaces() -> list[dict[str, Any]]:
    return [
        {
            "participantType": "VENUE",
            "purpose": "Submit secured-finance obligations and consume machine-readable execution outcomes.",
            "requiredInputs": [
                "obligationId",
                "obligationAmount",
                "settlementCurrency",
                "currentPostedLotIds",
                "substitutionRequest",
            ],
            "controlPlaneOutputs": [
                "OptimizationReport",
                "ExecutionReport",
                "SubstitutionReport",
                "ReturnReport",
            ],
            "guidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
        },
        {
            "participantType": "FINANCING_APP",
            "purpose": "Call policy evaluation, optimization, and workflow orchestration from a Canton-native lending or derivatives application.",
            "requiredInputs": [
                "CPL policy package",
                "inventory snapshot",
                "obligation snapshot",
                "workflow correlation id",
            ],
            "controlPlaneOutputs": [
                "PolicyEvaluationReport",
                "OptimizationReport",
                "workflow input payloads",
                "execution evidence",
            ],
            "guidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
        },
        {
            "participantType": "TOKEN_ISSUER",
            "purpose": "Honor settlement and encumbrance state changes without taking over policy or workflow authority.",
            "requiredInputs": [
                "SettlementInstruction contract fields",
                "tokenAdapterReference",
                "assetId",
                "custody and destination accounts",
            ],
            "controlPlaneOutputs": [
                "settlement intent references",
                "execution reports",
                "audit trail evidence",
            ],
            "guidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
        },
        {
            "participantType": "CUSTODIAN",
            "purpose": "Approve or reject control changes and confirm settlement-driven encumbrance updates.",
            "requiredInputs": [
                "approval request identifiers",
                "encumbered lot ids",
                "replacement or return lot ids",
                "settlement system routing",
            ],
            "controlPlaneOutputs": [
                "approval-gated workflow states",
                "execution-report event ids",
                "audit-ready workflow steps",
            ],
            "guidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
        },
    ]


def _render_final_demo_summary(pack: dict[str, Any]) -> str:
    lines = [
        "# Final Demo Pack Summary",
        "",
        f"- Demo pack ID: `{pack['demoPackId']}`",
        f"- Command: `{pack['command']}`",
        f"- Overall status: `{pack['overallStatus']}`",
        f"- Conformance report: `{pack['artifacts']['conformanceReportPath']}`",
        "",
        "## Demo Flows",
        "",
        "| Demo | Report Type | Command | Positive | Negative | Report |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for flow in pack["demoFlows"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    flow["demoType"],
                    flow["reportType"],
                    f"`{flow['command']}`",
                    ", ".join(flow["positiveScenarioIds"]),
                    ", ".join(flow["negativeScenarioIds"]),
                    f"`{flow['reportPath']}`",
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Invariant Output",
            "",
            "| Check | Status | Detail |",
            "| --- | --- | --- |",
        ]
    )

    for check in pack["invariantOutput"]["conformanceChecks"]:
        lines.append(
            f"| {check['checkId']} | {check['status']} | {check['detail']} |"
        )

    lines.extend(
        [
            "",
            "## Integration Surfaces",
            "",
            "| Participant | Purpose | Outputs |",
            "| --- | --- | --- |",
        ]
    )

    for surface in pack["integrationSurfaces"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    surface["participantType"],
                    surface["purpose"],
                    ", ".join(surface["controlPlaneOutputs"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Artifact Counts",
            "",
            f"- Machine-readable artifacts: `{len(pack['machineReadableArtifacts'])}`",
            f"- Human-readable artifacts: `{len(pack['humanReadableArtifacts'])}`",
            f"- Artifact index: `{pack['artifacts']['demoArtifactIndexPath']}`",
            "",
        ]
    )

    return "\n".join(lines) + "\n"


def _demo_pack_id(
    *,
    conformance_report: dict[str, Any],
    demo_reports: list[dict[str, Any]],
    integration_surfaces: list[dict[str, Any]],
) -> str:
    canonical = json.dumps(
        {
            "conformanceSuiteId": conformance_report["suiteId"],
            "demoReportIds": [
                next(
                    report[key]
                    for key in (
                        "executionId",
                        "substitutionReportId",
                        "returnReportId",
                    )
                    if key in report
                )
                for report in demo_reports
            ],
            "integrationSurfaces": integration_surfaces,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"fdp-{digest[:16]}"


def _resolve_path(repo_root: Path, candidate: str | Path) -> Path:
    candidate_path = Path(candidate)
    if candidate_path.is_absolute():
        return candidate_path
    return (repo_root / candidate_path).resolve()
