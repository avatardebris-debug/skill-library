---
name: lfg-all
description: Thin multi-aim ship: run /suggest once, human reviews the ranked list (or passes except/only filters), then serial full /lfg for every remaining rank. Unlike /autosuggest (auto-pick one aim, re-suggest, no human gate), /lfg-all never auto-selects and never skips the review gate unless except/only was given on the same turn. Use when the user runs /lfg-all, /LFG-all, "LFG all suggest ranks", "ship every suggested aim", or "lfg-all except 3&4". Do not use for ranked list only (/suggest), unattended auto-pick loops (/autosuggest), one fixed aim (/lfg), or residual continue (/encore).
---

# LFG All

Ship multiple aims serially from a single /suggest ranking, with a mandatory human review gate.

## Flow

1. Run `/suggest` (or reuse a recent ranking if the user points at one).
2. Present the ranked list clearly.
3. Wait for human review / filters ("except 3&4", "only 1 and 5", "go", etc.). Do **not** auto-select.
4. For each remaining rank in order, run a full `/lfg` cycle.
5. Surface status between aims; respect stop / pause.

## Rules

- Never skip the human review gate unless the user already supplied except/only filters on the same turn.
- Unlike autosuggest-style loops, this skill does not re-suggest or auto-pick the next aim.
- Each aim gets a complete LFG (research → gap-to-plan → gauntlet → review) before the next begins.
- Keep a durable board of which ranks have been shipped / parked / failed.
