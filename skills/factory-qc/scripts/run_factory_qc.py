#!/usr/bin/env python3
"""factory-qc meta: run leaf scanners, merge findings.v0, write stamp report."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# leaf_id -> (relative script under .grok/skills, extra args list)
LEAF_SCRIPTS: dict[str, tuple[str, list[str]]] = {
    "qc-static": ("qc-static/scripts/run_static.py", []),
    "qc-contracts": ("qc-contracts/scripts/run_contracts.py", []),
    "qc-honesty": ("qc-honesty/scripts/run_honesty.py", []),
    "qc-errors": ("qc-errors/scripts/run_errors.py", []),
    "qc-tests": ("qc-tests/scripts/run_tests.py", ["--skip-smoke"]),
    "qc-security": ("qc-security/scripts/run_security.py", []),
    "qc-runtime-control": ("qc-runtime-control/scripts/run_runtime_control.py", []),
    "qc-coupling-debt": ("qc-coupling-debt/scripts/run_debt.py", []),
    "qc-temporal": ("qc-temporal/scripts/run_temporal.py", []),
}

PRE_MERGE = [
    "qc-static",
    "qc-contracts",
    "qc-honesty",
    "qc-errors",
    "qc-tests",
    "qc-security",
    "qc-runtime-control",
]
DEEP_AUDIT = PRE_MERGE + ["qc-coupling-debt", "qc-temporal"]


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")


def _control_gap(leaf: str, evidence: str) -> dict:
    return {
        "id": f"meta-gap-{leaf}",
        "severity": "info",
        "control": "factory-qc",
        "title": f"Leaf missing or failed to produce findings: {leaf}",
        "evidence": evidence[:500],
        "paths": [],
        "effort": "S",
        "tags": ["control_gap"],
        "tool": "factory-qc",
        "recommendation": f"Install/fix leaf {leaf} or skip with --skip-leaves",
    }


def run_leaf(
    root: Path, leaf: str, stamp_dir: Path
) -> tuple[list[dict], dict | None, int]:
    """Return (findings, envelope_or_none, exit_code)."""
    rel, extra = LEAF_SCRIPTS[leaf]
    script = root / ".grok" / "skills" / rel
    if not script.is_file():
        return [_control_gap(leaf, f"script not found: {rel}")], None, 127

    leaf_out = stamp_dir / "leaves" / f"{leaf}.json"
    leaf_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(script),
        "--repo-root",
        str(root),
        "--out",
        str(leaf_out),
        *extra,
    ]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=600,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return [_control_gap(leaf, str(exc))], None, 124

    if not leaf_out.is_file():
        return [
            _control_gap(
                leaf,
                f"exit={proc.returncode}; no JSON written; stderr={(proc.stderr or '')[-300:]}",
            )
        ], None, proc.returncode

    try:
        env = json.loads(leaf_out.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [_control_gap(leaf, f"invalid JSON: {exc}")], None, proc.returncode

    findings = list(env.get("findings") or [])
    if proc.returncode != 0:
        findings.append(
            {
                "id": f"meta-leaf-exit-{leaf}",
                "severity": "high",
                "control": "factory-qc",
                "title": f"Leaf {leaf} exited {proc.returncode}",
                "evidence": (proc.stderr or proc.stdout or "")[-400:],
                "paths": [str(leaf_out.relative_to(root)).replace("\\", "/")],
                "effort": "M",
                "tags": [],
                "tool": "factory-qc",
                "recommendation": f"Investigate {leaf} runner",
            }
        )
    if not findings:
        findings.append(_control_gap(leaf, "empty findings list"))
    return findings, env, proc.returncode


def merge_summaries(findings: list[dict]) -> dict[str, int]:
    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        k = str(f.get("severity", "info"))
        if k not in summary:
            summary[k] = 0
        summary[k] += 1
    return summary


def write_report(
    path: Path,
    *,
    stamp: str,
    profile: str,
    leaves: list[str],
    summary: dict[str, int],
    findings: list[dict],
    commands: list[dict],
    ccr_note: str,
) -> None:
    top = [f for f in findings if f.get("severity") in ("critical", "high", "medium")]
    top = sorted(
        top,
        key=lambda f: {"critical": 0, "high": 1, "medium": 2}.get(str(f.get("severity")), 9),
    )[:25]
    lines = [
        f"# Factory QC Report",
        "",
        f"**Stamp:** `{stamp}`  ",
        f"**Profile:** `{profile}`  ",
        f"**Control:** `factory-qc`  ",
        f"**Generated at:** {_iso()}  ",
        "",
        "## Executive summary",
        "",
        f"- Finding counts: critical={summary.get('critical', 0)} · high={summary.get('high', 0)} · "
        f"medium={summary.get('medium', 0)} · low={summary.get('low', 0)} · info={summary.get('info', 0)}",
        f"- Leaves run: {', '.join(leaves)}",
        f"- Headline: {len(top)} critical/high/medium findings listed below (cap 25)",
        "",
        "## Scope",
        "",
        f"- Profile: {profile}",
        f"- Repo stamp dir: `notes/qc/{stamp}/`",
        "",
        "## Commands run",
        "",
        "| Command | Exit |",
        "|---------|------|",
    ]
    for c in commands:
        lines.append(f"| `{c.get('cmd', '')[:120]}` | {c.get('exit_code')} |")
    lines.extend(
        [
            "",
            "## Findings (top residual)",
            "",
            "| Severity | Control | Id | Title | Paths |",
            "|----------|---------|-----|-------|-------|",
        ]
    )
    for f in top:
        paths = ",".join((f.get("paths") or [])[:2])
        lines.append(
            f"| {f.get('severity')} | {f.get('control')} | {f.get('id')} | "
            f"{str(f.get('title', ''))[:80]} | {paths[:60]} |"
        )
    if not top:
        lines.append("| info | factory-qc | — | No medium+ residual (info-only run) | |")
    lines.extend(
        [
            "",
            "## Delegates",
            "",
            ccr_note,
            "",
            "## NON_CLAIMS",
            "",
            "- Factory health **≠** `field_proven`",
            "- Factory health **≠** `goal_proven` / `goal_proven_human`",
            "- This report **≠** product aim quality or dual-gate ship proof",
            "- Report is **aim fuel** for `/gap-to-plan`, `/implement Medium+`, or "
            "`/findings-triage` (large low residual) — **not** auto-LFG / auto-gauntlet",
            "",
            "## Next",
            "",
            "See `AIM_FROM_QC.md` in this stamp directory.",
            "",
            "Soft stream (user confirm; never auto-ship):",
            "",
            "```text",
            "/factory-qc-handoff",
            "  → Medium+  → /implement Medium+  or  /gap-to-plan",
            "  → low bulk → /findings-triage → /implement pack P1",
            "  → stop",
            "```",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_aim(path: Path, stamp: str, summary: dict[str, int]) -> None:
    n_mp = int(summary.get("critical", 0) or 0) + int(
        summary.get("high", 0) or 0
    ) + int(summary.get("medium", 0) or 0)
    n_low = int(summary.get("low", 0) or 0)
    # Adaptive options: prefer findings-triage when Medium+ clean and lows dominate.
    low_thr = 20
    options: list[str] = []
    if n_mp > 0:
        options.extend(
            [
                "1. `/gap-to-plan` with this aim + report as fuel",
                f"2. `/implement Medium+ findings from notes/qc/{stamp}/REPORT.md`",
            ]
        )
        n = 3
        if n_low >= low_thr:
            options.append(
                f"{n}. `/findings-triage` — bucket lows (after or beside Medium+); "
                f"`--stamp {stamp}` then `/implement` pack P1"
            )
            n += 1
        options.append(f"{n}. stop")
    else:
        if n_low >= low_thr:
            options.extend(
                [
                    f"1. `/findings-triage` — **preferred** for low residual "
                    f"(medium+=0, low={n_low})",
                    f"       python .grok/skills/findings-triage/scripts/"
                    f"run_findings_triage.py --repo-root . --stamp {stamp}",
                    "       then `/implement pack P1 from notes/triage/"
                    f"{stamp}/packs.json`",
                    "2. `/gap-to-plan` only if you want a multi-plan residual aim",
                    "3. stop — accept low residual",
                ]
            )
        elif n_low > 0:
            options.extend(
                [
                    f"1. `/findings-triage` (optional; low={n_low} < {low_thr})",
                    f"2. stop — or `/implement` only if you name specific sites",
                ]
            )
        else:
            options.extend(
                [
                    "1. stop — no Medium+ / low residual",
                    "2. `/factory-qc --profile deep-audit` if you want coupling-debt",
                ]
            )

    path.write_text(
        "\n".join(
            [
                "# Aim stub from factory-qc",
                "",
                f"Close factory QC residual from `notes/qc/{stamp}/REPORT.md`.",
                "",
                f"Counts: critical={summary.get('critical', 0)} high={summary.get('high', 0)} "
                f"medium={summary.get('medium', 0)} low={summary.get('low', 0)} "
                f"info={summary.get('info', 0)}",
                f"medium+: {n_mp}",
                "",
                "Constraints:",
                "- Structure-safe; do not weaken dual-gate honesty",
                "- Prefer Medium+ first; do **not** `/implement` all lows blind",
                f"- If medium+=0 and low>={low_thr}: prefer `/findings-triage` packs",
                "- Factory health residual ≠ product field_proven",
                "",
                "Options:",
                *options,
                "",
                "Handoff helper (prompt only):",
                f"  python .grok/skills/factory-qc-handoff/scripts/print_handoff.py "
                f"--repo-root . --stamp {stamp}",
                "",
                "Do **not** auto-run LFG/gauntlet/implement/findings-triage from this "
                "file alone.",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--profile", choices=("pre-merge", "deep-audit"), default="pre-merge")
    ap.add_argument(
        "--skip-leaves",
        default="",
        help="Comma-separated leaf ids to skip",
    )
    ap.add_argument("--stamp", default="", help="Override stamp id")
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    skip = {x.strip() for x in args.skip_leaves.split(",") if x.strip()}
    leaves = list(DEEP_AUDIT if args.profile == "deep-audit" else PRE_MERGE)
    leaves = [L for L in leaves if L not in skip]

    stamp = args.stamp or _stamp()
    stamp_dir = root / "notes" / "qc" / stamp
    stamp_dir.mkdir(parents=True, exist_ok=True)

    all_findings: list[dict] = []
    commands: list[dict] = []
    for leaf in leaves:
        findings, _env, code = run_leaf(root, leaf, stamp_dir)
        all_findings.extend(findings)
        rel, extra = LEAF_SCRIPTS[leaf]
        commands.append(
            {
                "cmd": f"python .grok/skills/{rel} --repo-root . {' '.join(extra)}".strip(),
                "exit_code": code,
                "leaf": leaf,
            }
        )

    if args.profile == "deep-audit":
        all_findings.append(
            {
                "id": "meta-ccr-delegate-001",
                "severity": "info",
                "control": "factory-qc",
                "title": "Optional deep-audit delegate: comprehensive-codebase-review",
                "evidence": "Do not reimplement CCR; run /comprehensive-codebase-review separately for prose audit",
                "paths": [],
                "effort": "L",
                "tags": ["pass_summary", "delegate"],
                "tool": "factory-qc",
                "recommendation": "Run CCR when deep prose audit needed; attach report path to stamp manually if desired",
            }
        )
        ccr_note = (
            "Optional: run `/comprehensive-codebase-review` (not executed by this meta skill). "
            "Attach its report path here if run separately."
        )
    else:
        ccr_note = "CCR not in pre-merge profile. Use deep-audit for delegate note."

    summary = merge_summaries(all_findings)
    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "factory-qc",
        "profile": args.profile,
        "scope": {
            "paths": ["pipeline/"],
            "note": str(root),
            "leaves": leaves,
            "stamp": stamp,
        },
        "commands_run": commands,
        "summary": summary,
        "findings": all_findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "factory health ≠ goal_proven_human",
            "report-only — not auto-LFG / auto-gauntlet / implement",
            "does not reimplement comprehensive-codebase-review",
        ],
    }

    findings_path = stamp_dir / "findings.json"
    findings_path.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    write_report(
        stamp_dir / "REPORT.md",
        stamp=stamp,
        profile=args.profile,
        leaves=leaves,
        summary=summary,
        findings=all_findings,
        commands=commands,
        ccr_note=ccr_note,
    )
    write_aim(stamp_dir / "AIM_FROM_QC.md", stamp, summary)
    scope = {
        "schema": "factory_qc_scope.v0",
        "stamp": stamp,
        "profile": args.profile,
        "leaves": leaves,
        "skip_leaves": sorted(skip),
        "repo_root": str(root),
        "generated_at": _iso(),
    }
    (stamp_dir / "scope.json").write_text(json.dumps(scope, indent=2) + "\n", encoding="utf-8")

    # latest pointer
    latest = root / "notes" / "qc" / "LATEST"
    latest.write_text(stamp + "\n", encoding="utf-8")

    print(f"stamp={stamp}")
    print(f"wrote {findings_path}")
    print(f"wrote {stamp_dir / 'REPORT.md'}")
    print(f"wrote {stamp_dir / 'AIM_FROM_QC.md'}")
    print(f"summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
