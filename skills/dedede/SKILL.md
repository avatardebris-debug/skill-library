---
name: dedede
description: >-
  Delineate, deconstruct, and deep-research a process, company, campaign, or
  org into multi-level parts (depts, roles, processes, metrics) with readiness
  tags (replicate/defer/human_only/unknown). Prep pack for later fan-out /lfg
  or orchestrator - does NOT replicate or build the master caller. Use when
  the user runs /dedede, /DE, "deconstruct this company", "delineate the
  process", "map org into parts for LFG", "break down marketing/SEO/studio",
  or wants a structured handoff tree before fan-out. Do not use to run /lfg,
  /autosuggest, or implement replication (separate skills).
metadata:
  short-description: "Multi-pass deconstruct + readiness pack for later fan-out"
argument-hint: "<entity> [--focus a,b] [--max-depth 5] [--research auto|always|never]"
---

# /dedede - Delineate, Deconstruct, Deep-research

You are the **deconstruction orchestrator**. You map a real (or stated) system
into a **stable, multi-level tree** with honest **readiness** tags so later work
can fan out (`/lfg`, `/autosuggest`) or wire a master orchestrator.

**You do NOT:**

- Replicate departments or ship product code for leaves  
- Run full `/lfg` / `/autosuggest` on leaves  
- Build the master "caller of callers"  
- Claim human-level capability for any leaf  

**You DO:**

- Multi-pass deconstruct (breadth -> depth -> research hot branches -> readiness)  
- Optional `/deep-research` by **discretion**  
- Write a machine-usable pack under `deconstructions/<slug>/`  
- Tag **can't-try / human_only / defer** at map time; leave **can't-reach-bar** to later build  

## Defaults

| Setting | Value |
|---------|--------|
| Max depth | **5** (L0 entity .. L4/L5 process/metrics) |
| Research | **auto** |
| Leaf grain | Prefer **process** (or role+process); not dept alone |
| Replication | **none** in this skill |
| Critic bar | Map honesty only (medium): complete tree + readiness, not human-level |

## Composition (this skill only)

```text
1. Lock entity + scope + root non-aims
2. Breadth pass   L0-L1 (full tree, shallow)
3. Depth pass     expand high-value / focus branches (parts of parts)
4. Research pass  discretionary deep-research on unknown hot nodes
5. Readiness pass tag replicate | defer | human_only | unknown + metrics where real
6. Write pack     deconstructions/<slug>/
7. Summary        counts + handoff (do not auto-LFG)
```

Later (separate skills / human):

```text
fan-out: for leaf readiness=replicate -> /lfg or /autosuggest until harsh bar
orchestrator: timing + interfaces + caller of shipped modules
```

---

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| **Entity** | Yes | Company, campaign, process, department, product org |
| Focus | No | `--focus art,seo,engineering` |
| Max depth | No | `--max-depth 5` (cap 6) |
| Research | No | `--research auto\|always\|never` |
| User materials | No | Pasted org charts, SOPs, URLs |

If entity missing: ask once for the target system and intended use (e.g. "prep fan-out for LFG").

---

## Levels

| Level | Kind examples | Stop expanding when |
|------:|---------------|---------------------|
| L0 | company, campaign, program | Named top entity |
| L1 | department, workstream | Clear ownership bucket |
| L2 | role (junior/senior if duties differ) | Distinct process set |
| L3 | process / workflow | Someone could own a loop |
| L4 | sub-steps, tools, artifacts | Leaf is LFG-sized or must defer |
| L5 | metrics, SLAs, failure modes | Only if measurable or research-backed |

**Multiple deconstruct passes are mandatory** (not one flat brainstorm).

---

## Readiness (can't / can try) - owned here

Tag every **leaf** (and optionally whole branches):

| Tag | Meaning |
|-----|---------|
| `replicate` | Plausible software/agent loop with some eval or clear I/O |
| `defer` | Possible later; not practical this program |
| `human_only` | Judgment, taste, legal identity, original authorship, live authority |
| `unknown` | Insufficient structure/research - do **not** treat as replicate |

Each leaf needs a **one-line rationale** for the tag.

**Root non-aims** in `DE.md` (examples): not replacing human directors; not claiming legal entity; not inventing fake KPIs.

**Not owned here:** "we tried LFG and plateaued below human" - that is **build-after-dedede** evidence.

See `references/readiness.md`.

---

## Research discretion

| Run `/deep-research` when | Skip when |
|---------------------------|-----------|
| Industry-standard roles/pipelines unknown on disk | User supplied full internal map |
| Metrics non-obvious for a replicate candidate | Purely user-fictional org already detailed |
| Competing models of "how X works" | Breadth+depth already enough for readiness |
| User forced `--research always` | `--research never` |

**auto:** breadth+depth first; research only **hot** nodes with `unknown` or high fan-out value. Cap research calls (suggest <= 4 per run unless user expands).

Persist under `deconstructions/<slug>/research/`.

---

## Artifacts (required)

Create:

```text
deconstructions/<slug>/
  DE.md                 # overview, scope, non-aims, pass log
  tree.json             # full tree (ids, parents, levels)
  leaves.json           # leaves only + readiness + metrics stubs
  graph.md              # optional dependencies between nodes
  research/             # only if research ran
  nodes/                # optional long-form per important node
```

**Slug:** kebab from entity, e.g. `indie-game-studio`, `seo-campaign-q3`.

### tree.json node (minimum)

```json
{
  "id": "eng.backend.deploy",
  "name": "Production deploy process",
  "level": 3,
  "kind": "process",
  "parent_id": "eng.backend",
  "summary": "Ship backend to prod with checks",
  "inputs": ["merged PR", "CI green"],
  "outputs": ["release", "rollback plan"],
  "actors": ["senior engineer", "oncall"],
  "tools": ["CI", "k8s"],
  "metrics": [],
  "depends_on": ["eng.backend.ci"],
  "readiness": "replicate",
  "readiness_rationale": "Clear I/O and automated gates",
  "research_refs": [],
  "interface_hint": "CLI or webhook trigger"
}
```

`kind`: `entity | dept | role | process | artifact | metric | tool`

### leaves.json

Array of nodes that are **leaves** (no children to expand further under max-depth policy), each with readiness.

### DE.md sections

1. Entity + date + scope/focus  
2. Root non-aims  
3. Pass log (breadth / depth / research / readiness)  
4. Counts: nodes, leaves by readiness  
5. Hot branches expanded  
6. Handoff: do not LFG inside dedede; next is fan-out or manual `/lfg` on leaf ids  

Full field list: `references/artifact-contract.md`.

---

## Workflow (execute in order)

### 0. Bootstrap

1. Resolve workspace root.  
2. Parse entity, focus, max-depth, research mode.  
3. Create `deconstructions/<slug>/`.  
4. Write draft `DE.md` header (entity, non-aims placeholders).

### 1. Breadth pass (L0-L1)

- Name L0 entity.  
- List L1 departments/workstreams covering the system (and "other/ops" if needed).  
- No deep role lists yet unless tiny system.  
- If focus flags set: mark out-of-focus L1 as `defer` branch (shallow only).

### 2. Depth pass (parts of parts)

For each in-focus L1 (or all if no focus):

- Expand L2 roles (split junior/senior only if processes differ).  
- Expand L3 processes under roles.  
- Expand L4 tools/steps where it changes readiness or I/O.  
- Stop a branch when: max-depth hit, leaf readiness clear, or further split does not change readiness.  

Re-run depth on branches still marked conceptually "blob" until leaves are process-sized.

### 3. Research pass (discretion)

For nodes with `unknown` readiness or thin industry knowledge:

- Run `/deep-research` with tight query (entity + branch + "roles, processes, metrics").  
- Merge findings into tree (do not invent metrics).  
- Re-tag readiness after research.

### 4. Readiness + metrics pass

- Every leaf gets readiness + rationale.  
- Metrics only if measurable; else omit or mark `unknown`.  
- Fill `depends_on` when order is structural (assets before build, copy before SEO publish).  
- `interface_hint` for replicate leaves (how a later module might be called).  

### 5. Write pack

- `tree.json`, `leaves.json`, `graph.md`, finalize `DE.md`.  
- Optional `nodes/<id>.md` for high-value leaves (long notes).

### 6. Summary (stop)

```markdown
## dedede complete

- entity / slug / path
- nodes: N | leaves: M
- readiness: replicate=a defer=b human_only=c unknown=d
- research: skipped | ran (paths)
- recommended next:
  - fan-out later on replicate leaves: <top 5 ids>
  - do not /lfg from this skill
  - human_only highlights: ...
```

**Do not** auto-start `/lfg` or `/autosuggest`.

---

## Quality bar (map honesty)

ACCEPT-quality pack means:

- Multi-pass happened (not single brain-dump)  
- Every leaf has readiness + rationale  
- Root non-aims present  
- Replicate leaves have I/O or tools or process steps  
- No fake "proved human-level" claims  
- Focus branches deeper than out-of-focus  

---

## Anti-patterns

- Flat list of job titles with no processes  
- Tagging everything `replicate`  
- Inventing KPIs without basis  
- Implementing code or LFG inside dedede  
- Infinite taxonomy (split past max-depth / no readiness change)  
- Research on every node by default  

---

## Success criteria

- `deconstructions/<slug>/DE.md` + `tree.json` + `leaves.json` exist  
- Leaves classified; counts reported  
- Handoff clear for fan-out / orchestrator  
- No replication work claimed  

## Related

| Skill | Role |
|-------|------|
| `/deep-research` | Optional fuel for hot branches |
| `/suggest` | Product aims from a **codebase** (different) |
| `/lfg` | Later: ship one leaf/aim |
| `/autosuggest` | Later: multi-cycle aim loops |
| `/fanout` | Serial leaf LFG from this pack |
| `fanscale` | Parallel leaf workers (`/workflow fanscale`) |
| `/compose` | Future master caller (not this skill) |

## References

- `references/artifact-contract.md`  
- `references/readiness.md`  
- `references/levels.md`  
