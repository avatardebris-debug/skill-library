#!/usr/bin/env python3
"""Print prompt-only handoff from a factory-qc stamp. Never runs ship skills."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Prefer findings-triage when Medium+ is empty/small and low residual is large.
DEFAULT_LOW_TRIAGE_THRESHOLD = 20


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    # Bare `--repo-root` (no value) and omit both mean cwd.
    ap.add_argument(
        "--repo-root",
        type=Path,
        nargs="?",
        const=Path.cwd(),
        default=Path.cwd(),
        help="Repo root (default: current directory). Bare --repo-root also means cwd.",
    )
    ap.add_argument("--stamp", default="", help="Stamp id; default notes/qc/LATEST")
    ap.add_argument("--top", type=int, default=12, help="Max medium+ titles to list")
    ap.add_argument(
        "--low-triage-threshold",
        type=int,
        default=DEFAULT_LOW_TRIAGE_THRESHOLD,
        help=(
            "When medium+=0 and low>=this, recommend /findings-triage "
            f"(default {DEFAULT_LOW_TRIAGE_THRESHOLD})"
        ),
    )
    args = ap.parse_args(argv)
    root = (args.repo_root or Path.cwd()).resolve()
    qc = root / "notes" / "qc"
    stamp = args.stamp.strip()
    if not stamp:
        latest = qc / "LATEST"
        if not latest.is_file():
            print("ERROR: notes/qc/LATEST missing; run factory-qc first", file=sys.stderr)
            return 2
        stamp = latest.read_text(encoding="utf-8").strip()
    stamp_dir = qc / stamp
    findings_path = stamp_dir / "findings.json"
    if not findings_path.is_file():
        print(f"ERROR: missing {findings_path}", file=sys.stderr)
        return 2

    data = json.loads(findings_path.read_text(encoding="utf-8"))
    summary = data.get("summary") or {}
    findings = list(data.get("findings") or [])
    profile = data.get("profile") or "unknown"
    medium_plus = [
        f
        for f in findings
        if f.get("severity") in ("critical", "high", "medium")
    ]
    medium_plus.sort(
        key=lambda f: {"critical": 0, "high": 1, "medium": 2}.get(
            str(f.get("severity")), 9
        )
    )
    n_crit = int(summary.get("critical", 0) or 0)
    n_high = int(summary.get("high", 0) or 0)
    n_med = int(summary.get("medium", 0) or 0)
    n_low = int(summary.get("low", 0) or 0)
    n_info = int(summary.get("info", 0) or 0)
    n_mp = len(medium_plus)
    # Prefer summary if present; fall back to counted medium+
    if not any(k in summary for k in ("critical", "high", "medium", "low")):
        n_mp = len(medium_plus)
        n_low = sum(1 for f in findings if f.get("severity") == "low")

    thr = max(0, int(args.low_triage_threshold))
    recommend_triage = n_mp == 0 and n_low >= thr
    triage_dir = root / "notes" / "triage" / stamp
    triage_exists = (triage_dir / "packs.json").is_file()

    aim_path = stamp_dir / "AIM_FROM_QC.md"
    aim_line = ""
    if aim_path.is_file():
        for line in aim_path.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.startswith("#"):
                aim_line = line.strip()
                break

    print("=" * 60)
    print("factory-qc-handoff (PROMPT ONLY — does not execute ship skills)")
    print("=" * 60)
    print(f"stamp:    notes/qc/{stamp}/")
    print(f"profile:  {profile}")
    print(
        "counts:   "
        f"critical={n_crit} high={n_high} medium={n_med} "
        f"low={n_low} info={n_info}"
    )
    print(f"medium+:  {n_mp} findings")
    if aim_line:
        print(f"aim:      {aim_line}")
    if recommend_triage:
        print(
            f"hint:     medium+=0 and low>={thr} → prefer /findings-triage "
            "before bulk implement"
        )
    if triage_exists:
        print(f"triage:   notes/triage/{stamp}/ already present (packs.json)")
    print()
    print("Top residual (Medium+):")
    if not medium_plus:
        print("  (none — info-only run or clean)")
    for f in medium_plus[: args.top]:
        title = str(f.get("title") or "")[:90]
        print(f"  - [{f.get('severity')}] {f.get('control')}: {title}")
    if len(medium_plus) > args.top:
        print(f"  … +{len(medium_plus) - args.top} more")
    print()
    print("Choose ONE (user confirm required before any skill runs):")
    print()

    opt = 1
    if n_mp > 0:
        print(f"  {opt}) /gap-to-plan")
        print(f"       Aim fuel: notes/qc/{stamp}/AIM_FROM_QC.md + REPORT.md")
        print()
        opt += 1
        print(f"  {opt}) /implement Medium+ findings from")
        print(f"       notes/qc/{stamp}/REPORT.md")
        print()
        opt += 1
        if n_low >= thr:
            print(f"  {opt}) /findings-triage")
            print(
                f"       Bucket lows after Medium+ (or in parallel): "
                f"--stamp {stamp}"
            )
            print(
                "       Then /implement pack P1 from notes/triage/<stamp>/packs.json"
            )
            print()
            opt += 1
    else:
        # Medium+ clean
        if recommend_triage or n_low > 0:
            print(f"  {opt}) /findings-triage")
            print(f"       Bucket low residual: --stamp {stamp}")
            print(
                "       python .grok/skills/findings-triage/scripts/"
                "run_findings_triage.py --repo-root . "
                f"--stamp {stamp}"
            )
            if triage_exists:
                print(
                    f"       (existing) /implement pack P1 from "
                    f"notes/triage/{stamp}/packs.json"
                )
            else:
                print(
                    "       Then /implement pack P1 from "
                    "notes/triage/<stamp>/packs.json"
                )
            print()
            opt += 1
        print(f"  {opt}) /gap-to-plan")
        print(
            f"       Only if you want a multi-plan residual aim "
            f"(fuel: notes/qc/{stamp}/AIM_FROM_QC.md)"
        )
        print()
        opt += 1

    print(f"  {opt}) stop")
    print()
    print("FORBIDDEN (this skill never auto-runs):")
    print(
        "  /lfg  /encore  /universal-gauntlet  /gap-to-plan  "
        "/implement  /findings-triage"
    )
    print()
    print("NON_CLAIMS: factory health ≠ field_proven; handoff text ≠ execution.")
    print("Stream: /factory-qc → handoff → [/findings-triage] → /implement pack")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
