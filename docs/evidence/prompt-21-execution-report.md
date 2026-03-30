# Prompt 21 Execution Report

## Scope

Rehearse the proposal reviewer path from a temporary reviewer workspace derived from the current repository snapshot, prove that `make proposal-package` works outside the active checkout, and confirm that the reviewer-start doc, memo, walkthrough script, and generated proposal manifest agree on the same artifact sequence.

## Commands

Initial temporary workspace attempt that copied the active `.runtime` directory:

```sh
tmpdir=$(mktemp -d /tmp/cccp-reviewer-rehearsal-XXXXXX)
clone_dir="$tmpdir/repo"
git clone --local /Users/charlesdusek/Code/canton-collateral-control-plane "$clone_dir"
rsync -a --delete --exclude '.git' /Users/charlesdusek/Code/canton-collateral-control-plane/ "$clone_dir/"
cd "$clone_dir"
make proposal-package
```

Fresh temporary reviewer workspace that excludes repo-local runtime and generated artifacts:

```sh
tmpdir=$(mktemp -d /tmp/cccp-reviewer-clean-XXXXXX)
clone_dir="$tmpdir/repo"
git clone --local /Users/charlesdusek/Code/canton-collateral-control-plane "$clone_dir"
rsync -a --delete --exclude '.git' --exclude '.runtime' --exclude '.daml' --exclude 'reports/generated' /Users/charlesdusek/Code/canton-collateral-control-plane/ "$clone_dir/"
cd "$clone_dir"
make proposal-package
python3 - <<'PY'
import json
from pathlib import Path

repo = Path('.').resolve()
manifest = json.loads((repo / 'reports/generated/proposal-submission-manifest.json').read_text())
summary = (repo / 'reports/generated/proposal-submission-summary.md').read_text()
reviewer = (repo / 'docs/evidence/REVIEWER_START_HERE.md').read_text()
memo = (repo / 'docs/evidence/PROPOSAL_SUBMISSION_MEMO.md').read_text()
walk = (repo / 'docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md').read_text()

expected_review_order = [
    'docs/evidence/REVIEWER_START_HERE.md',
    'docs/evidence/PROPOSAL_SUBMISSION_MEMO.md',
    'reports/generated/localnet-control-plane-deployment-receipt.json',
    'reports/generated/localnet-reference-token-adapter-execution-report.json',
    'reports/generated/localnet-reference-token-adapter-status.json',
    'reports/generated/conformance-suite-report.json',
    'reports/generated/final-demo-pack.json',
    'docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md',
]

for rel in manifest['artifacts'].values():
    assert (repo / rel).exists(), rel
for step in manifest['reviewerJourney']['reviewOrder']:
    assert (repo / step['path']).exists(), step['path']
for rel in manifest['walkthroughPackage']['artifactOrder']:
    assert (repo / rel).exists(), rel

assert [step['path'] for step in manifest['reviewerJourney']['reviewOrder']] == expected_review_order
assert 'reports/generated/conformance-suite-report.json' in reviewer
assert 'reports/generated/final-demo-pack.json' in reviewer
assert 'reports/generated/proposal-submission-manifest.json' in memo
assert 'docs/evidence/PROPOSAL_WALKTHROUGH_SCRIPT.md' in memo
assert 'reports/generated/proposal-submission-summary.md' in walk
assert 'reports/generated/conformance-suite-summary.md' in walk
assert manifest['submissionId'] in summary
PY
```

Focused repo validation after fixing the manifest review-order drift:

```sh
python3 -m py_compile app/orchestration/proposal_submission_pack.py test/conformance/test_proposal_submission_package.py
PYTHONPATH=app/orchestration python3 -m unittest discover -s test/conformance -p 'test_proposal_submission_package.py'
make proposal-package
make docs-lint
git diff --check
```

## Results

- the first temporary-workspace attempt failed as expected because copying the active `.runtime/localnet/cn-quickstart` directory into a new checkout produced a non-portable local Quickstart checkout path; `localnet-bootstrap` rejected that copied directory because it was not a valid git checkout in the new workspace
- the fresh temporary reviewer workspace that excluded `.runtime`, `.daml`, and `reports/generated` succeeded and rebuilt the full Quickstart-backed proposal package from the current source snapshot
- the reviewer rehearsal workspace regenerated:
  - `reports/generated/proposal-submission-manifest.json`
  - `reports/generated/proposal-submission-summary.md`
- the rehearsal exposed one real drift before the fix: the generated proposal manifest listed the final demo pack before conformance, while `REVIEWER_START_HERE.md`, `PROPOSAL_SUBMISSION_MEMO.md`, and `PROPOSAL_WALKTHROUGH_SCRIPT.md` all directed reviewers through conformance before the final demo pack
- `app/orchestration/proposal_submission_pack.py` was updated so the machine-readable review order now matches the reviewer docs, and `test/conformance/test_proposal_submission_package.py` now locks that order explicitly
- after the fix, the temporary reviewer workspace proved:
  - every artifact path in the proposal manifest exists
  - every review-order path exists
  - every walkthrough artifact-order path exists
  - the reviewer-start doc, memo, walkthrough script, and generated proposal manifest all agree on the same conformance-before-final-demo-pack review sequence
- focused validation passed:
  - `python3 -m py_compile ...`
  - isolated `test_proposal_submission_package.py`
  - `make proposal-package`
  - `make docs-lint`
  - `git diff --check`
- the regenerated proposal package now carries submission id `psp-8bc396964860907b`

## Remaining Limitation

The temporary reviewer workspace was derived from the current uncommitted source snapshot, so the generated proposal manifest still reports `worktreeStatus: DIRTY`. The next submission-freeze step is still to commit the intended proposal baseline and rerun `make proposal-package` so the machine-readable wrapper records the final source commit under a clean worktree state.
