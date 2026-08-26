---
name: lfg
description: Full outer ship loop from an aim: deep-research -> gap-to-plan -> ship ALL gap plans via planner + universal-gauntlet (medium critic) plan-by-plan and phase-by-phase -> comprehensive-codebase-review -> /implement Medium+ fixes -> remeasure gap-to-plan -> prompt /encore. Universal across codebases with a project adapter. Use when the user runs /lfg, /LFG, "let's fucking go", "full aim cycle", "research then gauntlet then review", or wants the complete research->ship->audit->remeasure pipeline. Do not use for single-phase implement only (/implement, /planner) or encore-only (/encore).
---

# LFG

Full outer ship loop from a single aim.

## Pipeline

1. **Deep research** (when external context or unknowns matter).
2. **gap-to-plan** — measure the gap and produce the plan hierarchy.
3. **Ship every gap plan** via planner + universal-gauntlet (medium critic), plan-by-plan and phase-by-phase.
4. **comprehensive-codebase-review**.
5. **/implement** Medium+ fixes from the review.
6. **Remeasure** with gap-to-plan.
7. Prompt the user for `/encore` if residual gap remains.

## Rules

- Universal across codebases (use a project adapter when needed).
- Do not skip the critic gates.
- Persist state so the loop can be resumed.
- Only claim completion when the remeasured gap is acceptably closed or the user accepts residual risk.

## Typical invocation

`/lfg <aim>` or “let’s fucking go on X”.
