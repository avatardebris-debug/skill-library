# Autosuggest loop contract

```text
cycle n:
  suggest -> select -> lfg -> log
default n = 1..4
```

## Select order

1. top **high** unused aim  
2. top **medium** unused aim  
3. else stop `no_viable_new_aim`

## Between cycles

- No `/encore`  
- Re-run `/suggest` on fresh disk  
- Prefer skip suggest deep-research if last LFG re-gap is fresh  

## Caps

| Cap | Value |
|-----|-------|
| loops | default 4, hard max 8 |
| aims per run | unique; no exact string repeat |
| lfg max-plans | default 3 |

## Resume

Read `.autosuggest/status.json` `cycle` and `cycles_done`; continue at next n.
