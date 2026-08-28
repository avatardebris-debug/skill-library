---
name: qc-honesty
description: >-
  Factory self-QC leaf: scan for dual-gate / soft≠execute / auto-LFG / field_proven
  honesty anti-patterns; emit findings.v0. Use near prove/ladder/handoff/complete_gate
  changes or /factory-qc. Not product dual-gate proof; not field_proven.
---

# qc-honesty — Factory honesty / invariant leaf

## When to use

- Changes under goal_prove, ladders, handoff, complete_gate, field_ship, meta_act
- `/factory-qc` pre-merge / deep-audit honesty step
- User runs `/qc-honesty`

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Prove a product field_proven | `/field-test` + dual-gate |
| Full code review | comprehensive-codebase-review / code-review |
| Fix all findings | `/implement` or gap pack from report |

## Inputs

| Input | Default |
|-------|---------|
| Repo root | cwd |
| Scope | `pipeline/` (override with `--path`) |
| Out | `notes/qc/_samples/honesty/findings.json` |
| Fixture mode | `--fixture-mode` scans only skill fixtures |

## Outputs

- findings.v0 JSON (≥1 finding; pass_summary if clean)

## Procedure

1. Load patterns from `references/honesty-patterns.md` (or embedded table in script).
2. Walk scoped `.py` files (skip `__pycache__`, large vendored).
3. Skip allowlisted honesty/non-claim lines.
4. Emit findings with path + line + rule id.
5. Validate with `scripts/validate_factory_qc_findings.py`.

## Commands

```powershell
python .grok/skills/qc-honesty/scripts/run_honesty.py --repo-root .
python .grok/skills/qc-honesty/scripts/run_honesty.py --repo-root . --fixture-mode
python scripts/validate_factory_qc_findings.py notes/qc/_samples/honesty/findings.json
python -m pytest test_qc_honesty.py -q
```

## Non-claims

- Not proof dual-gate works in production  
- Not field_proven / goal_proven  
- Scanner residual only; false negatives preferred over comment noise  

## Related

- Doctrine: `notes/ops/dual_gate_contract.md`
- Patterns: `references/honesty-patterns.md`
- Schema: `notes/qc/findings.v0.md`
