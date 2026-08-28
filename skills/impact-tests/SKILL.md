---
name: impact-tests
description: >
  Map changed files to pytest targets and soft-expand job_packet verify_commands.
  Use when implement/review needs impact-aware retest, "which tests for this diff",
  empty verify list, or /impact-tests. Python-first heuristics; no field_proven claims.
---

# Impact-aware tests

## When to use
- After editing Python sources: choose tests for verify
- Job packet `verify_commands` empty or incomplete
- Dual-engine implement / review retest selection

## One hop

```powershell
python -c "from pipeline.impact_tests import suggest_tests_for_paths, expand_packet_verify_from_paths; print(suggest_tests_for_paths('.', ['pipeline/job_packet.py']))"
```

Expand a packet (soft append):

```python
from pipeline.impact_tests import expand_packet_verify_from_paths
from pipeline.job_packet import build_job_packet

pkt = build_job_packet({"goal": "g", "done_when": ["ok"], "verify_commands": []}, mode="soft")
pkt = expand_packet_verify_from_paths(pkt, repo_root=".", changed_paths=["pipeline/foo.py"])
# pkt.verify_commands now has pytest targets (or package smoke fallback)
```

Git diff (best-effort):

```python
expand_packet_verify_from_paths(pkt, repo_root=".", use_git_diff=True)
```

## Rules
1. Prefer existing mapped test files over full-suite.
2. Empty map → package/repo smoke (`notes/ops/impact_tests.md`).
3. Soft-append only; do not wipe existing verify cmds.
4. **Never** claim `field_proven` from verify green. Dual-gate unchanged.

## Related
- Contract: `notes/ops/impact_tests.md`
- Job packet: `notes/ops/job_packet.md` · `pipeline/job_packet.py`
- Module: `pipeline/impact_tests.py`

## Done when
- Non-empty test list for known Python diffs with fixtures on disk
- Empty map uses documented smoke fallback
- Packet expand soft-appends; no field_proven keys
