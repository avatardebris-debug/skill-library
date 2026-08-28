# Phase tasks contract (pipeline)

Write **`phases/phase_{N}/tasks.md`** under the **project root** (never under `workspace/`).

Factory: `PIPELINE_DIR/projects/<slug>/phases/phase_{N}/tasks.md`.

Grok Build driver and classic executors **require** this checkbox format.

## Required shape

```markdown
# Phase {N} Tasks: {Phase Title}

- [ ] Task 1: [title]
  - What: [clear description of what to implement]
  - Files: [paths relative to workspace/]
  - Done when: [how to verify]

- [ ] Task 2: [title]
  - What: ...
  - Files: ...
  - Done when: ...
```

## Critical format rules

1. Every task is a **top-level** bullet. **phase-plan always emits `- [ ]` (open)** — never pre-check `- [x]`.
2. `- [x]` is a **gated receipt**: under `/universal-gauntlet` factory mode, only the orchestrator flips checks **after independent critic ACCEPT** for that phase (not phase-plan, not builder self-grade). Outside gauntlet, implement may still check tasks per normal driver habit.
3. Nested lines under a task use two spaces + `- What:` / `- Files:` / `- Done when:`.
4. **Do not** use `##` / `###` headings for individual tasks.
5. **Do not** use emoji checkmarks — only `- [ ]` and `- [x]`.
6. **Only this phase** — no tasks from other phases.
7. Tasks are **ordered**; later may depend on earlier.

## Task count guidance (flexible)

| Phase size | Typical tasks | Hard max |
|---|---|---|
| Tiny phase | 2–3 | |
| Normal phase | 3–6 | |
| Large phase (Grok implement) | 5–8 | **10** |

- Size each task for roughly **one implement session** (about 25–40 tool steps / Grok max-turns budget).
- Prefer **fewer, clearer** tasks over micro-slices that thrash context.
- Soft guide is not “always 3–5”; choose fit. **Never more than 10** tasks per phase.

## Required content quality

1. **Atomic** — one concept per task.
2. **Testable** — Done when is verifiable (command, file exists, test pass).
3. Include **at least one verification/tests** task when the phase ships product code.
4. **Files** paths relative to `workspace/` (e.g. `cli.py`, `pkg/main.py`).
5. Optional trailing section (not tasks):

```markdown
## Out of scope
- [deferred items for later phases]

## Notes
- [assumptions]
```

## Overflow

If work truly exceeds 10 tasks, put the remainder narrative in **Out of scope** or recommend a new phase in the master plan — do not emit 15 checkboxes.
