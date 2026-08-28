#!/usr/bin/env python3
"""List Grok Build sessions from ~/.grok/sessions (or GROK_HOME/sessions)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def grok_home() -> Path:
    env = os.environ.get("GROK_HOME")
    if env:
        return Path(env)
    return Path.home() / ".grok"


def load_summary(path: Path) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    info = data.get("info") or {}
    return {
        "id": info.get("id") or path.parent.name,
        "cwd": info.get("cwd") or "",
        "title": data.get("generated_title")
        or data.get("session_summary")
        or "(untitled)",
        "created_at": data.get("created_at") or "",
        "updated_at": data.get("updated_at") or data.get("last_active_at") or "",
        "num_messages": data.get("num_messages") or data.get("num_chat_messages") or 0,
        "model": data.get("current_model_id") or "",
        "path": str(path.parent),
    }


def iter_sessions(root: Path):
    if not root.is_dir():
        return
    for summary in root.rglob("summary.json"):
        # skip locks / nested junk
        if summary.name != "summary.json":
            continue
        row = load_summary(summary)
        if row:
            yield row


def matches(row: dict, query: str) -> bool:
    q = query.lower()
    blob = " ".join(
        [
            row.get("id", ""),
            row.get("title", ""),
            row.get("cwd", ""),
            row.get("path", ""),
            row.get("model", ""),
        ]
    ).lower()
    return all(part in blob for part in q.split())


def sort_key(row: dict):
    ts = row.get("updated_at") or row.get("created_at") or ""
    return ts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=None,
        help="Override sessions directory",
    )
    parser.add_argument(
        "--query",
        "-q",
        default="",
        help="Filter by id/title/cwd/path keywords (space = AND)",
    )
    parser.add_argument("--limit", type=int, default=30, help="Max rows (default 30)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON array instead of a table",
    )
    args = parser.parse_args()

    root = args.sessions_root or (grok_home() / "sessions")
    rows = list(iter_sessions(root))
    if args.query:
        rows = [r for r in rows if matches(r, args.query)]
    rows.sort(key=sort_key, reverse=True)
    rows = rows[: max(1, args.limit)]

    if args.json:
        json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return 0

    if not rows:
        print(f"No sessions found under {root}", file=sys.stderr)
        return 1

    print(f"{'UPDATED':<22} {'MSGS':>5}  {'ID':<36}  TITLE / CWD")
    print("-" * 100)
    for r in rows:
        updated = (r.get("updated_at") or "")[:19].replace("T", " ")
        title = (r.get("title") or "")[:50]
        cwd = r.get("cwd") or ""
        print(
            f"{updated:<22} {r.get('num_messages', 0):>5}  {r.get('id', ''):<36}  {title}"
        )
        if cwd:
            print(f"{'':<22} {'':>5}  {'':<36}  cwd: {cwd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
