---
name: test-exploratory
description: Run exploratory and adversarial sessions against the product using potential critical journeys expanded by a behaviorally-weighted synthetic distribution of human actions, then adversarial pressure. Finds crashes and soft failures before real users exist. Logs structured sessions for RCA. Use after smoke is green and analytics are present.
metadata:
  short-description: Potential journeys + synthetic human-like actions + adversarial crash hunting
  version: "1.0"
---

# Test Exploratory

Discover crashes and soft failures through realistic + adversarial exploration before real users arrive.

## Core approach

1. Start from the canonical potential journeys defined by the product / IDEA / TARGET / product vision (the intended critical paths).
2. Expand them into sessions using a **behaviorally-weighted synthetic distribution** of human actions drawn from the model’s approximate statistical understanding of real interaction patterns (hesitation, backtracking, partial completion, wrong order, impatience, curiosity, error-recovery attempts, accessibility-style navigation, etc.). This is not pure randomness and not only the happy path.
3. Apply controlled **adversarial pressure** on top (rapid inputs, malformed data, network/resource stress, concurrent sessions, boundary values) so the tail of the distribution is also exercised.
4. Log every session with enough structure that `rca-from-analytics` can group failures by journey + deviation type.

## Instructions

1. Load or derive the canonical potential journeys (prefer output from `test-smoke` or factory artifacts).
2. Confirm analytics instrumentation is present (call or require `instrument-analytics` if missing).
3. Generate a session plan:
   - Majority of sessions = realistic variations around the canonical journeys (behaviorally weighted).
   - Minority (default ~15–25%) = adversarial / low-probability / hostile actions.
4. Execute sessions in the appropriate surface (browser, simulator, API driver, CLI, device farm, or scripted UI). Prefer real runnable surfaces over pure mocks when available.
5. For each session record:
   - Journey ID and deviation class
   - Sequence of actions
   - Outcome (success, soft failure, crash, hang, unexpected state)
   - Telemetry / logs / screenshots / traces captured
6. Write results under `.factory/test/exploratory/`:
   - `SESSIONS.md` — summary table + links to per-session artifacts
   - `CRASHES.md` — reproducible failure cases with minimal steps to reproduce
   - Raw logs and media
7. Hand high-signal failures to `rca-from-analytics` (or produce initial root-cause hypotheses if RCA skill is not yet run).
8. After a fix, the exact failing scenario should be promoted into the automated regression / smoke suite.

## Rules

- Prefer high-likelihood human deviations over uniform random walks.
- Still deliberately sample the tail; do not only test the mode of the distribution.
- Every crash or soft failure must have a minimal reproducible sequence.
- Do not claim “no issues found” without stating how many sessions and what distribution was used.
- Keep the skill focused on discovery; permanent automation of the found cases belongs elsewhere.
