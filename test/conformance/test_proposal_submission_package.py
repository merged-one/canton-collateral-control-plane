import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "app/orchestration"))

from margin_call_demo import DemoExecutionError  # noqa: E402
from proposal_submission_pack import build_proposal_submission_package  # noqa: E402


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _write_text(path: Path, payload: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8")


class ProposalSubmissionPackageUnitTest(unittest.TestCase):
    maxDiff = None

    def test_build_proposal_submission_package_writes_manifest_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            reports_generated = repo_root / "reports/generated"
            docs_evidence = repo_root / "docs/evidence"
            docs_integration = repo_root / "docs/integration"
            docs_runbooks = repo_root / "docs/runbooks"

            _write_text(docs_evidence / "REVIEWER_START_HERE.md", "# Start\n")
            _write_text(docs_evidence / "PROPOSAL_SUBMISSION_MEMO.md", "# Memo\n")
            _write_text(docs_evidence / "PROPOSAL_WALKTHROUGH_SCRIPT.md", "# Walkthrough\n")
            _write_text(docs_evidence / "PROPOSAL_READINESS_ASSESSMENT.md", "# Readiness\n")
            _write_text(docs_evidence / "DEMO_ARTIFACT_INDEX.md", "# Index\n")
            _write_text(docs_integration / "THIRD_PARTY_INTEGRATION_GUIDE.md", "# Guide\n")
            _write_text(docs_runbooks / "FINAL_DEMO_RUNBOOK.md", "# Runbook\n")

            _write_text(reports_generated / "final-demo-pack-summary.md", "# Final demo pack summary\n")
            _write_text(reports_generated / "conformance-suite-summary.md", "# Conformance summary\n")
            _write_text(reports_generated / "localnet-control-plane-deployment-summary.md", "# Deployment summary\n")
            _write_text(reports_generated / "localnet-reference-token-adapter-summary.md", "# Adapter summary\n")

            for path in (
                "reports/generated/localnet-control-plane-deployment-receipt.json",
                "reports/generated/localnet-reference-token-adapter-execution-report.json",
                "reports/generated/localnet-reference-token-adapter-status.json",
                "reports/generated/margin-call-quickstart-execution-report.json",
                "reports/generated/substitution-quickstart-report.json",
                "reports/generated/return-quickstart-report.json",
            ):
                _write_json(repo_root / path, {"reportType": "TestArtifact"})

            _write_json(
                reports_generated / "conformance-suite-report.json",
                {
                    "suiteId": "csr-test-001",
                    "overallStatus": "PASS",
                    "runtimeEvidence": {
                        "validationFailures": [],
                    },
                    "artifacts": {
                        "conformanceReportPath": "reports/generated/conformance-suite-report.json",
                        "markdownSummaryPath": "reports/generated/conformance-suite-summary.md",
                    },
                },
            )

            _write_json(
                reports_generated / "margin-call-quickstart-execution-report.json",
                {
                    "executionId": "exec-001",
                    "overallStatus": "PASS",
                },
            )
            _write_json(
                reports_generated / "substitution-quickstart-report.json",
                {
                    "substitutionReportId": "sub-001",
                    "overallStatus": "PASS",
                },
            )
            _write_json(
                reports_generated / "return-quickstart-report.json",
                {
                    "returnReportId": "ret-001",
                    "overallStatus": "PASS",
                },
            )

            _write_json(
                reports_generated / "final-demo-pack.json",
                {
                    "demoPackId": "fdp-test-001",
                    "overallStatus": "PASS",
                    "artifacts": {
                        "finalDemoPackPath": "reports/generated/final-demo-pack.json",
                        "markdownSummaryPath": "reports/generated/final-demo-pack-summary.md",
                        "conformanceReportPath": "reports/generated/conformance-suite-report.json",
                        "conformanceSummaryPath": "reports/generated/conformance-suite-summary.md",
                        "demoArtifactIndexPath": "docs/evidence/DEMO_ARTIFACT_INDEX.md",
                        "integrationGuidePath": "docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md",
                        "proposalReadinessPath": "docs/evidence/PROPOSAL_READINESS_ASSESSMENT.md",
                        "runbookPath": "docs/runbooks/FINAL_DEMO_RUNBOOK.md",
                    },
                    "runtimeEvidence": {
                        "runtimeMode": "QUICKSTART",
                        "deploymentReceiptPath": "reports/generated/localnet-control-plane-deployment-receipt.json",
                        "deploymentSummaryPath": "reports/generated/localnet-control-plane-deployment-summary.md",
                        "referenceAdapterExecutionReportPath": "reports/generated/localnet-reference-token-adapter-execution-report.json",
                        "referenceAdapterStatusPath": "reports/generated/localnet-reference-token-adapter-status.json",
                        "referenceAdapterSummaryPath": "reports/generated/localnet-reference-token-adapter-summary.md",
                        "deployment": {
                            "quickstartCommit": "quickstart-commit-001",
                            "darFile": ".daml/dist-quickstart/test.dar",
                            "packageId": "package-001",
                            "participants": ["app-provider", "app-user"],
                        },
                        "referenceAdapterPath": {
                            "adapterName": "quickstart-reference-token-adapter",
                            "workflowType": "PostingWorkflow",
                            "settlementAction": "PostCollateral",
                            "receiptStatus": "EXECUTED",
                            "movementLotIds": ["lot-001", "lot-002"],
                            "providerVisibleAdapterReceiptCount": 1,
                            "providerVisibleEncumbranceCount": 2,
                        },
                    },
                    "readiness": {
                        "realOnQuickstart": ["Runtime-backed proof."],
                        "machineReadableProof": [
                            "reports/generated/localnet-control-plane-deployment-receipt.json"
                        ],
                        "prototypeOnly": ["Production adapters remain staged."],
                        "technicalDeltaFromEarlierPrototype": ["Quickstart is now primary."],
                    },
                    "demoFlows": [
                        {
                            "demoType": "CONFIDENTIAL_MARGIN_CALL",
                            "reportType": "ExecutionReport",
                            "command": "make demo-margin-call-quickstart",
                            "reportPath": "reports/generated/margin-call-quickstart-execution-report.json",
                            "positiveScenarioIds": ["positive-margin-call-quickstart"],
                            "negativeScenarioIds": ["negative-margin-call-quickstart"],
                        },
                        {
                            "demoType": "CONFIDENTIAL_COLLATERAL_SUBSTITUTION",
                            "reportType": "SubstitutionReport",
                            "command": "make demo-substitution-quickstart",
                            "reportPath": "reports/generated/substitution-quickstart-report.json",
                            "positiveScenarioIds": ["positive-substitution-quickstart"],
                            "negativeScenarioIds": ["negative-substitution-quickstart"],
                        },
                        {
                            "demoType": "CONFIDENTIAL_MARGIN_RETURN",
                            "reportType": "ReturnReport",
                            "command": "make demo-return-quickstart",
                            "reportPath": "reports/generated/return-quickstart-report.json",
                            "positiveScenarioIds": ["positive-return-quickstart"],
                            "negativeScenarioIds": ["negative-return-quickstart"],
                        },
                    ],
                },
            )

            with patch(
                "proposal_submission_pack._git_metadata",
                return_value={
                    "commitSha": "abc123def456",
                    "worktreeStatus": "CLEAN",
                    "dirtyPaths": [],
                },
            ):
                manifest = build_proposal_submission_package(
                    final_demo_pack_path=reports_generated / "final-demo-pack.json",
                    output_dir=reports_generated,
                    repo_root=repo_root,
                )

            self.assertEqual(manifest["reportType"], "ProposalSubmissionManifest")
            self.assertEqual(manifest["overallStatus"], "PASS")
            self.assertEqual(
                manifest["submissionBaseline"]["conformanceSuiteId"],
                "csr-test-001",
            )
            self.assertEqual(
                manifest["submissionBaseline"]["demoReports"][0]["reportId"],
                "exec-001",
            )
            self.assertEqual(
                set(manifest["artifacts"].keys()),
                {
                    "proposalSubmissionManifestPath",
                    "markdownSummaryPath",
                    "finalDemoPackPath",
                    "finalDemoPackSummaryPath",
                    "conformanceReportPath",
                    "conformanceSummaryPath",
                    "reviewerStartPath",
                    "reviewerMemoPath",
                    "walkthroughScriptPath",
                    "proposalReadinessPath",
                    "demoArtifactIndexPath",
                    "integrationGuidePath",
                    "runbookPath",
                },
            )
            self.assertEqual(
                set(manifest["walkthroughPackage"].keys()),
                {
                    "walkthroughScriptPath",
                    "commandsShown",
                    "artifactOrder",
                },
            )
            self.assertTrue(
                (reports_generated / "proposal-submission-manifest.json").is_file()
            )
            self.assertTrue(
                (reports_generated / "proposal-submission-summary.md").is_file()
            )

    def test_build_proposal_submission_package_fails_when_final_demo_pack_is_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_root = Path(tmp_dir)
            reports_generated = repo_root / "reports/generated"
            _write_json(
                reports_generated / "final-demo-pack.json",
                {
                    "demoPackId": "fdp-test-fail",
                    "overallStatus": "FAIL",
                },
            )

            with self.assertRaises(DemoExecutionError):
                build_proposal_submission_package(
                    final_demo_pack_path=reports_generated / "final-demo-pack.json",
                    output_dir=reports_generated,
                    repo_root=repo_root,
                )


if __name__ == "__main__":
    unittest.main()
