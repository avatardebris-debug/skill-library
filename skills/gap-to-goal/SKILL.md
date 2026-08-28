---
name: gap-to-goal
description: >-
  Small gap analysis: does a plan or Elon1 patch still meet stated goals /
  keep load-bearing requirements? Writes a thin gap pack. Use when /gap-to-goal,
  after /zero sketch, after /elon1 patch, or "will this still hit goals".
  Not /gap-to-plan; not live edit; not LFG.
---

# /gap-to-goal — Zero plan vs goals (thin gap)

You measure whether a **proposed plan** (usually from `/zero`) still delivers
**goals** and **mission-critical capabilities**. You do **not** ship multi-plan
hierarchies like `/gap-to-plan`, and you do **not** edit production code.

## Purpose

`/zero` optimizes for **simplicity**. This skill checks it did not **drop load-bearing goal capability**.

Opposite of expansion LFG: here the plan is fixed and we ask “what **must** still work?”

## When to use

- Required step inside `/zero` after ZERO_PLAN exists  
- **`/elon1` after a patch:** plan = the change; goals = keep + load-bearing rows (new-work; skip capability matrix)  
- Manual: `/gap-to-goal` with a plan path + goals  
- After a simplification sketch, before harsh-critic or human approve  

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Full aim → multi-plan hierarchy | `/gap-to-plan` |
| Ship missing features | `/lfg` or `/gap-to-plan` then LFG |
| Score simplicity bar | `/harsh-critic` |
| Clean-slate redesign | `/zero` |
| Live implement | `/implement` (only after human) |

## Hard safety

1. **Read-only** on production code.  
2. Gaps are **proposals** (`bridge_suggest`, `must_keep`, `park`) — never live deletes or silent adds.  
3. Do not invent goals not provided by user or original capability matrix.  
4. Do not claim field_proven / goal_proven_human from this analysis.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| **Plan** | Yes | `ZERO_PLAN.md`, pasted plan, or Elon1 patch (paths + one paragraph) |
| **Mission** | Yes | From `/zero`, `/elon1`, or user |
| **Goals** | Preferred | User list, or keep + load-bearing rows |
| **REQUIREMENTS.md** | Preferred | `load_bearing: yes` + `status: keep` as goals |
| **Original capability matrix** | Compress only | From `/zero` CAPABILITY_MATRIX. **Skip** on Elon1 / new-work |
| **Out dir** | No | Default `notes/zero/<slug>/`, `notes/req/<slug>/` (elon1), or `notes/gap_to_goal/<slug>/` |

If goals are empty: prefer **load-bearing keep rows** from REQUIREMENTS.md (label `from_requirements`). On **new-work / elon1**, do not invent a capability matrix. On compress, if no req rows: derive candidates only from mission-critical matrix rows (`inferred_from_matrix`).

## Workflow

### 1. Lock goal set

Normalize goals into a short list:

```text
G1: <goal>
G2: <goal>
...
```

Each goal: one line, measurable if possible (“still able to…”, “operator can…”).

### 2. Capability coverage matrix

For each goal × plan:

| goal_id | goal | covered_by_plan? | how (concept/step) | severity if missing |
|---------|------|------------------|--------------------|---------------------|
| G1 | … | yes/partial/no | … | none/small/medium/large |

Severity guide:

| Severity | Meaning |
|----------|---------|
| **large** | Mission-critical goal fails under plan |
| **medium** | Important path degraded; needs bridge |
| **small** | Edge / convenience |
| **none** | Covered |

### 3. Original vs plan (mission-critical only)

**Skip this section** on Elon1 / new-work (no matrix). Using capability matrix when present:

| capability | original | in_zero_plan? | keep_required? | note |
|------------|----------|---------------|----------------|------|
| … | yes | yes/no | yes if mission-critical and missing |

Flag **silent drops**: mission-critical original capabilities with `in_zero_plan=no`.

### 4. Gap parts (thin — not multi-plan ship)

List assemblable **bridge suggestions** only (cap ~10):

```text
Part: <name>
  Closes: <goal_ids / capabilities>
  Kind: keep_original_concept | add_concept | plan_row_only | human_process | park
  Severity: large | medium | small
  Suggest: <one line plan change — not live code>
```

**Grain:** this is a **thin gap pack**, not a full `/gap-to-plan` multi-plan tree.  
If gaps are huge and aim is “add a new product,” hand off: “use `/gap-to-plan` + `/lfg` for expansion; do not stuff empire into zero plan.”

### 5. Write artifacts

Prefer the caller’s pack dir:

```text
notes/zero/<slug>/GOAL_GAPS.md          # /zero / elon2
notes/req/<slug>/GOAL_GAPS.md           # /elon1
notes/gap_to_goal/<slug>/gap.md         # standalone
```

### 6. Summary for caller

Always return:

1. Goal count + large/medium/small gap counts  
2. Silent drops (mission-critical)  
3. Top 3 must-bridge items  
4. Verdict for zero pipeline:

```text
GOAL_COVERAGE: OK | BRIDGE_REQUIRED | EXPAND_INSTEAD
```

| Verdict | Meaning |
|---------|---------|
| **OK** | No large gaps; medium only optional |
| **BRIDGE_REQUIRED** | Large/medium mission-critical gaps — amend zero plan (plan-only) |
| **EXPAND_INSTEAD** | Goals imply **new** mission scope → recommend `/gap-to-plan`/`/lfg`, not stuffing into zero |

## GOAL_GAPS.md template

```markdown
# Goal gaps vs plan

## Mission
...

## Goals
- G1: ...
- G2: ... (inferred_from_matrix?)

## Coverage summary
- large: N
- medium: N
- small: N
- GOAL_COVERAGE: OK | BRIDGE_REQUIRED | EXPAND_INSTEAD

## Silent drops (mission-critical)
- ...

## Bridge suggestions (plan-only)
1. ...
2. ...

## Non-aims
- no live delete
- no auto implement
- no invent goals beyond inputs/matrix
```

## Relationship

| Skill | Relation |
|-------|----------|
| `/zero` | Caller; uses this after sketch |
| `/req` | Load-bearing keep rows seed goals when user goals sparse |
| `/harsh-critic` | Usually after bridges; simplicity + mission floors |
| `/restore` | Different: which ~10% to deliberately re-add (cost-benefit), not mission coverage alone |
| `/elon2` | Runs gap-to-goal inside `/zero`; may re-run after restore accept |
| `/elon1` | After the patch: keep rows vs what shipped |
| `/gap-to-plan` | Full expand hierarchy for **new** aims |
| `/lfg` | Ship expansion |

## Success criteria

- Matrix of goals vs plan written  
- Silent drops listed  
- GOAL_COVERAGE verdict  
- No production edits  
