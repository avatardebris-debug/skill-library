# Fixture: GOOD honesty / non-claim language (should NOT flag).
# honesty-fixture-good
# NEVER_TRAIN — scanner allowlist regression only; train_weight=0; corpus_exclude
# Phase 4 FP lock: H05 string-false / non-claims / **no** auto_lfg;
# H07 forbidden "auto_promote=True"; H10 Does **not** unlock outer RSI.

# field_proven = True is NEVER allowed without dual-gate
# candidate ≠ field_proven
# machine_success ≠ field_proven
# soft handoff ≠ auto-LFG
# accept ≠ execute
NON_CLAIMS = [
    "factory health ≠ field_proven",
    "does not claim goal_proven_human",
    "must not auto_promote",
]

# Honesty ban-list membership (H05 allowlist) — string entry, not execute
DOES_NOT_CLAIM = [
    "true_user_intent",
    "field_proven",
    "goal_proven_human",
    "auto_lfg",
]

# Documented refuse: never write process_packs
# never open constitution.yaml for write

# --- H05 FP class: soft handoff ban / False stamps ---
packet = {
    "auto_lfg": False,
    "constraints": ["no auto-LFG from this packet"],
}
# H05 FP class: quoted string false (JSON-ish soft seed)
soft_seed_meta = {
    "soft_seed_only": "true",
    "auto_lfg": "false",
}
# single-quoted string false also allowlisted
soft_seed_meta_sq = {
    'auto_lfg': 'false',
}
# Note-string deny form: bare "auto_lfg false"
notes = [
    "park ≠ delete",
    "auto_lfg false",
    "not auto_lfg",
]
# Soft factory-improve packet (no auto-LFG)

# Markdown honesty table false + bold ban word **no** auto_lfg
md_honesty = [
    "- field_proven: **false** (scorecard ≠ field_proven)",
    "- auto_lfg: **false**",
    "- **no** invent_human_verdict · **no** auto_lfg",
]
# H05 FP class: non-claims multi-token inventory (mid-bullet bare token)
non_claims_md = [
    "- invent_human_verdict · auto_lfg · public_agi",
]
# Never-sets inventory on one line (avoid line-wrap FP)
# Never sets field_proven / goal_proven_human / auto_lfg.

# --- H07 FP class: forbidden/deny-doc inventory (not live promote assign/call) ---
forbidden = [
    "auto_promote=True",
    "auto_primary=True",
]
human_commands = {
    "forbidden": [
        "auto_promote=True",  # H07 quoted forbid membership (not unquoted assign)
    ],
}
# never auto_promote / human promote only
# does not claim auto_promote; ban-before: does not auto_promote without human

# --- H10 FP class: outer RSI ban / deferred non-goal ---
honesty = {
    "not_outer_rsi": True,
    "outer_rsi_unlocked": False,
}
# **Do not** unlock outer RSI from these metrics
# does not unlock outer RSI or write train_weight
# Does **not** unlock outer RSI (markdown bold between ban words)
# Block RSI. Remeasure via gap-to-plan if needed.

# Refuse-list language (H08 allowlist) — not a write
raise ValueError(f"refusing write under process_packs: {path}")  # type: ignore[name-defined]
