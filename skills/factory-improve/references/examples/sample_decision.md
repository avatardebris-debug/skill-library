# Decision fi_sample_crawl_quality

- surface: `pipeline/github_crawl` (façade + `_github_crawl`)
- trigger: quality_debt
- route: **quality**
- borderline: no
- decision_id: fi_sample_crawl_quality

## Gates

| gate | result |
|------|--------|
| eligible_surface | pass |
| eligible_trigger | pass |
| mission_aligned | pass |
| coding_sized | pass |
| honesty_safe | pass |
| not_in_flight | pass |
| fixed_rules | pass |

## Scores

| axis | score | source |
|------|-------|--------|
| potential_usefulness | 0.6 | qual (crawl still used in fuel paths) |
| current_usefulness | 0.5 | call sites present; fixture path reds |
| potential_minus_current | 0.1 | derived |
| attach_cost | 0.3 | fixture restore + tests |
| proof_debt | 0.8 | missing tests/fixtures/github_crawl_candidates.json; baseline 8 fails |
| composability | 0.5 | rank/handoff leaf |
| operator_pain | 0.4 | known reds |
| honesty_risk | 0.2 | quality only |

**priority** ≈ high on proof_debt → **quality**

## Rationale

1. Hard gates pass; not invent/greenfield.  
2. proof_debt high with existing surface → quality before expand.  
3. Restoring fixture is attach_cost-low, honesty-safe.

## Handoff

- mode: `thin_quality`
- aim: n/a (thin)
- constraints: no promote invent; fail count may drop below 8 only via fixture honesty
- suggested_commands:
  1. Restore or document `tests/fixtures/github_crawl_candidates.json`
  2. `pytest test_github_crawl.py -q`
  3. Optional later: `/factory-improve pipeline/github_crawl` for expand if debt closed
