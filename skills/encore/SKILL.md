---
name: encore
description: >-
  Continue an LFG cycle without re-running deep-research: ship residual gap
  plans (planner + universal-gauntlet, medium critic) for all remaining plans,
  comprehensive-codebase-review, /implement Medium+ fixes, remeasure gap-to-plan,
  then prompt for another encore. Use when the user runs /encore, "encore the
  loop", "continue LFG without research", or after /lfg prompts for encore.
  Do not use for a brand-new aim (use /lfg) or single-phase work (/implement).
metadata:
  short-description: "LFG steps 3-6: ship residual plans -> review -> implement Medium+ -> re-gap -> prompt"
argument-hint: "[--critic medium|harsh] [--max-plans N] [--from-gap path] [--skip-ship]"
---

# /encore - LFG continuation (no deep-research)

You are the **encore orchestrator**. You continue a prior **`/lfg`** run (or an
equivalent gap pack) **without** re-running deep-research unless the user
explicitly asks to research again.

## Defaults

| Setting | Value |
|---------|--------|
| Critic tier | **medium** (same as LFG) |
| Ship mode | **all** residual / next gap plans before review |
| Fixes | **`/implement` Medium+** from review (not freeform implement) |
| Research | **skip** (use existing aim + re-gap) |
| Auto-repeat | **no** - prompt again after re-gap |

## Composition map (LFG steps 3-6)

```text
3. for each remaining / residual plan:
     /planner  +  /universal-gauntlet (factory, medium critic)
4. /comprehensive-codebase-review
5. /implement  Medium+ findings from review
6. /gap-to-plan remeasure
7. prompt user for another /encore or stop
```

**Do not** run `/deep-research` by default.  
**Do not** substitute prose for `/implement` in step 5.

## Preconditions

Load in order:

1. `.lfg/AIM.md` (or user-stated aim if missing - ask once)
2. `.lfg/status.json` if present (`encore_count`, paths)
3. Latest gap pack:
   - `--from-gap <path>`, else
   - `status.gap_dir`, else
   - newest `notes/gap_plans/*/` by mtime
4. `.gauntlet/GOAL.md` if present (resume honesty)

If no aim and no gap pack: **stop** and tell user to run `/lfg <aim>` first.

**Continue-state (req gate):** encore is resume-class, not a new LFG.

- Continue-state means `.lfg/status.json` exists and `stage` is
  `awaiting_encore`, `ship_plans`, `implement_fixes`, or `regap`.
- If continue-state: **do not** run the factory/meta req gate. Continue.
- If **not** continue-state (missing status, or `stage=bootstrap`, or a
  `--from-gap` / stated aim with no prior LFG loop): **STOP**. This is not
  encore. Tell the user `/lfg <aim>` (that skill owns the req gate).
- `stage=bootstrap` is a new LFG, not a continue.

## Workflow

Track:

- [ ] 0. Load aim + gap + status; bump encore_count
- [ ] 1. Choose plans to ship this encore
- [ ] 2. Ship all chosen plans (planner + gauntlet)
- [ ] 3. Comprehensive review
- [ ] 4. `/implement` Medium+
- [ ] 5. Re-gap + prompt

### 0. Bootstrap encore

1. Read AIM + status; set `stage=ship_plans`, increment `encore_count`.
2. Critic tier from `--critic` or status or **medium**.
3. Write a short line to `.gauntlet/GOAL.md` or `.lfg/status.json`: encore N started.

### 1. Select plans

From gap `plans/README.md` and residual re-gap:

| Case | Action |
|------|--------|
| Deferred plans not yet shipped | Ship next unshipped `plan_0K` series (cap max_plans) |
| All prior plans accepted; residual gap has new plans | `/gap-to-plan` already ran in last LFG/encore - use **that** pack’s plans |
| Only maintenance Medium+ left | `--skip-ship` or empty plan list -> jump to review |

Prefer **not** re-shipping plans already in `status.plans_accepted` unless re-gap
marks them incomplete.

### 2. Ship all selected plans

Same as LFG step 3:

For each plan:

1. **`/planner`** - promote plan, archive prior slug, phase-1 tasks only.
2. **`/universal-gauntlet`** - factory mode, critic medium/harsh, all phases +
   integration ACCEPT before next plan.

Load skills from:

- `~/.grok/skills/planner/SKILL.md`
- `~/.grok/skills/universal-gauntlet/SKILL.md`

Critic tiers: `~/.grok/skills/lfg/references/critic-tiers.md` (shared).

### 3. Comprehensive codebase review

Load **`/comprehensive-codebase-review`**. Scope to aim-touched areas + recent
ship. Write `docs/comprehensive-review-<date>.md` or `.lfg/review-<stamp>.md`.

### 4. `/implement` Medium+

1. Load **`/implement`** (`~/.grok/bundled/skills/implement/SKILL.md`).
2. Brief = Critical/High/Medium from review, max 15 items.
3. Run implement skill fully; then tests/smoke.

### 5. Re-gap + prompt

1. **`/gap-to-plan`** with original aim + post-encore disk.
2. Update status: `stage=awaiting_encore`, paths.
3. **Stop** and prompt:

```text
Encore N complete.

Aim: …
Plans this encore: …
Review: …
Medium+ implement: …
Residual gap: … (severities)

Next:
  /encore     - again (still no deep-research by default)
  /lfg <aim>  - new aim + research
  stop
```

Cap soft warning if `encore_count >= 3`: suggest stopping or new research if
residuals are external/unknown.

## Anti-patterns

- Re-running deep-research without user ask
- Auto-chaining encore without prompt
- Review before shipping selected plans (unless skip-ship)
- Prose implement instead of `/implement`
- Re-doing accepted plans without residual gap reason
- Using `/encore` as a new factory ship to skip the LFG req gate
- Applying the LFG req gate on a real continue (resume-class)

## Success criteria

- Residual plans shipped (or skip-ship justified)
- Review + `/implement` Medium+ (or zero findings)
- Re-gap on disk
- User prompted (not auto-encore)

## Related

| Skill | Role |
|-------|------|
| `/lfg` | Full cycle including research; factory/meta req gate lives there |
| `/req` `/elon1` | New factory aim — via `/lfg`, not encore |
| `/gap-to-plan` | Residual measurement |
| `/planner` + `/universal-gauntlet` | Ship |
| `/comprehensive-codebase-review` | Audit |
| `/implement` | Medium+ fixes |

## References

- Shared critic tiers: `../lfg/references/critic-tiers.md` or copy below
- `references/composition.md`
