#!/usr/bin/env python3
"""qc-coupling-debt leaf: LOC hotspots + remeasure pointer → findings.v0."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {"__pycache__", ".git", "node_modules", ".venv", "venv"}


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def count_lines(path: Path) -> int:
    try:
        return sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
    except OSError:
        return 0


def package_loc(pkg_dir: Path) -> tuple[int, list[str]]:
    total = 0
    files: list[str] = []
    for p in pkg_dir.rglob("*.py"):
        if any(x in SKIP_DIRS for x in p.parts):
            continue
        if p.name.endswith(".bak_pre_split"):
            continue
        n = count_lines(p)
        total += n
        files.append(p.name)
    return total, files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--threshold", type=int, default=800)
    ap.add_argument("--residual-md", type=Path, default=None)
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "coupling_debt" / "findings.json")
    residual_md = args.residual_md or (
        root / "notes" / "qc" / "_samples" / "coupling_debt" / "residual.md"
    )
    pipeline = root / "pipeline"
    findings: list[dict] = []
    rows: list[tuple[str, int, str]] = []

    # Top-level modules
    if pipeline.is_dir():
        for p in sorted(pipeline.glob("*.py")):
            if p.name.startswith("_"):
                continue
            n = count_lines(p)
            rel = f"pipeline/{p.name}"
            rows.append((rel, n, "module"))
            if n >= args.threshold:
                findings.append(
                    {
                        "id": f"debt-loc-{p.stem}",
                        "severity": "medium",
                        "control": "qc-coupling-debt",
                        "title": f"Large module {rel} (~{n} LOC ≥ {args.threshold})",
                        "evidence": f"physical_lines={n}",
                        "paths": [rel],
                        "effort": "L",
                        "rule": "D01_loc_module",
                        "recommendation": "Ownership-split behind façade (playbook) when next series allows",
                        "tags": ["debt", "loc"],
                        "tool": "qc-coupling-debt",
                    }
                )
        # Packages pipeline/_foo
        for pkg in sorted(pipeline.iterdir()):
            if not pkg.is_dir() or not pkg.name.startswith("_"):
                continue
            if pkg.name in SKIP_DIRS:
                continue
            total, _files = package_loc(pkg)
            rel = f"pipeline/{pkg.name}/"
            rows.append((rel, total, "package"))
            # Flag if package still has huge single impl
            impl = pkg / "impl.py"
            if impl.is_file():
                impl_n = count_lines(impl)
                if impl_n >= args.threshold:
                    findings.append(
                        {
                            "id": f"debt-impl-{pkg.name}",
                            "severity": "medium",
                            "control": "qc-coupling-debt",
                            "title": f"Large package impl {rel}impl.py (~{impl_n} LOC)",
                            "evidence": f"impl_lines={impl_n} package_total={total}",
                            "paths": [f"{rel}impl.py"],
                            "effort": "L",
                            "rule": "D02_loc_impl",
                            "recommendation": "Continue ownership split of impl body",
                            "tags": ["debt", "loc"],
                            "tool": "qc-coupling-debt",
                        }
                    )

    remeasure = root / "notes" / "ops" / "god_module_safe_split_series_remeasure.md"
    if remeasure.is_file():
        findings.append(
            {
                "id": "debt-remeasure-present-001",
                "severity": "info",
                "control": "qc-coupling-debt",
                "title": "Series remeasure note present",
                "evidence": str(remeasure.relative_to(root)).replace("\\", "/"),
                "paths": [str(remeasure.relative_to(root)).replace("\\", "/")],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "Keep residual list updated after splits",
                "tool": "qc-coupling-debt",
            }
        )
    else:
        findings.append(
            {
                "id": "debt-remeasure-missing-001",
                "severity": "info",
                "control": "qc-coupling-debt",
                "title": "Series remeasure note missing",
                "evidence": "notes/ops/god_module_safe_split_series_remeasure.md not found",
                "paths": [],
                "effort": "S",
                "tags": ["control_gap"],
                "recommendation": "Add remeasure after series or ignore if N/A",
                "tool": "qc-coupling-debt",
            }
        )

    inv = root / "scripts" / "god_module_import_inventory.py"
    findings.append(
        {
            "id": "debt-inventory-script-001",
            "severity": "info",
            "control": "qc-coupling-debt",
            "title": (
                "Import inventory script available"
                if inv.is_file()
                else "Import inventory script missing"
            ),
            "evidence": "scripts/god_module_import_inventory.py",
            "paths": ["scripts/god_module_import_inventory.py"] if inv.is_file() else [],
            "effort": "S",
            "tags": ["pass_summary"] if inv.is_file() else ["tool_missing"],
            "recommendation": "Run inventory for fan-in before splits",
            "tool": "qc-coupling-debt",
        }
    )

    if not any(f.get("rule") in ("D01_loc_module", "D02_loc_impl") for f in findings):
        findings.append(
            {
                "id": "debt-pass-001",
                "severity": "info",
                "control": "qc-coupling-debt",
                "title": f"No modules/packages ≥ {args.threshold} LOC (pass_summary)",
                "evidence": f"rows_checked={len(rows)}",
                "paths": ["pipeline/"],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "None",
                "tool": "qc-coupling-debt",
            }
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = summary.get(str(f.get("severity", "info")), 0) + 1

    # residual markdown
    residual_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Coupling / LOC residual (qc-coupling-debt sample)",
        "",
        f"Threshold: **{args.threshold}** physical lines",
        "",
        "| Path | LOC | Kind |",
        "|------|----:|------|",
    ]
    for rel, n, kind in sorted(rows, key=lambda x: -x[1])[:40]:
        mark = " **≥ thr**" if n >= args.threshold else ""
        lines.append(f"| `{rel}` | {n} | {kind}{mark} |")
    lines.append("")
    lines.append("Does not claim maintainability closed. Report-only.")
    lines.append("")
    residual_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-coupling-debt",
        "profile": "leaf",
        "scope": {"paths": ["pipeline/"], "note": str(root), "threshold": args.threshold},
        "commands_run": [
            {"cmd": f"qc-coupling-debt loc_scan threshold={args.threshold}", "exit_code": 0}
        ],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "does not split modules",
            "residual list ≠ maintainability closed",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    print(f"wrote {residual_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
