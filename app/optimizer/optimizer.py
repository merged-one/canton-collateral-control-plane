"""Deterministic first-pass collateral optimization engine."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from itertools import combinations
from pathlib import Path
from typing import Any

from optimizer_constants import (
    DECIMAL_CENTS,
    OBJECTIVE_ID,
    OBJECTIVE_SEQUENCE,
    REPORT_TYPE,
    REPORT_VERSION,
)


POLICY_ENGINE_DIR = Path(__file__).resolve().parents[1] / "policy-engine"
if str(POLICY_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(POLICY_ENGINE_DIR))

from evaluator import (  # noqa: E402
    InventoryInputError,
    finalize_screened_inventory,
    load_json,
    screen_inventory,
)


class OptimizationInputError(ValueError):
    """Raised when the optimization request cannot be processed."""


def optimize_collateral(
    policy: dict[str, Any],
    inventory: dict[str, Any],
    obligation: dict[str, Any],
) -> dict[str, Any]:
    _validate_obligation_shape(obligation)
    _validate_request_consistency(inventory, obligation)
    substitution_request = _substitution_request(obligation)
    must_replace_lot_ids = _must_replace_lot_ids(obligation)

    screened = screen_inventory(policy, inventory)
    lot_by_id = {
        lot["lotId"]: copy.deepcopy(lot)
        for lot in sorted(inventory["candidateLots"], key=lambda item: item["lotId"])
    }
    screened_result_by_id = {
        asset["lotId"]: copy.deepcopy(asset)
        for asset in sorted(screened["assetResults"], key=lambda item: item["lotId"])
    }
    current_posted_lot_ids = sorted(obligation.get("currentPostedLotIds", []))
    traces: list[dict[str, Any]] = []
    step = 1

    for asset in sorted(screened["assetResults"], key=lambda item: item["lotId"]):
        admissible = asset["decision"] == "ELIGIBLE" and asset["lendableValue"] > 0
        traces.append(
            _trace_entry(
                step=step,
                stage="SCREENING",
                outcome="ADMISSIBLE" if admissible else "BLOCKED",
                message=(
                    f"Screened lot {asset['lotId']} for non-concentration policy feasibility."
                ),
                lot_ids=[asset["lotId"]],
                reason_codes=[reason["code"] for reason in asset["reasons"]],
            )
        )
        step += 1

    candidate_universe = [
        _candidate_record(asset)
        for asset in sorted(screened["assetResults"], key=lambda item: item["lotId"])
    ]
    admissible_lot_ids = [
        candidate["lotId"]
        for candidate in candidate_universe
        if candidate["admissible"]
    ]

    current_portfolio = None
    if current_posted_lot_ids:
        current_portfolio = _evaluate_portfolio(
            policy,
            inventory,
            obligation,
            current_posted_lot_ids,
            lot_by_id,
            screened_result_by_id,
            screened["portfolioReasons"],
        )
        traces.append(
            _trace_entry(
                step=step,
                stage="CURRENT_PORTFOLIO",
                outcome="FEASIBLE" if current_portfolio["isFeasible"] else "BLOCKED",
                message=(
                    "Evaluated the currently posted lot set against coverage and portfolio-level policy constraints."
                ),
                lot_ids=current_portfolio["lotIds"],
                reason_codes=current_portfolio["blockingReasonCodes"],
                objective_snapshot=current_portfolio["objectiveVector"],
                coverage_amount=current_portfolio["allocatedLendableValue"],
            )
        )
        step += 1

    best_portfolio = None
    best_search_vector = None
    feasible_combination_count = 0
    considered_combination_count = 0
    global_blocking_codes = [reason["code"] for reason in screened["portfolioReasons"]]
    search_failure_reason_codes = set(global_blocking_codes)
    considered_replacement_portfolios = 0

    if not global_blocking_codes:
        for size in range(1, len(admissible_lot_ids) + 1):
            for subset in combinations(admissible_lot_ids, size):
                considered_combination_count += 1
                candidate_lot_ids = list(subset)
                if _retains_must_replace_lots(candidate_lot_ids, must_replace_lot_ids):
                    traces.append(
                        _trace_entry(
                            step=step,
                            stage="SEARCH",
                            outcome="BLOCKED_BY_SCOPE",
                            message=(
                                "Rejected the subset because it retains one or more lots that the substitution request requires to be released."
                            ),
                            lot_ids=sorted(candidate_lot_ids),
                            reason_codes=["SUBSTITUTION_LOT_RETENTION_NOT_ALLOWED"],
                        )
                    )
                    step += 1
                    continue

                considered_replacement_portfolios += 1
                candidate_portfolio = _evaluate_portfolio(
                    policy,
                    inventory,
                    obligation,
                    candidate_lot_ids,
                    lot_by_id,
                    screened_result_by_id,
                    screened["portfolioReasons"],
                )
                search_vector = _search_vector(candidate_portfolio["objectiveVector"])
                outcome = "BLOCKED"
                if candidate_portfolio["isFeasible"]:
                    feasible_combination_count += 1
                    if (
                        best_search_vector is None
                        or search_vector < best_search_vector
                    ):
                        best_search_vector = search_vector
                        best_portfolio = candidate_portfolio
                        outcome = "NEW_INCUMBENT"
                    else:
                        outcome = "FEASIBLE_BUT_INFERIOR"
                elif candidate_portfolio["blockingReasonCodes"]:
                    search_failure_reason_codes.update(
                        candidate_portfolio["blockingReasonCodes"]
                    )

                traces.append(
                    _trace_entry(
                        step=step,
                        stage="SEARCH",
                        outcome=outcome,
                        message=(
                            f"Evaluated subset {','.join(candidate_portfolio['lotIds'])}."
                        ),
                        lot_ids=candidate_portfolio["lotIds"],
                        reason_codes=candidate_portfolio["blockingReasonCodes"],
                        objective_snapshot=candidate_portfolio["objectiveVector"],
                        coverage_amount=candidate_portfolio["allocatedLendableValue"],
                    )
                )
                step += 1
    else:
        traces.append(
            _trace_entry(
                step=step,
                stage="SEARCH",
                outcome="BLOCKED",
                message=(
                    "Skipped subset search because the shared policy or settlement prerequisites reject the entire request."
                ),
                reason_codes=global_blocking_codes,
            )
        )
        step += 1

    if (
        substitution_request is not None
        and considered_replacement_portfolios == 0
        and not search_failure_reason_codes
    ):
        search_failure_reason_codes.add("SUBSTITUTION_LOT_RETENTION_NOT_ALLOWED")

    (
        status,
        recommended_action,
        recommended_portfolio,
        substitution_recommendation,
        final_reason_codes,
    ) = _select_recommendation(
        best_portfolio,
        current_portfolio,
        substitution_request=substitution_request,
        search_failure_reason_codes=sorted(search_failure_reason_codes),
    )

    traces.append(
        _trace_entry(
            step=step,
            stage="DECISION",
            outcome=recommended_action,
            message="Selected the final optimizer recommendation.",
            lot_ids=[] if recommended_portfolio is None else recommended_portfolio["lotIds"],
            reason_codes=final_reason_codes,
            objective_snapshot=None
            if recommended_portfolio is None
            else recommended_portfolio["objectiveVector"],
            coverage_amount=None
            if recommended_portfolio is None
            else recommended_portfolio["allocatedLendableValue"],
        )
    )

    optimization_id = _optimization_id(policy, inventory, obligation)
    obligation_amount = _money(obligation["obligationAmount"])
    portfolio_currency = inventory["evaluationContext"]["valuationCurrency"]

    return {
        "$schema": "../../reports/schemas/optimization-report.schema.json",
        "reportType": REPORT_TYPE,
        "reportVersion": REPORT_VERSION,
        "optimizationId": optimization_id,
        "status": status,
        "recommendedAction": recommended_action,
        "objective": {
            "objectiveId": OBJECTIVE_ID,
            "sequence": OBJECTIVE_SEQUENCE,
        },
        "policy": {
            "policyId": policy["policyId"],
            "policyVersion": policy["policyVersion"],
            "cplVersion": policy["cplVersion"],
            "profile": policy["profile"],
        },
        "inventory": {
            "inventorySetId": inventory["inventorySetId"],
            "inventoryVersion": inventory["inventoryVersion"],
            "asOf": inventory["evaluationContext"]["asOf"],
            "settlementCurrency": inventory["evaluationContext"]["settlementCurrency"],
            "valuationCurrency": portfolio_currency,
            "candidateLotCount": len(inventory["candidateLots"]),
        },
        "obligation": {
            "obligationId": obligation["obligationId"],
            "obligationVersion": obligation["obligationVersion"],
            "asOf": obligation["asOf"],
            "settlementCurrency": obligation["settlementCurrency"],
            "coverageMetric": obligation.get("coverageMetric", "LENDABLE_VALUE"),
            "obligationAmount": _json_number(obligation_amount),
            "currentPostedLotIds": current_posted_lot_ids,
            "substitutionRequest": (
                None
                if substitution_request is None
                else {
                    "requestId": substitution_request["requestId"],
                    "mustReplaceLotIds": must_replace_lot_ids,
                    "atomicityRequired": substitution_request["atomicityRequired"],
                }
            ),
        },
        "candidateUniverse": {
            "candidateLotCount": len(candidate_universe),
            "admissibleLotCount": len(admissible_lot_ids),
            "blockedLotCount": len(candidate_universe) - len(admissible_lot_ids),
            "consideredCombinationCount": considered_combination_count,
            "feasibleCombinationCount": feasible_combination_count,
            "screeningResults": candidate_universe,
        },
        "currentPortfolio": current_portfolio,
        "recommendedPortfolio": recommended_portfolio,
        "substitutionRecommendation": substitution_recommendation,
        "explanationTrace": traces,
    }


def default_output_path(report: dict[str, Any]) -> Path:
    return Path("reports/generated") / (
        f"{report['policy']['policyId']}-"
        f"{report['inventory']['inventorySetId']}-"
        f"{report['obligation']['obligationId']}-optimization-report.json"
    )


def write_report(report: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=True)
        handle.write("\n")
    return path


def _validate_obligation_shape(obligation: dict[str, Any]) -> None:
    required_fields = [
        "obligationId",
        "obligationVersion",
        "asOf",
        "settlementCurrency",
        "obligationAmount",
    ]
    for field in required_fields:
        if field not in obligation:
            raise OptimizationInputError(
                f"obligation input is missing required top-level field {field!r}"
            )

    coverage_metric = obligation.get("coverageMetric", "LENDABLE_VALUE")
    if coverage_metric != "LENDABLE_VALUE":
        raise OptimizationInputError(
            "obligation coverageMetric must be LENDABLE_VALUE for the first optimizer"
        )

    if _money(obligation["obligationAmount"]) <= Decimal("0"):
        raise OptimizationInputError("obligationAmount must be greater than zero")

    current_posted = obligation.get("currentPostedLotIds", [])
    if not isinstance(current_posted, list):
        raise OptimizationInputError("currentPostedLotIds must be an array when present")

    substitution_request = _substitution_request(obligation)
    if substitution_request is None:
        return

    required_request_fields = [
        "requestId",
        "mustReplaceLotIds",
        "atomicityRequired",
    ]
    for field in required_request_fields:
        if field not in substitution_request:
            raise OptimizationInputError(
                f"substitutionRequest is missing required field {field!r}"
            )

    if not substitution_request["requestId"]:
        raise OptimizationInputError("substitutionRequest.requestId must be non-empty")

    must_replace = substitution_request["mustReplaceLotIds"]
    if not isinstance(must_replace, list) or not must_replace:
        raise OptimizationInputError(
            "substitutionRequest.mustReplaceLotIds must be a non-empty array"
        )
    if len(must_replace) != len(set(must_replace)):
        raise OptimizationInputError(
            "substitutionRequest.mustReplaceLotIds must not contain duplicates"
        )
    if not isinstance(substitution_request["atomicityRequired"], bool):
        raise OptimizationInputError(
            "substitutionRequest.atomicityRequired must be a boolean"
        )


def _validate_request_consistency(
    inventory: dict[str, Any],
    obligation: dict[str, Any],
) -> None:
    lot_ids = [lot["lotId"] for lot in inventory["candidateLots"]]
    if len(lot_ids) != len(set(lot_ids)):
        raise OptimizationInputError("inventory candidate lots must use unique lotId values")

    if obligation["settlementCurrency"] != inventory["evaluationContext"]["settlementCurrency"]:
        raise OptimizationInputError(
            "obligation settlementCurrency must match inventory evaluationContext settlementCurrency"
        )

    if obligation["asOf"] != inventory["evaluationContext"]["asOf"]:
        raise OptimizationInputError(
            "obligation asOf must match inventory evaluationContext asOf for deterministic coverage review"
        )

    unknown_current_ids = sorted(
        set(obligation.get("currentPostedLotIds", [])) - set(lot_ids)
    )
    if unknown_current_ids:
        raise OptimizationInputError(
            "currentPostedLotIds references unknown inventory lots: "
            + ", ".join(unknown_current_ids)
        )

    substitution_request = _substitution_request(obligation)
    if substitution_request is None:
        return

    unknown_must_replace = sorted(
        set(substitution_request["mustReplaceLotIds"]) - set(lot_ids)
    )
    if unknown_must_replace:
        raise OptimizationInputError(
            "substitutionRequest.mustReplaceLotIds references unknown inventory lots: "
            + ", ".join(unknown_must_replace)
        )

    missing_from_current = sorted(
        set(substitution_request["mustReplaceLotIds"])
        - set(obligation.get("currentPostedLotIds", []))
    )
    if missing_from_current:
        raise OptimizationInputError(
            "substitutionRequest.mustReplaceLotIds must be a subset of currentPostedLotIds: "
            + ", ".join(missing_from_current)
        )


def _candidate_record(asset: dict[str, Any]) -> dict[str, Any]:
    return {
        "lotId": asset["lotId"],
        "assetId": asset["assetId"],
        "assetClass": asset["assetClass"],
        "issuerId": asset["issuerId"],
        "marketValue": asset["marketValue"],
        "lendableValue": asset["lendableValue"],
        "totalHaircutBps": asset["totalHaircutBps"],
        "admissible": asset["decision"] == "ELIGIBLE" and asset["lendableValue"] > 0,
        "reasonCodes": [reason["code"] for reason in asset["reasons"]],
    }


def _evaluate_portfolio(
    policy: dict[str, Any],
    inventory: dict[str, Any],
    obligation: dict[str, Any],
    lot_ids: list[str],
    lot_by_id: dict[str, dict[str, Any]],
    screened_result_by_id: dict[str, dict[str, Any]],
    portfolio_reasons: list[dict[str, Any]],
) -> dict[str, Any]:
    subset_lot_ids = sorted(lot_ids)
    subset_inventory = {
        "inventorySetId": inventory["inventorySetId"],
        "inventoryVersion": inventory["inventoryVersion"],
        "evaluationContext": copy.deepcopy(inventory["evaluationContext"]),
        "candidateLots": [copy.deepcopy(lot_by_id[lot_id]) for lot_id in subset_lot_ids],
    }
    subset_report = finalize_screened_inventory(
        policy,
        subset_inventory,
        [copy.deepcopy(screened_result_by_id[lot_id]) for lot_id in subset_lot_ids],
        portfolio_reasons=portfolio_reasons,
    )

    allocated_lendable = _money(subset_report["summary"]["totalLendableValue"])
    allocated_market = _money(subset_report["summary"]["totalMarketValue"])
    required_amount = _money(obligation["obligationAmount"])
    shortfall = max(Decimal("0"), required_amount - allocated_lendable)
    excess = max(Decimal("0"), allocated_lendable - required_amount)
    haircut_cost = sum(
        (
            _money(asset["valuationBasisValue"]) - _money(asset["lendableValue"])
            for asset in subset_report["assetResults"]
        ),
        start=Decimal("0"),
    )

    blocking_reason_codes = _blocking_reason_codes(subset_report, shortfall)
    objective_vector = {
        "marketValueAmount": _json_number(allocated_market),
        "haircutCostAmount": _json_number(haircut_cost),
        "excessAmount": _json_number(excess),
        "lotCount": len(subset_lot_ids),
        "tieBreakLotIds": subset_lot_ids,
    }

    return {
        "lotIds": subset_lot_ids,
        "policyEvaluationId": subset_report["evaluationId"],
        "policyDecision": subset_report["overallDecision"],
        "isFeasible": subset_report["overallDecision"] == "ACCEPT" and shortfall == 0,
        "requiredAmount": _json_number(required_amount),
        "allocatedMarketValue": _json_number(allocated_market),
        "allocatedLendableValue": _json_number(allocated_lendable),
        "shortfallAmount": _json_number(shortfall),
        "excessAmount": _json_number(excess),
        "haircutCostAmount": _json_number(haircut_cost),
        "lotCount": len(subset_lot_ids),
        "objectiveVector": objective_vector,
        "blockingReasonCodes": blocking_reason_codes,
        "selectedLots": [
            {
                "lotId": asset["lotId"],
                "assetId": asset["assetId"],
                "issuerId": asset["issuerId"],
                "assetClass": asset["assetClass"],
                "marketValue": asset["marketValue"],
                "valuationBasisValue": asset["valuationBasisValue"],
                "lendableValue": asset["lendableValue"],
                "totalHaircutBps": asset["totalHaircutBps"],
            }
            for asset in sorted(subset_report["assetResults"], key=lambda item: item["lotId"])
        ],
        "concentrationResults": subset_report["concentrationResults"],
    }


def _select_recommendation(
    best_portfolio: dict[str, Any] | None,
    current_portfolio: dict[str, Any] | None,
    *,
    substitution_request: dict[str, Any] | None,
    search_failure_reason_codes: list[str],
) -> tuple[str, str, dict[str, Any] | None, dict[str, Any], list[str]]:
    must_replace_lot_ids = [] if substitution_request is None else sorted(
        substitution_request["mustReplaceLotIds"]
    )
    atomicity_required = (
        False
        if substitution_request is None
        else substitution_request["atomicityRequired"]
    )
    request_id = None if substitution_request is None else substitution_request["requestId"]

    def recommendation_for(
        current_lot_ids: list[str],
        recommended_lot_ids: list[str],
        *,
        improves_objective: bool,
    ) -> dict[str, Any]:
        return {
            "requestId": request_id,
            "atomicityRequired": atomicity_required,
            "mustReplaceLotIds": must_replace_lot_ids,
            "currentPostedLotIds": current_lot_ids,
            "recommendedLotIds": recommended_lot_ids,
            "retainedLotIds": sorted(
                set(current_lot_ids).intersection(recommended_lot_ids)
            ),
            "removeLotIds": sorted(set(current_lot_ids) - set(recommended_lot_ids)),
            "addLotIds": sorted(set(recommended_lot_ids) - set(current_lot_ids)),
            "improvesObjective": improves_objective,
        }

    if best_portfolio is None:
        current_lot_ids = [] if current_portfolio is None else current_portfolio["lotIds"]
        return (
            "NO_SOLUTION",
            "NO_SOLUTION",
            None,
            recommendation_for(
                current_lot_ids,
                [],
                improves_objective=False,
            ),
            (
                search_failure_reason_codes
                or ([] if current_portfolio is None else current_portfolio["blockingReasonCodes"])
            ),
        )

    if current_portfolio is None:
        return (
            "OPTIMAL",
            "SUBSTITUTE" if substitution_request is not None else "POST_NEW_SET",
            best_portfolio,
            recommendation_for([], best_portfolio["lotIds"], improves_objective=True),
            [],
        )

    if not current_portfolio["isFeasible"]:
        return (
            "OPTIMAL",
            "SUBSTITUTE",
            best_portfolio,
            recommendation_for(
                current_portfolio["lotIds"],
                best_portfolio["lotIds"],
                improves_objective=True,
            ),
            current_portfolio["blockingReasonCodes"],
        )

    if substitution_request is not None:
        return (
            "OPTIMAL",
            "SUBSTITUTE",
            best_portfolio,
            recommendation_for(
                current_portfolio["lotIds"],
                best_portfolio["lotIds"],
                improves_objective=(
                    _economic_vector(best_portfolio["objectiveVector"])
                    < _economic_vector(current_portfolio["objectiveVector"])
                ),
            ),
            [],
        )

    if current_portfolio["lotIds"] == best_portfolio["lotIds"]:
        return (
            "OPTIMAL",
            "KEEP_CURRENT_POSTED_SET",
            current_portfolio,
            recommendation_for(
                current_portfolio["lotIds"],
                current_portfolio["lotIds"],
                improves_objective=False,
            ),
            [],
        )

    if _economic_vector(current_portfolio["objectiveVector"]) <= _economic_vector(
        best_portfolio["objectiveVector"]
    ):
        return (
            "OPTIMAL",
            "KEEP_CURRENT_POSTED_SET",
            current_portfolio,
            recommendation_for(
                current_portfolio["lotIds"],
                current_portfolio["lotIds"],
                improves_objective=False,
            ),
            [],
        )

    return (
        "OPTIMAL",
        "SUBSTITUTE",
        best_portfolio,
        recommendation_for(
            current_portfolio["lotIds"],
            best_portfolio["lotIds"],
            improves_objective=True,
        ),
        [],
    )


def _substitution_request(obligation: dict[str, Any]) -> dict[str, Any] | None:
    return obligation.get("substitutionRequest")


def _must_replace_lot_ids(obligation: dict[str, Any]) -> list[str]:
    substitution_request = _substitution_request(obligation)
    if substitution_request is None:
        return []
    return sorted(substitution_request["mustReplaceLotIds"])


def _retains_must_replace_lots(
    candidate_lot_ids: list[str],
    must_replace_lot_ids: list[str],
) -> bool:
    return bool(set(candidate_lot_ids).intersection(must_replace_lot_ids))


def _blocking_reason_codes(
    report: dict[str, Any],
    shortfall: Decimal,
) -> list[str]:
    reason_codes = {
        reason["code"] for reason in report["portfolioReasons"] if reason is not None
    }
    for asset in report["assetResults"]:
        reason_codes.update(reason["code"] for reason in asset["reasons"])
    if shortfall > 0:
        reason_codes.add("INSUFFICIENT_LENDABLE_VALUE")
    return sorted(reason_codes)


def _trace_entry(
    *,
    step: int,
    stage: str,
    outcome: str,
    message: str,
    lot_ids: list[str] | None = None,
    reason_codes: list[str] | None = None,
    objective_snapshot: dict[str, Any] | None = None,
    coverage_amount: float | None = None,
) -> dict[str, Any]:
    return {
        "step": step,
        "stage": stage,
        "outcome": outcome,
        "message": message,
        "lotIds": [] if lot_ids is None else lot_ids,
        "reasonCodes": [] if reason_codes is None else sorted(reason_codes),
        "coverageAmount": coverage_amount,
        "objectiveSnapshot": objective_snapshot,
    }


def _optimization_id(
    policy: dict[str, Any],
    inventory: dict[str, Any],
    obligation: dict[str, Any],
) -> str:
    canonical = json.dumps(
        {"policy": policy, "inventory": inventory, "obligation": obligation},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"opr-{digest[:16]}"


def _search_vector(objective_vector: dict[str, Any]) -> tuple[Any, ...]:
    return (
        Decimal(str(objective_vector["marketValueAmount"])),
        Decimal(str(objective_vector["haircutCostAmount"])),
        Decimal(str(objective_vector["excessAmount"])),
        objective_vector["lotCount"],
        tuple(objective_vector["tieBreakLotIds"]),
    )


def _economic_vector(objective_vector: dict[str, Any]) -> tuple[Any, ...]:
    return (
        Decimal(str(objective_vector["marketValueAmount"])),
        Decimal(str(objective_vector["haircutCostAmount"])),
        Decimal(str(objective_vector["excessAmount"])),
        objective_vector["lotCount"],
    )


def _money(value: Any) -> Decimal:
    return Decimal(str(value))


def _json_number(value: Decimal) -> float:
    return float(value.quantize(DECIMAL_CENTS, rounding=ROUND_HALF_UP))
