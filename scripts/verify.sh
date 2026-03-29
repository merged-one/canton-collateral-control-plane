#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

cd "$repo_root"
make --no-print-directory verify-portable
make --no-print-directory localnet-smoke
echo "verify: policy-engine, optimizer, Daml workflow, aggregate conformance suite, final demo pack, and Quickstart LocalNet foundation checks passed"
