# Elon2 completion pack (mandatory human-facing close)

At the **end of compress** (after `/restore` metrics, before any ship), print a
**plain conversational** pack. Tables and artifact paths are fine as support;
the lead sections must read like a human brief, not only skill jargon.

Do **not** auto-ship. Stop for human letters. Not Elon1.

---

## Required sections (in order)

### 1. Bottom line (3–5 sentences)

- What was analyzed (path, scale).  
- **Nothing live changed** (or list exceptions if human already approved clone earlier — rare).  
- One-sentence mission.  
- What the plan would keep vs drop vs restore (plain words).  
- Default recommendation (e.g. conceptual approve + thin restore + park).

### 2. Changes if accepted (plan only)

Short bullets, no LOC dump:

- Keep: …  
- Propose drop / thin: …  
- **Merge / share** (from peer-scan + F3): … or “no outside twins found”  
- **Split** (from F4 + partition): … and why not conflicting with merge  
- Optional later: …  
- Restore Tier A (if any): …

### 3. Risks (before accept — cheapest)

Pull from `BLAST_RADIUS.md`. Plain English:

- Who else imports / calls this?  
- What breaks if we split or drop X?  
- Floor/honesty touch? (should be none)  
- Highest residual risk if human later ships  

If `BLAST_RADIUS.md` missing → **write it now** before finishing; do not skip.

### 4. Blast radius table (compact)

| consumer | relies on | if plan ships… |
|----------|-----------|----------------|
| … | … | … |

### 5. Questions you should answer (or ask)

Always include a tailored list. Seed from the template below; **delete
irrelevant** and **add target-specific** ones (usage, graph bridges, etc.).

#### Template seeds

**Product / usage**

- Do you actually use the “nice to have” paths day-to-day (CLI hints, offline
  parse, secondary invent), or almost always the primary path?  
- Have you seen failures or junk output from paths the plan wants to drop?  
- Is the downstream bridge (graph, compose, agent bus) something you rely on
  **now**, or aspirational?

**Risk appetite**

- Prefer **notes only / park**, **thin clone of selected ids**, or a **larger
  gap-to-plan**?  
- Okay losing secondary behavior if the primary path remains?

**Contract / merge vs split**

- If we split: keep a **stable import façade** forever? (Default yes.)  
- Who owns shared constants used by other packages (name the consumer)?  
- Prefer **one reviewable package** or **many small files** for this surface?  
- Any twin the peer-scan found — **merge, share util, or leave**?  

**Process / requirements**

- Open **challenge** requirement rows — decide now or leave open?  
- Ship mode if anything: stop · clone thin · gap-to-plan · not LFG unless expand?

### 6. Options (letters)

Print **zero options** and **restore options** (from child skills).  
If inside full `/elon2` and both packs are ready, present **combined** defaults:

```text
Suggested thin path: zero A + restore A (or F park) + ship stop
```

### 7. Artifact index + metrics

Paths under `notes/zero/<slug>/` + D_prop / R_prop / ratio_prop + calibration note.

### 8. Explicit stop

One line: no ship/clone/LFG until human replies with letters or amend ids.

---

## Tone

Conversational, honest, slightly biased to **leave deleted** and **park**.
Celebrate early risk capture. Never bury importers in an appendix only.

## Anti-patterns

- Tables-only close with no prose risks  
- “ACCEPT” without blast radius  
- Jumping to LFG/clone in the same message as first completion  
- Whole-repo redundancy claims on a single-file target without saying scale is wrong
