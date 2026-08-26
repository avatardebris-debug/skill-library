---
name: req
description: >-
  Define and inventory requirements before Occam/zero: explicit rows with id,
  statement, source, kind, falsifier, owner, status, load-bearing flag. Challenge
  convenience requirements; human-floor kinds (mission core, safety, honesty,
  constitution) stay keep/challenge-only for agents. Writes REQUIREMENTS.md. Use
  when /req, requirements inventory, "list requirements before zero", or as
  mandatory step inside /zero after mission. Not live delete; not gap-to-plan;
  not LFG.
---

# Req

Inventory requirements explicitly before any zero-based redesign or simplification.

## Purpose

- Make every requirement visible, owned, and challengeable.
- Distinguish load-bearing / human-floor requirements from convenience ones.
- Produce a durable REQUIREMENTS.md that later zero / gap-to-plan / implement steps can reference.

## Required columns (or equivalent structured form)

- id
- statement
- source (who / where it came from)
- kind (mission-core, safety, honesty, constitution, functional, non-functional, convenience, etc.)
- falsifier (how we would know it is wrong or unnecessary)
- owner
- status (proposed, accepted, challenged, dropped, deferred)
- load-bearing flag

## Process

1. Extract candidate requirements from the aim, conversation, existing docs, and code comments.
2. Write each as an explicit row.
3. Challenge convenience requirements aggressively.
4. Protect human-floor kinds (mission core, safety, honesty, constitution) — agents may only keep or challenge, never silently drop.
5. Write / update REQUIREMENTS.md.
6. Surface the inventory for human review before proceeding to zero.

## Rules

- No live deletion of code or requirements without human visibility.
- Prefer falsifiable statements over vague wishes.
- Keep the inventory short enough to be useful; merge or drop obvious duplicates.
