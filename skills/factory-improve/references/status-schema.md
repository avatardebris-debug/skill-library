# `.factory-improve/` status schema

## Layout

```text
.factory-improve/
  status.json                 # latest triage pointer
  decisions/
    <decision_id>.md          # human-readable decision record
    <decision_id>.json        # optional machine copy
```

## status.json

```json
{
  "schema": "factory_improve_status.v0",
  "updated": "ISO-8601",
  "latest_decision_id": "fi_YYYYMMDD_HHMMSS",
  "surface": "pipeline/github_crawl|project:<slug>|skill:…",
  "route": "feature_expand|quality|connector|new_product|compose|defer|human",
  "handoff_path": ".factory-improve/decisions/…",
  "lfg_aim_suggested": "one-line aim or null",
  "encore_count_on_surface": 0,
  "does_not_claim": ["outer_RSI", "field_proven", "goal_proven"]
}
```

## Decision record (required fields)

| Field | Type | Notes |
|-------|------|--------|
| `decision_id` | string | unique |
| `surface` | string | module / project / skill path |
| `trigger` | string | complete \| field_proven \| feature_expand \| meta \| human \| quality_debt |
| `gates` | map gate→pass\|fail | hard eligibility |
| `scores` | map axis→0..1 | scorecard |
| `priority` | number | optional derived |
| `route` | enum | closed set only |
| `rationale` | 1–5 bullets | short |
| `handoff` | object | see handoff-packet.md |
| `borderline` | bool | true if forced to human or near-tie |
| `human_required` | bool | |

## decision markdown shape

```markdown
# Decision <id>

- surface: …
- trigger: …
- route: …
- borderline: yes|no

## Gates
| gate | result |
|------|--------|
| eligible_complete_or_field | pass |

## Scores
| axis | score | source |
|------|-------|--------|
| potential_usefulness | 0.7 | qual |

## Handoff
- mode: lfg | thin_quality | none
- aim: …
- constraints: …
```
