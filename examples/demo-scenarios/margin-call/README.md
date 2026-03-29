# Margin Call Demo Scenarios

This directory contains the first end-to-end margin-call demo bundle for the Canton Collateral Control Plane.

Contents:

- `demo-config.json` drives `make demo-margin-call`
- `quickstart-demo-config.json` drives `make demo-margin-call-quickstart`
- `positive-inventory.json` and `positive-obligation.json` define the successful path
- `quickstart-positive-inventory.json` and `quickstart-positive-obligation.json` define the Quickstart-backed positive path
- `negative-ineligible-inventory.json` covers a hard eligibility failure
- `quickstart-negative-ineligible-inventory.json` and `quickstart-negative-ineligible-obligation.json` cover the Quickstart policy-blocked path
- `negative-insufficient-inventory.json` and `negative-insufficient-obligation.json` cover insufficient lendable value
- `negative-expired-policy-window-inventory.json` covers a stale policy window
- `quickstart-negative-workflow-inventory.json` and `quickstart-negative-workflow-obligation.json` cover the Quickstart workflow-rejection path

The Quickstart manifest proves two negative-path controls in addition to the positive chain:

- no workflow or adapter artifact is fabricated when policy rejects the scenario
- no adapter receipt, holding, or encumbrance movement appears when the secured party rejects the posting on Quickstart

The demo command generates real artifacts under `reports/generated/` from these inputs.
