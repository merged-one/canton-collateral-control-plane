"""Deterministic CPL v0.1 policy evaluation engine."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from constants import (
    ASSET_REQUIRED_FIELDS,
    DECIMAL_CENTS,
    DECIMAL_RATIO,
    RATING_STRENGTH,
    REPORT_TYPE,
    REPORT_VERSION,
    ROUNDING_MODES,
    SEVERITY_ORDER,
)


class InventoryInputError(ValueError):
    """Raised when the inventory input cannot be evaluated."""


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def evaluate_policy(
    policy: dict[str, Any],
    inventory: dict[str, Any],
) -> dict[str, Any]:
    _validate_inventory_shape(inventory)

    evaluation_context = inventory["evaluationContext"]
    candidate_lots = sorted(
        inventory["candidateLots"], key=lambda lot: lot.get("lotId", "")
    )
    valuation_currency = evaluation_context["valuationCurrency"]
    settlement_currency = evaluation_context["settlementCurrency"]
    policy_rounding = policy["haircuts"]["roundingMode"]

    portfolio_reasons = []

    if not _policy_is_effective(policy, evaluation_context["asOf"]):
        portfolio_reasons.append(
            _reason(
                code="POLICY_NOT_EFFECTIVE",
                category="POLICY",
                severity="REJECT",
                message=(
                    "The evaluation timestamp falls outside the policy effective period."
                ),
                policy_path="effectivePeriod",
            )
        )

    if settlement_currency not in policy["settlement"]["currencyConstraints"][
        "allowedSettlementCurrencies"
    ]:
        portfolio_reasons.append(
            _reason(
                code="SETTLEMENT_CURRENCY_NOT_ALLOWED",
                category="SETTLEMENT",
                severity="REJECT",
                message=(
                    f"Settlement currency {settlement_currency} is not allowed by the policy."
                ),
                policy_path="settlement.currencyConstraints.allowedSettlementCurrencies",
                currency=settlement_currency,
            )
        )

    asset_evaluations = [
        _evaluate_lot(policy, evaluation_context, lot) for lot in candidate_lots
    ]
    concentration_results, concentration_reasons = _evaluate_concentration_limits(
        policy,
        evaluation_context,
        asset_evaluations,
        valuation_currency,
    )

    for lot_id, reasons in concentration_reasons.items():
        for asset in asset_evaluations:
            if asset["lotId"] == lot_id:
                asset["reasons"].extend(reasons)
                break

    for asset in asset_evaluations:
        asset["reasons"] = _sorted_reasons(asset["reasons"])
        asset["decision"] = _asset_decision(asset["reasons"])

    portfolio_reasons = _sorted_reasons(
        portfolio_reasons
        + [
            result["reason"]
            for result in concentration_results
            if result["reason"] is not None
        ]
    )

    summary = _build_summary(asset_evaluations, concentration_results)
    overall_decision = _overall_decision(asset_evaluations, portfolio_reasons)
    evaluation_id = _evaluation_id(policy, inventory)

    return {
        "$schema": "../../reports/schemas/policy-evaluation-report.schema.json",
        "reportType": REPORT_TYPE,
        "reportVersion": REPORT_VERSION,
        "evaluationId": evaluation_id,
        "overallDecision": overall_decision,
        "policy": {
            "policyId": policy["policyId"],
            "policyVersion": policy["policyVersion"],
            "cplVersion": policy["cplVersion"],
            "profile": policy["profile"],
        },
        "inventory": {
            "inventorySetId": inventory["inventorySetId"],
            "inventoryVersion": inventory["inventoryVersion"],
            "asOf": evaluation_context["asOf"],
            "settlementCurrency": settlement_currency,
            "valuationCurrency": valuation_currency,
            "candidateLotCount": len(candidate_lots),
        },
        "summary": summary,
        "portfolioReasons": portfolio_reasons,
        "assetResults": asset_evaluations,
        "concentrationResults": concentration_results,
    }


def default_output_path(report: dict[str, Any]) -> Path:
    policy_id = report["policy"]["policyId"]
    inventory_id = report["inventory"]["inventorySetId"]
    return Path("reports/generated") / (
        f"{policy_id}-{inventory_id}-policy-evaluation-report.json"
    )


def write_report(report: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=True)
        handle.write("\n")
    return path


def _validate_inventory_shape(inventory: dict[str, Any]) -> None:
    required_top_level = [
        "inventorySetId",
        "inventoryVersion",
        "evaluationContext",
        "candidateLots",
    ]
    for field in required_top_level:
        if field not in inventory:
            raise InventoryInputError(
                f"inventory input is missing required top-level field {field!r}"
            )

    required_context = [
        "asOf",
        "settlementCurrency",
        "valuationCurrency",
        "providerIssuerIds",
        "exposureCounterparties",
    ]
    for field in required_context:
        if field not in inventory["evaluationContext"]:
            raise InventoryInputError(
                f"inventory evaluationContext is missing required field {field!r}"
            )

    if not isinstance(inventory["candidateLots"], list) or not inventory["candidateLots"]:
        raise InventoryInputError(
            "inventory candidateLots must be a non-empty array of candidate lots"
        )


def _evaluate_lot(
    policy: dict[str, Any],
    evaluation_context: dict[str, Any],
    lot: dict[str, Any],
) -> dict[str, Any]:
    reasons = []
    missing_fields = [field for field in ASSET_REQUIRED_FIELDS if field not in lot]
    for field in missing_fields:
        reasons.append(
            _reason(
                code="MISSING_REQUIRED_LOT_FIELD",
                category="INPUT",
                severity="REJECT",
                message=f"Candidate lot is missing required field {field}.",
                policy_path="inventory.candidateLots",
            )
        )

    market_value = _money(lot.get("marketValue", 0))
    nominal_value = _money(lot.get("nominalValue", 0))
    outstanding_principal = _money(lot.get("outstandingPrincipal", 0))

    if lot.get("assetClass") not in policy["eligibility"]["eligibleAssetClasses"]:
        reasons.append(
            _reason(
                code="ASSET_CLASS_NOT_ELIGIBLE",
                category="ELIGIBILITY",
                severity="REJECT",
                message=(
                    f"Asset class {lot.get('assetClass')} is not listed in eligibleAssetClasses."
                ),
                policy_path="eligibility.eligibleAssetClasses",
            )
        )

    if lot.get("issueType") not in policy["eligibility"]["eligibleIssueTypes"]:
        reasons.append(
            _reason(
                code="ISSUE_TYPE_NOT_ELIGIBLE",
                category="ELIGIBILITY",
                severity="REJECT",
                message=(
                    f"Issue type {lot.get('issueType')} is not listed in eligibleIssueTypes."
                ),
                policy_path="eligibility.eligibleIssueTypes",
            )
        )

    reasons.extend(_evaluate_issuer_filters(policy["eligibility"]["issuerFilters"], evaluation_context, lot))
    reasons.extend(_evaluate_custodian_filters(policy["eligibility"]["custodianFilters"], lot))
    reasons.extend(
        _evaluate_jurisdiction_filters(policy["eligibility"]["jurisdictionFilters"], lot)
    )
    reasons.extend(
        _evaluate_settlement_currency(policy["settlement"]["currencyConstraints"], evaluation_context, lot)
    )
    reasons.extend(_evaluate_control_requirements(policy["controlRequirements"], lot))
    reasons.extend(
        _evaluate_wrong_way_risk(policy["wrongWayRiskExclusions"], evaluation_context, lot)
    )

    valuation_basis_value = _valuation_basis_value(
        policy["haircuts"]["valuationBasis"],
        market_value,
        nominal_value,
        outstanding_principal,
    )

    matched_rules = [
        rule
        for rule in policy["haircuts"]["schedule"]
        if _selectors_match(rule["selectors"], lot)
    ]
    matched_rule_ids = sorted(rule["ruleId"] for rule in matched_rules)
    applied_rule_ids = []
    base_haircut_bps = None
    mismatch_haircut_bps = 0
    total_haircut_bps = None
    lendable_value = Decimal("0")

    if not matched_rules:
        reasons.append(
            _reason(
                code="HAIRCUT_RULE_NOT_FOUND",
                category="HAIRCUT",
                severity="REJECT",
                message="No haircut rule matched the candidate lot selectors.",
                policy_path="haircuts.schedule",
            )
        )
    else:
        base_haircut_bps = max(rule["haircutBps"] for rule in matched_rules)
        applied_rule_ids = sorted(
            rule["ruleId"] for rule in matched_rules if rule["haircutBps"] == base_haircut_bps
        )
        if policy["settlement"]["currencyConstraints"][
            "requireSettlementCurrencyInHaircutSchedule"
        ]:
            settlement_currency = evaluation_context["settlementCurrency"]
            schedule_covers_settlement = any(
                "currencies" not in rule["selectors"]
                or settlement_currency in rule["selectors"]["currencies"]
                for rule in matched_rules
            )
            if not schedule_covers_settlement:
                reasons.append(
                    _reason(
                        code="SETTLEMENT_CURRENCY_NOT_COVERED_BY_HAIRCUT_SCHEDULE",
                        category="HAIRCUT",
                        severity="REJECT",
                        message=(
                            f"Settlement currency {settlement_currency} is not covered by the matched haircut schedule."
                        ),
                        policy_path="settlement.currencyConstraints.requireSettlementCurrencyInHaircutSchedule",
                        currency=settlement_currency,
                    )
                )

        mismatch_haircut_bps = _currency_mismatch_haircut_bps(
            policy,
            evaluation_context,
            lot,
        )
        total_haircut_bps = min(10000, base_haircut_bps + mismatch_haircut_bps)
        lendable_ratio = (Decimal(10000) - Decimal(total_haircut_bps)) / Decimal(10000)
        lendable_value = _round_money(
            valuation_basis_value * lendable_ratio,
            policy["haircuts"]["roundingMode"],
        )

    return {
        "lotId": lot.get("lotId"),
        "assetId": lot.get("assetId"),
        "decision": "ELIGIBLE",
        "assetClass": lot.get("assetClass"),
        "issueType": lot.get("issueType"),
        "issuerId": lot.get("issuerId"),
        "issuerType": lot.get("issuerType"),
        "issuerGroupIds": sorted(lot.get("issuerGroupIds", [])),
        "longTermRating": lot.get("longTermRating"),
        "collateralCurrency": lot.get("currency"),
        "issuanceJurisdiction": lot.get("issuanceJurisdiction"),
        "riskJurisdiction": lot.get("riskJurisdiction"),
        "custodianId": lot.get("custodianId"),
        "custodyJurisdiction": lot.get("custodyJurisdiction"),
        "accountType": lot.get("accountType"),
        "residualMaturityDays": lot.get("residualMaturityDays"),
        "marketValue": _json_number(market_value),
        "valuationBasisValue": _json_number(valuation_basis_value),
        "baseHaircutBps": base_haircut_bps,
        "currencyMismatchHaircutBps": mismatch_haircut_bps,
        "totalHaircutBps": total_haircut_bps,
        "matchedHaircutRuleIds": matched_rule_ids,
        "appliedHaircutRuleIds": applied_rule_ids,
        "lendableValue": _json_number(lendable_value),
        "reasons": reasons,
    }


def _evaluate_issuer_filters(
    issuer_filters: dict[str, Any],
    evaluation_context: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []

    issuer_id = lot.get("issuerId")
    issuer_type = lot.get("issuerType")
    rating = lot.get("longTermRating", "UNRATED")

    if issuer_type not in issuer_filters["allowedIssuerTypes"]:
        reasons.append(
            _reason(
                code="ISSUER_TYPE_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer type {issuer_type} is not allowed by issuerFilters.",
                policy_path="eligibility.issuerFilters.allowedIssuerTypes",
            )
        )

    if "allowListedIssuerIds" in issuer_filters and issuer_id not in issuer_filters["allowListedIssuerIds"]:
        reasons.append(
            _reason(
                code="ISSUER_NOT_ON_ALLOW_LIST",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer {issuer_id} is not present in allowListedIssuerIds.",
                policy_path="eligibility.issuerFilters.allowListedIssuerIds",
            )
        )

    if "denyListedIssuerIds" in issuer_filters and issuer_id in issuer_filters["denyListedIssuerIds"]:
        reasons.append(
            _reason(
                code="ISSUER_DENY_LISTED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer {issuer_id} is deny-listed by issuerFilters.",
                policy_path="eligibility.issuerFilters.denyListedIssuerIds",
            )
        )

    minimum_rating = issuer_filters.get("minimumLongTermRating")
    if rating == "UNRATED" and not issuer_filters.get("allowUnratedIssuers", False):
        reasons.append(
            _reason(
                code="UNRATED_ISSUER_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message="Unrated issuers are not allowed by issuerFilters.",
                policy_path="eligibility.issuerFilters.allowUnratedIssuers",
            )
        )
    elif minimum_rating and not _rating_meets_minimum(rating, minimum_rating):
        reasons.append(
            _reason(
                code="ISSUER_RATING_BELOW_MINIMUM",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer rating {rating} is below the minimum {minimum_rating}.",
                policy_path="eligibility.issuerFilters.minimumLongTermRating",
            )
        )

    provider_issuer_ids = set(evaluation_context["providerIssuerIds"])
    if not issuer_filters.get("allowSelfIssued", False) and issuer_id in provider_issuer_ids:
        reasons.append(
            _reason(
                code="SELF_ISSUED_COLLATERAL_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer {issuer_id} is treated as self-issued collateral.",
                policy_path="eligibility.issuerFilters.allowSelfIssued",
            )
        )

    counterparty_issuer_ids = set()
    for counterparty in evaluation_context["exposureCounterparties"]:
        counterparty_issuer_ids.update(counterparty.get("issuerIds", [counterparty["partyId"]]))
    if (
        not issuer_filters.get("allowCounterpartyIssued", False)
        and issuer_id in counterparty_issuer_ids
    ):
        reasons.append(
            _reason(
                code="COUNTERPARTY_ISSUED_COLLATERAL_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Issuer {issuer_id} matches an exposure counterparty issuer identifier.",
                policy_path="eligibility.issuerFilters.allowCounterpartyIssued",
            )
        )

    return reasons


def _evaluate_custodian_filters(
    custodian_filters: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []
    if lot.get("custodianId") not in custodian_filters["allowedCustodianIds"]:
        reasons.append(
            _reason(
                code="CUSTODIAN_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Custodian {lot.get('custodianId')} is not allowed.",
                policy_path="eligibility.custodianFilters.allowedCustodianIds",
            )
        )

    if "deniedCustodianIds" in custodian_filters and lot.get("custodianId") in custodian_filters["deniedCustodianIds"]:
        reasons.append(
            _reason(
                code="CUSTODIAN_DENIED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Custodian {lot.get('custodianId')} is explicitly denied.",
                policy_path="eligibility.custodianFilters.deniedCustodianIds",
            )
        )

    if lot.get("accountType") not in custodian_filters["allowedAccountTypes"]:
        reasons.append(
            _reason(
                code="ACCOUNT_TYPE_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Account type {lot.get('accountType')} is not allowed.",
                policy_path="eligibility.custodianFilters.allowedAccountTypes",
            )
        )

    if custodian_filters["requireSegregatedAccount"] and not lot.get("isSegregated", False):
        reasons.append(
            _reason(
                code="SEGREGATED_ACCOUNT_REQUIRED",
                category="CONTROL",
                severity="REJECT",
                message="The policy requires a segregated account for custody.",
                policy_path="eligibility.custodianFilters.requireSegregatedAccount",
            )
        )

    if custodian_filters["requireControlAgreement"] and not lot.get("hasControlAgreement", False):
        reasons.append(
            _reason(
                code="CONTROL_AGREEMENT_REQUIRED",
                category="CONTROL",
                severity="REJECT",
                message="The policy requires a control agreement for custody.",
                policy_path="eligibility.custodianFilters.requireControlAgreement",
            )
        )

    if not custodian_filters["allowInternalCustody"] and lot.get("isInternalCustody", False):
        reasons.append(
            _reason(
                code="INTERNAL_CUSTODY_NOT_ALLOWED",
                category="CONTROL",
                severity="REJECT",
                message="The policy does not allow internal custody for this collateral.",
                policy_path="eligibility.custodianFilters.allowInternalCustody",
            )
        )

    return reasons


def _evaluate_jurisdiction_filters(
    jurisdiction_filters: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []
    issuance_jurisdiction = lot.get("issuanceJurisdiction")
    risk_jurisdiction = lot.get("riskJurisdiction")
    custody_jurisdiction = lot.get("custodyJurisdiction")

    if issuance_jurisdiction not in jurisdiction_filters["allowedIssuanceJurisdictions"]:
        reasons.append(
            _reason(
                code="ISSUANCE_JURISDICTION_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=(
                    f"Issuance jurisdiction {issuance_jurisdiction} is not allowed."
                ),
                policy_path="eligibility.jurisdictionFilters.allowedIssuanceJurisdictions",
            )
        )

    if risk_jurisdiction not in jurisdiction_filters["allowedRiskJurisdictions"]:
        reasons.append(
            _reason(
                code="RISK_JURISDICTION_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Risk jurisdiction {risk_jurisdiction} is not allowed.",
                policy_path="eligibility.jurisdictionFilters.allowedRiskJurisdictions",
            )
        )

    if custody_jurisdiction not in jurisdiction_filters["allowedCustodyJurisdictions"]:
        reasons.append(
            _reason(
                code="CUSTODY_JURISDICTION_NOT_ALLOWED",
                category="ELIGIBILITY",
                severity="REJECT",
                message=f"Custody jurisdiction {custody_jurisdiction} is not allowed.",
                policy_path="eligibility.jurisdictionFilters.allowedCustodyJurisdictions",
            )
        )

    excluded = jurisdiction_filters.get("excludedJurisdictions", [])
    if (
        issuance_jurisdiction in excluded
        or risk_jurisdiction in excluded
        or custody_jurisdiction in excluded
    ):
        reasons.append(
            _reason(
                code="EXCLUDED_JURISDICTION",
                category="ELIGIBILITY",
                severity="REJECT",
                message="At least one jurisdiction field is explicitly excluded by the policy.",
                policy_path="eligibility.jurisdictionFilters.excludedJurisdictions",
            )
        )

    return reasons


def _evaluate_settlement_currency(
    currency_constraints: dict[str, Any],
    evaluation_context: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []
    settlement_currency = evaluation_context["settlementCurrency"]
    collateral_currency = lot.get("currency")

    if settlement_currency not in currency_constraints["allowedSettlementCurrencies"]:
        reasons.append(
            _reason(
                code="SETTLEMENT_CURRENCY_NOT_ALLOWED",
                category="SETTLEMENT",
                severity="REJECT",
                message=(
                    f"Settlement currency {settlement_currency} is not allowed by the policy."
                ),
                policy_path="settlement.currencyConstraints.allowedSettlementCurrencies",
                currency=settlement_currency,
            )
        )

    if (
        collateral_currency != settlement_currency
        and not currency_constraints["allowCollateralCurrencyMismatch"]
    ):
        reasons.append(
            _reason(
                code="COLLATERAL_CURRENCY_MISMATCH_NOT_ALLOWED",
                category="SETTLEMENT",
                severity="REJECT",
                message=(
                    f"Collateral currency {collateral_currency} does not match settlement currency {settlement_currency}."
                ),
                policy_path="settlement.currencyConstraints.allowCollateralCurrencyMismatch",
                currency=collateral_currency,
            )
        )

    return reasons


def _evaluate_control_requirements(
    control_requirements: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []
    encumbrance = control_requirements["encumbrance"]
    segregation = control_requirements["segregation"]

    if encumbrance["requireUnencumbered"] and lot.get("isEncumbered", False):
        reasons.append(
            _reason(
                code="ENCUMBERED_COLLATERAL_NOT_ALLOWED",
                category="CONTROL",
                severity="REJECT",
                message="The policy requires the collateral to be unencumbered.",
                policy_path="controlRequirements.encumbrance.requireUnencumbered",
            )
        )

    if not encumbrance["allowReuse"] and lot.get("isReuseOfReceivedCollateral", False):
        reasons.append(
            _reason(
                code="REUSE_NOT_ALLOWED",
                category="CONTROL",
                severity="REJECT",
                message="The policy does not allow reuse of received collateral.",
                policy_path="controlRequirements.encumbrance.allowReuse",
            )
        )

    free_allocation_percent = Decimal(str(lot.get("freeAllocationPercent", 0)))
    minimum_free_allocation = Decimal(
        str(encumbrance["minimumFreeAllocationPercent"])
    )
    if free_allocation_percent < minimum_free_allocation:
        reasons.append(
            _reason(
                code="FREE_ALLOCATION_BELOW_MINIMUM",
                category="CONTROL",
                severity="REJECT",
                message=(
                    f"Free allocation percent {free_allocation_percent} is below the minimum {minimum_free_allocation}."
                ),
                policy_path="controlRequirements.encumbrance.minimumFreeAllocationPercent",
                observed_value=float(free_allocation_percent),
                threshold_value=float(minimum_free_allocation),
            )
        )

    if segregation["required"] and lot.get("segregationType") != segregation["segregationType"]:
        reasons.append(
            _reason(
                code="SEGREGATION_TYPE_MISMATCH",
                category="CONTROL",
                severity="REJECT",
                message=(
                    f"Segregation type {lot.get('segregationType')} does not satisfy required type {segregation['segregationType']}."
                ),
                policy_path="controlRequirements.segregation.segregationType",
            )
        )

    eligible_designations = segregation.get("eligibleAccountDesignations", [])
    account_designation = lot.get("accountDesignation")
    if eligible_designations and account_designation not in eligible_designations:
        reasons.append(
            _reason(
                code="ACCOUNT_DESIGNATION_NOT_ALLOWED",
                category="CONTROL",
                severity="REJECT",
                message=(
                    f"Account designation {account_designation} is not permitted by segregation requirements."
                ),
                policy_path="controlRequirements.segregation.eligibleAccountDesignations",
            )
        )

    if (
        segregation["requireThirdPartyAcknowledgement"]
        and not lot.get("thirdPartyAcknowledgementReceived", False)
    ):
        reasons.append(
            _reason(
                code="THIRD_PARTY_ACKNOWLEDGEMENT_REQUIRED",
                category="CONTROL",
                severity="REJECT",
                message="Third-party acknowledgement is required by the segregation controls.",
                policy_path="controlRequirements.segregation.requireThirdPartyAcknowledgement",
            )
        )

    return reasons


def _evaluate_wrong_way_risk(
    exclusions: list[dict[str, Any]],
    evaluation_context: dict[str, Any],
    lot: dict[str, Any],
) -> list[dict[str, Any]]:
    reasons = []
    issuer_id = lot.get("issuerId")
    issuer_group_ids = set(lot.get("issuerGroupIds", []))
    issuance_jurisdiction = lot.get("issuanceJurisdiction")

    for exclusion in sorted(exclusions, key=lambda item: item["exclusionId"]):
        if exclusion["type"] == "ISSUER_EQUALS_EXPOSURE_COUNTERPARTY":
            if any(
                issuer_id in set(counterparty.get("issuerIds", [counterparty["partyId"]]))
                for counterparty in _matched_counterparties(
                    evaluation_context["exposureCounterparties"],
                    exclusion.get("matchExposureCounterpartyRole", "ANY"),
                )
            ):
                reasons.append(
                    _reason(
                        code=_wrong_way_code(exclusion["action"]),
                        category="WRONG_WAY_RISK",
                        severity=exclusion["action"],
                        message=(
                            f"Issuer {issuer_id} matches an exposure counterparty for exclusion {exclusion['exclusionId']}."
                        ),
                        policy_path="wrongWayRiskExclusions",
                        policy_rule_id=exclusion["exclusionId"],
                    )
                )

        elif exclusion["type"] == "ISSUER_IN_COUNTERPARTY_GROUP":
            if issuer_group_ids.intersection(set(exclusion["counterpartyGroupIds"])):
                reasons.append(
                    _reason(
                        code=_wrong_way_code(exclusion["action"]),
                        category="WRONG_WAY_RISK",
                        severity=exclusion["action"],
                        message=(
                            f"Issuer groups {sorted(issuer_group_ids)} intersect exclusion groups {sorted(exclusion['counterpartyGroupIds'])}."
                        ),
                        policy_path="wrongWayRiskExclusions",
                        policy_rule_id=exclusion["exclusionId"],
                    )
                )

        elif exclusion["type"] == "ISSUER_COUNTRY_EQUALS_EXPOSURE_COUNTRY":
            exposure_countries = {
                counterparty.get("country")
                for counterparty in evaluation_context["exposureCounterparties"]
                if counterparty.get("country")
            }
            if (
                issuance_jurisdiction in set(exclusion["jurisdictions"])
                and issuance_jurisdiction in exposure_countries
            ):
                reasons.append(
                    _reason(
                        code=_wrong_way_code(exclusion["action"]),
                        category="WRONG_WAY_RISK",
                        severity=exclusion["action"],
                        message=(
                            f"Issuance jurisdiction {issuance_jurisdiction} matches an exposure country under exclusion {exclusion['exclusionId']}."
                        ),
                        policy_path="wrongWayRiskExclusions",
                        policy_rule_id=exclusion["exclusionId"],
                    )
                )

        elif exclusion["type"] == "CUSTOM_ISSUER_LIST":
            if issuer_id in set(exclusion["issuerIds"]):
                reasons.append(
                    _reason(
                        code=_wrong_way_code(exclusion["action"]),
                        category="WRONG_WAY_RISK",
                        severity=exclusion["action"],
                        message=(
                            f"Issuer {issuer_id} appears in custom wrong-way-risk exclusion {exclusion['exclusionId']}."
                        ),
                        policy_path="wrongWayRiskExclusions",
                        policy_rule_id=exclusion["exclusionId"],
                    )
                )

        elif exclusion["type"] == "CUSTOM_JURISDICTION_LIST":
            if issuance_jurisdiction in set(exclusion["jurisdictions"]):
                reasons.append(
                    _reason(
                        code=_wrong_way_code(exclusion["action"]),
                        category="WRONG_WAY_RISK",
                        severity=exclusion["action"],
                        message=(
                            f"Issuance jurisdiction {issuance_jurisdiction} appears in custom wrong-way-risk exclusion {exclusion['exclusionId']}."
                        ),
                        policy_path="wrongWayRiskExclusions",
                        policy_rule_id=exclusion["exclusionId"],
                    )
                )

    return reasons


def _currency_mismatch_haircut_bps(
    policy: dict[str, Any],
    evaluation_context: dict[str, Any],
    lot: dict[str, Any],
) -> int:
    settlement_currency = evaluation_context["settlementCurrency"]
    collateral_currency = lot.get("currency")
    if collateral_currency == settlement_currency:
        return 0

    if not policy["settlement"]["currencyConstraints"]["allowCollateralCurrencyMismatch"]:
        return 0

    for override in policy["haircuts"]["currencyMismatch"]["pairOverrides"]:
        if (
            override["collateralCurrency"] == collateral_currency
            and override["settlementCurrency"] == settlement_currency
        ):
            return override["haircutBps"]

    return policy["haircuts"]["currencyMismatch"]["defaultHaircutBps"]


def _evaluate_concentration_limits(
    policy: dict[str, Any],
    evaluation_context: dict[str, Any],
    asset_results: list[dict[str, Any]],
    valuation_currency: str,
) -> tuple[list[dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    included_assets = [
        asset
        for asset in asset_results
        if not _has_reject_reason(asset["reasons"]) and asset["lendableValue"] > 0
    ]
    total_collateral_value = sum(
        (_money(asset["valuationBasisValue"]) for asset in included_assets),
        start=Decimal("0"),
    )
    total_lendable_value = sum(
        (_money(asset["lendableValue"]) for asset in included_assets),
        start=Decimal("0"),
    )

    results = []
    asset_reasons: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for limit in sorted(policy["concentrationLimits"], key=lambda item: item["limitId"]):
        threshold = limit["threshold"]
        applicable_assets = included_assets
        if "appliesTo" in limit:
            applicable_assets = [
                asset for asset in included_assets if _selectors_match(limit["appliesTo"], asset)
            ]

        if threshold["metric"] == "ABSOLUTE_MARKET_VALUE" and threshold["currency"] != valuation_currency:
            reason = _reason(
                code="ABSOLUTE_LIMIT_CURRENCY_UNSUPPORTED",
                category="CONCENTRATION",
                severity="REJECT",
                message=(
                    f"Absolute market value limit {limit['limitId']} uses currency {threshold['currency']}, but the inventory valuation currency is {valuation_currency}."
                ),
                policy_path="concentrationLimits",
                policy_rule_id=limit["limitId"],
                currency=threshold["currency"],
            )
            results.append(
                {
                    "limitId": limit["limitId"],
                    "dimension": limit["dimension"],
                    "scope": limit["scope"],
                    "metric": threshold["metric"],
                    "decision": "REJECT",
                    "thresholdValue": _threshold_value(limit["threshold"]),
                    "thresholdCurrency": threshold["currency"],
                    "bucket": "__UNSUPPORTED__",
                    "bucketValue": 0,
                    "denominatorValue": 0,
                    "observedRatio": None,
                    "relatedLotIds": [],
                    "reason": reason,
                }
            )
            continue

        bucket_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for asset in applicable_assets:
            for bucket in _bucket_values(limit["dimension"], asset):
                bucket_map[bucket].append(asset)

        for bucket in sorted(bucket_map):
            bucket_assets = bucket_map[bucket]
            lot_ids = sorted(asset["lotId"] for asset in bucket_assets)
            observed_value = _observed_limit_value(threshold["metric"], bucket_assets)
            denominator = _limit_denominator(
                threshold["metric"],
                total_collateral_value,
                total_lendable_value,
            )
            observed_ratio = None
            breached = False

            if threshold["metric"] in (
                "PERCENT_OF_COLLATERAL_VALUE",
                "PERCENT_OF_LENDABLE_VALUE",
            ):
                observed_ratio = (
                    Decimal("0")
                    if denominator == 0
                    else observed_value / denominator
                )
                breached = observed_ratio > Decimal(str(threshold["value"]))
            else:
                breached = observed_value > _money(threshold["value"])

            decision = "PASS"
            reason = None
            if breached:
                decision = limit["breachAction"]
                reason = _reason(
                    code="CONCENTRATION_LIMIT_BREACH",
                    category="CONCENTRATION",
                    severity=limit["breachAction"],
                    message=(
                        f"Concentration limit {limit['limitId']} breached for bucket {bucket}."
                    ),
                    policy_path="concentrationLimits",
                    policy_rule_id=limit["limitId"],
                    related_lot_ids=lot_ids,
                    bucket=bucket,
                    observed_value=float(_quantize(observed_value, DECIMAL_CENTS)),
                    threshold_value=float(_threshold_decimal(threshold)),
                    currency=threshold.get("currency"),
                )
                for asset in bucket_assets:
                    asset_reasons[asset["lotId"]].append(reason)

            results.append(
                {
                    "limitId": limit["limitId"],
                    "dimension": limit["dimension"],
                    "scope": limit["scope"],
                    "metric": threshold["metric"],
                    "decision": decision,
                    "thresholdValue": _threshold_value(limit["threshold"]),
                    "thresholdCurrency": threshold.get("currency"),
                    "bucket": bucket,
                    "bucketValue": _json_number(observed_value),
                    "denominatorValue": _json_number(denominator),
                    "observedRatio": None
                    if observed_ratio is None
                    else float(_quantize(observed_ratio, DECIMAL_RATIO)),
                    "relatedLotIds": lot_ids,
                    "reason": reason,
                }
            )

    return results, asset_reasons


def _bucket_values(dimension: str, asset: dict[str, Any]) -> list[str]:
    if dimension == "ISSUER":
        return [asset["issuerId"]]
    if dimension == "ISSUER_GROUP":
        return sorted(asset.get("issuerGroupIds", []))
    if dimension == "ASSET_CLASS":
        return [asset["assetClass"]]
    if dimension == "ISSUE_TYPE":
        return [asset["issueType"]]
    if dimension == "CURRENCY":
        return [asset["collateralCurrency"]]
    if dimension == "JURISDICTION":
        return [asset.get("issuanceJurisdiction") or asset.get("riskJurisdiction")]
    if dimension == "CUSTODIAN":
        return [asset.get("custodianId")]
    return ["__UNKNOWN__"]


def _observed_limit_value(metric: str, bucket_assets: list[dict[str, Any]]) -> Decimal:
    field = {
        "PERCENT_OF_COLLATERAL_VALUE": "valuationBasisValue",
        "PERCENT_OF_LENDABLE_VALUE": "lendableValue",
        "ABSOLUTE_MARKET_VALUE": "marketValue",
    }[metric]
    return sum((_money(asset[field]) for asset in bucket_assets), start=Decimal("0"))


def _limit_denominator(
    metric: str,
    total_collateral_value: Decimal,
    total_lendable_value: Decimal,
) -> Decimal:
    if metric == "PERCENT_OF_COLLATERAL_VALUE":
        return total_collateral_value
    if metric == "PERCENT_OF_LENDABLE_VALUE":
        return total_lendable_value
    return Decimal("0")


def _selectors_match(selectors: dict[str, Any], asset: dict[str, Any]) -> bool:
    if "assetClasses" in selectors and asset.get("assetClass") not in selectors["assetClasses"]:
        return False
    if "issueTypes" in selectors and asset.get("issueType") not in selectors["issueTypes"]:
        return False
    if "issuerTypes" in selectors and asset.get("issuerType") not in selectors["issuerTypes"]:
        return False
    if "issuerIds" in selectors and asset.get("issuerId") not in selectors["issuerIds"]:
        return False
    if "currencies" in selectors and asset.get("currency", asset.get("collateralCurrency")) not in selectors["currencies"]:
        return False
    if (
        "issuanceJurisdictions" in selectors
        and asset.get("issuanceJurisdiction") not in selectors["issuanceJurisdictions"]
    ):
        return False
    if (
        "riskJurisdictions" in selectors
        and asset.get("riskJurisdiction") not in selectors["riskJurisdictions"]
    ):
        return False
    if "custodianIds" in selectors and asset.get("custodianId") not in selectors["custodianIds"]:
        return False
    if "minimumLongTermRating" in selectors and not _rating_meets_minimum(
        asset.get("longTermRating", "UNRATED"),
        selectors["minimumLongTermRating"],
    ):
        return False
    if "maximumLongTermRating" in selectors and not _rating_meets_maximum(
        asset.get("longTermRating", "UNRATED"),
        selectors["maximumLongTermRating"],
    ):
        return False
    if (
        "minResidualMaturityDays" in selectors
        and asset.get("residualMaturityDays", -1) < selectors["minResidualMaturityDays"]
    ):
        return False
    if (
        "maxResidualMaturityDays" in selectors
        and asset.get("residualMaturityDays", 10**12) > selectors["maxResidualMaturityDays"]
    ):
        return False
    return True


def _valuation_basis_value(
    valuation_basis: str,
    market_value: Decimal,
    nominal_value: Decimal,
    outstanding_principal: Decimal,
) -> Decimal:
    if valuation_basis == "MARKET_VALUE":
        return market_value
    if valuation_basis == "LOWER_OF_MARKET_AND_NOMINAL":
        return min(market_value, nominal_value)
    if valuation_basis == "LOWER_OF_MARKET_AND_OUTSTANDING_PRINCIPAL":
        return min(market_value, outstanding_principal)
    raise ValueError(f"unsupported valuation basis {valuation_basis}")


def _policy_is_effective(policy: dict[str, Any], as_of: str) -> bool:
    effective_from = _parse_datetime(policy["effectivePeriod"]["effectiveFrom"])
    effective_until = policy["effectivePeriod"].get("effectiveUntil")
    as_of_dt = _parse_datetime(as_of)
    if as_of_dt < effective_from:
        return False
    if effective_until is not None and as_of_dt >= _parse_datetime(effective_until):
        return False
    return True


def _matched_counterparties(
    counterparties: list[dict[str, Any]],
    role: str,
) -> list[dict[str, Any]]:
    if role == "ANY":
        return counterparties
    return [counterparty for counterparty in counterparties if counterparty["role"] == role]


def _wrong_way_code(action: str) -> str:
    return {
        "REJECT": "WRONG_WAY_RISK_REJECT",
        "ESCALATE": "WRONG_WAY_RISK_ESCALATE",
    }[action]


def _asset_decision(reasons: list[dict[str, Any]]) -> str:
    severities = {reason["severity"] for reason in reasons}
    if "REJECT" in severities:
        return "INELIGIBLE"
    if "ESCALATE" in severities:
        return "ESCALATE"
    if "REVIEW" in severities:
        return "REVIEW"
    return "ELIGIBLE"


def _overall_decision(
    asset_results: list[dict[str, Any]],
    portfolio_reasons: list[dict[str, Any]],
) -> str:
    severities = {reason["severity"] for reason in portfolio_reasons}
    for asset in asset_results:
        severities.update(reason["severity"] for reason in asset["reasons"])
    if "REJECT" in severities:
        return "REJECT"
    if "ESCALATE" in severities:
        return "ESCALATE"
    if "REVIEW" in severities:
        return "REVIEW"
    return "ACCEPT"


def _build_summary(
    asset_results: list[dict[str, Any]],
    concentration_results: list[dict[str, Any]],
) -> dict[str, Any]:
    total_market_value = sum(
        (_money(asset["marketValue"]) for asset in asset_results),
        start=Decimal("0"),
    )
    total_lendable_value = sum(
        (_money(asset["lendableValue"]) for asset in asset_results),
        start=Decimal("0"),
    )
    decisions = defaultdict(int)
    for asset in asset_results:
        decisions[asset["decision"]] += 1

    breach_count = sum(
        1 for result in concentration_results if result["decision"] != "PASS"
    )
    return {
        "candidateLotCount": len(asset_results),
        "decisionCounts": {
            "eligible": decisions["ELIGIBLE"],
            "ineligible": decisions["INELIGIBLE"],
            "escalate": decisions["ESCALATE"],
            "review": decisions["REVIEW"],
        },
        "totalMarketValue": _json_number(total_market_value),
        "totalLendableValue": _json_number(total_lendable_value),
        "concentrationIssueCount": breach_count,
    }


def _evaluation_id(policy: dict[str, Any], inventory: dict[str, Any]) -> str:
    canonical = json.dumps(
        {"policy": policy, "inventory": inventory},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return f"per-{digest[:16]}"


def _reason(
    *,
    code: str,
    category: str,
    severity: str,
    message: str,
    policy_path: str,
    policy_rule_id: str | None = None,
    related_lot_ids: list[str] | None = None,
    bucket: str | None = None,
    observed_value: float | None = None,
    threshold_value: float | None = None,
    currency: str | None = None,
) -> dict[str, Any]:
    reason = {
        "code": code,
        "category": category,
        "severity": severity,
        "message": message,
        "policyPath": policy_path,
    }
    if policy_rule_id is not None:
        reason["policyRuleId"] = policy_rule_id
    if related_lot_ids is not None:
        reason["relatedLotIds"] = related_lot_ids
    if bucket is not None:
        reason["bucket"] = bucket
    if observed_value is not None:
        reason["observedValue"] = observed_value
    if threshold_value is not None:
        reason["thresholdValue"] = threshold_value
    if currency is not None:
        reason["currency"] = currency
    return reason


def _sorted_reasons(reasons: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        reasons,
        key=lambda reason: (
            SEVERITY_ORDER[reason["severity"]],
            reason["category"],
            reason["code"],
            reason.get("policyRuleId", ""),
            reason["message"],
        ),
    )


def _has_reject_reason(reasons: list[dict[str, Any]]) -> bool:
    return any(reason["severity"] == "REJECT" for reason in reasons)


def _rating_meets_minimum(rating: str, minimum_rating: str) -> bool:
    return RATING_STRENGTH.get(rating, 0) >= RATING_STRENGTH[minimum_rating]


def _rating_meets_maximum(rating: str, maximum_rating: str) -> bool:
    return RATING_STRENGTH.get(rating, 0) <= RATING_STRENGTH[maximum_rating]


def _round_money(value: Decimal, rounding_mode: str) -> Decimal:
    return _quantize(value, DECIMAL_CENTS, rounding_mode)


def _money(value: Any) -> Decimal:
    return Decimal(str(value))


def _threshold_decimal(threshold: dict[str, Any]) -> Decimal:
    if threshold["metric"] in (
        "PERCENT_OF_COLLATERAL_VALUE",
        "PERCENT_OF_LENDABLE_VALUE",
    ):
        return _quantize(Decimal(str(threshold["value"])), DECIMAL_RATIO)
    return _money(threshold["value"])


def _threshold_value(threshold: dict[str, Any]) -> float:
    return float(_threshold_decimal(threshold))


def _quantize(
    value: Decimal,
    exponent: str,
    rounding_mode: str = "ROUND_HALF_UP",
) -> Decimal:
    return value.quantize(Decimal(exponent), rounding=ROUNDING_MODES[rounding_mode])


def _json_number(value: Decimal) -> float:
    quantized = _quantize(value, DECIMAL_CENTS)
    return float(quantized)


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
