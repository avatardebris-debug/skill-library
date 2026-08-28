#!/usr/bin/env python3
"""qc-contracts leaf: freeze tests + path-ref + freeze coverage gaps → findings.v0."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOT_FACADES = [
    ("pipeline.github_crawl", "FROZEN_GITHUB_CRAWL"),
    ("pipeline.goal_graph", "FROZEN_GOAL_GRAPH"),
    ("pipeline.research_candidates", "FROZEN_RESEARCH_CANDIDATES"),
    ("pipeline.research_fuel_adapters", "FROZEN_RESEARCH_FUEL_ADAPTERS"),
    ("pipeline.research_fuel_handoff", "FROZEN_RESEARCH_FUEL_HANDOFF"),
    ("pipeline.goal_prove", "FROZEN_GOAL_PROVE"),
    ("pipeline.goal_amend_ladder", "FROZEN_GOAL_AMEND_LADDER"),
    ("pipeline.budget_ladder", "FROZEN_BUDGET_LADDER"),
    ("pipeline.agent_process", "FROZEN_AGENT_PROCESS"),
    ("pipeline.external_ingest", "FROZEN_EXTERNAL_INGEST"),
    ("pipeline.engines.field_ship", "FROZEN_FIELD_SHIP"),
    ("pipeline.engines.grok_build", "FROZEN_GROK_BUILD"),
]


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _run(cmd: list[str], cwd: Path, timeout: int = 180) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except OSError as exc:
        return 127, str(exc)
    blob = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()
    return proc.returncode, blob[-4000:]


def _frozen_names(contract_path: Path) -> set[str]:
    if not contract_path.is_file():
        return set()
    text = contract_path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"^FROZEN_[A-Z0-9_]+\s*=", text, flags=re.M))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--skip-path-ref", action="store_true")
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "contracts" / "findings.json")

    findings: list[dict] = []
    commands_run: list[dict] = []

    # 1) public API freeze tests
    pytest_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "test_pipeline_public_api_contracts.py",
        "-q",
        "--tb=no",
    ]
    code, blob = _run(pytest_cmd, root)
    commands_run.append({"cmd": " ".join(pytest_cmd), "exit_code": code})
    if code == 0:
        findings.append(
            {
                "id": "contracts-pytest-pass-001",
                "severity": "info",
                "control": "qc-contracts",
                "title": "Public API contract tests passed",
                "evidence": (blob or "pytest exit 0")[:500],
                "paths": ["test_pipeline_public_api_contracts.py"],
                "effort": "S",
                "tool": "pytest",
                "tags": ["pass_summary"],
                "recommendation": "None",
            }
        )
    else:
        findings.append(
            {
                "id": "contracts-pytest-fail-001",
                "severity": "high",
                "control": "qc-contracts",
                "title": "Public API contract tests failed",
                "evidence": (blob or f"exit {code}")[:800],
                "paths": ["test_pipeline_public_api_contracts.py"],
                "effort": "M",
                "tool": "pytest",
                "tags": [],
                "recommendation": "Restore frozen public names on façades",
            }
        )

    # 2) path-ref script
    path_ref = root / "scripts" / "check_pipeline_path_refs.py"
    if args.skip_path_ref:
        findings.append(
            {
                "id": "contracts-path-ref-skipped-001",
                "severity": "info",
                "control": "qc-contracts",
                "title": "path-ref check skipped by flag",
                "evidence": "--skip-path-ref",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "Run without skip on deep-audit",
            }
        )
    elif path_ref.is_file():
        pref_cmd = [sys.executable, str(path_ref)]
        pcode, pblob = _run(pref_cmd, root, timeout=120)
        commands_run.append({"cmd": " ".join(pref_cmd), "exit_code": pcode})
        if pcode == 0:
            findings.append(
                {
                    "id": "contracts-path-ref-pass-001",
                    "severity": "info",
                    "control": "qc-contracts",
                    "title": "path-ref check exited 0",
                    "evidence": (pblob or "exit 0")[:500],
                    "paths": ["scripts/check_pipeline_path_refs.py"],
                    "effort": "S",
                    "tool": "check_pipeline_path_refs",
                    "tags": ["pass_summary"],
                    "recommendation": "None",
                }
            )
        else:
            findings.append(
                {
                    "id": "contracts-path-ref-fail-001",
                    "severity": "low",
                    "control": "qc-contracts",
                    "title": "path-ref check reported issues",
                    "evidence": (pblob or f"exit {pcode}")[:800],
                    "paths": ["scripts/check_pipeline_path_refs.py"],
                    "effort": "M",
                    "tool": "check_pipeline_path_refs",
                    "tags": [],
                    "recommendation": "Fix stale path refs or allowlist false positives",
                }
            )
    else:
        findings.append(
            {
                "id": "contracts-path-ref-missing-001",
                "severity": "info",
                "control": "qc-contracts",
                "title": "path-ref script missing",
                "evidence": "scripts/check_pipeline_path_refs.py not found",
                "paths": [],
                "effort": "S",
                "tags": ["tool_missing"],
                "recommendation": "Add script or accept gap",
            }
        )

    # 3) freeze coverage for hot façades
    contract_py = root / "test_pipeline_public_api_contracts.py"
    frozen_defined = _frozen_names(contract_py)
    # also names that appear as FROZEN_* = frozenset
    text = contract_py.read_text(encoding="utf-8", errors="replace") if contract_py.is_file() else ""
    for mod, frozen_const in HOT_FACADES:
        if frozen_const in text or f"{frozen_const} " in text:
            continue
        # partial: research freezes use FROZEN_RESEARCH_*
        short = frozen_const.replace("FROZEN_", "")
        if short in text or frozen_const in frozen_defined:
            continue
        if frozen_const in text:
            continue
        # explicit presence check
        present = frozen_const in text
        if present:
            continue
        findings.append(
            {
                "id": f"contracts-freeze-gap-{mod.replace('.', '-')}",
                "severity": "info",
                "control": "qc-contracts",
                "title": f"No freeze constant for hot façade {mod}",
                "evidence": f"{frozen_const} not found in test_pipeline_public_api_contracts.py",
                "paths": ["test_pipeline_public_api_contracts.py", mod.replace(".", "/") + ".py"],
                "effort": "S",
                "tags": ["freeze_gap"],
                "recommendation": f"Add {frozen_const} when intentionally freezing {mod}",
            }
        )

    # Ensure non-empty (always true given loops)
    if not findings:
        findings.append(
            {
                "id": "contracts-empty-001",
                "severity": "info",
                "control": "qc-contracts",
                "title": "No contract findings generated",
                "evidence": "unexpected empty",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "None",
            }
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        k = str(f.get("severity", "info"))
        summary[k] = summary.get(k, 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-contracts",
        "profile": "leaf",
        "scope": {"paths": ["test_pipeline_public_api_contracts.py", "pipeline/"], "note": str(root)},
        "commands_run": commands_run,
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "factory health ≠ goal_proven_human",
            "contracts green ≠ product aim quality",
            "does not invent new public APIs",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
