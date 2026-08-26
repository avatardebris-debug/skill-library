# Skill Library

A curated library of Grok / agent skills for high-agency software engineering, ideation, quality gates, and production-grade agentic workflows.

These skills were developed for building ambitious AI systems, multi-agent factories, gap analysis, zero-based redesign, and continuous improvement loops.

## Skills Included

| Skill | Description |
|-------|-------------|
| **adhd** | Parallel divergent ideation with multiple cognitive frames |
| **comprehensive-codebase-review** | Full-repo proactive audit (bugs, security, performance, debt) |
| **creativity-engine** | Metaphorical, lateral, multi-future creative thinking |
| **elon** | Elon-style engineering: requirements → delete → simplify → accelerate |
| **factory-fanout** | Fan ideas horizontally through software-factory |
| **gap-to-plan** | Measure current vs aim and produce assemblable plans |
| **i-have-adhd** | Shape output for ADHD readers (action-first, numbered steps) |
| **idea-expansion-planner** | First-, second-, and third-order effects analysis |
| **instrument-analytics** | Add structured analytics, metrics, traces, error reporting |
| **lfg** | Full outer ship loop: research → gap-to-plan → gauntlet → review |
| **lfg-all** | Multi-aim ship from ranked suggestions |
| **qc-report** | Meta quality-control report orchestrating specialized checks |
| **rca-from-analytics** | Root-cause analysis from logs/traces/analytics |
| **req** | Requirements inventory before zeroing |
| **slice-deconstruct** | Recursively cut multi-month series into gap-ready packs |
| **software-factory** | Core factory engine from directional aim to production software |
| **suggest** | High-ROI next aims for /lfg |
| **suggest-100-ideas** | ~100 ranked & clustered ideas from an aim |
| **suggest-next-5** | Top 5 next projects with execution path |
| **test-conflict** | Shared-state races and contention testing |
| **test-exploratory** | Adversarial exploratory sessions + synthetic human journeys |
| **test-maintainability** | Audit the test suite itself |
| **test-production-readiness** | Final go/no-go production readiness gate |
| **test-smoke** | Minimal critical-path smoke suite |
| **universal-gauntlet** | High-effort builder ↔ critic loops until quality bar is met |
| **zero** | Zero-based redesign (mission, requirements, from-scratch plan) |
| **zero2** | Code-level mapping after /zero |

## Installation

These skills work with the Grok skill-installer.

### Install a single skill

```bash
# Using the skill-installer skill (recommended)
bash /root/.grok/skills/skill-installer/scripts/install-skill.sh \
  --repo avatardebris-debug/skill-library \
  --path skills/<skill-name> \
  --ref main
```

Or with a full URL:

```bash
bash /root/.grok/skills/skill-installer/scripts/install-skill.sh \
  --url https://github.com/avatardebris-debug/skill-library/tree/main/skills/<skill-name>
```

### Install all skills (example)

You can loop over the directories or install them one by one.

## Structure

```
skills/
  <skill-name>/
    SKILL.md          # Required frontmatter + instructions
```

## License

MIT (where declared). Individual skills may carry their own license in the frontmatter.

## Notes

- These are the **custom / user skills**, not the platform-bundled ones (docx, pdf, pptx, xlsx, ffmpeg, etc.).
- Skills use progressive disclosure: name + description are always visible; body loads on demand.
- Many of these form a coherent stack for ambitious agentic development (suggest → gap-to-plan → software-factory → gauntlet → tests → qc).
