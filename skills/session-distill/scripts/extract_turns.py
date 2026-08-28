#!/usr/bin/env python3
"""Extract user/assistant text turns from a Grok session directory.

Prefers updates.jsonl (display stream). Falls back to chat_history.jsonl.
Writes a simple JSONL of {role, content, kind} for the agent to refine into SFT pairs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


def grok_home() -> Path:
    env = os.environ.get("GROK_HOME")
    if env:
        return Path(env)
    return Path.home() / ".grok"


def find_session_dir(session_id: str, root: Path) -> Path | None:
    # exact folder name match
    for p in root.rglob(session_id):
        if p.is_dir() and (p / "summary.json").exists():
            return p
    return None


def text_from_content(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, dict):
        if content.get("type") == "text":
            return content.get("text") or ""
        # nested
        parts = []
        for k in ("text", "content"):
            if k in content and isinstance(content[k], str):
                parts.append(content[k])
        return "\n".join(parts)
    if isinstance(content, list):
        chunks = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text" and item.get("text"):
                    chunks.append(item["text"])
                elif isinstance(item.get("text"), str):
                    chunks.append(item["text"])
            elif isinstance(item, str):
                chunks.append(item)
        return "\n".join(chunks)
    return str(content)


NOISE_PREFIXES = (
    "<user_info>",
    "<system-reminder>",
    "<skill_information>",
    "You are Grok",
)


def is_noise(text: str) -> bool:
    t = text.strip()
    if not t:
        return True
    if len(t) > 20000:
        return True
    for p in NOISE_PREFIXES:
        if t.startswith(p):
            return True
    if t.startswith("{") and "sessionUpdate" in t[:200]:
        return True
    return False


def extract_from_updates(path: Path) -> list[dict]:
    """Merge streaming chunks into turns."""
    user_buf: list[str] = []
    asst_buf: list[str] = []
    thought_buf: list[str] = []
    turns: list[dict] = []

    def flush_user():
        nonlocal user_buf
        text = "".join(user_buf).strip()
        user_buf = []
        if text and not is_noise(text):
            turns.append({"role": "user", "content": text, "kind": "user"})

    def flush_assistant():
        nonlocal asst_buf, thought_buf
        text = "".join(asst_buf).strip()
        thought = "".join(thought_buf).strip()
        asst_buf = []
        thought_buf = []
        if text and not is_noise(text):
            item = {"role": "assistant", "content": text, "kind": "assistant"}
            if thought:
                item["thought"] = thought
            turns.append(item)

    if not path.exists():
        return turns

    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            params = ev.get("params") or {}
            update = params.get("update") or {}
            kind = update.get("sessionUpdate") or ""
            content = update.get("content")
            text = text_from_content(content)

            if kind == "user_message_chunk":
                # new user chunk after assistant → flush assistant first
                if asst_buf or thought_buf:
                    flush_assistant()
                user_buf.append(text)
            elif kind == "agent_message_chunk":
                if user_buf:
                    flush_user()
                asst_buf.append(text)
            elif kind == "agent_thought_chunk":
                if user_buf:
                    flush_user()
                thought_buf.append(text)
            elif kind in ("turn_completed", "agent_end", "message_end"):
                if user_buf:
                    flush_user()
                if asst_buf or thought_buf:
                    flush_assistant()

    if user_buf:
        flush_user()
    if asst_buf or thought_buf:
        flush_assistant()
    return turns


def extract_from_chat_history(path: Path) -> list[dict]:
    turns: list[dict] = []
    if not path.exists():
        return turns
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            role = msg.get("type") or msg.get("role") or ""
            if role not in ("user", "assistant"):
                continue
            text = text_from_content(msg.get("content"))
            if is_noise(text):
                continue
            # strip user_query wrappers when present
            m = re.search(r"<user_query>\s*(.*?)\s*</user_query>", text, re.DOTALL)
            if m:
                text = m.group(1).strip()
            turns.append({"role": role, "content": text, "kind": role})
    return turns


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", required=True, help="Session UUID")
    parser.add_argument(
        "--sessions-root",
        type=Path,
        default=None,
        help="Override sessions root",
    )
    parser.add_argument(
        "--session-dir",
        type=Path,
        default=None,
        help="Direct path to session directory",
    )
    parser.add_argument("--out", type=Path, default=None, help="Write JSONL here")
    parser.add_argument(
        "--include-thoughts",
        action="store_true",
        help="Keep agent thought text in output",
    )
    args = parser.parse_args()

    root = args.sessions_root or (grok_home() / "sessions")
    session_dir = args.session_dir or find_session_dir(args.session_id, root)
    if not session_dir:
        print(f"Session not found: {args.session_id}", file=sys.stderr)
        return 1

    updates = session_dir / "updates.jsonl"
    history = session_dir / "chat_history.jsonl"
    turns = extract_from_updates(updates)
    source = "updates.jsonl"
    if len(turns) < 2:
        turns = extract_from_chat_history(history)
        source = "chat_history.jsonl"

    if not args.include_thoughts:
        for t in turns:
            t.pop("thought", None)

    out_lines = [json.dumps(t, ensure_ascii=False) for t in turns]
    payload = "\n".join(out_lines) + ("\n" if out_lines else "")

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload, encoding="utf-8")
        print(f"Wrote {len(turns)} turns from {source} → {args.out}")
    else:
        sys.stdout.write(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
