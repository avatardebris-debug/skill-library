---
name: factory-improve
description: >
  Factory triage skill for idea-impl2: after product complete / field_proven (or
  goal-route feature_expand), run eligibility gates → lightweight scorecard →
  closed-enum router → decision record → handoff to /lfg (or thin quality pass).
  For system/meta agent prompting and complete-gate routing—not the primary human
  aim ship loop (/lfg, /encore). Use when user or meta runs /factory-improve,
  "triage factory improve", "post-field expand route", "what to improve next on
  complete projects", or complete_gate suggests capability improvement.
metadata:
  short-description: "Gates+scorecard+router → improve handoff (not outer RSI)"
argument-hint: "[surface|auto] [--route force] [--no-handoff] [--continue-lfg]"
---

# /factory-improve — Triage when/what/how to improve

You are the **factory-improve orchestrator** for **this monorepo factory**
(idea-impl2 and its pipeline / cloud projects). You **classify and hand off**.
You do **not** replace `/lfg` unless the user passes `--continue-lfg` or explicitly
asks to run LFG after the packet.

**Not outer RSI.** Fixed doctrine and dual-gate stay fixed. Human/budget slack is
negative feedback. See `references/rsi-boundary.md` and
`references/gates-scorecard-router.md`.

## When to use

| Trigger | Action |
|---------|--------|
| Product / idea **complete** or **field_proven** | Triage expand vs quality vs connector vs defer |
| Goal-route / amend **feature_expand** | Name surface; score; packet |
| Meta: “what capability to improve?” | Score candidates; pick top route |
| Human: `/factory-improve` | Same |

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Human full aim cycle (known aim) | `/lfg` |
| Continue LFG residual | `/encore` |
| Single known implement | `/implement` / gauntlet |
| Outer unattended self-rewrite of gates | **Refuse** (deferred outer RSI) |

## Composition map

```text
0. Lock surface(s) + mission/values snapshot
1. Hard eligibility gates (pass/fail)  -> fail => defer|human
2. Lightweight scorecard (axes 0-1)
3. Closed-enum router                 -> route
4. Write decision record (.factory-improve/)
5. Handoff packet (lfg | thin_quality | none)
6. STOP (or --continue-lfg only if user asked)
```

## Closed routes (only)

`feature_expand` | `quality` | `connector` | `new_product` | `compose` | `defer` | `human`

## References (load these)

| File | Role |
|------|------|
| `references/status-schema.md` | `.factory-improve/` layout |
| `references/gates-scorecard-router.md` | gates, axes, thresholds |
| `references/handoff-packet.md` | LFG / thin quality packet |
| `references/rsi-boundary.md` | not outer RSI |
| `references/examples/sample_decision.md` | worked example |

## Durable state

```text
.factory-improve/
  status.json
  decisions/<decision_id>.md
```

Create dirs when writing the first decision.

---

## Workflow (full)

### 0. Bootstrap

1. Workspace root = factory monorepo.  
2. Ensure `.factory-improve/decisions/` can be created.  
3. Load `notes/doctrine.md` (mission/values) if present.  
4. Resolve **surface**:
   - User arg (path/slug), or  
   - `auto`: list 3–7 candidates from complete/`product_complete`/field signals + high proof_debt modules; rank later.  
5. Init `decision_id` = `fi_YYYYMMDD_HHMMSS` (or surface short + stamp).

### 1. Gates

Apply hard gates from `gates-scorecard-router.md`.  
Any hard fail → set route `defer` or `human`, write record, stop (unless user overrides surface with full awareness).

### 2. Scorecard

Score each axis 0.0–1.0 with `source` (quant|qual|unknown|derived).  
Compute `potential_minus_current` and `priority` with default weights (log weights in record).

### 3. Router

Apply threshold table → **one** closed enum.  
If top-2 priorities within 0.08 → `human` (borderline) unless user `--route`.  
Never route `feature_expand` if expand-as-greenfield cues fire (from-scratch, entire platform).

### 4. Decision record

Write `.factory-improve/decisions/<id>.md` using status-schema shape.  
Update `.factory-improve/status.json` (`latest_decision_id`, route, surface).

### 5. Handoff

Fill packet per `handoff-packet.md`.

- `feature_expand` / `connector` / `new_product` / `compose` → usually `mode=lfg` + aim line  
- `quality` → usually `mode=thin_quality`  
- `defer` / `human` → `mode=none`  

Print for user/meta:

```text
factory-improve decision: <id>
surface: …
route: …
mode: …
suggested:
  …
```

### 6. Stop / continue

**Default: stop.**  

Only if user said `--continue-lfg` or “run lfg on this packet”:

1. Load `/lfg` skill.  
2. Aim = packet aim.  
3. Critic medium unless user said harsh.  

**Never** auto-encore.

---

## Anti-patterns

- Second LFG that always ships without triage  
- Auto-encore / always-on self-improve tick as this skill’s default  
- Claiming outer RSI or prove crowns  
- Free-form routes outside the enum  
- Essay meta-eval every time  
- Inventing usage metrics not on disk  

## Related skills

| Skill | Role |
|-------|------|
| `/lfg` | Execute full aim after packet |
| `/encore` | Residual after LFG |
| `/gap-to-plan` | Inside LFG |
| `/universal-gauntlet` | Phase gates inside LFG |
| `goal_amend_ladder` | Goal-local feature_expand signal (upstream) |

## Success criteria (one run)

- Decision record on disk  
- Route ∈ closed enum  
- Handoff packet printed  
- No prove-crown claims  
- Stopped unless continue explicitly requested  
