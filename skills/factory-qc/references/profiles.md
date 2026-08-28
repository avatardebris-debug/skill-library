# factory-qc profiles

## pre-merge (fast / default)

| Order | Leaf | Script args notes |
|------:|------|-------------------|
| 1 | qc-static | default |
| 2 | qc-contracts | default |
| 3 | qc-honesty | default (pipeline/) — may be large |
| 4 | qc-errors | default |
| 5 | qc-tests | `--skip-smoke` for speed |
| 6 | qc-security | default |
| 7 | qc-runtime-control | overnight stall proxies (dead-role / thrash / false-MVP) |

**Not included:** qc-coupling-debt, qc-temporal (deep-audit only)

## deep-audit

All **pre-merge** leaves, plus:

| Order | Leaf | Notes |
|------:|------|-------|
| 8 | qc-coupling-debt | LOC residual |
| 9 | qc-temporal | git-history observation; top-N; not pre-merge |
| — | CCR (delegate) | Finding only: run `/comprehensive-codebase-review` separately; do **not** reimplement |

qc-tests in deep-audit may omit `--skip-smoke` if `--full-smoke` flag set (default still skip for time).

## Failure policy

- Leaf script missing → `control_gap` finding (info), continue  
- Leaf non-zero exit → finding high + still try to read partial JSON if written  
- Always write stamp REPORT even if some leaves fail  

## Forbidden (meta never does)

- `/gap-to-plan`, `/universal-gauntlet`, `/implement`, `/lfg`, auto-encore  
- Setting field_proven / product dual-gate crowns  
