---
name: elon
description: >-
  Orchestrate Elon-style engineering: make requirements less dumb (/req),
  delete (/zero), simplify/map (/zero2, optional zero-cross), human add-back
  (/restore), then accelerate via clone or gap-to-plan/LFG/gauntlet, optional
  factory-qc and comprehensive-codebase-review bookends, automate last. Playlist
  of existing skills — no live delete, no auto-LFG. Use when /elon, Elon 5-step,
  delete-then-restore loop, or full compress+reconstruct cycle.
---

# Elon

Orchestrate the classic five-step engineering loop using the existing skill playlist. This skill does not invent new process; it sequences and gates the others.

## The five steps (in order)

1. **Make the requirements less dumb** → run `/req` (or the req skill).
2. **Delete** → run `/zero` (zero-based redesign). Conceptual only — never live delete code.
3. **Simplify / map** → run `/zero2` (and optionally zero-cross).
4. **Accelerate** → human add-back of the essential pieces, then clone existing high-quality solutions or run gap-to-plan → LFG / gauntlet.
5. **Automate** last.

Optional bookends: factory-qc or comprehensive-codebase-review before and after.

## Rules

- This is a **playlist / orchestrator**, not a live mutator.
- Never perform live deletes or in-place rewrites of production code from this skill.
- Always keep the human in the loop for the restore / add-back step.
- Prefer existing skills (req, zero, zero2, gap-to-plan, lfg, universal-gauntlet, software-factory) over inventing new process.
- Surface clear decision points and the current step status.

## Typical invocation

User says `/elon` or “run the Elon loop on X”.
You walk the five steps, calling the appropriate skill at each stage and recording state under `.factory/elon/` or equivalent.
