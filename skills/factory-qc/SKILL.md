---
name: factory-qc
description: >-
  Measure-only factory self-QC meta: run leaf scanners by profile (pre-merge /
  deep-audit), merge findings.v0, write notes/qc/<stamp>/REPORT.md + findings.json
  + AIM_FROM_QC.md. Use /factory-qc for factory health checks. Report is aim fuel
  for gap-to-plan, implement Medium+, or findings-triage (large low residual) —
  does NOT ship, gauntlet, or auto-LFG. Factory health ≠ field_proven.
---

# factory-qc — Meta measure skill

## When to use

- `/factory-qc`, factory health check, pre-merge factory changes, post-series remeasure
- After shipping factory-qc leaves

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Soft next-step prompt | `/factory-qc-handoff` |
| Bucket large low residual | `/findings-triage` (after handoff when recommended) |
| Ship Medium+ punch list | `/implement Medium+ findings from notes/qc/<stamp>/REPORT.md` |
| Ship triage pack | `/implement pack P1 from notes/triage/<stamp>/packs.json` |
| Product field proof | `/field-test` |
| Diff PR review | `/code-review` |
| Full prose audit only | `/comprehensive-codebase-review` (also optional deep-audit delegate) |

## Profiles

See `references/profiles.md`.

| Profile | Leaves |
|---------|--------|
| `pre-merge` | static, contracts, honesty, errors, tests(--skip-smoke), security |
| `deep-audit` | pre-merge + coupling-debt + qc-temporal + CCR delegate note |

## Commands

```powershell
python .grok/skills/factory-qc/scripts/run_factory_qc.py --repo-root . --profile pre-merge
python .grok/skills/factory-qc/scripts/run_factory_qc.py --repo-root . --profile deep-audit
python .grok/skills/factory-qc/scripts/run_factory_qc.py --repo-root . --profile pre-merge --skip-leaves qc-honesty,qc-errors
```

Outputs under `notes/qc/<stamp>/`:

- `findings.json` — merged factory_qc_findings.v0  
- `REPORT.md` — human summary  
- `AIM_FROM_QC.md` — aim stub for gap-to-plan  
- `scope.json` — profile, leaves, commands  

Validate:

```powershell
python scripts/validate_factory_qc_findings.py notes/qc/<stamp>/findings.json
```

## Non-claims / forbid

- factory health **≠** field_proven / goal_proven_human  
- Report-only — **does not** run gap-to-plan, gauntlet, implement, LFG, encore  
- Does not reimplement comprehensive-codebase-review  

## Soft stream (user confirm; never auto-ship)

```text
/factory-qc
  → /factory-qc-handoff
       ├─ Medium+ → /implement Medium+  or  /gap-to-plan
       ├─ medium+=0 & low large → /findings-triage → /implement pack P1
       └─ stop
```

`AIM_FROM_QC.md` and `REPORT.md` **Next** sections name `/findings-triage` when
low residual dominates. This skill does **not** run triage or implement.

## Related

- Leaves: `qc-static` … `qc-security`  
- Schema: `notes/qc/findings.v0.md`  
- Handoff: `factory-qc-handoff`  
- Low residual packs: `findings-triage`  
