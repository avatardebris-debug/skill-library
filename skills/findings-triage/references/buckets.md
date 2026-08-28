# Buckets — findings-triage

Closed enum. Path/rule heuristics in `scripts/run_findings_triage.py` implement these.

## A — safety-adjacent

Sites where soft-fail or import holes can hide **real safety/honesty regressions**.

**Path / name cues (any):**

- `shell_safety`, `field_prove`, `field_test_runner`
- `evidence_edges`, `_evidence_edges`
- `hypothesis_promote`, `complete_gate` (when coupled to proof)
- `constitution`, `process_packs` write smells
- `path_safe_slug`, mcp slug path builders when security-tagged
- rules: `H05`, `H07`, `H09`, security controls, `E02` on lock/import modules listed above

**Next:** implement pack preferred; treat as elevated even if QC severity is low.

## B — hot control-plane

Overnight / loop / budget surfaces where silent except causes **stall thrash**.

**Path cues:**

- `run_loop_health`, `run_loop`, `runner.py`
- `control_plane_invariants`, `run_loop_budget`
- `dead_role`, bus ageout modules
- `project_phase`, `stall_hygiene` (control-ish)

**Next:** pack ≤ max-per-pack; add tests when implementing.

## C — agent soft-except

Agent personas with intentional soft recovery.

**Path cues:**

- `pipeline/agents/`

**Next:** prefer soft_log_exc over bare pass; often defer unless same file is on fire.

## D — accept residual

Default for remaining **low/info** bulk (typical E02 across engines/finetune/util).

**Next:** document in `DEFER.md`; do not open LFG solely for D.

## Medium+ override

Any finding with severity in `{critical, high, medium}` is **ship-candidate** regardless of path bucket, and is listed first when building packs.
