---
name: qc-temporal
description: >-
  Factory self-QC leaf: git history as observation that direction is becoming
  wrong (churn, growth, repeated-fix). Measure-only findings.v0. Use on
  factory-qc deep-audit, not pre-merge. Not a cost-reward refactor loop.
---

# qc-temporal — Temporal lint leaf

Normal lint asks what is structurally wrong now.
This leaf asks what pattern of change suggests the structure is becoming wrong.

A junior runs the two python commands, opens the table, and stops.

## When to use

- `/factory-qc` profile `deep-audit` (wired after volume cap)
- Standalone `/qc-temporal` after a series that kept touching the same files
- When coupling-debt LOC is stable but change cost still feels high

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Fast pre-merge | `/factory-qc` profile `pre-merge` (this leaf is not in it) |
| Full-repo snapshot audit | `/comprehensive-codebase-review` |
| Diff maintainability now | `/code-review` |
| LOC snapshot | `qc-coupling-debt` |
| Ship / LFG / gauntlet | do not — this leaf is measure-only |

## Junior run

From repo root:

```powershell
python .grok/skills/qc-temporal/scripts/run_temporal.py --repo-root .
python scripts/validate_factory_qc_findings.py notes/qc/_samples/temporal/findings.json
```

Then open `notes/qc/_samples/temporal/TABLE.md` and **stop**. Do not implement. Do not LFG.

Default scope is `pipeline/` (opt in skills with `--path .grok/skills/`). Top 20 hotspot paths only; extras are one info count finding. `medium` only when the same path is churn **and** grow **and** repeat-fix.

## Table (required)

| file | pattern | why-direction-wrong |
|------|---------|---------------------|
| path | churn / grow / repeat-fix | one sentence |

Patterns:

- **churn** — many commits on one path in the window
- **grow** — net lines up by the grow threshold
- **repeat-fix** — commit subject starts with `fix` or contains hotfix/bugfix

## Honesty

- Git history is observation, not a proof crown.
- A hot file is not field_proven debt and not ADEQUATE.
- Do not treat drop in churn as goal_proven.
- Do not build a refactor agent scored on "future change cost."
- Do not add this leaf to pre-merge.
- Table ≠ implement order. Residual omitted paths are not secretly higher priority.

## Non-claims

- factory health ≠ field_proven / goal_proven_human
- table ≠ implement order
- temporal finding ≠ CCR rewrite
