#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)
. "$script_dir/toolchain.env"

quickstart_pin="$repo_root/infra/quickstart/overlay/upstream-pin.env"
if [ -f "$quickstart_pin" ]; then
	. "$quickstart_pin"
fi

runtime_dir="$repo_root/.runtime"
env_file="$runtime_dir/env.sh"
localnet_workdir="$runtime_dir/localnet/cn-quickstart"
localnet_env_file="$localnet_workdir/${QS_QUICKSTART_SUBDIR:-quickstart}/.env.local"

printf 'Mission-control status\n'
grep -m 1 '^Current Phase:' "$repo_root/docs/mission-control/MASTER_TRACKER.md"

printf '\nPinned toolchain\n'
printf '  Python (recommended): %s\n' "$PYTHON_TOOL_VERSION"
printf '  Temurin JDK: %s\n' "$JAVA_VERSION"
printf '  Daml SDK: %s\n' "$DAML_SDK_VERSION"
printf '  Canton baseline: %s\n' "$CANTON_VERSION"
printf '  CPL validator: %s\n' "$CHECK_JSONSCHEMA_VERSION"
if [ -n "${QS_COMMIT:-}" ]; then
	printf '  CN Quickstart pin: %s\n' "$QS_COMMIT"
fi

printf '\nInstalled toolchain\n'
if [ -f "$env_file" ]; then
	. "$env_file"
	printf '  daml: %s\n' "$("$DAML_BIN" version | sed -n '2p' | sed 's/^  //')"
	printf '  java: %s\n' "$("$JAVA_HOME/bin/java" -version 2>&1 | head -n 1)"
	printf '  validator: %s\n' "$("$CHECK_JSONSCHEMA_BIN" --version 2>&1 | head -n 1)"
else
	printf '  runtime: not bootstrapped; run make bootstrap\n'
fi

printf '\nQuickstart foundation\n'
if [ -d "$localnet_workdir/.git" ]; then
	current_quickstart_commit=$(git -C "$localnet_workdir" rev-parse HEAD 2>/dev/null || printf 'unknown')
	printf '  upstream repo: %s\n' "${QS_REPO_URL:-unknown}"
	printf '  pinned commit: %s\n' "${QS_COMMIT:-unknown}"
	printf '  staged commit: %s\n' "$current_quickstart_commit"
	if [ -f "$localnet_env_file" ]; then
		printf '  overlay env: %s\n' "$localnet_env_file"
		printf '  party hint: %s\n' "$(sed -n 's/^PARTY_HINT=//p' "$localnet_env_file" | head -n 1)"
		printf '  auth mode: %s\n' "$(sed -n 's/^AUTH_MODE=//p' "$localnet_env_file" | head -n 1)"
		printf '  observability: %s\n' "$(sed -n 's/^OBSERVABILITY_ENABLED=//p' "$localnet_env_file" | head -n 1)"
	else
		printf '  overlay env: missing; run make localnet-bootstrap\n'
	fi
else
	printf '  localnet: not bootstrapped; run make localnet-bootstrap\n'
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
printf '  make localnet-bootstrap\n'
printf '  make localnet-smoke\n'
printf '  make status\n'
printf '  make validate-cpl\n'
printf '  make policy-eval\n'
printf '  make optimize\n'
printf '  make test-policy-engine\n'
printf '  make test-optimizer\n'
printf '  make daml-build\n'
printf '  make daml-test\n'
printf '  make demo-run\n'
printf '  make demo-margin-call\n'
printf '  make demo-substitution\n'
printf '  make verify\n'

printf '\nGit\n'
git -C "$repo_root" status --short --branch
