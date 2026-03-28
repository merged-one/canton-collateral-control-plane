# CPL v0.1 Examples

This document explains the example policies published for `CPL v0.1`. Each example is a real validation fixture and is intended to exercise a distinct market-practice profile.

## Validation Command

```sh
make validate-cpl
```

## Example Set

| File | Profile | Purpose |
| --- | --- | --- |
| [examples/policies/central-bank-style-policy.json](../../examples/policies/central-bank-style-policy.json) | `central_bank` | Shows explicit sovereign-style eligibility, maturity-sensitive haircuts, restricted custody, and operator-controlled settlement windows. |
| [examples/policies/tri-party-style-policy.json](../../examples/policies/tri-party-style-policy.json) | `tri_party` | Shows tri-party agent inventory control, broad but bounded eligibility, and operational substitution rights. |
| [examples/policies/ccp-style-policy.json](../../examples/policies/ccp-style-policy.json) | `ccp` | Shows layered concentration limits, conservative mismatch haircuts, and stricter settlement/expiry controls. |
| [examples/policies/bilateral-csa-style-policy.json](../../examples/policies/bilateral-csa-style-policy.json) | `bilateral_csa` | Shows negotiated settlement currencies, bilateral substitution consent, and counterparty wrong-way-risk deny lists. |

## What Each Example Exercises

### Central-Bank Style

Key fields:

- issuer allow-list plus minimum external rating
- custody restricted to central-bank or approved third-party accounts
- maturity-bucket haircut schedule
- restricted segregation type and operator-controlled substitution

Why it matters:
This example mirrors central-bank practice where the eligibility list, haircut matrix, custody posture, and operating windows are explicit control surfaces.

### Tri-Party Style

Key fields:

- tri-party custody account type
- broad eligibility across cash, government, covered, corporate, and MMF collateral
- same-day substitution with `TRIPARTY_AGENT` inventory control
- ratio-based and absolute concentration controls

Why it matters:
This example shows that CPL can separate static policy from the agent-managed inventory process without collapsing the two concerns.

### CCP Style

Key fields:

- conservative sovereign and agency-only eligibility
- layered concentration caps across issuer, currency, and jurisdiction
- tighter expiries and `CCP_CONTROL` substitution mode
- wrong-way-risk exclusions that escalate or reject

Why it matters:
This example demonstrates that CCP-style concentration and operational controls fit the same policy package shape without special-case schema branches.

### Bilateral CSA Style

Key fields:

- negotiated settlement currencies
- non-segregated legal structure represented explicitly with `segregationType: NONE`
- secured-party consent on substitution
- explicit wrong-way-risk deny list for counterparty-related issuers

Why it matters:
This example confirms that the schema can represent negotiated bilateral policy without assuming central utilities or segregated infrastructure.

## Example Design Notes

- The examples are illustrative control profiles, not regulatory claims or calibrated production schedules.
- Each example uses the same top-level sections so later policy-engine work can load them through one contract.
- The set is intentionally diverse enough to exercise asset filters, concentration limits, wrong-way risk, settlement windows, and substitution rights.
