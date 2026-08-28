#!/usr/bin/env python3
"""qc-static leaf: detect/run ruff (optional); emit factory_qc_findings.v0."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _has_ruff_config(root: Path) -> bool:
    pyproject = root / "pyproject.toml"
    if pyproject.is_file() and "ruff" in pyproject.read_text(encoding="utf-8", errors="replace").lower():
        return True
    return (root / "ruff.toml").is_file() or (root / ".ruff.toml").is_file()


def _run_ruff(root: Path, paths: list[str]) -> tuple[int, str, list[dict]]:
    targets = paths or ["pipeline", "scripts"]
    cmd = ["ruff", "check", *targets, "--output-format=concise"]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except OSError as exc:
        return 127, str(exc), []
    out = (proc.stdout or "") + (proc.stderr or "")
    findings: list[dict] = []
    # concise: path:line:col: CODE message
    line_re = re.compile(r"^(.+?):(\d+):\d+:\s+(\S+)\s+(.*)$")
    for i, line in enumerate(out.splitlines()):
        m = line_re.match(line.strip())
        if not m:
            continue
        rel, lineno, code, msg = m.group(1), int(m.group(2)), m.group(3), m.group(4)
        sev = "medium" if code.startswith(("E", "F", "S")) else "low"
        findings.append(
            {
                "id": f"static-ruff-{i+1:03d}",
                "severity": sev,
                "control": "qc-static",
                "title": f"ruff {code}: {msg[:120]}",
                "evidence": line.strip()[:500],
                "paths": [rel.replace("\\", "/")],
                "effort": "S",
                "tool": "ruff",
                "rule": code,
                "line": lineno,
                "recommendation": "Fix lint or document intentional noqa",
                "tags": [],
            }
        )
    return proc.returncode, " ".join(cmd), findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--path", action="append", dest="paths", default=[])
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "static" / "findings.json")

    commands_run: list[dict] = []
    findings: list[dict] = []
    ruff_bin = shutil.which("ruff")
    configured = _has_ruff_config(root)

    if not ruff_bin and not configured:
        findings.append(
            {
                "id": "static-tool-missing-001",
                "severity": "info",
                "control": "qc-static",
                "title": "No static tool configured (ruff not on PATH / no ruff config)",
                "evidence": "shutil.which('ruff') is None; no [tool.ruff] detected",
                "paths": [],
                "effort": "S",
                "tool": "ruff",
                "tags": ["tool_missing"],
                "recommendation": "Install ruff or accept tool_missing until configured",
            }
        )
        commands_run.append({"cmd": "which ruff", "exit_code": 1})
    else:
        if not ruff_bin:
            findings.append(
                {
                    "id": "static-tool-missing-002",
                    "severity": "info",
                    "control": "qc-static",
                    "title": "ruff config present but ruff binary not on PATH",
                    "evidence": "config detected; which ruff failed",
                    "paths": ["pyproject.toml"],
                    "effort": "S",
                    "tool": "ruff",
                    "tags": ["tool_missing"],
                    "recommendation": "pip install ruff or add to PATH",
                }
            )
            commands_run.append({"cmd": "which ruff", "exit_code": 1})
        else:
            code, cmd, ruff_findings = _run_ruff(root, list(args.paths or []))
            commands_run.append({"cmd": cmd, "exit_code": code})
            findings.extend(ruff_findings)
            if not ruff_findings and code == 0:
                findings.append(
                    {
                        "id": "static-pass-001",
                        "severity": "info",
                        "control": "qc-static",
                        "title": "ruff check clean (pass_summary)",
                        "evidence": f"{cmd} exit 0, no concise findings",
                        "paths": list(args.paths or ["pipeline", "scripts"]),
                        "effort": "S",
                        "tool": "ruff",
                        "tags": ["pass_summary"],
                        "recommendation": "None",
                    }
                )
            elif not ruff_findings and code != 0:
                findings.append(
                    {
                        "id": "static-ruff-raw-001",
                        "severity": "low",
                        "control": "qc-static",
                        "title": f"ruff exited {code} without parseable lines",
                        "evidence": f"cmd={cmd}",
                        "paths": [],
                        "effort": "S",
                        "tool": "ruff",
                        "tags": [],
                        "recommendation": "Re-run ruff with human-readable output",
                    }
                )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = summary.get(str(f.get("severity", "info")), 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-static",
        "profile": "leaf",
        "scope": {"paths": list(args.paths or ["pipeline", "scripts"]), "note": str(root)},
        "commands_run": commands_run,
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "factory health ≠ goal_proven_human",
            "static clean ≠ product aim quality",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
