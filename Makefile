SHELL := /bin/sh
PYTHON ?= python3
REPO_ROOT := $(CURDIR)
RUNTIME_DIR := .runtime
RUNTIME_ENV := $(RUNTIME_DIR)/env.sh
BOOTSTRAP_SCRIPT := scripts/bootstrap.sh
STATUS_SCRIPT := scripts/dev-status.sh
VERIFY_SCRIPT := scripts/verify.sh

include scripts/toolchain.env

VENV := .venv
CHECK_JSONSCHEMA := $(VENV)/bin/check-jsonschema
CPL_SCHEMA := schema/cpl.schema.json
POLICY_EVAL_REPORT_SCHEMA := reports/schemas/policy-evaluation-report.schema.json
POLICY ?= examples/policies/central-bank-style-policy.json
INVENTORY ?= examples/inventory/central-bank-eligible-inventory.json
REPORT ?=
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
	reports/README.md \
	reports/schemas/policy-evaluation-report.schema.json \
	test/README.md \
	test/policy-engine/test_policy_engine.py \
	examples/README.md \
	examples/inventory/central-bank-eligible-inventory.json \
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
	docs/runbooks/README.md \
	docs/integration/INTEGRATION_SURFACES.md \
	docs/integration/QUICKSTART_INTEGRATION_PLAN.md \
	docs/integration/TOKEN_STANDARD_ALIGNMENT.md \
	docs/domain/GLOSSARY.md \
	docs/domain/COLLATERAL_DOMAIN_MODEL.md \
	docs/domain/ACTORS_AND_ROLES.md \
	docs/domain/LIFECYCLE_STATES.md \
	docs/domain/DAML_MAPPING.md \
	docs/specs/CPL_SPEC_v0_1.md \
	docs/specs/CPL_EXAMPLES.md \
	docs/specs/POLICY_EVALUATION_REPORT_SPEC.md \
	docs/testing/CPL_VALIDATION_TEST_PLAN.md \
	docs/testing/DAML_TEST_PLAN.md \
	docs/testing/POLICY_ENGINE_TEST_PLAN.md \
	docs/testing/TEST_STRATEGY.md \
	docs/security/THREAT_MODEL.md \
	docs/change-control/CHANGE_CONTROL.md \
	$(CPL_SCHEMA) \
	$(POLICY_EVAL_REPORT_SCHEMA) \
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

.PHONY: bootstrap docs-lint status verify validate-cpl policy-eval test-policy-engine daml-build daml-test demo-run clean-runtime

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
	@for script in $(BOOTSTRAP_SCRIPT) $(STATUS_SCRIPT) $(VERIFY_SCRIPT); do \
		test -x "$$script" || { echo "docs-lint: expected executable $$script"; exit 1; }; \
	done
	@grep -q "^sdk-version: $(DAML_SDK_VERSION)$$" daml.yaml || { echo "docs-lint: daml.yaml sdk-version mismatch"; exit 1; }
	@grep -q "^python $(PYTHON_TOOL_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned python"; exit 1; }
	@grep -q "^java temurin-$(JAVA_VERSION)$$" .tool-versions || { echo "docs-lint: .tool-versions missing pinned java"; exit 1; }
	@grep -q "make bootstrap" README.md || { echo "docs-lint: README missing bootstrap command"; exit 1; }
	@grep -q "make daml-build" README.md || { echo "docs-lint: README missing daml-build command"; exit 1; }
	@grep -q "make daml-test" README.md || { echo "docs-lint: README missing daml-test command"; exit 1; }
	@grep -q "make demo-run" README.md || { echo "docs-lint: README missing demo-run command"; exit 1; }
	@grep -q "make policy-eval" README.md || { echo "docs-lint: README missing policy-eval command"; exit 1; }
	@grep -q "make test-policy-engine" README.md || { echo "docs-lint: README missing test-policy-engine command"; exit 1; }
	@grep -q "make daml-test" AGENTS.md || { echo "docs-lint: AGENTS missing daml-test command"; exit 1; }
	@grep -q "make policy-eval" AGENTS.md || { echo "docs-lint: AGENTS missing policy-eval command"; exit 1; }
	@grep -q "make test-policy-engine" AGENTS.md || { echo "docs-lint: AGENTS missing test-policy-engine command"; exit 1; }
	@grep -q "make daml-test" CONTRIBUTING.md || { echo "docs-lint: CONTRIBUTING missing daml-test command"; exit 1; }
	@grep -q "workflowSmokeTest" daml.yaml || { echo "docs-lint: daml.yaml missing workflow smoke init script"; exit 1; }
	@grep -q "Daml SDK $(DAML_SDK_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Daml SDK pin"; exit 1; }
	@grep -q "Temurin JDK $(JAVA_VERSION)" docs/setup/DEPENDENCY_POLICY.md || { echo "docs-lint: dependency policy missing Java pin"; exit 1; }
	@grep -q "make daml-test" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing daml-test"; exit 1; }
	@grep -q "make policy-eval" docs/setup/LOCAL_DEV_SETUP.md || { echo "docs-lint: local setup missing policy-eval"; exit 1; }
	@grep -q "make demo-run" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing demo-run"; exit 1; }
	@grep -q "make daml-test" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing daml-test"; exit 1; }
	@grep -q "make test-policy-engine" docs/testing/TEST_STRATEGY.md || { echo "docs-lint: test strategy missing test-policy-engine"; exit 1; }
	@grep -q "ADR 0006" docs/adrs/0006-runtime-foundation.md || { echo "docs-lint: ADR 0006 missing title"; exit 1; }
	@grep -q "ADR 0007" docs/adrs/0007-daml-contract-boundaries.md || { echo "docs-lint: ADR 0007 missing title"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-04-execution-report.md || { echo "docs-lint: prompt 4 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-05-execution-report.md || { echo "docs-lint: prompt 5 execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-06-execution-report.md || { echo "docs-lint: prompt 6 execution report incomplete"; exit 1; }
	@grep -q "Prompt 5 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 5 status"; exit 1; }
	@grep -q "Prompt 6 status" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing prompt 6 status"; exit 1; }
	@echo "docs-lint: policy engine, runtime foundation, Daml workflow skeleton, and command surface documentation are present"

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

test-policy-engine: $(CHECK_JSONSCHEMA)
	@PYTHONPATH=app/policy-engine $(PYTHON) -m unittest discover -s test/policy-engine -p 'test_*.py'
	@$(MAKE) --no-print-directory policy-eval POLICY=examples/policies/central-bank-style-policy.json INVENTORY=examples/inventory/central-bank-eligible-inventory.json REPORT=reports/generated/central-bank-domestic-window-policy-central-bank-eligible-set-policy-evaluation-report.json
	@echo "test-policy-engine: deterministic policy-engine tests and report validation passed"

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

verify:
	@$(VERIFY_SCRIPT)

clean-runtime:
	@rm -rf $(RUNTIME_DIR) .daml/dist .daml/package-database
