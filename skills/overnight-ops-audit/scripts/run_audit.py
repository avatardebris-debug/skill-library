#!/usr/bin/env python3
"""overnight-ops-audit: receipt-first parse of logs/overnight_* dirs.

Measure-only. Never mutates projects. Never auto-LFG.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from collections import Counter
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = "overnight_ops_audit.v0"
CLASSIC_ROLES = frozenset(
    {
        "idea_planner",
        "phase_planner",
        "executor",
        "validator",
        "reviewer",
        "manager",
        "ideator",
    }
)

STALL_RE = re.compile(r"STALL DETECTED:\s*(.+)", re.I)
HEALTH_RE = re.compile(
    r"Health check:\s*(\d+)\s*auto-fixed(?:,\s*(\d+)\s*reported)?", re.I
)
SEEDED_RE = re.compile(r"Seeded idea:\s*(.+)", re.I)
REQUEUE_RE = re.compile(r"Re-queued\s+'([^']+)'", re.I)
ADVANCE_RE = re.compile(r"phase\s+(\d+)\s+passed", re.I)
COMPLETE_RE = re.compile(
    r"(complete_with_bugs|completed all phases|mvp_complete|mvp complete)", re.I
)
MVP_RE = re.compile(r"MVP complete\s*\(phase\s*(\d+)/(\d+)\)", re.I)
FALLBACK_RE = re.compile(r"engine_fallback|\[grok_build\].*error", re.I)
WINGET_RE = re.compile(r"winget|Graphviz|choco\s+install|scoop\s+install", re.I)
SOFT_LOG_RE = re.compile(r"soft_log_exc|NameError:\s*name 'soft_log", re.I)
BLOCKED_RE = re.compile(r"\[blocked\].*", re.I)
EXIT_RE = re.compile(r"end\s+(\S+)\s+exit=(\S+)", re.I)
START_RE = re.compile(r"start\s+(\S+)", re.I)
# agent logs: Completed message … (success=…, tokens=N, steps=N)
AGENT_DONE_RE = re.compile(
    r"Completed message\s+\S+\s+\(success=(\w+),\s*tokens=(\d+)",
    re.I,
)


@dataclass
class Finding:
    severity: str  # critical|high|medium|low|info
    cls: str
    message: str
    evidence: str = ""
    recommendation: str = ""


@dataclass
class OvernightAudit:
    overnight_dir: str
    generated_at: str
    preflight: dict[str, Any] = field(default_factory=dict)
    runner: dict[str, Any] = field(default_factory=dict)
    health_auto_fixed: list[int] = field(default_factory=list)
    stalls: list[str] = field(default_factory=list)
    seeds: list[str] = field(default_factory=list)
    transitions: list[str] = field(default_factory=list)
    dead_role_pending: dict[str, int] = field(default_factory=dict)
    agent_tokens: dict[str, int] = field(default_factory=dict)
    agent_completes: dict[str, int] = field(default_factory=dict)
    mvp_complete_count: int = 0
    false_mvp_slugs: list[str] = field(default_factory=list)
    reseed_soak: dict[str, Any] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    non_claims: list[str] = field(
        default_factory=lambda: [
            "audit report ≠ field_proven",
            "measure-only — does not fix runner",
            "truth_density tokens may undercount agent logs",
            "reseed soak receipt ≠ overnight field_proven",
        ]
    )

    def summary(self) -> dict[str, int]:
        s = {k: 0 for k in ("critical", "high", "medium", "low", "info")}
        for f in self.findings:
            s[f.severity] = s.get(f.severity, 0) + 1
        return s


def _iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    raw = path.read_bytes()
    if len(raw) >= 2 and raw[1] == 0 and raw[0] != 0:
        try:
            return raw.decode("utf-16-le")
        except UnicodeDecodeError:
            pass
    if raw.startswith(b"\xff\xfe"):
        return raw.decode("utf-16-le")
    if raw.startswith(b"\xfe\xff"):
        return raw.decode("utf-16-be")
    for enc in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return json.loads(_read_text(path))
    except json.JSONDecodeError:
        return {}


def _default_pipeline_dir() -> Path:
    import os

    env = os.environ.get("PIPELINE_DIR", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    home = Path.home() / "aicompete" / "thepipeline"
    if home.is_dir():
        return home
    return Path.cwd()


def list_overnight_dirs(logs: Path, latest: int | None = None) -> list[Path]:
    if not logs.is_dir():
        return []
    dirs = sorted(
        [p for p in logs.iterdir() if p.is_dir() and p.name.startswith("overnight_")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if latest is not None:
        dirs = dirs[: max(0, latest)]
    return dirs


def _audit_dead_role_bus(pipeline_dir: Path) -> dict[str, int]:
    db = pipeline_dir / "state" / "message_bus.db"
    if not db.is_file():
        return {}
    out: dict[str, int] = {}
    try:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
        rows = conn.execute(
            """
            SELECT to_agent, COUNT(*) FROM messages
            WHERE status IN ('pending', 'processing')
            GROUP BY to_agent
            """
        ).fetchall()
        conn.close()
        for agent, n in rows:
            if agent and agent not in CLASSIC_ROLES and n:
                out[str(agent)] = int(n)
    except Exception:
        return {}
    return out


def audit_overnight(overnight_dir: Path, pipeline_dir: Path | None = None) -> OvernightAudit:
    od = Path(overnight_dir)
    pipe = Path(pipeline_dir) if pipeline_dir else od.parent.parent
    audit = OvernightAudit(overnight_dir=str(od), generated_at=_iso())
    audit.preflight = _load_json(od / "preflight.json")

    rlog = _read_text(od / "runner.log")
    rout = _read_text(od / "runner.out.log")
    rerr = _read_text(od / "runner.err.log")

    start_m = START_RE.search(rlog)
    end_m = EXIT_RE.search(rlog)
    audit.runner = {
        "start": start_m.group(1) if start_m else None,
        "end": end_m.group(1) if end_m else None,
        "exit": end_m.group(2) if end_m else None,
        "has_end_line": bool(end_m),
        "err_bytes": (od / "runner.err.log").stat().st_size
        if (od / "runner.err.log").is_file()
        else 0,
        "out_chars": len(rout),
    }

    if not end_m and rlog.strip():
        audit.findings.append(
            Finding(
                "high",
                "exit",
                "runner.log missing clean end/exit line (incomplete/crash/kill)",
                evidence="runner.log",
                recommendation="Recover truth-density; restart overnight on fixed code if mid-fix",
            )
        )
    elif end_m and end_m.group(2) not in ("0", "null"):
        audit.findings.append(
            Finding(
                "medium",
                "exit",
                f"runner exit={end_m.group(2)}",
                evidence=end_m.group(0)[:120],
                recommendation="Inspect runner.err and last STALL/complete lines",
            )
        )

    for m in STALL_RE.finditer(rout):
        audit.stalls.append(m.group(0).strip()[:200])
    if audit.stalls:
        audit.findings.append(
            Finding(
                "high" if len(audit.stalls) >= 2 else "medium",
                "stall",
                f"{len(audit.stalls)} stall event(s) in runner.out",
                evidence="; ".join(audit.stalls[:3]),
                recommendation="Check dead-role bus, phase_reviewed advance, last LLM age",
            )
        )

    for m in HEALTH_RE.finditer(rout):
        audit.health_auto_fixed.append(int(m.group(1)))
    if audit.health_auto_fixed:
        mx = max(audit.health_auto_fixed)
        counts = Counter(audit.health_auto_fixed)
        thrash = mx >= 50 or any(n >= 50 and c >= 2 for n, c in counts.items())
        repeated = any(c >= 3 and n >= 20 for n, c in counts.items())
        if thrash or repeated:
            audit.findings.append(
                Finding(
                    "high",
                    "auto_fix_thrash",
                    f"Health auto_fix thrash: max={mx} series={audit.health_auto_fixed[:8]}",
                    evidence=f"counts={dict(counts)}",
                    recommendation="factory-root stray skip / idempotent health fixes",
                )
            )
        elif mx > 0:
            audit.findings.append(
                Finding(
                    "info",
                    "auto_fix",
                    f"Health auto-fixed max={mx} (not thrash-scale)",
                    evidence=str(audit.health_auto_fixed[:10]),
                )
            )

    if SOFT_LOG_RE.search(rerr) or SOFT_LOG_RE.search(rout):
        audit.findings.append(
            Finding(
                "critical",
                "soft_log_crash",
                "soft_log_exc NameError or soft_log crash signature in logs",
                evidence=(rerr or rout)[:300],
                recommendation="Import soft_log_exc on all call sites; restart runner process",
            )
        )
    elif "Traceback" in rerr:
        audit.findings.append(
            Finding(
                "high",
                "traceback",
                "Traceback present in runner.err",
                evidence=rerr[-500:],
                recommendation="Read runner.err full stack",
            )
        )

    if WINGET_RE.search(rout) or WINGET_RE.search(rerr):
        audit.findings.append(
            Finding(
                "high",
                "side_effect",
                "Implement/OS package side-effect keywords (winget/Graphviz/choco)",
                evidence="runner.out/err match",
                recommendation="Deny unattended winget in implement; DOT-only for graph tools",
            )
        )

    for m in SEEDED_RE.finditer(rout):
        audit.seeds.append(m.group(1).strip()[:120])
    for m in REQUEUE_RE.finditer(rout):
        audit.transitions.append(f"requeue:{m.group(1)}")
    for m in ADVANCE_RE.finditer(rout):
        audit.transitions.append(f"advance_phase:{m.group(1)}")
    for m in COMPLETE_RE.finditer(rout):
        audit.transitions.append(m.group(0).strip()[:80])
    for m in BLOCKED_RE.finditer(rout):
        audit.transitions.append(m.group(0).strip()[:100])
    audit.mvp_complete_count = len(MVP_RE.findall(rout))
    if audit.mvp_complete_count >= 5:
        advances = sum(1 for t in audit.transitions if t.startswith("advance_phase:"))
        audit.findings.append(
            Finding(
                "high" if audit.mvp_complete_count >= 10 else "medium",
                "mass_mvp",
                f"{audit.mvp_complete_count} MVP complete line(s) in runner.out "
                f"(phase advances logged≈{advances})",
                evidence="mvp_complete early-exit pattern; check phase-heading advance",
                recommendation=(
                    "If p1/N with ## Phase 2 in plan: control_plane_invariants + "
                    "scripts/revive_false_mvp.py --apply"
                ),
            )
        )

    if FALLBACK_RE.search(rout):
        audit.findings.append(
            Finding(
                "medium",
                "engine_fallback",
                "grok_build error or engine_fallback mentioned",
                recommendation="Check engine_fallback_reason on project state",
            )
        )

    # Agent log token rollup (sibling logs/*.log) — prefer overnight date window
    logs_dir = od.parent
    # overnight dir name overnight_YYYYMMDD_HHMMSS → date filter YYYY-MM-DD
    date_prefix = ""
    m_name = re.match(r"overnight_(\d{4})(\d{2})(\d{2})_", od.name)
    if m_name:
        date_prefix = f"{m_name.group(1)}-{m_name.group(2)}-{m_name.group(3)}"
    for role in sorted(CLASSIC_ROLES):
        logp = logs_dir / f"{role}.log"
        if not logp.is_file():
            continue
        try:
            raw = logp.read_bytes()
            if len(raw) > 6_000_000:
                raw = raw[-6_000_000:]
            text = raw.decode("utf-8", errors="replace")
        except OSError:
            continue
        tok = 0
        n_done = 0
        for line in text.splitlines():
            if date_prefix and date_prefix not in line:
                continue
            m = AGENT_DONE_RE.search(line)
            if not m:
                continue
            n_done += 1
            tok += int(m.group(2))
        if n_done or tok:
            audit.agent_tokens[role] = tok
            audit.agent_completes[role] = n_done
    if audit.agent_tokens:
        total_tok = sum(audit.agent_tokens.values())
        audit.findings.append(
            Finding(
                "info",
                "agent_tokens",
                f"Agent log token sum≈{total_tok} "
                f"(window={date_prefix or 'all'}; by role: "
                f"{dict(list(audit.agent_tokens.items())[:6])})",
                evidence="Completed message tokens= from logs/*.log filtered by overnight date",
                recommendation="Prefer this over truth_density 0 when agents worked",
            )
        )

    # False MVP scan on pipeline projects (current disk state)
    try:
        sys_path_root = Path(__file__).resolve().parents[4]
        # .../idea-impl2/.grok/skills/overnight-ops-audit/scripts -> parents[4]=idea-impl2
        import sys

        if str(sys_path_root) not in sys.path:
            sys.path.insert(0, str(sys_path_root))
        from pipeline.control_plane_invariants import list_false_mvp_projects

        fm = list_false_mvp_projects(pipe / "projects")
        audit.false_mvp_slugs = [x["slug"] for x in fm[:40]]
        if fm:
            audit.findings.append(
                Finding(
                    "high",
                    "false_mvp_disk",
                    f"{len(fm)} project(s) currently false mvp_complete "
                    f"(next phase still available): {', '.join(audit.false_mvp_slugs[:8])}"
                    + ("…" if len(fm) > 8 else ""),
                    evidence="classify_false_mvp_risk on projects/*/state",
                    recommendation="python scripts/revive_false_mvp.py --pipeline-dir … --apply",
                )
            )
    except Exception:
        pass

    # Optional project grok_implement side-effect scan (touched in morning_rows)
    morning = _load_json(od / "morning_rows.json")
    seen_side: set[str] = set()
    if isinstance(morning, list):
        for row in morning[:20]:
            slug = (row or {}).get("slug") or ""
            if not slug:
                continue
            impl = pipe / "projects" / slug / "phases"
            if not impl.is_dir():
                continue
            for logf in impl.rglob("grok_implement.log"):
                text = _read_text(logf)
                if not WINGET_RE.search(text):
                    continue
                key = f"{slug}:{logf.name}"
                if key in seen_side:
                    continue
                seen_side.add(key)
                audit.findings.append(
                    Finding(
                        "high",
                        "side_effect",
                        f"winget/Graphviz/choco in {slug} grok_implement.log",
                        evidence=str(logf.relative_to(pipe))
                        if pipe in logf.parents
                        else str(logf),
                        recommendation="Policy: no unattended OS package install",
                    )
                )

    dead = _audit_dead_role_bus(pipe)
    audit.dead_role_pending = dead
    if dead:
        audit.findings.append(
            Finding(
                "medium",
                "dead_role_bus",
                f"Pending/processing on non-classic roles: {dead}",
                evidence="message_bus.db",
                recommendation="Ignore for advance (AGENT_ROLES only) or age-out dead-role msgs",
            )
        )

    # Optional durable stall receipts from run_loop_health
    receipt = pipe / "state" / "stall_receipts.json"
    if receipt.is_file():
        try:
            doc = json.loads(_read_text(receipt))
            n_ev = len(doc.get("events") or [])
            if n_ev:
                last = (doc.get("events") or [])[-1]
                audit.findings.append(
                    Finding(
                        "info",
                        "stall_receipt",
                        f"{n_ev} stall receipt event(s); last={last.get('stall_class')}: {str(last.get('message'))[:80]}",
                        evidence=str(receipt),
                        recommendation="See pipeline state/stall_receipts.json for stall_class history",
                    )
                )
        except Exception:
            pass

    # Reseed soak: [reseed] after post-complete / empty-queue (measure-only)
    try:
        sys_path_root = Path(__file__).resolve().parents[4]
        import sys

        if str(sys_path_root) not in sys.path:
            sys.path.insert(0, str(sys_path_root))
        from pipeline.reseed_soak_receipt import receipt_from_text

        reseed_r = receipt_from_text(rout, source=str(od / "runner.out.log"))
        audit.reseed_soak = {
            "soak_status": reseed_r.soak_status,
            "counts": reseed_r.counts,
            "observed_seeded_post_complete": reseed_r.observed_seeded_post_complete,
            "observed_seeded_empty_queue": reseed_r.observed_seeded_empty_queue,
            "observed_no_slots": reseed_r.observed_no_slots,
            "observed_any_reseed": reseed_r.observed_any_reseed,
        }
        if reseed_r.observed_any_reseed:
            audit.findings.append(
                Finding(
                    "info",
                    "reseed_soak",
                    f"reseed soak_status={reseed_r.soak_status} "
                    f"events={reseed_r.counts.get('events', 0)} "
                    f"post_complete={reseed_r.observed_seeded_post_complete} "
                    f"empty_queue={reseed_r.observed_seeded_empty_queue} "
                    f"no_slots={reseed_r.observed_no_slots}",
                    evidence="runner.out.log [reseed] lines",
                    recommendation=(
                        "python -m pipeline.reseed_soak_receipt --overnight-dir "
                        + str(od)
                    ),
                )
            )
        else:
            audit.findings.append(
                Finding(
                    "info",
                    "reseed_soak",
                    "no [reseed] lines in runner.out (soak_status=no_reseed_lines) "
                    "— not a soak pass; classic Seeded idea may still appear",
                    evidence="runner.out.log",
                    recommendation=(
                        "If post-complete reseed was expected: confirm live runner "
                        "has run_loop_seed_idle reseed prints; re-run overnight"
                    ),
                )
            )
    except Exception as exc:
        audit.findings.append(
            Finding(
                "low",
                "reseed_soak",
                f"reseed soak parse skipped: {exc}",
                evidence="pipeline.reseed_soak_receipt",
            )
        )

    if not audit.findings:
        audit.findings.append(
            Finding(
                "info",
                "clean",
                "No high-signal stall/thrash/crash patterns matched",
                recommendation="Still skim MORNING.md for product quality",
            )
        )

    return audit


def format_markdown(audits: list[OvernightAudit]) -> str:
    lines = [
        f"# Overnight ops audit",
        f"",
        f"- Schema: `{SCHEMA}`",
        f"- Generated: `{_iso()}`",
        f"- Runs: **{len(audits)}**",
        f"",
    ]
    for a in audits:
        lines.append(f"## `{Path(a.overnight_dir).name}`")
        lines.append("")
        lines.append(f"- Path: `{a.overnight_dir}`")
        lines.append(f"- Exit: `{a.runner.get('exit')}` · end_line={a.runner.get('has_end_line')}")
        tl = a.preflight.get("time_limit_min")
        if tl is not None:
            lines.append(f"- time_limit_min: {tl}")
        lines.append(f"- Stalls: {len(a.stalls)} · health auto_fixed series: {a.health_auto_fixed[:12]}")
        lines.append(f"- Seeds: {len(a.seeds)} (show {a.seeds[:5]})")
        lines.append(f"- MVP complete lines: {a.mvp_complete_count}")
        if a.reseed_soak:
            lines.append(
                f"- Reseed soak: **`{a.reseed_soak.get('soak_status')}`** "
                f"`{a.reseed_soak.get('counts')}` "
                f"post_complete={a.reseed_soak.get('observed_seeded_post_complete')} "
                f"empty_queue={a.reseed_soak.get('observed_seeded_empty_queue')}"
            )
        if a.agent_tokens:
            lines.append(
                f"- Agent tokens (log rollup): **{sum(a.agent_tokens.values())}** "
                f"`{a.agent_tokens}`"
            )
        if a.false_mvp_slugs:
            lines.append(
                f"- False MVP on disk now: {len(a.false_mvp_slugs)} "
                f"({', '.join(a.false_mvp_slugs[:6])}…)"
            )
        lines.append(f"- Dead-role pending: {a.dead_role_pending or '{}'}")
        lines.append("")
        lines.append("| Sev | Class | Message |")
        lines.append("|-----|-------|---------|")
        for f in a.findings:
            msg = f.message.replace("|", "/")[:120]
            lines.append(f"| {f.severity} | `{f.cls}` | {msg} |")
        lines.append("")
        lines.append("### Summary counts")
        lines.append(f"`{a.summary()}`")
        lines.append("")
    lines.extend(
        [
            "## Handoff options",
            "",
            "1. `/lfg <named fix>` — if Medium+ runner bug is clear",
            "2. Re-run overnight — if fix already on disk and process was stale",
            "3. stop",
            "",
            "## Non-claims",
            "",
        ]
    )
    if audits:
        for nc in audits[0].non_claims:
            lines.append(f"- {nc}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Overnight ops audit (measure-only)")
    ap.add_argument("--pipeline-dir", type=Path, default=None)
    ap.add_argument("--overnight-dir", type=Path, action="append", default=None)
    ap.add_argument("--latest", type=int, default=1, help="Audit N newest overnight_* dirs")
    ap.add_argument("--json", type=Path, default=None, help="Write JSON report")
    ap.add_argument("--md", type=Path, default=None, help="Write markdown report")
    args = ap.parse_args(argv)

    pipe = (args.pipeline_dir or _default_pipeline_dir()).resolve()
    if args.overnight_dir:
        dirs = [Path(p).resolve() for p in args.overnight_dir]
    else:
        dirs = list_overnight_dirs(pipe / "logs", latest=args.latest)

    if not dirs:
        print(f"No overnight dirs under {pipe / 'logs'}")
        return 2

    audits = [audit_overnight(d, pipeline_dir=pipe) for d in dirs]
    md = format_markdown(audits)
    print(md)
    if args.md:
        args.md.parent.mkdir(parents=True, exist_ok=True)
        args.md.write_text(md, encoding="utf-8")
        print(f"wrote {args.md}")
    if args.json:
        payload = {
            "schema": SCHEMA,
            "generated_at": _iso(),
            "pipeline_dir": str(pipe),
            "runs": [
                {
                    **{k: v for k, v in asdict(a).items() if k != "findings"},
                    "findings": [asdict(f) for f in a.findings],
                    "summary": a.summary(),
                }
                for a in audits
            ],
            "non_claims": audits[0].non_claims if audits else [],
        }
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
