---
name: adhd
description: Parallel divergent ideation that forces lateral and fluid thinking. Spawns isolated branches under different cognitive frames (regulator, biology, speedrunner, 10-year-old, $0 budget), scores, clusters, prunes traps, and deepens top survivors. Use on /adhd, ADHD mode, brainstorm/ideate intents, or open-ended design, architecture, naming, API/SDK surface, and fuzzy-debugging decisions. Skip for syntax, lookups, bugs with known root cause, or closed phrasing (quick, standard, canonical, textbook).
license: MIT
metadata:
  source: https://github.com/UditAkhourii/adhd
  version: "0.1"
---

# ADHD

Stop picking the textbook answer. The first three answers the model would give are the answers a senior engineer would give in thirty seconds. Correct. Forgettable. The interesting answers live past number three, in the awkward middle nobody walks into. This skill makes the model walk there.

## Pre-flight (run before Phase 1)

This skill is expensive (multiple reasoning passes). Do not pay that cost when a direct answer is better. Run this gate before Phase 1.

**Step 1. Explicit invocation check.**

If the user typed `/adhd` or explicitly asked for ADHD mode, "use the adhd skill", or "run ADHD on this", **SKIP the rest of this section and go straight to Phase 1**. The user opted in. Do not second-guess.
