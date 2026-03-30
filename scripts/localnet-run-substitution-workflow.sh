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
Usage: localnet-run-substitution-workflow.sh --input-file PATH --output-file PATH

Advance a seeded Quickstart substitution scenario through the real substitution
workflow states up to the adapter handoff point, or to a deterministic blocked
partial-substitution outcome, and write a machine-readable workflow artifact.
EOF
}

WORKFLOW_INPUT_FILE=
WORKFLOW_OUTPUT_FILE=

while [ "$#" -gt 0 ]; do
	case "$1" in
		--input-file)
			shift
			WORKFLOW_INPUT_FILE=${1:-}
			;;
		--output-file)
			shift
			WORKFLOW_OUTPUT_FILE=${1:-}
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "localnet-run-substitution-workflow: unknown argument '$1'" >&2
			usage >&2
			exit 1
			;;
	esac
	shift
done

test -n "$WORKFLOW_INPUT_FILE" || {
	echo "localnet-run-substitution-workflow: --input-file is required" >&2
	exit 1
}

test -n "$WORKFLOW_OUTPUT_FILE" || {
	echo "localnet-run-substitution-workflow: --output-file is required" >&2
	exit 1
}

test -f "$WORKFLOW_INPUT_FILE" || {
	echo "localnet-run-substitution-workflow: missing input file $WORKFLOW_INPUT_FILE" >&2
	exit 1
}

need_cmd git localnet-run-substitution-workflow
need_cmd docker localnet-run-substitution-workflow
need_cmd python3 localnet-run-substitution-workflow
need_cmd curl localnet-run-substitution-workflow

prepare_control_plane_dirs
require_bootstrapped_localnet localnet-run-substitution-workflow
ensure_running_control_plane_stack localnet-run-substitution-workflow

test -f "$LOCALNET_SEED_RECEIPT" || {
	echo "localnet-run-substitution-workflow: missing $LOCALNET_SEED_RECEIPT; run the Quickstart substitution seed flow first" >&2
	exit 1
}

write_control_plane_auth_env
write_adapter_participant_config

"$script_dir/run-quickstart-daml-script.sh" \
	--script-name CantonCollateral.QuickstartSubstitution:runSubstitutionWorkflow \
	--participant-config "$ADAPTER_PARTICIPANT_CONFIG" \
	--input-file "$WORKFLOW_INPUT_FILE" \
	--output-file "$WORKFLOW_OUTPUT_FILE"

echo "localnet-run-substitution-workflow: wrote $WORKFLOW_OUTPUT_FILE"
