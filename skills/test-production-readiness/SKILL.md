---
name: test-production-readiness
description: Meta skill that orchestrates smoke, conflict, analytics, exploratory, RCA, and maintainability evidence plus deployability, config isolation, rollback, and synthetic monitoring hooks. Emits a single go/no-go with evidence. Final gate before claiming production readiness inside software-factory or gauntlet.
metadata:
  short-description: Final production-readiness go/no-go with full dynamic evidence
  version: "1.0"
  argument-hint: "[scope] [--require-all]"
---

# Test Production Readiness

You are the **production-readiness gate**.

## Goal

Answer, with evidence: Is this safe to put in front of real users / real traffic?

## Instructions

1. Require or run the supporting skills and collect their artifacts:
   - test-smoke (must be PASS or explicit waiver)
   - instrument-analytics (schema + emission present)
   - test-exploratory (sessions run, crashes triaged)
   - rca-from-analytics (open high-severity items addressed or accepted)
   - test-conflict (shared-state risks understood)
   - test-maintainability (suite is not a liability)
   - test-strategy (recommended; required if user asked for a release bar)
   - acceptance-from-req when REQUIREMENTS.md exists (unbound load-bearing rows → CONDITIONAL)
   - On release-profile strategy or `--require-all` also collect
     test-performance, test-security, test-resilience, and field-test mechanical results
     (PENDING/SKIPPED with written waiver is allowed; silent omit is not)
2. Additionally check:
   - Deployability and environment/config isolation
   - Rollback or feature-flag safety story
   - Post-deploy synthetic monitoring or health-check hooks
   - Basic operational readiness (logs reachable, errors visible)
3. Emit a single verdict file `.factory/test/PRODUCTION-READINESS.md`:
   - GO / NO-GO / CONDITIONAL
   - Evidence links
   - Remaining risks and explicit acceptances
4. Do not flip any factory or gauntlet DONE flags yourself; supply the evidence for the orchestrator and critic.

## Rules

- Missing smoke or missing analytics is an automatic NO-GO unless the user explicitly waives with recorded rationale.
- Critical unrepaired crashes from exploratory are NO-GO.
- Prefer honest CONDITIONAL with a short punch-list over a soft GO.
