---
name: autosuggest
description: >-
  Auto multi-cycle factory loop: run /suggest, auto-select the best aim, run
  full /lfg, then /suggest again - default 4 LFG cycles. Durable state under
  .autosuggest/. Use when the user runs /autosuggest, "auto LFG loop", "suggest
  and LFG N times", "autonomous aim loop", or wants unattended suggest->select->lfg
  repeats. Do not use for a single ranked list only (/suggest), one fixed aim
  (/lfg), or residual-only continue (/encore).
metadata:
  short-description: "suggest -> select -> /lfg, default 4 cycles"
argument-hint: "[theme] [--loops 4] [--research auto|always|never] [--critic medium|harsh] [--max-plans 3] [--resume]"
---

# /autosuggest - Suggest, select, LFG (repeat)

You are the **autosuggest orchestrator**. Each cycle:

```text
/suggest  ->  auto-select best aim  ->  /lfg <aim>
```

By default run **4** full cycles (suggest again after each LFG). You **do** auto-select
and **do** run `/lfg` (unlike bare `/suggest`). You **do not** auto-run `/encore`
between cycles - prefer a fresh `/suggest` so aims update from new disk state.

## Defaults

| Setting | Value |
|---------|--------|
| Loops | **4** (cap 8) |
| Suggest research | **auto** (passed through to `/suggest`) |
| LFG critic | **medium** |
| LFG max-plans | **3** |
| Auto-encore | **never** (next cycle re-suggests) |
| Human gate mid-loop | Only on dry-streak / no viable aim / hard failure |

## Composition map

```text
for cycle = 1 .. loops:          # default loops=4
  1. Load and run /suggest       # ~/.grok/skills/suggest/SKILL.md
  2. Auto-select one aim         # rules below
  3. Load and run /lfg <aim>     # ~/.grok/skills/lfg/SKILL.md
       - On LFG step 7 (encore prompt): do NOT wait for user;
         record "skipped encore - next autosuggest cycle"
  4. Log cycle result to .autosuggest/
  5. Early-stop checks
report summary; stop
```

**Never** invent aims without running the suggest workflow (snapshot + rank).  
**Never** flatten suggest into a one-line guess.

## Inputs

| Input | Default | Notes |
|-------|---------|--------|
| Theme / constraint | none | Forwarded to `/suggest` |
| `--loops N` | 4 | Cap 8 |
| `--research` | auto | Forwarded to suggest |
| `--critic` | medium | Forwarded to LFG |
| `--max-plans` | 3 | Forwarded to LFG |
| `--resume` | off | Continue from `.autosuggest/status.json` |

---

## Durable state

```text
.autosuggest/
  status.json           # cycle index, aims chosen, paths, stop reason
  cycles/
    01_suggest.md       # full suggest output that cycle
    01_lfg_summary.md   # short LFG outcome
    02_...
```

### status.json (minimum)

```json
{
  "skill": "autosuggest",
  "loops_target": 4,
  "cycle": 1,
  "theme": "",
  "research": "auto",
  "critic": "medium",
  "max_plans": 3,
  "cycles_done": [],
  "aims_used": [],
  "stop_reason": null,
  "updated": "ISO-8601"
}
```

Each `cycles_done` entry: `{ "n", "aim", "suggest_path", "lfg_status", "gap_post", "notes" }`.

Update after **every** cycle for resume / compaction recovery.

---

## Workflow

### 0. Bootstrap

1. Workspace root; create `.autosuggest/cycles/`.
2. Parse loops / research / critic / max-plans / theme.
3. If `--resume` and status has incomplete cycles, continue at next `cycle`.
4. Write initial status; announce: `autosuggest loops=N critic=... theme=...`.

### 1. Cycle loop (1..loops)

For each cycle `n`:

#### 1a. Suggest

1. Load **`/suggest`** (`~/.grok/skills/suggest/SKILL.md`).
2. Run full suggest with theme + `--research` mode.
3. Save ranked output to `.autosuggest/cycles/NN_suggest.md` (NN zero-padded).

#### 1b. Auto-select

Pick **exactly one** aim using these rules (first match wins):

1. Highest-ranked aim with priority **high** that is **not** in `aims_used` (normalize: lowercase, collapse whitespace).
2. Else highest **medium** not in `aims_used`.
3. Else if only **low** or repeats of used aims: **early-stop** (`no_viable_new_aim`).
4. Else if suggest says preferred next is **stop** / only "not recommended": **early-stop** (`suggest_stop`).
5. Prefer aims whose "Success looks like" is verifiable on disk after LFG.

Record selection rationale in the cycle log (1-3 sentences).

**Do not** select:

- Aims marked "not recommended now" (including Hard DEFER)  
- Factory/meta aims with no req pack — same rule as `/suggest`
  `references/aim-rubric.md` Hard DEFER (load that file; do not copy it here)  
- Near-duplicate of an aim already in `aims_used` this autosuggest run  
- Vague slogans that fail the suggest aim quality bar  

If the only leftovers are those: **early-stop** `factory_meta_no_pack` (or
`suggest_stop` if suggest already said stop). Do not LFG them.  

#### 1c. LFG

1. Load **`/lfg`** (`~/.grok/skills/lfg/SKILL.md`).
2. Run with: selected aim text, `--critic`, `--max-plans`.
3. **Override LFG step 7:** after re-gap, do **not** block on human encore prompt.
   Write re-gap path into cycle summary and continue the autosuggest loop.
4. On LFG hard failure (research empty, dry-streak pause that needs human, critic stuck 3x,
   **or req-gate STOP** — factory/meta, no pack, no waiver):
   - Log failure; **do not** mark the cycle as LFG success.
   - **early-stop** unless user said `--force-continue` (not default).
5. Append aim to `aims_used`; write `.autosuggest/cycles/NN_lfg_summary.md`.

#### 1d. Early-stop checks (after each cycle)

| Condition | stop_reason |
|-----------|-------------|
| `n == loops` | `loops_complete` |
| No viable new aim | `no_viable_new_aim` |
| Suggest recommended stop only | `suggest_stop` |
| Only factory/meta no-pack DEFERs left | `factory_meta_no_pack` |
| LFG unrecoverable failure (incl. req-gate STOP) | `lfg_failed` |
| Same aim selected twice despite filter | `aim_thrash` |
| User cancel / STOP file if present | `cancel` |

If early-stop: break loop, go to summary.

### 2. Final summary (always)

```markdown
## Autosuggest complete

- cycles_target / cycles_ran
- stop_reason
- aims_used (list)
- per cycle: aim, lfg status, key artifact paths
- residual: point at latest post-gap + .lfg/status.json
- next human options: /suggest | /lfg <aim> | /encore | /autosuggest --resume | stop
```

Do **not** start another autosuggest or encore unless user asks.

---

## Selection heuristics (detail)

When two high aims tie:

1. Prefer **hard-find / product capability** over pure docs  
2. Prefer **closes large residual** from latest re-gap  
3. Prefer **smaller max-plans fit** if both high ROI  
4. Prefer theme match if user passed a theme  

When suggest research=auto and cycle > 1: usually **skip** deep-research inside suggest
if the just-finished LFG re-gap is fresh (disk-rich); still re-snapshot.

---

## Interaction with LFG encore

| Skill | Role in autosuggest |
|-------|---------------------|
| `/lfg` | Full ship cycle for selected aim |
| `/encore` | **Not** auto-invoked between cycles |
| Next `/suggest` | Replaces encore as "what next" under automation |

If after LFG the only residual is the **same aim unfinished**, next suggest may re-propose
a **narrower residual aim** (OK) but not the identical string if marked complete.

---

## Anti-patterns

- Infinite loops without `loops` cap  
- Skipping suggest and hard-coding aims  
- Running 4 LFGs on the same aim  
- Waiting on encore prompt between cycles  
- Claiming success without cycle logs on disk  
- Starting cycle 5 when default loops=4  
- Auto-selecting a factory/meta aim with no req pack  
- Counting an LFG req-gate STOP as cycle success  

## Success criteria

- `.autosuggest/status.json` complete with stop_reason  
- For each completed cycle: suggest markdown + lfg summary on disk  
- Up to `loops` LFG runs unless early-stop  
- Final summary for human  

## Related

| Skill | Path |
|-------|------|
| suggest | `~/.grok/skills/suggest/SKILL.md` |
| lfg | `~/.grok/skills/lfg/SKILL.md` |
| encore | `~/.grok/skills/encore/SKILL.md` (manual only here) |
| req / elon1 | Factory/meta no pack → not a selectable autosuggest aim |

## References

- `references/loop-contract.md`  
