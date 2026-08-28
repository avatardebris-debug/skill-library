---
name: test-strategy
description: Risk-based product test strategy that decides which journeys and failure classes get smoke, exploratory, contracts, performance, security, resilience, or field-test. Use when /test-strategy, write a test plan, what should we test, risk-based testing, or before factory/gauntlet test fan-out. Not a test runner. Not factory-qc profiles (those are factory health).
metadata:
  short-description: Risk-ranked product test plan and skill routing
  version: "1.0"
  argument-hint: "[scope] [--profile lean|standard|release]"
---

# Test Strategy

You are the **product test strategist**. You choose *what* to run and *how much* is enough. You do not execute suites.

Factory-qc `pre-merge` / `deep-audit` profiles are factory-health strategy. This skill is for the **shipped product** (workspace, AIM/IDEA/TARGET, or explicit scope).

## When to use

- Before `test-smoke` / `test-exploratory` / `field-test` on a new product
- User says test plan, risk-based testing, "what do we actually need to test"
- Production-readiness wants a written plan instead of running every lab

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Run critical paths | `test-smoke` |
| Break-it sessions | `test-exploratory` |
| Factory scanners | `factory-qc` |
| Prove the product | `field-test` (mechanical) + dual gate |
| Session diff verify | `check-work` / `impact-tests` |

## Profiles

| Profile | Default labs |
|---------|----------------|
| `lean` | smoke + honesty of claims + 1 negative path per critical journey |
| `standard` | lean + exploratory + conflict (if shared state) + analytics schema |
| `release` | standard + performance + security-dynamic + resilience + field-test plan |

Override from AIM risk (money, auth, PII, multi-tenant, overnight autonomy = release).

## Procedure

1. Load AIM / IDEA / TARGET / REQUIREMENTS.md / field aim if present.
2. List 3–8 **canonical journeys** and 3–8 **failure classes** (auth fail, dependency down, poison input, concurrent write, slow dependency, leaked secret).
3. Score each journey × class as impact × likelihood (H/M/L). Do not invent precision.
4. Route each High cell to a **named skill** and an exit criterion.
5. Write `.factory/test/STRATEGY.md` (and copy under `notes/test/STRATEGY.md` if no factory dir).
6. Stop. Do not run the labs unless the user asked in the same turn.

## STRATEGY.md contract

```markdown
# Test strategy — <product or scope>
Profile: lean | standard | release
Bar: what "enough" means in one sentence

## Journeys
| ID | Journey | Why critical |

## Risks
| ID | Failure class | Impact | Likelihood | Owner skill | Exit criterion |

## Out of scope
- … (named, with why)

## Sequence
1. test-smoke
2. …

## Non-claims
- Plan file ≠ tests passed
- Strategy ≠ field_proven
```

## Rules

- Prefer fewer High rows over a matrix that nobody will run.
- Every High row must name an existing skill or an explicit "no skill — manual".
- Money, authZ, data-loss, and secret-leak cannot be Out of scope without a written waiver.
- Factory health leaves (`qc-*`) do not satisfy product High rows.

## Related

- Feeds `test-smoke`, `test-exploratory`, `test-conflict`, `test-performance`, `test-security`, `test-resilience`, `acceptance-from-req`, `field-test`
- Required evidence for a honest `test-production-readiness` CONDITIONAL/GO when profile is `release`
- `req` supplies statements; this skill ranks them as test risk
