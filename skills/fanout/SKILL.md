---
name: fanout
description: >-
  Consume a /dedede pack (deconstructions/<slug>/), select replicate leaves,
  run serial /lfg per leaf with harsh critic, write fanout/<slug>/ outcomes
  for later /compose. Prep for scaled runs via fanscale workflow. Use when the
  user runs /fanout, "fan out leaves", "LFG each replicate leaf", "build from
  deconstruction pack", or after /dedede when ready to ship modules. Do not use
  to deconstruct orgs (/dedede), single ad-hoc aim only (/lfg), or multi-aim
  auto loop without a DE pack (/autosuggest).
metadata:
  short-description: "DE pack -> serial leaf LFG -> fanout status registry"
argument-hint: "<pack-path|slug> [--ids a,b] [--max-leaves 5] [--critic harsh] [--resume]"
---

# /fanout - Leaf LFG from a dedede pack

You are the **fanout orchestrator**. You turn `replicate` leaves from a
`/dedede` pack into **shipped modules** (or honest plateau/fail), one leaf at a
time by default, and write a **registry** that `/compose` (later) can consume.

**You do NOT:**

- Re-run full org deconstruction (use `/dedede`)  
- Auto-build the master orchestrator (use future `/compose`)  
- LFG `human_only` or `defer` leaves without explicit user override  
- Claim human-level capability without harsh critic evidence  

**You DO:**

- Read `deconstructions/<slug>/leaves.json` + `tree.json`  
- Select and order leaves (topo by `depends_on` when possible)  
- Synthesize a **scoped /lfg aim** per leaf  
- Run **`/lfg`** with **harsh** critic (default)  
- Write `fanout/<slug>/` outcomes for resume and compose  

For **parallel at scale**, prefer the **`fanscale`** workflow (`~/.grok/workflows/fanscale.rhai`
or `/workflow fanscale`), which dispatches multiple leaf workers. This skill is
the **policy + serial default**.

## Defaults

| Setting | Value |
|---------|--------|
| Leaf filter | `readiness == replicate` only |
| Max leaves | **5** per run (cap 15) |
| Order | User `--ids`, else topo `depends_on`, else DE top list |
| Mode | **Serial** LFG per leaf |
| Critic | **harsh** |
| LFG max-plans | **2** (leaf-scoped; cap 3) |
| Live trading / capital | **never** auto; sandbox/paper only |
| Auto-compose | **never** |

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Pack | Yes | Path `deconstructions/hedge-fund` or slug `hedge-fund` |
| `--ids` | No | Comma leaf ids to force |
| `--max-leaves` | No | Default 5 |
| `--critic` | No | Default harsh |
| `--max-plans` | No | Default 2 for each leaf LFG |
| `--resume` | No | Continue unfinished leaves from fanout status |
| `--allow-defer` | No | Include defer only if user set |
| `--force-human` | No | Dangerous; default off |

Resolve pack:

- If arg is a directory with `leaves.json`, use it  
- Else `deconstructions/<arg>/`  
- Else fail with list of available `deconstructions/*`  

---

## Artifacts

```text
fanout/<slug>/
  status.json
  RUN.md                    # human summary of this run
  leaves/<leaf.id>/
    aim.md                  # synthesized LFG aim
    status.json             # shipped|plateau|failed|skipped|in_progress
    notes.md                # optional critic / plateau evidence
```

Do **not** silently rewrite dedede readiness; append outcomes here only.

### status.json (registry)

```json
{
  "schema_version": 1,
  "slug": "hedge-fund",
  "pack_path": "deconstructions/hedge-fund",
  "critic": "harsh",
  "max_leaves": 5,
  "selected": ["id1", "id2"],
  "order": ["id1", "id2"],
  "leaves": {
    "id1": {
      "status": "shipped",
      "aim": "...",
      "module_path": "optional/path",
      "lfg_gap": "notes/gap_plans/...",
      "updated": "ISO-8601"
    }
  },
  "stop_reason": null,
  "updated": "ISO-8601"
}
```

Per-leaf `status`:

| Status | Meaning |
|--------|---------|
| `pending` | Selected, not started |
| `in_progress` | LFG running |
| `shipped` | Harsh/integration ACCEPT; usable by compose |
| `plateau` | Tried; can't improve easily (evidence in notes) |
| `failed` | Unrecoverable |
| `skipped` | Dep missing, human gate, or user skip |

See `references/status-schema.md`.

---

## Workflow

### 0. Bootstrap

1. Resolve pack path; require `leaves.json` (+ prefer `tree.json`, `DE.md`).  
2. Create `fanout/<slug>/`.  
3. If `--resume`, load existing `fanout/<slug>/status.json` and continue non-terminal leaves.  
4. Else init fresh status.

### 1. Select leaves

1. Load all leaves from pack.  
2. Filter:
   - Default: `readiness == "replicate"`  
   - Drop `human_only` unless `--force-human` (log loud warning)  
   - Drop `defer` unless `--allow-defer`  
   - Drop `unknown`  
3. If `--ids`, intersect with filter (missing ids -> error list).  
4. Order:
   - Prefer topological sort using each leaf's `depends_on` (and parent chain if needed)  
   - Among ready set, prefer ids listed in DE.md "Top replicate" if present  
5. Cap to `max_leaves`; log dropped ids.  
6. Write `selected` + `order` into status; set each to `pending` if new.

**Dependency rule:** If leaf A `depends_on` B and B is not `shipped` in fanout status (and B is also selected later), either:

- Run B before A in serial order, or  
- `skip` A with reason `dependency_unmet: B` if B not selected and not already shipped  

### 2. Serial leaf loop

For each leaf id in `order`:

1. If status already `shipped` or `plateau` and `--resume`, skip.  
2. Set `in_progress`.  
3. **Synthesize aim** (write `leaves/<id>/aim.md`):

```text
Ship an offline/sandbox module for leaf `<id>` (`<name>`).

Process: <summary>
Inputs: ...
Outputs: ...
Tools/metrics: ...
Depends on: ...

Success: tests or fixtures prove the I/O contract; harsh critic ACCEPT.
Non-goals: live capital/orders; replacing human_only parents (CIO/CRO/CCO/PM authority);
claiming investment alpha; unsupervised production trading.
Interface hint: <interface_hint if any>
```

4. Load and run **`/lfg`** (`~/.grok/skills/lfg/SKILL.md`) with that aim text,
   `--critic harsh` (or user critic), `--max-plans` as configured.  
   - Override LFG encore prompt: after re-gap, **do not wait**; return to fanout.  
5. Map LFG outcome -> leaf status:
   - All plans ACCEPT + usable module -> `shipped`  
   - Dry-streak / can't improve -> `plateau` + notes  
   - Hard fail -> `failed` + notes  
6. Record `module_path` if discoverable (new package dir, CLI entry, etc.).  
7. Update `fanout/<slug>/status.json` after **every** leaf (resume safety).

### 3. Summary (stop)

Write `fanout/<slug>/RUN.md` and print:

```markdown
## fanout complete

- pack / slug
- selected / shipped / plateau / failed / skipped
- leaf table: id | status | module_path
- next:
  - /fanout <pack> --resume
  - /workflow fanscale  (parallel scale)
  - /compose when ready (not auto)
  - do not LFG human_only leaves
```

**Do not** auto-run compose or fanscale unless user asked.

---

## Safety doctrine (always)

- Prefer **paper/sandbox** modules for anything near orders or capital.  
- Outputs are **proposals, recon packs, monitors, drafts** unless user explicitly
  requests a live integration (still require human gate in aim non-goals).  
- Never auto-own `human_only` parent responsibilities.  

See `references/safety.md`.

---

## Relation to fanscale workflow

| | `/fanout` skill | `fanscale` workflow |
|--|-----------------|---------------------|
| Parallelism | Serial leaves | Parallel leaf agents |
| Policy | Full rules here | Agents must follow this skill |
| Resume | status.json | Per-run journal + status writes |
| When | Default, first pilots | Scale after serial works |

When invoked from fanscale, each agent handles **one leaf id** end-to-end
(status under same `fanout/<slug>/`, careful not to clobber whole-file status
without merge - prefer write `leaves/<id>/status.json` then optional aggregator).

---

## Anti-patterns

- One LFG for whole company  
- Ignoring readiness tags  
- Parallel in this skill without user asking fanscale  
- Silent skip of dependency failures  
- Marking shipped without tests/critic  
- Mutating dedede pack readiness in place  

## Success criteria

- `fanout/<slug>/status.json` exists with terminal statuses for attempted leaves  
- Each attempted leaf has `aim.md`  
- No human_only leaves shipped as automated owners  
- Clear handoff to resume / fanscale / compose  

## Related

| Skill / workflow | Role |
|------------------|------|
| `/dedede` | Source pack |
| `/lfg` | Per-leaf ship |
| `fanscale` | Parallel host |
| `/compose` | Future master caller |

## References

- `references/status-schema.md`  
- `references/aim-template.md`  
- `references/safety.md`  
