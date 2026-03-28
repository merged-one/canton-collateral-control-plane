#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
. "$script_dir/toolchain.env"

runtime_dir="$repo_root/.runtime"
env_file="$runtime_dir/env.sh"

printf 'Mission-control status\n'
grep -m 1 '^Current Phase:' "$repo_root/docs/mission-control/MASTER_TRACKER.md"

printf '\nPinned toolchain\n'
printf '  Python (recommended): %s\n' "$PYTHON_TOOL_VERSION"
printf '  Temurin JDK: %s\n' "$JAVA_VERSION"
printf '  Daml SDK: %s\n' "$DAML_SDK_VERSION"
printf '  Canton baseline: %s\n' "$CANTON_VERSION"
printf '  CPL validator: %s\n' "$CHECK_JSONSCHEMA_VERSION"

printf '\nInstalled toolchain\n'
if [ -f "$env_file" ]; then
	. "$env_file"
	printf '  daml: %s\n' "$("$DAML_BIN" version | sed -n '2p' | sed 's/^  //')"
	printf '  java: %s\n' "$("$JAVA_HOME/bin/java" -version 2>&1 | head -n 1)"
	printf '  validator: %s\n' "$("$CHECK_JSONSCHEMA_BIN" --version 2>&1 | head -n 1)"
else
	printf '  runtime: not bootstrapped; run make bootstrap\n'
fi

printf '\nScaffold\n'
for dir in daml app reports scripts test examples infra docs/setup; do
	if [ -d "$repo_root/$dir" ]; then
		printf '  present: %s\n' "$dir"
	else
		printf '  missing: %s\n' "$dir"
	fi
done

printf '\nCommand surface\n'
printf '  make bootstrap\n'
printf '  make status\n'
printf '  make validate-cpl\n'
printf '  make daml-build\n'
printf '  make demo-run\n'
printf '  make verify\n'

printf '\nGit\n'
git -C "$repo_root" status --short --branch
