# Skill Library

A curated library of Grok / agent skills for high-agency software engineering, ideation, quality gates, and production-grade agentic workflows.

These skills were developed for building ambitious AI systems, multi-agent factories, gap analysis, zero-based redesign, and continuous improvement loops.

This repo is the **cross-device source of truth**. Install into a Grok skills dir; do not treat any one working checkout as canonical.

## Installation

```bash
bash /root/.grok/skills/skill-installer/scripts/install-skill.sh \
  --repo avatardebris-debug/skill-library \
  --path skills/<skill-name> \
  --ref main
```

## Quality stacks

Two complementary stacks. Do not collapse them.

- **Factory self-QC** — `factory-qc` + `qc-*` leaves + `findings-triage`. Measures factory health. Green ≠ `field_proven`.
- **Product QA/QC** — `test-strategy` → labs (`test-smoke`, exploratory, conflict, performance, security, resilience, field-test) → `test-production-readiness`.

## Skills

### Ideation and planning

| Skill | Role |
|-------|------|
| adhd | Parallel divergent ideation |
| autosuggest | Unattended suggest loop |
| creativity-engine | Lateral / multi-future thinking |
| deconstructor | Break a thing into parts |
| dedede | Series deconstruction readiness |
| idea-expansion-planner | First/second/third-order effects |
| idea-plan | Master plan contract |
| phase-plan | Phase + task contract |
| planner | Generic planner |
| gap-to-plan | Current vs aim → plans |
| gap-to-goal | Gap verdict vs a goal |
| slice-deconstruct | Multi-month slice → gap packs |
| suggest / suggest-next-5 / suggest-100-ideas | Next aims |
| think-route | Route how to think |

### Factory and ship loops

| Skill | Role |
|-------|------|
| software-factory | Aim → idea → streams → QC → vote → gauntlet |
| factory-fanout / fanout | Horizontal factory runs |
| factory-improve | Post-field factory product routing |
| factory-qc / factory-qc-handoff | Factory health measure + soft next |
| lfg / lfg-all / encore | Full / multi / residual ship loops |
| universal-gauntlet | Builder ↔ critic until bar |
| elon / elon1 / elon2 | Requirements → delete → restore → accelerate |
| zero / zero2 | Zero-based redesign + code map |
| req | Requirements inventory |
| restore | Human add-back after zero |
| admit-fuel | Fuel admission rubric |
| blocker-identifier | Name blockers |
| pile-shrink | Shrink the pile |

### Factory QC leaves

| Skill | Role |
|-------|------|
| qc-static | Lint/type if tools exist |
| qc-contracts | Public API freeze + path-refs |
| qc-honesty | Dual-gate / soft≠execute smells |
| qc-errors | Bare except / swallowed errors |
| qc-tests | Contract pytest + weak-test heuristic |
| qc-security | Factory secrets / allow_live / shell-safety |
| qc-runtime-control | Static stall proxies |
| qc-coupling-debt | LOC god-modules |
| qc-temporal | Git churn / grow / repeat-fix |
| qc-report | Meta product/static quality report |
| findings-triage | Findings → buckets → packs |

### Product test labs

| Skill | Role |
|-------|------|
| test-strategy | Risk plan and skill routing |
| acceptance-from-req | REQUIREMENTS.md → Given/When/Then |
| test-smoke | Critical-path e2e |
| test-exploratory | Synthetic humans + adversarial tail |
| test-conflict | Races / shared state |
| test-performance | Load / soak / spike vs SLOs |
| test-security | Product threat sketch + probes |
| test-resilience | Fault injection / chaos |
| test-maintainability | Health of the test suite |
| test-production-readiness | GO / NO-GO |
| field-test | Product field plan+run (no self-prove) |
| impact-tests | Diff → pytest targets |
| instrument-analytics | Event schema + queries |
| rca-from-analytics | Telemetry → ranked causes |

### Review, debug, ops

| Skill | Role |
|-------|------|
| check-work | Session verifier subagent |
| code-review | Diff review |
| comprehensive-codebase-review | Full-repo audit |
| harsh-critic | Scorecard critic |
| systematic-debugging | Root-cause discipline |
| json-fixture-diff | Fixture compare |
| overnight-ops-audit | Overnight receipt audit |
| morning-ops-pack | Morning ops pack |
| session-distill | Distill session traces |

### Meta / UX

| Skill | Role |
|-------|------|
| create-skill | Author a new skill |
| help | Skill help |
| i-have-adhd | ADHD-shaped output |
| imagine | Image generation workflow |

## Structure

```
skills/
  <skill-name>/
    SKILL.md
    scripts/      # optional
    references/   # optional
```

## License

MIT (where declared). Individual skills may carry their own license in the frontmatter.

## Notes

- Custom / user skills only — not platform-bundled docx/pdf/pptx/xlsx/ffmpeg.
- Progressive disclosure: name + description always visible; body loads on demand.
- `qc-security` ≠ `test-security`. Factory leaf vs product lab.
- `factory-qc` green ≠ `field_proven`.
