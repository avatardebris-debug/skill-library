# dedede artifact contract

## Layout

```text
deconstructions/<slug>/
  DE.md
  tree.json
  leaves.json
  graph.md
  research/           # optional
  nodes/<id>.md       # optional
```

## tree.json

```json
{
  "schema_version": 1,
  "entity": "string",
  "slug": "string",
  "created": "ISO-8601",
  "max_depth": 5,
  "nodes": [ /* node objects */ ]
}
```

### Node object

| Field | Required | Notes |
|-------|----------|-------|
| id | yes | stable dotted or kebab id |
| name | yes | human title |
| level | yes | 0..5 |
| kind | yes | entity\|dept\|role\|process\|artifact\|metric\|tool |
| parent_id | yes | null for L0 |
| summary | yes | 1-3 lines |
| inputs | no | list |
| outputs | no | list |
| actors | no | role names |
| tools | no | systems |
| metrics | no | [{name, how, lagging\|leading}] |
| depends_on | no | list of node ids |
| readiness | leaf yes | replicate\|defer\|human_only\|unknown |
| readiness_rationale | leaf yes | one line |
| research_refs | no | paths or URLs |
| interface_hint | no | for replicate leaves |

## leaves.json

```json
{
  "schema_version": 1,
  "slug": "string",
  "leaves": [ /* subset of nodes that are leaves */ ],
  "counts": {
    "replicate": 0,
    "defer": 0,
    "human_only": 0,
    "unknown": 0
  }
}
```

## graph.md

Human-readable dependency notes:

```markdown
# Dependencies
- eng.backend.deploy depends on eng.backend.ci
- art.assets before eng.integration
```

## DE.md

Must include: entity, scope, non-aims, pass log, counts, handoff.
