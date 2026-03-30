#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

"$script_dir/bootstrap.sh" >/dev/null

cd "$repo_root"
make --no-print-directory docs-lint
make --no-print-directory validate-cpl
make --no-print-directory test-policy-engine
make --no-print-directory test-optimizer
make --no-print-directory daml-build
make --no-print-directory daml-test
make --no-print-directory demo-run
make --no-print-directory proposal-package
echo "verify-portable: policy-engine, optimizer, Daml workflow, aggregate conformance suite, final demo pack, and proposal submission package checks passed"
