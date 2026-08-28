---
name: elon2
description: >-
  After-the-fact compress (Elon2): make requirements less dumb (/req),
  delete (/zero), simplify/map (/zero2, optional zero-cross), human add-back
  (/restore), then accelerate via clone or gap-to-plan/LFG/gauntlet, optional
  factory-qc and comprehensive-codebase-review bookends, automate last.
  Early blast-radius + plain-language completion pack before accept.
  Playlist of existing skills — no live delete, no auto-LFG. Use when /elon2,
  formerly /elon, Elon 5-step compress, delete-then-restore, or reconstruct
  something that already got too big. Not how new work should start (Elon1
  culture: notes/ops/operator_method.md).
metadata:
  short-description: "Elon2 compress: req→zero→zero2→restore→ship"
argument-hint: "[target] [--scale module|package|system] [--slug name] [--no-qc] [--no-cross]"
---

# /elon2 — After-the-fact compress (orchestrator)

Formerly `/elon`. Same playlist. This is **Elon2**: compress a target that
already grew too expensive. New work uses **`/elon1`** (define → tightness → smallest patch). Culture card:
`notes/ops/operator_method.md`. Not this skill.

You run the **five-step algorithm** by **calling existing skills**. You do not
reimplement Occam, filters, gauntlet, or LFG inside this file.

## The five steps → skills

| # | Elon step | Skill(s) |
|---|-----------|----------|
| 1 | Make requirements less dumb | **`/req`** |
| 2 | Delete | **`/zero`** (concepts/plan only; includes `/gap-to-goal` + `/harsh-critic`) |
| 3 | Simplify / optimize | **`/zero2`** module; optional **zero-cross** profile |
| 4 | Accelerate cycle | Human-approved **clone** implement **or** `/gap-to-plan` + planner + universal-gauntlet **or** `/lfg` / `/encore` |
| 5 | Automate | **Last**, only if 1–4 are stable and human asks — scripts/qc leaves, not sooner |

**Mandatory human fork:** **`/restore`** after compress (end of 2–3) and **before** ship (4).

**Mandatory planning safety (before any accept):** early **blast-radius / risks**
(`references/risks.md`) and a **plain-language completion pack**
(`references/completion-pack.md`) at compress end.

## When to use

- Full compress → weigh-in → optional reconstruct on a **target that already exists and is too big**  
- “Run Elon2 / compress playlist on X” (old `/elon` means this)  
- Practice elite deletion/reconstruction with metrics  

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Requirements only | `/req` |
| Score Ted digests / research fuel admission | **`/admit-fuel`** (not elon2) |
| Expand a new product aim with research | `/admit-fuel` then `/suggest` then `/lfg` (Elon1 culture first: `/req`) |
| New smallest-sufficient automation | **`/elon1`** — not this compress playlist |
| Factory health only | `/factory-qc` |
| Multiyear series cut | `/slice-deconstruct` first, then elon2 per leaf |
| Live cutover without human | **Forbidden** |

## Hard safety (non-negotiable)

1. **Never** live-delete or rewrite production as part of elon2.  
2. **Never** auto-LFG / invent proof crowns / auto-compress true.  
3. **Stop** at every human pack in child skills (`/zero`, `/restore`, ship branch).  
4. zero-cross only with **caps** (see zero2); default **module** scale.  
5. Do not force restore ratio to 10% for metrics.  
6. Factory “never” language is binding unless human waives a specific line in writing this session.  
7. **Do not** ask the human to accept a plan without (a) `BLAST_RADIUS.md` and (b) plain-language risks + questions in the completion pack.  
8. High/block coupling risks need **named mitigations** (façade, freeze tests, leave deleted, clone-only) before letter options.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| **Target** | Yes | Path, module, subsystem, or named surface |
| **Scale** | No | `module` (default) \| `package` \| `system` — `references/scale-routing.md` |
| **Slug** | No | Default from target |
| **Mission hint** | No | Passed to zero/req |
| **Flags** | No | `--no-qc`, `--no-cross`, `--restore-only`, `--zero-only` |

## Workflow

Load `references/playlist.md`. Track:

- [ ] 0. Optional measure bookend + **scale routing** + **blast-radius seed**  
- [ ] 1. `/req` (compress mode)  
- [ ] 2. `/zero` + human conceptual gate  
- [ ] 3. `/zero2` module + refresh BLAST_RADIUS  
- [ ] 4. Optional zero-cross  
- [ ] 5. `/restore` + human portfolio gate  
- [ ] 5b. **Completion pack** — **always stop**  
- [ ] 6. Ship branch (only if human)  
- [ ] 7. Optional remeasure  
- [ ] 8. Automate? (only if human)  
- [ ] 9. Write ELON_STATUS + metrics summary  

### 0. Bookend in + scale + early risks

If not `--no-qc` and target is factory-ish or user wants health context:

- Run **factory-qc** if available in project (measure-only; handoff aims only)  
- Or note “skip qc — product module focus”  

If surface is large and mission unknown, optional **comprehensive-codebase-review** (read-only inventory). Do **not** let review dictate Occam; mission still comes from `/zero` step 1.

**Scale routing:** load `references/scale-routing.md`.

- Single file → `module`  
- Small folder → `module`/`package`  
- Multi-package subsystem → `system` → allow zero-cross with caps  
- Whole worktree / multiyear → **slice-deconstruct** or multi-elon2; do not one-shot  

**Blast-radius seed:** as soon as target paths are known, start `notes/zero/<slug>/BLAST_RADIUS.md` per `references/risks.md` (importers/callers). Capture “who points at this” **before** Occam.

### 1. `/req`

Load project or `~/.grok/skills/req/SKILL.md`. Out dir: `notes/zero/<slug>/`. **Compress mode.**

When rows are `propose_delete` or `challenge`, add a one-line risk note into BLAST_RADIUS.

### 2. `/zero`

Load `~/.grok/skills/zero/SKILL.md`. Same slug/pack. Includes gap-to-goal + harsh.

For each `propose_remove` / pruned concept, ensure BLAST_RADIUS has a row (even if risk=low).

**Stop** for zero human pack if running zero-only or human must resolve challenges first.  
On full elon2, you may continue to zero2/restore and present **one combined** completion pack — still must not ship without human letters.

If human rejects/parks early → write ELON_STATUS and exit.

### 3. `/zero2` module

Load `~/.grok/skills/zero2/SKILL.md`, profile **module**, scope = target paths.

**Required:**

- **Outside-twin look** — bounded grep *outside* the target for twin helpers / already-shared utils. If `zero2/references/peer-scan.md` exists, follow it (F8). Else write twins/importers into BLAST_RADIUS.  
- **Partition** — merge-vs-split so F3 and F4 do not fight (`references/scale-routing.md`).  
- **F7 + blast radius** refresh. Every high/med `propose_*` gets a risk row and a **mitigation before accept**.

### 4. Optional zero-cross

Only if:

- `scale=system` **or** user asked cross, **and**  
- not `--no-cross`, **and**  
- ≥2 packages / meaningful multi-dir surface  

Then `/zero2` profile **zero-cross** with path caps. Not a separate skill.

### 5. `/restore`

Load `~/.grok/skills/restore/SKILL.md`. **Always** for full elon2 (unless `--zero-only`).

Score tiers with residual risks from BLAST_RADIUS in mind (do not Tier-A restore junk that reintroduces high risk without benefit).

**Stop** for restore human pack. Record metrics per restore skill + `references/metrics.md`.

### 5b. Completion pack (mandatory)

Load `references/completion-pack.md` and **print** to the user:

1. Bottom line (live code untouched)  
2. Changes if accepted (plain English)  
3. Risks + blast radius  
4. Questions the human should answer  
5. Zero + restore letter options + suggested thin path  
6. Metrics + artifact index  
7. Explicit **stop** — no ship  

This is the **primary** human-facing close. Deep md files support it; they do not replace it.

### 6. Ship branch (human only)

| Human choice | Action |
|--------------|--------|
| Map/portfolio only | Stop; no implement |
| Thin restore ids | Clone/worktree implement of **selected ids only**; re-run `/gap-to-goal` if keep-set changed; optional harsh on implement plan; honor façade mitigations from BLAST_RADIUS |
| Fat restore / multi-part | `/gap-to-plan` with aim from selected restore ids (“gap-to-feature” mode: aim = restore these) → then planner + universal-gauntlet **or** hand to `/lfg` if research+full outer loop needed |
| New mission expand | `/lfg` / `/suggest` — not forced from elon2 |

### 7. Optional remeasure (bookend out)

After any clone ship: optional factory-qc and/or comprehensive-codebase-review. Report only.

### 8. Automate (Elon 5)

Only if human explicitly wants automation **and** steps 1–4 produced a boring, repeatable pattern: propose scripts or qc leaves — do not automate delete/restore judgment or risk accept.

### 9. ELON_STATUS.md

Write:

```text
notes/zero/<slug>/ELON_STATUS.md
# or notes/elon/<slug>/ELON_STATUS.md if no zero pack yet
```

```markdown
# Elon status — <slug>

## Steps completed
- …

## Scale
- flag: module|package|system
- zero2 profile: module | module+zero-cross

## Human gates
- zero: …
- restore: …

## Risks
- BLAST_RADIUS.md: present
- top residual: …
- mitigations named: yes|no

## Metrics
- D_prop, R_prop, ratio_prop, R_human if any
- calibration: in_band | hint (summary)

## Next
- stop | clone ids | gap-to-plan | lfg | encore

## Safety
- live_delete: false
- auto_lfg: false
```

## Multiyear / series

If target is a multi-year series or huge monorepo rewrite:

1. Tell user: run **`slice-deconstruct`** (or series tree) first.  
2. `/elon2` per **gap_ready** leaf — not one unbounded elon2.  
3. `/factory-improve` or `/suggest` may choose which leaf is next.

## Calibration

See `~/.grok/skills/restore/references/calibration.md` and `references/metrics.md`.

On full elon2 end: ensure restore appended `runs.jsonl`; surface any CALIBRATION_HINT to the human in the final summary.

## Relationship

| Skill | Role in elon2 |
|-------|----------------|
| `/req` | Step 1 (compress mode) |
| `/zero` | Step 2 |
| `/zero2` | Step 3 (+ optional cross); F7 feeds blast radius |
| `/restore` | Post-compress / pre-ship |
| `references/risks.md` | Early BLAST_RADIUS |
| `references/completion-pack.md` | Plain-language close |
| `references/scale-routing.md` | module vs folder vs system |
| `/gap-to-goal` `/harsh-critic` | Inside zero; re-check after restore accept if needed |
| `/gap-to-plan` planner gauntlet `/lfg` | Step 4 ship |
| factory-qc comprehensive-codebase-review | Bookends |
| slice-deconstruct | Before elon2 at series scale |
| `/admit-fuel` | Research intake scoring (before ship pressure; complementary phase) |
| `/suggest` | After park: next aim |

## Success criteria

- Child skills invoked (not reinvented)  
- Human gates respected  
- `/restore` run on full elon2  
- **BLAST_RADIUS.md** written and refreshed before accept  
- **Completion pack** printed in plain English (risks + questions)  
- Production unmodified by elon2 itself  
- Metrics path used when restore runs  
- Clear NEXT handoff  
- Scale/profile chosen deliberately (not silent whole-repo)  

## Tone

Ruthless about complexity, humble about cutover. Prefer small targets until the playlist is muscle memory. Capture risk early; speak plainly at the end.
