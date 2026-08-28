---
name: findings-triage
description: >-
  Bucket factory-qc (or CCR) findings into safety / hot-control / agent-soft /
  accept residual, emit 0–N bounded implement packs under notes/triage/<stamp>/.
  Never auto-LFG, gauntlet, or implement. Use when the user runs /findings-triage,
  /qc-triage, "triage QC findings", "bucket the lows", "what to implement from
  QC", or after factory-qc when low/info residual is large and Medium+ is clean
  or mixed. Not product field_proven; not factory-improve product routing.
metadata:
  short-description: "QC/CCR findings → buckets + bounded packs (no ship)"
argument-hint: "[--stamp ID] [--max-per-pack N] [--max-packs N]"
---

# /findings-triage — Findings → buckets → ship-shaped packs

You are the **findings triage orchestrator**. You **classify and emit packs**.
You do **not** run `/implement`, `/gap-to-plan`, `/lfg`, or gauntlet unless the
user explicitly asks after seeing the triage output.

**Factory health ≠ field_proven.** Triage packs are aim fuel only.

## When to use

| Trigger | Action |
|---------|--------|
| After `/factory-qc` with large low residual | Bucket + packs |
| User: `/findings-triage`, "triage lows", "bucket QC" | Same |
| CCR report with many Medium/Low | Optional fuel via `--source` |
| Medium+ clean, unsure whether to touch E02 bulk | Prefer this before implement |

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Run scanners | `/factory-qc` |
| Soft next options only (Medium+ focus) | `/factory-qc-handoff` |
| Ship a known short Medium+ list | `/implement …` directly |
| Product post-field expand | `/factory-improve` |
| Next LFG aim portfolio | `/suggest` |
| Full multi-plan aim from zero | `/gap-to-plan` / `/lfg` |

## Defaults

| Setting | Value |
|---------|--------|
| Source | `notes/qc/LATEST` → `findings.json` |
| Max findings per pack | **15** |
| Max ship packs | **3** |
| Auto ship skills | **never** |

## Composition

```text
1. Resolve stamp / source findings
2. Run scripts/run_findings_triage.py
3. Read notes/triage/<stamp>/TRIAGE.md + packs.json
4. Print human handoff (options only)
5. STOP — wait for user choice
```

## Procedure (agent)

1. **Resolve repo root** (workspace cwd).
2. **Resolve stamp:**
   - User `--stamp <id>`, or
   - `notes/qc/LATEST` contents, or
   - explicit path to `findings.json` / stamp dir.
3. **Run triage script** (do not invent buckets without running it when the script exists):

```powershell
python .grok/skills/findings-triage/scripts/run_findings_triage.py --repo-root . --stamp <id>
# optional:
#   --max-per-pack 15
#   --max-packs 3
#   --findings-json path\to\findings.json
```

4. **Read** `notes/triage/<stamp>/TRIAGE.md`, `packs.json`, `DEFER.md`.
5. **Print handoff** (exact shape below). **Stop.** Do not auto-implement.

## Handoff print shape

```text
findings-triage complete
stamp: notes/qc/<stamp>/  (or source)
out:   notes/triage/<stamp>/
counts: critical=… high=… medium=… low=… info=…
buckets: A=… B=… C=… D=…
packs:   N (≤ max-packs)

Pack list:
  P1 … (n items) → /implement …
  …

Choose ONE:
  1) /implement pack P1 from notes/triage/<stamp>/packs.json
  2) /gap-to-plan using notes/triage/<stamp>/TRIAGE.md as fuel (if multi-pack)
  3) stop — accept DEFER residual
  4) re-run with --max-per-pack / different stamp

FORBIDDEN (this skill never auto-runs):
  /lfg  /encore  /universal-gauntlet  /implement  /gap-to-plan
```

## Buckets (closed)

See `references/buckets.md`.

| Id | Name | Ship? |
|----|------|-------|
| **A** | safety-adjacent | Prefer pack / implement |
| **B** | hot control-plane | Pack ≤ max-per-pack |
| **C** | agent soft-except | Soft_log only or defer |
| **D** | accept residual | Stop / document |

**Medium+** (critical/high/medium) always lands in **ship candidates** first (still capped by max-per-pack / max-packs); overflow → note for encore/gap.

## Output contract

See `references/output-contract.md`.

```text
notes/triage/<stamp>/
  TRIAGE.md
  packs.json
  DEFER.md
  summary.json
```

## Anti-patterns

- Auto-running `/implement` on all lows
- One pack with 100+ items
- Claiming field_proven from QC green + triage
- Rewriting bucket policy ad hoc without updating `references/buckets.md`
- Using this for product expand routing (`factory-improve`)

## Related

| Skill | Role |
|-------|------|
| `factory-qc` | Measure → stamp; AIM/REPORT soft-link here when low bulk |
| `factory-qc-handoff` | Soft next options; **recommends** this skill when medium+=0 & low≥20 |
| `implement` | Ship one pack after user confirm |
| `gap-to-plan` | Multi-pack residual aim |
| `suggest` | Next LFG aims (not finding lines) |

**Wiring note:** handoff/AIM **name** this skill; they never auto-execute it.

## Success criteria

- Script ran; `notes/triage/<stamp>/` written
- Buckets A–D assigned with counts
- Packs ≤ max-packs and each ≤ max-per-pack
- User shown options; **no ship skill auto-started**
- Non-claims printed (factory health ≠ field_proven)
