#!/usr/bin/env python3
"""qc-runtime-control leaf: static proxies for overnight stall classes → findings.v0."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

CONTROL = "qc-runtime-control"

# Modules that form the overnight control plane
HOT_FILES = (
    "pipeline/run_loop.py",
    "pipeline/run_loop_health.py",
    "pipeline/health_checks.py",
    "pipeline/project_phase.py",
    "pipeline/control_plane_invariants.py",
    "pipeline/message_bus.py",
    "pipeline/engines/driver.py",
)


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _finding(
    fid: str,
    severity: str,
    title: str,
    *,
    path: str = "",
    line: int | None = None,
    evidence: str = "",
    recommendation: str = "",
    tags: list[str] | None = None,
) -> dict:
    return {
        "id": fid,
        "severity": severity,
        "control": CONTROL,
        "title": title,
        "evidence": evidence[:800],
        "paths": [path] if path else [],
        "line": line,
        "effort": "S",
        "tags": tags or ["runtime-control"],
        "recommendation": recommendation or "See control_plane_invariants + overnight postmortem",
        "tool": CONTROL,
    }


def _read(root: Path, rel: str) -> tuple[str, list[str]]:
    p = root / rel
    if not p.is_file():
        return "", []
    text = p.read_text(encoding="utf-8", errors="replace")
    return text, text.splitlines()


def _def_in_text(text: str, name: str) -> bool:
    """True if *name* is defined as a function in *text* (def or async def)."""
    if not text or not name:
        return False
    return bool(re.search(rf"(?m)^\s*(?:async\s+)?def\s+{re.escape(name)}\s*\(", text))


def _private_package_dir(root: Path, public_rel: str) -> Path | None:
    """pipeline/foo.py → pipeline/_foo/ when that package directory exists."""
    p = Path(public_rel)
    if p.suffix != ".py" or len(p.parts) < 2:
        return None
    pkg = root / p.parent / f"_{p.stem}"
    return pkg if pkg.is_dir() else None


def _looks_like_reexport_facade(text: str, public_stem: str) -> bool:
    """Heuristic: thin monofile re-exports from pipeline._<stem> package."""
    if not text:
        return False
    # Explicit private package import surface
    if re.search(rf"pipeline\._{re.escape(public_stem)}\b", text):
        return True
    if re.search(rf"from\s+pipeline\._{re.escape(public_stem)}", text):
        return True
    # Generic thin-façade markers used in this factory
    if "import *" in text and re.search(r"pipeline\._\w+", text):
        return True
    return False


def _package_py_texts(pkg: Path) -> list[tuple[Path, str]]:
    """Read non-backup .py files under a private package (shallow-ish rglob)."""
    out: list[tuple[Path, str]] = []
    if not pkg.is_dir():
        return out
    for p in sorted(pkg.rglob("*.py")):
        name = p.name
        # skip backups / cache artifacts
        if name.endswith(".bak") or ".bak_" in name or "bak_pre" in name:
            continue
        if "__pycache__" in p.parts:
            continue
        try:
            out.append((p, p.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    return out


def api_def_present(
    root: Path,
    *,
    public_rel: str,
    monofile_text: str,
    name: str,
) -> bool:
    """True if public API *name* is defined on monofile or re-exported package leaves.

    Façade-aware: thin ``pipeline/foo.py`` re-exporting ``pipeline/_foo/**`` does
    not need ``def name`` in the monofile when a leaf defines it.
    Fail-closed when neither monofile nor package has the def.
    """
    if _def_in_text(monofile_text, name):
        return True
    stem = Path(public_rel).stem
    pkg = _private_package_dir(root, public_rel)
    if pkg is None:
        return False
    # Only trust package leaves when monofile is a re-export façade (or empty
    # but package exists — still require re-export markers when monofile has content).
    if monofile_text.strip() and not _looks_like_reexport_facade(monofile_text, stem):
        return False
    for _p, text in _package_py_texts(pkg):
        if _def_in_text(text, name):
            return True
    return False


def _package_corpus_text(root: Path, public_rel: str, monofile_text: str) -> str:
    """Monofile + package leaf texts for façade-aware content scans (quantifier etc.)."""
    parts = [monofile_text or ""]
    pkg = _private_package_dir(root, public_rel)
    stem = Path(public_rel).stem
    if pkg is not None and (
        not monofile_text.strip() or _looks_like_reexport_facade(monofile_text, stem)
    ):
        for _p, t in _package_py_texts(pkg):
            parts.append(t)
    return "\n".join(parts)


def scan_repo(root: Path) -> list[dict]:
    findings: list[dict] = []
    n = 0

    def add(**kw):
        nonlocal n
        n += 1
        fid = kw.pop("fid", None) or f"rtc-{n:03d}"
        findings.append(_finding(fid, **kw))

    # --- S_DEAD_ROLE: all_queues_empty without classic idle helper ---
    rel = "pipeline/run_loop.py"
    text, lines = _read(root, rel)
    if text:
        uses_all = bool(re.search(r"\.all_queues_empty\s*\(", text))
        uses_classic = (
            "classic_roles_idle" in text or "has_active_work_for_roles" in text
        )
        if uses_all and not uses_classic:
            # find line
            ln = next(
                (i + 1 for i, L in enumerate(lines) if "all_queues_empty" in L),
                None,
            )
            add(
                severity="medium",
                title="S_DEAD_ROLE proxy: all_queues_empty without classic-role filter",
                path=rel,
                line=ln,
                evidence="all_queues_empty() present but classic_roles_idle/has_active_work_for_roles missing",
                recommendation="Use classic_roles_idle(bus, AGENT_ROLES) for overnight all_empty",
                tags=["S_DEAD_ROLE", "runtime-control"],
            )
        # Prefer shared helper
        if "all_empty" in text and "classic_roles_idle" not in text and uses_classic:
            # has_active_work_for_roles alone is OK
            pass

    # --- S_HEALTH_THRASH: factory root stray without guard ---
    rel = "pipeline/health_checks.py"
    text, lines = _read(root, rel)
    if text:
        has_stray = "check_stray_files" in text or "Rescued loose file" in text
        has_guard = "_is_factory_code_root" in text
        if has_stray and not has_guard:
            add(
                severity="medium",
                title="S_HEALTH_THRASH proxy: stray rescue without factory-root guard",
                path=rel,
                evidence="stray/test rescue paths present; _is_factory_code_root not found",
                recommendation="Skip factory PROJECT_ROOT in check_stray_files / run_all_checks",
                tags=["S_HEALTH_THRASH", "runtime-control"],
            )

    # --- S_FALSE_MVP: f-string quantifier trap ---
    for rel in (
        "pipeline/project_phase.py",
        "pipeline/control_plane_invariants.py",
    ):
        text, lines = _read(root, rel)
        if not text:
            continue
        # Bad pattern: rf"...#{1,6}..." without double braces — in source file
        # we look for the mistaken form that f-string would break: #{1,6} as
        # single braces in an rf" string containing {next_phase} or similar.
        for i, L in enumerate(lines):
            if "rf\"" not in L and "rf'" not in L and 'rf"""' not in text:
                # multi-line rf strings: check line for #{1,6} not #{{1,6}}
                pass
            # Direct smell: #{1,6} without double brace (broken when inside f/rf with other {})
            if re.search(r"#\{1,\s*6\}", L) and "#{{1,6}}" not in L and "#{{1, 6}}" not in L:
                # only flag if line is an f/rf string that also has other {vars}
                if re.search(r'\b[fr]f?["\']', L) or (
                    i > 0 and re.search(r'\b[fr]f?["\']', lines[i - 1])
                ):
                    if "{next_phase}" in L or "{n}" in L or "phase_num" in "".join(lines[max(0, i - 3) : i + 1]):
                        add(
                            severity="high",
                            title="S_FALSE_MVP proxy: regex quantifier may be f-string-interpolated",
                            path=rel,
                            line=i + 1,
                            evidence=L.strip()[:200],
                            recommendation="Use #{{1,6}} inside rf-strings; prefer phase_heading_regex()",
                            tags=["S_FALSE_MVP", "runtime-control"],
                        )

        # project_phase should use control_plane_invariants for headings
        if rel == "pipeline/project_phase.py":
            if "def _advance_phase" in text and "phase_heading_present" not in text:
                if "control_plane_invariants" not in text:
                    add(
                        severity="medium",
                        title="S_FALSE_MVP proxy: _advance_phase without control_plane_invariants",
                        path=rel,
                        evidence="_advance_phase present; phase_heading_present/control_plane_invariants missing",
                        recommendation="Delegate heading match to pipeline.control_plane_invariants",
                        tags=["S_FALSE_MVP", "runtime-control"],
                    )

    # --- control_plane_invariants module exists and exports key API ---
    # Façade-aware: defs may live under pipeline/_control_plane_invariants/**
    # when monofile is a thin re-export (structure-only split).
    rel = "pipeline/control_plane_invariants.py"
    text, _ = _read(root, rel)
    if not text:
        add(
            severity="high",
            title="control_plane_invariants.py missing",
            path=rel,
            evidence="file not found",
            recommendation="Restore pipeline/control_plane_invariants.py",
            tags=["runtime-control"],
        )
    else:
        for name in (
            "phase_heading_present",
            "classic_roles_idle",
            "would_advance_to_next_phase",
            "write_stall_receipt",
        ):
            if not api_def_present(
                root, public_rel=rel, monofile_text=text, name=name
            ):
                add(
                    severity="medium",
                    title=f"control_plane_invariants missing def {name}",
                    path=rel,
                    evidence=(
                        f"def {name} not found in monofile or re-export package "
                        f"pipeline/_control_plane_invariants/"
                    ),
                    recommendation=(
                        f"Implement {name} on monofile or under "
                        f"pipeline/_control_plane_invariants/ and re-export"
                    ),
                    tags=["runtime-control"],
                )
        # Ensure quantifier helper is safe (scan package when façade re-exports)
        corpus = _package_corpus_text(root, rel, text)
        if "phase_heading_regex" in corpus and "#{{1,6}}" not in corpus and r"#\{1,6\}" not in corpus:
            # file should contain double-brace form in source
            if "1,6" in corpus and "{{1,6}}" not in corpus:
                add(
                    severity="high",
                    title="phase_heading_regex may lack safe {{1,6}} quantifier",
                    path=rel,
                    evidence="1,6 present without {{1,6}} (monofile+package)",
                    recommendation="Use rf'...#{{1,6}}...' in phase_heading_regex",
                    tags=["S_FALSE_MVP", "runtime-control"],
                )

    # --- soft_log NameError risk on hot files (soft_log_exc call, no import) ---
    for rel in HOT_FILES:
        text, lines = _read(root, rel)
        if not text or "soft_log_exc(" not in text:
            continue
        if re.search(
            r"from\s+pipeline\.soft_log\s+import\s+[^\n]*soft_log_exc", text
        ):
            continue
        if "control_plane_invariants" in rel:
            continue
        # allow import via soft_log in same module differently
        if "soft_log_exc" in text and "import soft_log" not in text:
            # project_phase uses soft_log_exc from star/constants sometimes
            if "from pipeline.soft_log import" in text:
                continue
            # only flag if clearly calling without any soft_log import line
            if not re.search(r"soft_log", text.split("soft_log_exc(")[0][-500:]):
                pass
            has_import = bool(
                re.search(r"import\s+.*soft_log|from\s+.*\s+import\s+.*soft_log", text)
            )
            if not has_import:
                ln = next(
                    (i + 1 for i, L in enumerate(lines) if "soft_log_exc(" in L),
                    None,
                )
                add(
                    severity="medium",
                    title="S_SOFT_LOG proxy: soft_log_exc used without soft_log import",
                    path=rel,
                    line=ln,
                    evidence="soft_log_exc( call(s) without pipeline.soft_log import",
                    recommendation="from pipeline.soft_log import soft_log_exc",
                    tags=["S_SOFT_LOG", "runtime-control"],
                )

    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="qc-runtime-control leaf")
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument(
        "--out",
        type=Path,
        default=None,
        help="findings.json path (file)",
    )
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (
        root / "notes" / "qc" / "_samples" / "runtime-control" / "findings.json"
    )

    findings = scan_repo(root)
    if not findings:
        findings.append(
            _finding(
                "rtc-pass-001",
                "info",
                "No runtime-control stall proxies hit (pass_summary)",
                evidence=f"scanned {len(HOT_FILES)} hot files under {root}",
                tags=["pass_summary", "runtime-control"],
                recommendation="None",
            )
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        summary[str(f.get("severity", "info"))] = (
            summary.get(str(f.get("severity", "info")), 0) + 1
        )

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": CONTROL,
        "profile": "leaf",
        "scope": {
            "paths": list(HOT_FILES),
            "note": str(root),
            "stall_classes": [
                "S_DEAD_ROLE",
                "S_HEALTH_THRASH",
                "S_FALSE_MVP",
                "S_SOFT_LOG",
            ],
        },
        "commands_run": [
            {"cmd": f"qc-runtime-control scan root={root}", "exit_code": 0}
        ],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "static proxy ≠ multi-hour overnight soak",
            "clean leaf ≠ product dual-gate",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
