# Prompt 22 Execution Report

## Scope

Freeze a clean proposal baseline commit, rerun `make proposal-package`, and make the proposal-submission manifest report that baseline cleanly by excluding regenerated `reports/generated` outputs from the git-cleanliness calculation while still detecting dirty source or documentation paths outside that generated-output scope.

## Commands

Validation before freezing the new baseline:

```sh
python3 -m py_compile app/orchestration/proposal_submission_pack.py test/conformance/test_proposal_submission_package.py
PYTHONPATH=app/orchestration python3 -m unittest discover -s test/conformance -p 'test_proposal_submission_package.py'
```

Freeze the new proposal baseline commit:

```sh
git add app/orchestration/proposal_submission_pack.py \
  test/conformance/test_proposal_submission_package.py \
  docs/mission-control/WORKLOG.md \
  reports/generated/conformance-suite-report.json \
  reports/generated/final-demo-pack.json \
  reports/generated/localnet-control-plane-deployment-receipt.json \
  reports/generated/proposal-submission-manifest.json \
  reports/generated/proposal-submission-summary.md
git commit -m "Freeze clean proposal baseline"
git rev-parse HEAD
```

Rerun the proposal package from that clean baseline and inspect the resulting manifest:

```sh
make proposal-package
python3 - <<'PY'
import json
from pathlib import Path

manifest = json.loads(Path('reports/generated/proposal-submission-manifest.json').read_text())
print('submissionId', manifest['submissionId'])
print('sourceCommit', manifest['submissionBaseline']['sourceCommit'])
print('worktreeStatus', manifest['submissionBaseline']['worktreeStatus'])
print('ignoredDirtyPathPrefixes', manifest['submissionBaseline']['ignoredDirtyPathPrefixes'])
print('dirtyPaths', manifest['submissionBaseline']['dirtyPaths'])
print('quickstartCommit', manifest['submissionBaseline']['quickstartCommit'])
print('deployedPackageId', manifest['submissionBaseline']['deployedPackageId'])
PY
grep -n "Worktree status at package build" reports/generated/proposal-submission-summary.md
git status --short
git diff --check
```

## Results

- before the fix, rerunning `make proposal-package` from a clean `HEAD` still produced `worktreeStatus: DIRTY` because `make demo-all` refreshed tracked files under `reports/generated/` before the proposal wrapper captured git status
- `app/orchestration/proposal_submission_pack.py` now excludes dirty paths under `reports/generated/` from the frozen-source cleanliness check and carries that scope explicitly in the generated manifest as `ignoredDirtyPathPrefixes`
- `test/conformance/test_proposal_submission_package.py` now proves both sides of the contract:
  - dirty paths only under `reports/generated/` produce `worktreeStatus: CLEAN`
  - dirty paths outside `reports/generated/` still produce `worktreeStatus: DIRTY`
- the new proposal baseline was frozen at commit `71c9a3baac375a2f92460fd470f2f71281577faf`
- rerunning `make proposal-package` from that baseline succeeded and produced:
  - submission id `psp-7d263e9219b1c4e2`
  - source commit `71c9a3baac375a2f92460fd470f2f71281577faf`
  - `worktreeStatus: CLEAN`
  - `ignoredDirtyPathPrefixes: ["reports/generated/"]`
  - no dirty source paths outside the excluded generated-output scope
  - Quickstart commit `fe56d460af650b71b8e20098b3e76693397a8bf9`
  - deployed package id `2535dc1e6f8ab629482bc6c186334df1c79ab0fe5c59302d7bcb20f5a7c139fb`
- the generated summary now states `Worktree status at package build (excluding reports/generated/): CLEAN`
- after the rerun, `git status --short` still showed the refreshed files under `reports/generated/`, which is expected because the clean-baseline calculation now explicitly separates committed source state from regenerated evidence outputs
- `git diff --check` passed

## Remaining Decision

The frozen source baseline is now explicit and machine-readable, but the repository still needs an operating convention for whether regenerated `reports/generated` artifacts should be committed as a separate evidence commit, shipped out-of-band with the baseline commit hash, or both when assembling the final external proposal submission bundle.
