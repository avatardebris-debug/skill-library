---
name: test-production-readiness
description: Meta skill that orchestrates smoke, conflict, analytics, exploratory, RCA, and maintainability evidence plus deployability, config isolation, rollback, and synthetic monitoring hooks. Emits a single go/no-go with evidence. Final gate before claiming production readiness inside software-factory or gauntlet.
metadata:
  short-description: Final production-readiness go/no-go with full dynamic evidence
  version: "1.0"
---

# Test Production Readiness

Final gate that aggregates evidence from the other test skills and operational concerns into a single go / no-go decision.

## Evidence sources

- test-smoke
- test-conflict
- instrument-analytics + rca-from-analytics
- test-exploratory
- test-maintainability
- Deployability, config isolation, rollback procedure, synthetic monitoring hooks

## Process

1. Collect or trigger the required evidence.
2. Score each area (pass / partial / fail).
3. Identify any blocking issues.
4. Emit a clear go / no-go with the supporting artifact links.

## Output

Single verdict + evidence summary. No-go must list the concrete blockers.
