---
name: deconstructor
description: >
  LLM-deconstruct an org, credits list, tool surface, or genre into typed candidate
  nodes (skill|prompt|mcp_simple|mcp_complex|factory|human|research|process).
  Uses pipeline deconstructor agent/prompt → deconstruct.v0 JSON. Bridge to draft
  graph.v1 via to-graph (never smoke_pass). Not production graph.
  Use when: /deconstructor, "deconstruct this org", "break down credits",
  "tool surface inventory", "genre systems breakdown", or before graph engineer.
---

# Deconstructor (LLM)

**Job:** Extrapolate 80/20 structure from a target (including short titles) →  
**candidate inventory + replacement classes** → optional **draft** graph.v1 map.

**Not:** production `graph.v1`, auto-attach sockets, auto MCP wrap, or auto `smoke_pass`.

This is a **pipeline agent** (like idea_planner): system prompt + LLM call + schema critique.  
A bare title is valid input for `run`. Do **not** use structure-only `build` expecting invention.

## How to call

### Primary — LLM

```text
python scripts/deconstructor.py run --mode org --target "award-winning modern game studio"
python scripts/deconstructor.py run --mode org --target-file mission.txt
python scripts/deconstructor.py run --mode credits --target "NES platformer credits list"
```

Env (same as rest of factory):

- `PIPELINE_DIR`
- `PIPELINE_PROVIDER` (default `ollama`)
- `PIPELINE_MODEL` (default pipeline model)
- `OLLAMA_PLANNER_TIMEOUT`

Agent process:

```text
python -m pipeline.agents.deconstructor --target "community hospital" --mode org
```

### Secondary — no LLM

| Command | When |
|---------|------|
| `build` | Target **already** lists parts (bullets / `Dept: a,b`). Bare title → `needs_structure` exit 2 |
| `from-json` | You already have candidate JSON |
| `validate` / `plan-fill` / `list` | Post-process |
| `to-graph` | Bridge saved deconstruct → **draft** `graph.v1` under `$PIPELINE_DIR/graphs/` |

Offline/test inject (no live model):

```text
python scripts/deconstructor.py run --mode org --target "studio" --inject-response fixture.json
```

## Closed classes

`skill | prompt | agent_role | mcp_simple | mcp_complex | factory | human | research | process | process_series`

After a good deconstruct:

```text
python scripts/deconstructor.py plan-fill --id <id>
# skill leaves → create-skill → register --sandbox → promote → attach
# mcp_simple → mcp_factory wrap + smoke (manual; not auto from to-graph)
```

## Draft graph bridge (Phase 4)

**Draft graph ≠ smoke_pass.** Convert only maps candidates → nodes/edges.

```text
# After deconstruct (run/build/from-json):
python scripts/deconstructor.py to-graph --id <deconstruct_id> [--goal-id <gid>]
# or:
python scripts/goal_compose.py from-deconstruct --id <deconstruct_id> [--goal-id <gid>]

# Store: $PIPELINE_DIR/graphs/{goal_id}.json  schema graph.v1  status draft|critiqued
# production_graph: false · smoke_pass: false · nodes all status=draft

# Smoke is a SEPARATE step (after nodes resolve / factories fill):
python scripts/goal_compose.py smoke --goal-id <gid>
```

Mapping:

- `replacement_class` → closed `NODE_KINDS` via `CLASS_TO_GRAPH_KIND`
- `oracle_hint` → oracle stub (not proof)
- `parent_id` → hierarchy edges
- optional `plan_fill` metadata on graph notes — **no** auto MCP wrap

## Agent workflow (this chat)

1. Call `run` (or ask the model to emit deconstruct.v0 JSON and `from-json`).
2. Check `critique.ok` and that names match the **domain** (hospital ≠ game studio).
3. `plan-fill` → fill via block_registry / MCP factory habits.
4. `to-graph` → draft map only; never claim executable/smoke_pass from convert alone.
5. Never set `production_graph: true`.

Store: `$PIPELINE_DIR/deconstructs/{id}.json` schema `deconstruct.v0`.  
Draft graphs: `$PIPELINE_DIR/graphs/{goal_id}.json` schema `graph.v1`.
