---
name: factory-fanout
description: Workflow that takes a list of ideas or the output of suggest-next-5 / suggest-100-ideas and fans them out horizontally (or in controlled waves) through the software-factory skill. Supports apply-all on filtered subsets of 100 ideas. Use for /factory-fanout, apply all to software factory, fan out the ideas, run the 5 through factory, or process these N aims with software-factory.
metadata:
  short-description: Horizontal fan-out of ideas through software-factory with wave control
  version: "1.0"
  argument-hint: "[list | path-to-ideas | top-N] [--wave-size K] [--sequential | --parallel-waves] [--filter <criteria>]"
---

# Factory Fanout

You are the **horizontal factory orchestrator**. You do not implement product code yourself; you schedule and gate runs of software-factory.

## Core capability — Apply All

Yes. Given ~100 ideas (or any list), you can:

1. Filter / rank / cull to a workable subset (or accept user filter).
2. Partition into waves (default wave size 3–5 to avoid context and resource explosion).
3. For each idea in a wave, invoke the full software-factory pipeline (aim → idea lock → delineation → multi-agent work → QC → 5-opinion vote → target → gauntlet).
4. Track per-idea status in a shared board.
5. Proceed to the next wave only after the current wave has clear terminal states (shipped / parked / failed-with-evidence).

## Instructions

1. Ingest the idea list (user paste, notes/ideas/ideas-100-*.md, next-5, or explicit aims).
2. Confirm or apply filters (size, domain, risk, dependency). Default: top-ranked first.
3. Create durable board: .factory/fanout/BOARD.md (or status.json) with columns Idea | Wave | Status | Factory path | Outcome.
4. Choose mode:
   - Sequential (safest): one software-factory at a time.
   - Wave-parallel (default for >5): up to --wave-size concurrent factory runs with shared QC standards and no shared mutable main until merge agents coordinate.
5. For each selected idea:
   - Write a short AIM for it.
   - Load and run software-factory with that aim.
   - Record result and QC/gauntlet evidence paths.
6. After each wave, surface a wave summary and ask (or auto if user pre-approved) whether to continue.
7. Never silently drop ideas; parked ideas stay on the board with reason.

## Guards

- Hard cap concurrent factories unless user overrides (resource and coherence risk).
- Shared quality bar: every factory run must still hit its own TARGET via universal-gauntlet; fan-out does not lower the bar.
- If an idea is too large, auto-suggest slice-deconstruct or gap-to-plan first, then fan the slices.
- Respect user stop / pause at any wave boundary.

## Output

Keep the board live. Final summary lists shipped, parked, and failed with links to each .factory/ (or per-idea subdir) tree.
