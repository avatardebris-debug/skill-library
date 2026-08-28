---
name: test-security
description: Product security lab for a running surface — threat sketch, authZ matrix, input attacks, dependency/SCA notes, and optional DAST-style probes. Use when /test-security, threat model, DAST, authZ matrix, OWASP check on the product, or release-profile security. Distinct from qc-security (factory secrets/allow_live greps). Not a pentest firm and not field_proven.
metadata:
  short-description: Product threat sketch plus dynamic security probes
  version: "1.0"
  argument-hint: "[scope] [--mode sketch|matrix|dast|full]"
---

# Test Security

Product-facing security QC. Leave factory scanners to `qc-security`.

## When to use

- Auth, multi-tenant, PII, webhooks, file upload, tool/shell escape, or payment journeys
- Release-profile `test-strategy`
- User asks for threat model, DAST, authZ matrix, OWASP on **this product**

## When NOT to use

| Intent | Use instead |
|--------|-------------|
| Factory secrets / allow_live / shell_safety greps | `qc-security` |
| Prose SAST of a whole repo | `comprehensive-codebase-review` |
| Honesty of prove-gates | `qc-honesty` |
| "We are secure" crown | never this skill alone |

## Modes

| Mode | Output |
|------|--------|
| `sketch` | STRIDE-lite threats + trust boundaries only |
| `matrix` | actor × action × object allow/deny cases |
| `dast` | probes against a running surface |
| `full` | sketch + matrix + whatever probes the surface allows |

## Procedure

1. Draw trust boundaries (user, admin, worker, model/tool, datastore, third party).
2. List 5–15 credible threats. Skip movie-plot.
3. Write an authZ matrix for load-bearing actions (read/write/delete/admin/tool-exec).
4. If a surface is up, run **non-destructive** probes only unless the user explicitly allows destructive ones
   - unauth access to admin routes
   - IDOR-style object swap on one fixture id
   - oversized / unexpected content-type on upload or JSON
   - path/header injection samples
   - secret-in-response check on error bodies
5. If lockfiles exist, note unpinned / known-old deps as findings (SCA-lite). Do not dump CVE encyclopedias.
6. Write `.factory/test/security/SECURITY.md`. High findings need a repro and an owner fix path.
7. Stop. Do not declare the product hardened.

## SECURITY.md contract

```markdown
# Security
Mode: sketch | matrix | dast | full
Surface: …

## Boundaries
## Threats
| ID | Threat | Boundary | Severity | Probe? | Result |

## AuthZ matrix
| Actor | Action | Object | Expected | Observed |

## Dependency notes
## Verdict: PASS | FAIL | CONDITIONAL | PENDING
## Non-claims
- Not a pentest
- Not qc-security factory health
- Green probes ≠ field_proven
```

## Rules

- Default probes are read-only / fixture-scoped. No production spray, no credential stuffing wordlists.
- Do not write exploit how-to beyond the minimum repro the fix needs.
- Missing surface → PENDING sketch, not PASS.
- Factory `allow_live` policy stays in `qc-security`.

## Related

- `qc-security` = factory leaf
- `test-strategy` routes High auth/PII rows here
- `test-resilience` covers dead dependencies, not hostile callers
- `test-production-readiness` may require this for release profile
