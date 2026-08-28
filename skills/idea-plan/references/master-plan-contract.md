# Master plan contract (pipeline)

Write **`state/master_plan.md`** under the **project root** (not under `workspace/`).

Factory layout: `PIPELINE_DIR/projects/<slug>/state/master_plan.md`.

## Required shape

```markdown
# Master Plan: {Idea Title}

## Goal
[1-2 sentence summary of what we're building and why]

## Phase 1: {title} — {short label}
- **Description**: [what this phase builds]
- **Deliverable**: [concrete output on disk / UX]
- **Dependencies**: none
- **Success criteria**:
  - [specific, testable criterion]
  - [another criterion]

## Phase 2: {title} — {short label}
- **Description**: ...
- **Deliverable**: ...
- **Dependencies**: Phase 1
- **Success criteria**:
  - [criterion]

## Phase N: ...
[only if justified]

## Architecture Notes
[stack, layout, key APIs]

## Risks
[uncertain / failure modes]

## Phase count
- total_phases: N
```

## Phase count guidance (flexible)

| Idea shape | Typical phases | Notes |
|---|---|---|
| Tiny CLI / single script | **1** | One shippable tool |
| Simple tool + polish | **2** | MVP then hardening/docs/UX |
| Multi-surface product | **3–5** | Web + API + data, etc. |
| Large / multi-subsystem | **up to 8** | Hard max; collapse if more |

- Prefer **fewer** phases when Phase 1 can be a full working MVP.
- **Hard max: 8 phases.** If you want more, you are over-scoping — merge.
- Do **not** force exactly 3 or 5. Choose N from complexity.

## Phase 1 rule

**Phase 1 must be a complete working MVP** for the core idea when feasible — not empty scaffolding. Later phases add depth, not the first “hello world only” unless the idea itself is that small.

## State side effects

After writing the plan, update **`state/current_idea.json`**:

- `slug`: unique (see `plan-archive-contract.md` — `base` or `base_2`, `base_3`, …)
- `total_phases`: integer N matching the plan
- `phase`: `1` for a new idea; keep existing only on same-slug replan
- Do **not** invent unrelated status transitions on same-slug replan (leave `status` alone unless seeding)

**Before** replacing a different idea: archive prior live plan/tasks per `plan-archive-contract.md`.

Also snapshot: `state/archive/<slug>/master_plan.md` + `current_idea.json`.

Use UTF-8 **without BOM**. Preserve other JSON keys on same-slug replan.
