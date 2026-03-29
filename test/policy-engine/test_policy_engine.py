import copy
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "app/policy-engine"))

from evaluator import evaluate_policy  # noqa: E402
from testsupport.fixture_builders import (  # noqa: E402
    inventory_with_candidate_indexes,
    load_inventory_fixture,
    load_policy_fixture,
    relaxed_policy_fixture,
)


class PolicyEngineTest(unittest.TestCase):
    maxDiff = None

    def load_policy(self, name: str) -> dict:
        return load_policy_fixture(name)

    def load_inventory(self) -> dict:
        return load_inventory_fixture()

    def relaxed_policy(self, name: str) -> dict:
        return relaxed_policy_fixture(name)

    def asset_result(self, report: dict, lot_id: str) -> dict:
        for asset in report["assetResults"]:
            if asset["lotId"] == lot_id:
                return asset
        raise AssertionError(f"missing lot {lot_id}")

    def assert_reason_code(self, asset: dict, code: str) -> None:
        codes = {reason["code"] for reason in asset["reasons"]}
        self.assertIn(code, codes)

    def test_eligible_asset(self) -> None:
        policy = self.relaxed_policy("central-bank-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(report["overallDecision"], "ACCEPT")
        self.assertEqual(asset["decision"], "ELIGIBLE")
        self.assertEqual(asset["totalHaircutBps"], 200)
        self.assertAlmostEqual(asset["lendableValue"], 245000.0)

    def test_ineligible_issuer(self) -> None:
        policy = self.relaxed_policy("central-bank-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)
        inventory["candidateLots"][0]["issuerId"] = "bad-issuer"

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(report["overallDecision"], "REJECT")
        self.assertEqual(asset["decision"], "INELIGIBLE")
        self.assert_reason_code(asset, "ISSUER_NOT_ON_ALLOW_LIST")

    def test_haircut_application(self) -> None:
        policy = self.relaxed_policy("central-bank-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)
        inventory["candidateLots"][0]["marketValue"] = 400000.0
        inventory["candidateLots"][0]["nominalValue"] = 420000.0
        inventory["candidateLots"][0]["outstandingPrincipal"] = 410000.0
        inventory["candidateLots"][0]["residualMaturityDays"] = 540

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(asset["baseHaircutBps"], 600)
        self.assertEqual(asset["totalHaircutBps"], 600)
        self.assertAlmostEqual(asset["valuationBasisValue"], 400000.0)
        self.assertAlmostEqual(asset["lendableValue"], 376000.0)

    def test_currency_mismatch_haircut(self) -> None:
        policy = self.relaxed_policy("bilateral-csa-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)
        inventory["evaluationContext"]["settlementCurrency"] = "USD"
        lot = inventory["candidateLots"][0]
        lot["assetClass"] = "CORPORATE_BOND"
        lot["issueType"] = "SENIOR_UNSECURED"
        lot["issuerId"] = "issuer-a"
        lot["issuerType"] = "CORPORATE"
        lot["longTermRating"] = "A"
        lot["currency"] = "EUR"
        lot["issuanceJurisdiction"] = "DE"
        lot["riskJurisdiction"] = "DE"
        lot["custodianId"] = "bilateral-custodian-a"
        lot["custodyJurisdiction"] = "US"
        lot["accountType"] = "BILATERAL_CUSTODY"
        lot["isSegregated"] = False
        lot["hasControlAgreement"] = False
        lot["segregationType"] = "NONE"
        lot["thirdPartyAcknowledgementReceived"] = False
        lot["marketValue"] = 100000.0
        lot["nominalValue"] = 100000.0
        lot["outstandingPrincipal"] = 100000.0
        inventory["evaluationContext"]["providerIssuerIds"] = ["dealer-a"]
        inventory["evaluationContext"]["exposureCounterparties"][0]["issuerIds"] = ["dealer-a"]

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(asset["decision"], "ELIGIBLE")
        self.assertEqual(asset["baseHaircutBps"], 1500)
        self.assertEqual(asset["currencyMismatchHaircutBps"], 300)
        self.assertEqual(asset["totalHaircutBps"], 1800)
        self.assertAlmostEqual(asset["lendableValue"], 82000.0)

    def test_concentration_limit_breach(self) -> None:
        policy = self.load_policy("central-bank-style-policy.json")
        inventory = inventory_with_candidate_indexes(0, 0, 1)
        inventory["candidateLots"][0]["lotId"] = "breach-lot-001"
        inventory["candidateLots"][0]["marketValue"] = 500000.0
        inventory["candidateLots"][0]["nominalValue"] = 500000.0
        inventory["candidateLots"][0]["outstandingPrincipal"] = 500000.0
        inventory["candidateLots"][1]["lotId"] = "breach-lot-002"
        inventory["candidateLots"][1]["marketValue"] = 200000.0
        inventory["candidateLots"][1]["nominalValue"] = 200000.0
        inventory["candidateLots"][1]["outstandingPrincipal"] = 200000.0
        inventory["candidateLots"][2]["lotId"] = "breach-lot-003"
        inventory["candidateLots"][2]["marketValue"] = 300000.0
        inventory["candidateLots"][2]["nominalValue"] = 300000.0
        inventory["candidateLots"][2]["outstandingPrincipal"] = 300000.0

        report = evaluate_policy(policy, inventory)
        issuer_results = [
            result
            for result in report["concentrationResults"]
            if result["limitId"] == "issuer-cap"
        ]

        self.assertEqual(report["overallDecision"], "REJECT")
        self.assertTrue(any(result["decision"] == "REJECT" for result in issuer_results))
        self.assert_reason_code(
            self.asset_result(report, "breach-lot-001"),
            "CONCENTRATION_LIMIT_BREACH",
        )

    def test_wrong_way_risk_exclusion(self) -> None:
        policy = self.relaxed_policy("bilateral-csa-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)
        lot = inventory["candidateLots"][0]
        lot["assetClass"] = "CORPORATE_BOND"
        lot["issueType"] = "SENIOR_UNSECURED"
        lot["issuerId"] = "counterparty-parent-bank"
        lot["issuerType"] = "CORPORATE"
        lot["longTermRating"] = "A"
        lot["currency"] = "USD"
        lot["issuanceJurisdiction"] = "US"
        lot["riskJurisdiction"] = "US"
        lot["custodianId"] = "bilateral-custodian-a"
        lot["custodyJurisdiction"] = "US"
        lot["accountType"] = "BILATERAL_CUSTODY"
        lot["isSegregated"] = False
        lot["hasControlAgreement"] = False
        lot["segregationType"] = "NONE"
        lot["thirdPartyAcknowledgementReceived"] = False

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(asset["decision"], "INELIGIBLE")
        self.assert_reason_code(asset, "WRONG_WAY_RISK_REJECT")

    def test_encumbrance_restriction_failure(self) -> None:
        policy = self.relaxed_policy("central-bank-style-policy.json")
        inventory = inventory_with_candidate_indexes(0)
        inventory["candidateLots"][0]["isEncumbered"] = True

        report = evaluate_policy(policy, inventory)
        asset = self.asset_result(report, "cb-lot-001")

        self.assertEqual(asset["decision"], "INELIGIBLE")
        self.assert_reason_code(asset, "ENCUMBERED_COLLATERAL_NOT_ALLOWED")

    def test_deterministic_output(self) -> None:
        policy = self.load_policy("central-bank-style-policy.json")
        inventory = self.load_inventory()

        first = evaluate_policy(copy.deepcopy(policy), copy.deepcopy(inventory))
        second = evaluate_policy(copy.deepcopy(policy), copy.deepcopy(inventory))

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
