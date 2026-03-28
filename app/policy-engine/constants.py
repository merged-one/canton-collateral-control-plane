"""Policy-engine constants shared across the CPL v0.1 evaluator."""

from decimal import ROUND_DOWN, ROUND_HALF_UP, ROUND_UP


REPORT_VERSION = "0.1.0"
REPORT_TYPE = "PolicyEvaluationReport"

RATING_ORDER = [
    "AAA",
    "AA+",
    "AA",
    "AA-",
    "A+",
    "A",
    "A-",
    "BBB+",
    "BBB",
    "BBB-",
    "BB+",
    "BB",
    "BB-",
    "B+",
    "B",
    "B-",
    "CCC",
    "CC",
    "C",
    "D",
    "UNRATED",
]

RATING_STRENGTH = {
    rating: len(RATING_ORDER) - index for index, rating in enumerate(RATING_ORDER)
}

DECIMAL_CENTS = "0.01"
DECIMAL_RATIO = "0.000001"

ROUNDING_MODES = {
    "ROUND_HALF_UP": ROUND_HALF_UP,
    "ROUND_DOWN": ROUND_DOWN,
    "ROUND_UP": ROUND_UP,
}

SEVERITY_ORDER = {
    "REJECT": 0,
    "ESCALATE": 1,
    "REVIEW": 2,
}

ASSET_REQUIRED_FIELDS = [
    "lotId",
    "assetId",
    "assetClass",
    "issueType",
    "issuerId",
    "issuerType",
    "longTermRating",
    "currency",
    "issuanceJurisdiction",
    "riskJurisdiction",
    "custodianId",
    "custodyJurisdiction",
    "accountType",
    "marketValue",
    "nominalValue",
    "outstandingPrincipal",
    "residualMaturityDays",
    "isSegregated",
    "hasControlAgreement",
    "isInternalCustody",
    "isEncumbered",
    "freeAllocationPercent",
    "segregationType",
    "thirdPartyAcknowledgementReceived",
]
