---
name: comprehensive-codebase-review
description: >-
  Full-repository proactive audit for functional/logical bugs, security issues,
  performance anti-patterns, maintainability debt, and architectural flaws.
  Evidence-backed findings with severity, file/line, and remediation. Use when
  the user asks for whole-codebase review, find all bugs, code quality audit,
  technical debt assessment, pre-release health check, onboarding audit, or runs
  /comprehensive-codebase-review. Do NOT use for a single known bug (use
  systematic-debugging or pipeline-bug-investigate), session verify+fix
  (/check-work), maintainability of a diff only (/code-review), or production
  stack traces (Sentry).
---

# Comprehensive Codebase Review

Proactive, whole-repository audit. Surface real problems with evidence, not style nits.

## Scope

- Functional / logical bugs
- Security issues
- Performance anti-patterns
- Maintainability debt
- Architectural flaws

## Process

1. Inventory the repository structure, entry points, critical paths, and recent changes.
2. Walk the code systematically (or sample high-risk areas if the repo is enormous).
3. For every finding record:
   - Severity (blocker / high / medium / low)
   - File and line (or clear location)
   - Concrete evidence (snippet, data flow, missing check, etc.)
   - Recommended remediation
4. Group findings by category and prioritize.
5. Produce a durable report (markdown under `.factory/review/` or similar) that a human or gauntlet can act on.

## Rules

- Prefer evidence over speculation.
- Do not turn this into a style or lint dump unless the style issue is a real maintainability or correctness problem.
- If the repo is too large for a complete pass in one go, say so and deliver a high-value partial audit with a clear plan for the remainder.
- Never claim “no issues found” without stating the coverage of the review.
