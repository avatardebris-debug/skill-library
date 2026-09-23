# after-series-qc contract

## One-liner

```text
/series-loop → /after-series-qc [--auto report|soft]
  → morning → /factory-qc → /factory-qc-handoff
  → [soft: findings-triage if Medium+=0 & low≥20]
  → STOP
```

## Hard rules

1. Default is **report** (stop after handoff).
2. **soft** may write triage packs only; never implement / gauntlet / resume.
3. Medium+ always human (or explicit later ask) — soft does not ship them.
4. Factory health ≠ field_proven ≠ Gate ACCEPT.
5. Missing QC skills → install note; no fake findings.
6. Visual / Meshy / plant ACCEPT out of band.

## Soft eligibility

| Condition | Action |
|-----------|--------|
| `--auto report` | Never auto triage |
| Medium+ > 0 | Never auto triage |
| low < 20 | Skip triage |
| Medium+=0 & low≥20 & scripts present | Run findings-triage once |
