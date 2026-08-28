# Handoff packet (factory-improve → LFG / thin quality)

After route is chosen, fill a packet. **Do not** auto-start `/encore`.  
**Do not** auto-start `/lfg` unless the user (or explicit meta budget) said continue.

## Packet fields

| Field | Required | Description |
|-------|----------|-------------|
| `mode` | yes | `lfg` \| `thin_quality` \| `none` |
| `aim` | if lfg | One measurable aim line for `.lfg/AIM.md` |
| `surface` | yes | Target path/slug |
| `route` | yes | Closed enum from router |
| `constraints` | yes | Non-goals, dual-gate, budgets |
| `suggested_commands` | yes | Ordered list for human/meta |
| `decision_id` | yes | Link to decision record |
| `critic_tier` | if lfg | default `medium` |

## mode selection

| Route | Default mode |
|-------|----------------|
| `feature_expand` | `lfg` (aim = expand surface X with budget) |
| `quality` | `thin_quality` unless debt spans multi-plan |
| `connector` | `lfg` |
| `new_product` | `lfg` |
| `compose` | `lfg` or thin note to goal compose |
| `defer` | `none` |
| `human` | `none` (+ questions) |

## thin_quality template

When mode = `thin_quality`:

1. List 1–5 concrete fixes (tests, fixtures, docs honesty)  
2. Suggest `/implement` or small gauntlet on a **quality** master plan only if multi-file  
3. Re-run impact tests for surface  

## lfg template aim examples

```text
Expand <surface> with <capability> under feature_expand budgets; dual-gate intact; no auto-promote.
```

```text
Quality pass on <surface>: close proof debt (fixtures/tests); no behavior expansion.
```

```text
Add connector/MCP leaf for <capability> reusing <surface>; secondary honesty if external.
```

## suggested_commands block (example)

```text
1. Review decision: .factory-improve/decisions/<id>.md
2. /lfg <aim from packet> --critic medium
   # or thin: implement listed quality items
3. After ship: optional /factory-improve again on same surface only if residual debt
```
