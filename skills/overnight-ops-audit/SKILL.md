---
name: overnight-ops-audit
description: >-
  Receipt-first audit of factory overnight runs: parse logs/overnight_* for
  stalls, health auto_fix thrash, dead-role bus occupancy, implement
  side-effects (winget/OS install), soft_log/NameError crashes. Writes a
  structured report; never auto-LFG, never mutates projects, never claims
  field_proven. Use when user runs /overnight-ops-audit, "audit overnight",
  "why did overnight stall", "morning log check", or after overnight finishes.
---

# /overnight-ops-audit — Overnight receipt audit

## Defaults

| Setting | Value |
|---------|--------|
| Mode | **measure-only** |
| Input | `$PIPELINE_DIR/logs/overnight_*` (or `--overnight-dir`) |
| Auto-LFG | **never** |
| Mutate projects | **never** |

## When to use

- After overnight finishes (or mid-run health check)
- User asks why stall / 0 tokens / high auto-fix / incomplete_recovered
- Comparing last N overnights

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Fix runner code | `/lfg` or `/implement` after audit |
| Factory code smell scan | `/factory-qc` |
| Live product field proof | field-test / dual-gate path |

## Procedure (agent)

1. Resolve `PIPELINE_DIR` (env or `~/aicompete/thepipeline` or user path).  
2. Run the CLI (preferred) or reimplement the same checks:

```powershell
python .grok/skills/overnight-ops-audit/scripts/run_audit.py --pipeline-dir $env:PIPELINE_DIR --latest 1
python .grok/skills/overnight-ops-audit/scripts/run_audit.py --pipeline-dir $env:PIPELINE_DIR --latest 3 --json notes/ops/overnight_audit_latest.json
python .grok/skills/overnight-ops-audit/scripts/run_audit.py --overnight-dir C:\path\to\logs\overnight_YYYYMMDD_HHMMSS
```

3. Present: severity counts, top findings, timeline one-liner, three options.  
4. **Stop** — do not auto-gap-to-plan or implement unless user confirms.

## What the CLI detects

| Finding class | Source |
|---------------|--------|
| `stall` | runner.out `STALL DETECTED` lines + ages |
| `auto_fix_thrash` | `Health check: N auto-fixed` with N≥50 or same N repeated ≥3 |
| `soft_log_crash` / traceback | runner.err NameError soft_log_exc, Traceback |
| `exit` | runner.log exit code / incomplete |
| `mass_mvp` | many `MVP complete (phase a/b)` vs few advances |
| `false_mvp_disk` | `list_false_mvp_projects` on current pipeline disk |
| `agent_tokens` | role logs `Completed message … tokens=N` (date-filtered) |
| `seed_block` | throng6 / blocked requires |
| `project_transition` | Seeded / complete_with_bugs / mvp_complete / phase advance |
| `side_effect` | winget / Graphviz / choco in out/err or project grok logs |
| `dead_role_bus` | message_bus.db pending to non-classic roles |
| `stall_receipt` | `state/stall_receipts.json` if present |
| `reseed_soak` | runner.out `[reseed]` post-complete / empty-queue (via `pipeline.reseed_soak_receipt`) |

## Three options (after report)

1. **`/lfg <fix aim>`** — if Medium+ runner bug named  
2. **Re-run overnight** — if code fix already on disk and process was stale  
3. **stop**

## Forbidden

- Auto `/lfg` / `/encore`  
- Claiming field_proven from a green-looking morning  
- Deleting or rewriting overnight logs  
- “Quiet” product project edits  

## Non-claims

- Audit report ≠ product dual-gate proof  
- Token counts in truth_density may undercount agent logs  
- factory health ≠ field_proven  

## Related

- Research fuel: `.lfg/research/overnight-ops-audit-2026-08-06.md`  
- Fixes context: run_loop dead-role emptiness, health_checks factory skip  
