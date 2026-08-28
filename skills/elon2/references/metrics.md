# Elon metrics ledger

## Paths (workspace)

```text
notes/elon/metrics/
  runs.jsonl                 # append-only run records
  calibration_state.json     # last adjust + policy notes
  LAST_HINT.md               # latest suggest-modify (optional)
  README.md                  # one-screen how to read
```

## runs.jsonl

One JSON object per line. Fields: see `/restore` skill. Elon may also log:

```json
{
  "event": "elon_cycle",
  "ts": "...",
  "slug": "...",
  "steps_completed": ["req","zero","zero2","restore"],
  "zero_cross": false,
  "human_zero": "approved_conceptual|...",
  "human_restore": "pending|accepted|...",
  "D_prop": 0,
  "R_prop": 0,
  "R_human": null,
  "ratio_prop": null,
  "ratio_human": null
}
```

Prefer **one restore metrics line** (from `/restore`) as source of truth for ratios; elon_cycle line is optional summary.

## calibration_state.json

```json
{
  "target_restore_ratio": 0.10,
  "last_calibration_adjust_at": null,
  "adjust_reason": null,
  "runs_since_adjust": 0,
  "early_delete_bias_ok": true,
  "notes": "Bands: see restore/references/calibration.md"
}
```

When human adjusts process (req/zero/restore rules), set `last_calibration_adjust_at` and reset `runs_since_adjust`.

## Aggregation (agent does on restore/elon end)

1. Read all lines since `last_calibration_adjust_at` (or all).  
2. Prefer closed `human_gate: accepted` with non-null `ratio_human`.  
3. Mean, optional std, N.  
4. Apply stage bands (S10 / S25 / S50 / S100).  
5. If outside → CALIBRATION_HINT only.

No automatic skill edits.
