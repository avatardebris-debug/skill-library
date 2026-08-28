#!/usr/bin/env python3
"""
findings-triage: bucket factory-qc findings → notes/triage/<stamp>/.

Measure-only packing. Never runs implement/LFG/gauntlet.
Factory health ≠ field_proven.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA = "findings_triage_packs.v0"

# Path / evidence heuristics → bucket A|B|C (else D for low/info)
_A_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"shell_safety",
        r"field_prove",
        r"field_test_runner",
        r"evidence_edges",
        r"_evidence_edges",
        r"hypothesis_promote",
        r"path_safe_slug",
        r"constitution",
        r"mcp_factory",
        r"_mcp_factory",
        r"github_publish",
        r"capability_tools",
        r"\block\b",
        r"_acquire_file_lock",
    )
]
_B_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"run_loop_health",
        r"run_loop_budget",
        r"run_loop",
        r"control_plane",
        r"complete_gate",
        r"stall_hygiene",
        r"dead_role",
        r"project_phase",
        r"pipeline/runner\.py",
        r"/runner\.py",
    )
]
_C_PATTERNS = [re.compile(r"pipeline[/\\]agents[/\\]", re.I)]

_SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _paths_blob(f: dict[str, Any]) -> str:
    parts: list[str] = []
    for p in f.get("paths") or []:
        parts.append(str(p))
    ev = f.get("evidence") or ""
    parts.append(str(ev))
    parts.append(str(f.get("title") or ""))
    parts.append(str(f.get("id") or ""))
    return "\n".join(parts)


def _bucket_for(f: dict[str, Any]) -> str:
    sev = str(f.get("severity") or "info").lower()
    blob = _paths_blob(f)
    # Medium+ always ship-candidate; still assign path bucket for labeling
    path_bucket = "D"
    for pat in _A_PATTERNS:
        if pat.search(blob):
            path_bucket = "A"
            break
    if path_bucket == "D":
        for pat in _B_PATTERNS:
            if pat.search(blob):
                path_bucket = "B"
                break
    if path_bucket == "D":
        for pat in _C_PATTERNS:
            if pat.search(blob):
                path_bucket = "C"
                break
    if sev in ("critical", "high", "medium"):
        # Elevate label: keep path bucket but mark as medium_plus via severity
        return path_bucket if path_bucket != "D" else "A"
    return path_bucket


def _item(f: dict[str, Any], bucket: str) -> dict[str, Any]:
    paths = f.get("paths") or []
    path = str(paths[0]) if paths else ""
    line = f.get("line")
    if line is None and f.get("evidence"):
        m = re.search(r":(\d+):", str(f.get("evidence")))
        if m:
            line = int(m.group(1))
    return {
        "id": f.get("id"),
        "severity": f.get("severity"),
        "bucket": bucket,
        "path": path,
        "line": line,
        "title": f.get("title"),
        "rule": f.get("rule") or f.get("control"),
        "recommendation": f.get("recommendation"),
        "control": f.get("control"),
    }


def _load_findings(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected object in {path}")
    return data


def run(
    *,
    repo_root: Path,
    stamp: str,
    findings_json: Path | None,
    max_per_pack: int,
    max_packs: int,
) -> Path:
    root = repo_root.resolve()
    qc = root / "notes" / "qc"
    if findings_json is not None:
        fj = findings_json.resolve()
        stamp_id = stamp.strip() or fj.parent.name
    else:
        stamp_id = stamp.strip()
        if not stamp_id:
            latest = qc / "LATEST"
            if not latest.is_file():
                raise FileNotFoundError("notes/qc/LATEST missing; run factory-qc first")
            stamp_id = latest.read_text(encoding="utf-8").strip()
        fj = qc / stamp_id / "findings.json"
    if not fj.is_file():
        raise FileNotFoundError(f"missing findings: {fj}")

    data = _load_findings(fj)
    findings = list(data.get("findings") or [])
    summary = dict(data.get("summary") or {})
    if not summary:
        summary = dict(Counter(str(f.get("severity") or "info") for f in findings))

    # Assign buckets
    by_bucket: dict[str, list[dict[str, Any]]] = {
        "A": [],
        "B": [],
        "C": [],
        "D": [],
    }
    medium_plus: list[dict[str, Any]] = []
    for f in findings:
        b = _bucket_for(f)
        by_bucket[b].append(f)
        if str(f.get("severity") or "").lower() in ("critical", "high", "medium"):
            medium_plus.append(f)

    def sort_key(f: dict[str, Any]) -> tuple[int, str]:
        sev = str(f.get("severity") or "info").lower()
        return (_SEV_ORDER.get(sev, 9), str(f.get("id") or ""))

    for b in by_bucket:
        by_bucket[b].sort(key=sort_key)
    medium_plus.sort(key=sort_key)

    # Build ship queue: medium+ first, then A, then B (not C/D by default)
    ship_queue: list[tuple[str, dict[str, Any]]] = []
    seen: set[str] = set()

    def push(bucket: str, f: dict[str, Any]) -> None:
        fid = str(f.get("id") or id(f))
        if fid in seen:
            return
        seen.add(fid)
        ship_queue.append((bucket, f))

    for f in medium_plus:
        push(_bucket_for(f), f)
    for f in by_bucket["A"]:
        push("A", f)
    for f in by_bucket["B"]:
        push("B", f)

    # Pack up to max_packs * max_per_pack
    packs: list[dict[str, Any]] = []
    overflow: list[dict[str, Any]] = []
    idx = 0
    pack_n = 0
    while idx < len(ship_queue) and pack_n < max_packs:
        chunk = ship_queue[idx : idx + max_per_pack]
        idx += len(chunk)
        pack_n += 1
        focus = sorted({b for b, _ in chunk})
        items = [_item(f, b) for b, f in chunk]
        # Title
        if any(
            str(f.get("severity")).lower() in ("critical", "high", "medium")
            for _, f in chunk
        ):
            title = f"Ship Medium+/elevated residual pack {pack_n}"
        elif "A" in focus:
            title = f"Safety-adjacent soft-fail / path pack {pack_n}"
        else:
            title = f"Hot control-plane soft-fail pack {pack_n}"
        packs.append(
            {
                "id": f"P{pack_n}",
                "title": title,
                "bucket_focus": focus,
                "suggested_skill": "implement",
                "finding_ids": [str(i.get("id")) for i in items],
                "items": items,
            }
        )
    for b, f in ship_queue[idx:]:
        overflow.append(_item(f, b))

    out_dir = root / "notes" / "triage" / stamp_id
    out_dir.mkdir(parents=True, exist_ok=True)

    packs_doc = {
        "schema": SCHEMA,
        "stamp": stamp_id,
        "source_findings": str(fj.relative_to(root)) if fj.is_relative_to(root) else str(fj),
        "generated_at": _iso(),
        "max_per_pack": max_per_pack,
        "max_packs": max_packs,
        "field_proven": False,
        "packs": packs,
    }
    (out_dir / "packs.json").write_text(
        json.dumps(packs_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    bucket_counts = {k: len(v) for k, v in by_bucket.items()}
    summary_out = {
        "schema": "findings_triage_summary.v0",
        "stamp": stamp_id,
        "generated_at": _iso(),
        "severity_summary": summary,
        "bucket_counts": bucket_counts,
        "medium_plus_count": len(medium_plus),
        "pack_ids": [p["id"] for p in packs],
        "pack_item_counts": {p["id"]: len(p["items"]) for p in packs},
        "overflow_count": len(overflow),
        "deferred_bucket_d": bucket_counts.get("D", 0),
        "field_proven": False,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary_out, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # TRIAGE.md
    lines = [
        f"# Findings triage — {stamp_id}",
        "",
        f"**Generated:** {_iso()}  ",
        f"**Source:** `{packs_doc['source_findings']}`  ",
        f"**Schema:** `{SCHEMA}`  ",
        "",
        "## Honesty",
        "",
        "- Factory health / triage **≠** `field_proven` / `goal_proven`",
        "- This skill **never** auto-runs `/implement`, `/lfg`, or gauntlet",
        "",
        "## Severity counts (source)",
        "",
        f"- critical: {summary.get('critical', 0)}",
        f"- high: {summary.get('high', 0)}",
        f"- medium: {summary.get('medium', 0)}",
        f"- low: {summary.get('low', 0)}",
        f"- info: {summary.get('info', 0)}",
        f"- medium+ total: {len(medium_plus)}",
        "",
        "## Bucket counts",
        "",
        f"| Bucket | Count | Meaning |",
        f"|--------|------:|---------|",
        f"| A safety-adjacent | {bucket_counts.get('A', 0)} | Prefer pack |",
        f"| B hot control-plane | {bucket_counts.get('B', 0)} | Pack with tests |",
        f"| C agent soft-except | {bucket_counts.get('C', 0)} | soft_log or defer |",
        f"| D accept residual | {bucket_counts.get('D', 0)} | Stop / DEFER.md |",
        "",
        "## Packs (ship candidates)",
        "",
    ]
    if not packs:
        lines.append("_No ship packs — Medium+ empty and no A/B residual under caps._")
        lines.append("")
    else:
        lines.append("| Pack | Items | Focus | Suggested |")
        lines.append("|------|------:|-------|-----------|")
        for p in packs:
            lines.append(
                f"| {p['id']} | {len(p['items'])} | "
                f"{','.join(p['bucket_focus'])} | `/{p['suggested_skill']}` |"
            )
        lines.append("")
        for p in packs:
            lines.append(f"### {p['id']}: {p['title']}")
            lines.append("")
            for it in p["items"][: max_per_pack]:
                loc = it.get("path") or "?"
                if it.get("line") is not None:
                    loc = f"{loc}:{it['line']}"
                lines.append(
                    f"- `{loc}` · [{it.get('severity')}] {it.get('title')} "
                    f"({it.get('rule')})"
                )
            lines.append("")
            lines.append("Suggested command:")
            lines.append("")
            lines.append("```text")
            lines.append(
                f"/implement Findings triage {p['id']} from notes/triage/{stamp_id}/packs.json: "
                f"only the finding_ids listed for {p['id']}; "
                f"prefer soft_log_exc over bare pass on A/B; no E02 bulk beyond pack; "
                f"no god-module splits; no field_proven claims"
            )
            lines.append("```")
            lines.append("")

    if overflow:
        lines.append("## Overflow (beyond max-packs)")
        lines.append("")
        lines.append(
            f"{len(overflow)} additional A/B/medium+ items not packed — "
            "re-run with higher `--max-packs` or open gap-to-plan."
        )
        lines.append("")

    lines.extend(
        [
            "## Next options (human gate)",
            "",
            "1. `/implement` pack **P1** (then P2…) from `packs.json`",
            "2. `/gap-to-plan` with this TRIAGE.md as fuel (multi-pack residual)",
            "3. **stop** — accept `DEFER.md` residual",
            "",
            "## Forbidden",
            "",
            "- Auto `/lfg` / `/encore` / gauntlet / implement without user confirm",
            "",
        ]
    )
    (out_dir / "TRIAGE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # DEFER.md
    defer_lines = [
        f"# Deferred residual — {stamp_id}",
        "",
        f"**Bucket D (accept):** {bucket_counts.get('D', 0)} findings  ",
        f"**Bucket C (agent soft, not packed by default):** {bucket_counts.get('C', 0)}  ",
        f"**Overflow unpacked A/B/medium+:** {len(overflow)}  ",
        "",
        "## Policy",
        "",
        "- D is **accepted residual** unless a site is promoted by human review.",
        "- C may get soft_log hygiene later; not a default implement pack.",
        "- Overflow needs a new triage run or gap-to-plan — do not silent-expand packs.",
        "",
        "## Honesty",
        "",
        "- Deferring ≠ fixed",
        "- Factory health ≠ field_proven",
        "",
    ]
    if overflow:
        defer_lines.append("## Overflow sample (up to 25)")
        defer_lines.append("")
        for it in overflow[:25]:
            loc = it.get("path") or "?"
            defer_lines.append(f"- `{loc}` · {it.get('id')} · {it.get('title')}")
        defer_lines.append("")
    (out_dir / "DEFER.md").write_text("\n".join(defer_lines) + "\n", encoding="utf-8")

    return out_dir


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repo root (default: cwd)",
    )
    ap.add_argument(
        "--stamp",
        default="",
        help="QC stamp id (default: notes/qc/LATEST)",
    )
    ap.add_argument(
        "--findings-json",
        type=Path,
        default=None,
        help="Explicit findings.json path (overrides stamp path)",
    )
    ap.add_argument("--max-per-pack", type=int, default=15)
    ap.add_argument("--max-packs", type=int, default=3)
    args = ap.parse_args(argv)

    try:
        out = run(
            repo_root=args.repo_root,
            stamp=args.stamp,
            findings_json=args.findings_json,
            max_per_pack=max(1, int(args.max_per_pack)),
            max_packs=max(0, int(args.max_packs)),
        )
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    summary_path = out / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    print("=" * 60)
    print("findings-triage (MEASURE ONLY — does not ship)")
    print("=" * 60)
    print(f"out:      {out}")
    print(f"stamp:    {summary.get('stamp')}")
    sev = summary.get("severity_summary") or {}
    print(
        "counts:   "
        f"critical={sev.get('critical', 0)} "
        f"high={sev.get('high', 0)} "
        f"medium={sev.get('medium', 0)} "
        f"low={sev.get('low', 0)} "
        f"info={sev.get('info', 0)}"
    )
    bc = summary.get("bucket_counts") or {}
    print(
        "buckets:  "
        f"A={bc.get('A', 0)} B={bc.get('B', 0)} "
        f"C={bc.get('C', 0)} D={bc.get('D', 0)}"
    )
    print(f"packs:    {', '.join(summary.get('pack_ids') or []) or '(none)'}")
    print(f"overflow: {summary.get('overflow_count', 0)}")
    print()
    print("Files: TRIAGE.md  packs.json  DEFER.md  summary.json")
    print()
    print("Choose ONE (user confirm before any ship skill):")
    print("  1) /implement pack P1 from notes/triage/<stamp>/packs.json")
    print("  2) /gap-to-plan using notes/triage/<stamp>/TRIAGE.md as fuel")
    print("  3) stop — accept DEFER residual")
    print()
    print("FORBIDDEN auto-run: /lfg /encore /gauntlet /implement /gap-to-plan")
    print("NON_CLAIM: factory health ≠ field_proven")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
