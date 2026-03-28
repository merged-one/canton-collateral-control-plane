SHELL := /bin/sh
PYTHON ?= python3
REPO_ROOT := $(CURDIR)
RUNTIME_DIR := .runtime
RUNTIME_ENV := $(RUNTIME_DIR)/env.sh
BOOTSTRAP_SCRIPT := scripts/bootstrap.sh
STATUS_SCRIPT := scripts/dev-status.sh
VERIFY_SCRIPT := scripts/verify.sh
LOCALNET_BOOTSTRAP_SCRIPT := infra/quickstart/bootstrap-localnet.sh
LOCALNET_SMOKE_SCRIPT := scripts/run-localnet-smoke.sh

include scripts/toolchain.env

VENV := .venv
CHECK_JSONSCHEMA := $(VENV)/bin/check-jsonschema
CPL_SCHEMA := schema/cpl.schema.json
POLICY_EVAL_REPORT_SCHEMA := reports/schemas/policy-evaluation-report.schema.json
OPTIMIZATION_REPORT_SCHEMA := reports/schemas/optimization-report.schema.json
EXECUTION_REPORT_SCHEMA := reports/schemas/execution-report.schema.json
SUBSTITUTION_REPORT_SCHEMA := reports/schemas/substitution-report.schema.json
POLICY ?= examples/policies/central-bank-style-policy.json
INVENTORY ?= examples/inventory/central-bank-eligible-inventory.json
OBLIGATION ?= examples/obligations/central-bank-window-call.json
REPORT ?=
MARGIN_CALL_DEMO_MANIFEST ?= examples/demo-scenarios/margin-call/demo-config.json
MARGIN_CALL_DEMO_OUTPUT_DIR ?= reports/generated
SUBSTITUTION_DEMO_MANIFEST ?= examples/demo-scenarios/substitution/demo-config.json
SUBSTITUTION_DEMO_OUTPUT_DIR ?= reports/generated
LOCALNET_PROFILE ?= lean
LOCALNET_WORKDIR ?= $(REPO_ROOT)/.runtime/localnet/cn-quickstart
LOCALNET_PARTY_HINT ?= canton-collateral-1
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
	scripts/verify.sh \
	app/README.md \
	app/policy-engine/cli.py \
	app/policy-engine/constants.py \
	app/policy-engine/evaluator.py \
	app/optimizer/cli.py \
	app/optimizer/optimizer.py \
	app/optimizer/optimizer_constants.py \
	app/orchestration/cli.py \
	app/orchestration/margin_call_demo.py \
	app/orchestration/substitution_cli.py \
	app/orchestration/substitution_demo.py \
	reports/README.md \
	reports/schemas/policy-evaluation-report.schema.json \
	reports/schemas/optimization-report.schema.json \
	reports/schemas/execution-report.schema.json \
	reports/schemas/substitution-report.schema.json \
	test/README.md \
	test/policy-engine/test_policy_engine.py \
	test/optimizer/test_optimizer.py \
	examples/README.md \
	examples/inventory/central-bank-eligible-inventory.json \
	examples/obligations/central-bank-window-call.json \
	examples/obligations/central-bank-window-remediation.json \
	examples/demo-scenarios/margin-call/README.md \
	examples/demo-scenarios/margin-call/demo-config.json \
	examples/demo-scenarios/margin-call/positive-inventory.json \
	examples/demo-scenarios/margin-call/positive-obligation.json \
	examples/demo-scenarios/margin-call/negative-ineligible-inventory.json \
	examples/demo-scenarios/margin-call/negative-ineligible-obligation.json \
	examples/demo-scenarios/margin-call/negative-insufficient-inventory.json \
	examples/demo-scenarios/margin-call/negative-insufficient-obligation.json \
	examples/demo-scenarios/margin-call/negative-expired-policy-window-inventory.json \
	examples/demo-scenarios/margin-call/negative-expired-policy-window-obligation.json \
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
	docs/adrs/0013-quickstart-demo-foundation.md \
	docs/setup/LOCAL_DEV_SETUP.md \
	docs/setup/DEPENDENCY_POLICY.md \
	docs/invariants/INVARIANT_REGISTRY.md \
	docs/risks/RISK_REGISTER.md \
	docs/evidence/EVIDENCE_MANIFEST.md \
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
	docs/evidence/rename-to-collateral-control-plane-execution-report.md \
	docs/runbooks/README.md \
	docs/runbooks/MARGIN_CALL_DEMO_RUNBOOK.md \
	docs/runbooks/SUBSTITUTION_DEMO_RUNBOOK.md \
	docs/integration/INTEGRATION_SURFACES.md \
	docs/integration/LOCALNET_DEMO_PLAN.md \
	docs/integration/QUICKSTART_INTEGRATION_PLAN.md \
	docs/integration/ASSET_ADAPTER_PLAN.md \
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
	docs/specs/SUBSTITUTION_REPORT_SPEC.md \
	docs/economic/OPTIMIZATION_OBJECTIVES.md \
	docs/testing/CPL_VALIDATION_TEST_PLAN.md \
	docs/testing/DAML_TEST_PLAN.md \
	docs/testing/POLICY_ENGINE_TEST_PLAN.md \
	docs/testing/OPTIMIZER_TEST_PLAN.md \
	docs/testing/TEST_STRATEGY.md \
	docs/security/THREAT_MODEL.md \
	docs/change-control/CHANGE_CONTROL.md \
	infra/quickstart/README.md \
	infra/quickstart/bootstrap-localnet.sh \
	infra/quickstart/overlay/README.md \
	infra/quickstart/overlay/upstream-pin.env \
	infra/quickstart/overlay/profiles/faithful.env.local \
	infra/quickstart/overlay/profiles/lean.env.local \
	scripts/run-localnet-smoke.sh \
	$(CPL_SCHEMA) \
	$(POLICY_EVAL_REPORT_SCHEMA) \
	$(OPTIMIZATION_REPORT_SCHEMA) \
	$(EXECUTION_REPORT_SCHEMA) \
	$(SUBSTITUTION_REPORT_SCHEMA) \
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

.PHONY: bootstrap localnet-bootstrap localnet-smoke docs-lint status verify validate-cpl policy-eval optimize test-policy-engine test-optimizer daml-build daml-test demo-run demo-margin-call demo-substitution clean-runtime

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
	@for script in $(BOOTSTRAP_SCRIPT) $(STATUS_SCRIPT) $(VERIFY_SCRIPT) $(LOCALNET_BOOTSTRAP_SCRIPT) $(LOCALNET_SMOKE_SCRIPT); do \
		test -x "$$script" || { echo "docs-lint: expected executable $$script"; exit 1; }; \
	done
	@grep -q "^sdk-version: $(DAML_SDK_VERSION)$$" daml.yaml || { echo "docs-lint: daml.yaml sdk-version mismatch"; exit 1; }
	@grep -q "^python $(PYTHON_TOOL_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned python"; exit 1; }
	@grep -q "^java temurin-$(JAVA_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned java"; exit 1; }
	@grep -q "make bootstrap" README.md || { echo "docs-lint: README missing bootstrap command"; exit 1; }
	@grep -q "make localnet-bootstrap" README.md || { echo "docs-lint: README missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" README.md || { echo "docs-lint: README missing localnet-smoke command"; exit 1; }
	@grep -q "make daml-build" README.md || { echo "docs-lint: README missing daml-build command"; exit 1; }
	@grep -q "make daml-test" README.md || { echo "docs-lint: README missing daml-test command"; exit 1; }
	@grep -q "make demo-run" README.md || { echo "docs-lint: README missing demo-run command"; exit 1; }
	@grep -q "make demo-margin-call" README.md || { echo "docs-lint: README missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-substitution" README.md || { echo "docs-lint: README missing demo-substitution command"; exit 1; }
	@grep -q "make policy-eval" README.md || { echo "docs-lint: README missing policy-eval command"; exit 1; }
	@grep -q "make optimize" README.md || { echo "docs-lint: README missing optimize command"; exit 1; }
	@grep -q "make test-policy-engine" README.md || { echo "docs-lint: README missing test-policy-engine command"; exit 1; }
	@grep -q "make test-optimizer" README.md || { echo "docs-lint: README missing test-optimizer command"; exit 1; }
	@grep -q "make localnet-bootstrap" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" AGENTS.md || { echo "docs-lint: AGENTS missing localnet-smoke command"; exit 1; }
	@grep -q "make daml-test" AGENTS.md || { echo "docs-lint: AGENTS missing daml-test command"; exit 1; }
	@grep -q "make demo-margin-call" AGENTS.md || { echo "docs-lint: AGENTS missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-substitution" AGENTS.md || { echo "docs-lint: AGENTS missing demo-substitution command"; exit 1; }
	@grep -q "make policy-eval" AGENTS.md || { echo "docs-lint: AGENTS missing policy-eval command"; exit 1; }
	@grep -q "make optimize" AGENTS.md || { echo "docs-lint: AGENTS missing optimize command"; exit 1; }
	@grep -q "make test-policy-engine" AGENTS.md || { echo "docs-lint: AGENTS missing test-policy-engine command"; exit 1; }
	@grep -q "make test-optimizer" AGENTS.md || { echo "docs-lint: AGENTS missing test-optimizer command"; exit 1; }
	@grep -q "make localnet-bootstrap" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-bootstrap command"; exit 1; }
	@grep -q "make localnet-smoke" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing localnet-smoke command"; exit 1; }
	@grep -q "make daml-test" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing daml-test command"; exit 1; }
	@grep -q "make demo-margin-call" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-margin-call command"; exit 1; }
	@grep -q "make demo-substitution" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing demo-substitution command"; exit 1; }
	@grep -q "make optimize" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing optimize command"; exit 1; }
	@grep -q "make test-optimizer" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing test-optimizer command"; exit 1; }
	@grep -q "workflowSmokeTest" daml.yaml || { echo "docs-lint: daml.yaml missing workflow smoke init script"; exit 1; }
	@grep -q "Daml SDK $(DAML_SDK_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Daml SDK pin"; exit 1; }
	@grep -q "Temurin JDK $(JAVA_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Java pin"; exit 1; }
	@grep -q "make localnet-bootstrap" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-bootstrap"; exit 1; }
	@grep -q "make localnet-smoke" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing localnet-smoke"; exit 1; }
	@grep -q "make daml-test" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing daml-test"; exit 1; }
	@grep -q "make demo-margin-call" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-margin-call"; exit 1; }
	@grep -q "make demo-substitution" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing demo-substitution"; exit 1; }
	@grep -q "make policy-eval" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing policy-eval"; exit 1; }
	@grep -q "make optimize" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing optimize"; exit 1; }
	@grep -q "make test-optimizer" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing test-optimizer"; exit 1; }
	@grep -q "make localnet-smoke" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing localnet-smoke"; exit 1; }
	@grep -q "make demo-run" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-run"; exit 1; }
	@grep -q "make daml-test" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing daml-test"; exit 1; }
	@grep -q "make demo-margin-call" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-margin-call"; exit 1; }
	@grep -q "make demo-substitution" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-substitution"; exit 1; }
	@grep -q "make test-policy-engine" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-policy-engine"; exit 1; }
	@grep -q "make optimize" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing optimize"; exit 1; }
	@grep -q "make test-optimizer" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-optimizer"; exit 1; }
	@grep -q "ADR 0006" docs/adrs/0006-runtime-foundation.md || { echo "docs-lint: ADR 0006 missing title"; exit 1; }
	@grep -q "ADR 0007" docs/adrs/0007-daml-contract-boundaries.md || { echo "docs-lint: ADR 0007 missing title"; exit 1; }
	@grep -q "ADR 0011" docs/adrs/0011-margin-call-demo-shape.md || { echo "docs-lint: ADR 0011 missing title"; exit 1; }
	@grep -q "ADR 0012" docs/adrs/0012-substitution-atomicity.md || { echo "docs-lint: ADR 0012 missing title"; exit 1; }
	@grep -q "ADR 0013" docs/adrs/0013-quickstart-demo-foundation.md || { echo "docs-lint: ADR 0013 missing title"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-04-execution-report.md || { echo "docs-lint: prompt 4 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-05-execution-report.md || { echo "docs-lint: prompt 5 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-06-execution-report.md || { echo "docs-lint: prompt 6 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-07-execution-report.md || { echo "docs-lint: prompt 7 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-08-execution-report.md || { echo "docs-lint: prompt 8 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-09-execution-report.md || { echo "docs-lint: prompt 9 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-10-execution-report.md || { echo "docs-lint: prompt 10 execution report incomplete"; exit 1; }
	@grep -q "Prompt 5 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 5 status"; exit 1; }
	@grep -q "Prompt 6 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 6 status"; exit 1; }
	@grep -q "Prompt 7 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 7 status"; exit 1; }
	@grep -q "Prompt 8 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 8 status"; exit 1; }
	@grep -q "Prompt 9 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 9 status"; exit 1; }
	@grep -q "Prompt 10 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 10 status"; exit 1; }
	@echo "docs-lint: policy engine, optimizer, substitution demo, Quickstart foundation, runtime foundation, Daml workflow skeleton, and command surface documentation are present"

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

status:
	@$(STATUS_SCRIPT)

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

demo-substitution: daml-build $(CHECK_JSONSCHEMA)
	@set -e; \
		. "$(RUNTIME_ENV)"; \
		output_path=$$($(PYTHON) app/orchestration/substitution_cli.py --manifest "$(SUBSTITUTION_DEMO_MANIFEST)" --output-dir "$(SUBSTITUTION_DEMO_OUTPUT_DIR)" --repo-root "$(REPO_ROOT)"); \
		$(CHECK_JSONSCHEMA) --schemafile $(SUBSTITUTION_REPORT_SCHEMA) "$$output_path"; \
		test -f "$(SUBSTITUTION_DEMO_OUTPUT_DIR)/substitution-demo-summary.md" || { echo "demo-substitution: missing markdown summary"; exit 1; }; \
		test -f "$(SUBSTITUTION_DEMO_OUTPUT_DIR)/substitution-demo-timeline.md" || { echo "demo-substitution: missing timeline markdown"; exit 1; }; \
		echo "demo-substitution: generated $$output_path"

verify:
	@$(VERIFY_SCRIPT)

clean-runtime:
	@rm -rf $(RUNTIME_DIR) .daml/dist .daml/package-database
