---
name: suggest-100-ideas
description: Generate approximately 100 ranked and clustered ideas from a directional aim, open brief, or current workspace context. Use for /suggest-100-ideas, give me 100 ideas, idea flood, or as input to factory-fanout. Output is structured for later filtering and software-factory runs.
metadata:
  short-description: ~100 ranked & clustered ideas from an aim or context
  version: "1.0"
---

# Suggest 100 Ideas

Flood the problem space with a large, ranked, clustered set of ideas so later filtering and factory-fanout have high-quality raw material.

## Process

1. Clarify the directional aim or open brief (or invent one from workspace if none given).
2. Generate ideas across multiple frames (user value, technical leverage, business model, risk inversion, adjacent markets, 10x, 0.1x, etc.).
3. Cluster related ideas.
4. Rank inside and across clusters by expected ROI / leverage / feasibility balance.
5. Output ~100 items in a structured, filterable format (markdown table or numbered list with cluster tags).

## Output format

- Cluster name
- Ranked ideas with one-line rationale
- Optional: estimated effort / impact tags

The result is intended to be fed into factory-fanout or manual selection.
