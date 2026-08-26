---
name: slice-deconstruct
description: Recursively cut a multi-month capability series slice into smaller slices until leaves are gap-to-plan sized (gap_ready). Writes notes/series/<slug>/ tree + leaves with readiness tags; does NOT run gap-to-plan, LFG, or implement. Use when: /slice-deconstruct, /series-slice, "slice this Plan A phase", "break series into gap packs", "decompose multi-year slice into packs", or before fan-out of gap-to-plan on Plan A / multi-pack aims.
---

# Slice Deconstruct

Recursively decompose a large multi-month (or multi-year) capability series into gap-to-plan-sized leaves.

## Purpose

- Take a big “Plan A” or series slice and cut it until every leaf is small enough for a clean gap-to-plan.
- Produce a durable tree under `notes/series/<slug>/` with readiness tags.
- Do **not** run gap-to-plan, LFG, or implementation from this skill.

## Process

1. Accept the series / phase / Plan A description.
2. Recursively slice it into smaller pieces.
3. Stop when a leaf is `gap_ready` (suitable size and clarity for gap-to-plan).
4. Write the tree structure and leaf descriptions with readiness tags.
5. Surface the resulting pack list so the user (or a later fan-out) can run gap-to-plan on each leaf.

## Rules

- Pure decomposition. No implementation, no gap measurement, no shipping.
- Prefer fewer, clearer leaves over many tiny ones.
- Keep the original intent and constraints visible at every level of the tree.
