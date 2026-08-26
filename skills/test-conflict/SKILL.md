---
name: test-conflict
description: Detect and exercise shared-state conflicts, races, resource contention, and ordering hazards under concurrent or interleaved use. Use after multi-agent merges or any code that touches shared resources, caches, databases, or global state.
metadata:
  short-description: Shared-state races, contention, and ordering hazard testing
  version: "1.0"
---

# Test Conflict

Exercise the system under concurrent and interleaved access to shared resources so races and ordering bugs surface before production.

## Focus areas

- Shared mutable state (caches, in-memory stores, global config)
- Database transactions and isolation levels
- File-system or lock contention
- Multi-agent / multi-worker coordination points
- Ordering assumptions that break under interleaving

## Process

1. Identify shared resources and critical sections.
2. Design concurrent scenarios (parallel writers, reader-writer mixes, delayed operations).
3. Run or simulate the scenarios.
4. Record failures, lost updates, deadlocks, or surprising orderings.
5. Propose hardening (locks, versioning, idempotency, retries, etc.).

## Output

Evidence of conflicts found (or clean bill of health) plus recommended fixes.
