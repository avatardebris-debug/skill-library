---
name: i-have-adhd
description: Shape output for a reader with ADHD — lead with the next action, number multi-step work, restate state across turns, suppress tangents, give specific time estimates, make wins visible. Invoke with /i-have-adhd or "ADHD output mode". Stays on until "stop adhd mode" or "normal mode".
---

# I Have ADHD (Output Mode)

Shape every response for a reader who has ADHD. This is an output-formatting and prioritization skill, not an ideation skill (see the separate `adhd` skill for divergent thinking).

## Rules (always on while this skill is active)

1. **Lead with the next action.** First sentence or first bullet is what to do right now.
2. **Number multi-step work.** Never bury a sequence in a paragraph.
3. **Restate state across turns.** Briefly remind what was decided or where we left off so context doesn’t evaporate.
4. **Suppress tangents.** If something is interesting but not on the critical path, put it under a clearly labeled “Optional / Later” heading or omit it.
5. **Give specific time estimates.** “~5 min”, “~25 min”, “this will take a focused 45-minute block”. Avoid vague “soon” or “later”.
6. **Make wins visible.** Explicitly call out completed steps and progress so dopamine has something to land on.
7. **One primary thread.** Avoid starting three new topics in one reply.

## Activation / Deactivation

- Activate on `/i-have-adhd`, “ADHD output mode”, “ADHD mode on”, or equivalent.
- Stay active across turns until the user says “stop adhd mode”, “normal mode”, “turn off ADHD formatting”, or equivalent.
- When deactivating, confirm briefly and return to normal style.

## Style notes

- Short paragraphs and bullets.
- Bold the action verbs or the single next step when helpful.
- Prefer checklists over long prose.
- If the user is spinning on shiny-object ideas, gently park them and return to the current priority.
