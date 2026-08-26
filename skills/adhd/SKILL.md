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

**Step 2. Self-judge (only if Step 1 did not match).**

Ask yourself three questions. If the answer to any is no, ABORT.

1. **Open-ended?** Would a senior engineer give multiple viable answers here, or is there one canonical answer? If canonical, abort.
2. **High-stakes?** Is the cost of the obvious answer being wrong actually high? Architecture decisions, public API surfaces, naming a real product, fuzzy bugs with no known root cause, schema design = yes. Side project at 11pm = no.
3. **Open phrasing?** Did the user avoid words like "quick", "standard", "canonical", "textbook", "just", "one-line"? If they used any of those, they want the direct answer.

If any answer is no → respond with the normal direct answer and do not enter the ADHD process.

## Phase 1 — Spawn isolated branches

Create five (or more) independent reasoning branches. Each branch uses a different cognitive frame. Do not let the branches see each other yet.

Frames (use these or close variants):

1. **Regulator / safety** — what would a careful compliance or risk officer insist on?
2. **Biology / evolution** — what would natural selection or a living system do?
3. **Speedrunner** — what is the absolute minimum viable path that still works?
4. **10-year-old** — how would a smart, unconstrained child solve or name this?
5. **$0 budget** — what if money, headcount, and existing infrastructure were zero?

Additional useful frames when relevant: alien anthropologist, future historian, adversarial red-team, extreme user, etc.

Each branch produces 1–3 candidate ideas / approaches. Keep them short and concrete.

## Phase 2 — Score and cluster

Bring the candidates together. Score each on:

- Novelty (how far from the textbook answer)
- Plausibility / physics / engineering realism
- Leverage (how much it changes the outcome if true)
- Cost / risk

Cluster similar ideas. Prune obvious traps (ideas that only sound clever).

## Phase 3 — Deepen the survivors

Take the top 2–4 surviving ideas and deepen them: mechanisms, failure modes, first experiments, naming implications, API surface consequences, etc.

## Phase 4 — Present

Return the deepened survivors ranked, with a short note on why each survived. Do not force a single winner unless the user asks for one. Make the interesting middle visible.

## Rules

- Never skip the pre-flight unless the user explicitly invoked the skill.
- Prefer surprising but grounded ideas over pure fantasy.
- If every branch converges on the same answer, that is itself useful signal — report it.
