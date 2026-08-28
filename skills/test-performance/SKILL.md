---
name: test-performance
description: Run product load, soak, spike, or stress against stated SLOs and write a PASS/FAIL performance report. Use when /test-performance, load test, soak test, latency SLO, p95, capacity, or qc-report performance pillar needs execution not just static complexity notes. Not a profiler-only code review. Not factory overnight soak.
metadata:
  short-description: Execute load/soak/spike vs SLOs
  version: "1.0"
  argument-hint: "[scope] [--mode load|soak|spike|stress]"
---

# Test Performance

You **execute** performance work against a runnable product surface. `qc-report` may flag complexity; this skill produces runtime evidence.

## When to use

- TARGET or STRATEGY names latency, throughput, or saturation SLOs
- Release-profile strategy
- User asks for load / soak / spike / stress

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Big-O / hotspot reading of source | `qc-report` / CCR |
| Factory overnight stall receipts | `overnight-ops-audit` |
| Race conditions | `test-conflict` |
| Dependency death | `test-resilience` |

## Inputs

- SLO source (TARGET.md, STRATEGY.md, or user). If missing, propose defaults and wait or mark CONDITIONAL.
- Runnable surface (HTTP, CLI loop, queue worker). If none, write a pending plan and stop.

## Modes

| Mode | Question | Default bar |
|------|----------|-------------|
| `load` | Holds target RPS/concurrency with p95 under SLO | 1–5 min |
| `soak` | No leak / error-rate creep at modest load | 10+ min if environment allows |
| `spike` | Recovers after 3–5× burst | burst + settle |
| `stress` | Where it breaks (find saturation, do not require pass) | document cliff |

## Procedure

1. Record environment (CPU, replicas, dataset size). Missing env notes = CONDITIONAL.
2. Pick one primary journey from strategy/smoke (do not boil the ocean).
3. Drive load with the simplest available tool (hey, wrk, k6, vegeta, locust, custom loop). Do not invent a platform.
4. Capture p50/p95/p99, error rate, timeouts, CPU/RSS if available.
5. Compare to SLO. Write `.factory/test/performance/PERFORMANCE.md` plus raw logs.
6. Promote any hard fail into a regression note for smoke or a dedicated perf script.

## PERFORMANCE.md contract

```markdown
# Performance
Mode: load | soak | spike | stress
Surface: …
SLO: …
Tool + command: …
Duration / concurrency: …

| Metric | SLO | Observed | Verdict |

## Saturation notes
## Failures / timeouts
## Verdict: PASS | FAIL | CONDITIONAL | PENDING
```

## Rules

- No runnable surface → PENDING, not PASS.
- Stress mode documents the cliff; do not call a crash at 100× a FAIL unless SLO said it must survive.
- Do not claim field_proven from a green 60-second load.
- Do not treat static complexity scores as this skill's output.

## Related

- Called by release-profile `test-strategy`
- Evidence for `test-production-readiness`
- Pair with `instrument-analytics` so p95 is queryable next time
