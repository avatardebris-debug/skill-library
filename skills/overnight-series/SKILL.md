---
name: overnight-series
description: >-
  Unattended playlist: one or more /series-loop waves, each followed by
  /after-series-qc, with hard caps and stop rules. Use when /overnight-series,
  "overnight series playlist", "multi series-loop night", or "run series then
  QC until cap". Not aim bootstrap (/aim-to-series), not auto-gauntlet, not
  empty-ROADMAP invent. Factory/ship surplus ceilings apply; never field_proven.
metadata:
  short-description: "Playlist: series-loop waves + after-series-qc with caps"
argument-hint: "[--series SLUG] [--waves N] [--leaves N] [--mode thin|lfg] [--qc-auto report|soft] [--effort N]"
---

# /overnight-series — Series-loop + after-series-qc playlist

You are a **playlist orchestrator**. You call `/series-loop` and
`/after-series-qc` in order under ceilings. You do **not** implement product
code, invent series packs, run universal-gauntlet, or flip field_proven.

Contract: `references/contract.md`.

## Defaults (ceilings)

| Setting | Default | Hard max |
|---------|---------|----------|
| `--waves` | 1 | **3** |
| `--leaves` per wave | 1 | **2** (forwarded; series-loop max 3 but playlist keeps ≤2) |
| `--mode` | thin | thin\|lfg |
| `--qc-auto` | **soft** | report\|soft |
| `--effort` | 1 | forwarded to series-loop |
| Auto gauntlet / encore / suggest | **never** | — |
| Empty ROADMAP invent | **never** | hand off to `/aim-to-series` |
| field_proven | **never** | — |

## Composition map

```text
0. bootstrap + resolve series
1. for wave = 1 .. waves:
     a. /series-loop --series … --leaves L --mode … --effort …
     b. /after-series-qc --skip-morning (wave>1) --auto qc-auto
     c. apply STOP rules → break or continue
2. final overnight summary (always)
3. STOP — no chained aim-to-series / gauntlet / autosuggest
```

## STOP rules (check after each after-series-qc)

Stop the playlist immediately if any:

| Signal | `stop_reason` |
|--------|----------------|
| series-loop `implement_failed` | `implement_failed` |
| series-loop `still_series` on the only candidate | `still_series` |
| series-loop `no_leaf` | `no_leaf` |
| QC / handoff reports **critical** or **high** Medium+ (or Critical/High counts > 0) | `qc_medium_plus` |
| after-series-qc missing factory-qc skills | `qc_skills_missing` |
| wave cap reached | `waves_complete` |
| operator interrupt / skill error | `error` |

On `no_leaf` with empty usable ROADMAP: print
`next: /aim-to-series "<product aim>"` — **do not** invent leaves overnight.

## Child skills

| Step | Skill |
|------|--------|
| leaf ship | `~/.grok/skills/series-loop/SKILL.md` |
| post QC | `~/.grok/skills/after-series-qc/SKILL.md` |

Load them fully. Do not prose-substitute implement.

## Inputs

| Input | Default | Notes |
|-------|---------|--------|
| `--series` | series-loop default resolution | Pack slug |
| `--waves` | 1 | Cap 3 |
| `--leaves` | 1 | Cap 2 in this playlist |
| `--mode` | thin | Forwarded |
| `--qc-auto` | soft | Forwarded to after-series-qc |
| `--effort` | 1 | Forwarded |
| `--resume` | off | If set, first wave uses series-loop `--resume` |

## Durable state

```text
.overnight-series/
  status.json     # wave, stop_reason, per-wave pointers
  summary.md      # final brief
```

`status.json` minimal fields: `series`, `waves_target`, `waves_done`,
`leaves_per_wave`, `qc_auto`, `stop_reason`, `waves[]` with
`series_loop_stop`, `qc_stamp`, `triage_path`, `soft_skip`.

Write status after every wave.

## Workflow

### 0. Bootstrap

1. Factory root with `notes/series/` (or explicit `--series` path context).
2. Confirm `series-loop` and `after-series-qc` skills exist; else STOP
   `skills_missing`.
3. Clamp waves ≤3, leaves ≤2.
4. Init `.overnight-series/status.json`.
5. Announce caps.

### 1. Wave loop

For each wave:

1. Load `/series-loop` with args (add `--resume` only on wave 1 if requested).
2. Read `.series-loop/status.json` → record `stop_reason`.
3. If STOP rule hits before QC → write summary; exit.
4. Load `/after-series-qc` with `--repo-root . --auto <qc-auto>` and
   `--skip-morning` when `wave > 1` (wave 1 runs morning unless user said skip).
5. Read `.after-series-qc/summary.md` / stamps; apply QC stop rules.
6. Append wave record; continue or break.

### 2. Final summary

```markdown
## overnight-series complete

- series, waves_done / waves_target, leaves_per_wave, qc_auto
- stop_reason
- per wave: series-loop stop, qc stamp, triage path or skip
- non-claim: no field_proven; soft packs ≠ ship
- next: morning eyes | /implement from triage or REPORT | /aim-to-series if no_leaf | stop
```

## Forbidden

- Calling `/universal-gauntlet`, `/encore`, `/autosuggest`, `/lfg` as outer loop
- Inventing ROADMAP leaves when empty
- Auto `/implement` (after-series soft must not either)
- Raising leaves/waves above hard max via "just one more"
- Claiming series or product proven

## Related

| Skill | Role |
|-------|------|
| `/series-loop` | One wave inner ship |
| `/after-series-qc` | Per-wave measure (+ soft triage) |
| `/aim-to-series` | When ROADMAP empty — human-gated bootstrap |
| `/morning-ops-pack` | Optional next morning re-brief |

## Success criteria

- [ ] status.json has stop_reason
- [ ] Each completed wave has series-loop + after-series-qc attempt (or honest early stop)
- [ ] Caps respected
- [ ] No gauntlet / invent / field_proven
- [ ] Final summary for morning

## References

- `references/contract.md`
