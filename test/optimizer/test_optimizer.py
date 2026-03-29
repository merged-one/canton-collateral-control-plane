import copy
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "app/optimizer"))
sys.path.insert(0, str(REPO_ROOT / "app/policy-engine"))

from optimizer import optimize_collateral  # noqa: E402
from testsupport.fixture_builders import (  # noqa: E402
    build_obligation,
    inventory_with_candidate_indexes,
    load_inventory_fixture,
    load_policy_fixture,
    relaxed_policy_fixture,
)


class OptimizerTest(unittest.TestCase):
    maxDiff = None

    def load_policy(self) -> dict:
        return load_policy_fixture("central-bank-style-policy.json")

    def load_inventory(self) -> dict:
        return load_inventory_fixture()

    def relaxed_policy(self) -> dict:
        return relaxed_policy_fixture("central-bank-style-policy.json")

    def obligation(
        self,
        inventory: dict,
        amount: float,
        current_posted=None,
        substitution_request=None,
    ) -> dict:
        return build_obligation(
            inventory,
            amount,
            current_posted=current_posted,
            substitution_request=substitution_request,
        )

    def test_cheapest_eligible_asset_wins_when_unconstrained(self) -> None:
        policy = self.relaxed_policy()
        inventory = inventory_with_candidate_indexes(0, 3)
        inventory["candidateLots"][0]["lotId"] = "cheap-sovereign"
        inventory["candidateLots"][0]["assetId"] = "cheap-sovereign-asset"
        inventory["candidateLots"][1]["lotId"] = "expensive-agency"
        inventory["candidateLots"][1]["assetId"] = "expensive-agency-asset"
        inventory["candidateLots"][1]["marketValue"] = 260000.0
        inventory["candidateLots"][1]["nominalValue"] = 260000.0
        inventory["candidateLots"][1]["outstandingPrincipal"] = 260000.0

        report = optimize_collateral(policy, inventory, self.obligation(inventory, 240000.0))

        self.assertEqual(report["status"], "OPTIMAL")
        self.assertEqual(report["recommendedAction"], "POST_NEW_SET")
        self.assertEqual(report["recommendedPortfolio"]["lotIds"], ["cheap-sovereign"])

    def test_concentration_rule_changes_the_allocation(self) -> None:
        policy = self.load_policy()
        for limit in policy["concentrationLimits"]:
            if limit["limitId"] == "issuer-cap":
                limit["threshold"]["value"] = 0.6

        inventory = inventory_with_candidate_indexes(0, 0, 1)
        inventory["candidateLots"][0]["lotId"] = "ust-large"
        inventory["candidateLots"][0]["assetId"] = "ust-large-asset"
        inventory["candidateLots"][1]["lotId"] = "ust-small"
        inventory["candidateLots"][1]["assetId"] = "ust-small-asset"
        inventory["candidateLots"][1]["marketValue"] = 200000.0
        inventory["candidateLots"][1]["nominalValue"] = 200000.0
        inventory["candidateLots"][1]["outstandingPrincipal"] = 200000.0
        inventory["candidateLots"][2]["lotId"] = "kfw-diversifier"
        inventory["candidateLots"][2]["assetId"] = "kfw-diversifier-asset"
        inventory["candidateLots"][2]["marketValue"] = 260000.0
        inventory["candidateLots"][2]["nominalValue"] = 260000.0
        inventory["candidateLots"][2]["outstandingPrincipal"] = 260000.0

        report = optimize_collateral(policy, inventory, self.obligation(inventory, 430000.0))

        self.assertEqual(report["status"], "OPTIMAL")
        self.assertEqual(
            report["recommendedPortfolio"]["lotIds"],
            ["kfw-diversifier", "ust-small"],
        )
        blocked_same_issuer = [
            trace
            for trace in report["explanationTrace"]
            if trace["stage"] == "SEARCH"
            and trace["lotIds"] == ["ust-large", "ust-small"]
        ]
        self.assertEqual(len(blocked_same_issuer), 1)
        self.assertIn("CONCENTRATION_LIMIT_BREACH", blocked_same_issuer[0]["reasonCodes"])

    def test_substitution_improves_objective_while_preserving_policy_compliance(self) -> None:
        policy = self.relaxed_policy()
        inventory = inventory_with_candidate_indexes(0, 1, 2)
        inventory["candidateLots"][0]["lotId"] = "best-single"
        inventory["candidateLots"][0]["assetId"] = "best-single-asset"
        inventory["candidateLots"][1]["lotId"] = "current-a"
        inventory["candidateLots"][1]["assetId"] = "current-a-asset"
        inventory["candidateLots"][1]["marketValue"] = 140000.0
        inventory["candidateLots"][1]["nominalValue"] = 140000.0
        inventory["candidateLots"][1]["outstandingPrincipal"] = 140000.0
        inventory["candidateLots"][2]["lotId"] = "current-b"
        inventory["candidateLots"][2]["assetId"] = "current-b-asset"
        inventory["candidateLots"][2]["marketValue"] = 140000.0
        inventory["candidateLots"][2]["nominalValue"] = 140000.0
        inventory["candidateLots"][2]["outstandingPrincipal"] = 140000.0

        report = optimize_collateral(
            policy,
            inventory,
            self.obligation(inventory, 240000.0, current_posted=["current-a", "current-b"]),
        )

        self.assertEqual(report["recommendedAction"], "SUBSTITUTE")
        self.assertEqual(report["recommendedPortfolio"]["lotIds"], ["best-single"])
        self.assertEqual(
            report["substitutionRecommendation"]["removeLotIds"],
            ["current-a", "current-b"],
        )
        self.assertEqual(report["substitutionRecommendation"]["addLotIds"], ["best-single"])
        self.assertEqual(report["substitutionRecommendation"]["mustReplaceLotIds"], [])
        self.assertEqual(report["substitutionRecommendation"]["retainedLotIds"], [])
        self.assertTrue(report["substitutionRecommendation"]["improvesObjective"])
        self.assertTrue(report["currentPortfolio"]["isFeasible"])

    def test_forced_substitution_can_replace_a_better_incumbent_when_release_is_required(self) -> None:
        policy = self.relaxed_policy()
        inventory = inventory_with_candidate_indexes(0, 1, 2)
        inventory["candidateLots"][0]["lotId"] = "current-a"
        inventory["candidateLots"][0]["assetId"] = "current-a-asset"
        inventory["candidateLots"][0]["marketValue"] = 120000.0
        inventory["candidateLots"][0]["nominalValue"] = 120000.0
        inventory["candidateLots"][0]["outstandingPrincipal"] = 120000.0
        inventory["candidateLots"][1]["lotId"] = "current-b"
        inventory["candidateLots"][1]["assetId"] = "current-b-asset"
        inventory["candidateLots"][1]["marketValue"] = 120000.0
        inventory["candidateLots"][1]["nominalValue"] = 120000.0
        inventory["candidateLots"][1]["outstandingPrincipal"] = 120000.0
        inventory["candidateLots"][2]["lotId"] = "replacement-only"
        inventory["candidateLots"][2]["assetId"] = "replacement-only-asset"
        inventory["candidateLots"][2]["marketValue"] = 250000.0
        inventory["candidateLots"][2]["nominalValue"] = 250000.0
        inventory["candidateLots"][2]["outstandingPrincipal"] = 250000.0

        report = optimize_collateral(
            policy,
            inventory,
            self.obligation(
                inventory,
                210000.0,
                current_posted=["current-a", "current-b"],
                substitution_request={
                    "requestId": "forced-substitution",
                    "mustReplaceLotIds": ["current-a", "current-b"],
                    "atomicityRequired": True,
                },
            ),
        )

        self.assertEqual(report["recommendedAction"], "SUBSTITUTE")
        self.assertEqual(report["recommendedPortfolio"]["lotIds"], ["replacement-only"])
        self.assertEqual(
            report["obligation"]["substitutionRequest"]["mustReplaceLotIds"],
            ["current-a", "current-b"],
        )
        self.assertEqual(
            report["substitutionRecommendation"]["mustReplaceLotIds"],
            ["current-a", "current-b"],
        )
        self.assertFalse(report["substitutionRecommendation"]["improvesObjective"])
        blocked_scope_traces = [
            trace
            for trace in report["explanationTrace"]
            if trace["outcome"] == "BLOCKED_BY_SCOPE"
        ]
        self.assertTrue(blocked_scope_traces)

    def test_forced_substitution_returns_no_solution_when_replacements_breach_concentration(self) -> None:
        policy = self.load_policy()
        for limit in policy["concentrationLimits"]:
            if limit["limitId"] == "issuer-cap":
                limit["threshold"]["value"] = 0.6

        inventory = inventory_with_candidate_indexes(1, 2, 0, 0)
        inventory["candidateLots"][0]["lotId"] = "current-kfw"
        inventory["candidateLots"][0]["assetId"] = "current-kfw-asset"
        inventory["candidateLots"][1]["lotId"] = "current-eib"
        inventory["candidateLots"][1]["assetId"] = "current-eib-asset"
        inventory["candidateLots"][2]["lotId"] = "replacement-ust-a"
        inventory["candidateLots"][2]["assetId"] = "replacement-ust-a-asset"
        inventory["candidateLots"][2]["marketValue"] = 220000.0
        inventory["candidateLots"][2]["nominalValue"] = 220000.0
        inventory["candidateLots"][2]["outstandingPrincipal"] = 220000.0
        inventory["candidateLots"][3]["lotId"] = "replacement-ust-b"
        inventory["candidateLots"][3]["assetId"] = "replacement-ust-b-asset"
        inventory["candidateLots"][3]["marketValue"] = 220000.0
        inventory["candidateLots"][3]["nominalValue"] = 220000.0
        inventory["candidateLots"][3]["outstandingPrincipal"] = 220000.0

        report = optimize_collateral(
            policy,
            inventory,
            self.obligation(
                inventory,
                430000.0,
                current_posted=["current-eib", "current-kfw"],
                substitution_request={
                    "requestId": "concentration-breach",
                    "mustReplaceLotIds": ["current-eib", "current-kfw"],
                    "atomicityRequired": True,
                },
            ),
        )

        self.assertEqual(report["status"], "NO_SOLUTION")
        self.assertEqual(report["recommendedAction"], "NO_SOLUTION")
        self.assertIsNone(report["recommendedPortfolio"])
        decision_trace = next(
            trace
            for trace in report["explanationTrace"]
            if trace["stage"] == "DECISION"
        )
        self.assertIn("CONCENTRATION_LIMIT_BREACH", decision_trace["reasonCodes"])

    def test_no_solution_case_is_handled_cleanly(self) -> None:
        policy = self.relaxed_policy()
        inventory = inventory_with_candidate_indexes(0)
        inventory["candidateLots"][0]["lotId"] = "insufficient-lot"

        report = optimize_collateral(policy, inventory, self.obligation(inventory, 300000.0))

        self.assertEqual(report["status"], "NO_SOLUTION")
        self.assertEqual(report["recommendedAction"], "NO_SOLUTION")
        self.assertIsNone(report["recommendedPortfolio"])
        self.assertEqual(report["candidateUniverse"]["feasibleCombinationCount"], 0)
        self.assertTrue(
            any(
                "INSUFFICIENT_LENDABLE_VALUE" in trace["reasonCodes"]
                for trace in report["explanationTrace"]
                if trace["stage"] == "SEARCH"
            )
        )

    def test_optimizer_output_is_deterministic(self) -> None:
        policy = self.relaxed_policy()
        inventory = inventory_with_candidate_indexes(0, 3)

        obligation = self.obligation(inventory, 240000.0)
        first = optimize_collateral(
            copy.deepcopy(policy),
            copy.deepcopy(inventory),
            copy.deepcopy(obligation),
        )
        second = optimize_collateral(
            copy.deepcopy(policy),
            copy.deepcopy(inventory),
            copy.deepcopy(obligation),
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
