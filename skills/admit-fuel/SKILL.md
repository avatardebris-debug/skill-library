---
name: admit-fuel
description: >-
  Score Ted digests and research fuel at intake: usefulness, cost, risk,
  unify vs divert, coherence. Emit ADMIT|MODIFY|DEFER|REJECT scorecards under
  notes/ops/ted_scored/. Directs fuel into /suggest; never auto-LFG or promote.
  Use when /admit-fuel, "score Ted notes", "admit research fuel", intake
  ranking, or pre-suggest admission. Not /elon2 compress; not /lfg ship.
metadata:
  short-description: "Score research fuel ADMIT/MODIFY/DEFER/REJECT; no auto-LFG"
argument-hint: "[path|fixture] [--aims-file path] [--no-write]"
---

# /admit-fuel — Research fuel admission (not compress)

You run **admission scoring** on research notes before they become ship pressure.

```text
Ted notes → score → ADMIT|MODIFY|DEFER|REJECT → /suggest only from ADMIT+MODIFY
                                                      ↓
                                              human gate → sparse LFG
                                                      ↓
                                         density high → /elon2 (compress)
```

**Not** `/elon2` (that deletes/simplifies **code** after surplus).  
**Not** `/lfg` (that ships).  
**Not** auto-promote.

## Defaults

| Setting | Value |
|---------|--------|
| Source | `notes/ted.txt` or fixture |
| Out | `notes/ops/ted_scored/<stamp>/` + LATEST |
| Auto-LFG | **never** |
| Human final | **always** (heuristic floors only) |

## Workflow

1. Workspace root.  
2. Run scorer:

```text
python -m pipeline.research_fuel_admission --path notes/ted.txt --json
# or
python -m pipeline.research_fuel_admission --fixture --json
# score suggest-style aims
python -m pipeline.research_fuel_admission --aims-file aims.json --json
```

3. Read `notes/ops/ted_scored/LATEST.md` (or stamp path).  
4. Present summary: verdict counts, shippable rows (ADMIT+MODIFY) with factory_map, DEFER/REJECT one-liners.  
5. **Stop.** Recommend next: `/suggest` (honor shippable only) · `/elon2 <hot>` if density · `stop`.  
6. Never invoke `/lfg` or `/lfg-all` from this skill.

## When to use

- After Ted appends a digest  
- Weekday ops: `python scripts/ops_import_ted_weekday.py --score`  
- Before `/lfg-all go` on research-heavy ranks  
- Human asks “is this paper shippable?”

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Compress god-module | `/elon2` / `/zero2` |
| Rank product residual from disk only | `/suggest` |
| Adversarial redesign plan | `/harsh-critic` |
| Ship code | `/lfg` |

## Verdict policy (repeat to human)

| Verdict | Feed `/suggest`? |
|---------|------------------|
| ADMIT | Yes |
| MODIFY | Yes — must name unify path |
| DEFER | No ship rank (inventory OK) |
| REJECT | No |

Prefer human gate **`only 1`** / **`only 1,2`**, not go-all-5.

## Honesty

- field_proven: false  
- auto_lfg: false  
- auto_promote: false  
- Scorecard is heuristic; human may override verdicts in writing  

## Related

| Path | Role |
|------|------|
| `pipeline/research_fuel_admission.py` | Scorer CLI |
| `notes/ops/ted_research_charter.md` | Ted briefing (streams A+B) |
| `notes/ops/ted_research_parallel_efficiency.md` | Parallel efficiency track (does not replace SOTA digest) |
| `notes/ops/ted_hit_list.md` | Stream B targets |
| `notes/ops/suggest_admission_bar.md` | Shared bar |
| `suggest/references/aim-rubric.md` | Ship-aim axes (extended) |
| `/elon2` | Compress after density |
| `/harsh-critic` | Plan REJECT default |

## Success criteria

- Scorecard on disk  
- Verdict counts shown  
- No LFG launched  
- Shippable set explicit and small  
