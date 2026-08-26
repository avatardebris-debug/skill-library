---
name: instrument-analytics
description: Add or verify structured analytics, metrics, traces, and error reporting so the system is observable. Defines event schema and key queries/dashboards. Use early in factory runs and before production-readiness or exploratory testing. Enables later root-cause analysis.
metadata:
  short-description: Structured analytics, metrics, traces, and error reporting for observability
  version: "1.0"
---

# Instrument Analytics

Make the system observable so later RCA, exploratory testing, and production monitoring have real data.

## When to run

- Early in any software-factory or gauntlet run (before heavy implementation).
- Before test-exploratory or test-production-readiness.
- Whenever the codebase lacks structured events, traces, or error reporting.

## Core deliverables

1. **Event schema** — named events with required fields (user/session ids, timestamps, action, outcome, error codes, latency).
2. **Metrics** — counters, gauges, histograms for key flows (success rate, latency percentiles, error rates).
3. **Traces** — correlation IDs and span structure for multi-step flows.
4. **Error reporting** — structured capture of exceptions with context (no PII leakage).
5. **Key queries / dashboards** — the 5–10 questions an operator or RCA skill should be able to answer immediately.

## Instructions

1. Inventory existing logging/metrics/traces (if any).
2. Define the minimal event schema needed for the main user journeys and critical paths.
3. Add or update instrumentation code (or config) so the schema is emitted.
4. Document the schema and the key queries in a durable place (e.g. `.factory/analytics/SCHEMA.md` or equivalent).
5. Verify that at least one happy-path and one error-path event is actually emitted when the relevant code runs.
6. Hand off to test-smoke / test-exploratory / rca-from-analytics with the schema location.

## Guards

- Prefer structured fields over free-text log lines.
- Never log secrets, tokens, or raw PII.
- Keep the schema small and evolvable; avoid premature high-cardinality dimensions.
- If the project already has good observability, document it and skip re-instrumentation.
