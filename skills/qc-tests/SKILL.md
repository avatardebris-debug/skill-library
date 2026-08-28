---
name: qc-tests
description: >-
  Factory self-QC leaf: run public API pytest + optional critical-path smoke;
  weak-test heuristic for hot modules without tests; emit findings.v0.
  Use pre-merge / factory-qc. Not mutation testing or product field tests.
---

# qc-tests — Impact / smoke / weak-test leaf

## When to use

- Pre-merge factory changes
- `/factory-qc` tests profile step

## Commands

```powershell
# Fast (default for CI leaf): contracts only + weak-test heuristic
python .grok/skills/qc-tests/scripts/run_tests.py --repo-root . --skip-smoke

# Full leaf: also critical-path smoke --skip-crawl
python .grok/skills/qc-tests/scripts/run_tests.py --repo-root .

python scripts/validate_factory_qc_findings.py notes/qc/_samples/tests/findings.json
```

## Heuristics

| Signal | Severity |
|--------|----------|
| Public API contract pytest fail | high |
| Critical-path smoke fail | high |
| Hot module ≥800 LOC without `test_*.py` hit | medium |
| All green | info pass_summary |

## Non-claims

- Not mutation score / coverage % gate  
- Not product field tests / dual-gate proof  
