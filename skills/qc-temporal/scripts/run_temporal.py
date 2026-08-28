#!/usr/bin/env python3
"""qc-temporal leaf: git-history observation → findings.v0 + TABLE.md."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Subject starts with fix( / fix: or contains hotfix/bugfix as a word.
FIX_RE = re.compile(r"(?i)^fix\b|\bhotfix\b|\bbugfix\b")
SKIP_PREFIX = (".git/", "node_modules/", "_archive/", ".pipeline/")
DEFAULT_PATHS = ("pipeline/",)
TOP_N = 20


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def git(root: Path, args: list[str]) -> tuple[str, int]:
    p = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return (p.stdout if p.returncode == 0 else ""), int(p.returncode)


def interesting(path: str, prefixes: tuple[str, ...]) -> bool:
    if not path or path.startswith(SKIP_PREFIX):
        return False
    if " => " in path:
        path = path.split(" => ")[-1].strip()
    if not path.endswith((".py", ".md")):
        return False
    return any(path.startswith(p) for p in prefixes)


def parse_numstat(
    text: str,
    *,
    prefixes: tuple[str, ...],
) -> tuple[int, dict[str, int], dict[str, int], dict[str, int]]:
    """Return commits, churn, net_delta, fix_counts."""
    commits = 0
    churn: dict[str, int] = defaultdict(int)
    delta: dict[str, int] = defaultdict(int)
    fixes: dict[str, int] = defaultdict(int)
    subject = ""
    for line in text.splitlines():
        if not line.strip():
            continue
        if "\t" not in line:
            subject = line
            commits += 1
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        add_s, del_s, path = parts[0], parts[1], parts[2]
        if " => " in path:
            path = path.split(" => ")[-1].strip()
        if not interesting(path, prefixes):
            continue
        try:
            added = 0 if add_s == "-" else int(add_s)
            deleted = 0 if del_s == "-" else int(del_s)
        except ValueError:
            continue
        churn[path] += 1
        delta[path] += added - deleted
        if FIX_RE.search(subject):
            fixes[path] += 1
    return commits, churn, delta, fixes


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--churn-min", type=int, default=8)
    ap.add_argument("--grow-min", type=int, default=80)
    ap.add_argument("--fix-min", type=int, default=3)
    ap.add_argument("--top", type=int, default=TOP_N)
    ap.add_argument(
        "--path",
        action="append",
        dest="paths",
        default=None,
        help="Path prefix to include (repeatable). Default: pipeline/",
    )
    ap.add_argument(
        "--numstat-file",
        type=Path,
        default=None,
        help="Use this git-log --numstat text instead of invoking git (tests).",
    )
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    prefixes = tuple(args.paths) if args.paths else DEFAULT_PATHS
    prefixes = tuple(p if p.endswith("/") else p + "/" for p in prefixes)
    sample = root / "notes" / "qc" / "_samples" / "temporal"
    sample.mkdir(parents=True, exist_ok=True)
    out = args.out or (sample / "findings.json")
    table_path = sample / "TABLE.md"

    git_exit = 0
    cmd = f"git log --since={args.days}.days --numstat --format=%s"
    if args.numstat_file is not None:
        text = args.numstat_file.read_text(encoding="utf-8", errors="replace")
        cmd = f"numstat-file {args.numstat_file}"
    else:
        text, git_exit = git(root, ["log", f"--since={args.days}.days", "--numstat", "--format=%s"])

    commits, churn, delta, fixes = parse_numstat(text, prefixes=prefixes)

    def is_churn(p: str) -> bool:
        return churn[p] >= args.churn_min

    def is_grow(p: str) -> bool:
        return delta[p] >= args.grow_min

    def is_fix(p: str) -> bool:
        return fixes[p] >= args.fix_min

    hot = [p for p in churn if is_churn(p) or is_grow(p) or is_fix(p)]

    def score(p: str) -> tuple[int, int, int, int]:
        triple = int(is_churn(p) and is_grow(p) and is_fix(p))
        return (triple, churn[p], delta[p], fixes[p])

    hot_sorted = sorted(hot, key=score, reverse=True)
    top_paths = hot_sorted[: max(0, args.top)]
    omitted = max(0, len(hot_sorted) - len(top_paths))

    findings: list[dict] = []
    rows: list[tuple[str, str, str]] = []

    def add(
        fid: str,
        path: str,
        pattern: str,
        why: str,
        evidence: str,
        severity: str,
    ) -> None:
        findings.append(
            {
                "id": fid,
                "severity": severity,
                "control": "qc-temporal",
                "title": f"{pattern}: {path}",
                "evidence": evidence,
                "paths": [path],
                "effort": "S",
                "rule": f"T01_{pattern}",
                "recommendation": "Observation only. Do not auto-LFG. Not an implement order.",
                "tags": ["temporal", pattern],
                "tool": "qc-temporal",
            }
        )
        rows.append((path, pattern, why))

    if git_exit != 0 and not args.numstat_file:
        findings.append(
            {
                "id": "temporal-git-failed",
                "severity": "info",
                "control": "qc-temporal",
                "title": "git log failed; no temporal observation",
                "evidence": f"exit_code={git_exit}",
                "paths": [],
                "effort": "S",
                "rule": "T00_git_failed",
                "tags": ["tool_missing"],
                "tool": "qc-temporal",
            }
        )
    else:
        for path in top_paths:
            sev = (
                "medium"
                if (is_churn(path) and is_grow(path) and is_fix(path))
                else "info"
            )
            if is_churn(path):
                add(
                    f"temporal-churn-{len(findings)+1}",
                    path,
                    "churn",
                    f"{churn[path]} commits in {args.days}d — same seam keeps moving",
                    f"commits={churn[path]} window_days={args.days}",
                    sev,
                )
            if is_grow(path):
                add(
                    f"temporal-grow-{len(findings)+1}",
                    path,
                    "grow",
                    f"net +{delta[path]} lines in {args.days}d",
                    f"net_lines={delta[path]}",
                    sev,
                )
            if is_fix(path):
                add(
                    f"temporal-fix-{len(findings)+1}",
                    path,
                    "repeat-fix",
                    f"{fixes[path]} fix-titled commits (fix(/hotfix/bugfix)",
                    f"fix_commits={fixes[path]}",
                    sev,
                )
        if omitted:
            findings.append(
                {
                    "id": "temporal-omitted",
                    "severity": "info",
                    "control": "qc-temporal",
                    "title": f"{omitted} additional hotspot paths omitted (top {args.top})",
                    "evidence": f"hotspots={len(hot_sorted)} shown={len(top_paths)} omitted={omitted}",
                    "paths": [],
                    "effort": "S",
                    "rule": "T00_omitted",
                    "tags": ["pass_summary"],
                    "tool": "qc-temporal",
                }
            )
        if not findings:
            findings.append(
                {
                    "id": "temporal-pass",
                    "severity": "info",
                    "control": "qc-temporal",
                    "title": "No temporal-direction hotspots in window",
                    "evidence": f"commits_scanned={commits} window_days={args.days}",
                    "paths": [],
                    "effort": "S",
                    "rule": "T00_pass",
                    "tags": ["pass_summary"],
                    "tool": "qc-temporal",
                }
            )

    summary = {k: 0 for k in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[f["severity"]] = summary.get(f["severity"], 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-temporal",
        "profile": "leaf",
        "scope": {
            "paths": list(prefixes),
            "note": f"git log --since={args.days}.days --numstat; top={args.top}",
        },
        "commands_run": [{"cmd": cmd, "exit_code": git_exit}],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "factory health ≠ goal_proven_human",
            "git history is observation not a proof crown",
            "table ≠ implement order",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")

    lines = [
        "| file | pattern | why-direction-wrong |",
        "|------|---------|---------------------|",
    ]
    if rows:
        for path, pattern, why in rows:
            lines.append(f"| `{path}` | {pattern} | {why} |")
    else:
        lines.append("| — | pass | no hotspot in window |")
    table_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(table_path)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
