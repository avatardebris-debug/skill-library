# Scale routing — module vs folder vs worktree

Redundancy hunting and Occam are the **same skills**; the **profile and caps**
change with surface size. Prefer **not** inventing a second top-level skill
unless zero-cross + outside-twin scan repeatedly fail.

Elon2 only. New work uses Elon1 (`notes/ops/operator_method.md` + `/req`).

## The single-file trap

Looking only *inside* one file:

- **Misses** twin helpers in other files (should **share/merge**).  
- **Over-proposes** splits (file is long) without checking whether a concept
  already has a home elsewhere.  
- **Under-proposes** “call existing util” when F5 / an outside-twin look would catch it.

**Mitigation (default):** every module-scale `/zero2` looks **outside** the
target for twins of focus symbols, plus merge-vs-split so F3 and F4 do not
fight. That is **not** a separate skill.

This worktree `/zero2` ships **F1–F7**. If `zero2/references/peer-scan.md`
exists, run F8 as written. If missing: bounded grep of focus symbols /
importers into `BLAST_RADIUS.md` — do not invent a new zero2 leaf this run.

## Decision table

| Target shape | Elon2 `--scale` | zero2 profile | Redundancy focus | Notes |
|--------------|-----------------|---------------|------------------|-------|
| One file / thin module | `module` (default) | **module** + outside twins + partition | Internal orphans/dups + **outside twins** + merge↔split | Importer blast radius mandatory |
| Small folder / package (≤ ~15 files) | `module` or `package` | module over folder; F3 in-folder; twins outside package | Intra-package dups + external shares | Still one mission |
| Multi-package / subsystem | `system` | module on spine + **zero-cross** | Cross-package ownership of merges | Caps: ≤8 packages default |
| Whole worktree / monorepo | **not one elon2** | slice or multi-elon2 | Only via capped packages or series leaves | `slice-deconstruct` or repeated elon2 |
| Multiyear series | n/a | per leaf | n/a | slice-deconstruct first |

## Merge vs split (elon2 must not ignore friction)

| Bias | Source | Counterweight |
|------|--------|---------------|
| Split everything long | F4 / LOC reviews | Partition rubric; façade; co-locate same concept |
| Merge everything similar | F3 / outside twins | Different concepts / floors / change rates → split or boundary |
| One file always better | Fake simplicity | Reviewability + blast radius |
| Many files always better | Fake modularity | Import thrash; no façade |

`/elon2` completion pack should say in plain English: **what we would merge,
what we would split, and why those are not in conflict.**

## Why not two (or three) separate skills?

| Concern | Answer |
|---------|--------|
| “Need wide look for dups” | Bounded outside-twin look on every module run |
| “Folder needs different approach” | Same filters; **scope** expands; zero-cross for multi-package claims |
| “Merge vs split is hard” | Partition after F3/F4 — still zero2 |
| “Worktree needs different skill” | Unbounded tree → slice/caps, not a new Occam |
| New skill cost | Dual maintenance, dual human packs, split metrics |
| When to revisit | If outside-twin + zero-cross still miss systematic monorepo dups after **3+** pilots → thin `redundancy-map` **leaf** under zero2 (not a parallel `/elon2`) |

## Redundancy heuristics by scale

### Module (single file)

- F2 orphans, F3 local, F4 god-file  
- Outside twins / already-shared  
- Partition so merge and split proposals do not fight  
- Blast radius = importers of **this** module  

### Package / folder

- F3 across files in folder  
- F5 share opportunities (slug utils, soft_log already shared?)  
- Still one MISSION / REQUIREMENTS pack  

### System / zero-cross

- Fan-out packages with **claims** so two agents don’t both “own” the same merge  
- Cross-package `propose_merge` defaults to **high** risk  
- Integration critic + partition across packages  
- BLAST_RADIUS must list **inter-package** edges  

## Operator flags

```text
/elon2 path/to/file.py --scale module
/elon2 path/to/pkg/ --scale module          # package as one surface
/elon2 path/to/subsystem --scale system    # enable zero-cross
/elon2 . --scale system                    # force caps; prefer slice first if huge
```

Optional child flags (pass through to zero2): `--no-peer-scan` (rare).

If user passes a directory or `.` without scale:

1. Count files/packages.  
2. If multi-package and not `--no-cross`, **recommend** `--scale system` or
   slice; do not silently whole-repo fan-out.  
3. Note in ELON_STATUS which profile ran, whether an outside-twin look ran, and why.
