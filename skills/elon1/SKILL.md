---
name: elon1
description: >-
  Elon-from-the-start: define requirements (/req new-work, agent look 1 then
  look 2), climb a tightness ladder, ship the smallest sufficient patch in this
  session, check keep/load-bearing via /gap-to-goal, stop. No zero/restore, no
  LFG, no auto-LFG.
  Use when /elon1, new workable problem, smallest sufficient automation, Elon
  culture from the start. Not after-the-fact compress (/elon2).
metadata:
  short-description: "Elon1: req → tightness → smallest patch → stop"
argument-hint: "[target] [--slug name]"
---

# /elon1 — Smallest sufficient (orchestrator)

New work. **Not** compress. Compress is `/elon2`.

You call existing skills. You do not reimplement `/req` or `/gap-to-goal`.
You do not run `/zero`, `/zero2`, `/restore`, `/lfg`, `/encore`, or gauntlet.

## Playlist

| Step | Action | Gate |
|------|--------|------|
| 0 | Lock target + mission (1–2 sentences) | Stop if mission muddy |
| 1 | **`/req` new-work** — cannot skip | Agent look 1 then look 2 (same turn, in order). No human wait |
| 2 | Load `references/tightness.md`; implement **keep + load-bearing** only | Same session; no gauntlet |
| 3 | **`/gap-to-goal` new-work** — patch vs keep rows | If not OK → back to 2 |
| 4 | **STOP** | Do not add |

## When to use

- One workable problem in front of you (Martian)
- New factory/product leaf that should stay tight
- After slice/gap-to-plan named **one** leaf to do

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Target already too big / density | `/elon2` |
| Requirements inventory only | `/req` |
| Multi-plan ship | `/lfg` after a req pack exists |
| Series too big | `/slice-deconstruct` first, then elon1 per leaf |
| Factory health | `/factory-qc` |

## Hard safety

1. Never skip `/req`. Do not wait for a human `look 2` token. `1` is not a job pick.  
2. Never live-delete. Never auto-LFG. Never invent field_proven.  
3. Never call `/zero` / `/zero2` / `/restore` from this skill.  
4. Never run `/lfg` or gauntlet inside this skill.  
5. Factory “never” language is binding unless the human waives a line in writing this session.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| **Target** | Yes | Path or named surface |
| **Mission hint** | No | Else extract 1–2 sentences |
| **Slug** | No | Default from target; pack under `notes/req/<slug>/` |

If the problem is still a series: tell the user to slice; do not one-shot.

## Workflow

### 0. Mission

Write 1–2 sentences. No modules. If muddy, stop.

### 1. `/req` (mandatory)

Load `.grok/skills/req/SKILL.md` (or `~/.grok/skills/req/SKILL.md`).

- Mode **new-work**  
- Out: `notes/req/<slug>/`  
- Look 1 writes the pack. Look 2 re-reads the file (critic hat), then
  continue. Same human turn, **in order**. Not parallel. No new skill.

Do not implement until look 2 **finishes** (agent-owned). Then step 2 in this
same turn.

**Human chat:** only the step 4 operator card. Do **not** paste the
requirements table. Do not wait mid-loop.

```text
Job
<1–2 sentences>

Change
<paths>. Pack: <path to REQUIREMENTS.md>. GOAL_COVERAGE: …

Risk
<one line>

Next
stop
```

### 2. Tightness + patch

Load `references/tightness.md`. Climb the ladder. Same agent, this session.
Only keep + load-bearing rows. Prefer reuse over new files.

### 3. `/gap-to-goal` (new-work)

Load `.grok/skills/gap-to-goal/SKILL.md`.

- Plan = what you just changed (paths + one-paragraph how)  
- Goals = `load_bearing: yes` + `status: keep` from the req pack  
- Skip capability matrix  

`GOAL_COVERAGE: OK` → step 4.  
`BRIDGE_REQUIRED` → step 2 again (smallest).  
`EXPAND_INSTEAD` → stop; tell user `/gap-to-plan` / `/lfg`, not more elon1.

### 4. Stop

Print the operator card (Job / Change / Risk / Next). Change includes files
touched and `GOAL_COVERAGE`. Next is `stop`.

Do not encore. Do not LFG. Do not list leftover leaves.

## Relationship

| Skill | Role |
|-------|------|
| `/req` | Step 1. Cannot skip |
| `references/tightness.md` | Step 2 ladder |
| `/gap-to-goal` | Step 3 watcher (new-work clause) |
| `/elon2` | Compress leftover gods — different playlist |
| `notes/ops/operator_method.md` | Culture card |

## Success criteria

- Req pack on disk with agent look 2 (no human wait)  
- Tightness loaded (not ponytail plugin)  
- Patch is the first sufficient rung  
- gap-to-goal ran against keep rows  
- No LFG / zero / restore from this run  

## Tone

Operator card to the human. Table on disk. Stop when falsifiers pass.
