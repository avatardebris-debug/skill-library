---
name: morning-ops-pack
description: >-
  Operator morning pack after overnight factory runs: receipt audit, pipeline
  status, portfolio honesty scan, seed/hygiene peek, then a human decision menu.
  Measure-only by default; never auto-LFG, never mutates projects, never claims
  field_proven. Use when user runs /morning-ops-pack, "morning check", "what
  happened overnight", "ops pack", or after overnight_grok_from_list finishes.
metadata:
  short-description: "Morning operator checklist for overnight factory runs"
---

# /morning-ops-pack — Morning / overnight ops pack

Skill Contract for AGI-LMAOOO operator mornings. Wraps `/overnight-ops-audit`
plus status + honesty surfaces into one receipt-first loop.

## Skill Contract

| Field | Value |
|-------|--------|
| **Trigger** | `/morning-ops-pack`, "morning check", "overnight ops", after overnight finishes |
| **Inputs** | `PIPELINE_DIR` (env or user path); optional `--overnight-dir`; optional `--latest N` (default 1) |
| **Mode** | **measure-only** (default). No writes to `projects/`, no status promotion, no auto-LFG |
| **Done-when** | Structured morning brief delivered + three options offered + agent **stops** |
| **Failure** | Missing `PIPELINE_DIR` / no overnight logs → report blocker, list how to resolve, stop |
| **Side effects** | May write report JSON under `notes/ops/` or overnight log dir only if user asks; default = chat brief only |

## Honesty doctrine (hard)

- Mechanical runner green ≠ `field_proven`
- `complete` / `mvp_complete` / `field_test_passed` ≠ product-proven
- Audit / morning report ≠ dual-gate proof
- Reseed soak receipt ≠ pass
- Evidence edges / `--check-claim` ≠ dual-gate promote
- **Never invent** `field_proven`, Adequacy ADEQUATE, or human `goal_proven`

## When to use

- First look after overnight (`overnight_grok_from_list.ps1` or equivalent)
- Mid-morning "is the factory healthy?"
- Comparing last N overnights before deciding LFG / re-run / ship-drain

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Deep log forensics only | `/overnight-ops-audit` |
| Fix runner / factory code | `/lfg` after this pack names the aim |
| Factory code smell scan | `/factory-qc` |
| Controlled ship-prove entry | ship-prove skill / `scripts/run_ship_prove.*` |
| Live product field proof | `/field-test` + dual-gate path |
| Hyp / outer RSI promote | human checklist (`notes/ops/outer_rsi_unlock.md`) |

## Procedure (agent)

### 0) Resolve context

1. Resolve `PIPELINE_DIR` (`$env:PIPELINE_DIR`, `~/aicompete/thepipeline`, cloud `.pipeline/`, or ask once).
2. Confirm factory root (checkout with `.grok/skills/`, `pipeline/`, `COMMANDS.md`).
3. Note host clock vs overnight dir timestamps (America/Chicago for operator brief).

### 1) Overnight receipt audit (required)

Prefer the existing skill CLI:

```powershell
python .grok/skills/overnight-ops-audit/scripts/run_audit.py --pipeline-dir $env:PIPELINE_DIR --latest 1
# Optional compare:
python .grok/skills/overnight-ops-audit/scripts/run_audit.py --pipeline-dir $env:PIPELINE_DIR --latest 3 --json notes/ops/overnight_audit_latest.json
```

If CLI unavailable, reimplement the same finding classes from
`.grok/skills/overnight-ops-audit/SKILL.md` + `references/receipt-fields.md`
(`stall`, `auto_fix_thrash`, `soft_log_crash`, `exit`, `mass_mvp`,
`false_mvp_disk`, `dead_role_bus`, `side_effect`, `reseed_soak`, …).

Also run morning report if log dir known:

```powershell
python scripts/overnight_report.py --log-dir $env:PIPELINE_DIR\logs\overnight_YYYYMMDD_HHMMSS
```

### 2) Live ops dashboard (required)

```bash
python -m pipeline.pipeline_status
python -m pipeline.portfolio_metrics
# optional JSON for tooling:
python -m pipeline.portfolio_metrics --json
```

Capture: active projects, stuck/budget_exceeded, ship terminals, false-MVP risk,
engine fallbacks. Remember portfolio vocabulary:
`complete` ≠ `field_proven`; `field_test_passed` ≠ proven.

### 3) Honesty / hygiene peek (measure-only)

Run only read-only probes; skip any that fail soft:

```bash
# Truth density for the overnight window (if since-dir exists)
python scripts/report_truth_density.py --since "$PIPELINE_DIR/logs/overnight_YYYYMMDD_HHMMSS"

# Evidence edges for any slug the audit flagged (tooling claim ≠ proven)
# python -m pipeline.evidence_edges --slug <slug> --check-claim

# Seed / list hygiene signals from overnight dir if present
# seed_hygiene.log, morning_rows.json (see receipt-fields.md)
```

Optional process-pack smoke (factory integrity, not product proof):

```bash
python scripts/check_process_pack_v1.py
```

### 4) Compose the morning brief

Deliver in this order (keep it short):

1. **Headline** — overnight exit / time window / one-line health
2. **Severity counts** — from overnight-ops-audit
3. **Top findings** — ≤5, with class + evidence pointer (log line / path)
4. **Portfolio snapshot** — counts by honest status buckets (no invented proven)
5. **Reseed / soak** — present / absent / blocked (never call absence a pass)
6. **Human queue** — items that need the operator (hyp promote, outer RSI,
   ship-drain go/no-go, LFG aim, re-run overnight)
7. **Three options** (see below)

### 5) Three options — then STOP

1. **`/lfg <named fix aim>`** — only if Medium+ factory/runner bug is named with evidence  
2. **Re-run / continue overnight** — if code fix already on disk or process was stale; or controlled `-ShipDrain` / `-NoFreshListOnly` with caps  
3. **stop** — park; no silent follow-on skills

Do **not** auto-gap-to-plan, auto-encore, or auto ship-prove.

## Forbidden

- Auto `/lfg`, `/encore`, `/factory-improve`
- Claiming `field_proven` from a green-looking morning
- Mutating `projects/<slug>/` or rewriting overnight logs
- Mass `--ship-prove` / unfiltered drain
- Collapsing author / runner / judge into one self-prove step
- Treating meta_reasoner `ack` or evidence `--check-claim` as promote

## Non-claims

| Artifact | Is NOT |
|----------|--------|
| Overnight audit report | Product dual-gate proof |
| `morning_rows.json` / overnight_report | `field_proven` |
| `pipeline_status` green-ish view | Ship success |
| Truth-density field_proven/hour | License to mint new proven |
| Process pack smoke | Capability or goal proof |
| Reseed soak with zero lines | Pass (`no_reseed_lines`) |

## Related

- `.grok/skills/overnight-ops-audit/` — receipt CLI + finding classes  
- `notes/ops/dual_gate_contract.md` — mechanical ≠ proven  
- `notes/ops/ship_drain_overnight.md` — controlled drain runbook  
- `COMMANDS.md` — overnight preflight + status map  
- `notes/ops/outer_rsi_unlock.md` — human-gated outer RSI  
- `/factory-qc`, `/qc-honesty`, `/field-test` — adjacent, not substitutes  

## Fixture / acceptance (for Skill Forge later)

A good run of this skill produces:

- [ ] Named `PIPELINE_DIR` + overnight dir (or explicit "none")
- [ ] Audit severity table + ≥1 evidence pointer per Medium+ finding
- [ ] Portfolio counts using closed vocabulary (no new status strings)
- [ ] Explicit non-claim line: "No field_proven inferred"
- [ ] Exactly one of the three options recommended, then stop
