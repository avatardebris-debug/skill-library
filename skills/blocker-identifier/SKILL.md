---
name: blocker-identifier
description: >
  Diagnose why an AICompete / Grok Build project is stuck (budget_exceeded,
  budget_yielded, dep_waiting, stalled validation) and emit a structured
  blocker_report.v1 for the manager routing menu. Does not implement fixes or
  force-advance. Use when the user runs /blocker-identifier, asks to identify
  blockers, budget exceeded routing, BE2/BE3 triage, why requires is blocked,
  yield review, or manager needs a cost/benefit blocker report before extend
  budget, debug, soft-skip requires, park, or ask operator.
---

# Blocker Identifier

## Role

You are a **diagnosis + routing reporter**, not a fixer.

**Produce** a `blocker_report.v1` JSON (and a short human summary) so a **manager**
(or operator) can choose from a closed decision menu.

**Do not:** rewrite the factory, mark deps complete, force-advance phases,
spawn new ideas, or run unbounded multi-skill fix loops. If a tactical fix is
recommended, name the skill/path only (`systematic-debugging`, thin field, etc.).

## When to run

- Status is `budget_exceeded` / `budget_yielded` / strike ≥ 2, or user asks “why is this blocked?”
- Open `requires:` chains wait on this slug
- Manager BE3 / evaluation pass needs structure before deciding
- Operator asks for a yield review before ignore / bypass / re-queue

## Strike ladder (context only)

| Strike | Meaning | Your job |
|--------|---------|----------|
| 1 | Yielded once; auto-retry OK | Light report OK; often `timer_glitch` or clean re-entry |
| 2 | After BE2 tactical attempt failed or skipped | Full report; recommend one tactical path if cheap |
| ≥3 | Manager / evaluation | Full report + cost/benefit + goal relevance + `next_policy` hints |

If strikes are unknown, infer from `budget_note`, `budget_strikes`, `yield_reviews`, and notes.

## Procedure

### 1. Resolve target

Inputs (any subset):

- Project **slug** (required if not inferable)
- `PIPELINE_DIR` / projects root (default: env `PIPELINE_DIR`, else `.pipeline`)
- Optional: factory repo root, goal ids

Locate:

```text
{PIPELINE_DIR}/projects/{slug}/state/current_idea.json
{PIPELINE_DIR}/projects/{slug}/phases/phase_N/{tasks,validation_report,fix_report}.md
{PIPELINE_DIR}/projects/{slug}/workspace/
```

Also scan (when present):

- `master_ideas.md` for unchecked lines with `requires: {slug}` or this project’s deps
- Peer deps’ `current_idea.json` statuses
- `manager_decisions.md`, `budget_note`, `pre_budget_status`, `phase_retries.json`

If the project dir is missing, report `blocker_class: missing_project` and stop.

### 2. Gather evidence (read-only)

Collect:

1. **Status surface:** status, phase/total_phases, tasks_done/tasks_total, budget_lock, depends_on, pre_budget_status, budget_note, session_started_at / started_at
2. **Near-done?** phase ≥ total_phases or final-phase validating/reviewing with artifacts
3. **Timer hygiene:** wall elapsed vs budget; multi-day gaps; sleep/calendar glitch pattern (huge minutes, little workspace change)
4. **Validation / fix history:** last validation_report, fix_report, retry counters
5. **Deps:** each `depends_on` → status; whether deps satisfy full complete / field_proven
6. **Dependents:** open master_ideas (or on-disk dep_waiting) that require this slug
7. **Prior reviews:** yield_reviews, last_decision, next_policy if stored

Do **not** mutate state unless the user explicitly asks to write the report file.

### 3. Classify blocker

Pick **one** primary `blocker_class` (see references):

| Class | Signals |
|-------|---------|
| `timer_glitch` | Absurd wall minutes; stale session_started_at; little progress delta |
| `validate_stuck` | Same validation failures; pre_budget in validating |
| `missing_dep` | depends_on not full complete / field_proven |
| `scope_too_big` | Huge task list; mid-phase forever; retries explode |
| `wrong_approach` | Fix reports cycle; design mismatch |
| `external` | GPU/API/keys/network/hardware |
| `retry_storm` | Lifetime retries / counter corruption notes |
| `near_done_unproven` | pN/N artifacts exist; never field_proven / complete |
| `dep_chain_critical` | Open dependents + this slug is the only hard blocker |
| `unknown` | Insufficient evidence |

Secondary classes go in `secondary_classes[]`.

### 4. Estimate cost / benefit (honest ranges)

- `est_fix_minutes` — if near-done or clear single root cause  
- `est_rebuild_minutes` — full replan/rebuild  
- `est_debug_pass_minutes` — one systematic-debug / thin-field pass  
- `goal_relevance`: `high|medium|low|unknown` (use goal tags / dependents / operator context)  
- Prefer **fix prereq** over inventing new ideas that re-require this slug  

### 5. Recommend manager decisions

Recommend **ordered** subset of the closed menu (do not invent new decision names):

| Decision | Use when |
|----------|----------|
| `EXTEND_BUDGET` | On-goal, progressing, timer was real active work or lock-worthy |
| `DEBUG_AGAIN` | Clear technical root cause; cheap; strike allows |
| `THIN_FIELD` | Near-done product; prove unlocks deps |
| `BYPASS_RETURN` | Yield slot; keep in portfolio; re-queue later |
| `SOFT_SKIP_REQUIRES` | Dependent MVP does not need hard wait — **never** marks this slug complete |
| `SUBSTITUTE` | Another field_proven / GitHub capability covers the need |
| `IGNORE_NEXT` | Low relevance; skip one cycle |
| `ASK_OPERATOR` | Ambiguous, goal-critical, or first soft-bypass of requires |
| `ARCHIVE_GOAL_EDGE` | Not needed for current goals |
| `AUTO_RETRY_CLEAN` | Strike 1 / timer_glitch — fresh active clock only |

Default policy hints:

- Goal-critical + first soft-bypass → include `ASK_OPERATOR`
- `timer_glitch` → prefer `AUTO_RETRY_CLEAN` over ARCHIVE
- Open dependents + near_done → prefer `THIN_FIELD` or `DEBUG_AGAIN` over new ideas

### 6. next_policy

Suggest one:

- `remain_queue` — keep auto-eligible  
- `ask_again` — next BE3 must ASK_OPERATOR  
- `ignore_next` — skip one manager cycle  
- `ignore_until` — needs `ignore_until` ISO or cycle count  
- `cooldown` — needs `cooldown_days`  

### 7. Emit artifacts

**Always** print:

1. A fenced JSON block matching `blocker_report.v1` (see `references/blocker_report.v1.md`)
2. A short markdown summary for humans / manager_decisions append

**Write to disk when path is known and user did not forbid writes:**

```text
{PIPELINE_DIR}/projects/{slug}/state/blocker_report.json
```

Optional append one section to:

```text
{PIPELINE_DIR}/state/manager_decisions.md
```

Format:

```markdown
## blocker-identifier {slug} {ISO}
- class: ...
- recommended: ...
- next_policy: ...
(path to blocker_report.json)
```

## Output rules

- Prefer evidence over speculation; mark unknowns  
- **Never** set status to complete/field_proven  
- **Never** claim deps satisfied because of budget_exceeded  
- One primary recommendation first in `recommended[]`  
- If multiple slugs: one report per slug (batch only if user asks)  
- Keep JSON valid (no comments inside the JSON fence)

## Related skills (name only — do not auto-run unless user asks)

- Strike 2 tactical: `systematic-debugging`, field-test / thin ship, review  
- Verify after fix: check-work / verification-before-completion  
- This skill stops at the report; manager (or user) chooses the path  

## Quick start prompts

```text
/blocker-identifier sim_real_comparator
```

```text
Identify blockers for all budget_exceeded projects that block open requires:
```

```text
BE3 review: write blocker_report.v1 for {slug} and recommend manager menu option
```
