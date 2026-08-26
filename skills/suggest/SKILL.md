---
name: suggest
description: Suggest high-ROI aims for /lfg from the current workspace: inventory disk state, residual gaps, receipts, and optional discretionary deep-research when external context or unknowns matter. Outputs ranked, copy-pasteable /lfg aim lines with rationale. Use when the user runs /suggest, /suggest-aim, "what should I LFG next", "suggest aims", "next aim for LFG", "what to ship next", or is stuck choosing between encore vs new aim. Do not use to run full /lfg (use /lfg) or continue a cycle (/encore).
---

# Suggest

Produce a short ranked list of high-ROI aims that are ready for `/lfg` (or the full research → gap-to-plan → gauntlet pipeline).

## Process

1. Inventory the current workspace: code, notes, `.factory/` artifacts, residual gaps, recent receipts, open TODOs.
2. Identify unfinished threads, high-leverage next pieces, and any obvious blockers.
3. Optionally perform light external research if the domain has important unknowns.
4. Rank candidate aims by expected ROI, readiness, and strategic fit.
5. Output 3–7 ranked, **copy-pasteable** `/lfg <aim>` lines, each with a one- or two-sentence rationale.

## Output format

```
1. /lfg <concise aim statement>
   Why: ...
2. /lfg ...
   Why: ...
```

Keep the list short and actionable. The user should be able to pick one and run it immediately.
