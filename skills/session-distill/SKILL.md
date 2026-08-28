---
name: session-distill
description: >
  Distill Grok Build sessions (or pasted long chats) into OpenAI chat-format JSONL
  fine-tune pairs that teach project thinking, troubleshooting, feature expansion,
  testing, and engineering judgment. Scans ~/.grok/sessions/ (summary + chat_history/updates)
  or the current conversation; writes to ~/.grok/fine-tunes/. Use when the user runs
  /session-distill, says "distill this session", "make fine-tune pairs", "export training
  data from this chat", "session to SFT", or wants to train a model (e.g. Qwen) on how
  projects were developed and debugged.
metadata:
  short-description: "Session to fine-tune JSONL pairs"
argument-hint: "[current | session-id | project-path | keywords]"
---

# Session Distill

Turn Grok Build sessions (or a long chat in the current thread) into **high-signal SFT pairs** that teach a model how to reason about real projects: how features were planned, built, tested, expanded, and debugged.

This skill produces a **dataset only**. Training base weights (Qwen, etc.) is a separate step; point Unsloth / LLaMA-Factory / Axolotl / TRL at the JSONL this skill writes.

## Defaults

| Setting | Value |
|--------|--------|
| Sessions root | `~/.grok/sessions/` (Windows: `C:\Users\avata\.grok\sessions\`) |
| Output dir | `~/.grok/fine-tunes/` (Windows: `C:\Users\avata\.grok\fine-tunes\`) |
| Format | OpenAI chat JSONL - one object per line: `{"messages":[...]}` |
| Also write | Optional ShareGPT twin if user asks |
| Training target | Qwen-family and other chat models via standard SFT tooling |

Resolve `~` to the user's home / `GROK_HOME` when set.

## Arguments

Parse `$ARGUMENTS` (or the user's message after the skill trigger):

| Input | Meaning |
|-------|---------|
| empty / `current` / `this` | Distill **this** conversation (use in-context turns; if thin, load the session dir for this session id from disk) |
| UUID-like session id | Distill that session under `sessions/**/<id>/` |
| path / project name / keywords | Find matching sessions by `summary.json` title, cwd, or path slug |
| `list` | Only list candidate sessions; do not write pairs yet |
| `merge` | After writing per-session files, also append/merge into a corpus file |

If ambiguous, list top matches (id, title, cwd, updated_at, message counts) and ask which to distill.

## Workflow

### 1. Resolve source

**A. Current conversation**

- Prefer the live thread the user is in (user asks + agent replies + tool outcomes they care about).
- Also load on-disk files when available: find `sessions/**/<session-id>/` where `summary.json` → `info.id` matches the current session, or the most recently updated session for this cwd.

**B. Past Grok sessions**

Layout (see Grok docs `17-sessions.md`):

```
~/.grok/sessions/<url-encoded-cwd>/<session-id>/
  summary.json          # title, timestamps, model, message counts, cwd
  updates.jsonl         # authoritative stream (user + agent + tools)
  chat_history.jsonl    # raw model-facing messages (noisy: system prompts, synthetic)
```

Prefer **`updates.jsonl`** for human-visible dialogue. Use `chat_history.jsonl` only as a fallback when updates are sparse.

Helper (optional, faster bulk listing):

```bash
python "%USERPROFILE%\.grok\skills\session-distill\scripts\list_sessions.py"
python "%USERPROFILE%\.grok\skills\session-distill\scripts\list_sessions.py" --query "rpgbuild"
python "%USERPROFILE%\.grok\skills\session-distill\scripts\extract_turns.py" --session-id <id> --out turns.jsonl
```

On non-Windows, replace `%USERPROFILE%\.grok` with `~/.grok`.

**C. Pasted transcript**

If the user pastes a long chat, treat that text as the only source.

### 2. Reconstruct the story

Do **not** dump the session raw into training data. Read enough of the session to answer:

1. What was the project / goal?
2. How did requirements evolve?
3. What features were added, changed, or rejected — and why?
4. How was work tested / verified?
5. What broke, how was it investigated, what fixed it?
6. What architecture or tradeoff decisions were made?
7. What would a strong agent do next time given the same user request?

Chunk multi-topic sessions into separate arcs (e.g. "auth setup", "debug deploy", "add export"). One arc → one or more training examples.

### 3. Extract high-signal pairs

Emit pairs in these **archetypes** (use whichever the session supports; skip empty ones):

| Archetype | User side | Assistant side |
|-----------|-----------|----------------|
| **project-thinking** | Goal or vague idea | Clarify scope, propose plan, sequence of work, risks |
| **feature-expand** | "Add X" / grow capability | Design touchpoints, files to change, tests, rollout |
| **troubleshoot** | Bug / failure / unexpected | Hypotheses, evidence, minimal repro, root cause, fix, verify |
| **test-verify** | "Does it work?" / ship check | What to run, what success looks like, gaps |
| **tool-judgment** | Task needing investigation | What to inspect first, what not to touch, safety |
| **recovery** | Failed approach | Why it failed, pivot, correct path |

**Include**

- Clear user intent → structured reasoning → concrete next steps or resolution
- Multi-turn examples when the session shows iterative debug (user → probe → result → fix)
- Compressed tool use: summarize tool results in the assistant text ("I ran the tests; 2 failed in auth…") rather than pasting megabytes of logs

**Exclude**

- Pure chitchat, skill-menu noise, system prompts, credential dumps
- Failed thrashing with no learning (unless reframed as a recovery pair)
- Duplicate near-identical turns
- Entire raw `chat_history` system blobs

**Quality bar:** each pair should teach *how to think*, not only the final code snippet. Prefer reasoning + decision + verification over copy-paste patches alone.

### 4. Redact secrets

Before writing any file:

- Replace API keys, tokens, passwords, private URLs with placeholders (`<REDACTED_API_KEY>`, etc.)
- Redact emails / personal identifiers if present in secrets context
- Never copy `.env` contents into pairs
- If unsure whether a string is a secret, redact it

### 5. Write outputs

Create `~/.grok/fine-tunes/` if missing.

**Per-session file:**

```
~/.grok/fine-tunes/<YYYYMMDD>-<short-title-or-id>.jsonl
```

Example: `20260721-rpgbuild-auth-debug.jsonl`

**Optional corpus** (when user says merge, or after multiple sessions):

```
~/.grok/fine-tunes/corpus-sft.jsonl
```

Append new lines; do not rewrite the whole corpus unless asked.

**Line format (required):**

```json
{"messages":[{"role":"system","content":"<SYSTEM>"},{"role":"user","content":"<USER>"},{"role":"assistant","content":"<ASSISTANT>"}],"meta":{"archetype":"troubleshoot","source_session":"<id>","title":"<session title>"}}
```

`meta` is optional for trainers that strip unknown fields; keep it for provenance. If a trainer rejects `meta`, also offer a clean `messages`-only variant on request.

**Default system prompt** (unless the session implies a better one):

```text
You are a senior software engineering agent. You reason carefully about project goals, design tradeoffs, implementation steps, testing, and troubleshooting. Prefer root-cause investigation over random fixes. Explain plans clearly, verify work, and keep changes focused.
```

**Assistant style in pairs:**

- Complete sentences, concrete steps
- Show investigation before fixes when troubleshooting
- Mention verification (tests run, what passed)
- Avoid Grok-internal tool JSON / function-call markup; describe actions in natural language suitable for a normal chat model

### 6. Multi-turn examples

When the arc is iterative, use multiple user/assistant turns inside one `messages` array:

```json
{"messages":[
  {"role":"system","content":"..."},
  {"role":"user","content":"The deploy fails with exit 1."},
  {"role":"assistant","content":"I'll check the CI log and the last deploy config before changing anything..."},
  {"role":"user","content":"Log shows missing DATABASE_URL in staging."},
  {"role":"assistant","content":"Root cause is missing env in the staging secret set. Fix: ... Verify by ..."}
]}
```

Cap roughly **6–12 turns** per example; split longer arcs.

### 7. Report to the user

After writing:

1. Paths written
2. Pair count by archetype
3. Source session id(s) and titles
4. Any redactions performed (counts, not secret values)
5. Short note on next training steps (see `references/training-notes.md`)

Do **not** claim the model was fine-tuned — only that the dataset is ready.

## Pair quality checklist

Before finishing, scan the JSONL:

- [ ] Valid JSON per line
- [ ] Every example has `user` and `assistant`
- [ ] No secrets in cleartext
- [ ] No giant system-prompt dumps from Grok internals
- [ ] At least one of: plan / debug / feature / test reasoning per example
- [ ] Titles/filenames are filesystem-safe

If fewer than 3 solid pairs can be made, say so and suggest which other sessions (by keyword/project) to pull in.

## Current-session shortcut

When the user runs `/session-distill` mid-project with a long thread:

1. Distill **this** thread first (highest priority).
2. Offer to also pull older sessions for the same cwd / project name.
3. Write immediately so they can iterate: distill → skim pairs → re-run with feedback ("more debug, less setup").

## Do not

- Train or download model weights unless the user explicitly asks for a separate training run
- Upload fine-tune files to any external service without explicit permission
- Overwrite existing JSONL without confirming (append or use a new timestamped name)
- Invent project facts not grounded in the session
---