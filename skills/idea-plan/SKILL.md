---
name: idea-plan
description: >-
  Turn a raw product idea into a multi-phase master plan for the AICompete
  pipeline / Grok Build factory. Writes state/master_plan.md with flexible
  phase count (1-8, not fixed 3), concrete deliverables and success criteria,
  and updates total_phases in current_idea.json when present. Archives the
  previous idea under state/archive/<slug>/ and phases/archive/<slug>/ before
  overwrite; assigns a unique slug (base or base_2, base_3, …). Use when the user
  asks for a master plan, roadmap, idea plan, deconstruct idea into phases,
  /idea-plan, /master-plan, or before phase-plan / implement.
metadata:
  short-description: "Idea to master_plan.md + archive prior slug"
---

# /idea-plan — Master plan from idea

You are the **idea planner** for an autonomous build factory. Produce a
**structured multi-phase roadmap** concrete enough that `/phase-plan` (or the
classic phase planner) can turn each phase into checkbox tasks, and
`/implement` can ship phase-by-phase.

## When to use

- New idea: title + description only
- User wants a **master plan** / roadmap / phase deconstruction
- Grok Build seed before phase-1 tasks exist
- Replan when the old plan is wrong or too rigid

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Break one phase into tasks | `/phase-plan` |
| Write product code | implement skill / coding session |
| Prove product works | `/field-test` |
| Full idea + phase-1 tasks in one go | `/planner` |

## Inputs

Resolve (ask only if ambiguous):

| Input | Typical path |
|-------|----------------|
| **Project root** | `PIPELINE_DIR/projects/<slug>/` or cwd |
| **Idea** | `state/current_idea.json` (`title`, `description`) or user text |
| **Master plan out** | `state/master_plan.md` (live) |
| **Workspace** | `workspace/` — optional recon if code already exists |

**Soft layout:** plans and tasks never live under `workspace/`.

## Workflow

Track:

- [ ] 1. Recon idea (+ workspace if any)
- [ ] 2. Resolve unique slug (base or base_N)
- [ ] 3. **Archive previous idea** if slug changes (see archive contract)
- [ ] 4. Choose phase count (flexible)
- [ ] 5. Write live `state/master_plan.md` + archive snapshot for new slug
- [ ] 6. Update `state/current_idea.json` (slug, total_phases, …)
- [ ] 7. Summarize for the user

### 1. Recon

1. Read title + description (and any `idea.md` in workspace).
2. If workspace has code, skim entrypoints so phases build on reality.
3. State the **core deliverable** in one sentence (what “done” means).
4. Read existing `state/current_idea.json` if present (old slug, status).

### 2. Unique slug

Follow **`references/plan-archive-contract.md`**:

- Derive **base** from title (e.g. `meta_reasoner`, `nested_graph_bridge`).
- If base is free → use it.
- If occupied → **`base_2`, `base_3`, …** until free.
- Never reuse another idea’s archived slug for a different plan.

### 3. Archive previous idea (mandatory when replacing)

If live `current_idea.json` has a different slug (or you are replacing a finished idea with a new plan):

1. Archive `master_plan.md` + `current_idea.json` under `state/archive/<old_slug>/`.
2. Move live `phases/phase_N/tasks.md` → `phases/archive/<old_slug>/phase_N/tasks.md`.
3. Leave `phases/legacy*`, `phases/ship/`, existing archives alone.

**Do not** write the new plan until archive succeeds (or there is nothing to archive).

### 4. Choose phase count

Follow **flexible** guidance in `references/master-plan-contract.md`:

- Simple CLI / single script → **1–2** phases  
- Multi-component app → **3–5**  
- Hard max **8** — collapse rather than invent Phase 9+  
- Prefer **Phase 1 = working MVP** when the idea allows  

Do **not** force exactly 3 or 5 phases for consistency cosplay.

### 5. Write master plan

Write **`state/master_plan.md`** using the contract in
`references/master-plan-contract.md`.

Also copy to **`state/archive/<new_slug>/master_plan.md`** (durable snapshot).

Rules:

1. Concrete deliverables and success criteria (testable).
2. Explicit dependencies between phases.
3. Architecture notes + risks (short).
4. Include `total_phases: N` under Phase count (or equivalent clear N).

### 6. Update state

Write **`state/current_idea.json`** (and copy to `state/archive/<new_slug>/current_idea.json`):

- `slug`: unique slug from step 2  
- `title`, `description`  
- `total_phases`: N  
- `phase`: `1` for a new idea (keep existing phase only on same-slug replan)  
- `status`: `active` for new ideas  
- UTF-8 **no BOM**  
- Preserve unrelated keys when same-slug replan  

### 7. Output to user

1. Paths: live `master_plan.md`, archive dir, **slug**  
2. Phase table: N | title | deliverable  
3. If prior idea archived: old slug + archive path  
4. Next step: run **`/phase-plan`** for phase 1 (or `/planner`)  

## Success criteria

- Live `state/master_plan.md` exists with 1–8 phases and success criteria  
- Unique `slug` in `current_idea.json`; no silent clobber of prior idea without archive  
- Prior live phases (if any) live under `phases/archive/<old_slug>/`  
- Phase 1 is a shippable MVP when feasible  
- No task checkboxes in the master plan (those belong in `tasks.md`)  

## Related

| Skill | Role |
|-------|------|
| `/phase-plan` | Phase N → live `phases/phase_N/tasks.md` |
| `/planner` | Orchestrate idea-plan then phase-plan |
| `/field-test` | After product is built |

## References

- `references/master-plan-contract.md`
- `references/plan-archive-contract.md`
