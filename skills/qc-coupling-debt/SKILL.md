---
name: qc-coupling-debt
description: >-
  Factory self-QC leaf: LOC hotspots and residual god-module list → findings.v0.
  Adapts inventory/remeasure; does not split modules. Use after refactors or
  /factory-qc deep-audit.
---

# qc-coupling-debt — Coupling / residual debt leaf

## When to use

- After large refactors / ownership splits
- factory-qc deep-audit residual step
- Series remeasure

## Procedure

1. Count physical lines of `pipeline/*.py` and `pipeline/_*/**/*.py` (impl-heavy).
2. Emit finding per module/package ≥ threshold (default 800 LOC) severity medium.
3. Note remeasure doc if present (`notes/ops/god_module_safe_split_series_remeasure.md`).
4. Optionally point at `scripts/god_module_import_inventory.py` (do not require it green).

## Commands

```powershell
python .grok/skills/qc-coupling-debt/scripts/run_debt.py --repo-root .
python scripts/validate_factory_qc_findings.py notes/qc/_samples/coupling_debt/findings.json
```

## Non-claims

- Does **not** split modules or claim maintainability closed  
- Residual list ≠ all debt fixed  
