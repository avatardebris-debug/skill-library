---
name: zero
description: >-
  Zero-based redesign: mission, /req requirements inventory, minimum viable
  concepts, from-scratch plan, capability matrix, then /gap-to-goal and
  /harsh-critic. Occasional cleanup (e.g. before factory-qc on a small surface).
  Conceptual and plan/clone only — never live delete or in-place rewrite.
  Use when the user runs /zero, zero-based rethink, simplify from scratch, or
  Occam/Feynman redesign of existing code/tool/system.
---

# /zero — Zero-based redesign (plan / clone only)

You run a **disciplined clean-slate rethink**. Existing code is a **hypothesis under glass**, not sacred—and **not to be deleted live**.

## Purpose

Fight complexity drift by:

1. Re-deriving design from the **mission**  
2. **Defining** requirements as owned rows (`/req`) before Occam  
3. Keeping only **minimum viable concepts** (aligned to keep / load-bearing R’s)  
4. Sketching a **simpler** plan  
5. Checking the plan still covers **goals** (`/gap-to-goal`)  
6. Surviving **`/harsh-critic`**  
7. Presenting **diffs / nuances to the human** — no silent cutover  

## When to use

- Occasional cleanup of a **small** subsystem (not the whole monorepo on first runs)
- Before factory-qc on a surface that has grown messy (optional hygiene)
- Major refactor **planning** (still plan-only until human approves implement)

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Requirements inventory only | `/req` alone |
| New capability for an arriving goal | `/gap-to-plan` + `/lfg` |
| Scored critique of an existing plan | `/harsh-critic` alone |
| Full multi-plan ship | `/lfg` |
| Measure factory health | `/factory-qc` |
| Live compress execute / delete modules | **Forbidden** |

## Hard safety (non-negotiable)

1. **Never** delete, strip, or rewrite files in the live production tree as part of Occam.  
2. Occam “delete if yes” applies only to **requirement rows** (`propose_delete`), **concept list**, and **proposed plan** rows — never live `rm`/edit of originals.  
3. Optional mock: **clone / worktree / notes under `notes/zero/<slug>/` only** — original stays intact.  
4. **No cutover** without explicit human approval after comparison pack.  
5. Do not invent field_proven / published_live / invent_human_verdict / auto-compress.  
6. Prefer **git branch or worktree** if any experimental tree is created; never sole copy of critical state.  
7. **Human-floor requirements** from `/req` (mission_core, safety, honesty, constitution, legal_compliance) are not agent-deleted; see `/req` skill.  
8. Factory language that says **never** auto-LFG / outer RSI / live delete is **binding for this agent run** unless the human explicitly waives a specific line in writing this session. Do not act as if “never” is optional.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| **Target** | Yes | Path, module, tool name, or description |
| **Mission hint** | No | User one-liner; else extract from code/docs |
| **Goals to protect** | No | Multi-step / product goals the system must still serve |
| **Slug** | No | Default from target name |

## Workflow

Track:

- [ ] 1. Mission extraction (Feynman)
- [ ] 2. Original capability matrix (read-only inventory)
- [ ] 3. **`/req`** — REQUIREMENTS.md (define + challenge rows)
- [ ] 4. Minimum viable concepts (Occam on **list only**, driven by keep R’s)
- [ ] 5. Zero-based sketch
- [ ] 6. Write / refresh artifacts under `notes/zero/<slug>/`
- [ ] 7. `/gap-to-goal` (zero plan vs goals + load-bearing R’s)
- [ ] 8. Bridge load-bearing gaps only (plan rows)
- [ ] 9. `/harsh-critic` (mandatory gate)
- [ ] 10. Loop ≤3 (refine → gap-to-goal if goals changed → harsh) or RESTART
- [ ] 11. Human pack — stop for approval

### 1. Mission extraction (Feynman)

Write **1–2 sentences**: what job, for whom, under what constraints. **No** implementation detail.

Then **required Feynman check**:

> Explain the mission in plain language as if teaching a smart 12-year-old (2–3 sentences).

If muddy → rewrite mission before continuing. Write draft to `notes/zero/<slug>/MISSION.md` early if helpful.

### 2. Original capability matrix (read-only)

From disk (read only), list **mission-critical behaviors/capabilities** of the current system:

| capability | evidence (path/note) | mission-critical? |

Ignore implementation structure. This is the baseline for `/req` sources, comparison, and `/gap-to-goal`.

Write `CAPABILITY_MATRIX.md` (may refine later).

### 3. `/req` (required)

Load and follow **`req`** skill (`~/.grok/skills/req/SKILL.md`).

Inputs:

- Target, mission, capability matrix, optional user goals  
- Out dir: **`notes/zero/<slug>/`** (same pack)  
- Doctrine/constitution paths if present  

Output: **`notes/zero/<slug>/REQUIREMENTS.md`** (optional `requirements.json`).

Rules for zero after `/req`:

- Occam on concepts must **not drop** behaviors needed by `load_bearing: yes` + `status: keep` without a plan bridge or human challenge resolution  
- Rows with `status: propose_delete` become **candidates** for concept prune / plan `propose_remove` — still not live delete  
- Rows with `status: challenge` or `unknown`: prefer **not** pruning dependent concepts until human answers; if you must proceed, list them under STATUS as open questions  
- Floor kinds remain protected per `/req`  

If `/req` cannot run (missing mission): stop and fix step 1.

### 4. Minimum viable concepts (Occam on list only)

List **concepts only** (not files, not libraries).

Drive the list from:

- Mission  
- REQUIREMENTS with `status: keep` (especially `load_bearing: yes`)  
- Capability matrix (mission-critical rows still keep-aligned)  

For **each** concept, apply:

> Apply Occam’s razor: Is this concept **strictly necessary** to fulfill the mission and **keep** load-bearing requirements, or can those still be achieved without it? Prefer the smaller set.

- If not necessary → move to **`pruned_concepts`** with one-line rationale (**proposal**, not live delete).  
- Prefer linking pruned concepts to `propose_delete` requirement ids when relevant.  
- Surviving list = **`CONCEPTS.md`**.

### 5. Zero-based sketch

Describe the **simplest** system that delivers **only** surviving concepts **and** keep load-bearing requirements.

- Conceptual / interface level first  
- Occam: fewest moving parts, clearest boundaries  
- Feynman: re-explain the whole proposed system simply; if jargon-heavy, simplify the design  

Include optional table of **proposed changes** vs original:

| concept | original approach | proposed approach | action | related_req_ids |
|---------|-------------------|-------------------|--------|-----------------|
| … | … | … | keep \| propose_merge \| propose_remove \| propose_add | R1, R3 |

`propose_remove` is **never** executed here.

### 6. Artifacts

Write under workspace (create dirs as needed):

```text
notes/zero/<slug>/
  MISSION.md
  REQUIREMENTS.md      # from /req (mandatory)
  requirements.json    # optional
  CONCEPTS.md          # surviving + pruned sections
  CAPABILITY_MATRIX.md # original
  ZERO_PLAN.md         # sketch + proposed change table
  COMPARISON.md        # side-by-side capabilities (feature/behavior only)
  STATUS.md            # stage, open challenge/unknown R’s, harsh verdict, human gate pending
```

Do **not** edit the target module’s production files.

### 7. `/gap-to-goal` (required)

Load and follow **`gap-to-goal`** skill (`~/.grok/skills/gap-to-goal/SKILL.md`).

Inputs: mission, ZERO_PLAN, CAPABILITY_MATRIX, optional user goals list, **plus load-bearing keep rows from REQUIREMENTS.md** as goals when user goals are sparse.

Output: `notes/zero/<slug>/GOAL_GAPS.md` (and any files that skill writes).

If goal-gaps are **large** (load-bearing): bridge **minimum** plan rows into ZERO_PLAN (still plan-only). Do not expand scope into a new product empire.

### 8. `/harsh-critic` (required)

Load and follow **`harsh-critic`** skill.

Feed: mission, REQUIREMENTS summary (floor + load-bearing), concepts, ZERO_PLAN, original capability matrix, plus GOAL_GAPS summary.

Paste or write critic output to `notes/zero/<slug>/HARSH.md`.

### 9. Friction loop

| Critic / gap result | Action |
|---------------------|--------|
| harsh ACCEPT and no large goal gaps | Proceed to human pack |
| REJECT or CONDITIONAL or open goal gaps | Refine plan only; re-run gap-to-goal if goals affected; re-harsh |
| 3rd consecutive harsh REJECT on same lineage | **RESTART** from mission extraction (re-run `/req` if mission or target changed); note in STATUS |

Max **3** refine cycles per lineage before restart.

### 10. Human pack (always stop here)

Present:

1. Mission  
2. REQUIREMENTS summary (counts; propose_delete shortlist; challenge/unknown queue; floor ids)  
3. Concept list (surviving / pruned)  
4. Comparison matrix (original vs proposed **capabilities**)  
5. GOAL_GAPS summary  
6. Harsh VERDICT + scores  
7. Explicit options for human:

```text
A) Approve conceptual plan only (no code)
B) Approve implement on clone/worktree only
C) Bridge listed items only (plan amend)
D) Resolve challenge/unknown requirements, then re-run from /req or concepts
E) Reject / park / restart mission
F) Do not touch original; leave notes for later
G) Continue → /zero2 then /restore (or full /elon2 remaining steps)
```

**Do not** implement cutover unless user explicitly chooses B (or equivalent) in a follow-up.

### 11. Implementation (only if human approved clone)

If and only if user approved:

- Build under **parallel path / worktree** — never in-place original  
- Re-compare capabilities empirically  
- Cutover remains a **separate** human decision  

Default for first uses: **stop after human pack**.

## Relationship to other skills

| Skill | Role |
|-------|------|
| **`/req`** | **Mandatory:** define + challenge requirements before concept Occam |
| `/harsh-critic` | Mandatory quality/simplicity gate |
| `/gap-to-goal` | Mandatory: does zero plan still hit goals / load-bearing R’s? |
| `/zero2` | After this pack: code-level map + adjustment candidates (module or zero-cross fan-out) |
| `/restore` | After zero (+ zero2): human add-back portfolio (~10% band); pre clone/LFG |
| `/elon2` | Orchestrator: req→zero→zero2→restore→ship compress playlist |
| `/gap-to-plan` | **Different** — expand for a new aim (use when goals need more capability, not when simplifying) |
| `/factory-qc` | Measure-only health; zero is occasional cleanup, not a QC replacement |
| `/lfg` | Ship expand aims; not the default after zero (use after `/restore` picks) |

## Tone

Clear, structured, ruthless about complexity. Mission and requirements table first, then concepts. Comparison matrices easy to scan.

## Success criteria

- Artifacts under `notes/zero/<slug>/` including **REQUIREMENTS.md**  
- `/req` run (or user-waived in writing — rare)  
- Occam only on requirements/concepts/plan, not live tree  
- gap-to-goal + harsh-critic both run (or user waived in writing)  
- Human pack presented; no silent cutover  
- Original production code unmodified by this skill  
