#!/usr/bin/env sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$script_dir/.." && pwd)

. "$script_dir/toolchain.env"
. "$repo_root/infra/quickstart/overlay/upstream-pin.env"

LOCALNET_WORKDIR=${LOCALNET_WORKDIR:-"$repo_root/.runtime/localnet/cn-quickstart"}
quickstart_dir="$LOCALNET_WORKDIR/$QS_QUICKSTART_SUBDIR"
LOCALNET_ONBOARDING_CONTAINER=${LOCALNET_ONBOARDING_CONTAINER:-control-plane-splice-onboarding}

. "$script_dir/localnet-control-plane-common.sh"

usage() {
	cat <<'EOF'
Usage: localnet-run-substitution-token-adapter.sh --input-file PATH --output-file PATH

Execute the Quickstart-backed reference token adapter for a pending-settlement
substitution instruction and write a machine-readable adapter execution report.
EOF
}

ADAPTER_INPUT_ARG=
ADAPTER_OUTPUT_ARG=

while [ "$#" -gt 0 ]; do
	case "$1" in
		--input-file)
			shift
			ADAPTER_INPUT_ARG=${1:-}
			;;
		--output-file)
			shift
			ADAPTER_OUTPUT_ARG=${1:-}
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "localnet-run-substitution-token-adapter: unknown argument '$1'" >&2
			usage >&2
			exit 1
			;;
	esac
	shift
done

test -n "$ADAPTER_INPUT_ARG" || {
	echo "localnet-run-substitution-token-adapter: --input-file is required" >&2
	exit 1
}

test -n "$ADAPTER_OUTPUT_ARG" || {
	echo "localnet-run-substitution-token-adapter: --output-file is required" >&2
	exit 1
}

test -f "$ADAPTER_INPUT_ARG" || {
	echo "localnet-run-substitution-token-adapter: missing input file $ADAPTER_INPUT_ARG" >&2
	exit 1
}

need_cmd git localnet-run-substitution-token-adapter
need_cmd docker localnet-run-substitution-token-adapter
need_cmd python3 localnet-run-substitution-token-adapter
need_cmd curl localnet-run-substitution-token-adapter

prepare_control_plane_dirs
require_bootstrapped_localnet localnet-run-substitution-token-adapter
ensure_running_control_plane_stack localnet-run-substitution-token-adapter

test -f "$LOCALNET_SEED_RECEIPT" || {
	echo "localnet-run-substitution-token-adapter: missing $LOCALNET_SEED_RECEIPT; run the Quickstart substitution seed flow first" >&2
	exit 1
}

write_control_plane_auth_env
write_adapter_participant_config

"$script_dir/run-quickstart-daml-script.sh" \
	--script-name CantonCollateral.QuickstartSubstitution:referenceTokenSubstitutionAdapterReport \
	--participant-config "$ADAPTER_PARTICIPANT_CONFIG" \
	--input-file "$ADAPTER_INPUT_ARG" \
	--output-file "$ADAPTER_OUTPUT_ARG"

echo "localnet-run-substitution-token-adapter: wrote $ADAPTER_OUTPUT_ARG"
