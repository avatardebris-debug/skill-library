# Plan archive + unique slug contract

Live paths stay fixed for the implement driver:

| Live (current idea only) | Purpose |
|--------------------------|---------|
| `state/current_idea.json` | Active idea pointer |
| `state/master_plan.md` | Active master plan |
| `phases/phase_N/tasks.md` | Active phase tasks |

**Never** lose the previous idea by silent overwrite.

## Unique slug

1. Derive **base slug** from title/description: lowercase, `[a-z0-9]+` joined by `_` or `-` (prefer `_` to match factory `nested_graph_bridge` style). Strip non-alnum; collapse repeats; max 48 chars.
2. **Occupied** if any of:
   - `state/archive/<slug>/` exists
   - `phases/archive/<slug>/` exists
   - `state/current_idea.json` has that `slug` and you are planning a **different** idea (new title/gap plan)
3. If base is free → use it.
4. If occupied → try `base_2`, `base_3`, … until free (**numeric suffix**, not random UUID).
5. Write the chosen slug into `current_idea.json` as `slug`.

Same idea replan (user says replan / same slug explicitly): **keep slug**, archive is optional snapshot under `state/archive/<slug>/revisions/YYYYMMDD_HHMMSS/` only if overwriting a non-empty master plan with substantial change.

## Archive-before-overwrite (new idea)

When about to write a **new** idea (new slug ≠ current slug, or no current idea → first write is fine):

If `state/current_idea.json` exists and has a non-empty `slug` (call it `old`):

1. Create `state/archive/<old>/` if missing.
2. Copy (prefer move only when live files will be fully replaced):
   - `state/master_plan.md` → `state/archive/<old>/master_plan.md`
   - `state/current_idea.json` → `state/archive/<old>/current_idea.json`
3. For each `phases/phase_N/` that contains `tasks.md` (N = 1..10):
   - Move/copy to `phases/archive/<old>/phase_N/tasks.md`
   - Remove empty live `phases/phase_N/` after move when appropriate
4. **Do not** touch `phases/legacy/`, `phases/legacy2/`, `phases/ship/`, or existing `phases/archive/*`.
5. Then write the new live `master_plan.md` + `current_idea.json`.

If archive target `state/archive/<old>/master_plan.md` already exists, write to  
`state/archive/<old>/revisions/<UTC timestamp>/` instead of clobbering the first archive.

## After write (optional durable copy of new plan)

Also copy the **new** live plan into `state/archive/<new_slug>/master_plan.md` (and current_idea) so the archive has a snapshot even before the next idea supersedes it. Safe to overwrite same-slug archive on intentional replan of the same idea.

## phase-plan

- Writes only **live** `phases/phase_N/tasks.md` for the **current** idea.
- Does **not** archive by itself (idea-plan already archived the previous idea).
- When replan of phase N only: overwrite live `tasks.md` is OK; optional copy previous tasks to  
  `phases/archive/<slug>/phase_N/tasks.prev.md` if file existed and user asked replan.
