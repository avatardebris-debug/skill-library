# Output contract — findings-triage

## Directory

`notes/triage/<stamp>/` where `<stamp>` matches QC stamp id (or `manual-<date>`).

## TRIAGE.md

Human summary:

- Source stamp / profile
- Severity counts
- Bucket counts A–D
- Pack table (id, n items, bucket focus, suggested next skill)
- Honesty non-claims

## packs.json

```json
{
  "schema": "findings_triage_packs.v0",
  "stamp": "2026-08-09T05-54-54Z",
  "max_per_pack": 15,
  "max_packs": 3,
  "packs": [
    {
      "id": "P1",
      "title": "…",
      "bucket_focus": ["A", "medium_plus"],
      "suggested_skill": "implement",
      "finding_ids": ["…"],
      "items": [
        {
          "id": "…",
          "severity": "low",
          "bucket": "A",
          "path": "pipeline/foo.py",
          "line": 12,
          "title": "…",
          "rule": "E02_except_pass",
          "recommendation": "…"
        }
      ]
    }
  ]
}
```

## DEFER.md

- Count and rationale for bucket D (+ overflow beyond max-packs)
- Explicit: not field_proven work

## summary.json

Machine-readable counts + pack ids for other tools.
