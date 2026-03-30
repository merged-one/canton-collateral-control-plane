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
Usage: localnet-substitution-status.sh --output-file PATH

Query the provider-visible Quickstart substitution status surface for the
currently seeded substitution scenario and write a machine-readable artifact.
EOF
}

STATUS_OUTPUT_FILE=

while [ "$#" -gt 0 ]; do
	case "$1" in
		--output-file)
			shift
			STATUS_OUTPUT_FILE=${1:-}
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			echo "localnet-substitution-status: unknown argument '$1'" >&2
			usage >&2
			exit 1
			;;
	esac
	shift
done

test -n "$STATUS_OUTPUT_FILE" || {
	echo "localnet-substitution-status: --output-file is required" >&2
	exit 1
}

need_cmd git localnet-substitution-status
need_cmd docker localnet-substitution-status
need_cmd python3 localnet-substitution-status
need_cmd curl localnet-substitution-status

prepare_control_plane_dirs
require_bootstrapped_localnet localnet-substitution-status
ensure_running_control_plane_stack localnet-substitution-status

test -f "$LOCALNET_SEED_RECEIPT" || {
	echo "localnet-substitution-status: missing $LOCALNET_SEED_RECEIPT; run the Quickstart substitution seed flow first" >&2
	exit 1
}

write_control_plane_auth_env
write_status_participant_config

SEED_RECEIPT_PATH="$LOCALNET_SEED_RECEIPT" \
STATUS_INPUT_PATH="$STATUS_INPUT_FILE" \
python3 - <<'PY'
import json
import os

with open(os.environ["SEED_RECEIPT_PATH"], "r", encoding="utf-8") as f:
    receipt = json.load(f)

status_input = {
    "scenarioId": receipt["scenarioId"],
    "obligationId": receipt["obligationId"],
    "providerParty": receipt["providerParty"],
    "currentEncumberedLotIds": [lot["lotId"] for lot in receipt["currentEncumberedLots"]],
    "replacementLotIds": [lot["lotId"] for lot in receipt["replacementLots"]],
}

with open(os.environ["STATUS_INPUT_PATH"], "w", encoding="ascii") as f:
    json.dump(status_input, f, indent=2)
    f.write("\n")
PY

"$script_dir/run-quickstart-daml-script.sh" \
	--script-name CantonCollateral.QuickstartSubstitution:substitutionStatusForProviderView \
	--participant-config "$STATUS_PARTICIPANT_CONFIG" \
	--input-file "$STATUS_INPUT_FILE" \
	--output-file "$STATUS_OUTPUT_FILE"

echo "localnet-substitution-status: wrote $STATUS_OUTPUT_FILE"
