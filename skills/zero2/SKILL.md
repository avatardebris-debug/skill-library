---
name: zero2
description: >-
  Code-level map after /zero: multi-filter analysis of functions/files against
  surviving concepts; propose merges, orphans, shares, splits — never live delete
  or in-place rewrite. Profiles: module (default), zero-cross (fan-out claim+critic
  across a path set). Use when /zero2, zero-code-map, map code to zero plan,
  cross-module redundancy candidates, or fan-out review of large surface for
  simplification. Plan/clone only; not /implement cutover.
---

# Zero2

After a `/zero` pass has produced the surviving concepts and from-scratch plan, map the existing code against those concepts.

## Purpose

- Identify what can be merged, shared, split, or treated as orphan.
- Produce a clear code-level simplification map.
- Never perform live deletes or in-place rewrites from this skill.

## Profiles

- **module** (default): analyze within a focused module or directory.
- **zero-cross**: fan-out claim + critic across a larger path set to surface cross-module redundancy.

## Process

1. Load the surviving concepts and plan from the preceding `/zero`.
2. Inventory functions / files in the target surface.
3. Apply multiple filters (concept match, duplication, responsibility, size, call graph, etc.).
4. Propose concrete merges, shares, splits, and orphans with rationale.
5. Output a durable map (markdown or structured notes) that a later human or implement step can follow.

## Rules

- Plan and clone only. No live mutation of the codebase.
- Prefer evidence (call sites, data flow, conceptual overlap) over taste.
- Keep the output actionable for a subsequent restore / implement pass.
