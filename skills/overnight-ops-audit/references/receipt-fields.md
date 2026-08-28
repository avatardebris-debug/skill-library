# Overnight receipt fields (v0)

## Directory

`{PIPELINE_DIR}/logs/overnight_{YYYYMMDD}_{HHMMSS}/`

## Core files

| File | Parse |
|------|--------|
| preflight.json | time_limit_min, factory_root, warnings |
| runner.log | start, end, exit= |
| runner.out.log | STALL, Health check, Seeded, complete, **`[reseed]`** |
| runner.err.log | Traceback, soft_log_exc NameError |
| morning_rows.json | slugs + status |
| seed_hygiene.log | traps / seedable |

## Reseed soak (`[reseed]`)

Emitted by `pipeline.run_loop_seed_idle` after terminal post-complete or empty-queue idle:

| Line | Meaning |
|------|---------|
| `[reseed] seeded next idea (post-complete status=… slug=…)` | greenfield after terminal project |
| `[reseed] seeded next idea (empty-queue idle)` | greenfield when bus idle + from_list |
| `[reseed] no free seed slots (parallel=N) — …` | capacity gate blocked seed |

CLI: `python -m pipeline.reseed_soak_receipt --overnight-dir <dir>`  
Schema: `reseed_soak_receipt.v0` — **≠ field_proven**. Zero lines ⇒ `no_reseed_lines` (not a pass).

## Finding classes

stall · auto_fix_thrash · soft_log_crash · exit · side_effect · dead_role_bus · engine_fallback · **reseed_soak** · clean
