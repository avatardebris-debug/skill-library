# RESTORE_PORTFOLIO.md schema

## Header

```markdown
# Restore portfolio — <slug>

## Mission
...

## Pack sources
- REQUIREMENTS: path
- CONCEPTS pruned: path
- ADJUSTMENT_CANDIDATES: path (optional)
- GOAL_GAPS: path (optional)

## Counts
- D_prop (propose_delete / pruned): N
- R_prop (tier A+B suggest): N
- ratio_prop: x.xx
- load_bearing D / R: …
```

## Row table

| id | from | statement | tier | gap_to_prior | benefit | cost | risk_if_wrong | risk_if_omit | falsifier | related_ids | human |
|----|------|-----------|------|--------------|---------|------|---------------|--------------|-----------|-------------|-------|
| rest_1 | R3 / C_pruned / z2_… | … | A\|B\|C | high\|med\|low | 1–5 | 1–5 | … | … | … | R3,C2 | pending |

### tier

| Tier | Meaning |
|------|---------|
| **A** | Suggest restore (~aim small fraction of deletes; not 50%) |
| **B** | Discuss only — human judgment |
| **C** | Leave deleted; mission still true under zero plan |

### gap_to_prior

How far product/shape drifts from prior if **not** restored: high = big shape change.

### benefit / cost

Integer 1–5. Prefer restore when benefit−cost high and risk_if_omit high.

## Sections

```markdown
## Tier A — suggest restore
...

## Tier B — discuss
...

## Tier C — leave deleted
...

## If you drop a Tier A
- consequences per id

## If you force-restore a Tier C
- complexity / dual-system risks

## Calibration snapshot
- ratio_prop, stage band if metrics loaded
```
