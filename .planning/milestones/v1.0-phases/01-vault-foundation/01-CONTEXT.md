# Phase 1: Vault Foundation - Context

**Gathered:** 2026-04-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Scaffold the Obsidian vault with folder structure, plugins, templates, git sync, MOC files,
and two Claude Code skills (deslop, review-pr). After this phase, Jose can close a
cashea-backend ticket and write a complete reflection note in under 2 minutes — correct
structure, tags, and wikilinks — without making any structural decisions.

This phase does NOT write concept articles (Phase 2) or set up deliberate practice
habits (Phase 3). It builds the container everything else lives in.
</domain>

<decisions>
## Implementation Decisions

### Existing Notes Migration
- **D-01:** The 7 existing notes in `Personal/` root (Spanish, cashea-backend topics) are migrated
  into the new `Cashea/` folder structure as part of Phase 1. No wasted work — they become seed content.
  - Notes about specific features/guards → `20-tickets/` or `10-concepts/` depending on content
  - e.g. `Cashea — Employee Guard Mechanism.md` → `10-concepts/` (architectural concept)
  - e.g. `Suggest password change.md` → `20-tickets/` (feature/ticket reflection)
  - Preserve the original content; update with any missing frontmatter tags as part of migration

### Language Strategy
- **D-02:** Bilingual — section headers in **English** (consistent with PR descriptions, commits,
  upstream comms), guiding questions and callout prompts in **Spanish** (reflection comfort,
  matches Jose's existing writing style in the vault).
- **D-03:** MOC files and tag taxonomy use English (they're navigation infrastructure).
- **D-04:** File names use English with slug format: `nestjs-guards.md`, `employee-guard.md`.

### Template Prompt Style
- **D-05:** Templates use **Obsidian callout blocks with guiding questions** (not bare headers).
  Format per section:
  ```
  ## What Was Hard
  > [!question] ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?
  ```
  This makes sections visually distinct, hard to leave blank, and fast to start writing.
- **D-06:** Each section has **1-2 guiding questions** (in Spanish), not a full paragraph of prompts.
  Goal: writable in under 2 minutes — prompts help, they don't slow down.

### Ticket Reflection Template Structure
- **D-07:** Ticket reflection template sections (English headers, Spanish callout questions):
  1. `## Pre-mortem` (added in Phase 3 — placeholder comment only in Phase 1)
  2. `## What Was Hard` — ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?
  3. `## What I Learned` — ¿Qué aprendí hoy? ¿Qué patrón usé?
  4. `## Concepts Encountered` — (list of `[[wikilinks]]` to concept articles)
  5. `## What I'd Do Differently` — Si lo hiciera de nuevo, ¿qué cambiaría?
  - Frontmatter: `date`, `ticket`, `branch`, `status`, `tags: [#ticket, #domain]`

### Concept Article Template Structure
- **D-08:** Concept article template sections:
  1. `## What It Is` — ¿Qué es esto en una oración?
  2. `## How It Works` — ¿Cómo funciona internamente?
  3. `## How We Use It in cashea-backend` — ¿Dónde lo usamos? (code references ok here)
  4. `## Related Concepts` — (list of `[[wikilinks]]`)
  5. `## Resources to Go Deeper` — 1 official doc + 1 deep resource + 1 quick mental model
  6. `## Things to Learn / Reinforce` — #learning-gap items
  - Frontmatter: `date`, `tags: [#concept, #domain]`, `confidence: low|medium|high`

### Weekly Review Template Structure
- **D-09:** Weekly review uses **both** trend arrows AND numeric score per domain:
  ```
  | Domain | Score (1-5) | Trend | Note |
  |--------|-------------|-------|------|
  | Coding patterns | 3 | → | Stuck on hexagonal boundary violations |
  | System design | 2 | ↑ | Naked design exercise this week |
  | GCP / Infra | 2 | → | |
  | DevOps | 2 | → | |
  | Observability | 1 | → | |
  | Communication | 3 | ↑ | PR rewrite drill |
  ```
  Historical tracking (score) + quick visual signal (trend) in the same view.
- **D-10:** Weekly review Dataview queries auto-pull:
  - Tickets closed this week: `table ticket, date from "20-tickets" where date >= date(today) - dur(7 days)`
  - Learning gaps: `list from "10-concepts" where contains(tags, "#learning-gap")`
  - Resources to read: `list from "40-resources" where contains(tags, "#to-read")`
- **D-11:** Weekly review ends with mandatory **capability assertion**:
  ```
  ## Esta semana puedo
  > [!success] Puedo hacer X que antes no podía.
  ```
  If this can't be filled in, the learning approach needs to change.

### Plugin Configuration
- **D-12:** Plugin install order is strict (Templater first, before any notes are created):
  1. Templater → folder: `99-templates/`, auto-trigger on new file: enabled
  2. Dataview → JavaScript queries: enabled, auto-refresh: 500ms
  3. Tasks → custom statuses: `[/]` in-progress, `[-]` cancelled
  4. Obsidian Git → auto-backup: 30 min, auto-pull on startup: enabled
  5. Periodic Notes → weekly note folder: `30-weekly/`, format: `YYYY-[W]WW`
  6. Excalidraw → default: dark theme, save as .excalidraw.md
  7. Omnisearch → replace native search: enabled
  8. Linter → run on save: enabled, enforce frontmatter: enabled

### Vault Git Setup
- **D-13:** Vault git repo is a separate private GitHub repo named `cashea-knowledge-vault`.
  It must be created on GitHub manually BEFORE Plan 01-01 runs. The plan will `git init`
  and push to it — the remote must exist first.
- **D-14:** The vault repo is initialized at the vault root, NOT inside cashea-backend.
  Path: `/Users/thyfus/Documents/obsidian vaults/personal/` (the vault root, not `Personal/Cashea/`)

### Skills (Already Created)
- **D-15:** `deslop.md` exists at `.claude/get-shit-done/skills/deslop.md` — ready to use. No changes needed.
- **D-16:** `review-pr.md` exists at `.claude/get-shit-done/skills/review-pr.md` — cashea-backend specific
  (NestJS guards, hexagonal architecture, conventional commits, auth guard pattern). Ready to use.
- **D-17:** SKILL-03 (weekly skill retrospective) is a standing question in the weekly review template,
  not a separate skill file: "¿Qué se repitió esta semana que debería convertirse en skill o automatización?"

### Folder Structure
- **D-18:** Vault structure at `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/`:
  ```
  Cashea/
  ├── 00-inbox/         — quick captures, processed weekly
  ├── 10-concepts/      — permanent knowledge articles
  │   ├── backend/
  │   ├── infra/
  │   ├── system-design/
  │   └── security/
  ├── 20-tickets/       — ticket reflections (GROWTH-XXXX filenames)
  ├── 30-weekly/        — weekly reviews (YYYY-WNN format)
  ├── 40-resources/     — book/article/video metadata notes
  ├── 50-mocs/          — domain navigation index files
  └── 99-templates/     — Templater templates (never linked)
  ```

### Claude's Discretion
- Exact Dataview query syntax (test against real vault data during Phase 1)
- Linter rules specifics (enforce what already exists in the vault)
- Obsidian graph view color group configuration
- MOC file prose descriptions (brief — these are navigation, not content)
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — Full v1 requirement list with IDs (VAULT-01 to SKILL-03)

### Research
- `.planning/research/SUMMARY.md` — Synthesized findings: plugin stack, template patterns, vault architecture, pitfalls
- `.planning/research/ARCHITECTURE.md` — Vault folder structure, linking strategy, MOC patterns, tag taxonomy, Dataview query patterns

### Project Context
- `.planning/PROJECT.md` — Core value, constraints, design principles

No external specs or ADRs — all requirements captured in the files above.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- 7 existing notes at `/Users/thyfus/Documents/obsidian vaults/personal/Personal/` — Spanish,
  cashea-backend topics. Will be migrated into the new `Cashea/` structure as part of Phase 1.
  Good examples of existing note style to inform template design.
- `deslop.md` and `review-pr.md` skill files already exist in `.claude/get-shit-done/skills/`

### Established Patterns (from existing notes)
- Existing notes use: H1 title (Spanish), metadata block (Fecha/Rama/Estado), H2 sections with prose
- Notes are detailed and technical — templates should not over-constrain existing writing style
- Mix of architecture diagrams (text-based) and code snippets in existing notes

### Integration Points
- Vault root: `/Users/thyfus/Documents/obsidian vaults/personal/Personal/`
- New structure: `Cashea/` subfolder inside `Personal/`
- Skills: `.claude/get-shit-done/skills/` (already set up)
- GSD state: `.planning/STATE.md` (update after Phase 1 complete)
</code_context>

<specifics>
## Specific Ideas

- "Guiding questions and callouts" — Obsidian `[!question]` callout blocks inside each template section
  with 1-2 Spanish guiding questions. Not bare headers, not a wall of prompts.
- "Both trend arrows and score" — Weekly review table has both columns: Score (1-5) AND Trend (↑→↓).
  Historic tracking via score, quick signal via trend.
- Bilingual: English for infrastructure/navigation (file names, MOC titles, skill retrospective question in English),
  Spanish for reflection prompts inside templates.
</specifics>

<deferred>
## Deferred Ideas

- Breadcrumbs plugin (`parent:` frontmatter hierarchy) — evaluate in Phase 2 after vault has notes
- Advanced URI / VS Code integration — Phase 5 (advanced integrations milestone)
- Obsidian Spaced Repetition plugin — v2 requirement, defer until habit is stable
- Readwise Reader integration — v2 requirement

None — discussion stayed within Phase 1 scope.
</deferred>

---

*Phase: 01-vault-foundation*
*Context gathered: 2026-04-13*
