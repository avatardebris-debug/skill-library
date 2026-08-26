---
name: rca-from-analytics
description: Consume analytics, logs, traces, and crash reports to produce ranked root-cause hypotheses with evidence and concrete fix candidates. Feeds the gauntlet fix loop. Use after exploratory sessions, production-like failures, or when crashes need diagnosis.
metadata:
  short-description: Ranked root-cause hypotheses from logs/traces/analytics with fix candidates
  version: "1.0"
---

# RCA from Analytics

Turn observability data into ranked, evidence-backed root-cause hypotheses and concrete fix candidates.

## Inputs

- Structured events / metrics (from instrument-analytics)
- Logs and traces
- Crash / error reports
- Session or exploratory test artifacts

## Process

1. Gather the relevant time window and correlation IDs.
2. Reconstruct the failing journey(s) from traces/events.
3. Identify the first divergence from expected behavior.
4. Generate 3–7 ranked root-cause hypotheses, each with:
   - Evidence (specific log lines, metric spikes, trace spans)
   - Confidence
   - Blast radius
5. For the top hypotheses, propose concrete fix candidates (code, config, or process).
6. Write a short RCA note that the gauntlet or human can act on.

## Output

- Ranked list of hypotheses with evidence
- Recommended next action (fix candidate or further instrumentation)
- Links to the supporting data

## Guards

- Prefer evidence over speculation.
- Distinguish correlation from causation.
- Flag when data is insufficient and what additional instrumentation would close the gap.
