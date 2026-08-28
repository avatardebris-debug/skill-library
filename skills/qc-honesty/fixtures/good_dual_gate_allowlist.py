# Fixture: GOOD dual-gate honesty / non-claim language (should NOT high-flag).
# honesty-fixture-good
# NEVER_TRAIN — allowlist samples for scanner regression only; train_weight=0
# Measure-only QC fuel. Not product code.

# mechanical pass ≠ field_proven
# complete ≠ field_proven
# soft residual ≠ product_complete
# soft demote ≠ hard block
# accept ≠ execute
# candidate ≠ field_proven

DOES_NOT_CLAIM = [
    "field_proven",
    "goal_proven_human",
    "auto_lfg",
    "accept_equals_execute",
    "invent_human_verdict",
    "soft_residual_equals_product_complete",
]

# Soft handoff ban stamps (H05 allowlist)
packet = {
    "auto_lfg": False,
    "field_proven": False,
    "accept_equals_execute": False,
    "hard_blocks_product_complete": False,
    "constraints": ["no auto-LFG", "never invent human_verdict"],
}
# H05 FP class: quoted string false + bold **no** ban (phase-4 lock)
soft_seed = {"auto_lfg": "false", "soft_seed_only": "true"}
md_ban = [
    "- **no** auto_lfg",
    "- invent_human_verdict · auto_lfg · public_agi",
]

# Markdown honesty tables
md = [
    "- field_proven: **false**",
    "- auto_lfg: **false**",
    "- soft residual ≠ product_complete",
]

# Never-sets inventory
# Never sets field_proven / goal_proven_human / auto_lfg / invent_human_verdict.

# H07 FP class: forbidden-list string (not live assign/call)
forbidden = ["auto_promote=True"]
# never auto_promote / human promote only

# H10 FP class: Does **not** unlock outer RSI (bold ban-before)
# Does **not** unlock outer RSI from dual-gate metrics
outer_rsi_unlocked = False

# Dual-gate contract language
HONESTY_RULE = (
    "mechanical pass (field_test_passed / runner all_passed) ≠ field_proven; "
    "field_proven requires runner pass + ADEQUATE + min product/integration bars"
)

# Telemetry audit (not crown)
telemetry_event = {
    "field_proven": False,
    "auto_lfg": False,
    "human_verdict": None,
    "soft_ne_execute": True,
    "note": "must not set field_proven from telemetry",
}
