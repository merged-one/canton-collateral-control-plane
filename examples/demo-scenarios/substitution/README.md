# Substitution Demo Scenario

This directory contains the manifest, policy, inventory snapshots, and obligation inputs for the confidential collateral substitution prototype.

Current contents:

- `substitution-policy.json` for the demo-specific policy variant with required secured-party and custodian consent plus no-partial substitution handling
- `positive-inventory.json` and `positive-obligation.json` for the successful atomic substitution path
- `negative-ineligible-inventory.json` and `negative-ineligible-obligation.json` for the replacement-asset ineligibility path
- `negative-concentration-inventory.json` and `negative-concentration-obligation.json` for the concentration-breach replacement path
- `negative-unauthorized-obligation.json` and `negative-partial-obligation.json` for workflow-control failures against the positive inventory snapshot
- `demo-config.json` for the manifest consumed by `make demo-substitution`
