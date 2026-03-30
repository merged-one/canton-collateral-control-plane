"""Build the reviewer-facing proposal submission package."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from margin_call_demo import DemoExecutionError, _load_json, _relative_path, _utc_now, _write_json, _write_text


REPORT_ID_FIELDS = (
    "executionId",
    "substitutionReportId",
    "returnReportId",
)
REVIEWER_DOC_PATHS = {
    "reviewerStartPath": "docs/evidence/REVIEWER_START_HERE.md",
    "reviewerMemoPath": "docs/evidence/PROPOSAL_SUBMISSION_MEMO.md",
    "walkthroughScriptPath": "docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md",
}
DO_NOT_INFER = [
    "The reference token adapter path is not a generalized production custodian, issuer, or settlement-network integration surface.",
    "The current workflow-party and provider-visible evidence surfaces do not yet prove broader role-scoped disclosure profiles.",
    "Workflow-coupled optimizer reservation, settlement-window enforcement, retry and recovery semantics, and reference-data contracts remain staged roadmap scope.",
]


def build_proposal_submission_package(
    *,
    final_demo_pack_path: str | Path,
    output_dir: str | Path,
    repo_root: str | Path,
) -> dict[str, Any]:
    repo_root_path = Path(repo_root).resolve()
    output_dir_path = Path(output_dir).resolve()
    output_dir_path.mkdir(parents=True, exist_ok=True)

    final_demo_pack = _load_json(_resolve_path(repo_root_path, final_demo_pack_path))
    if final_demo_pack["overallStatus"] != "PASS":
        raise DemoExecutionError(
            "The final demo pack must pass before the proposal submission package can be built."
        )

    conformance_report = _load_json(
        _resolve_path(repo_root_path, final_demo_pack["artifacts"]["conformanceReportPath"])
    )
    if conformance_report["overallStatus"] != "PASS":
        raise DemoExecutionError(
            "The conformance suite must pass before the proposal submission package can be built."
        )

    reviewer_docs = _reviewer_docs(repo_root_path)
    demo_reports = [
        _load_json(_resolve_path(repo_root_path, demo_flow["reportPath"]))
        for demo_flow in final_demo_pack["demoFlows"]
    ]
    git_metadata = _git_metadata(repo_root_path)

    manifest_path = output_dir_path / "proposal-submission-manifest.json"
    summary_path = output_dir_path / "proposal-submission-summary.md"

    review_order = _review_order(
        final_demo_pack=final_demo_pack,
        reviewer_docs=reviewer_docs,
    )
    baseline = _submission_baseline(
        final_demo_pack=final_demo_pack,
        conformance_report=conformance_report,
        demo_reports=demo_reports,
        git_metadata=git_metadata,
    )

    manifest = {
        "reportType": "ProposalSubmissionManifest",
        "reportVersion": "0.1.0",
        "submissionId": _submission_id(
            final_demo_pack=final_demo_pack,
            conformance_report=conformance_report,
            git_metadata=git_metadata,
            reviewer_docs=reviewer_docs,
        ),
        "generatedAt": _utc_now(),
        "overallStatus": "PASS",
        "command": "make proposal-package",
        "artifacts": {
            "proposalSubmissionManifestPath": _relative_path(manifest_path, repo_root_path),
            "markdownSummaryPath": _relative_path(summary_path, repo_root_path),
            "finalDemoPackPath": _relative_path(
                _resolve_path(repo_root_path, final_demo_pack_path),
                repo_root_path,
            ),
            "finalDemoPackSummaryPath": final_demo_pack["artifacts"]["markdownSummaryPath"],
            "conformanceReportPath": final_demo_pack["artifacts"]["conformanceReportPath"],
            "conformanceSummaryPath": final_demo_pack["artifacts"]["conformanceSummaryPath"],
            **reviewer_docs,
            "proposalReadinessPath": final_demo_pack["artifacts"]["proposalReadinessPath"],
            "demoArtifactIndexPath": final_demo_pack["artifacts"]["demoArtifactIndexPath"],
            "integrationGuidePath": final_demo_pack["artifacts"]["integrationGuidePath"],
            "runbookPath": final_demo_pack["artifacts"]["runbookPath"],
        },
        "submissionBaseline": baseline,
        "reviewerJourney": {
            "primaryCommand": "make proposal-package",
            "timebox": "10-15 minutes",
            "reviewOrder": review_order,
        },
        "claimBoundaries": {
            "realOnQuickstart": final_demo_pack["readiness"]["realOnQuickstart"],
            "machineReadableProof": final_demo_pack["readiness"]["machineReadableProof"],
            "prototypeOnly": final_demo_pack["readiness"]["prototypeOnly"],
            "technicalDeltaFromEarlierPrototype": final_demo_pack["readiness"]["technicalDeltaFromEarlierPrototype"],
            "doNotInfer": DO_NOT_INFER,
        },
        "walkthroughPackage": {
            "walkthroughScriptPath": reviewer_docs["walkthroughScriptPath"],
            "commandsShown": [
                "make proposal-package",
            ],
            "artifactOrder": [
                "reports/generated/proposal-submission-summary.md",
                "reports/generated/proposal-submission-manifest.json",
                final_demo_pack["runtimeEvidence"]["deploymentReceiptPath"],
                final_demo_pack["runtimeEvidence"]["referenceAdapterExecutionReportPath"],
                final_demo_pack["runtimeEvidence"]["referenceAdapterStatusPath"],
                *[demo_flow["reportPath"] for demo_flow in final_demo_pack["demoFlows"]],
                final_demo_pack["artifacts"]["conformanceReportPath"],
                final_demo_pack["artifacts"]["finalDemoPackPath"],
            ],
        },
    }

    _write_json(manifest_path, manifest)
    _write_text(summary_path, _render_submission_summary(manifest))
    return manifest


def _reviewer_docs(repo_root: Path) -> dict[str, str]:
    for artifact in REVIEWER_DOC_PATHS.values():
        if not (repo_root / artifact).is_file():
            raise DemoExecutionError(
                f"Proposal submission package references a missing reviewer document: {artifact}"
            )
    return dict(REVIEWER_DOC_PATHS)


def _submission_baseline(
    *,
    final_demo_pack: dict[str, Any],
    conformance_report: dict[str, Any],
    demo_reports: list[dict[str, Any]],
    git_metadata: dict[str, Any],
) -> dict[str, Any]:
    runtime_evidence = final_demo_pack["runtimeEvidence"]
    return {
        "sourceCommit": git_metadata["commitSha"],
        "sourceCommitShort": git_metadata["commitSha"][:7],
        "worktreeStatus": git_metadata["worktreeStatus"],
        "dirtyPaths": git_metadata["dirtyPaths"],
        "finalDemoPackId": final_demo_pack["demoPackId"],
        "conformanceSuiteId": conformance_report["suiteId"],
        "passStates": {
            "conformanceSuite": conformance_report["overallStatus"],
            "finalDemoPack": final_demo_pack["overallStatus"],
            "proposalSubmissionPackage": "PASS",
        },
        "runtimeMode": runtime_evidence["runtimeMode"],
        "quickstartCommit": runtime_evidence["deployment"]["quickstartCommit"],
        "deployedDarFile": runtime_evidence["deployment"]["darFile"],
        "deployedPackageId": runtime_evidence["deployment"]["packageId"],
        "participants": runtime_evidence["deployment"]["participants"],
        "referenceAdapterPath": runtime_evidence["referenceAdapterPath"],
        "demoReports": [
            {
                "demoType": demo_flow["demoType"],
                "reportType": demo_flow["reportType"],
                "reportId": _report_id(report),
                "overallStatus": report["overallStatus"],
                "command": demo_flow["command"],
                "reportPath": demo_flow["reportPath"],
                "positiveScenarioIds": demo_flow["positiveScenarioIds"],
                "negativeScenarioIds": demo_flow["negativeScenarioIds"],
            }
            for demo_flow, report in zip(final_demo_pack["demoFlows"], demo_reports, strict=True)
        ],
    }


def _review_order(
    *,
    final_demo_pack: dict[str, Any],
    reviewer_docs: dict[str, str],
) -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "label": "Reviewer start",
            "path": reviewer_docs["reviewerStartPath"],
            "purpose": "Start with the shortest orientation path and the exact command surface.",
        },
        {
            "step": 2,
            "label": "Reviewer memo",
            "path": reviewer_docs["reviewerMemoPath"],
            "purpose": "Read the runtime-backed claims, staged scope, and technical delta in one place.",
        },
        {
            "step": 3,
            "label": "Quickstart deployment",
            "path": final_demo_pack["runtimeEvidence"]["deploymentReceiptPath"],
            "purpose": "Confirm the pinned Quickstart commit, deployed DAR, and package identity.",
        },
        {
            "step": 4,
            "label": "Reference adapter",
            "path": final_demo_pack["runtimeEvidence"]["referenceAdapterExecutionReportPath"],
            "purpose": "Verify the concrete settlement-instruction-to-adapter proof path.",
        },
        {
            "step": 5,
            "label": "Adapter status",
            "path": final_demo_pack["runtimeEvidence"]["referenceAdapterStatusPath"],
            "purpose": "Confirm the provider-visible post-execution state after the adapter path ran.",
        },
        {
            "step": 6,
            "label": "Quickstart demos",
            "path": final_demo_pack["artifacts"]["finalDemoPackPath"],
            "purpose": "Use the final demo pack to inspect the margin-call, substitution, and return runtime paths.",
        },
        {
            "step": 7,
            "label": "Conformance",
            "path": final_demo_pack["artifacts"]["conformanceReportPath"],
            "purpose": "Confirm the aggregate invariant pass or fail output for the Quickstart-backed proof set.",
        },
        {
            "step": 8,
            "label": "Walkthrough",
            "path": reviewer_docs["walkthroughScriptPath"],
            "purpose": "Use the repo-tracked walkthrough script for reviewer replay or live presentation.",
        },
    ]


def _render_submission_summary(manifest: dict[str, Any]) -> str:
    baseline = manifest["submissionBaseline"]
    lines = [
        "# Proposal Submission Summary",
        "",
        f"- Submission ID: `{manifest['submissionId']}`",
        f"- Command: `{manifest['command']}`",
        f"- Overall status: `{manifest['overallStatus']}`",
        f"- Source commit: `{baseline['sourceCommit']}`",
        f"- Worktree status at package build: `{baseline['worktreeStatus']}`",
        f"- Final demo pack ID: `{baseline['finalDemoPackId']}`",
        f"- Conformance suite ID: `{baseline['conformanceSuiteId']}`",
        f"- Quickstart commit: `{baseline['quickstartCommit']}`",
        f"- Deployed package ID: `{baseline['deployedPackageId']}`",
        "",
        "## Reviewer Journey",
        "",
        "| Step | Label | Path | Purpose |",
        "| --- | --- | --- | --- |",
    ]

    for step in manifest["reviewerJourney"]["reviewOrder"]:
        lines.append(
            f"| {step['step']} | {step['label']} | `{step['path']}` | {step['purpose']} |"
        )

    lines.extend(
        [
            "",
            "## Frozen Runtime Proof",
            "",
            f"- Runtime mode: `{baseline['runtimeMode']}`",
            f"- Reference adapter receipt status: `{baseline['referenceAdapterPath']['receiptStatus']}`",
            "- Adapter movement lots: `"
            + ", ".join(baseline["referenceAdapterPath"]["movementLotIds"])
            + "`",
            "",
            "| Demo | Report ID | Command | Report |",
            "| --- | --- | --- | --- |",
        ]
    )

    for demo_report in baseline["demoReports"]:
        lines.append(
            f"| {demo_report['demoType']} | `{demo_report['reportId']}` | `{demo_report['command']}` | `{demo_report['reportPath']}` |"
        )

    lines.extend(
        [
            "",
            "## Real Vs Staged",
            "",
            "### Real On Quickstart",
            "",
        ]
    )

    for item in manifest["claimBoundaries"]["realOnQuickstart"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "### Do Not Infer",
            "",
        ]
    )

    for item in manifest["claimBoundaries"]["doNotInfer"]:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Walkthrough Package",
            "",
            f"- Walkthrough script: `{manifest['walkthroughPackage']['walkthroughScriptPath']}`",
            f"- Commands shown: `{', '.join(manifest['walkthroughPackage']['commandsShown'])}`",
            f"- Artifact order count: `{len(manifest['walkthroughPackage']['artifactOrder'])}`",
            "",
        ]
    )

    return "\n".join(lines) + "\n"


def _submission_id(
    *,
    final_demo_pack: dict[str, Any],
    conformance_report: dict[str, Any],
    git_metadata: dict[str, Any],
    reviewer_docs: dict[str, str],
) -> str:
    canonical = json.dumps(
        {
            "finalDemoPackId": final_demo_pack["demoPackId"],
            "conformanceSuiteId": conformance_report["suiteId"],
            "sourceCommit": git_metadata["commitSha"],
            "reviewerDocs": reviewer_docs,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"psp-{digest[:16]}"


def _git_metadata(repo_root: Path) -> dict[str, Any]:
    commit_sha = _git_stdout(repo_root, "rev-parse", "HEAD").strip()
    dirty_paths = [
        line
        for line in _git_stdout(repo_root, "status", "--short").splitlines()
        if line.strip()
    ]
    return {
        "commitSha": commit_sha,
        "worktreeStatus": "CLEAN" if not dirty_paths else "DIRTY",
        "dirtyPaths": dirty_paths,
    }


def _git_stdout(repo_root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def _report_id(report: dict[str, Any]) -> str:
    for field in REPORT_ID_FIELDS:
        if field in report:
            return report[field]
    raise DemoExecutionError("Demo report is missing a recognized report identifier field.")


def _resolve_path(repo_root: Path, candidate: str | Path) -> Path:
    candidate_path = Path(candidate)
    if candidate_path.is_absolute():
        return candidate_path
    return (repo_root / candidate_path).resolve()
