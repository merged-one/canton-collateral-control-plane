# Prompt 20 Execution Report

## Scope

Prepare the Canton Collateral Control Plane for proposal submission by adding a deterministic reviewer-facing proposal package on top of the existing Quickstart-backed final demo pack, plus reviewer memo and walkthrough materials that stay pinned to generated evidence.

## Commands

```sh
python3 -m py_compile app/orchestration/proposal_submission_pack.py app/orchestration/proposal_submission_cli.py test/conformance/test_proposal_submission_package.py
PYTHONPATH=app/orchestration python3 -m unittest discover -s test/conformance -p 'test_proposal_submission_package.py'
make test-conformance
make demo-all
make proposal-package
make docs-lint
make verify
PYTHONPATH=app/orchestration python3 -m unittest discover -s test/conformance -p 'test_*.py'
git diff --check
```

## Results

- the new proposal-submission generator, CLI, and isolated unit test compiled successfully
- the isolated `test_proposal_submission_package.py` unit tests passed under the repo's normal discovery path
- `make test-conformance` passed and regenerated `reports/generated/conformance-suite-report.json` with suite id `csr-d7e4b4c29646d5d4`, overall status `PASS`, and runtime mode `QUICKSTART`
- `make demo-all` passed and regenerated `reports/generated/final-demo-pack.json` with demo pack id `fdp-ad4246d5144c77eb`, overall status `PASS`, Quickstart commit `fe56d460af650b71b8e20098b3e76693397a8bf9`, and deployed package id `2535dc1e6f8ab629482bc6c186334df1c79ab0fe5c59302d7bcb20f5a7c139fb`
- `make proposal-package` passed and generated:
  - `reports/generated/proposal-submission-manifest.json`
  - `reports/generated/proposal-submission-summary.md`
- the generated proposal-submission manifest recorded:
  - submission id `psp-4bcc74b5b1f72eca`
  - source commit `f62f22e7b86cd2a730a29a2c924c9b25080ba42b`
  - final demo pack id `fdp-ad4246d5144c77eb`
  - conformance suite id `csr-d7e4b4c29646d5d4`
  - Quickstart commit `fe56d460af650b71b8e20098b3e76693397a8bf9`
  - deployed package id `2535dc1e6f8ab629482bc6c186334df1c79ab0fe5c59302d7bcb20f5a7c139fb`
  - margin-call report id `exr-9bc26ea5d960c241`
  - substitution report id `srr-a8a9d213c0f6408a`
  - return report id `rrr-163cdd5d84a09b71`
- the proposal package kept the walkthrough surface repo-tracked rather than depending on any out-of-repo media asset
- `make docs-lint` passed after the command inventories, reviewer docs, ADR, tracker, invariant, evidence, and runbook surfaces were aligned to the proposal-package command
- `make verify` passed after `verify-portable` was updated to exercise `make proposal-package` as part of the standard repository validation loop
- the full conformance unit discovery run passed
- `git diff --check` passed
