---
name: factory-qc-handoff
description: >-
  Prompt-only handoff after /factory-qc: read latest stamp REPORT + findings,
  print severity counts and next options (implement Medium+, findings-triage for
  large low residual, gap-to-plan, stop). Never auto-runs LFG, gauntlet,
  gap-to-plan, implement, or findings-triage. Use when user asks what next after
  factory-qc.
---

# factory-qc-handoff — Soft next-step prompt

## When to use

- After `/factory-qc` (or `run_factory_qc.py`)
- User asks “what next?” with a QC stamp

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Run the measure suite | `/factory-qc` / `run_factory_qc.py` |
| Bucket lows into packs | `/findings-triage` (after handoff recommend) |
| Actually ship residual | User confirms → `/implement` or `/gap-to-plan` |
| Product post-field triage | `factory-improve` |

## Procedure (agent)

1. Resolve stamp: `notes/qc/LATEST` or user-provided path.
2. Prefer script (keeps options consistent):

```powershell
python .grok/skills/factory-qc-handoff/scripts/print_handoff.py --repo-root .
python .grok/skills/factory-qc-handoff/scripts/print_handoff.py --repo-root . --stamp <id>
```

3. Print handoff block (severity counts, top Medium+, adaptive options).
4. **Stop and wait** for user choice. Do **not** invoke other skills unless asked.

## Options (adaptive)

Script chooses based on counts (`low-triage-threshold` default **20**):

| Situation | Options (user confirm) |
|-----------|-------------------------|
| **Medium+ > 0** | 1) `/gap-to-plan` 2) `/implement Medium+` 3) `/findings-triage` if low≥threshold 4) stop |
| **Medium+ = 0 and low ≥ threshold** | 1) **`/findings-triage`** (preferred) 2) `/gap-to-plan` (only if multi-plan aim) 3) stop |
| **Medium+ = 0 and low < threshold** | 1) optional `/findings-triage` if any lows 2) gap 3) stop |

After findings-triage: `/implement pack P1 from notes/triage/<stamp>/packs.json`.

## Stream (soft compose)

```text
/factory-qc
  → /factory-qc-handoff          # this skill — prompt only
       ├─ Medium+ → /implement or /gap-to-plan
       ├─ Medium+=0 & low large → /findings-triage → /implement pack
       └─ stop
```

**Never auto-run** findings-triage or implement from this skill.

## Forbidden (never auto)

- `/lfg`, `/encore`, `/universal-gauntlet`, `/gap-to-plan`, `/implement`, `/findings-triage` without user confirm  
- Claiming field_proven from QC green  
- Full **qc-LFG** outer loop (measure→gap→ship→remeasure) — **future pack only**

## Non-claims

- Handoff text ≠ execution  
- factory health ≠ product dual-gate proof  

## Related

- Meta measure: `.grok/skills/factory-qc/`  
- Low residual packs: `.grok/skills/findings-triage/`  
- Stamps: `notes/qc/<stamp>/`  
