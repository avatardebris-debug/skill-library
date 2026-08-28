# Gates → scorecard → router (factory-improve v0)

## Architecture

```text
hard gates (pass/fail) → scorecard (0..1 axes) → closed-enum router → handoff
```

Optional **meta-eval** only on borderline (top-2 within ε) or human audit — not every run.

---

## 1. Hard eligibility gates (boolean)

Any **fail** on a hard gate → route `defer` or `human` (no scoring theater).

| Gate id | Pass when | Fail → |
|---------|-----------|--------|
| `eligible_surface` | Surface is named module/project/skill path that exists or is a deliberate invent target | defer |
| `eligible_trigger` | Trigger ∈ {complete, field_proven, feature_expand, meta, human, quality_debt} | defer |
| `mission_aligned` | Not OOS vs doctrine / values (no medical weaponize, no dual-gate smuggle) | human |
| `coding_sized` | Plausible as software/skill work under factory budgets (not “unlock AGI”) | defer |
| `honesty_safe` | Improve does not require auto-promote, fake field_proven, or crown invent | human |
| `not_in_flight` | No competing LFG/gauntlet on same surface (or user overrides) | defer |
| `fixed_rules` | Improver will **not** rewrite dual-gate / invent threshold / critic ownership | human |

**Note:** `eligible_complete_or_field` is soft for meta “scan portfolio” mode: prefer surfaces with complete/field, but human may force any surface.

---

## 2. Scorecard axes (0.0–1.0)

Prefer **disk quant**. If unmeasured, use low-weight qual or leave 0.5 neutral and mark `source=unknown`.

| Axis | Prefer source | High means |
|------|---------------|------------|
| `potential_usefulness` | demand proxies, mission fit (qual ok) | would unlock many goals / reuse |
| `current_usefulness` | invoke counts, call sites, campaign solves | already earning keep |
| `potential_minus_current` | **derived** = max(0, potential − current) | classic expand priority |
| `attach_cost` | LOC/files estimate; invert for priority (high cost = high score here = bad) | expensive to change |
| `proof_debt` | failing tests, missing fixtures, honesty holes | needs quality |
| `composability` | registry edges / graph leaves if cheap | valuable as leaf |
| `operator_pain` | repeated human work signals if any | automatable pain |
| `honesty_risk` | mostly gate; residual soft score | risky to touch |

### Derived priority (default weights)

```text
priority = 0.35 * potential_minus_current
         + 0.20 * current_usefulness
         + 0.20 * proof_debt
         + 0.10 * composability
         + 0.10 * operator_pain
         - 0.25 * attach_cost
         - 0.15 * honesty_risk
```

Clamp display to sensible range; rank surfaces by priority.

**v0 honesty:** weights are starting policy, not science. Log them in the decision record.

---

## 3. Closed-enum router

**Only** these routes:

| Route | Meaning |
|-------|---------|
| `feature_expand` | Add capability to **existing** surface (budgeted; not greenfield) |
| `quality` | Tests, honesty, fixtures, refactor hygiene — no new product face required |
| `connector` | MCP / connector / requires-bridge to existing capability |
| `new_product` | New project/idea (LFG invent path); not expand-as-greenfield lie |
| `compose` | Multi-leaf combine / graph compose |
| `defer` | Not now |
| `human` | Borderline, values, or hard-gate soft fail needing person |

### Threshold policy (v0)

```text
if any hard gate fail:
  if honesty_safe or mission fail → human
  else → defer

elif proof_debt >= 0.7 and current_usefulness >= 0.4:
  → quality

elif potential_minus_current >= 0.35 and attach_cost <= 0.5 and honesty_risk <= 0.4:
  → feature_expand

elif missing_connector_signal and potential_usefulness >= 0.5:
  → connector

elif no_leaf_exists and potential_usefulness >= 0.6 and attach_cost high:
  → new_product

elif multi_leaf_near_miss:
  → compose

elif abs(priority_top - priority_second) < 0.08:
  → human   # borderline

else:
  → defer
```

`missing_connector_signal` / `multi_leaf_near_miss` / `no_leaf_exists` are **explicit booleans** set by the agent from inventory (registry, goal_route, handoff notes) — not free invent.

### Force flags

- User `--route X` allowed only if hard gates still pass (except human override of surface).
- Never force route that fails `honesty_safe`.

---

## 4. Meta-evaluator (optional second stage)

Use only if:

- borderline, or  
- human asked “explain”, or  
- first-time high-risk surface  

Output: each axis pass/mid/fail + **one sentence** — not an essay. Feeds human slack, not auto-execute.

---

## 5. Slack / negative feedback (Bateson-style, human layer)

- Borderline → `human`  
- No auto-encore after handoff  
- Max concurrent improve ships: prefer 1 surface  
- Budgets for feature_expand align with goal_amend_ladder defaults (≤~150 LOC / 3 files soft)  

---

## Does not claim

- Outer RSI  
- Optimal utility  
- field_proven or goal_proven from triage alone  
