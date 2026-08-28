---
name: field-test
description: >-
  Design product field tests and run them with strict author≠runner≠judge
  separation (ship-prove field track). Writes phases/ship/field_tests.md,
  executes commands (or delegates to field_test_runner), records results —
  never claims FIELD PASS / field_proven without durable results evidence.
  Use when the user asks for field tests, ship-prove field testing, product
  proof, "prove it works", /field-test, /fieldtest, or interactive field repair.
metadata:
  short-description: "Plan + run field tests (dual-gate; no self-prove)"
---

# /field-test — Product field plan + run (dual gate)

Prove that a **finished** product meets its idea — with **three separate steps**.
You are **not** allowed to plan, run, and rubber-stamp proven in one uncritical pass.

## Dual-gate language (mandatory)

Factory contract inventory: `notes/ops/dual_gate_contract.md` (checkout-relative; shared vocabulary `pipeline/dual_gate_contract.py`). Mechanical pass ≠ field_proven; this skill must not self-prove.

| Claim | Meaning | Who decides |
|-------|---------|-------------|
| **Mechanical pass** (`field_test_passed`) | Commands in the plan ran green | Runner / shell evidence only |
| **Field proven** (`field_proven`) | Runner pass **and** adequacy ADEQUATE **and** min product/integration bars | Separate evaluator / dual gate — **not** this skill alone |
| **FIELD PASS** (results file) | All recorded tasks have real command evidence of pass | Only after step 2 results exist |

**Forbidden:**

- Treating “wrote `field_tests.md`” as FIELD PASS or field_proven
- Claiming field_proven / ADEQUATE without `field_test_results.md` evidence
- Inventing command output or exit codes
- Single-step “done when plan file exists”

## Grok Build thin ship vs this skill

| Path | Author | Runner | Judge |
|------|--------|--------|-------|
| **Thin field ship** (`pipeline/engines/field_ship.py`) | `FIELD_PLAN_ENGINE` = grok CLI / `pipeline_llm` / heuristic / existing file — **does not** auto-load this SKILL.md | Deterministic `field_test_runner` | Dual gate (`field_prove_gate`): mechanical pass ≠ field_proven |
| **Classic agents** | `field_test_planner` | runner | `ship_evaluator` (ADEQUATE closed verdicts) |
| **This skill** | Interactive plan | Shell or runner | Stop before self-judging proven; hand off or report mechanical evidence only |

Use this skill for **interactive** plan+run+repair. Overnight/from-list stops
at complete and does not thin-ship or crown field. Explicit ship-prove / thin
ship uses plan engines + runner + dual gate — not necessarily this file.

## When to use

- Project status is `complete` (or user points at a workspace to prove)
- Interactive ship-prove / repair after field FAIL
- "Field test this", "prove the product works"

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Phase code review | `/code-review` or build-track review packs |
| Full-repo bug hunt | `/comprehensive-codebase-review` |
| Factory runner stalls | `pipeline-bug-investigate` |
| Unit tests mid-phase | implement + pytest in build track |
| Mass ship-prove | classic `run_ship_prove` / thin ship ops |

## Inputs

| Input | Typical location |
|-------|------------------|
| **Project root** | `PIPELINE_DIR/projects/<slug>/` or user path |
| **Workspace** | `<project>/workspace/` — run all commands here |
| **Master plan / idea** | `<project>/state/master_plan.md`, `current_idea.json` |
| **Field plan** | `<project>/phases/ship/field_tests.md` |
| **Results** | `<project>/phases/ship/field_test_results.md` |

Python: absolute interpreter on every Command line.

---

## Workflow — three steps (do not collapse)

Track progress:

- [ ] **Step 1 — Plan only** → write `field_tests.md` (stop; do not claim pass)
- [ ] **Step 2 — Run only** → execute via shell or `field_test_runner`; write results
- [ ] **Step 3 — Stop before self-proven** → report mechanical evidence; optional evaluator handoff

### Step 1 — Plan only (author)

1. Recon: idea aim + workspace reality (entrypoints, public APIs).
2. Write **`phases/ship/field_tests.md`** per `references/field-tests-contract.md`.
3. Goals:
   - ~4–8 **product** (`P*`) and ~2–4 **integration** (`I*`) with **non-trivial Expect**
   - Prove product aim — not only `--help` / `py_compile` / bare import
   - Do **not** list baseline B1/B2/B3 (runner adds those)
4. **Stop.** Plan file existing is **not** success. Say: “Plan written; next: run.”

### Step 2 — Run only (runner)

From **workspace root**:

1. For each P/I task, run Command; check Expect (`exit N`, substring, `keys`, or `forbid`).
2. Prefer factory runner when available:

```text
# From factory checkout (conceptual)
python -c "from pathlib import Path; from pipeline.field_test_runner import run_all_field_tests, format_results_markdown; ..."
```

3. Write **`phases/ship/field_test_results.md`** with per-task PASS/FAIL, command, output tail.

```markdown
# Field Test Results

- Passed: N
- Failed: M
- Product aim: <one sentence>

## P1: <title> — PASS|FAIL
- Command: `...`
- Detail: ...

## Verdict: PASS|FAIL
```

**Results Verdict: PASS** only with real command evidence for product/integration tasks.
Smoke-only green is mechanical smoke — say so; do not imply field_proven.

If any task FAIL → classify and repair path (below); re-run; update results.

### Step 3 — Stop before self-judging proven (evaluator handoff)

After results exist:

1. Report **mechanical** outcome: runner PASS or FAIL + paths to plan/results.
2. **Do not** set project status to `field_proven` yourself.
3. **Do not** emit “FIELD PROVEN / ADEQUATE” unless a separate dual-gate path
   (thin ship `field_prove_gate` or classic `ship_evaluator`) has run on durable results.
4. Optional handoff language:

```text
Mechanical: field_test_passed | field_test_failed
Adequacy: not judged by this skill — use ship_evaluator / dual gate
Min bars: ≥1 non-trivial product + ≥1 non-trivial integration (defaults)
```

If user asks “is it proven?”: answer with dual-gate language — runner green alone is
**field_test_passed**, not **field_proven**.

---

## On failure — route, do not shrug

1. **Classify:** product bug | bad field test | environment | factory infrastructure
2. **Depth:** reproduce → fix or fix report → re-run (step 2 only)
3. Leave a fix report if not fully fixed
4. Never mark ship success if product objectives still fail

## Success criteria (this skill)

- Plan maps to idea aim (not generic “python works”)
- Results file exists with command evidence
- User sees dual-gate language (mechanical vs proven)
- No claim of field_proven / ADEQUATE without separate evaluator evidence

## Output to user

1. Product aim (one line)
2. Paths to `field_tests.md` + `field_test_results.md`
3. Pass/fail table (mechanical)
4. Mechanical verdict: **FIELD PASS** or **FIELD FAIL** (results only)
5. Explicit: **not field_proven** until dual gate / ship_evaluator ADEQUATE
6. Fix report / next step if FAIL

## Related skills

| Skill | When |
|-------|------|
| `pipeline-bug-investigate` | Factory/runner stalls |
| `code-review` / `review` | Structure blocks product behavior |
| `comprehensive-codebase-review` | Optional deep audit after systemic fails |
| `check-work` | Session verify after fixes |
