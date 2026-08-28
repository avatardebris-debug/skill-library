#!/usr/bin/env python3
"""qc-honesty leaf: scan honesty anti-patterns → factory_qc_findings.v0."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# (rule_id, severity, compiled regex, title, recommendation)
PATTERNS: list[tuple[str, str, re.Pattern[str], str, str]] = [
    (
        "H01_field_proven_true",
        "high",
        re.compile(r"\bfield_proven\s*=\s*True\b"),
        "field_proven=True assignment",
        "Never assign field_proven=True outside dual-gate promote path",
    ),
    (
        "H02_field_proven_true_json",
        "high",
        re.compile(r"""["']field_proven["']\s*:\s*True\b"""),
        "field_proven: True in dict/JSON stamp",
        "Keep field_proven false/None; scrub on write",
    ),
    (
        "H03_goal_proven_human_auto",
        "high",
        re.compile(r"\bgoal_proven_human\s*=\s*True\b"),
        "goal_proven_human=True without human gate",
        "Only set via apply_human_verdict accept path",
    ),
    (
        "H04_provisional_as_human",
        "medium",
        re.compile(r"""status\s*=\s*["']goal_proven_human["']"""),
        "status assigned goal_proven_human directly",
        "Use provisional until human verdict",
    ),
    (
        "H05_auto_lfg",
        "high",
        re.compile(r"\bauto[_-]?lfg\b|\bauto_run_lfg\b|\brun_lfg_automatically\b", re.I),
        "auto-LFG / automatic LFG execute language",
        "Soft handoff prompt only; never auto-LFG",
    ),
    (
        "H06_accept_equals_execute",
        "medium",
        re.compile(r"accept\s*==\s*execute|accept_means_execute|\bauto_apply\s*=\s*True\b", re.I),
        "accept equated to execute / auto_apply=True",
        "Meta accept ≠ execute",
    ),
    (
        "H07_auto_promote",
        "high",
        re.compile(r"\bauto[_-]?promote\s*=\s*True\b|\bauto_promote\s*\(", re.I),
        "auto_promote enabled or called",
        "Human promote only",
    ),
    (
        "H08_pack_rewrite",
        "high",
        re.compile(
            r"process_packs.*(write|overwrite|rewrite)|(write|overwrite|rewrite).*process_packs",
            re.I,
        ),
        "process_packs write/rewrite smell",
        "Refuse pack rewrite; research store only",
    ),
    (
        "H09_constitution_write",
        "high",
        re.compile(r"constitution\.yaml[^\n]{0,40}['\"]w|open\([^\)]*constitution\.yaml[^\)]*['\"]w"),
        "constitution.yaml opened for write",
        "Constitution is read-only for factory modules",
    ),
    (
        "H10_outer_rsi_unlock",
        "medium",
        re.compile(r"outer_rsi\s*=\s*True|unlock[_\s-]*outer[_\s-]?rsi|outer_rsi_unlock\s*=\s*True", re.I),
        "outer RSI unlock stamp",
        "Outer RSI remains deferred non-goal",
    ),
    (
        "H11_complete_as_field",
        "medium",
        re.compile(r"field_proven\s*=\s*.*complete|complete.*\bfield_proven\s*=\s*True", re.I),
        "complete collapsed into field_proven assignment",
        "complete_gate must not set field_proven",
    ),
    (
        "H13_machine_success_as_field",
        "medium",
        re.compile(
            r"field_proven\s*=\s*machine_success\b"
            r"|goal_proven_human\s*=\s*machine_success\b"
            r"|if\s+machine_success.{0,60}field_proven\s*=\s*True",
            re.I,
        ),
        "machine_success collapsed into field_proven / goal_proven_human",
        "Goal suite greens are not product field_proven",
    ),
]

ALLOW_RE = re.compile(
    r"(?i)(≠|non[-_ ]?claim|non_claims|does not claim|must not|never\b|honesty:|"
    r"not\s+field_proven|not\s+goal_proven|soft\s+handoff|report-only|"
    r"honesty-fixture-good|"
    # ban language: "no auto-LFG" / markdown "**no** auto_lfg"
    r"(?:\*+\s*)?\bno\s*(?:\*+\s*)?auto[_-]?lfg\b|"
    r"(?:\*+\s*)?\bnot\s*(?:\*+\s*)?auto[_-]?lfg\b)"
)

# H05: True / execute stamps must never be line- or match-skipped by allowlists.
H05_TRUE_STAMP_RE = re.compile(
    r"(?i)("
    r"\bauto[_-]?lfg\s*=\s*True\b|"
    r"""["']auto[_-]?lfg["']\s*:\s*True\b|"""
    r"""\[["']auto[_-]?lfg["']\]\s*=\s*True\b|"""
    r"\bauto_run_lfg\b|"
    r"\brun_lfg_automatically\b"
    r")"
)

# H05: ban stamps, False flags, ban-list membership, and does_not_claim footers
# are soft-handoff honesty, not execute.
H05_BAN_RE = re.compile(
    r"(?i)("
    # False stamps: auto_lfg: False / "auto_lfg": False / auto_lfg = False
    # Markdown honesty tables: auto_lfg: **false** / auto_lfg: **False**
    # Quoted string false (JSON-ish soft seed): "auto_lfg": "false" / 'false'
    # (quoted arm has no trailing \b — quote then comma is not a word boundary)
    r"""auto[_-]?lfg\s*[\"']?\s*[:=]\s*(?:\*+\s*)?(?:False\b|["']false["'])(?:\s*\*+)?|"""
    # bare note-string deny: "auto_lfg false" / auto_lfg false (not True)
    r"""["']?auto[_-]?lfg\s+false["']?\b|"""
    # subscript False: row["auto_lfg"] = False
    r"""\[["']auto[_-]?lfg["']\]\s*=\s*False\b|"""
    # ban prose: no / not / never auto_lfg; optional markdown bold around ban word
    # (**no** auto_lfg / **not** auto-LFG) — never matches True stamps
    r"(?:\*+\s*)?\b(?:no|not|never)\b(?:\s*\*+)?\s+auto[_-]?lfg\b|"
    r"\(\s*no\s+auto[_-]?lfg\s*\)|"
    # string list membership without True: "auto_lfg",  'auto_lfg']  "auto_lfg")
    r"""["']auto[_-]?lfg["']\s*[,\]\)]|"""
    # does_not_claim / DOES_NOT_CLAIM / does not claim / non_claims near auto_lfg
    # (markdown bold allowed: Does **not** claim)
    r"(?:does_not_claim|non_claims|"
    r"does\s*(?:\*+\s*)?not\s*(?:\*+\s*)?claim)"
    r".{0,100}auto[_-]?lfg|"
    r"auto[_-]?lfg.{0,100}"
    r"(?:does_not_claim|non_claims|"
    r"does\s*(?:\*+\s*)?not\s*(?:\*+\s*)?claim)|"
    # ban-before prose: do/does not ... auto_lfg (docstrings, not True assign)
    # also: "never sets ... auto_lfg" (same line after rejoin / inventory)
    r"\b(?:do(?:es)?\s*(?:\*+\s*)?not|don't|dont|never|must\s+not)\b"
    r".{0,100}auto[_-]?lfg|"
    r"\bnever\s+sets\b.{0,120}auto[_-]?lfg|"
    # bare ban inventory lines listing crown non-claims (doc "Does not claim" body)
    r"(?:field_proven|goal_proven_human|true_user_intent).{0,80}auto[_-]?lfg|"
    r"auto[_-]?lfg.{0,80}(?:field_proven|goal_proven_human|true_user_intent)|"
    # Non-claims multi-token inventory: invent_human_verdict · auto_lfg · public_agi
    # (mid-bullet bare auto_lfg between middle-dot / bullet separators)
    r"(?:invent_human_verdict|public_agi).{0,80}auto[_-]?lfg|"
    r"auto[_-]?lfg.{0,80}(?:invent_human_verdict|public_agi)|"
    r"[·•]\s*auto[_-]?lfg\s*[·•]"
    r")"
)

# H07: True promote execute stamps must never be line- or match-skipped.
# Unquoted assignment or call only — quoted ban-list strings are not True stamps.
H07_TRUE_STAMP_RE = re.compile(
    r"(?i)("
    # auto_promote = True / auto-promote=True without surrounding quotes on the token
    r"""(?<![\"'])\bauto[_-]?promote\s*=\s*True\b(?![\"'])|"""
    # live call: auto_promote(
    r"\bauto_promote\s*\("
    r")"
)

# H07: forbidden/deny-doc strings listing auto_promote=True ≠ live promote execute.
H07_BAN_RE = re.compile(
    r"(?i)("
    # Quoted ban-list membership: "auto_promote=True" / 'auto_promote=True'
    # (forbidden: [...] inventories; not bare assignment)
    r"""["']auto[_-]?promote\s*=\s*True["']|"""
    # ban prose: no / not / never auto_promote (optional markdown bold around ban word)
    r"(?:\*+\s*)?\b(?:no|not|never)\b(?:\s*\*+)?\s+auto[_-]?promote\b|"
    # does_not_claim / non_claims / does not claim near auto_promote
    r"(?:does_not_claim|non_claims|"
    r"does\s*(?:\*+\s*)?not\s*(?:\*+\s*)?claim)"
    r".{0,100}auto[_-]?promote|"
    r"auto[_-]?promote.{0,100}"
    r"(?:does_not_claim|non_claims|"
    r"does\s*(?:\*+\s*)?not\s*(?:\*+\s*)?claim)|"
    # ban-before prose: do/does not ... auto_promote (docstrings)
    r"\b(?:do(?:es)?\s*(?:\*+\s*)?not|don't|dont|never|must\s+not)\b"
    r".{0,100}auto[_-]?promote"
    r")"
)

# H10: ban/doc language about outer RSI (False stamps, "do not unlock") ≠ unlock.
# Ban words must appear *before* the unlock phrase (no trailing deferred/never arm —
# that would silence `unlock_outer_rsi = True  # deferred`). Bare `\bno\b` omitted
# (too broad vs H05 phrase-level "no auto-LFG").
H10_BAN_RE = re.compile(
    r"(?i)("
    # False / locked stamps: outer_rsi=False, outer_rsi_unlocked: False
    r"outer_rsi(?:_unlock(?:ed)?)?\s*[\"']?\s*[:=]\s*False\b|"
    # Honesty keys: not_outer_rsi, not_outer_rsi_unlock
    r"\bnot[_-]?outer[_-]?rsi(?:[_-]?unlock(?:ed)?)?\b|"
    # Ban prose: do not / does not / never / must not *before* unlock outer RSI
    # Markdown bold allowed between ban words: Does **not** … unlock outer RSI
    # (mirrors H05 ban-before `\*+` allowance)
    r"\b(?:do(?:es)?\s*(?:\*+\s*)?not|don't|dont|never|must\s+not)\b"
    r"[^.\n]{0,60}unlock[_\s-]*outer[_\s-]?rsi|"
    r"\bblock(?:s|ed|ing)?\s+(?:outer\s+)?rsi\b"
    r")"
)

# True unlock/assignment stamps must never be line- or match-skipped by allowlists.
H10_TRUE_STAMP_RE = re.compile(
    r"(?i)("
    r"\bouter_rsi(?:_unlock)?\s*=\s*True\b|"
    r"\bunlock[_\s-]*outer[_\s-]?rsi\s*=\s*True\b|"
    r"""["']outer_rsi(?:_unlock(?:ed)?)?["']\s*:\s*True\b"""
    r")"
)

# H08: refuse guards mention write+process_packs without performing write
H08_REFUSE_RE = re.compile(
    r"(?i)("
    r"refus(?:e|ing)\s+write\b|"
    r"refuse[sd]?\s+.*process_packs|"
    r"never\s+write\s+.*process_packs|"
    r"raise\s+ValueError\s*\([^)]*process_packs"
    r")"
)

# H01 dual-gate promote path lives only in field_prove_gate.py (two assigns)
H01_ALLOW_PATH_SUFFIXES = (
    "pipeline/field_prove_gate.py",
    "pipeline\\field_prove_gate.py",
)

SKIP_DIR_NAMES = {
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "_archive",
    ".pytest_cache",
}


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _should_skip_line(line: str) -> bool:
    # Real True unlock / auto-LFG / auto_promote execute stamps must not be
    # silenced by ALLOW_RE (e.g. trailing "# never ..." comments).
    if H10_TRUE_STAMP_RE.search(line):
        return False
    if H05_TRUE_STAMP_RE.search(line):
        return False
    if H07_TRUE_STAMP_RE.search(line):
        return False
    if ALLOW_RE.search(line):
        return True
    stripped = line.lstrip()
    if stripped.startswith("#") and any(
        k in stripped.lower()
        for k in ("honesty", "non-claim", "field_proven", "≠", "never", "auto-lfg", "auto_lfg")
    ):
        # comment documenting ban — skip pure comments
        return True
    return False


def _should_skip_match(rule_id: str, line: str, rel: str) -> bool:
    """Rule-aware allowlists for dual-gate / soft-handoff / refuse-list FPs."""
    rel_norm = rel.replace("\\", "/")
    if rule_id == "H05_auto_lfg":
        # True / execute stamps always flag (even if ban words also on line).
        if H05_TRUE_STAMP_RE.search(line):
            return False
        if H05_BAN_RE.search(line):
            return True
    if rule_id == "H07_auto_promote":
        # True assign / live call always flag (even if ban words also on line).
        if H07_TRUE_STAMP_RE.search(line):
            return False
        if H07_BAN_RE.search(line):
            return True
    if rule_id == "H10_outer_rsi_unlock":
        # True assignment/unlock stamps always flag (even if ban words also on line).
        if H10_TRUE_STAMP_RE.search(line):
            return False
        if H10_BAN_RE.search(line):
            return True
    if rule_id == "H08_pack_rewrite" and H08_REFUSE_RE.search(line):
        return True
    if rule_id == "H01_field_proven_true":
        # Only the dual-gate / legacy promote module may assign True
        if rel_norm.endswith("pipeline/field_prove_gate.py") or rel_norm == "pipeline/field_prove_gate.py":
            return True
        if any(rel_norm.endswith(s.replace("\\", "/")) for s in H01_ALLOW_PATH_SUFFIXES):
            return True
    return False


def scan_file(path: Path, rel: str) -> list[dict]:
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return findings
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _should_skip_line(line):
            continue
        for rule_id, severity, cre, title, rec in PATTERNS:
            if not cre.search(line):
                continue
            if _should_skip_match(rule_id, line, rel):
                continue
            findings.append(
                {
                    "id": f"honesty-{rule_id}-{rel.replace('/', '-')}-{lineno}",
                    "severity": severity,
                    "control": "qc-honesty",
                    "title": title,
                    "evidence": f"{rel}:{lineno}: {line.strip()[:200]}",
                    "paths": [rel.replace("\\", "/")],
                    "effort": "M" if severity == "high" else "S",
                    "rule": rule_id,
                    "line": lineno,
                    "recommendation": rec,
                    "tags": ["honesty"],
                    "tool": "qc-honesty",
                }
            )
    return findings


def iter_py_files(root: Path, paths: list[str]) -> list[Path]:
    files: list[Path] = []
    bases = [root / p for p in paths] if paths else [root / "pipeline"]
    for base in bases:
        if base.is_file() and base.suffix == ".py":
            files.append(base)
            continue
        if not base.is_dir():
            continue
        for p in base.rglob("*.py"):
            if any(part in SKIP_DIR_NAMES for part in p.parts):
                continue
            files.append(p)
    return files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", type=Path, default=Path.cwd())
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--path", action="append", dest="paths", default=[])
    ap.add_argument(
        "--fixture-mode",
        action="store_true",
        help="Scan only skill fixtures (for smoke tests)",
    )
    args = ap.parse_args(argv)
    root = args.repo_root.resolve()
    out = args.out or (root / "notes" / "qc" / "_samples" / "honesty" / "findings.json")

    if args.fixture_mode:
        fix_dir = root / ".grok" / "skills" / "qc-honesty" / "fixtures"
        scan_paths = [str(fix_dir.relative_to(root))] if fix_dir.is_dir() else []
        files = list(fix_dir.glob("*.py")) if fix_dir.is_dir() else []
    else:
        scan_paths = list(args.paths or ["pipeline"])
        files = iter_py_files(root, scan_paths)

    findings: list[dict] = []
    for fp in files:
        try:
            rel = str(fp.relative_to(root)).replace("\\", "/")
        except ValueError:
            rel = str(fp)
        findings.extend(scan_file(fp, rel))

    # Cap explosion on large trees
    max_findings = 200
    truncated = False
    if len(findings) > max_findings:
        findings = findings[:max_findings]
        truncated = True

    if not findings:
        findings.append(
            {
                "id": "honesty-pass-001",
                "severity": "info",
                "control": "qc-honesty",
                "title": "No honesty anti-pattern hits in scope (pass_summary)",
                "evidence": f"scanned {len(files)} files under {scan_paths}",
                "paths": scan_paths,
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "None",
                "tool": "qc-honesty",
            }
        )
    elif truncated:
        findings.append(
            {
                "id": "honesty-truncated-001",
                "severity": "info",
                "control": "qc-honesty",
                "title": f"Findings truncated to {max_findings}",
                "evidence": "max_findings cap",
                "paths": [],
                "effort": "S",
                "tags": ["pass_summary"],
                "recommendation": "Narrow --path scope",
                "tool": "qc-honesty",
            }
        )

    summary = {s: 0 for s in ("critical", "high", "medium", "low", "info")}
    for f in findings:
        k = str(f.get("severity", "info"))
        summary[k] = summary.get(k, 0) + 1

    envelope = {
        "schema": "factory_qc_findings.v0",
        "generated_at": _iso(),
        "control": "qc-honesty",
        "profile": "leaf",
        "scope": {"paths": scan_paths, "note": str(root), "files_scanned": len(files)},
        "commands_run": [
            {
                "cmd": f"qc-honesty scan files={len(files)} fixture_mode={args.fixture_mode}",
                "exit_code": 0,
            }
        ],
        "summary": summary,
        "findings": findings,
        "non_claims": [
            "factory health ≠ field_proven",
            "factory health ≠ goal_proven_human",
            "scanner residual ≠ dual-gate production proof",
            "not auto_lfg",
        ],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} findings={len(findings)} summary={summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
