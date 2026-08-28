# fanout status schema

## fanout/<slug>/status.json

```json
{
  "schema_version": 1,
  "slug": "hedge-fund",
  "pack_path": "deconstructions/hedge-fund",
  "critic": "harsh",
  "max_leaves": 5,
  "selected": ["hf.ops.recon"],
  "order": ["hf.ops.recon"],
  "leaves": {
    "hf.ops.recon": {
      "status": "shipped",
      "aim": "one-line aim",
      "module_path": "optional",
      "lfg_gap": "optional path",
      "notes": "optional",
      "updated": "ISO-8601"
    }
  },
  "stop_reason": "complete|max_leaves|failed|cancel",
  "updated": "ISO-8601"
}
```

## fanout/<slug>/leaves/<id>/status.json

Same leaf object fields; written per leaf so parallel workers can avoid full-file races.
