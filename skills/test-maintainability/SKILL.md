---
name: test-maintainability
description: Audit the health of the test suite itself — flakiness, speed, coverage of critical paths, clarity of invariants, duplication, and ease of extension. Use periodically or as a gauntlet critic requirement so the testing layer does not rot.
metadata:
  short-description: Test-suite health and maintainability audit
  version: "1.0"
---

# Test Maintainability

Audit the test suite so it remains a reliable, fast, and extensible safety net.

## Checklist

- Flakiness rate and known flake sources
- Wall-clock time of the critical-path suite
- Coverage of the main user journeys and negative paths
- Clarity of invariants being asserted
- Duplication and shared fixtures
- Ease of adding a new test for a new critical path
- Dependence on external services or brittle setup

## Output

Findings with severity, concrete examples, and recommended cleanups or structural changes.
