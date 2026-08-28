---
name: qc-static
description: >-
  Factory self-QC leaf: run available static tools (ruff, etc.) and emit
  findings.v0 JSON. If tools missing, emit structured tool_missing (valid success).
  Use when /factory-qc static profile, pre-merge factory changes, or /qc-static.
  Not a SAST platform; not product field_proven.
---

# qc-static — Factory static analysis leaf

## When to use

- `/factory-qc` pre-merge / deep-audit static step
- User runs `/qc-static` or “factory lint check → findings”

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Full prose audit | `/comprehensive-codebase-review` |
| Product field proof | `/field-test` |
| Fix lint mass-auto | implement after report |

## Inputs

| Input | Default |
|-------|---------|
| Repo root | cwd / workspace |
| Scope paths | optional list |
| Out path | `notes/qc/_samples/static/findings.json` |

## Outputs

- `factory_qc_findings.v0` JSON (≥1 finding)
- Optional short markdown fragment

## Procedure

1. Resolve repo root.
2. Detect tools (do **not** install):
   - `ruff` on PATH and/or `[tool.ruff]` in pyproject.toml
   - optional: mypy/pyright if clearly configured
3. If **no** tools: emit one `tool_missing` finding (severity `info`).
4. If tools present: run with scoped paths; map issues → findings (lint → low/medium).
5. Always include `non_claims` from schema.
6. Validate with `scripts/validate_factory_qc_findings.py` when available.

## Commands

```powershell
python .grok/skills/qc-static/scripts/run_static.py --repo-root .
python .grok/skills/qc-static/scripts/run_static.py --repo-root . --out notes/qc/_samples/static/findings.json
python scripts/validate_factory_qc_findings.py notes/qc/_samples/static/findings.json
```

## Non-claims

- Not SAST / pen test / product security proof  
- Clean static **≠** field_proven  
- factory health **≠** goal_proven_human  

## Related

- Schema: `notes/qc/findings.v0.md`
- Meta (later): `factory-qc`
