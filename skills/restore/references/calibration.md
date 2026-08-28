# Restore-ratio calibration (observational)

**Purpose:** Over many compress cycles, measure how much is proposed (and later actually) added back after delete. If the average sits outside a band that **tightens with N**, suggest modifying `/req` challenge strength, `/zero` Occam depth, or restore scoring — **never** auto-edit production or auto-delete more.

**Not a quota.** Do not force a run to hit 10%. Report and suggest only.

## Definitions

| Symbol | Meaning |
|--------|---------|
| `D_prop` | Count of requirement/concept rows marked `propose_delete` / pruned (same pack) |
| `R_prop` | Count of rows in restore portfolio Tier A + Tier B **suggested** restore (or human-facing “suggest restore”) |
| `R_human` | Count human **accepted** for restore this run (`human_restore_accept`) |
| `R_ship` | Count actually planned/shipped back later (`actual_restore`, when known) |
| `ratio_prop` | `R_prop / max(D_prop, 1)` |
| `ratio_human` | `R_human / max(D_prop, 1)` |
| `ratio_ship` | `R_ship / max(D_prop, 1)` when ship outcomes logged |

**Primary calibration series (default):** `ratio_human` when human closed the restore gate; else `ratio_prop` for incomplete runs (label `provisional`).

**Load-bearing variant (optional second series):** same ratios using only `load_bearing: yes` rows — report both if N allows.

## Early bias

Early program (first ~10 closed human gates): slight **delete bias** is OK — expect ratios often toward the **low** side of the band. Do **not** panic-widen delete on first low samples. Prefer “need more N” until the stage-10 band fires.

Over time, move toward a **normal band around ~10%** (Elon-style “add ~10% back if you deleted enough”), with tightening width.

## Stage bands (suggest modify if mean outside)

Use **closed human-gate runs only** for `ratio_human` mean, unless N_closed < 5 — then use `ratio_prop` and mark `provisional: true`.

| Stage | N (closed runs in window) | Lower if mean **&lt;** | Upper if mean **&gt;** | Note |
|-------|---------------------------|------------------------|------------------------|------|
| **S10** | ≥ 10 | 3% | 25% | Wide; early delete bias OK |
| **S25** | ≥ 25 | 5% | 20% | |
| **S50** | ≥ 50 | 7% | 13% | Near long-run center |
| **S100** | ≥ 100 **since last_calibration_adjust** | 8% (10%−2) | 12% (10%+2) | Target **10% ± 2%** |

**Window:** default all runs in `notes/elon/metrics/runs.jsonl` since `last_calibration_adjust_at` (or forever if never adjusted). Optional: last 100 runs if ledger grows huge.

**Which stage applies:** use the **strictest stage whose N threshold is met**. Example: N=30 → S25 band (5–20%), not S10.

## Suggest-modify actions (text only)

If mean outside band, write `CALIBRATION_HINT` with **one** primary hypothesis:

| Symptom | Likely lever |
|---------|----------------|
| Mean **too low** (under-restore / over-delete of needed stuff, or timid restore scorer) | Soften restore cost barrier; re-check gap-to-goal silent drops; `/req` may be over-`propose_delete` on real needs |
| Mean **too high** (add-back flood) | Stronger `/req` challenge; deeper `/zero` Occam; restore Tier A too generous; mission muddy |
| High variance (std high, mean OK) | Inconsistent targets (mix module vs system); split series by `scale` tag |

Never auto-change skill files. Human decides calibration adjust; then set `last_calibration_adjust_at` + note in `calibration_state.json`.

## After a calibration adjust

1. Human notes what changed (req wording, zero depth, restore tier rules).  
2. Update `notes/elon/metrics/calibration_state.json`: `last_calibration_adjust_at`, `adjust_reason`, `runs_since_adjust: 0`.  
3. S100 clock resets (N since adjust).  
4. Do not re-fire S10 panic on the first 3 runs after adjust.

## Std-dev (optional after N≥25)

If sample std of `ratio_human` **> 0.15** (15 points) while mean in band → note “process unstable / mixed scales”; suggest tagging runs `scale: module|system` and separate means.

## Anti-patterns

- Forcing this run’s portfolio to 10% to “fix the metric”  
- Using only `D_prop=0` packs (already-minimal targets) in the mean without flagging `thin_target: true`  
- Claiming field_proven from calibration  
