SHELL := /bin/sh

REQUIRED_DOCS := \
	README.md \
	AGENTS.md \
	CONTRIBUTING.md \
	SECURITY.md \
	CODEOWNERS \
	.gitignore \
	Makefile \
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
	docs/invariants/INVARIANT_REGISTRY.md \
	docs/risks/RISK_REGISTER.md \
	docs/evidence/EVIDENCE_MANIFEST.md \
	docs/evidence/prompt-01-execution-report.md \
	docs/evidence/prompt-02-execution-report.md \
	docs/runbooks/README.md \
	docs/integration/INTEGRATION_SURFACES.md \
	docs/integration/QUICKSTART_INTEGRATION_PLAN.md \
	docs/integration/TOKEN_STANDARD_ALIGNMENT.md \
	docs/domain/GLOSSARY.md \
	docs/domain/COLLATERAL_DOMAIN_MODEL.md \
	docs/domain/ACTORS_AND_ROLES.md \
	docs/domain/LIFECYCLE_STATES.md \
	docs/testing/TEST_STRATEGY.md \
	docs/security/THREAT_MODEL.md \
	docs/change-control/CHANGE_CONTROL.md

.PHONY: docs-lint status verify

docs-lint:
	@for file in $(REQUIRED_DOCS); do \
		test -f "$$file" || { echo "docs-lint: missing $$file"; exit 1; }; \
	done
	@grep -q "C-COPE" README.md || { echo "docs-lint: README missing C-COPE framing"; exit 1; }
	@grep -q "^Current Phase:" docs/mission-control/MASTER_TRACKER.md || { echo "docs-lint: tracker missing Current Phase"; exit 1; }
	@grep -qi "Control-Plane Boundaries" docs/architecture/OVERVIEW.md || { echo "docs-lint: architecture overview missing boundary section"; exit 1; }
	@grep -qi "policy evaluation engine" docs/architecture/COMPONENTS.md || { echo "docs-lint: component model missing policy evaluation engine"; exit 1; }
	@grep -qi "Privacy Objective" docs/architecture/PRIVACY_MODEL.md || { echo "docs-lint: privacy model incomplete"; exit 1; }
	@grep -qi "authorization and role control" docs/invariants/INVARIANT_REGISTRY.md || { echo "docs-lint: invariant taxonomy incomplete"; exit 1; }
	@grep -qi "concentration-limit enforcement" docs/invariants/INVARIANT_REGISTRY.md || { echo "docs-lint: proposal-aligned invariants incomplete"; exit 1; }
	@grep -qi "CollateralAsset" docs/domain/COLLATERAL_DOMAIN_MODEL.md || { echo "docs-lint: domain model incomplete"; exit 1; }
	@grep -qi "margin call issuance" docs/domain/LIFECYCLE_STATES.md || { echo "docs-lint: lifecycle states incomplete"; exit 1; }
	@grep -qi "security review" docs/evidence/EVIDENCE_MANIFEST.md || { echo "docs-lint: evidence categories incomplete"; exit 1; }
	@grep -qi "Quickstart-based LocalNet" docs/integration/QUICKSTART_INTEGRATION_PLAN.md || { echo "docs-lint: quickstart integration plan incomplete"; exit 1; }
	@grep -qi "token-standard-style" docs/integration/TOKEN_STANDARD_ALIGNMENT.md || { echo "docs-lint: token alignment incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-01-execution-report.md || { echo "docs-lint: prompt execution report incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-02-execution-report.md || { echo "docs-lint: prompt 2 execution report incomplete"; exit 1; }
	@echo "docs-lint: required documentation files and key sections are present"

status:
	@echo "Mission-control status"
	@grep -m 1 "^Current Phase:" docs/mission-control/MASTER_TRACKER.md
	@echo
	@git status --short --branch

verify: docs-lint
	@! rg --files -g '*.py' -g '*.ts' -g '*.tsx' -g '*.js' -g '*.jsx' -g '*.go' -g '*.rs' -g '*.java' -g '*.kt' -g '*.daml' >/dev/null || { echo "verify: unexpected implementation files present"; exit 1; }
	@echo "verify: documentation-only baseline checks passed"
