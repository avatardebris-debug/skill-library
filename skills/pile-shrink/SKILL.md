---
name: pile-shrink
description: >-
  Classify PIPELINE_DIR projects into skip vs maybe so Gene is not one-by-one
  on the 370/412/24 production pile. Writes counts + a small Gene sample for
  manual labels until skip buckets are trusted. Use when /pile-shrink, "shrink
  the pile", "classify 412 projects", "falsify candidates", or "Gene sample of
  skip vs maybe". Not the use-list (that inbox is already walked). Never
  auto-LFG, never invent field_proven, never mutate project state, never RL-train.
metadata:
  short-description: "Classify 412-pile skip/maybe + Gene sample; no LFG"
argument-hint: "[--pipeline-dir PATH] [--sample-n-per N] [--record-label SLUG PREDICTED VERDICT]"
---

# /pile-shrink — Shrink the production pile (not the use-list)

The **use-list** is what you + Gene already walked. This skill classifies the
**waste pile** (disk `field_proven` / 412 projects / bare complete) so most of
it can be skipped. Until that skip is trusted, the same run emits a **small
sample** for quick labels (`agree` / `wrong:<bucket>`).

```text
PIPELINE_DIR/projects → buckets → counts + Gene sample → labels.jsonl
                                                      ↓
                                         trust skip only after labels agree
                                                      ↓
                                              never LFG / never crown
```

**Not** `/suggest` (LFG aims). **Not** the use-list routine. **Not** RL.

## Buckets (closed)

| Bucket | Meaning | Gene? |
|--------|---------|-------|
| `already_use_list` | Named on USE_LIST (open/parked/rejected/skip) | no — already decided |
| `harness_skip` | Factory harness / probe / trial | sample only |
| `souvenir` | Thin complete / factory leftover | sample only |
| `blocked_key` | TOS / scrape / key / bank | sample only |
| `product_maybe` | Might be a real use | sample + later inbox |
| `inspect` | Not enough signal | sample only |

Disk `status=field_proven` is **not** product evidence.

## Workflow

1. Workspace root.
2. Run:

```text
python -m pipeline.pile_shrink --pipeline-dir $env:PIPELINE_DIR
# or
python scripts/pile_shrink.py --pipeline-dir $env:PIPELINE_DIR
```

3. Read `notes/ops/pile_shrink/LATEST.md` and `.../SAMPLE.md`.
4. Print counts + the sample. Ask for labels on the sample only.
5. Record labels (append-only, no retrain):

```text
python -m pipeline.pile_shrink --record-label <slug> <predicted> agree
python -m pipeline.pile_shrink --record-label <slug> <predicted> wrong:product_maybe
```

6. **Stop.** Do not LFG. Do not append USE_LIST rows. Do not crown.

## When to use

- After noticing 370/412/24 cannot be consumed
- Before asking Gene to walk more disk-stamped projects
- When calibrating skip buckets with a short human/Gene sample

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Walk one already-named product | use-list `ROUTINE.md` |
| Next LFG aim | `/suggest` |
| Score Ted notes | `/admit-fuel` |
| Revive stalled mvp_complete | `scripts/revive_false_mvp.py` |
| Train RL on labels | later, after skip is trusted — not this skill |

## Honesty

- field_proven: false
- auto_lfg: false
- heuristic_not_trusted: true until sample labels agree
- use-list is not this classifier

## Related

| Path | Role |
|------|------|
| `pipeline/pile_shrink.py` | Classifier CLI |
| `notes/ops/use_list/USE_LIST.md` | Already-walked inbox (do not dump the pile here) |
| `/admit-fuel` | Research admission, different pile |

## Success criteria

- classifications.json covers every `current_idea.json`
- Gene sample excludes `already_use_list`
- No project state mutated
- No LFG launched
