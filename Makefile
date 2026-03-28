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
	docs/adrs/README.md \
	docs/adrs/0001-repo-principles.md \
	docs/adrs/0002-c-cope-solution-shape.md \
	docs/invariants/INVARIANT_REGISTRY.md \
	docs/risks/RISK_REGISTER.md \
	docs/evidence/EVIDENCE_MANIFEST.md \
	docs/evidence/prompt-01-execution-report.md \
	docs/runbooks/README.md \
	docs/integration/INTEGRATION_SURFACES.md \
	docs/domain/GLOSSARY.md \
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
	@grep -qi "authorization and role control" docs/invariants/INVARIANT_REGISTRY.md || { echo "docs-lint: invariant taxonomy incomplete"; exit 1; }
	@grep -qi "concentration-limit enforcement" docs/invariants/INVARIANT_REGISTRY.md || { echo "docs-lint: proposal-aligned invariants incomplete"; exit 1; }
	@grep -qi "security review" docs/evidence/EVIDENCE_MANIFEST.md || { echo "docs-lint: evidence categories incomplete"; exit 1; }
	@grep -q "^## Results" docs/evidence/prompt-01-execution-report.md || { echo "docs-lint: prompt execution report incomplete"; exit 1; }
	@echo "docs-lint: required documentation files and key sections are present"

status:
	@echo "Mission-control status"
	@grep -m 1 "^Current Phase:" docs/mission-control/MASTER_TRACKER.md
	@echo
	@git status --short --branch

verify: docs-lint
	@! rg --files -g '*.py' -g '*.ts' -g '*.tsx' -g '*.js' -g '*.jsx' -g '*.go' -g '*.rs' -g '*.java' -g '*.kt' -g '*.daml' >/dev/null || { echo "verify: unexpected implementation files present"; exit 1; }
	@echo "verify: documentation-only baseline checks passed"
