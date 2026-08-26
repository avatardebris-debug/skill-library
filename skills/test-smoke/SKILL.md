---
name: test-smoke
description: Generate and run a minimal critical-path smoke suite that proves the main flows work end-to-end. Covers intended happy paths plus a few key negative paths. Use after merges, before votes or gauntlet phase advance, or when asked for smoke tests. Writes pass/fail plus artifacts under .factory/test/smoke/.
metadata:
  short-description: Critical-path smoke suite for end-to-end flow verification
  version: "1.0"
---

# Test Smoke

Minimal, fast, critical-path suite that proves the main flows still work.

## Scope

- Happy-path end-to-end for the primary user journeys
- A few key negative / error paths
- Avoid exhaustive coverage; that belongs to other test skills

## Process

1. Identify the 3–7 critical paths.
2. Generate or update the smoke tests.
3. Run them.
4. Write pass/fail results and any artifacts under `.factory/test/smoke/`.
5. Surface a clear green / red signal.

## Guards

- Keep the suite fast (target under a few minutes).
- Prefer deterministic setup over heavy external dependencies.
- Fail loudly and with actionable messages.
