---
name: qc-errors
description: >-
  Factory self-QC leaf: scan bare except / swallowed errors; emit findings.v0.
  Prefer soft_log patterns. Use on agent/handoff/bus changes or /factory-qc.
  Not full reliability engineering.
---

# qc-errors — Error-surface leaf

## When to use

- agent_process / handoff / bus / soft-fail changes
- `/factory-qc` pre-merge errors step

## Procedure

1. Scan scoped `.py` for bare `except:`, `except Exception: pass`, two-line pass.
2. Allowlist lines/bodies with `soft_log_exc` / `_soft_log_exc` / `soft_log` /
   `intentional` / `qc-errors-allow`.
3. **Severity policy (residual plan 03):**
   - **Hot-path** modules (agent metrics/supervisor, autonomy metrics,
     block_registry, health_checks, agent_process, message_bus, complete_gate,
     field_prove_gate, goal_prove, runner): E01/E02 → **medium**
   - All other pipeline paths: E01/E02 → **low** (volume backlog denoise)
4. Emit findings.v0.

## Commands

```powershell
python .grok/skills/qc-errors/scripts/run_errors.py --repo-root .
python scripts/validate_factory_qc_findings.py notes/qc/_samples/errors/findings.json
python -m pytest test_qc_errors.py test_soft_log.py -q
```

## Prefer

`from pipeline.soft_log import soft_log_exc` (or agent_process `_soft_log_exc`)
instead of bare `except: pass`.

## Non-claims

- Not SRE completeness  
- Clean scan ≠ field_proven  
- low bulk residual ≠ fixed  
