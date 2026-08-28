---
name: test-resilience
description: Fault-inject against a running product — kill or delay dependencies, drop messages, restart mid-journey, fill disk or starve CPU if safe — and record recovery vs expected degrade. Use when /test-resilience, chaos, fault injection, dependency down, timeout storm, or release-profile resilience. Distinct from test-conflict (races) and qc-runtime-control (static stall proxies).
metadata:
  short-description: Chaos and fault-injection on a running product
  version: "1.0"
  argument-hint: "[scope] [--faults timeout,down,restart]"
---

# Test Resilience

You break **neighbors and timing**, not source structure.

## When to use

- Product talks to DB, queue, LLM, object store, or another process
- Overnight / always-on loops
- Release-profile strategy names "dependency down" as High

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Races / lost updates | `test-conflict` |
| Static factory stall smells | `qc-runtime-control` |
| Overnight log receipts | `overnight-ops-audit` |
| Hostile caller / authZ | `test-security` |
| Load while healthy | `test-performance` |

## Fault catalog (pick 2–5)

| Fault | Typical inject |
|-------|----------------|
| `timeout` | delay dependency 2–10× SLO |
| `down` | refuse connection / kill sidecar |
| `error` | 500 / malformed body from stub |
| `restart` | SIGTERM mid-journey |
| `partition` | drop messages one way |
| `resource` | disk-full or RSS cap — only in disposable env |

## Procedure

1. Confirm disposable environment. Refuse resource/down faults on anything that looks like shared prod.
2. Pick one canonical journey from smoke/strategy.
3. Establish a healthy baseline (one successful run).
4. Inject one fault at a time. Record observed degrade (error, retry, queue, partial write).
5. Remove fault. Record recovery (self-heal vs stuck vs duplicate side effect).
6. Write `.factory/test/resilience/RESILIENCE.md` with exact inject commands.
7. Promote a sticky fail into smoke or a dedicated regression.

## RESILIENCE.md contract

```markdown
# Resilience
Env: disposable? yes/no
Journey: …

| Fault | Inject | During | After remove | Expected | Verdict |

## Duplicate / lost-write notes
## Verdict: PASS | FAIL | CONDITIONAL | SKIPPED
```

## Expected-degrade rule

PASS does **not** require the journey to succeed under every fault. PASS means
observed behavior matches the written expect (fail closed, retry, idempotent
replay, or operator-visible stuck). Unexpected data corruption or silent drop
is FAIL.

## Rules

- No inject without a documented off switch.
- Do not claim chaos-engineering maturity from one timeout test.
- Static `qc-runtime-control` green does not skip this skill.
- Not field_proven.

## Related

- `test-conflict`, `test-performance`, `test-security`
- `qc-runtime-control` / `overnight-ops-audit` for factory control plane
- `test-production-readiness` release evidence
