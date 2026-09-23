# overnight-series contract

## Playlist

```text
for wave in 1..W (W≤3):
  /series-loop --leaves L (L≤2)
  /after-series-qc --auto soft|report
  stop if implement_failed | still_series | no_leaf | qc Medium+ critical/high | skills missing
```

## Ceilings

- Waves ≤ 3, leaves/wave ≤ 2
- qc default **soft** (packs only)
- Never gauntlet / encore / autosuggest / invent series
- Empty ROADMAP → point at `/aim-to-series`, stop

## Honesty

Overnight playlist progress ≠ field_proven ≠ Gate ACCEPT.
