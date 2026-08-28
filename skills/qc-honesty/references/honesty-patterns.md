# Honesty anti-patterns (factory QC)

Doctrine: `notes/ops/dual_gate_contract.md`  
Prefer **false negatives** over noisy comment hits. Lines matching allowlist
prefixes (`# honesty`, `≠`, `non-claim`, `NON_CLAIMS`, `does not claim`) are skipped.

| Id | Severity | Heuristic (Python-ish) | Why bad | Recommendation |
|----|----------|------------------------|---------|----------------|
| `H01_field_proven_true` | high | `field_proven\s*=\s*True` (assignment) | Auto-stamps dual-gate crown | Never assign True outside dual_gate path |
| `H02_field_proven_true_json` | high | `"field_proven"\s*:\s*true` in code (not tests of scrub) | JSON stamp of field proof | Keep false / scrub on write |
| `H03_goal_proven_human_auto` | high | `goal_proven_human\s*=\s*True` without human_verdict context nearby | Collapses provisional→human | Only via apply_human_verdict accept |
| `H04_provisional_as_human` | medium | `status\s*=\s*["']goal_proven_human["']` in non-verdict modules | Status invent | Use provisional until human |
| `H05_auto_lfg` | high | `auto[_-]?lfg|auto_run_lfg|/lfg.*auto` execute-ish | Soft handoff becomes ship | Soft prompt only |
| `H06_accept_equals_execute` | medium | `accept\s*==\s*execute|accept_means_execute|auto_apply\s*=\s*True` | Meta accept runs work | accept ≠ execute |
| `H07_auto_promote` | high | `auto[_-]?promote\s*=\s*True|auto_promote\s*\(` | External/capability promote | Human promote only |
| `H08_pack_rewrite` | high | `process_packs.*(write\|overwrite\|rewrite)` or `rewrite.*process_pack` | Forbidden write surface | Refuse list |
| `H09_constitution_write` | high | `open\(.*constitution\.yaml.*['\"]w` or write to constitution.yaml | Core doctrine mutate | Read-only |
| `H10_outer_rsi_unlock` | medium | `outer_rsi.*=\s*True|unlock.*outer[_-]?rsi` | Outer RSI claim | Deferred non-goal |
| `H11_complete_as_field` | medium | `complete.*field_proven|field_proven.*complete_gate` collapse language as assignment | complete ≠ field | Keep gates separate |
| `H12_soft_fail_silent` | low | `except\s+Exception\s*:\s*pass` near handoff/prove keywords (optional noisy) | Hides honesty path failures | Use soft_log |
| `H13_machine_success_as_field` | medium | `field_proven = machine_success` or same-line `if machine_success … field_proven = True` | Goal suite green sold as product field | Keep goal lane ≠ field lane (`notes/ops/goal_vs_field.md`) |

## Allowlist (skip line)

- Contains `≠` or `!=` near the match (non-claim)
- Contains `never`, `must not`, `non-claim`, `NON_CLAIMS`, `does not claim`, `honesty:`
- Contains `no auto-LFG` / `not auto-LFG` (ban language)
- Path under `notes/qc/`, `*/test_*.py` fixtures marked `# honesty-fixture-good`
- Comments documenting the ban (not implementing it)

## Rule-aware allowlists (residual triage 2026-08-01)

| Rule | Skip when | Keep flagging |
|------|-----------|---------------|
| `H01` | path is `pipeline/field_prove_gate.py` (sole dual-gate/legacy promote assigns) | `field_proven=True` anywhere else |
| `H05` | `auto_lfg: False` / `"auto_lfg": False` / `row["auto_lfg"]=False`; markdown honesty ``auto_lfg: **false**`` (optional `*+` around false); **quoted string false** `"auto_lfg": "false"` / `'false'` (JSON-ish soft-seed maps); bare note deny `auto_lfg false` / `"auto_lfg false"`; `no`/`not`/`never auto-LFG` with optional markdown bold around ban word (``**no** auto_lfg``); `(no auto-LFG)`; string ban-list membership (`"auto_lfg",` / `'auto_lfg']`); `does_not_claim`/`DOES_NOT_CLAIM`/`does not claim`/`non_claims` lines with `auto_lfg` (no True); ban-before prose (`does not`…`auto_lfg`); `never sets`…`auto_lfg` inventory (prefer same-line / rejoin wraps); bare crown inventory docs (`field_proven`…`auto_lfg`); Non-claims multi-token inventory (`invent_human_verdict · auto_lfg · public_agi` / mid-bullet `· auto_lfg ·`). True stamps never allowlisted. | `auto_lfg=True`, `"auto_lfg": True`, `auto_run_lfg`, `run_lfg_automatically` |
| `H07` | Quoted forbidden/deny-doc membership `"auto_promote=True"` / `'auto_promote=True'` (e.g. inside `forbidden: [` lists); `no`/`not`/`never auto_promote` ban prose (optional markdown bold around ban word); `does_not_claim`/`non_claims`/`does not claim` near `auto_promote`; ban-before `does not`…`auto_promote`. True assign and live `auto_promote(` call never allowlisted (`H07_TRUE_STAMP_RE` hard first). | `auto_promote = True`, `auto_promote=True` (unquoted assign), `auto_promote(` |
| `H08` | `refusing write under process_packs` / ValueError refuse guards | actual rewrite/write of process_packs without refuse |
| `H10` | `outer_rsi*=False` / `outer_rsi_unlocked: False`; `not_outer_rsi`; ban words *before* unlock (`do not`/`does not`/`never`/`must not` unlock outer RSI) with optional markdown bold between ban words (``Does **not** … unlock outer RSI``); `Block RSI`. No bare `no`; no trailing deferred/never arm. True stamps never allowlisted. | `outer_rsi=True`, `outer_rsi_unlock=True`, `unlock_outer_rsi=True`, bare positive unlock prose, True+trailing ban comment |

See: `notes/ops/qc_honesty_high_triage_2026-08-01.md`

## Regression fixtures (phase 4 FP lock)

Lock H05/H07/H10 allowlist arms with skill fixtures under
`.grok/skills/qc-honesty/fixtures/` (`MANIFEST.json` lists `covers_fp_classes`
and `expected_rules`). Scanner source is unchanged in phase 4 — fixtures +
docs + tests only.

| FP class | Good fixture sample (expect **0** H05/H07/H10) | Bad True stamp (expect flag) |
|----------|--------------------------------------------------|------------------------------|
| H05 string false | `"auto_lfg": "false"` / `'auto_lfg': 'false'` in `good_honesty_comments.py` | `auto_lfg = True`, `"auto_lfg": True` |
| H05 non-claims inventory | `invent_human_verdict · auto_lfg · public_agi` mid-bullet | `auto_run_lfg` / `run_lfg_automatically` |
| H05 bold **no** | ``- **no** auto_lfg`` markdown ban | True + trailing ban comment still flags |
| H07 forbidden string | `"auto_promote=True"` inside `forbidden: [` | unquoted `auto_promote = True`, `auto_promote(` |
| H10 Does **not** unlock | ``Does **not** unlock outer RSI`` ban-before bold | `outer_rsi=True`, `outer_rsi_unlock=True`, `unlock_outer_rsi=True` |

**Commands:**

```text
python .grok/skills/qc-honesty/scripts/run_honesty.py --repo-root . --fixture-mode
python -m pytest test_qc_honesty.py -q
```

**Hard rule:** `H05_TRUE_STAMP_RE` / `H07_TRUE_STAMP_RE` / `H10_TRUE_STAMP_RE`
checked first — never skip True execute stamps. Note: quoted `"auto_lfg=True"`
is **not** an H05 allowlist (only bare membership `"auto_lfg",` / False stamps);
H07 alone allows quoted `"auto_promote=True"` forbid-list membership.

## Severity defaults

- **high**: crown stamps, auto promote/LFG, pack/constitution write  
- **medium**: status collapses, outer RSI, complete=field language as code  
- **low**: noisy soft-fail heuristics (optional)
