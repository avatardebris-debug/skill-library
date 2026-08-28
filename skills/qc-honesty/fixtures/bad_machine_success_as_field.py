# Fixture: intentional BAD mix of goal machine_success → product field.
# honesty-fixture-bad
# NEVER_TRAIN — adversarial defect samples; corpus_exclude; train_weight=0

machine_success = True
field_proven = machine_success
goal_proven_human = machine_success
if machine_success: field_proven = True
