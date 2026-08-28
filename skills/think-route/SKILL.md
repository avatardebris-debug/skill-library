---
name: think-route
description: >-
  Coordinator for how to think on muddy intake or goal failure: pick a closed
  think-kind, name an existing actor, write a trace. Finite meta (depth 0, at
  most one nested layer). Use when /think-route, "which think kind", "route
  thinking on failure", or after a use/goal reject. Propose only — never
  auto-LFG, never execute the actor, never train, never invent field_proven.
  meta_reasoner is kind factory_meta only, not a portable thinking OS.
metadata:
  short-description: "Pick think-kind + actor; traces; no execute/LFG/train"
argument-hint: "--trigger muddy|failure|success|factory [--kind KIND] [--depth 0|1|2]"
---

# /think-route — Coordinator (not a thinking OS)

This skill **structures** thinking. It does **not** apply, iterate, or simulate
it. Existing skills are the actors.

```text
trigger (muddy|failure|success|factory)
    → closed kind + named actor + trace
    → human/actor disposes
    → never LFG from here
```

Req: `notes/req/think-route/REQUIREMENTS.md`  
Strong-form leaf: `notes/gap_plans/strong-form-agi-remeasure/plans/plan_T1_think_route.md`

**Think graph** (this) is not the **goal/KG graph** (bridge / `kg_library`).

## Closed kinds → actors

| Kind | Actor | When |
|------|-------|------|
| `question` | `/req` | muddy intake (default) |
| `deep_think` | `/harsh-critic` | failure at depth 0 |
| `verify` | `/gap-to-goal` | failure at depth 1 (meta) |
| `restructure` | `/elon1` | structure is wrong |
| `route` | `/suggest` | known job — **not** `/lfg` |
| `factory_meta` | `generate_proposals` (no enqueue) | factory self-model |
| `stop` | none | success, depth cap, or done |

Explicit rungs (finite; the model's associative/self depth is already inside each actor call):

| Depth | Name | Default kind on failure |
|------:|------|-------------------------|
| 0 | object | `deep_think` |
| 1 | kind-fit | `verify` |
| 2 | stance / self-relation | `question` |
| >2 | refused | `stop` (`depth_cap`) |

Gauntlet inner loops count as **inside** `deep_think`, not another rung. Do not emulate neurons/synapses.

## Workflow

1. Run:

```text
python -m pipeline.think_route --trigger failure
python -m pipeline.think_route --trigger muddy
python -m pipeline.think_route --trigger success
python -m pipeline.think_route --trigger factory
```

2. Print `kind` + `actor`. Do **not** invoke the actor unless the user names it after this output.
3. Trace is append-only under `notes/ops/think_route/traces.jsonl`.
4. **Stop.**

`factory_meta` may *read* `generate_proposals`. It must not enqueue, ack, or apply. Do not edit `PROPOSAL_TYPES`.

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Ship an aim | `/lfg` after the user picks (not from this skill) |
| Factory proposal quality | plan_02 / meta_reasoner Manager path |
| Walk a use-list row | `ROUTINE.md` |
| Train on traces | later, after labels trusted — not this skill |

## Honesty

- field_proven: false
- auto_lfg: false
- auto_execute: false
- train: false
- graph: think (goal graph is separate)

## Success criteria

- Kind is in the closed set (or refuse)
- Depth > 1 refused
- A trace line exists
- No actor auto-started
- No `notes/series/think-route/` tree
