---
name: qc-security
description: >-
  Factory self-QC leaf: secrets greps, shell_safety usage on runners, write-root
  and allow-live smells → findings.v0. Use on engines/ingest/env-flag changes or
  factory-qc deep-audit. Not full SAST/pen test.
---

# qc-security — Factory security-surface leaf

## When to use

- engines / shell / external_ingest / allow-live changes
- `/factory-qc` deep-audit security step

## S12 allow_live policy (residual plan 04)

**Flag:** real `allow_live=True` enable (assignment / call kwarg).  
**Skip:** argparse `--allow-live` registration, help strings, comments,
default-off / `allow_live=False`, refuse/not-implemented / network_stub docs.

## Commands

```powershell
python .grok/skills/qc-security/scripts/run_security.py --repo-root .
python scripts/validate_factory_qc_findings.py notes/qc/_samples/security/findings.json
python -m pytest test_qc_security.py -q
```

## Non-claims

- Not full SAST/SCA platform  
- Not pen test  
- Not product field_proven  

## Related

- `references/security-surface.md`
- `pipeline/shell_safety.py`
