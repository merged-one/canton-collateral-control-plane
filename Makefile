SHELL := /bin/sh
PYTHON ?= python3
REPO_ROOT := $(CURDIR)
RUNTIME_DIR := .runtime
RUNTIME_ENV := $(RUNTIME_DIR)/env.sh
BOOTSTRAP_SCRIPT := scripts/bootstrap.sh
STATUS_SCRIPT := scripts/dev-status.sh
VERIFY_PORTABLE_SCRIPT := scripts/verify-portable.sh
VERIFY_SCRIPT := scripts/verify.sh
LOCALNET_BOOTSTRAP_SCRIPT := infra/quickstart/bootstrap-localnet.sh
LOCALNET_SMOKE_SCRIPT := scripts/run-localnet-smoke.sh
LOCALNET_BUILD_DAR_SCRIPT := scripts/build-quickstart-dar.sh
LOCALNET_DEPLOY_DAR_SCRIPT := scripts/localnet-deploy-dar.sh
LOCALNET_START_CONTROL_PLANE_SCRIPT := scripts/localnet-start-control-plane.sh
LOCALNET_SEED_DEMO_SCRIPT := scripts/localnet-seed-demo.sh
LOCALNET_STATUS_CONTROL_PLANE_SCRIPT := scripts/localnet-status-control-plane.sh
LOCALNET_RUN_MARGIN_CALL_WORKFLOW_SCRIPT := scripts/localnet-run-margin-call-workflow.sh
LOCALNET_RUN_TOKEN_ADAPTER_SCRIPT := scripts/localnet-run-token-adapter.sh
LOCALNET_ADAPTER_STATUS_SCRIPT := scripts/localnet-adapter-status.sh
LOCALNET_DAML_SCRIPT_RUNNER := scripts/run-quickstart-daml-script.sh

include scripts/toolchain.env

VENV := .venv
CHECK_JSONSCHEMA := $(VENV)/bin/check-jsonschema
CPL_SCHEMA := schema/cpl.schema.json
POLICY_EVAL_REPORT_SCHEMA := reports/schemas/policy-evaluation-report.schema.json
OPTIMIZATION_REPORT_SCHEMA := reports/schemas/optimization-report.schema.json
EXECUTION_REPORT_SCHEMA := reports/schemas/execution-report.schema.json
SUBSTITUTION_REPORT_SCHEMA := reports/schemas/substitution-report.schema.json
RETURN_REPORT_SCHEMA := reports/schemas/return-report.schema.json
ADAPTER_EXECUTION_REPORT_SCHEMA := reports/schemas/adapter-execution-report.schema.json
POLICY ?= examples/policies/central-bank-style-policy.json
INVENTORY ?= examples/inventory/central-bank-eligible-inventory.json
OBLIGATION ?= examples/obligations/central-bank-window-call.json
REPORT ?=
MARGIN_CALL_DEMO_MANIFEST ?= examples/demo-scenarios/margin-call/demo-config.json
MARGIN_CALL_QUICKSTART_DEMO_MANIFEST ?= examples/demo-scenarios/margin-call/quickstart-demo-config.json
MARGIN_CALL_DEMO_OUTPUT_DIR ?= reports/generated
SUBSTITUTION_DEMO_MANIFEST ?= examples/demo-scenarios/substitution/demo-config.json
SUBSTITUTION_DEMO_OUTPUT_DIR ?= reports/generated
RETURN_DEMO_MANIFEST ?= examples/demo-scenarios/return/demo-config.json
RETURN_DEMO_OUTPUT_DIR ?= reports/generated
CONFORMANCE_OUTPUT_DIR ?= reports/generated
CONFORMANCE_REPORT ?= $(CONFORMANCE_OUTPUT_DIR)/conformance-suite-report.json
FINAL_DEMO_OUTPUT_DIR ?= reports/generated
LOCALNET_PROFILE ?= lean
LOCALNET_WORKDIR ?= $(REPO_ROOT)/.runtime/localnet/cn-quickstart
LOCALNET_PARTY_HINT ?= canton-collateral-1
LOCALNET_SCENARIO_MANIFEST ?= infra/quickstart/scenarios/confidential-margin-scenario.json
LOCALNET_ADAPTER_OUTPUT_DIR ?= reports/generated
CPL_EXAMPLES := \
	examples/policies/central-bank-style-policy.json \
	examples/policies/tri-party-style-policy.json \
	examples/policies/ccp-style-policy.json \
	examples/policies/bilateral-csa-style-policy.json

REQUIRED_DOCS := \
	README.md \
	AGENTS.md \
	CONTRIBUTING.md \
	SECURITY.md \
	CODEOWNERS \
	.gitignore \
	.tool-versions \
	Makefile \
	daml.yaml \
	scripts/toolchain.env \
	scripts/bootstrap.sh \
	scripts/dev-status.sh \
	scripts/build-quickstart-dar.sh \
	scripts/localnet-deploy-dar.sh \
	scripts/localnet-control-plane-common.sh \
	scripts/run-quickstart-daml-script.sh \
	scripts/localnet-start-control-plane.sh \
	scripts/localnet-seed-demo.sh \
	scripts/localnet-status-control-plane.sh \
	scripts/localnet-run-margin-call-workflow.sh \
	scripts/localnet-run-token-adapter.sh \
	scripts/localnet-adapter-status.sh \
	scripts/verify-portable.sh \
	scripts/verify.sh \
	app/README.md \
	app/policy-engine/cli.py \
	app/policy-engine/constants.py \
	app/policy-engine/evaluator.py \
	app/optimizer/cli.py \
	app/optimizer/optimizer.py \
	app/optimizer/optimizer_constants.py \
	app/orchestration/cli.py \
	app/orchestration/conformance_cli.py \
	app/orchestration/conformance_suite.py \
	app/orchestration/final_demo_cli.py \
	app/orchestration/final_demo_pack.py \
	app/orchestration/margin_call_demo.py \
	app/orchestration/return_cli.py \
	app/orchestration/return_demo.py \
	app/orchestration/substitution_cli.py \
	app/orchestration/substitution_demo.py \
	reports/README.md \
	reports/schemas/policy-evaluation-report.schema.json \
	reports/schemas/optimization-report.schema.json \
	reports/schemas/execution-report.schema.json \
	reports/schemas/return-report.schema.json \
	reports/schemas/substitution-report.schema.json \
	reports/schemas/adapter-execution-report.schema.json \
	test/README.md \
	test/conformance/test_conformance.py \
	test/conformance/test_conformance_checks.py \
	test/policy-engine/test_policy_engine.py \
	test/optimizer/test_optimizer.py \
	testsupport/__init__.py \
	testsupport/fixture_builders.py \
	examples/README.md \
	examples/inventory/central-bank-eligible-inventory.json \
	examples/obligations/central-bank-window-call.json \
	examples/obligations/central-bank-window-remediation.json \
	examples/demo-scenarios/margin-call/README.md \
	examples/demo-scenarios/margin-call/demo-config.json \
	examples/demo-scenarios/margin-call/quickstart-demo-config.json \
	examples/demo-scenarios/margin-call/positive-inventory.json \
	examples/demo-scenarios/margin-call/positive-obligation.json \
	examples/demo-scenarios/margin-call/quickstart-positive-inventory.json \
	examples/demo-scenarios/margin-call/quickstart-positive-obligation.json \
	examples/demo-scenarios/margin-call/negative-ineligible-inventory.json \
	examples/demo-scenarios/margin-call/negative-ineligible-obligation.json \
	examples/demo-scenarios/margin-call/quickstart-negative-ineligible-inventory.json \
	examples/demo-scenarios/margin-call/quickstart-negative-ineligible-obligation.json \
	examples/demo-scenarios/margin-call/negative-insufficient-inventory.json \
	examples/demo-scenarios/margin-call/negative-insufficient-obligation.json \
	examples/demo-scenarios/margin-call/negative-expired-policy-window-inventory.json \
	examples/demo-scenarios/margin-call/negative-expired-policy-window-obligation.json \
	examples/demo-scenarios/margin-call/quickstart-negative-workflow-inventory.json \
	examples/demo-scenarios/margin-call/quickstart-negative-workflow-obligation.json \
	examples/demo-scenarios/substitution/README.md \
	examples/demo-scenarios/substitution/demo-config.json \
	examples/demo-scenarios/substitution/substitution-policy.json \
	examples/demo-scenarios/substitution/positive-inventory.json \
	examples/demo-scenarios/substitution/positive-obligation.json \
	examples/demo-scenarios/substitution/negative-ineligible-inventory.json \
	examples/demo-scenarios/substitution/negative-ineligible-obligation.json \
	examples/demo-scenarios/substitution/negative-concentration-inventory.json \
	examples/demo-scenarios/substitution/negative-concentration-obligation.json \
	examples/demo-scenarios/substitution/negative-unauthorized-obligation.json \
	examples/demo-scenarios/substitution/negative-partial-obligation.json \
	examples/demo-scenarios/return/README.md \
	examples/demo-scenarios/return/demo-config.json \
	examples/demo-scenarios/return/return-policy.json \
	examples/demo-scenarios/return/positive-inventory.json \
	examples/demo-scenarios/return/positive-obligation.json \
	examples/demo-scenarios/return/negative-unauthorized-obligation.json \
	examples/demo-scenarios/return/negative-replay-obligation.json \
	examples/demo-scenarios/return/negative-mismatch-obligation.json \
	infra/README.md \
	daml/Foundation.daml \
	daml/Bootstrap.daml \
	daml/CantonCollateral/Types.daml \
	daml/CantonCollateral/Roles.daml \
	daml/CantonCollateral/Asset.daml \
	daml/CantonCollateral/Inventory.daml \
	daml/CantonCollateral/Encumbrance.daml \
	daml/CantonCollateral/Settlement.daml \
	daml/CantonCollateral/Report.daml \
	daml/CantonCollateral/Obligation.daml \
	daml/CantonCollateral/Posting.daml \
	daml/CantonCollateral/Substitution.daml \
	daml/CantonCollateral/Return.daml \
	daml/CantonCollateral/Demo.daml \
	daml/CantonCollateral/Test.daml \
	daml/CantonCollateral/QuickstartSeed.daml \
	daml/CantonCollateral/QuickstartMarginCall.daml \
	daml/CantonCollateral/ReferenceToken.daml \
	daml/CantonCollateral/QuickstartAdapter.daml \
	docs/mission-control/MASTER_TRACKER.md \
	docs/mission-control/ROADMAP.md \
	docs/mission-control/WORKLOG.md \
	docs/mission-control/DECISION_LOG.md \
	docs/architecture/OVERVIEW.md \
	docs/architecture/COMPONENTS.md \
	docs/architecture/DATA_FLOW.md \
	docs/architecture/DEPLOYMENT_MODEL.md \
	docs/architecture/PRIVACY_MODEL.md \
	docs/adrs/README.md \
	docs/adrs/0001-repo-principles.md \
	docs/adrs/0002-system-boundaries.md \
	docs/adrs/0003-policy-optimization-workflow-separation.md \
	docs/adrs/0004-report-fidelity-and-evidence.md \
	docs/adrs/0005-cpl-format-and-versioning.md \
	docs/adrs/0006-runtime-foundation.md \
	docs/adrs/0007-daml-contract-boundaries.md \
	docs/adrs/0008-policy-evaluation-engine.md \
	docs/adrs/0009-optimization-objective-and-determinism.md \
	docs/adrs/0010-rename-to-canton-collateral-control-plane.md \
	docs/adrs/0011-margin-call-demo-shape.md \
	docs/adrs/0012-substitution-atomicity.md \
		docs/adrs/0013-return-and-release-control.md \
	docs/adrs/0014-conformance-and-demo-package.md \
	docs/adrs/0015-quickstart-demo-foundation.md \
	docs/adrs/0016-quickstart-runtime-bridge.md \
	docs/adrs/0017-quickstart-confidential-seed.md \
	docs/adrs/0018-reference-token-adapter-path.md \
	docs/adrs/0019-quickstart-margin-call-demo-orchestration.md \
		docs/setup/LOCAL_DEV_SETUP.md \
	docs/setup/DEPENDENCY_POLICY.md \
	docs/invariants/INVARIANT_REGISTRY.md \
	docs/risks/RISK_REGISTER.md \
	docs/evidence/EVIDENCE_MANIFEST.md \
	docs/evidence/DEMO_ARTIFACT_INDEX.md \
	docs/evidence/prompt-01-execution-report.md \
	docs/evidence/prompt-02-execution-report.md \
	docs/evidence/prompt-03-execution-report.md \
	docs/evidence/prompt-04-execution-report.md \
	docs/evidence/prompt-05-execution-report.md \
	docs/evidence/prompt-06-execution-report.md \
	docs/evidence/prompt-07-execution-report.md \
	docs/evidence/prompt-08-execution-report.md \
	docs/evidence/prompt-09-execution-report.md \
		docs/evidence/prompt-10-execution-report.md \
		docs/evidence/prompt-11-execution-report.md \
		docs/evidence/prompt-12-execution-report.md \
		docs/evidence/prompt-13-execution-report.md \
		docs/evidence/prompt-14-execution-report.md \
		docs/evidence/prompt-15-execution-report.md \
		docs/evidence/prompt-16-execution-report.md \
		docs/evidence/rename-to-collateral-control-plane-execution-report.md \
	docs/runbooks/README.md \
	docs/runbooks/FINAL_DEMO_RUNBOOK.md \
	docs/runbooks/LOCALNET_CONTROL_PLANE_RUNBOOK.md \
	docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md \
	docs/runbooks/RETURN_DEMO_RUNBOOK.md \
	docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md \
	docs/integration/INTEGRATION_SURFACES.md \
	docs/integration/LOCALNET_DEMO_PLAN.md \
	docs/integration/QUICKSTART_INTEGRATION_PLAN.md \
	docs/integration/ASSET_ADAPTER_PLAN.md \
	docs/integration/THIRD_PARTY_INTEGRATION_GUIDE.md \
	docs/integration/TOKEN_STANDARD_ALIGNMENT.md \
	docs/domain/GLOSSARY.md \
	docs/domain/COLLATERAL_DOMAIN_MODEL.md \
	docs/domain/ACTORS_AND_ROLES.md \
	docs/domain/LIFECYCLE_STATES.md \
	docs/domain/DAML_MAPPING.md \
	docs/specs/CPL_SPEC_v0_1.md \
	docs/specs/CPL_EXAMPLES.md \
	docs/specs/POLICY_EVALUATION_REPORT_SPEC.md \
	docs/specs/OPTIMIZATION_REPORT_SPEC.md \
	docs/specs/EXECUTION_REPORT_SPEC.md \
	docs/specs/RETURN_REPORT_SPEC.md \
	docs/specs/SUBSTITUTION_REPORT_SPEC.md \
	docs/economic/OPTIMIZATION_OBJECTIVES.md \
	docs/testing/CPL_VALIDATION_TEST_PLAN.md \
	docs/testing/CONFORMANCE_SUITE.md \
	docs/testing/DAML_TEST_PLAN.md \
	docs/testing/POLICY_ENGINE_TEST_PLAN.md \
	docs/testing/OPTIMIZER_TEST_PLAN.md \
	docs/testing/TEST_STRATEGY.md \
	docs/security/THREAT_MODEL.md \
	docs/change-control/CHANGE_CONTROL.md \
	infra/quickstart/README.md \
	infra/quickstart/bootstrap-localnet.sh \
	infra/quickstart/overlay/README.md \
	infra/quickstart/overlay/control-plane-compose.yaml \
	infra/quickstart/overlay/upstream-pin.env \
	infra/quickstart/overlay/profiles/faithful.env.local \
	infra/quickstart/overlay/profiles/lean.env.local \
	infra/quickstart/scenarios/confidential-margin-scenario.json \
	infra/quickstart/scenarios/confidential-margin-demo-positive-scenario.json \
	infra/quickstart/scenarios/confidential-margin-demo-rejected-scenario.json \
	scripts/run-localnet-smoke.sh \
	$(CPL_SCHEMA) \
	$(POLICY_EVAL_REPORT_SCHEMA) \
	$(OPTIMIZATION_REPORT_SCHEMA) \
	$(EXECUTION_REPORT_SCHEMA) \
	$(RETURN_REPORT_SCHEMA) \
	$(SUBSTITUTION_REPORT_SCHEMA) \
	$(ADAPTER_EXECUTION_REPORT_SCHEMA) \
	$(CPL_EXAMPLES) \
	requirements-cpl-validation.txt

REQUIRED_DIRS := \
	daml \
	app \
	reports \
	scripts \
	test \
	examples \
	infra \
	docs/setup

.PHONY: bootstrap localnet-bootstrap localnet-smoke localnet-build-dar localnet-deploy-dar localnet-start-control-plane localnet-seed-demo localnet-status-control-plane localnet-run-margin-call-workflow localnet-run-token-adapter localnet-adapter-status docs-lint status verify-portable verify validate-cpl policy-eval optimize test-policy-engine test-optimizer test-conformance daml-build daml-test demo-run demo-margin-call demo-margin-call-quickstart demo-return demo-substitution demo-all clean-runtime

$(CHECK_JSONSCHEMA): requirements-cpl-validation.txt
	@$(PYTHON) -m venv $(VENV)
	@$(VENV)/bin/python -m pip install --upgrade pip >/dev/null
	@$(VENV)/bin/python -m pip install --requirement requirements-cpl-validation.txt >/dev/null

bootstrap:
	@$(BOOTSTRAP_SCRIPT)

docs-lint:
	@for file in $(REQUIRED_DOCS); do \
		test -f "$$file" || { echo "docs-lint: missing $$file"; exit 1; }; \
	done
	@for dir in $(REQUIRED_DIRS); do \
		test -d "$$dir" || { echo "docs-lint: missing directory $$dir"; exit 1; }; \
	done
	@for script in $(BOOTSTRAP_SCRIPT) $(STATUS_SCRIPT) $(LOCALNET_BUILD_DAR_SCRIPT) $(LOCALNET_DEPLOY_DAR_SCRIPT) $(LOCALNET_START_CONTROL_PLANE_SCRIPT) $(LOCALNET_SEED_DEMO_SCRIPT) $(LOCALNET_STATUS_CONTROL_PLANE_SCRIPT) $(LOCALNET_RUN_MARGIN_CALL_WORKFLOW_SCRIPT) $(LOCALNET_RUN_TOKEN_ADAPTER_SCRIPT) $(LOCALNET_ADAPTER_STATUS_SCRIPT) $(LOCALNET_DAML_SCRIPT_RUNNER) $(VERIFY_PORTABLE_SCRIPT) $(VERIFY_SCRIPT) $(LOCALNET_BOOTSTRAP_SCRIPT) $(LOCALNET_SMOKE_SCRIPT); do \
		test -x "$$script" || { echo "docs-lint: expected executable $$script"; exit 1; }; \
	done
	@grep -q "^sdk-version: $(DAML_SDK_VERSION)$$" daml.yaml || { echo "docs-lint: daml.yaml sdk-version mismatch"; exit 1; }
	@grep -q "^python $(PYTHON_TOOL_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned python"; exit 1; }
	@grep -q "^java temurin-$(JAVA_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned java"; exit 1; }
	@grep -q "make bootstrap" README.md || { echo "docs-lint: README missing bootstrap command"; exit 1; }
	@grep -q "make localnet-bootstrap" README.md || { echo "docs-lint: README missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" README.md || { echo "docs-lint: README missing localnet-smoke command"; exit 1; }
	@grep -q "make localnet-start-control-plane" README.md || { echo "docs-lint: README missing localnet-start-control-plane command"; exit 1; }
	@grep -q "make localnet-seed-demo" README.md || { echo "docs-lint: README missing localnet-seed-demo command"; exit 1; }
	@grep -q "make localnet-status-control-plane" README.md || { echo "docs-lint: README missing localnet-status-control-plane command"; exit 1; }
	@grep -q "make localnet-run-token-adapter" README.md || { echo "docs-lint: README missing localnet-run-token-adapter command"; exit 1; }
	@grep -q "make localnet-adapter-status" README.md || { echo "docs-lint: README missing localnet-adapter-status command"; exit 1; }
	@grep -q "make daml-build" README.md || { echo "docs-lint: README missing daml-build command"; exit 1; }
	@grep -q "make daml-test" README.md || { echo "docs-lint: README missing daml-test command"; exit 1; }
	@grep -q "make demo-run" README.md || { echo "docs-lint: README missing demo-run command"; exit 1; }
	@grep -q "make demo-margin-call" README.md || { echo "docs-lint: README missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-margin-call-quickstart" README.md || { echo "docs-lint: README missing demo-margin-call-quickstart command"; exit 1; }
	@grep -q "make demo-return" README.md || { echo "docs-lint: README missing demo-return command"; exit 1; }
	@grep -q "make demo-substitution" README.md || { echo "docs-lint: README missing demo-substitution command"; exit 1; }
	@grep -q "make test-conformance" README.md || { echo "docs-lint: README missing test-conformance command"; exit 1; }
	@grep -q "make demo-all" README.md || { echo "docs-lint: README missing demo-all command"; exit 1; }
	@grep -q "make verify-portable" README.md || { echo "docs-lint: README missing verify-portable command"; exit 1; }
	@grep -q "make policy-eval" README.md || { echo "docs-lint: README missing policy-eval command"; exit 1; }
	@grep -q "make optimize" README.md || { echo "docs-lint: README missing optimize command"; exit 1; }
	@grep -q "make test-policy-engine" README.md || { echo "docs-lint: README missing test-policy-engine command"; exit 1; }
	@grep -q "make test-optimizer" README.md || { echo "docs-lint: README missing test-optimizer command"; exit 1; }
	@grep -q "make localnet-bootstrap" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-smoke command"; exit 1; }
	@grep -q "make localnet-start-control-plane" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-start-control-plane command"; exit 1; }
	@grep -q "make localnet-seed-demo" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-seed-demo command"; exit 1; }
	@grep -q "make localnet-status-control-plane" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-status-control-plane command"; exit 1; }
	@grep -q "make localnet-run-token-adapter" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-run-token-adapter command"; exit 1; }
	@grep -q "make localnet-adapter-status" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-adapter-status command"; exit 1; }
	@grep -q "make daml-test" AGENTS.md || { echo "docs-lint: AGENTS missing daml-test command"; exit 1; }
	@grep -q "make demo-margin-call" AGENTS.md || { echo "docs-lint: AGENTS missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-margin-call-quickstart" AGENTS.md || { echo "docs-lint: AGENTS missing demo-margin-call-quickstart command"; exit 1; }
	@grep -q "make demo-return" AGENTS.md || { echo "docs-lint: AGENTS missing demo-return command"; exit 1; }
	@grep -q "make demo-substitution" AGENTS.md || { echo "docs-lint: AGENTS missing demo-substitution command"; exit 1; }
	@grep -q "make test-conformance" AGENTS.md || { echo "docs-lint: AGENTS missing test-conformance command"; exit 1; }
	@grep -q "make demo-all" AGENTS.md || { echo "docs-lint: AGENTS missing demo-all command"; exit 1; }
	@grep -q "make verify-portable" AGENTS.md || { echo "docs-lint: AGENTS missing verify-portable command"; exit 1; }
	@grep -q "make policy-eval" AGENTS.md || { echo "docs-lint: AGENTS missing policy-eval command"; exit 1; }
	@grep -q "make optimize" AGENTS.md || { echo "docs-lint: AGENTS missing optimize command"; exit 1; }
	@grep -q "make test-policy-engine" AGENTS.md || { echo "docs-lint: AGENTS missing test-policy-engine command"; exit 1; }
	@grep -q "make test-optimizer" AGENTS.md || { echo "docs-lint: AGENTS missing test-optimizer command"; exit 1; }
	@grep -q "make localnet-bootstrap" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-smoke command"; exit 1; }
	@grep -q "make localnet-start-control-plane" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-start-control-plane command"; exit 1; }
	@grep -q "make localnet-seed-demo" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-seed-demo command"; exit 1; }
	@grep -q "make localnet-status-control-plane" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-status-control-plane command"; exit 1; }
	@grep -q "make localnet-run-token-adapter" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-run-token-adapter command"; exit 1; }
	@grep -q "make localnet-adapter-status" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-adapter-status command"; exit 1; }
	@grep -q "make daml-test" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing daml-test command"; exit 1; }
	@grep -q "make demo-margin-call" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-margin-call-quickstart" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-margin-call-quickstart command"; exit 1; }
	@grep -q "make demo-return" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-return command"; exit 1; }
	@grep -q "make demo-substitution" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-substitution command"; exit 1; }
	@grep -q "make test-conformance" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing test-conformance command"; exit 1; }
	@grep -q "make demo-all" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-all command"; exit 1; }
	@grep -q "make verify-portable" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing verify-portable command"; exit 1; }
	@grep -q "make optimize" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing optimize command"; exit 1; }
	@grep -q "make test-optimizer" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing test-optimizer command"; exit 1; }
	@grep -q "workflowSmokeTest" daml.yaml || { echo "docs-lint: daml.yaml missing workflow smoke init script"; exit 1; }
	@grep -q "Daml SDK $(DAML_SDK_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Daml SDK pin"; exit 1; }
	@grep -q "Temurin JDK $(JAVA_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Java pin"; exit 1; }
	@grep -q "make localnet-bootstrap" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-bootstrap"; exit 1; }
	@grep -q "make localnet-smoke" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-smoke"; exit 1; }
	@grep -q "make localnet-start-control-plane" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-start-control-plane"; exit 1; }
	@grep -q "make localnet-seed-demo" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-seed-demo"; exit 1; }
	@grep -q "make localnet-status-control-plane" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-status-control-plane"; exit 1; }
	@grep -q "make localnet-run-token-adapter" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-run-token-adapter"; exit 1; }
	@grep -q "make localnet-adapter-status" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-adapter-status"; exit 1; }
	@grep -q "make daml-test" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing daml-test"; exit 1; }
	@grep -q "make demo-margin-call" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-margin-call"; exit 1; }
	@grep -q "make demo-margin-call-quickstart" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-margin-call-quickstart"; exit 1; }
	@grep -q "make demo-return" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-return"; exit 1; }
	@grep -q "make demo-substitution" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-substitution"; exit 1; }
	@grep -q "make test-conformance" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing test-conformance"; exit 1; }
	@grep -q "make demo-all" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-all"; exit 1; }
	@grep -q "make verify-portable" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing verify-portable"; exit 1; }
	@grep -q "make policy-eval" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing policy-eval"; exit 1; }
	@grep -q "make optimize" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing optimize"; exit 1; }
	@grep -q "make test-optimizer" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing test-optimizer"; exit 1; }
	@grep -q "make localnet-smoke" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-smoke"; exit 1; }
	@grep -q "make localnet-start-control-plane" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-start-control-plane"; exit 1; }
	@grep -q "make localnet-seed-demo" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-seed-demo"; exit 1; }
	@grep -q "make localnet-status-control-plane" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-status-control-plane"; exit 1; }
	@grep -q "make localnet-run-token-adapter" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-run-token-adapter"; exit 1; }
	@grep -q "make localnet-adapter-status" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-adapter-status"; exit 1; }
	@grep -q "make demo-run" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-run"; exit 1; }
	@grep -q "make daml-test" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing daml-test"; exit 1; }
	@grep -q "make demo-margin-call" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-margin-call"; exit 1; }
	@grep -q "make demo-margin-call-quickstart" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-margin-call-quickstart"; exit 1; }
	@grep -q "make demo-return" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-return"; exit 1; }
	@grep -q "make demo-substitution" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-substitution"; exit 1; }
	@grep -q "make test-conformance" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-conformance"; exit 1; }
	@grep -q "make demo-all" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-all"; exit 1; }
	@grep -q "make verify-portable" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing verify-portable"; exit 1; }
	@grep -q "make test-policy-engine" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-policy-engine"; exit 1; }
	@grep -q "make optimize" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing optimize"; exit 1; }
	@grep -q "make test-optimizer" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-optimizer"; exit 1; }
	@grep -q "ADR 0006" docs/adrs/0006-runtime-foundation.md || { echo "docs-lint: ADR 0006 missing title"; exit 1; }
	@grep -q "ADR 0007" docs/adrs/0007-daml-contract-boundaries.md || { echo "docs-lint: ADR 0007 missing title"; exit 1; }
	@grep -q "ADR 0011" docs/adrs/0011-margin-call-demo-shape.md || { echo "docs-lint: ADR 0011 missing title"; exit 1; }
	@grep -q "ADR 0012" docs/adrs/0012-substitution-atomicity.md || { echo "docs-lint: ADR 0012 missing title"; exit 1; }
	@grep -q "ADR 0013" docs/adrs/0013-return-and-release-control.md || { echo "docs-lint: ADR 0013 missing title"; exit 1; }
	@grep -q "ADR 0014" docs/adrs/0014-conformance-and-demo-package.md || { echo "docs-lint: ADR 0014 missing title"; exit 1; }
	@grep -q "ADR 0015" docs/adrs/0015-quickstart-demo-foundation.md || { echo "docs-lint: ADR 0015 missing title"; exit 1; }
	@grep -q "ADR 0016" docs/adrs/0016-quickstart-runtime-bridge.md || { echo "docs-lint: ADR 0016 missing title"; exit 1; }
	@grep -q "ADR 0017" docs/adrs/0017-quickstart-confidential-seed.md || { echo "docs-lint: ADR 0017 missing title"; exit 1; }
	@grep -q "ADR 0018" docs/adrs/0018-reference-token-adapter-path.md || { echo "docs-lint: ADR 0018 missing title"; exit 1; }
	@grep -q "ADR 0019" docs/adrs/0019-quickstart-margin-call-demo-orchestration.md || { echo "docs-lint: ADR 0019 missing title"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-04-execution-report.md || { echo "docs-lint: prompt 4 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-05-execution-report.md || { echo "docs-lint: prompt 5 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-06-execution-report.md || { echo "docs-lint: prompt 6 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-07-execution-report.md || { echo "docs-lint: prompt 7 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-08-execution-report.md || { echo "docs-lint: prompt 8 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-09-execution-report.md || { echo "docs-lint: prompt 9 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-10-execution-report.md || { echo "docs-lint: prompt 10 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-11-execution-report.md || { echo "docs-lint: prompt 11 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-12-execution-report.md || { echo "docs-lint: prompt 12 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-13-execution-report.md || { echo "docs-lint: prompt 13 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-14-execution-report.md || { echo "docs-lint: prompt 14 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-15-execution-report.md || { echo "docs-lint: prompt 15 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-16-execution-report.md || { echo "docs-lint: prompt 16 execution report incomplete"; exit 1; }
	@grep -q "Prompt 5 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 5 status"; exit 1; }
	@grep -q "Prompt 6 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 6 status"; exit 1; }
	@grep -q "Prompt 7 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 7 status"; exit 1; }
	@grep -q "Prompt 8 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 8 status"; exit 1; }
	@grep -q "Prompt 9 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 9 status"; exit 1; }
	@grep -q "Prompt 10 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 10 status"; exit 1; }
	@grep -q "Prompt 11 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 11 status"; exit 1; }
	@grep -q "Prompt 12 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 12 status"; exit 1; }
	@grep -q "Prompt 13 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 13 status"; exit 1; }
	@grep -q "Prompt 14 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 14 status"; exit 1; }
	@grep -q "Prompt 15 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 15 status"; exit 1; }
	@grep -q "Prompt 16 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 16 status"; exit 1; }
	@echo "docs-lint: policy engine, optimizer, Quickstart seeded scenario, runtime bridge, return demo, substitution demo, runtime foundation, Daml workflow skeleton, and command surface documentation are present"

localnet-bootstrap:
	@LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	$(LOCALNET_BOOTSTRAP_SCRIPT)

localnet-smoke: localnet-bootstrap
	@LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	$(LOCALNET_SMOKE_SCRIPT)

localnet-build-dar: bootstrap
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	$(LOCALNET_BUILD_DAR_SCRIPT)

localnet-deploy-dar: bootstrap localnet-bootstrap
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	$(LOCALNET_DEPLOY_DAR_SCRIPT)

localnet-start-control-plane: bootstrap localnet-bootstrap
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	LOCALNET_SCENARIO_MANIFEST="$(LOCALNET_SCENARIO_MANIFEST)" \
	$(LOCALNET_START_CONTROL_PLANE_SCRIPT)

localnet-seed-demo: bootstrap localnet-bootstrap
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	LOCALNET_SCENARIO_MANIFEST="$(LOCALNET_SCENARIO_MANIFEST)" \
	$(LOCALNET_SEED_DEMO_SCRIPT)

localnet-status-control-plane: bootstrap localnet-bootstrap
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	LOCALNET_SCENARIO_MANIFEST="$(LOCALNET_SCENARIO_MANIFEST)" \
	$(LOCALNET_STATUS_CONTROL_PLANE_SCRIPT)

localnet-run-margin-call-workflow: bootstrap localnet-bootstrap
	@echo "localnet-run-margin-call-workflow: use scripts/localnet-run-margin-call-workflow.sh with explicit --input-file and --output-file paths"

localnet-run-token-adapter: bootstrap localnet-bootstrap localnet-seed-demo $(CHECK_JSONSCHEMA)
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	LOCALNET_SCENARIO_MANIFEST="$(LOCALNET_SCENARIO_MANIFEST)" \
	LOCALNET_CONTROL_PLANE_OUTPUT_DIR="$(LOCALNET_ADAPTER_OUTPUT_DIR)" \
	$(LOCALNET_RUN_TOKEN_ADAPTER_SCRIPT)
	@$(CHECK_JSONSCHEMA) --schemafile $(ADAPTER_EXECUTION_REPORT_SCHEMA) "$(LOCALNET_ADAPTER_OUTPUT_DIR)/localnet-reference-token-adapter-execution-report.json"
	@echo "localnet-run-token-adapter: generated $(LOCALNET_ADAPTER_OUTPUT_DIR)/localnet-reference-token-adapter-execution-report.json"

localnet-adapter-status: bootstrap localnet-bootstrap localnet-seed-demo
	@LOCALNET_WORKDIR="$(LOCALNET_WORKDIR)" \
	LOCALNET_PROFILE="$(LOCALNET_PROFILE)" \
	LOCALNET_PARTY_HINT="$(LOCALNET_PARTY_HINT)" \
	LOCALNET_SCENARIO_MANIFEST="$(LOCALNET_SCENARIO_MANIFEST)" \
	LOCALNET_CONTROL_PLANE_OUTPUT_DIR="$(LOCALNET_ADAPTER_OUTPUT_DIR)" \
	$(LOCALNET_ADAPTER_STATUS_SCRIPT)
	@echo "localnet-adapter-status: refreshed $(LOCALNET_ADAPTER_OUTPUT_DIR)/localnet-reference-token-adapter-status.json"

validate-cpl: $(CHECK_JSONSCHEMA)
	@$(CHECK_JSONSCHEMA) --check-metaschema $(CPL_SCHEMA)
	@$(CHECK_JSONSCHEMA) --schemafile $(CPL_SCHEMA) $(CPL_EXAMPLES)
	@tmpdir=$$(mktemp -d); \
		trap 'rm -rf "$$tmpdir"' EXIT; \
		sed '/"policyId":/d' examples/policies/central-bank-style-policy.json > "$$tmpdir/missing-policy-id.json"; \
		if $(CHECK_JSONSCHEMA) --schemafile $(CPL_SCHEMA) "$$tmpdir/missing-policy-id.json" >/dev/null 2>&1; then \
			echo "validate-cpl: expected missing policyId case to fail"; \
			exit 1; \
		fi; \
		awk 'NR == 1 { print "{"; print "  \"unexpectedTopLevel\": true,"; next } { print }' examples/policies/central-bank-style-policy.json > "$$tmpdir/unknown-property.json"; \
		if $(CHECK_JSONSCHEMA) --schemafile $(CPL_SCHEMA) "$$tmpdir/unknown-property.json" >/dev/null 2>&1; then \
			echo "validate-cpl: expected unknown property case to fail"; \
			exit 1; \
		fi
	@echo "validate-cpl: schema and example policy checks passed"

policy-eval: $(CHECK_JSONSCHEMA)
	@test -n "$(POLICY)" || { echo "policy-eval: POLICY=... is required"; exit 1; }
	@test -n "$(INVENTORY)" || { echo "policy-eval: INVENTORY=... is required"; exit 1; }
	@$(CHECK_JSONSCHEMA) --schemafile $(CPL_SCHEMA) "$(POLICY)"
	@if [ -n "$(REPORT)" ]; then \
		output_path=$$($(PYTHON) app/policy-engine/cli.py --policy "$(POLICY)" --inventory "$(INVENTORY)" --output "$(REPORT)"); \
	else \
		output_path=$$($(PYTHON) app/policy-engine/cli.py --policy "$(POLICY)" --inventory "$(INVENTORY)"); \
	fi; \
	$(CHECK_JSONSCHEMA) --schemafile $(POLICY_EVAL_REPORT_SCHEMA) "$$output_path"; \
	echo "policy-eval: generated $$output_path"

optimize: $(CHECK_JSONSCHEMA)
	@test -n "$(POLICY)" || { echo "optimize: POLICY=... is required"; exit 1; }
	@test -n "$(INVENTORY)" || { echo "optimize: INVENTORY=... is required"; exit 1; }
	@test -n "$(OBLIGATION)" || { echo "optimize: OBLIGATION=... is required"; exit 1; }
	@$(CHECK_JSONSCHEMA) --schemafile $(CPL_SCHEMA) "$(POLICY)"
	@if [ -n "$(REPORT)" ]; then \
		output_path=$$($(PYTHON) app/optimizer/cli.py --policy "$(POLICY)" --inventory "$(INVENTORY)" --obligation "$(OBLIGATION)" --output "$(REPORT)"); \
	else \
		output_path=$$($(PYTHON) app/optimizer/cli.py --policy "$(POLICY)" --inventory "$(INVENTORY)" --obligation "$(OBLIGATION)"); \
	fi; \
	$(CHECK_JSONSCHEMA) --schemafile $(OPTIMIZATION_REPORT_SCHEMA) "$$output_path"; \
	echo "optimize: generated $$output_path"

test-policy-engine: $(CHECK_JSONSCHEMA)
	@PYTHONPATH=app/policy-engine $(PYTHON) -m unittest discover -s test/policy-engine -p 'test_*.py'
	@$(MAKE) --no-print-directory policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json REPORT=reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json
	@echo "test-policy-engine: deterministic policy-engine tests and report validation passed"

test-optimizer: $(CHECK_JSONSCHEMA)
	@PYTHONPATH=app/optimizer:app/policy-engine $(PYTHON) -m unittest discover -s test/optimizer -p 'test_*.py'
	@$(MAKE) --no-print-directory optimize POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json OBLIGATION=examples/obligations/central-bank-window-call.json REPORT=reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-central-bank-window-call-optimization-report.json
	@echo "test-optimizer: deterministic optimizer tests and report validation passed"

test-conformance: daml-build $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/conformance_cli.py --output-dir "$(CONFORMANCE_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		test -f "$$output_path" || { echo "test-conformance: missing conformance report"; exit 1; }; \
		PYTHONPATH=app/orchestration $(PYTHON) -m unittest discover -s test/conformance -p 'test_*.py'; \
		echo "test-conformance: generated $$output_path and validated the aggregate conformance suite"

status:
	@$(STATUS_SCRIPT)

verify-portable:
	@$(VERIFY_PORTABLE_SCRIPT)

daml-build: bootstrap
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		rm -rf "$(REPO_ROOT)/.daml/dist"; \
		"$$DAML_BIN" build --project-root "$(REPO_ROOT)"; \
		dar_file=$$(find "$(REPO_ROOT)/.daml/dist" -maxdepth 1 -name '*.dar' | head -n 1); \
		test -n "$$dar_file" || { echo "daml-build: no DAR produced"; exit 1; }; \
		echo "daml-build: built $$dar_file"

daml-test: daml-build
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		dar_file=$$(find "$(REPO_ROOT)/.daml/dist" -maxdepth 1 -name '*.dar' | head -n 1); \
		test -n "$$dar_file" || { echo "daml-test: missing DAR file"; exit 1; }; \
		"$$DAML_BIN" script --dar "$$dar_file" --script-name CantonCollateral.Test:marginCallLifecycleTest --ide-ledger >/dev/null; \
		"$$DAML_BIN" script --dar "$$dar_file" --script-name CantonCollateral.Test:postingAndSubstitutionLifecycleTest --ide-ledger >/dev/null; \
		"$$DAML_BIN" script --dar "$$dar_file" --script-name CantonCollateral.Test:returnLifecycleTest --ide-ledger >/dev/null; \
		echo "daml-test: lifecycle scripts passed"

demo-run: daml-build
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		dar_file=$$(find "$(REPO_ROOT)/.daml/dist" -maxdepth 1 -name '*.dar' | head -n 1); \
		test -n "$$dar_file" || { echo "demo-run: missing DAR file"; exit 1; }; \
		"$$DAML_BIN" script --dar "$$dar_file" --script-name Bootstrap:workflowSmokeTest --ide-ledger

demo-margin-call: daml-build $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/cli.py --manifest "$(MARGIN_CALL_DEMO_MANIFEST)" --output-dir "$(MARGIN_CALL_DEMO_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		$(CHECK_JSONSCHEMA) --schemafile $(EXECUTION_REPORT_SCHEMA) "$$output_path"; \
		test -f "$(MARGIN_CALL_DEMO_OUTPUT_DIR)/margin-call-demo-summary.md" || { echo "demo-margin-call: missing markdown summary"; exit 1; }; \
		test -f "$(MARGIN_CALL_DEMO_OUTPUT_DIR)/margin-call-demo-timeline.md" || { echo "demo-margin-call: missing timeline markdown"; exit 1; }; \
		echo "demo-margin-call: generated $$output_path"

demo-margin-call-quickstart: localnet-start-control-plane $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/cli.py \
			--manifest "$(MARGIN_CALL_QUICKSTART_DEMO_MANIFEST)" \
			--output-dir "$(MARGIN_CALL_DEMO_OUTPUT_DIR)" \
			--repo-root "$(REPO_ROOT)" \
			--runtime QUICKSTART \
			--report-basename margin-call-quickstart \
			--command-name "make demo-margin-call-quickstart"); \
		$(CHECK_JSONSCHEMA) --schemafile $(EXECUTION_REPORT_SCHEMA) "$$output_path"; \
		test -f "$(MARGIN_CALL_DEMO_OUTPUT_DIR)/margin-call-quickstart-summary.md" || { echo "demo-margin-call-quickstart: missing markdown summary"; exit 1; }; \
		test -f "$(MARGIN_CALL_DEMO_OUTPUT_DIR)/margin-call-quickstart-timeline.md" || { echo "demo-margin-call-quickstart: missing timeline markdown"; exit 1; }; \
		echo "demo-margin-call-quickstart: generated $$output_path"

demo-return: daml-build $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/return_cli.py --manifest "$(RETURN_DEMO_MANIFEST)" --output-dir "$(RETURN_DEMO_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		$(CHECK_JSONSCHEMA) --schemafile $(RETURN_REPORT_SCHEMA) "$$output_path"; \
		test -f "$(RETURN_DEMO_OUTPUT_DIR)/return-demo-summary.md" || { echo "demo-return: missing markdown summary"; exit 1; }; \
		test -f "$(RETURN_DEMO_OUTPUT_DIR)/return-demo-timeline.md" || { echo "demo-return: missing timeline markdown"; exit 1; }; \
		echo "demo-return: generated $$output_path"

demo-substitution: daml-build $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/substitution_cli.py --manifest "$(SUBSTITUTION_DEMO_MANIFEST)" --output-dir "$(SUBSTITUTION_DEMO_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		$(CHECK_JSONSCHEMA) --schemafile $(SUBSTITUTION_REPORT_SCHEMA) "$$output_path"; \
		test -f "$(SUBSTITUTION_DEMO_OUTPUT_DIR)/substitution-demo-summary.md" || { echo "demo-substitution: missing markdown summary"; exit 1; }; \
		test -f "$(SUBSTITUTION_DEMO_OUTPUT_DIR)/substitution-demo-timeline.md" || { echo "demo-substitution: missing timeline markdown"; exit 1; }; \
		echo "demo-substitution: generated $$output_path"

demo-all: test-conformance
	@output_path=$$($(PYTHON) app/orchestration/final_demo_cli.py --conformance-report "$(CONFORMANCE_REPORT)" --output-dir "$(FINAL_DEMO_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		test -f "$$output_path" || { echo "demo-all: missing final demo-pack report"; exit 1; }; \
		test -f "$(FINAL_DEMO_OUTPUT_DIR)/final-demo-pack-summary.md" || { echo "demo-all: missing markdown summary"; exit 1; }; \
		echo "demo-all: generated $$output_path"

verify:
	@$(VERIFY_SCRIPT)

clean-runtime:
	@rm -rf $(RUNTIME_DIR) .daml/dist .daml/dist-quickstart .daml/package-database
