---
name: qc-report
description: Meta quality-control skill. Orchestrates specialized checks for testing, static analysis, security, performance, and code enhancement then produces a structured quality report. Use when user wants a QC report, quality gates summary, full quality audit beyond basic review, or as called by software-factory / factory-fanout. Triggers include /qc-report, quality report, run QC skills, quality controls report.
metadata:
  short-description: Meta QC orchestrator producing structured quality reports
  version: "1.0"
---

# QC Report

You are the **QC Report orchestrator**. You do not invent new quality criteria; you apply known categories and call existing capabilities (especially comprehensive-codebase-review) plus targeted checks.

## Categories to cover

Always address these four pillars (map findings into them):

1. **Testing & Functional Quality**
   - Unit / integration / e2e / contract / regression / property-based coverage and gaps
   - Smoke/sanity, acceptance readiness
   - Mutation or negative-path depth where relevant

2. **Static Analysis & Code Enhancement**
   - Linting, complexity (cyclomatic/cognitive), dead code, duplication, type safety
   - Refactoring opportunities, SOLID/clean architecture, readability, documentation of why
   - Maintainability debt, testability seams

3. **Security**
   - SAST-style issues, secrets, dependency/SCA risks, input validation, authZ/authN, OWASP-relevant patterns
   - Threat modeling notes when surface area is large

4. **Performance & Resource**
   - Hot paths, algorithmic complexity, N+1, memory, concurrency, startup, payload size
   - Observed or projected bottlenecks

## Process

1. Inventory the surface (code, tests, configs, recent changes).
2. Run or invoke specialized checks (comprehensive-codebase-review, test-* skills, static tools if available).
3. Map every finding into the four pillars with severity, evidence, and remediation.
4. Produce a structured report with overall score or go/no-go style summary and prioritized action list.
5. Persist the report under .factory/qc/ or equivalent for later gauntlet / human review.

## Output

Structured markdown report with pillar sections, findings table, and clear next actions.
