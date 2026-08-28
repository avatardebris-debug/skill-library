---
name: qc-runtime-control
description: >-
  Factory self-QC leaf: static proxies for overnight control-plane stall classes
  (dead-role bus emptiness, health thrash factory-root, phase-heading advance
  f-string trap, control_plane_invariants wiring). Emits findings.v0. Use on
  run_loop/health/project_phase changes or /factory-qc. Not full runtime soak;
  not field_proven.
---

# qc-runtime-control — Control-plane stall proxies

## When to use

- Changes to `run_loop.py`, `health_checks.py`, `project_phase.py`, `control_plane_invariants.py`
- `/factory-qc` pre-merge or deep-audit
- After overnight stall postmortems

## Procedure

1. Scan hot control-plane modules for known bad patterns.  
2. Emit `factory_qc_findings.v0` (severity medium for true stall risks).  
3. Pass_summary info if clean.

## Commands

```powershell
python .grok/skills/qc-runtime-control/scripts/run_runtime_control.py --repo-root .
python -m pytest test_qc_runtime_control.py -q
```

## Non-claims

- Static proxy ≠ multi-hour overnight proof  
- factory health ≠ field_proven  
- Clean leaf ≠ product dual-gate  

## Related

- `pipeline/control_plane_invariants.py`  
- `/overnight-ops-audit` (receipt-side)  
