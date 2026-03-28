# Architecture Overview

## Purpose

The Canton Collateral Control Plane is a Canton-native collateral control plane. It is designed as reusable infrastructure for bilateral margining, tri-party collateral management, CCP-style control, treasury collateral mobility, and related secured-finance workflows.

The repository does not model a venue, a CCP, or a custodian. It models the control-plane capabilities those systems need in common:

- versioned collateral policy and schedules
- deterministic policy evaluation
- optimization under policy constraints
- atomic multi-party workflow execution on Canton
- machine-readable reporting and evidence
- reproducible demo and runtime infrastructure

## Design Goals

- keep policy, optimization, workflow, reporting, and runtime concerns separate
- make deterministic decisions reproducible from explicit inputs
- keep Canton ledger state authoritative for workflow and encumbrance transitions
- preserve least-privilege visibility for each participant and operator role
- support later integration with token-standard-style assets and other Canton applications
- allow the prototype to run on a Quickstart-based LocalNet without a hard fork of upstream components

## Control Plane Vs Data Plane

| Plane | Responsibilities | Representative Surfaces |
| --- | --- | --- |
| Control plane | define policy, evaluate eligibility, compute haircuts and lendable value, enforce concentration and release logic, optimize collateral choices, orchestrate substitutions, and emit conformance and reporting outputs | `CPL`, policy engine, optimization engine, workflow library, conformance suite, reporting and evidence layer |
| Data plane | hold or move collateral facts and committed execution state without becoming the source of policy semantics | token-standard-style assets, Daml Finance-style assets, Canton ledger state and contract instances, settlement and DvP rails, Quickstart or LocalNet runtime environment |

The workflow library is part of the control plane, but the committed ledger state and contract instances it produces belong to the data plane. This split keeps control semantics, execution authority, and runtime hosting concerns explicit.

## Control-Plane Boundaries

| Boundary | Owns | Primary Inputs | Primary Outputs | Explicitly Does Not Own |
| --- | --- | --- | --- | --- |
| Collateral Policy Language and schedules | versioned eligibility, haircut, concentration, control, substitution-right, and settlement-window rules | policy authoring inputs, profile templates | policy package and effective schedule set | live inventory, workflow state, settlement execution |
| Policy evaluation engine | deterministic eligibility, lendable value, concentration checks, release checks, and decision traces | policy package, asset facts, valuation snapshot, encumbrance state, obligation context | policy decision report | optimization objectives, workflow approvals, report publishing |
| Optimization engine | candidate selection, cheapest-to-deliver or best-to-post proposals, substitution recommendations, explanation traces | policy decision report, inventory state, objective settings, operational constraints | optimization proposal | authoritative eligibility rules, ledger state mutation, settlement |
| Workflow library and orchestration | obligations, encumbrance transitions, substitution, return, approvals, settlement instructions, exception handling | approved business actions, policy references, optimization proposal references, party approvals | committed Canton workflow state and settlement instructions | policy authoring, optimization tuning, report editing |
| Reporting and evidence generation | state-derived execution reports, audit views, traceability records, prompt execution evidence | committed workflow state, policy decision reports, valuation snapshot metadata, command logs | machine-readable execution report, evidence manifest links | authoritative decision making, hidden side effects |
| Demo and runtime infrastructure | LocalNet topology, package deployment, service wiring, observability, demo bootstrap | pinned Quickstart base, overlay config, package builds, service images | runnable environment | business rules, optimization logic, report semantics |

## Authoritative Sources Of Truth

| Fact | Authoritative Source |
| --- | --- |
| policy rules and schedules | versioned policy package in the policy registry |
| reference prices and FX rates used in a decision | immutable valuation snapshot |
| obligation, encumbrance, approval, and settlement state | committed Daml contracts on Canton |
| why an asset was eligible or rejected | policy decision report tied to a policy version and snapshot |
| why a candidate set was proposed | optimization proposal tied to deterministic inputs |
| what actually executed | execution report derived from committed workflow state |
| how the prototype was started or verified | worklog and evidence execution reports |

## Reference Architecture

1. Policy authors publish reusable policy packages and schedule versions.
2. A valuation or inventory event produces an immutable valuation snapshot and current collateral facts.
3. The policy evaluation engine determines eligibility, lendable value, concentration headroom, and release constraints.
4. The optimization engine proposes candidate lots only after policy feasibility has been established.
5. The workflow library commits call obligations, postings, substitutions, returns, and exceptions atomically into Canton ledger state.
6. Reporting services derive execution reports and evidence from committed state, not from pre-commit simulations.
7. Demo and runtime infrastructure host the preceding components without changing their semantics.

## Architectural Principles

- A policy package is portable across workflows; it is not embedded inside a single Daml template.
- An optimization proposal is advisory until a workflow contract commits it.
- Workflow contracts may reference policy and optimization outputs, but they do not rewrite them.
- Reports and evidence are downstream products; they never become hidden inputs to execution.
- Demo overlays may add parties, packages, and services, but they may not introduce demo-only shortcuts in the control path.

## Out Of Scope For This Phase

- live integrations with custodians, CCPs, or central-bank infrastructure
- legal document management or agreement negotiation
- quantitative model calibration beyond documented schedule structure
- user interfaces or operational dashboards
- production hardening, resiliency tuning, or multi-region deployment
