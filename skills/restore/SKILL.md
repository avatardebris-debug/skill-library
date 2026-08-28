---
name: restore
description: >-
  Human weigh-in after compress: rank what to add back (~10% band) vs leave
  deleted. Cost-benefit + gap-to-prior portfolio from propose_delete / pruned
  concepts / zero2 candidates. Logs ratios for calibration. End of /elon2
  compress or pre gap-to-plan/LFG. Use when /restore, re-add features, add-back
  portfolio, or Elon "deleted so much you add ~10% back". Not live delete;
  not full gap-to-plan; not gap-to-goal (different question).
metadata:
  short-description: "Add-back portfolio after zero compress"
argument-hint: "[slug] [--out notes/zero/<slug>]"
---

# /restore — Add-back portfolio (human gate)

You help the human decide **which deleted/proposed-deleted things deserve to
come back**. You do **not** ship. You do **not** live-delete. You **do** write
a portfolio and optionally append a **metrics run** for long-horizon calibration.

## Purpose

Elon-style discipline: delete hard, then **deliberately** restore a **small**
fraction. This skill is the weigh-in between compress (`/req` `/zero` `/zero2`)
and ship (`clone` / `/gap-to-plan` / `/lfg`).

| Skill | Question |
|-------|----------|
| `/gap-to-goal` | If we **don’t** add these back, does mission still hold? |
| **`/restore`** | Which ~10% **should** we deliberately put back, at what cost? |
| `/gap-to-plan` | Multi-part hierarchy to **build** chosen restores or new aims |

## When to use

- End of `/elon2` compress loop (default)  
- After `/zero` + optional `/zero2` when human wants re-add ranking  
- Pre-LFG / pre–gap-to-plan: feed selected Tier A/B into an aim  
- Standalone: `/restore <slug>` with existing `notes/zero/<slug>/`  

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Still defining requirements | `/req` |
| Clean-slate concepts | `/zero` |
| Code map only | `/zero2` |
| Mission coverage check only | `/gap-to-goal` |
| Full ship | `/lfg` after human picks ids |

## Hard safety

1. Read-only on production sources.  
2. Writes under `notes/zero/<slug>/` and optionally `notes/elon/metrics/`.  
3. No live delete, no auto-implement, no auto-LFG.  
4. Floor kinds (`mission_core`, `safety`, `honesty`, `constitution`, `legal_compliance`) are **not** “left deleted” if they were never legally `propose_delete` — if missing from zero plan, flag **critical bridge**, not Tier C.  
5. Do not force portfolio ratio to 10% to game metrics.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| **Slug / zero pack** | Yes | `notes/zero/<slug>/` |
| **REQUIREMENTS.md** | Preferred | propose_delete, challenge, keep load-bearing |
| **CONCEPTS.md** | Preferred | pruned_concepts |
| **ADJUSTMENT_CANDIDATES.md** | Optional | zero2 high/med propose_* |
| **GOAL_GAPS.md** | Optional | silent drops / bridges |
| **ZERO_PLAN.md** | Preferred | what survives without restore |
| **Human notes** | Optional | “I care about X” |

If pack missing: stop and ask for `/zero` (or `/elon2`) first.

## Workflow

Track:

- [ ] 1. Load pack + inventory delete candidates  
- [ ] 2. Score each candidate (benefit, cost, gap_to_prior, risks)  
- [ ] 3. Assign tiers A/B/C (aim small A, not half of D)  
- [ ] 4. Write RESTORE_PORTFOLIO.md  
- [ ] 5. Append metrics run (see calibration)  
- [ ] 6. Calibration snapshot + optional CALIBRATION_HINT  
- [ ] 7. Human pack — stop  

### 1. Inventory candidates

Union of:

- R rows with `status: propose_delete` (and optionally `challenge`)  
- Pruned concepts from CONCEPTS.md  
- zero2 rows: `propose_orphan`, high-risk `propose_merge` that remove behavior (not pure refactors)  
- GOAL_GAPS silent drops / park items that zero treated as droppable  

Dedupe by related ids. Cap portfolio rows ~**30**; park overflow in “later” list.

`D_prop` = count of distinct delete-side candidates (document definition in pack).

### 2. Score (tables, not essays)

For each candidate:

| Field | Guide |
|-------|--------|
| **benefit** 1–5 | Mission / operator value if restored |
| **cost** 1–5 | Complexity, LOC, dual-system, ops load |
| **gap_to_prior** | high/med/low shape drift if **omitted** |
| **risk_if_wrong** | If we restore and it was junk |
| **risk_if_omit** | If we leave out and it was load-bearing |
| **falsifier** | How we’d know restore succeeded or omit failed |

Prefer Tier A when: high benefit, cost not extreme, risk_if_omit ≥ med, and zero plan is weaker without it **or** gap_to_prior high **and** mission still OK without it (shape/product, not floor).

### 3. Tiers

| Tier | Rule of thumb |
|------|----------------|
| **A suggest restore** | Best re-adds; target rough order **~5–15% of D_prop** count when D_prop ≥ 10; if D_prop small, A can be 0–2 rows without forcing % |
| **B discuss** | Borderline; human must talk |
| **C leave deleted** | Mission true under ZERO_PLAN; convenience/legacy |

If Tier A would exceed ~25% of D_prop, re-score — portfolio is too timid on delete or too eager on restore; note in STATUS.

### 4. Artifacts

```text
notes/zero/<slug>/
  RESTORE_PORTFOLIO.md
  RESTORE_STATUS.md
```

Optional machine rows:

```text
notes/zero/<slug>/restore_portfolio.json
```

See `references/portfolio-schema.md`.

### RESTORE_STATUS.md

```text
slug, D_prop, R_prop, ratio_prop,
human_gate: pending|accepted|amended|parked,
tier_a_ids, next: clone|gap-to-plan|lfg|stop
```

### 5. Metrics append (required when workspace writable)

Append one JSON line to:

```text
notes/elon/metrics/runs.jsonl
```

Create `notes/elon/metrics/` if needed. Schema (one object per line):

```json
{
  "ts": "ISO-8601",
  "slug": "...",
  "scale": "module|system|unknown",
  "thin_target": false,
  "D_prop": 0,
  "R_prop": 0,
  "R_human": null,
  "R_ship": null,
  "ratio_prop": 0.0,
  "ratio_human": null,
  "ratio_ship": null,
  "human_gate": "pending",
  "provisional": true,
  "pack_path": "notes/zero/<slug>/",
  "notes": ""
}
```

When human later accepts a portfolio in-session, **update** by appending a **new** line with same slug + `human_gate: accepted` + `R_human` + `ratio_human` + `provisional: false` (append-only; do not rewrite history).

Load `references/calibration.md`. Read `notes/elon/metrics/calibration_state.json` if present.

### 6. Calibration snapshot

If enough closed runs exist, compute mean `ratio_human` (else provisional mean `ratio_prop`) in window since last adjust.

Apply stage bands from `references/calibration.md`. If outside band → write section **CALIBRATION_HINT** in portfolio or `notes/elon/metrics/LAST_HINT.md` with suggest-modify text only.

Do **not** change skill files.

### 7. Human pack (always stop)

Present:

1. Counts: D_prop, R_prop, ratio_prop  
2. Tier A shortlist (ids + one-liners)  
3. Tier B discuss list  
4. Tier C sample (not full dump if long)  
5. “If you drop A / force C” bullets  
6. Calibration snapshot / hint if any  
7. Options:

```text
A) Accept portfolio as-is (record R_human = tier A, or A+selected B)
B) Discuss specific ids (Q&A; amend tiers; re-write portfolio)
C) Promote/demote rows then accept
D) Hand selected ids → thin plan amend + clone/worktree only
E) Hand selected ids → /gap-to-plan (or /lfg) as restore/expand aim
F) Park — no ship; metrics stay provisional if no R_human
```

Default first runs: **A or B**, not E.

## Relationship

| Skill | Relation |
|-------|----------|
| `/elon2` | Calls this at end of compress; pre-ship fork |
| `/zero` `/req` `/zero2` | Upstream delete candidates |
| `/gap-to-goal` | Different question; re-run if keep-set changes after accept |
| `/gap-to-plan` `/lfg` | Downstream ship for fat restores |
| `/harsh-critic` | Optional on “why these A’s” summary |
| factory-qc / comprehensive-codebase-review | Not substitutes for restore |

## Success criteria

- RESTORE_PORTFOLIO.md with tiers  
- No production edits  
- Metrics line appended when possible  
- Human pack presented  
- No forced 10% gaming  

## Tone

Table-first, cost-aware, slightly biased to **leave deleted** unless benefit clear. Celebrate small Tier A when D_prop was large.
