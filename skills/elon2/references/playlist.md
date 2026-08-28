# /elon2 playlist (invoke existing skills)

Formerly `/elon`. After-the-fact compress only. Not Elon1.

Orchestrator only — load each skill’s SKILL.md and follow it. Do not reimplement Occam/filters inside elon2.

## Default playlist

| Step | Skill / action | Human gate? |
|------|----------------|-------------|
| 0a | **Optional** `factory-qc` (measure health / aim fuel) | No (report only) |
| 0b | **Optional** `comprehensive-codebase-review` if surface unknown | No |
| 0c | **Scale routing** — pick module vs system; note in ELON_STATUS (see `scale-routing.md`) | Soft (agent chooses; human can override) |
| 0d | **Early blast seed** — start `BLAST_RADIUS.md` (importers/callers) as soon as paths known | No |
| 1 | **`/req`** (compress mode) | Soft (challenge queue) |
| 2 | **`/zero`** (includes gap-to-goal + harsh-critic) | **Yes** — conceptual approve *(may defer single stop until restore if full elon2 continues)* |
| 3 | **`/zero2`** module: F1–F7 + outside-twin look + refresh BLAST_RADIUS | Soft |
| 4 | **Optional** `/zero2` profile **`zero-cross`** if multi-package + scale system (caps) | Soft |
| 5 | **`/restore`** (read residual risks when scoring tiers) | **Yes** — portfolio accept |
| 5b | **Completion pack** — plain English risks + questions (`completion-pack.md`); stop | **Yes** — combined human pack |
| 6a | Thin restore → clone/worktree implement only if human B-style approve | **Yes** |
| 6b | Fat restore / new aim → `/gap-to-plan` then planner+gauntlet **or** `/lfg` | **Yes** |
| 7 | **Optional** comprehensive-codebase-review and/or factory-qc remeasure | No |
| 8 | **Optional** “automate?” only if cycle boring/repeatable | **Yes** |

## Scale flags

| Flag | Behavior |
|------|----------|
| `--scale module` | Single file or small package; skip zero-cross unless user forces |
| `--scale package` | Treat as module profile over a folder; intra-package F3; still skip zero-cross unless system |
| `--scale system` | Allow zero-cross with **caps** (≤8 packages / path caps in zero2) |
| Multiyear series | **Before** elon2: `slice-deconstruct`; each leaf may get its own `/elon2` or `/lfg` — do not embed series inside one elon2 |

See `scale-routing.md` for redundancy-by-scale (not a separate skill).

## Risk timing (non-negotiable)

1. Seed blast radius **before** human is asked to accept a plan.  
2. Refresh after zero2 proposals.  
3. Surface top risks in the **completion pack**, not only in deep md files.  
4. High/block risks → propose mitigations (façade, freeze tests, leave deleted) **before** letter options.

## Skip matrix

| User says | Skip |
|-----------|------|
| restore-only | 0–4 if pack exists; run 5+ (still require BLAST_RADIUS if missing) |
| zero-only | Stop after 2 human pack; still write BLAST_RADIUS seed + plain risks |
| no-qc | Skip 0a and 7 |
| no-cross | Skip 4 |

## Never

- Auto-LFG / outer RSI from elon2  
- Live delete / in-place rewrite of production  
- Whole-repo zero-cross without caps  
- Accept presentation without plain-language risks/questions  
- Breathing loop (compress↔expand forever without human)  
- Invent a parallel “redundancy skill” by default — use zero2 module / zero-cross  
- Run this playlist as Elon1 (new work) — use `/req` new-work + operator_method  
