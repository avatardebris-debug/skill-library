# Fixture: intentional BAD soft-pass / soft≠execute honesty smells (do not import).
# honesty-fixture-bad
# NEVER_TRAIN — adversarial defect samples; corpus_exclude; train_weight=0
# Do NOT feed into finetune / goal_trace train_weight / session-distill SFT pairs.
# Measure-only QC fuel. Not product code. Not under pipeline/ or workspace/.

# --- H05: auto-LFG / automatic LFG execute language ---
auto_lfg = True
auto_run_lfg = True
run_lfg_automatically = True
payload = {"auto_lfg": True}

# --- H07: auto_promote True assign (must flag; not quoted forbidden) ---
auto_promote = True

# --- H06: accept equals execute / auto_apply ---
accept_equals_execute = True
accept_means_execute = True
auto_apply = True

# --- Soft residual collapsed into product complete (honesty collapse) ---
soft_residual_equals_product_complete = True
soft_demote_product_complete_confidence = False
# Soft pass treated as execute:
soft_pass_means_execute = True

# --- invent human verdict (soft path crown) ---
human_verdict = "PASS"
goal_proven_human = True
