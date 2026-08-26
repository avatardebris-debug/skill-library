---
name: zero
description: >-
  Zero-based redesign: mission, /req requirements inventory, minimum viable
  concepts, from-scratch plan, capability matrix, then /gap-to-goal and
  /harsh-critic. Occasional cleanup (e.g. before factory-qc on a small surface).
  Conceptual and plan/clone only — never live delete or in-place rewrite. Use
  when the user runs /zero, zero-based rethink, simplify from scratch, or
  Occam/Feynman redesign of existing code/tool/system.
---

# Zero

Zero-based redesign. Start from the mission and rebuild the conceptual minimum, then map the gap.

## Steps

1. **Mission** — restate the true purpose in the simplest possible terms.
2. **Requirements inventory** — run or invoke `/req` so every requirement is explicit and challengeable.
3. **Minimum viable concepts** — what is the smallest set of concepts that still deliver the mission?
4. **From-scratch plan** — describe how you would build it if nothing existed today.
5. **Capability matrix** — map required capabilities to the concepts.
6. **Gap analysis** — measure current state against the from-scratch plan (hand off to gap-to-plan / gap-to-goal when useful).
7. **Harsh critic** — attack the plan and the retained pieces.

## Rules

- Conceptual and plan/clone only. **Never** live-delete or in-place rewrite production code from this skill.
- Prefer deletion of concepts over clever retention.
- Keep human-floor requirements (safety, honesty, constitution, mission core) visible and protected.
- Output durable artifacts (REQUIREMENTS.md, ZERO_PLAN.md, etc.) under a clear location.

## Typical use

User says `/zero` or “zero-based redesign of X”. You walk the steps above and produce a clean conceptual restart that later implement / restore / LFG steps can follow.
