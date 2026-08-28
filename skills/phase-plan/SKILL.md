---
name: phase-plan
description: >-
  Decompose one master-plan phase into ordered checkbox tasks for the AICompete
  pipeline / Grok Build implement loop. Writes phases/phase_N/tasks.md in the
  exact - [ ] contract (What / Files / Done when), with flexible task count
  (about 2-8, max 10) sized for one implement session. Uses current idea slug
  from state/current_idea.json; optional backup of prior tasks under
  phases/archive/<slug>/ on replan. Use when the user asks for phase tasks,
  sprint plan, task breakdown, /phase-plan, before /implement, or when tasks.md
  is missing for the current phase.
metadata:
  short-description: "Phase → tasks.md for current idea slug"
---

# /phase-plan — Phase → implementable tasks

You are the **phase planner** for an autonomous build factory. Turn **one phase**
from the master plan into a **checkbox task list** for implement.

**Checkbox rule:** always write tasks as `- [ ]` (unchecked). Never pre-check
`- [x]`. Under `/universal-gauntlet` (factory mode), only the **orchestrator**
flips `- [x]` after an **independent critic ACCEPT** for that phase — not
phase-plan, and not the builder at implement time.

## When to use

- `state/master_plan.md` exists; need `phases/phase_N/tasks.md`
- User says “break down phase N”, “write tasks”, “sprint plan”
- Grok driver cannot run implement until `tasks.md` exists
- Replan a phase after scope change

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Whole-idea roadmap / new idea | `/idea-plan` (archives prior idea first) |
| Write product code | implement skill / coding session |
| Field proof | `/field-test` |
| Idea + phase-1 tasks together | `/planner` |

## Inputs

| Input | Typical path |
|-------|----------------|
| **Project root** | `PIPELINE_DIR/projects/<slug>/` or cwd |
| **Phase number N** | User / `state/current_idea.json` → `phase` (default 1) |
| **Slug** | `state/current_idea.json` → `slug` (required for archive backups) |
| **Master plan** | `state/master_plan.md` (live current idea only) |
| **Tasks out** | `phases/phase_N/tasks.md` (live) |
| **Workspace** | `workspace/` — **must** recon so Files: match reality |

Create `phases/phase_N/` if missing. **Never** write tasks under `workspace/`.  
**Never** write into another idea’s `phases/archive/<other_slug>/` as live tasks.

## Workflow

Track:

- [ ] 1. Load phase N from master plan + current slug
- [ ] 2. Recon workspace
- [ ] 3. Draft 2–8 tasks (max 10), sized for one implement
- [ ] 4. If replan and live tasks exist: backup under archive
- [ ] 5. Write live `phases/phase_N/tasks.md` (exact contract)
- [ ] 6. Summarize for the user

### 1. Load phase

1. Read `state/current_idea.json` → `slug`, default phase.
2. Read `state/master_plan.md`; extract **Phase N** title, description, deliverable, success criteria.
3. If master plan missing → stop and tell user to run **`/idea-plan`** first.
4. Confirm N with user only if ambiguous.

### 2. Recon workspace

1. List entrypoints and existing modules.
2. Prefer tasks that extend real files; do not invent package names that conflict with layout.
3. Note tests already present.

### 3. Size the task list

Follow `references/tasks-contract.md`:

- Soft target **3–6** tasks; **2–8** normal band; **hard max 10**  
- Each task ~ one implement session (not 15 micro-tasks)  
- Ordered; atomic; testable **Done when**  
- At least one **tests / verification** task if product code ships  
- Optional `## Out of scope` for deferred work  

Do **not** force exactly 3–5 for old 35B habit when Grok can hold a slightly larger phase — still avoid 12+ checkboxes.

### 4. Backup on replan (same idea)

If `phases/phase_N/tasks.md` already exists and you are rewriting it:

- Copy to `phases/archive/<slug>/phase_N/tasks.prev.md` (or timestamped if `.prev` exists).
- See idea-plan `references/plan-archive-contract.md` for layout.

Do **not** delete `phases/archive/` or `phases/legacy*`.

### 5. Write tasks.md

Exact checkbox grammar (pipeline-critical):

```markdown
# Phase {N} Tasks: {Phase Title}

- [ ] Task 1: [title]
  - What: ...
  - Files: ...
  - Done when: ...
```

Rules:

- Top-level bullets only for tasks: **`- [ ]` only** — never write `- [x]` from phase-plan  
- Nested `What` / `Files` / `Done when`  
- No `## Task 1` headings, no emoji checkmarks  
- Files relative to **workspace/** when factory project; else repo paths as used in this monorepo  
- Do not mark the phase complete in master_plan or `current_idea.json` from phase-plan  
- Prefer planning **only the requested phase N** (not phases N+1.. in the same write) unless the user explicitly asked for multi-phase task files without implement gates

### 6. Output to user

1. Path to live `tasks.md` (+ backup path if any)  
2. Ordered task titles  
3. Current **slug**  
4. Next: **implement** this phase; under `/universal-gauntlet`, then **independent critic** before phase-plan N+1 or flipping `- [x]`  

## Success criteria

- Live `phases/phase_N/tasks.md` parses as checkbox tasks for the driver  
- All tasks emitted as `- [ ]` (none pre-checked)  
- Tasks map to phase success criteria and workspace reality  
- Task count in 2–10 with clear Done when  
- No other phases’ work mixed in  
- Prior tasks preserved under archive when replanning  

## Related

| Skill | Role |
|-------|------|
| `/idea-plan` | Idea → master_plan + archive prior slug |
| `/planner` | Orchestrate idea-plan + phase-plan |
| `/universal-gauntlet` | Factory: implement → per-phase critic → only then `[x]` and phase N+1 |
| `/field-test` | After product complete |
| `systematic-debugging` | After implement fails tests |
