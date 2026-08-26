---
name: universal-gauntlet
description: >
 High-effort, long-running quality gauntlet for any ambitious goal.
 Runs builder <-> independent critic loops with durable GOAL.md state until a hard,
 inspectable quality bar is met. Factory mode: sequential phase-plan → implement →
 per-phase critic gate (no N+1 until ACCEPT); builder never owns task [x] or master_plan
 DONE — orchestrator flips those only after critic ACCEPT. Use when the user wants
 maximum quality, AAA / production-grade results, continuous improvement until perfect,
 multi-hour runs, multi-agent fan-out with skeptics, factory plan ships with honest
 gates, or says "gauntlet", "highest standards", "keep going until perfect",
 "SpaceXAI of Duty", "Claude of Duty style", or runs /universal-gauntlet. Do not use
 for small one-shot edits or casual Q&A.
---

# Universal Gauntlet

High-effort builder ↔ independent critic loops until a hard, inspectable quality bar is met.

## Core loop

- Durable GOAL.md (or equivalent) holds the target quality bar and current state.
- Builder proposes / implements.
- Independent critic evaluates against the bar and issues ACCEPT / REJECT with evidence.
- Only the orchestrator (not the builder) marks tasks complete or master plan DONE after critic ACCEPT.

## Factory mode specifics

- Sequential phase-plan → implement → per-phase critic gate.
- No advancing to phase N+1 until the current phase has critic ACCEPT.
- Builder never owns the final [x] or DONE flag.

## Rules

- The quality bar must be hard and inspectable (not “looks good”).
- Critic is independent; do not let the builder grade its own work.
- Persist evidence and decisions so the loop can be resumed or audited.
- Prefer continuing until the bar is actually met over declaring early victory.

## Typical use

Ambitious aims that need production-grade or AAA quality. Compose with software-factory, gap-to-plan, and the test-* skills.
