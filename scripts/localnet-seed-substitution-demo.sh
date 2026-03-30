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

need_cmd git localnet-seed-substitution-demo
need_cmd docker localnet-seed-substitution-demo
need_cmd python3 localnet-seed-substitution-demo
need_cmd curl localnet-seed-substitution-demo

prepare_control_plane_dirs
require_bootstrapped_localnet localnet-seed-substitution-demo
ensure_running_control_plane_stack localnet-seed-substitution-demo

test -f "${LOCALNET_DAR_OUTPUT_DIR:-"$repo_root/.daml/dist-quickstart"}/quickstart-dar-metadata.env" || {
	echo "localnet-seed-substitution-demo: missing Quickstart DAR metadata; run make localnet-start-control-plane or make localnet-deploy-dar first" >&2
	exit 1
}

LOCALNET_SCENARIO_MANIFEST=${LOCALNET_SCENARIO_MANIFEST:-"$repo_root/infra/quickstart/scenarios/confidential-substitution-demo-positive-scenario.json"}
LOCALNET_SUBSTITUTION_STATUS_JSON="$LOCALNET_CONTROL_PLANE_OUTPUT_DIR/localnet-substitution-status.json"

if [ -f "$LOCALNET_SEED_RECEIPT" ]; then
	if CURRENT_SEED_RECEIPT="$LOCALNET_SEED_RECEIPT" CURRENT_SCENARIO_MANIFEST="$LOCALNET_SCENARIO_MANIFEST" python3 - <<'PY'
import json
import os
import sys

with open(os.environ["CURRENT_SEED_RECEIPT"], "r", encoding="utf-8") as f:
    receipt = json.load(f)
with open(os.environ["CURRENT_SCENARIO_MANIFEST"], "r", encoding="utf-8") as f:
    scenario = json.load(f)

if receipt.get("scenarioId") == scenario.get("scenarioId"):
    sys.exit(0)
sys.exit(1)
PY
	then
		"$script_dir/localnet-substitution-status.sh" \
			--output-file "$LOCALNET_SUBSTITUTION_STATUS_JSON" >/dev/null
		if STATUS_PATH="$LOCALNET_SUBSTITUTION_STATUS_JSON" CURRENT_SCENARIO_MANIFEST="$LOCALNET_SCENARIO_MANIFEST" python3 - <<'PY'
import json
import os
import sys

with open(os.environ["STATUS_PATH"], "r", encoding="utf-8") as f:
    status = json.load(f)
with open(os.environ["CURRENT_SCENARIO_MANIFEST"], "r", encoding="utf-8") as f:
    scenario = json.load(f)

expected_current_lot_ids = sorted(lot["lotId"] for lot in scenario["currentEncumberedLots"])

current_holding_lot_ids = sorted(
    holding["lotId"] for holding in status.get("providerVisibleCurrentLotHoldings", [])
)
replacement_holding_lot_ids = sorted(
    holding["lotId"] for holding in status.get("providerVisibleReplacementLotHoldings", [])
)
active_pledged_lot_ids = sorted(
    encumbrance["lotId"]
    for encumbrance in status.get("providerVisibleEncumbrances", [])
    if encumbrance.get("status") == "EncumbrancePledged"
)

if (
    current_holding_lot_ids == expected_current_lot_ids
    and active_pledged_lot_ids == expected_current_lot_ids
    and replacement_holding_lot_ids == []
):
    sys.exit(0)
sys.exit(1)
PY
		then
			echo "localnet-seed-substitution-demo: scenario already active on Quickstart; refreshed status artifact instead of reseeding"
			exit 0
		fi
	fi
fi

write_control_plane_auth_env
write_seed_participant_config

SCENARIO_PATH="$LOCALNET_SCENARIO_MANIFEST" \
SEED_INPUT_PATH="$SEED_INPUT_FILE" \
AUTH_ENV_PATH="$AUTH_ENV_FILE" \
python3 - <<'PY'
import json
import os

with open(os.environ["SCENARIO_PATH"], "r", encoding="utf-8") as f:
    scenario = json.load(f)

auth_values = {}
with open(os.environ["AUTH_ENV_PATH"], "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, value = line.split("=", 1)
        auth_values[key] = value

seed_input = {
    "scenarioId": scenario["scenarioId"],
    "obligationId": scenario["obligationId"],
    "correlationId": scenario["correlationId"],
    "policyVersion": scenario["policyVersion"],
    "snapshotId": scenario["snapshotId"],
    "decisionReference": scenario["decisionReference"],
    "providerParty": auth_values["APP_USER_PARTY"],
    "providerUserId": auth_values["APP_USER_VALIDATOR_USER_ID"],
    "securedParty": auth_values["APP_PROVIDER_PARTY"],
    "securedPartyUserId": auth_values["APP_PROVIDER_VALIDATOR_USER_ID"],
    "operatorPartyHint": scenario["operator"]["partyHint"],
    "operatorDisplayName": scenario["operator"]["displayName"],
    "operatorUserId": scenario["operator"]["userId"],
    "custodianPartyHint": (
        auth_values["APP_PROVIDER_PARTY"].split("::", 1)[0]
        if scenario["custodian"].get("reuseSecuredPartyHostedIdentity")
        else scenario["custodian"]["partyHint"]
    ),
    "custodianDisplayName": scenario["custodian"]["displayName"],
    "custodianUserId": (
        auth_values["APP_PROVIDER_VALIDATOR_USER_ID"]
        if scenario["custodian"].get("reuseSecuredPartyHostedIdentity")
        else scenario["custodian"]["userId"]
    ),
    "currentEncumberedLots": scenario["currentEncumberedLots"],
    "replacementLots": scenario["replacementLots"],
}

with open(os.environ["SEED_INPUT_PATH"], "w", encoding="ascii") as f:
    json.dump(seed_input, f, indent=2)
    f.write("\n")
PY

"$script_dir/run-quickstart-daml-script.sh" \
	--script-name CantonCollateral.QuickstartSubstitution:seedSubstitutionScenario \
	--participant-config "$SEED_PARTICIPANT_CONFIG" \
	--input-file "$SEED_INPUT_FILE" \
	--output-file "$LOCALNET_SEED_RECEIPT"

echo "localnet-seed-substitution-demo: wrote $LOCALNET_SEED_RECEIPT"
