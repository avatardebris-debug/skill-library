---
name: aim-to-series
description: >-
  Bootstrap a large product/capability aim into a series pack (ROADMAP +
  leaves.json + first gap aims), then STOP for human skim before unattended
  /series-loop or /overnight-series. Optional thin research. Use when
  /aim-to-series, "make a series from this aim", "bootstrap ROADMAP", "replace
  my manual ask→series→loop", or overnight hits no_leaf/empty series. Do not
  auto-run series-loop, overnight-series, gauntlet, or invent field_proven.
metadata:
  short-description: "Large aim → series pack; human checkpoint before loops"
argument-hint: "[--slug SLUG] [--research thin|off] [--max-leaves N] <aim>"
---

# /aim-to-series — Aim → series pack (human gate)

You are a **bootstrap orchestrator**. You turn one large aim into a **series
pack on disk**, ready for `/series-loop` later. You **STOP for human review**.
You do **not** start `/series-loop`, `/overnight-series`, `/lfg`, or gauntlet
unless the user explicitly asks after the checkpoint.

Contract: `references/contract.md`.

## Defaults

| Setting | Value |
|---------|--------|
| `--research` | **thin** (off = skip) |
| `--max-leaves` | **12** (hard max **24**) |
| Auto series-loop | **never** |
| Auto overnight-series | **never** |
| field_proven | **never** |
| Series root as one mega-leaf | **never** |

## Composition map

```text
0. parse aim + slug
1. optional thin research (notes only)
2. draft series spine: themes → leaves (gap_ready / defer / human_only / forbidden)
3. write notes/series/<slug>/ (ROADMAP.md, leaves.json, SERIES.md brief)
4. optional: first 1–3 gap_to_plan_aim stubs only (not full gap packs unless asked)
5. write .aim-to-series/summary.md
6. STOP — human skim menu
```

## When to use

- Operator has a large aim and used to manually chat a series into existence
- `/overnight-series` or `/series-loop` stopped with `no_leaf` / empty ROADMAP
- Expanding a product line **with** an explicit aim string (not silent invent)

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Walk existing gap_ready leaves | `/series-loop` |
| Multi-wave overnight | `/overnight-series` |
| One leaf gap→plan→implement | `/gap-to-plan` + thin loop |
| Post-loop QC | `/after-series-qc` |
| Meta "invent what to build next" with no aim | `/suggest` / human; not silent overnight |

## Child skills / references (load as needed)

| Step | Skill / note |
|------|----------------|
| research thin | Prefer existing research/suggest notes; optional `/suggest` **read-only** ideas — do not auto-LFG |
| series readiness | `~/.grok/skills/dedede/SKILL.md` if present (deconstruct readiness) |
| grain | Keep leaves gap_to_plan sized; if still_series grain, mark expand_more / split |
| gap | Do **not** bulk `/gap-to-plan` all leaves unless user asks; stubs in leaves.json enough |

## Series pack layout (required)

```text
notes/series/<slug>/
  SERIES.md      # aim, non-aims, product honesty, recommended first leaf
  ROADMAP.md     # ordered leaf ids + one-line purpose
  leaves.json    # id, status, depends_on, gap_to_plan_aim, notes
```

`leaves.json` status vocabulary (closed): `gap_ready`, `done`, `defer`,
`forbidden`, `human_only`, `expand_more`. Default new leaves to `gap_ready`
only when the aim is concrete enough for `/gap-to-plan`; else `expand_more`
or `human_only`.

## Inputs

| Input | Default | Notes |
|-------|---------|--------|
| aim (positional) | required | Large capability / product aim |
| `--slug` | slugify(aim) | Directory name under `notes/series/` |
| `--research` | thin | `off` to skip |
| `--max-leaves` | 12 | Cap 24 |

## Durable state

```text
.aim-to-series/
  summary.md
  last_slug.txt
```

## Workflow

### 0. Bootstrap

1. Factory root (`notes/series/` should be creatable).
2. Require non-empty aim text.
3. Resolve slug (unique; if exists, ask to overwrite vs new slug — if unattended
   overnight handoff created this run, use `-v2` suffix rather than destroy).
4. Announce: `aim-to-series slug=… research=… max-leaves=…`.

### 1. Thin research (optional)

If `--research thin`:

- Skim workspace notes / SERIES siblings / skill-library patterns for priors.
- Write at most one short `notes/series/<slug>/research_thin.md` (bullets,
  links, open questions). No fake citations.
- If `--research off`, skip.

### 2. Spine

Deconstruct aim into **leaves** (not phases of one mega-plan):

- Each leaf: one `gap_to_plan_aim` sentence a `/gap-to-plan` can swallow.
- Dependencies explicit.
- Non-aims listed in SERIES.md (mills, unpaid Meshy-as-required, Unreal MCP,
  visual ACCEPT from stills, etc. as appropriate to domain).
- Cap leaf count; overflow → `expand_more` parent note, don’t emit 50 leaves.

### 3. Write pack

Create/update `SERIES.md`, `ROADMAP.md`, `leaves.json`. Honest: pack is a
**proposal** until human confirms.

### 4. Optional gap stubs

You may add empty `notes/gap_plans/<leaf-kebab>/` placeholders **or** only
aim strings in leaves.json. Do **not** run full `/gap-to-plan` + `/idea-plan`
for every leaf in this skill.

### 5. STOP menu

```markdown
## aim-to-series complete

- slug, path notes/series/<slug>/
- leaf counts by status
- recommended first leaf id
- non-claim: pack ≠ proven; no loop started

Choose ONE:
  1) skim / edit ROADMAP (human)
  2) /gap-to-plan on recommended first leaf
  3) /series-loop --series <slug> --leaves 1
  4) /overnight-series --series <slug> --waves 1 --qc-auto soft
  5) stop
```

**Forbidden to auto-pick 3–4.** Wait for user.

## Forbidden

- Auto-starting series-loop / overnight-series / LFG / gauntlet
- One leaf that is the whole series aim (`still_series` grain)
- Marking leaves `done`
- Claiming Meshy/visual/product ACCEPT
- Silent overnight invent with empty aim string

## Related

| Skill | Role |
|-------|------|
| `/series-loop` | After human OK |
| `/overnight-series` | After human OK |
| `/gap-to-plan` | First leaf |
| `/dedede` | Readiness aid |
| `/after-series-qc` | After loops |

## Success criteria

- [ ] `notes/series/<slug>/` has SERIES.md + ROADMAP.md + leaves.json
- [ ] ≤ max-leaves emitted; statuses from closed vocab
- [ ] Recommended first leaf named
- [ ] Agent stopped with choose-ONE menu; no loop auto-started

## References

- `references/contract.md`
- Prefer matching existing series-loop pack expectations (`leaves.json` fields
  series-loop already reads: readiness, depends_on, gap_to_plan_aim)
