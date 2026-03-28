# Margin Call Demo Scenarios

This directory contains the first end-to-end margin-call demo bundle for the Canton Collateral Control Plane.

Contents:

- `demo-config.json` drives `make demo-margin-call`
- `positive-inventory.json` and `positive-obligation.json` define the successful path
- `negative-ineligible-inventory.json` covers a hard eligibility failure
- `negative-insufficient-inventory.json` and `negative-insufficient-obligation.json` cover insufficient lendable value
- `negative-expired-policy-window-inventory.json` covers a stale policy window

The demo command generates real artifacts under `reports/generated/` from these inputs.
