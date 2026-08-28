#!/usr/bin/env python3
"""qc-errors leaf: bare/swallowed except → factory_qc_findings.v0.

Severity policy (residual plan 03):
  - Hot-path modules (agent/supervisor/metrics/registry/health/gates): E02 medium
  - All other pipeline modules: E02/E01 downgraded to **low** (volume backlog)
  - soft_log_exc / soft_log bodies are allowlisted (not findings)

Does not claim full reliability engineering.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BARE_EXCEPT = re.compile(r"^\s*except\s*:\s*(?:pass\s*)?(?:#.*)?$")
EXCEPT_PASS = re.compile(
    r"^\s*except\s+(\w+(?:\s*,\s*\w+)*)\s*(?:as\s+\w+)?\s*:\s*pass\s*(?:#.*)?$"
)
EXCEPT_ELLIPSIS = re.compile(r"^\s*except\s+.*:\s*\.\.\.\s*(?:#.*)?$")
EXCEPT_HDR = re.compile(r"^\s*except\s+.+:\s*$")
PASS_ONLY = re.compile(r"^\s*pass\s*(?:#.*)?$")
ALLOW = re.compile(
    r"(?i)(_soft_log_exc|soft_log_exc|soft_log|intentional|qc-errors-allow|ruff:\s*noqa)"
)
SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv", ".pytest_cache"}

# Modules where silent swallow is still Medium (factory hot paths).
# Non-matching paths get E01/E02 severity=low (denoise bulk backlog).
HOT_PATH_FRAGMENTS: tuple[str, ...] = (
    "pipeline/agent_metrics.py",
    "pipeline/agent_supervisor.py",
    "pipeline/autonomy_metrics.py",
    "pipeline/block_registry.py",
    "pipeline/health_checks.py",
    "pipeline/agent_process.py",
    "pipeline/_agent_process/",
    "pipeline/message_bus.py",
    "pipeline/complete_gate.py",
    "pipeline/field_prove_gate.py",
    "pipeline/goal_prove.py",
    "pipeline/_goal_prove/",
    "pipeline/runner.py",
    "pipeline/soft_log.py",
)


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _is_hot_path(rel: str) -> bool:
    rel_n = rel.replace("\\", "/")
    return any(frag in rel_n for frag in HOT_PATH_FRAGMENTS)


def _severity_for(rel: str, default: str = "medium") -> str:
    if default in ("info", "low"):
        return default
    return "medium" if _is_hot_path(rel) else "low"


def _body_allowlisted(lines: list[str], except_idx: int) -> bool:
    """True if except header or next few body lines mention soft_log / allow markers."""
    for j in range(except_idx, min(len(lines), except_idx + 4)):
        if ALLOW.search(lines[j]):
            return True
    # peek previous non-empty
    for j in range(except_idx - 1, max(-1, except_idx - 4), -1):
        if lines[j].strip():
            return bool(ALLOW.search(lines[j]))
    return False


def scan_file(path: Path, rel: str) -> list[dict]:
    out: list[dict] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return out
    for i, line in enumerate(lines):
        if ALLOW.search(line):
            continue
        if BARE_EXCEPT.match(line):
            if _body_allowlisted(lines, i):
                continue
            out.append(
                {
                    "id": f"errors-bare-{rel.replace('/', '-')}-{i+1}",
                    "severity": _severity_for(rel, "medium"),
                    "control": "qc-errors",
                    "title": "Bare except:",
                    "evidence": f"{rel}:{i+1}: {line.strip()}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "S",
                    "rule": "E01_bare_except",
                    "line": i + 1,
                    "recommendation": "Catch specific exceptions or soft_log_exc",
                    "tags": ["error_surface"]
                    + (["hot_path"] if _is_hot_path(rel) else ["bulk"]),
                    "tool": "qc-errors",
                }
            )
            continue

        # single-line except X: pass
        if EXCEPT_PASS.match(line):
            if _body_allowlisted(lines, i):
                continue
            out.append(
                {
                    "id": f"errors-pass-{rel.replace('/', '-')}-{i+1}",
                    "severity": _severity_for(rel, "medium"),
                    "control": "qc-errors",
                    "title": "Swallowed exception (except …: pass)",
                    "evidence": f"{rel}:{i+1}: {line.strip()}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "S",
                    "rule": "E02_except_pass",
                    "line": i + 1,
                    "recommendation": "Log via soft_log_exc or re-raise",
                    "tags": ["error_surface"]
                    + (["hot_path"] if _is_hot_path(rel) else ["bulk"]),
                    "tool": "qc-errors",
                }
            )
            continue

        # two-line: except …: / pass
        if (
            EXCEPT_HDR.match(line)
            and i + 1 < len(lines)
            and PASS_ONLY.match(lines[i + 1])
        ):
            if _body_allowlisted(lines, i):
                continue
            out.append(
                {
                    "id": f"errors-pass-{rel.replace('/', '-')}-{i+1}",
                    "severity": _severity_for(rel, "medium"),
                    "control": "qc-errors",
                    "title": "Swallowed exception (except …: pass)",
                    "evidence": f"{rel}:{i+1}: {line.strip()}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "S",
                    "rule": "E02_except_pass",
                    "line": i + 1,
                    "recommendation": "Log via soft_log_exc or re-raise",
                    "tags": ["error_surface"]
                    + (["hot_path"] if _is_hot_path(rel) else ["bulk"]),
                    "tool": "qc-errors",
                }
            )
            continue

        if EXCEPT_ELLIPSIS.match(line):
            out.append(
                {
                    "id": f"errors-ellipsis-{rel.replace('/', '-')}-{i+1}",
                    "severity": "low",
                    "control": "qc-errors",
                    "title": "except body is ellipsis",
                    "evidence": f"{rel}:{i+1}: {line.strip()}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "S",
                    "rule": "E03_except_ellipsis",
                    "line": i + 1,
                    "recommendation": "Implement handling or soft_log",
                    "tags": ["error_surface"],
                    "tool": "qc-errors",
                }
            )
    return out


def iter_py(root: Path, paths: list[str]) -> list[Path]:
    files: list[Path] = []
    bases = [root / p for p in (paths or ["pipeline"])]
    for base in bases:
        if base.is_file() and base.suffix == ".py":
            files.append(base)
            continue
        if not base.is_dir():
            continue
        for p in base.rglob("*.py"):
            if any(x in SKIP_DIRS for x in p.parts):
                continue
            files.append(p)
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--path", action="append", dest="paths", default=[])
    ap.add_argument("--max-findings", type=int, default=300)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "errors" / "findings.json")
    paths = list(args.paths or ["pipeline"])
    files = iter_py(root, paths)
    findings: list[dict] = []
    for fp in files:
        try:
            rel = str(fp.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel = str(fp)
        findings.extend(scan_file(fp, rel))
    # Prefer hot-path / higher severity when capping so bulk low does not hide medium
    _sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    findings.sort(
        key=lambda f: (
            _sev_rank.get(str(f.get("severity", "info")), 9),
            str((f.get("paths") or [""])[0]),
            int(f.get("line") or 0),
        )
    )
    truncated = False
    total_before_cap = len(findings)
    if len(findings) > args.max_findings:
        findings = findings[: args.max_findings]
        truncated = True
        findings.append(
            {
                "id": "errors-truncated-001",
                "severity": "info",
                "control": "qc-errors",
                "title": f"Truncated to {args.max_findings} findings (severity-priority)",
                "evidence": f"total_before_cap={total_before_cap}; kept medium/high first",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "Narrow --path or raise --max-findings",
                "tool": "qc-errors",
            }
        )
    if not findings:
        findings.append(
            {
                "id": "errors-pass-001",
                "severity": "info",
                "control": "qc-errors",
                "title": "No bare/swallowed except hits (pass_summary)",
                "evidence": f"scanned {len(files)} files",
                "paths": paths,
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "None",
                "tool": "qc-errors",
            }
        )
    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = summary.get(
            str(f.get("severity", "info")), 0
        ) + 1
    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-errors",
        "profile": "leaf",
        "scope": {
            "paths": paths,
            "note": str(root),
            "files_scanned": len(files),
            "hot_path_fragments": list(HOT_PATH_FRAGMENTS),
            "severity_policy": "hot_path=medium else low for E01/E02",
            "truncated": truncated,
        },
        "commands_run": [{"cmd": f"qc-errors scan files={len(files)}", "exit_code": 0}],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "error scan ≠ full reliability engineering",
            "low bulk residual ≠ fixed",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
