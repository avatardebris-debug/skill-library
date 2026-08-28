---
name: qc-contracts
description: >-
  Factory self-QC leaf: run public API freeze tests and path-ref checks; emit
  findings.v0 including freeze-coverage gaps for hot façades. Use after splits,
  /factory-qc pre-merge, or /qc-contracts. Does not invent new public APIs.
---

# qc-contracts — Public API + path-ref leaf

## When to use

- After façade / god-module splits
- `/factory-qc` pre-merge contracts step
- User asks for freeze coverage residual

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Add new product API | implement + freeze intentionally |
| Full repo review | comprehensive-codebase-review |

## Inputs

| Input | Default |
|-------|---------|
| Repo root | cwd |
| Out | `notes/qc/_samples/contracts/findings.json` |
| Skip path-ref | `--skip-path-ref` if noisy |

## Outputs

- findings.v0 JSON (≥1 finding)
- Includes informational freeze gaps for uncovered hot façades

## Procedure

1. Run `pytest test_pipeline_public_api_contracts.py -q`.
2. Run `python scripts/check_pipeline_path_refs.py` if present (soft-fail → findings).
3. Compare known hot façades to FROZEN_* in contract test file → `freeze_gap` info/medium.
4. Emit pass_summary if tests green and no gaps required.
5. Validate with `scripts/validate_factory_qc_findings.py`.

## Commands

```powershell
python .grok/skills/qc-contracts/scripts/run_contracts.py --repo-root .
python scripts/validate_factory_qc_findings.py notes/qc/_samples/contracts/findings.json
```

## Hot façades (coverage inventory)

`github_crawl`, `goal_graph`, `research_candidates`, `research_fuel_adapters`,
`research_fuel_handoff`, `goal_prove`, `goal_amend_ladder`, `budget_ladder`,
`agent_process`, `external_ingest`, `engines.field_ship`, `engines.grok_build`

(Freezes may be partial — gaps are findings, not auto-fixes.)

## Non-claims

- Does not invent public API  
- Green contracts **≠** field_proven  
- Path-ref may false-positive (low severity)

## Related

- `test_pipeline_public_api_contracts.py`
- `scripts/check_pipeline_path_refs.py`
- Schema: `notes/qc/findings.v0.md`
