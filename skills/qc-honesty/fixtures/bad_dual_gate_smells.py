# Fixture: intentional BAD dual-gate honesty smells for qc-honesty smoke (do not import).
# honesty-fixture-bad
# NEVER_TRAIN — adversarial defect samples; corpus_exclude; train_weight=0
# Do NOT feed into finetune / goal_trace train_weight / session-distill SFT pairs.
# Measure-only QC fuel. Not product code. Not under pipeline/ or workspace/.

# --- Dual-gate crown invent (H01 / H02) ---
field_proven = True
payload = {"field_proven": True, "status": "field_proven"}

# --- complete collapsed into field_proven (H11-ish language as assignment) ---
complete_gate_result = {"field_proven": True, "status": "complete"}
# force complete as field stamp:
product_complete_as_field_proven = True

# --- invent human verdict stamp (not apply_human_verdict path) ---
goal_proven_human = True
human_verdict = "PASS"  # invent_human_verdict smell (static fixture only)
status = "goal_proven_human"

# --- soft residual wrongly crowned product complete ---
soft_residual_equals_product_complete = True
soft_demote_product_complete_confidence = False
hard_blocks_product_complete = True  # soft path must never hard-block; bad if true as crown

# --- auto path (H05 / H06 / H07) ---
auto_lfg = True
accept_equals_execute = True
auto_apply = True
auto_promote = True
# live promote call (H07 True stamp)
auto_promote(payload)  # type: ignore[name-defined]
# --- outer RSI True unlock (H10) ---
outer_rsi_unlock = True
