# Quickstart Integration Plan

## Objective

Use an upstream Quickstart-based LocalNet as the prototype's Canton runtime while keeping Control-Plane-specific topology, packages, and services in overlays or adjacent services. Quickstart and LocalNet remain data-plane execution surfaces; the policy, optimization, workflow, and reporting subsystems remain part of the Control Plane. The goal is to maximize compatibility with the Quickstart ecosystem and minimize long-lived forks.

## Current Pinned Runtime Foundation

The repository now pins the first executable foundation around:

- Daml SDK `2.10.4`
- Canton open-source `2.10.4`
- Temurin JDK `17.0.18+8`

These versions support local package compilation and a minimal Daml smoke scenario today. Quickstart overlay wiring remains a follow-on task.

## Integration Principles

- start from a pinned upstream Quickstart release
- express Control-Plane-specific participants, parties, package deployment, and service wiring through overlays first
- run policy, valuation, optimization, reporting, and integration services adjacent to Canton, not inside patched Quickstart internals
- fork upstream only when an extension point is missing and the gap is documented through an ADR
- keep the prototype topology reproducible from repo-controlled configuration

## Proposed LocalNet Shape

| Layer | Planned Content |
| --- | --- |
| upstream base | domain, sequencer, mediator, baseline participant setup, developer tooling |
| Control Plane overlay | participant and party additions for pledgor, secured party, and custodian roles; package deployment config; bootstrap data hooks |
| adjacent services | policy registry, valuation service, optimization service, reporting service, integration gateway |
| scenario tools | reproducible commands for seed data, workflow execution, and report validation |

## Recommended Delivery Strategy

### Step 1: Pin the base

- select and pin the Quickstart release that will anchor LocalNet development
- use the already pinned Daml SDK and Canton `2.10.4` foundation as the compatibility floor
- record image or package versions in a dedicated dependency ADR before workflow code starts

### Step 2: Add overlays, not forks

- define overlay configuration for extra parties, participants, package deployment, and service endpoints
- keep base Quickstart files untouched where override or composition mechanisms exist
- isolate repo-specific topology under a Control-Plane-owned overlay directory once implementation begins

### Step 3: Deploy Control Plane Daml packages on top

- treat the Control Plane workflow package as an application deployed into the LocalNet, not as a modification to Quickstart core services
- keep obligation, encumbrance, settlement, and approval templates in the Control Plane package boundary

### Step 4: Attach adjacent services

- policy registry serves versioned policy packages to the workflow orchestrator and reporter
- valuation service produces immutable snapshots consumed by policy evaluation and reports
- optimization service ranks feasible collateral without becoming the source of truth
- reporting service subscribes to committed workflow state and emits execution reports

### Step 5: Validate with conformance scenarios

- use scenario runners against the LocalNet deployment
- confirm that overlays do not change control semantics compared with the documented architecture
- capture prompt and scenario execution reports as evidence

## When A Fork Is Acceptable

A Quickstart fork is acceptable only if all of the following are true:

1. the needed topology or integration point cannot be expressed with an overlay or adjacent service
2. the missing extension point blocks an implementation milestone
3. the fork scope is minimal and documented
4. an ADR records why the fork exists and how to retire it later

## Planned Boundaries For The Prototype

| Concern | Preferred Placement | Reason |
| --- | --- | --- |
| multi-party workflow execution | Quickstart LocalNet plus deployed Control Plane workflow package | keeps authoritative workflow state on Canton |
| policy versioning | adjacent policy registry | avoids coupling policy lifecycle to package deployment |
| optimization | adjacent service | keeps objective tuning out of workflow contracts |
| reporting | adjacent service | allows role-specific report profiles and re-generation from state |
| demo bootstrap | overlay scripts and config | keeps environment logic separate from business semantics |

## Simplifications In Early Prototype Phases

- LocalNet may run all services on one machine while still preserving logical role separation
- bootstrap data may use synthetic counterparties and assets, but only through documented seed inputs
- early settlement adapters may stop at instruction emission rather than real external asset movement
- observability may be local-only before shared demo infrastructure exists

## Exit Criteria For Moving Beyond Planning

- Quickstart version pinned
- Daml SDK and Canton baseline pinned for local compilation
- overlay strategy documented in repo-controlled config
- Daml package boundary defined
- adjacent service contracts defined for policy, valuation, optimization, and reporting
- at least one reproducible LocalNet scenario planned end to end
