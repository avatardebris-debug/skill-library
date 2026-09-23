---
name: after-series-qc
description: >-
  Post series-loop measure pack: morning receipts, factory-qc (pre-merge),
  factory-qc-handoff, then STOP (default) or --auto soft (findings-triage packs
  only when Medium+=0 and low residual large; never auto-implement / gauntlet /
  series resume). Use when /after-series-qc, "after series-loop", "post overnight
  series QC", or series-loop final summary. Factory health ≠ field_proven. Do not
  use for series-loop itself, product field-test, or visual canary loops.
metadata:
  short-description: "After series-loop: morning + factory-qc + handoff (+ optional soft triage)"
argument-hint: "[--repo-root PATH] [--profile pre-merge|deep-audit] [--skip-morning] [--auto report|soft]"
---

# /after-series-qc — Post series-loop QC orchestrator

You are a **thin orchestrator**. You load child skills / CLIs in order, write a
short durable summary, and either **STOP for human choice** (`--auto report`,
default) or run **soft triage only** (`--auto soft`). You do **not** implement
product code, flip Gate ACCEPT, claim field_proven, auto-encore, auto-gauntlet,
or auto `/series-loop --resume`.

Frozen playlist: `references/contract.md`. Prefer the contract over improvising.

## Defaults

| Setting | Value |
|---------|--------|
| `--auto` | **report** |
| Profile | **pre-merge** (`deep-audit` only if user asks or multi-leaf night) |
| Morning pack | **on** (skip with `--skip-morning`) |
| Auto findings-triage | **only** when `--auto soft` and soft rules match |
| Auto implement | **never** (even in soft) |
| Auto series-loop resume | **never** |
| field_proven / Gate ACCEPT | **never** flip |
| Visual ACCEPT | **never** invent |
| Soft low threshold | **20** (same as factory-qc-handoff default) |

## Modes

### `--auto report` (default)

```text
0. resolve repo root + series-loop status
1. /morning-ops-pack   # or thin .series-loop morning
2. /factory-qc
3. /factory-qc-handoff
4. write .after-series-qc/summary.md
5. STOP — wait for user
```

### `--auto soft`

Same through handoff, then:

```text
5a. If Medium+ > 0: do NOT triage; note "Medium+ needs human / implement"; STOP
5b. If Medium+ = 0 and low >= threshold: run /findings-triage once; write packs; STOP
5c. Else: STOP (nothing to triage)
5d. NEVER /implement, /gap-to-plan, /lfg, /encore, /universal-gauntlet, series resume
```

Soft exists to shrink the morning pile into bounded packs. Ship still needs a human.

## Soft branches after handoff (report mode = user must ask)

| Handoff | report | soft |
|---------|--------|------|
| Medium+ > 0 | user: implement or gap-to-plan | print only; STOP |
| Medium+=0 & low large | user: findings-triage | **auto** findings-triage; STOP |
| Plant leaf needs eyes | suggest human visual | suggest only; STOP |
| Clean | stop | stop |

## Child skills (load; do not copy bodies)

| Step | Path / skill |
|------|----------------|
| morning | `~/.grok/skills/morning-ops-pack/SKILL.md` |
| factory QC | `~/.grok/skills/factory-qc/SKILL.md` (+ qc-* leaves) |
| handoff | `~/.grok/skills/factory-qc-handoff/SKILL.md` |
| triage | `~/.grok/skills/findings-triage/SKILL.md` |

If QC skills are **missing**, stop after morning/status and tell the operator to
install from `avatardebris-debug/skill-library`. Do **not** fake a QC report.

## Inputs

| Input | Default | Notes |
|-------|---------|--------|
| `--repo-root` | cwd with `notes/series/` or `.series-loop/` | Factory checkout |
| `--profile` | `pre-merge` | `deep-audit` = heavier |
| `--skip-morning` | off | Morning already ran |
| `--auto` | `report` | `soft` = triage packs only under rules |

## Durable state

```text
.after-series-qc/
  summary.md
  last_stamp.txt
  last_triage.txt    # notes/triage/<stamp> if soft triage ran
```

## Workflow

### 0. Bootstrap

1. Resolve repo root.
2. Read `.series-loop/status.json` if present.
3. Parse `--auto` (`report`|`soft`). Unknown → treat as `report` and warn.
4. Announce: `after-series-qc root=… profile=… auto=… morning=on|off`.

### 1. Morning receipts

Load `/morning-ops-pack` when applicable.

**Series-loop adaptation:** if classic overnight logs absent but `.series-loop/`
exists, thin morning: status + `leaves/*/summary.md` one-liners + non-claim line
+ human stubs from `stop_reason`.

### 2. factory-qc

```powershell
python .grok/skills/factory-qc/scripts/run_factory_qc.py --repo-root . --profile pre-merge
```

### 3. factory-qc-handoff

```powershell
python .grok/skills/factory-qc-handoff/scripts/print_handoff.py --repo-root .
```

Capture Medium+ and low counts from handoff output / findings.

### 4. Soft triage (only `--auto soft`)

1. If findings-triage skill/script missing → note install; skip; go to summary.
2. If Medium+ > 0 → skip triage; `soft_skipped=medium_plus`.
3. If low < threshold → skip; `soft_skipped=low_below_threshold`.
4. Else run:

```powershell
python .grok/skills/findings-triage/scripts/run_findings_triage.py --repo-root . --stamp <id>
```

5. Record triage out path. **Do not** implement packs.

### 5. Summary + STOP

Write `.after-series-qc/summary.md` including `auto=` mode, qc stamp, triage
path or skip reason, non-claim, and choose-ONE menu (implement / triage if
report / human visual / series-loop later / stop).

Then **stop**.

## Forbidden

- Auto `/implement`, `/gap-to-plan`, `/lfg`, `/encore`, `/universal-gauntlet`
- Auto `/series-loop --resume`
- Soft mode running triage when Medium+ > 0
- Visual or Gate ACCEPT from stills / QC green
- Inventing QC when skills missing

## Non-claims

| Artifact | Is NOT |
|----------|--------|
| series-loop complete | Series done / field_proven |
| factory-qc green | Gate ACCEPT |
| soft triage packs | Permission to ship |
| handoff text | Auto-implement license |

## Related

| Skill | Role |
|-------|------|
| `/series-loop` | Before this |
| `/overnight-series` | Playlist that may call this with `--auto soft` |
| `/findings-triage` | Soft may run once |
| `/aim-to-series` | Bootstrap; not this |

## Success criteria

- [ ] Status read (or honest none)
- [ ] Morning or thin morning (unless skipped)
- [ ] QC stamp or missing-skill report
- [ ] Handoff printed
- [ ] Soft: triage ran or honest skip reason
- [ ] summary.md written; agent stopped; no implement auto-started

## References

- `references/contract.md`
