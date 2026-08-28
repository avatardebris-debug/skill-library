---
name: acceptance-from-req
description: Turn REQUIREMENTS.md rows into executable acceptance cases with Given/When/Then, falsifiers, and an owning test skill. Use when /acceptance-from-req, write acceptance criteria, BDD from requirements, definition of done, or bind req rows to field-test P-tasks. Does not mark requirements done. Does not claim field_proven.
metadata:
  short-description: Requirements to executable acceptance cases
  version: "1.0"
  argument-hint: "[REQUIREMENTS.md path]"
---

# Acceptance from Req

You bind `/req` inventory to checks other skills can run.

## When to use

- After `/req` or when REQUIREMENTS.md exists but field-test P* tasks are generic
- User wants acceptance criteria, BDD, Given/When/Then, falsifiers
- Production-readiness asks "which requirements were actually checked"

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Invent the requirement list | `req` |
| Rank what to test | `test-strategy` |
| Run the cases | `test-smoke`, `field-test`, or listed owner |
| Factory API freeze | `qc-contracts` |

## Inputs

- `REQUIREMENTS.md` (default) or user path
- AIM / IDEA / TARGET for journey names
- Existing `.factory/test/STRATEGY.md` if present

## Procedure

1. Read every requirement row (id, statement, kind, falsifier, load-bearing).
2. Skip rows already marked dropped / waived with recorded rationale.
3. For each keep/challenge row write one acceptance case:
   - `AC-<req-id>`
   - Given / When / Then
   - Falsifier (what observation proves it false)
   - Owner skill (`test-smoke`, `field-test`, `test-security`, …)
   - Evidence path to write
4. Load-bearing / human-floor kinds (safety, honesty, mission core) cannot be "owner = none".
5. Write `.factory/test/ACCEPTANCE.md` plus optional `acceptance.json` list.
6. If `phases/ship/field_tests.md` exists or user asks, propose P*/I* lines that map 1:1 to load-bearing ACs. Do not overwrite a field plan without saying so.

## ACCEPTANCE.md contract

```markdown
# Acceptance cases
Source: REQUIREMENTS.md

| AC | Req | Given | When | Then | Falsifier | Owner | Evidence |
|----|-----|-------|------|------|-----------|-------|----------|

## Unbound load-bearing
- REQ-… — why unbound, what skill should own it

## Non-claims
- Written AC ≠ passing AC
- Passing owner skill ≠ field_proven
```

## Rules

- One primary AC per requirement. Extra cases only for distinct falsifiers.
- Then-clauses must be observable (exit code, body key, log event, UI text, metric).
- Do not convert aspirations into ACs ("users love it").
- Do not mark REQUIREMENTS.md status done.

## Related

- Upstream `req`
- Downstream `field-test`, `test-smoke`, `test-production-readiness`
- Strategy may drop non-load-bearing ACs from the run sequence
