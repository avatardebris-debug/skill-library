---
name: planner
description: >-
  Orchestrate pipeline planning for Grok Build / AICompete: run idea-plan
  (master roadmap) and/or phase-plan (checkbox tasks) so implement/review have
  structure. Flexible phase and task counts with fixed file contracts. idea-plan
  archives prior ideas under state/archive/<slug>/ and unique slugs (base_N).
  Use when the user runs /planner, asks to plan a project for the factory,
  "plan then implement", missing master_plan or tasks.md, or full plan
  deconstruction.
metadata:
  short-description: "idea-plan + phase-plan; archive prior slugs"
---

# /planner — Plan orchestration (idea + phase)

Factory builds need **plans before implement**. This skill **routes and runs**
the planning stack; it does not invent a third plan format.

## Skills used

| Skill | Artifact |
|-------|----------|
| **`/idea-plan`** | Live `state/master_plan.md` + unique `slug` + **archive prior** idea |
| **`/phase-plan`** | Live `phases/phase_N/tasks.md` (backup on replan) |

Follow those skills’ contracts and flexible count rules. Load them if present
under `~/.grok/skills/idea-plan` and `~/.grok/skills/phase-plan`.

**Slug policy (summary):** new plan → unique `slug` (`base` or `base_2`, `base_3`, …).  
Before overwrite, archive previous `current_idea` + `master_plan` + live phase tasks under  
`state/archive/<old_slug>/` and `phases/archive/<old_slug>/`.  
Live paths stay fixed for the implement driver.

## Decision tree

```text
Need whole roadmap or no master_plan.md or NEW idea/slug?
  YES → run /idea-plan  (archives prior slug first)
Need tasks for current phase or no tasks.md?
  YES → run /phase-plan for phase N
Both done → report paths and stop (do not implement unless user asked)
```

### Default when user says only `/planner`

1. Resolve **project root** (ask if unclear).  
2. If user named a new idea / gap plan / different product → **idea-plan** (even if master_plan exists).  
3. Else if `state/master_plan.md` missing → **idea-plan**.  
4. N = `current_idea.json` `phase` or **1**.  
5. If `phases/phase_N/tasks.md` missing or empty → **phase-plan**.  
6. Summarize: **slug**, plan path, task path, archive path if any, next = implement.  

### User intent shortcuts

| User says | Do |
|-----------|-----|
| “master plan only” | idea-plan only |
| “tasks for phase 2” | phase-plan N=2 only |
| “full plan for implement” | idea-plan then phase-plan for phase 1 |
| “replan phases, keep code” | idea-plan (same slug if same idea) or phase-plan; never delete archives |
| “plan 2 from gap” / new gap plan | idea-plan as **new idea** → new or numbered slug; archive prior |

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Write code | implement / coding session |
| Field proof | `/field-test` |
| Code review | `/code-review` or review packs |

## Principles (from factory design)

1. **Structure before implement** — checkboxes and master plan stay.  
2. **Flexible counts** — not fixed 3 phases × 5 tasks; hard caps 8 phases / 10 tasks.  
3. **Fixed live contracts** — live paths and `- [ ]` grammar are non-negotiable for the driver.  
4. **Plans outside workspace** — `state/` and `phases/` only.  
5. **Archive before replace** — never silently destroy prior idea plans.  
6. **Do not implement** inside `/planner` unless the user explicitly asks to continue into code.  
7. **Default phase-plan is phase 1 only** (or the single requested N). Do not emit tasks for all phases up front when the user will implement under `/universal-gauntlet` — that skill phase-plans N+1 only after critic ACCEPT on N.  
8. **Tasks always start `- [ ]`** — never pre-checked from planner/phase-plan.

## Output to user

1. What ran (idea-plan / phase-plan)  
2. **slug** (and prior slug if archived)  
3. Absolute or project-relative paths written (live + archive)  
4. Phase count + task count  
5. Explicit next step: implement phase N  

## Success criteria

- Downstream implement has a master plan and a valid `tasks.md` for the target phase  
- Prior idea preserved under `state/archive/<slug>/` when a new idea was planned  
- Flexible sizing applied without breaking pipeline parsers  
