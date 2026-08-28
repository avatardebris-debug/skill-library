#!/usr/bin/env python3
"""qc-security leaf: secrets / shell_safety / write-root / allow-live → findings.v0."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv", ".pytest_cache", "notes"}

# Avoid matching our own pattern definitions / docs
SECRET_RES: list[tuple[str, re.Pattern[str], str]] = [
    (
        "S01_pem_private",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "PEM private key material",
    ),
    (
        "S02_aws_key",
        re.compile(r"AKIA[0-9A-Z]{16}"),
        "AWS access key id-like token",
    ),
    (
        "S03_generic_api_assign",
        re.compile(
            r"""(?i)(?:api[_-]?key|secret[_-]?key|auth[_-]?token)\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]"""
        ),
        "Hardcoded api/secret/token assignment",
    ),
]

WRITE_CONSTITUTION = re.compile(
    r"""open\([^\)]*constitution\.yaml[^\)]*['\"]w|Path\([^\)]*constitution\.yaml[^\)]*\)[^\n]{0,40}\.write""",
    re.I,
)
WRITE_PACKS = re.compile(
    r"""process_packs[^\n]{0,60}(write|open\([^\)]*['\"]w)|['\"]w['\"].{0,40}process_packs""",
    re.I,
)
ALLOW_LIVE = re.compile(r"allow_live\s*=\s*True|--allow-live", re.I)
# Real enable only: keyword/assignment allow_live=True (not docs about refuse)
ALLOW_LIVE_ENABLE = re.compile(r"\ballow_live\s*=\s*True\b")
SHELL_TRUE = re.compile(r"shell\s*=\s*True")
SHELL_SAFETY_IMPORT = re.compile(r"from pipeline\.shell_safety import|import pipeline\.shell_safety")

ALLOW_LINE = re.compile(
    r"(?i)(example|fixture|non-claim|≠|never|test_|fake_|placeholder|your_api_key|xxx+)"
)

# S12 denoise: docs / CLI surface / refuse messages (residual plan 04)
S12_DOC_REFUSE = re.compile(
    r"(?i)("
    r"not\s+implemented|refuses?|network_stub|default\s+off|"
    r"set\s+but\s+live\s+path\s+not|"
    r"requires?\s+(?:both\s+)?--allow-live|"
    r"requires?\s+--allow-live|"
    r"live\s+default\s+off|"
    r"omit\s+--allow-live|"
    r"fixture\s+adapter\s+only|"
    r"v0\s+returns\s+honest"
    r")"
)

RUNNER_GLOBS = [
    "pipeline/engines/**/*.py",
    "pipeline/agent_process.py",
    "pipeline/_agent_process/**/*.py",
]


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def iter_py(root: Path) -> list[Path]:
    files: list[Path] = []
    base = root / "pipeline"
    if not base.is_dir():
        return files
    for p in base.rglob("*.py"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        if p.name.endswith(".bak_pre_split"):
            continue
        files.append(p)
    return files


def _is_comment_or_doc_line(line: str) -> bool:
    stripped = line.lstrip()
    return stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''")


def _s20_should_skip(line: str, rel: str, file_text: str) -> bool:
    """S20 denoise: definition module, comments, policy-gated shell_run_kwargs callers."""
    rel_norm = rel.replace("\\", "/")
    # Definition module — documents shell=True policy; not an unguarded runner
    if rel_norm.endswith("pipeline/shell_safety.py") or rel_norm == "pipeline/shell_safety.py":
        return True
    if "shell_safety" in line:
        return True
    if _is_comment_or_doc_line(line):
        return True
    # Docstring body lines often mention shell=True policy
    if "shell=True only" in line or "shell=True when" in line:
        return True
    # Policy-gated: file already routes through shell_run_kwargs
    if "shell_run_kwargs" in file_text and SHELL_TRUE.search(line):
        return True
    return False


def _s12_should_flag(line: str) -> bool:
    """S12 allow_live: flag real enable only; skip docs/CLI/default-off/refuse.

    Flag:
      - bare ``allow_live=True`` assignment or call kwarg that enables live
    Skip:
      - comments / docstring noise
      - ``allow_live=False`` / default off
      - argparse ``--allow-live`` registration and help strings
      - refuse / not-implemented / network_stub documentation
    """
    if not ALLOW_LIVE.search(line):
        return False
    stripped = line.lstrip()
    if stripped.startswith("#"):
        return False
    # default off / False
    if re.search(r"allow_live\s*=\s*False", line, re.I):
        return False
    if re.search(r"(?i)default\s*[:=].*false|default\s*=\s*False", line):
        return False
    if "default" in line.lower() and "off" in line.lower():
        return False
    # argparse flag registration (not enabling live)
    if re.search(r"""add_argument\s*\(\s*['\"]--allow-live['\"]""", line):
        return False
    if re.search(r"""['\"]--allow-live['\"]""", line) and (
        "add_argument" in line or "help=" in line or "help =" in line
    ):
        return False
    # standalone argparse dest line: "--allow-live",
    if re.match(r"""^\s*['\"]--allow-live['\"]\s*,?\s*$""", line):
        return False
    # help / warning strings about live without enabling
    if S12_DOC_REFUSE.search(line):
        return False
    if "help=" in line and "--allow-live" in line:
        return False
    # Real enable: allow_live=True (not inside refuse/doc string)
    if ALLOW_LIVE_ENABLE.search(line):
        # string about refuse still has allow_live=True in text
        if S12_DOC_REFUSE.search(line):
            return False
        if re.search(r'(?i)(but\s+|refuses|not\s+implement|stub|using fixture)', line):
            return False
        # quoted docstring/example only
        if stripped.startswith(('"', "'", "`")) and "but" in line.lower():
            return False
        return True
    # bare --allow-live without enable assignment: CLI surface only → skip
    return False


def scan_secrets_and_writes(path: Path, rel: str) -> list[dict]:
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for i, line in enumerate(text.splitlines(), start=1):
        if ALLOW_LINE.search(line):
            continue
        for rule, cre, title in SECRET_RES:
            if cre.search(line):
                findings.append(
                    {
                        "id": f"sec-{rule}-{rel.replace('/', '-')}-{i}",
                        "severity": "critical" if "PRIVATE" in title or "AWS" in title else "high",
                        "control": "qc-security",
                        "title": title,
                        "evidence": f"{rel}:{i}: {line.strip()[:160]}",
                        "paths": [rel.replace("\\", "/")],
                        "effort": "S",
                        "rule": rule,
                        "line": i,
                        "recommendation": "Remove secret; rotate if real; use env",
                        "tags": ["secret"],
                        "tool": "qc-security",
                    }
                )
        if WRITE_CONSTITUTION.search(line):
            findings.append(
                {
                    "id": f"sec-const-write-{rel.replace('/', '-')}-{i}",
                    "severity": "high",
                    "control": "qc-security",
                    "title": "constitution.yaml write smell",
                    "evidence": f"{rel}:{i}: {line.strip()[:160]}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "M",
                    "rule": "S10_constitution_write",
                    "line": i,
                    "recommendation": "Constitution is read-only",
                    "tags": ["write_root"],
                    "tool": "qc-security",
                }
            )
        if WRITE_PACKS.search(line):
            findings.append(
                {
                    "id": f"sec-pack-write-{rel.replace('/', '-')}-{i}",
                    "severity": "high",
                    "control": "qc-security",
                    "title": "process_packs write smell",
                    "evidence": f"{rel}:{i}: {line.strip()[:160]}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "M",
                    "rule": "S11_pack_write",
                    "line": i,
                    "recommendation": "Refuse pack rewrite",
                    "tags": ["write_root"],
                    "tool": "qc-security",
                }
            )
        if _s12_should_flag(line):
            findings.append(
                {
                    "id": f"sec-allow-live-{rel.replace('/', '-')}-{i}",
                    "severity": "medium",
                    "control": "qc-security",
                    "title": "allow_live=True enable path",
                    "evidence": f"{rel}:{i}: {line.strip()[:160]}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "S",
                    "rule": "S12_allow_live",
                    "line": i,
                    "recommendation": "Ensure default off; CI never sets allow_live=True without guard",
                    "tags": ["network"],
                    "tool": "qc-security",
                }
            )
        if SHELL_TRUE.search(line) and not _s20_should_skip(line, rel, text):
            findings.append(
                {
                    "id": f"sec-shell-true-{rel.replace('/', '-')}-{i}",
                    "severity": "medium",
                    "control": "qc-security",
                    "title": "subprocess shell=True without shell_safety nearby",
                    "evidence": f"{rel}:{i}: {line.strip()[:160]}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "M",
                    "rule": "S20_shell_true",
                    "line": i,
                    "recommendation": "Use pipeline.shell_safety.shell_run_kwargs",
                    "tags": ["shell"],
                    "tool": "qc-security",
                }
            )
    return findings


def check_shell_safety_usage(root: Path) -> list[dict]:
    findings: list[dict] = []
    # engines grok_build should import shell_safety
    targets = [
        root / "pipeline" / "engines" / "grok_build.py",
        root / "pipeline" / "engines" / "_grok_build",
    ]
    files: list[Path] = []
    for t in targets:
        if t.is_file():
            files.append(t)
        elif t.is_dir():
            files.extend(t.rglob("*.py"))
    if not files:
        findings.append(
            {
                "id": "sec-shell-targets-missing-001",
                "severity": "info",
                "control": "qc-security",
                "title": "No grok_build engine paths found for shell_safety check",
                "evidence": "pipeline/engines/grok_build*",
                "paths": [],
                "effort": "S",
                "tags": ["control_gap"],
                "tool": "qc-security",
                "recommendation": "Point scanner at actual runner modules",
            }
        )
        return findings

    any_import = False
    for fp in files:
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if SHELL_SAFETY_IMPORT.search(text) or "shell_run_kwargs" in text:
            any_import = True
            try:
                rel = str(fp.relative_to(root)).replace("\\", "/")
            except ValueError:
                rel = str(fp)
            findings.append(
                {
                    "id": f"sec-shell-ok-{fp.stem}",
                    "severity": "info",
                    "control": "qc-security",
                    "title": f"shell_safety / shell_run_kwargs used in {rel}",
                    "evidence": "import or call present",
                    "paths": [rel],
                    "effort": "S",
                    "tags": ["pass_summary", "shell"],
                    "tool": "qc-security",
                    "recommendation": "None",
                }
            )
    if not any_import:
        findings.append(
            {
                "id": "sec-shell-missing-001",
                "severity": "medium",
                "control": "qc-security",
                "title": "grok_build path lacks shell_safety / shell_run_kwargs",
                "evidence": "scanned engines/_grok_build and façade",
                "paths": ["pipeline/engines/"],
                "effort": "M",
                "tags": ["shell"],
                "tool": "qc-security",
                "recommendation": "Wire shell_run_kwargs for CLI runs",
            }
        )
    # module exists
    ss = root / "pipeline" / "shell_safety.py"
    if ss.is_file():
        findings.append(
            {
                "id": "sec-shell-module-001",
                "severity": "info",
                "control": "qc-security",
                "title": "pipeline.shell_safety module present",
                "evidence": "pipeline/shell_safety.py",
                "paths": ["pipeline/shell_safety.py"],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "qc-security",
                "recommendation": "None",
            }
        )
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--max-findings", type=int, default=100)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "security" / "findings.json")

    findings: list[dict] = []
    files = iter_py(root)
    for fp in files:
        try:
            rel = str(fp.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel = str(fp)
        findings.extend(scan_secrets_and_writes(fp, rel))
    findings.extend(check_shell_safety_usage(root))

    if len(findings) > args.max_findings:
        findings = findings[: args.max_findings]
        findings.append(
            {
                "id": "sec-truncated-001",
                "severity": "info",
                "control": "qc-security",
                "title": f"Truncated to {args.max_findings}",
                "evidence": "max-findings",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "qc-security",
                "recommendation": "Narrow scope",
            }
        )

    if not findings:
        findings.append(
            {
                "id": "sec-pass-001",
                "severity": "info",
                "control": "qc-security",
                "title": "No security-surface hits (pass_summary)",
                "evidence": f"scanned {len(files)} files",
                "paths": ["pipeline/"],
                "effort": "S",
                "tags": ["pass_summary"],
                "tool": "qc-security",
                "recommendation": "None",
            }
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = summary.get(str(f.get("severity", "info")), 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-security",
        "profile": "leaf",
        "scope": {"paths": ["pipeline/"], "note": str(root), "files_scanned": len(files)},
        "commands_run": [{"cmd": f"qc-security scan files={len(files)}", "exit_code": 0}],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "not full SAST/SCA",
            "not pen test",
            "not product auth productization",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
