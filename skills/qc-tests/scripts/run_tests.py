#!/usr/bin/env python3
"""qc-tests leaf: contract pytest + optional smoke + weak-test heuristic → findings.v0."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOT_MODULES = [
    "goal_prove",
    "goal_amend_ladder",
    "budget_ladder",
    "agent_process",
    "external_ingest",
    "deconstructor",
    "mcp_factory",
    "block_registry",
    "troubleshoot_gate",
    "factory_candidates",
    "meta_reasoner",
    "github_crawl",
    "goal_graph",
]


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _run(cmd: list[str], cwd: Path, timeout: int = 300) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd, cwd=str(cwd), capture_output=True, text=True, timeout=timeout, check=False
        )
    except OSError as exc:
        return 127, str(exc)
    blob = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode, blob[-3000:]


def _line_count(p: Path) -> int:
    try:
        return sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
    except OSError:
        return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--skip-smoke", action="store_true")
    ap.add_argument("--loc-threshold", type=int, default=800)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "tests" / "findings.json")

    findings: list[dict] = []
    commands_run: list[dict] = []

    # 1) public API contracts
    py_cmd = [sys.executable, "-m", "pytest", "test_pipeline_public_api_contracts.py", "-q", "--tb=no"]
    code, blob = _run(py_cmd, root, timeout=120)
    commands_run.append({"cmd": " ".join(py_cmd), "exit_code": code})
    if code == 0:
        findings.append(
            {
                "id": "tests-contracts-pass-001",
                "severity": "info",
                "control": "qc-tests",
                "title": "Public API contract tests passed",
                "evidence": (blob or "exit 0")[:400],
                "paths": ["test_pipeline_public_api_contracts.py"],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "pytest",
                "recommendation": "None",
            }
        )
    else:
        findings.append(
            {
                "id": "tests-contracts-fail-001",
                "severity": "high",
                "control": "qc-tests",
                "title": "Public API contract tests failed",
                "evidence": (blob or f"exit {code}")[:800],
                "paths": ["test_pipeline_public_api_contracts.py"],
                "effort": "M",
                "tags": [],
                "tool": "pytest",
                "recommendation": "Restore façade freezes",
            }
        )

    # 2) critical-path smoke (optional)
    smoke = root / "scripts" / "factory_critical_path_smoke.py"
    if args.skip_smoke:
        findings.append(
            {
                "id": "tests-smoke-skipped-001",
                "severity": "info",
                "control": "qc-tests",
                "title": "Critical-path smoke skipped (--skip-smoke)",
                "evidence": "flag set",
                "paths": ["scripts/factory_critical_path_smoke.py"],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "qc-tests",
                "recommendation": "Run without --skip-smoke on deep-audit",
            }
        )
    elif smoke.is_file():
        scmd = [sys.executable, str(smoke), "--skip-crawl"]
        scode, sblob = _run(scmd, root, timeout=600)
        commands_run.append({"cmd": " ".join(scmd), "exit_code": scode})
        if scode == 0:
            findings.append(
                {
                    "id": "tests-smoke-pass-001",
                    "severity": "info",
                    "control": "qc-tests",
                    "title": "Critical-path smoke --skip-crawl passed",
                    "evidence": (sblob or "exit 0")[-400:],
                    "paths": ["scripts/factory_critical_path_smoke.py"],
                    "effort": "S",
                    "tags": ["pass_summary"],
                    "tool": "factory_critical_path_smoke",
                    "recommendation": "None",
                }
            )
        else:
            findings.append(
                {
                    "id": "tests-smoke-fail-001",
                    "severity": "high",
                    "control": "qc-tests",
                    "title": "Critical-path smoke failed",
                    "evidence": (sblob or f"exit {scode}")[-800:],
                    "paths": ["scripts/factory_critical_path_smoke.py"],
                    "effort": "L",
                    "tags": [],
                    "tool": "factory_critical_path_smoke",
                    "recommendation": "Fix factory spine before merge",
                }
            )
    else:
        findings.append(
            {
                "id": "tests-smoke-missing-001",
                "severity": "info",
                "control": "qc-tests",
                "title": "Critical-path smoke script missing",
                "evidence": "scripts/factory_critical_path_smoke.py",
                "paths": [],
                "effort": "S",
                "tags": ["tool_missing"],
                "tool": "qc-tests",
                "recommendation": "Add smoke script or accept gap",
            }
        )

    # 3) weak-test heuristic: large hot modules without matching test file name
    pipeline = root / "pipeline"
    for name in HOT_MODULES:
        mod = pipeline / f"{name}.py"
        if not mod.is_file():
            # package façade may still exist as meta_reasoner.py etc.
            continue
        loc = _line_count(mod)
        if loc < args.loc_threshold:
            continue
        # any test_* containing name fragment
        hits = list(root.glob(f"test_*{name}*.py")) + list(root.glob(f"**/test_*{name}*.py"))
        hits = [h for h in hits if h.is_file()]
        if hits:
            findings.append(
                {
                    "id": f"tests-coverage-ok-{name}",
                    "severity": "info",
                    "control": "qc-tests",
                    "title": f"Hot module {name} has test glob hits",
                    "evidence": f"loc={loc} tests={[str(h.name) for h in hits[:5]]}",
                    "paths": [f"pipeline/{name}.py"],
                    "effort": "S",
                    "tags": ["pass_summary", "weak_test"],
                    "tool": "qc-tests",
                    "recommendation": "None",
                }
            )
        else:
            findings.append(
                {
                    "id": f"tests-weak-{name}",
                    "severity": "medium",
                    "control": "qc-tests",
                    "title": f"Hot module {name} (~{loc} LOC) lacks test_*{name}* file",
                    "evidence": f"loc>={args.loc_threshold}; no test glob match",
                    "paths": [f"pipeline/{name}.py"],
                    "effort": "M",
                    "rule": "T01_weak_test",
                    "tags": ["weak_test"],
                    "tool": "qc-tests",
                    "recommendation": "Add focused tests or document intentional gap",
                }
            )

    if not findings:
        findings.append(
            {
                "id": "tests-empty-001",
                "severity": "info",
                "control": "qc-tests",
                "title": "No test findings",
                "evidence": "unexpected",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "qc-tests",
                "recommendation": "None",
            }
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = summary.get(str(f.get("severity", "info")), 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-tests",
        "profile": "leaf",
        "scope": {"paths": ["pipeline/", "test_*.py"], "note": str(root)},
        "commands_run": commands_run,
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "not mutation score",
            "not product field tests",
            "weak-test heuristic ≠ coverage %",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
