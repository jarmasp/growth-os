# Phase 3: Habits & Resources - Context

**Gathered:** 2026-04-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Embed deliberate practice routines and curated domain resources into the daily workflow.
After this phase: the ticket reflection template has a real pre-mortem section and assumption
log (not just placeholders), a standalone homework log tracks all recurring drills, and every
domain has a reading queue with an active book and resource notes in 40-resources/.

This phase does NOT run the practices repeatedly — it installs them. The system is set up so
Jose runs the pre-mortem on one real ticket to confirm it works, and the recurring drill tasks
are created and scheduled. Ongoing execution happens every sprint/week thereafter.
</domain>

<decisions>
## Implementation Decisions

### Pre-mortem Section (ticket-reflection.md)

- **D-01:** Replace the placeholder comment with a real `## Pre-mortem` section using a
  `[!question]` callout block — consistent with all other template sections (Phase 1 D-05).
  Position: FIRST in the template, before `## What Was Hard` — the pre-mortem runs before
  coding, not after.
  Format:
  ```markdown
  ## Pre-mortem

  > [!question] ¿Cuál es el contexto del negocio?
  > ¿Cuáles son los 3 puntos de falla más probables?
  > ¿Qué patrón de diseño aplica?
  ```
  This satisfies PRAC-01: business context + 3 failure points + design pattern named.

### Assumption Logging (ticket-reflection.md, PRAC-05)

- **D-02:** Add an `## Assumptions` section to ticket-reflection.md (for ambiguous tickets only).
  Same callout style. Position: after `## Pre-mortem`, before `## What Was Hard`.
  Format:
  ```markdown
  ## Assumptions

  > [!question] Para tickets ambiguos: ¿Qué estás asumiendo? ¿Qué pasa si estás equivocado?
  ```
  Contents: 2-5 explicit statements in format "Estoy asumiendo X porque Y. Si estoy mal: [consecuencia]."

### Homework Log Location

- **D-03:** Standalone note at `Cashea/homework-log.md` (vault root level, not inside a subfolder).
  NOT inside weekly review — the log persists across weeks, tasks carry forward until done.
  Structure: `## Recurring Drills` section + `## One-off Tasks` section.
  Uses Tasks plugin statuses: `[ ]` pending, `[/]` in-progress, `[x]` done.
  Recurring drills use 🔁 emoji + schedule (e.g., "🔁 every sprint") per Phase 1 D-12
  (Tasks plugin configured with custom statuses).

### Recurring Drills Initial Content

- **D-04:** Three recurring tasks seeded at creation:
  - `- [ ] PR rewrite drill — 🔁 once per sprint` (PRAC-02)
  - `- [ ] Naked system design (Excalidraw) — 🔁 every 2 weeks` (PRAC-03)
  - `- [ ] One-concept deepening (20 min) — 🔁 weekly` (PRAC-04)
  One-off task seeded: `- [ ] Run pre-mortem on a real ticket` (confirms PRAC-01 works in under 10 min).

### Domain Queue Structure in 40-resources/

- **D-05:** Both: one index file per domain + individual resource notes per book.
  - Index files: `40-resources/{domain}-queue.md` (e.g., `coding-patterns-queue.md`)
    Shows: Active book (currently reading), Queue (priority order), Done
  - Individual resource notes: one per book, using the existing `learning-resource.md` template
    Linked from the domain queue index AND from relevant concept articles' `## Resources to Go Deeper`

### Book Selections (active book first in each queue)

- **D-06:** Coding patterns queue:
  1. *Designing Data-Intensive Applications* — Martin Kleppmann (active)
  2. *A Philosophy of Software Design* — John Ousterhout
  3. *Clean Code / Clean Architecture* — Robert Martin

- **D-07:** System design queue (DDIA is in coding patterns):
  1. *System Design Interview Vol 1* — Alex Xu (active)
  2. *Building Microservices* — Sam Newman

- **D-08:** GCP/Infra queue:
  1. *Official Google Cloud ACE Study Guide* (active — certification path)
  2. *Site Reliability Engineering* — Google SRE Book (free online)
  3. *Google Cloud Platform in Action* — JJ Geewax

- **D-09:** DevOps queue (Claude's recommendation — Jose deferred):
  1. *Accelerate* — Forsgren, Humble, Kim (active — short, research-backed, DORA metrics)
  2. *The DevOps Handbook* — Kim et al. (practical companion)
  3. *The Phoenix Project* — Kim, Behr, Spafford (mental model, novel format)

- **D-10:** Observability queue (Claude's recommendation):
  1. *Distributed Systems Observability* — Cindy Sridharan (active — free online, foundational)
  2. *Observability Engineering* — Charity Majors, Liz Fong-Jones (comprehensive follow-up)

- **D-11:** Communication queue (Claude's recommendation):
  1. *On Writing Well* — William Zinsser (active — PR descriptions, tickets, technical docs)
  2. *The Pyramid Principle* — Barbara Minto (structured thinking for upward communication)

### Podcast/Video Recommendations

- **D-12:** Claude's discretion — top 3 per domain (podcast + video mix), linked from the
  relevant MOC file. Curated during planning/execution based on domain context.

### Resource Note Linking

- **D-13:** When resource notes are created for each book, also update the `## Resources to Go Deeper`
  section of the most relevant concept articles in `10-concepts/` (Phase 2 left these as empty
  callout prompts). One resource per article minimum — fulfills the deferred Phase 2 work.

### Claude's Discretion

- Exact podcast and video titles per domain (top 3 each)
- Which specific concept articles to seed with each book resource link (beyond the obvious ones)
- Domain index file prose descriptions (brief — navigation, not content)
- Exact frontmatter values for resource notes (domain tag choices)
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — LRNG-01 (domain queues), LRNG-02 (podcast/video), LRNG-03
  (homework log), LRNG-04 (resource notes), PRAC-01 (pre-mortem), PRAC-02 (PR rewrite),
  PRAC-03 (naked system design), PRAC-04 (one-concept deepening), PRAC-05 (assumption logging)

### Phase 1 Decisions (carry-forward)
- `.planning/phases/01-vault-foundation/01-CONTEXT.md` — D-05/D-06 (callout block template style,
  Spanish guiding questions), D-07 (ticket reflection template sections and pre-mortem placeholder),
  D-08 (concept article template with `## Resources to Go Deeper`), D-12 (Tasks plugin custom
  statuses), D-18 (vault folder structure — `40-resources/` path)

### Phase 2 Decisions (carry-forward)
- `.planning/phases/02-knowledge-seed/02-CONTEXT.md` — D-07 (`## Resources to Go Deeper` left
  empty in Phase 2, filled in Phase 3)

### Project Context
- `.planning/PROJECT.md` — 6 domain names, constraints, vault path, Jose's profile

### Vault Templates (read before modifying)
- `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md`
  — current state of the template being modified (pre-mortem placeholder is a comment, not a section)
- `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/learning-resource.md`
  — existing resource note template structure (has: date, tags, type, author, url frontmatter;
  Why This Resource, What It Covers, Key Takeaways, Concepts This Deepened, Rating sections)

No external specs or ADRs — all requirements captured in the files above.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `ticket-reflection.md` template — exists, has Pre-mortem as a comment placeholder and
  Assumptions not yet present. D-01 and D-02 modify this file.
- `learning-resource.md` template — exists with full structure. D-05 resource notes use this.
- `40-resources/` folder — exists but empty. Phase 3 populates it.
- Tasks plugin — already installed and configured (Phase 1 D-12) with `[/]` in-progress,
  `[-]` cancelled custom statuses. homework-log.md will use these.

### Established Patterns
- Template sections: `## Header` + `> [!question] Spanish prompt` callout block
- File naming: slug format in English (`on-writing-well.md`, `system-design-interview.md`)
- Frontmatter: `date`, `tags: [#resource, #to-read]`, `type: book`, `author:`, `url:`
- Wikilinks: `[[slug]]` or `[[slug|Display Name]]`

### Integration Points
- Vault path: `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/`
- ticket-reflection.md: `99-templates/ticket-reflection.md` (modify in place)
- New homework log: `Cashea/homework-log.md`
- Domain queue indices: `Cashea/40-resources/{domain}-queue.md` (create 6 files)
- Individual resource notes: `Cashea/40-resources/{book-slug}.md` (one per book)
- MOC files for podcast/video linking: `Cashea/50-mocs/MOC-{Domain}.md`
- Concept articles for resource seeding: `Cashea/10-concepts/` subdirectories
</code_context>

<specifics>
## Specific Ideas

- Pre-mortem goes FIRST in the ticket reflection template — it's a before-coding ritual,
  not an after-action review. Current placeholder is a comment; this becomes a real section.
- Homework log is standalone, not embedded in weekly review — it persists across weeks,
  tasks carry over. The weekly review can Dataview-query the homework log, but the log
  itself doesn't reset.
- DDIA (Designing Data-Intensive Applications) anchors the coding patterns queue — José
  confirmed this explicitly. It is NOT in the system design queue (to avoid duplication).
- For domains where José has low familiarity (DevOps, observability, communication), Claude
  makes the selection — José trusts the picks.
</specifics>

<deferred>
## Deferred Ideas

- Filling ALL concept articles' `## Resources to Go Deeper` sections comprehensively —
  Phase 3 seeds the most obviously linked ones, full curation is ongoing (moment of felt need)
- Podcast/video consumption tracking beyond the initial recommendation notes — future enhancement
- QuickAdd, Advanced URI, Obsidian Spaced Repetition — v2 requirements (carried from prior phases)

None added during this discussion — stayed within Phase 3 scope.
</deferred>

---

*Phase: 03-habits-resources*
*Context gathered: 2026-04-13*
