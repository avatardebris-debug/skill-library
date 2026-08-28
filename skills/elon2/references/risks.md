# Early risk capture (cheapest gate)

Capture risks **during planning**, before any human accepts zero or restore.
Do **not** wait for ship. Live code stays untouched.

Elon2 only (after-the-fact compress). Not Elon1.

## Why early

| When risk is found | Cost |
|--------------------|------|
| Before human accept | Notes only; plan amend free |
| After accept, before clone | Still free; amend portfolio |
| During clone | Rework + tests |
| After cutover | Highest |

## Artifact

```text
notes/zero/<slug>/BLAST_RADIUS.md
```

Optional machine summary: `risks.json` (same dir).

Write a **first draft as soon as target paths are known** (after `/req` or early
in `/zero2`). **Refresh** after zero2 candidates and before restore human pack.

## Required sections

### 1. Target shape

- paths, scale (`module` | `package` | `system`), LOC/file count if known

### 2. Importers / callers (blast radius)

Grep (or equivalent) for imports and string refs to the public surface:

| consumer path | symbols used | if API moves/drops… |
|---------------|--------------|---------------------|
| … | … | CLI break / graph compile / agent bus / tests |

Always include: tests, scripts/, agents, any graph/compile bridges.

### 3. Public contract (do not silently shrink)

List symbols/constants that external callers rely on (from importers + `__all__`
if present). Split/merge proposals must name a **façade / re-export** strategy
or list every consumer update.

### 4. Proposal → risk rows

For each high/med `propose_*` (from REQUIREMENTS propose_delete, CONCEPTS
pruned, zero2 candidates):

| id | proposal | risk | who breaks | mitigate before accept | residual if ship |
|----|----------|------|------------|------------------------|------------------|
| … | drop prose invent | med | free-text offline users; some tests | keep LLM path; note structure-only limits | thinner offline invent |
| … | split module | high | all `from X import Y` | keep façade; freeze tests; clone only | import thrash if no façade |

### 5. Floor / honesty risks

Any plan that could touch save roots, graph production writes, field_proven,
auto_lfg, dual-gate → **block** until explicit do_not_touch + human waiver.

### 6. Mitigations already in plan

Bullet list: façade, tests to run, clone-only, leave deleted, etc.

### 7. Open questions for human

3–8 plain questions (product usage, risk appetite, contract ownership).  
These feed the **completion pack** (see `completion-pack.md`).

## Severity guide

| Level | Meaning | Planning response |
|-------|---------|-------------------|
| **block** | Floor/honesty or multi-consumer silent break | Do not present as ACCEPT without bridge |
| **high** | Split / cross-module merge / drop used API | Façade + consumer table + clone-only default |
| **med** | Behavior drop with workaround | Document who loses what; restore tier |
| **low** | Docs/LOC/local helper | Note only |

## Mitigations library (reuse)

1. **Façade** — keep old import path; move guts only.  
2. **Freeze tests** — list pytest/CLI smokes that must stay green.  
3. **Clone/worktree only** — never in-place first cut.  
4. **Quarantine not delete** — move suspect path behind flag / private `_` with note.  
5. **Leave deleted on paper** — Tier C; no code change.  
6. **Bridge owner** — name which package owns shared constants (e.g. graph kinds).  
7. **Caps** — zero-cross path/package caps; no whole-repo default.

## Relationship

- `/zero2` F7 Coupling **must** feed this file for module targets.  
- `/restore` reads residual risks when scoring Tier A/B.  
- `/elon2` completion pack **must** surface top risks + questions in plain English.
