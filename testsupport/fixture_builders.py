"""Deterministic fixture builders shared across Python test suites."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_json_fixture(relative_path: str | Path) -> dict[str, Any]:
    with (REPO_ROOT / Path(relative_path)).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_policy_fixture(name: str) -> dict[str, Any]:
    return load_json_fixture(Path("examples/policies") / name)


def load_inventory_fixture(
    name: str = "central-bank-eligible-inventory.json",
) -> dict[str, Any]:
    return load_json_fixture(Path("examples/inventory") / name)


def inventory_with_candidate_indexes(
    *indexes: int,
    inventory_name: str = "central-bank-eligible-inventory.json",
) -> dict[str, Any]:
    inventory = load_inventory_fixture(inventory_name)
    candidate_lots = inventory["candidateLots"]
    inventory["candidateLots"] = [
        copy.deepcopy(candidate_lots[index]) for index in indexes
    ]
    return inventory


def relax_concentration_limits(policy: dict[str, Any]) -> dict[str, Any]:
    relaxed = copy.deepcopy(policy)
    for limit in relaxed["concentrationLimits"]:
        if limit["threshold"]["metric"] == "ABSOLUTE_MARKET_VALUE":
            limit["threshold"]["value"] = 10**12
        else:
            limit["threshold"]["value"] = 1
    return relaxed


def relaxed_policy_fixture(name: str) -> dict[str, Any]:
    return relax_concentration_limits(load_policy_fixture(name))


def build_obligation(
    inventory: dict[str, Any],
    amount: float,
    *,
    current_posted: list[str] | None = None,
    substitution_request: dict[str, Any] | None = None,
    obligation_id: str = "optimizer-test-obligation",
) -> dict[str, Any]:
    obligation = {
        "obligationId": obligation_id,
        "obligationVersion": "1.0.0",
        "asOf": inventory["evaluationContext"]["asOf"],
        "settlementCurrency": inventory["evaluationContext"]["settlementCurrency"],
        "coverageMetric": "LENDABLE_VALUE",
        "obligationAmount": amount,
        "currentPostedLotIds": [] if current_posted is None else current_posted,
    }
    if substitution_request is not None:
        obligation["substitutionRequest"] = substitution_request
    return obligation
