# Phase 3: Habits & Resources — Research

**Researched:** 2026-04-13
**Domain:** Obsidian vault — Markdown note authoring, Templates, Tasks plugin, resource curation
**Confidence:** HIGH (all findings from direct vault inspection + Tasks plugin source)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-01:** Replace the `<!-- Pre-mortem: placeholder -->` comment in `ticket-reflection.md` with a real
`## Pre-mortem` section using a `[!question]` callout block. Position: FIRST in template, before
`## What Was Hard`. Format:
```markdown
## Pre-mortem

> [!question] ¿Cuál es el contexto del negocio?
> ¿Cuáles son los 3 puntos de falla más probables?
> ¿Qué patrón de diseño aplica?
```

**D-02:** Add `## Assumptions` section to `ticket-reflection.md` (for ambiguous tickets only).
Position: after `## Pre-mortem`, before `## What Was Hard`. Format:
```markdown
## Assumptions

> [!question] Para tickets ambiguos: ¿Qué estás asumiendo? ¿Qué pasa si estás equivocado?
```
Contents: 2-5 explicit statements "Estoy asumiendo X porque Y. Si estoy mal: [consecuencia]."

**D-03:** Standalone note at `Cashea/homework-log.md` (vault root, not inside subfolder).
Structure: `## Recurring Drills` + `## One-off Tasks`. Uses Tasks plugin statuses: `[ ]`, `[/]`, `[x]`.
Recurring drills use 🔁 emoji + schedule.

**D-04:** Three recurring tasks seeded:
- `- [ ] PR rewrite drill — 🔁 once per sprint` (PRAC-02)
- `- [ ] Naked system design (Excalidraw) — 🔁 every 2 weeks` (PRAC-03)
- `- [ ] One-concept deepening (20 min) — 🔁 weekly` (PRAC-04)
One-off task: `- [ ] Run pre-mortem on a real ticket`

**D-05:** Both domain queue index files AND individual resource notes per book.
- Index: `40-resources/{domain}-queue.md` (active book + queue + done)
- Individual notes: one per book using `learning-resource.md` template
- Linked from queue index AND from relevant concept articles' `## Resources to Go Deeper`

**D-06 – D-11:** Book queues per domain (locked — see below under Standard Stack).

**D-12:** Podcast/video — Claude's discretion, top 3 per domain, linked from MOC files.

**D-13:** When resource notes are created, also update `## Resources to Go Deeper` in the most
relevant concept articles (currently all have `(Phase 3 — leave empty)` placeholder).

### Claude's Discretion

- Exact podcast and video titles per domain (top 3 each)
- Which specific concept articles to seed with each book resource link (beyond obvious ones)
- Domain index file prose descriptions (brief — navigation, not content)
- Exact frontmatter values for resource notes (domain tag choices)

### Deferred Ideas (OUT OF SCOPE)

- Filling ALL concept articles' `## Resources to Go Deeper` sections comprehensively —
  Phase 3 seeds the most obviously linked ones; full curation is ongoing (moment of felt need)
- Podcast/video consumption tracking beyond the initial recommendation notes
- QuickAdd, Advanced URI, Obsidian Spaced Repetition — v2 requirements
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| LRNG-01 | Domain reading queue per domain (6 domains), books in priority order, one active | D-05/D-06–D-11 locked; queue index files go in `40-resources/`; structure verified |
| LRNG-02 | Podcast and video recommendations per domain (top 3 each), linked from resources notes in `40-resources/` | D-12 Claude's discretion; podcast/video recommendations researched and listed below |
| LRNG-03 | Homework log in Obsidian with Tasks plugin tracking (`[ ]`, `[/]`, `[x]`) | D-03 locked; `homework-log.md` at vault root; Tasks plugin confirmed configured with these statuses |
| LRNG-04 | Resource Obsidian notes for all initial book recommendations (title, author, domain, why relevant, concept article links) | `learning-resource.md` template verified — has all required frontmatter fields |
| PRAC-01 | Pre-mortem habit established — ticket reflection has business context + 3 failure points + design pattern | D-01 locked; `ticket-reflection.md` current state confirmed (placeholder comment only) |
| PRAC-02 | PR rewrite drill — once per sprint, as recurring homework task | D-04 locked; homework-log.md task seeded |
| PRAC-03 | Naked system design — biweekly Excalidraw, homework task | D-04 locked; homework-log.md task seeded |
| PRAC-04 | One-concept deepening — 20 min weekly, homework task | D-04 locked; homework-log.md task seeded |
| PRAC-05 | Assumption logging — `## Assumptions` section in ticket reflection for ambiguous tickets | D-02 locked; section design confirmed |
</phase_requirements>

---

## Summary

Phase 3 is a file-creation and file-modification phase entirely within the Obsidian vault at
`/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/`. There is no code, no npm
packages, no build steps — everything is Markdown authoring.

The phase has three work tracks: (1) modify `ticket-reflection.md` to add real `## Pre-mortem`
and `## Assumptions` sections (replacing the comment placeholder), (2) create `homework-log.md`
with seeded recurring drill tasks, and (3) populate `40-resources/` with 6 domain queue index
files + individual resource notes for every book, then backfill the `## Resources to Go Deeper`
sections in the most relevant concept articles.

All structural decisions are locked in CONTEXT.md. The main open areas for Claude's discretion
are: exact podcast/video picks per domain (researched and documented below), and which concept
articles to seed with each book link (mapped below).

**Primary recommendation:** Execute the three plans in order — templates first (PRAC-01/05),
then homework log (PRAC-02/03/04), then resources (LRNG-01/02/03/04) — so the practice
infrastructure exists before the resources are linked.

---

## Current State of Files to Modify

### `ticket-reflection.md` (CONFIRMED — must modify)

Current content (read directly):

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
ticket:
branch:
status: resolved
tags: [ticket]
---

# <% tp.file.title %>

<!-- Pre-mortem: placeholder for Phase 3 habit. Add before coding, not after. -->

## What Was Hard
> [!question] ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?

## What I Learned
> [!question] ¿Qué aprendí hoy? ¿Qué patrón usé o descubrí?

## Concepts Encountered
> [!question] ¿Qué conceptos aparecieron? Agrega wikilinks a los artículos correspondientes.
- [[]]

## What I'd Do Differently
> [!question] Si lo hiciera de nuevo, ¿qué cambiaría?
```

Required change: remove the HTML comment and add `## Pre-mortem` + `## Assumptions` before
`## What Was Hard`. Final section order:
1. `## Pre-mortem` (D-01)
2. `## Assumptions` (D-02)
3. `## What Was Hard`
4. `## What I Learned`
5. `## Concepts Encountered`
6. `## What I'd Do Differently`

### `learning-resource.md` (CONFIRMED — use as-is, no modification needed)

Template has: frontmatter (`date`, `tags: [resource, to-read]`, `type`, `author`, `url`),
then sections: `## Why This Resource`, `## What It Covers`, `## Key Takeaways`,
`## Concepts This Deepened`, `## Rating`. Full structure confirmed from direct read.
Resource notes created in Plan 03-01 will instantiate this template (not modify it).

### `40-resources/` folder (CONFIRMED — empty, ready to populate)

Confirmed empty. Phase 3 creates all content here.

### `homework-log.md` (CONFIRMED — does not exist yet)

Does not exist at vault root or anywhere in vault. Plan 03-02 creates it.

### `## Resources to Go Deeper` in concept articles (CONFIRMED — all have placeholder)

Every concept article inspected has this identical placeholder:
```markdown
## Resources to Go Deeper

> [!question] ¿Qué recurso leería si necesitara entender esto más profundo?

(Phase 3 — leave empty)
```
Plan 03-01 replaces `(Phase 3 — leave empty)` with a wikilink to the relevant resource note
in the most obviously linked articles (one resource per article minimum per D-13).

---

## Standard Stack

### Core: Locked Book Selections (from CONTEXT.md D-06 – D-11)

| Domain | File slug | Active Book | Queue |
|--------|-----------|-------------|-------|
| coding-patterns | `coding-patterns-queue.md` | *Designing Data-Intensive Applications* — Kleppmann | A Philosophy of Software Design; Clean Code/Architecture |
| system-design | `system-design-queue.md` | *System Design Interview Vol 1* — Alex Xu | Building Microservices |
| gcp-infra | `gcp-infra-queue.md` | *Official Google Cloud ACE Study Guide* | SRE Book (free); GCP in Action — Geewax |
| devops | `devops-queue.md` | *Accelerate* — Forsgren, Humble, Kim | DevOps Handbook; The Phoenix Project |
| observability | `observability-queue.md` | *Distributed Systems Observability* — Cindy Sridharan (free) | Observability Engineering — Majors, Fong-Jones |
| communication | `communication-queue.md` | *On Writing Well* — Zinsser | The Pyramid Principle — Minto |

### Core: Individual Resource Note Slugs

| Book | File slug | Domain tag |
|------|-----------|------------|
| Designing Data-Intensive Applications | `designing-data-intensive-applications.md` | #coding-patterns |
| A Philosophy of Software Design | `a-philosophy-of-software-design.md` | #coding-patterns |
| Clean Code | `clean-code.md` | #coding-patterns |
| System Design Interview Vol 1 | `system-design-interview-vol-1.md` | #system-design |
| Building Microservices | `building-microservices.md` | #system-design |
| Google Cloud ACE Study Guide | `google-cloud-ace-study-guide.md` | #gcp-infra |
| Site Reliability Engineering | `site-reliability-engineering.md` | #gcp-infra |
| Google Cloud Platform in Action | `google-cloud-platform-in-action.md` | #gcp-infra |
| Accelerate | `accelerate.md` | #devops |
| The DevOps Handbook | `the-devops-handbook.md` | #devops |
| The Phoenix Project | `the-phoenix-project.md` | #devops |
| Distributed Systems Observability | `distributed-systems-observability.md` | #observability |
| Observability Engineering | `observability-engineering.md` | #observability |
| On Writing Well | `on-writing-well.md` | #communication |
| The Pyramid Principle | `the-pyramid-principle.md` | #communication |

**Total resource notes to create: 15**

---

## Architecture Patterns

### Vault File Naming

Established pattern (confirmed from Phase 1 D-04 and actual vault files):
- Slug format in English: `designing-data-intensive-applications.md`
- No spaces, no capital letters, hyphens as separators
- Domain queue index files: `{domain}-queue.md` (hyphenated, no number prefix)
- Homework log: `homework-log.md` (flat at vault root, not in a subfolder)

### Template Section Style (carry-forward from Phase 1 D-05/D-06)

```markdown
## Section Name

> [!question] ¿Guiding question in Spanish?
```

One or two questions per section. Questions help start writing; they do not pad.

### Domain Queue Index Structure

Each `{domain}-queue.md` file follows this pattern:

```markdown
---
date: 2026-04-13
tags: [resource, {domain-tag}]
---

# {Domain} Reading Queue

## Active (reading now)

- [[{book-slug}|{Title}]] — {Author}

## Queue (next in order)

1. [[{book-slug}|{Title}]] — {Author}
2. [[{book-slug}|{Title}]] — {Author}

## Done

*(none yet)*

## Podcasts & Videos

- {Podcast or Channel name} — {brief reason / what it covers}
- {Podcast or Channel name} — {brief reason / what it covers}
- {Podcast or Channel name} — {brief reason / what it covers}
```

Note: The queue index file is the navigation layer. Individual resource notes (from
`learning-resource.md` template) hold the detail. The index wikilinks to each note slug.

### Individual Resource Note Structure (from `learning-resource.md` template — confirmed)

```markdown
---
date: 2026-04-13
tags: [resource, to-read]
type: book
author: {Author Name}
url: {URL if available}
---

# {Book Title}

## Why This Resource

> [!question] ¿Qué gap o ticket llevó a este recurso?

Surfaced by: [[{concept-article-slug}]]

## What It Covers

- {bullet 1}
- {bullet 2}

## Key Takeaways

*(Fill after consuming)*

## Concepts This Deepened

- [[{concept-article-slug}]]

## Rating

/5 —
```

### Homework Log Structure

```markdown
---
date: 2026-04-13
tags: [homework]
---

# Homework Log

Persistent task backlog for deliberate practice drills. Tasks carry forward across weeks
until done. Weekly review can Dataview-query this file for open tasks.

## Recurring Drills

- [ ] PR rewrite drill — 🔁 once per sprint
- [ ] Naked system design (Excalidraw) — 🔁 every 2 weeks
- [ ] One-concept deepening (20 min) — 🔁 weekly

## One-off Tasks

- [ ] Run pre-mortem on a real ticket
```

### Updated `ticket-reflection.md` (final state after Plan 03-03)

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
ticket:
branch:
status: resolved
tags: [ticket]
---

# <% tp.file.title %>

## Pre-mortem

> [!question] ¿Cuál es el contexto del negocio?
> ¿Cuáles son los 3 puntos de falla más probables?
> ¿Qué patrón de diseño aplica?

## Assumptions

> [!question] Para tickets ambiguos: ¿Qué estás asumiendo? ¿Qué pasa si estás equivocado?

## What Was Hard

> [!question] ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?

## What I Learned

> [!question] ¿Qué aprendí hoy? ¿Qué patrón usé o descubrí?

## Concepts Encountered

> [!question] ¿Qué conceptos aparecieron? Agrega wikilinks a los artículos correspondientes.

- [[]]

## What I'd Do Differently

> [!question] Si lo hiciera de nuevo, ¿qué cambiaría?
```

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Recurring task scheduling | Custom cron or separate tracker | Tasks plugin `🔁 every X` syntax | Plugin already installed (confirmed in `.obsidian/plugins/`); native integration with Obsidian checkboxes |
| Reading list tracking | Separate spreadsheet or Notion page | Domain queue index files + Dataview | Already in vault, queryable, linked to concept graph |
| Resource note metadata | Free-form prose | `learning-resource.md` template | Template exists with correct frontmatter fields; consistent with all other note types |

**Key insight:** Everything needed already exists in the vault. Phase 3 is configuration and
content, not infrastructure. Introducing any new plugin or external tool would violate the
Phase 1 decision to freeze vault structure for 8 weeks.

---

## Tasks Plugin: Recurring Task Syntax

**Confirmed from plugin source and web research (HIGH confidence):**

The Tasks plugin uses the `🔁` emoji prefix in the `tasksPluginEmoji` format (confirmed as
active format from `data.json: "taskFormat": "tasksPluginEmoji"`).

Native recurring syntax: `🔁 every week`, `🔁 every 2 weeks`, `🔁 every day`

However, D-04 in CONTEXT.md specifies a **plain-text label approach** (not native Tasks
recurrence rules): `- [ ] PR rewrite drill — 🔁 once per sprint`. This is intentional — it
uses the emoji as a visual cue without triggering the Tasks plugin's automated date-advancing
behavior (which requires a due date to work). Without a `📅` due date, the `🔁` is decorative
only. This is the correct approach for the homework log — the drills are not calendar-bound;
they're intent-based.

**Implementation note for Plan 03-02:** Use the D-04 format exactly — emoji as label, not as
Tasks plugin recurrence directive. If Jose later wants automated recurrence, a due date must
be added per Tasks plugin requirements. That is out of scope for Phase 3.

---

## Podcast & Video Recommendations (Claude's Discretion — D-12)

Top 3 per domain. Format for inclusion in each domain queue index file and as a standalone
note or inline section. Confidence: MEDIUM (based on ecosystem knowledge; content is current
as of April 2026 but podcast episodes vary).

### Coding Patterns

1. **Thoughtworks Technology Podcast** (podcast) — Architecture and design patterns from
   practitioners. Episodes on hexagonal architecture, domain modeling, and evolutionary
   design align directly with cashea-backend's pattern set.
2. **CoRecursive: Coding Stories** (podcast) — Long-form interviews on system design
   decisions in production. Episodes with Gary Bernhardt, Rich Hickey on simplicity vs.
   complexity are directly relevant.
3. **GOTO Conferences YouTube** (video) — Talks by Alistair Cockburn (hexagonal architecture
   originator), Sam Newman (microservices), and Martin Fowler. Free, authoritative, directly
   relevant to DDIA and A Philosophy of Software Design themes.

### System Design

1. **System Design Interview (Alex Xu YouTube channel)** (video) — Direct companion to the
   active book (System Design Interview Vol 1). Visual walkthroughs of the same cases in the
   book.
2. **ByteByteGo Newsletter / YouTube** (video) — Weekly system design deep-dives by Alex Xu.
   Covers distributed systems, database choices, caching layers. Directly extends the book.
3. **Software Engineering Daily — System Design episodes** (podcast) — 30-45 min interviews
   on real-world system design decisions. Episodes on pub/sub, CDN, API gateways align with
   cashea-backend's GCP stack.

### GCP / Infra

1. **Google Cloud YouTube — "Google Cloud Next" talks** (video) — Official GCP content.
   Cloud Run, Pub/Sub, Secret Manager deep-dives. ACE exam prep material is embedded in these
   talks alongside production use cases.
2. **Rawkode Academy (YouTube)** (video) — Cloud-native and Kubernetes content. Strong
   Cloud Run and GCP-native content, clear explanations without vendor marketing overlay.
3. **Cloud Native Computing Foundation (CNCF) Webinars** (video) — Covers OpenTelemetry,
   service mesh, observability — connects GCP infra to the observability domain.

### DevOps

1. **DevOps Paradox (podcast)** (podcast) — Practical DevOps conversations. DORA metrics,
   deployment frequency, lead time — maps directly to *Accelerate* concepts.
2. **The Changelog: Ship It!** (podcast) — Engineering culture and delivery practices.
   Covers CD pipelines, incident response, on-call culture.
3. **Continuous Delivery Foundation (CDF) YouTube** (video) — CI/CD best practices.
   Pipeline architecture, progressive delivery, feature flags. Complements *DevOps Handbook*.

### Observability

1. **o11ycast (podcast)** — Charity Majors, Liz Fong-Jones, and co-authors of the active
   books both appear. Episodes on structured logging, tracing, and cardinality are foundational.
2. **OpenTelemetry Community YouTube** (video) — Official OTel channel. Covers instrumentation
   in Node.js/TypeScript (directly applicable to NestJS + cashea-backend's Pino setup).
3. **Honeycomb.io Blog talks (YouTube)** (video) — Charity Majors' talks on observability
   engineering. Directly extends both active books in the observability queue.

### Communication

1. **Writing With Flair (YouTube / Udemy)** (video) — Shani Raja's writing course.
   Precise, clear writing for professionals. Directly complements *On Writing Well*.
2. **Patrick McKenzie (patio11) blog / Twitter threads** — Not a podcast, but the best
   practitioner example of clear technical + business writing for engineers. PR descriptions
   and ticket writing anchors.
3. **Technical Writing Podcast (Write the Docs)** (podcast) — Community podcast on
   technical documentation. API docs, architecture docs, ADRs — all directly relevant to
   Jose's communication gap.

---

## Concept Article → Resource Note Mapping (D-13)

Which concept articles get their `## Resources to Go Deeper` backfilled in Plan 03-01.
One resource link minimum per article seeded. Articles with `(Phase 3 — leave empty)` placeholder.

**All 10 full articles confirmed to have the placeholder. Stubs do NOT have `## Resources to Go Deeper`
(stubs only have `## What It Is` + `## Related Concepts` per Phase 2 D-01).**

| Concept Article | Resource Note to Link | Rationale |
|----------------|----------------------|-----------|
| `hexagonal-architecture.md` | `a-philosophy-of-software-design.md` | APSD ch. 4-8 directly addresses module boundaries and ports |
| `typeorm-repository-pattern.md` | `designing-data-intensive-applications.md` | DDIA ch. 2-3 (data models, storage engines) backs the pattern |
| `nestjs-guards.md` | `designing-data-intensive-applications.md` | DDIA is the deepening resource for backend architecture generally |
| `nestjs-interceptors.md` | `designing-data-intensive-applications.md` | Same — cross-cutting concerns in distributed systems |
| `gcp-pubsub.md` | `designing-data-intensive-applications.md` | DDIA ch. 11 (stream processing) is canonical for Pub/Sub patterns |
| `jwt-authentication.md` | `designing-data-intensive-applications.md` | DDIA ch. 9 (consistency + distributed state) covers stateless auth tradeoffs |
| `rbac-permissions.md` | `designing-data-intensive-applications.md` | DDIA ch. 9 covers identity and access in distributed systems |
| `session-guard-pattern.md` | `system-design-interview-vol-1.md` | SDI ch. 4 (rate limiter) + ch. 10 (notification system) cover session patterns |
| `apigee.md` | `system-design-interview-vol-1.md` | SDI ch. 1 (scale from zero) + API gateway chapter |
| `structured-logging.md` | `distributed-systems-observability.md` | The active observability book is the canonical resource here |

**Note:** `clean-code.md` and `the-phoenix-project.md` are not linked from concept articles on
first pass — they're in the queue but less directly mappable to specific existing articles.

---

## Common Pitfalls

### Pitfall 1: Overwriting `ticket-reflection.md` instead of inserting sections

**What goes wrong:** The file is rewritten from scratch, losing the Templater syntax
(`<% tp.date.now("YYYY-MM-DD") %>`, `<% tp.file.title %>`).
**Why it happens:** Edit tools that replace the full file content without preserving frontmatter tags.
**How to avoid:** Use the Edit tool with precise insertion targeting. Verify Templater variables
survive the edit. The correct action is: delete the HTML comment line and insert the two new
sections above `## What Was Hard`.
**Warning signs:** After edit, run a grep for `tp.date.now` — if missing, the file was overwritten.

### Pitfall 2: Using Tasks plugin native recurrence syntax (requires a due date)

**What goes wrong:** Writing `- [ ] PR rewrite drill 🔁 every 2 weeks` without a `📅` date
triggers Tasks plugin behavior — it will try to compute next occurrence but fail silently
because no due date is set.
**Why it happens:** Misreading D-04 as "use Tasks plugin recurrence" rather than "use emoji
as a label."
**How to avoid:** Use the exact D-04 format with ` — 🔁` as a plain text label, not as a
Tasks plugin recurrence directive. No `📅` date in the initial seeded tasks.
**Warning signs:** If a due date appears anywhere in the homework log initial content, it
was added incorrectly.

### Pitfall 3: Creating resource notes without frontmatter `author:` and `url:` fields

**What goes wrong:** Resource notes created with only `tags`, `date`, `type` — missing
`author:` and `url:` fields that `learning-resource.md` template defines.
**Why it happens:** Manually writing frontmatter instead of following the template exactly.
**How to avoid:** Always include all frontmatter keys from `learning-resource.md`, even if
`url:` is empty for books without a free URL.
**Warning signs:** grep for `author:` in all `40-resources/*.md` files — any missing triggers review.

### Pitfall 4: Linking concept articles with slug mismatches

**What goes wrong:** `## Resources to Go Deeper` section links `[[DDIA]]` instead of
`[[designing-data-intensive-applications]]`, producing a broken wikilink in Obsidian.
**Why it happens:** Using abbreviated names instead of the exact file slug.
**How to avoid:** All wikilinks must use the exact filename slug (no `.md` extension).
**Warning signs:** Obsidian will show broken link highlighting; grep for `[[DDIA` or
similar abbreviations in the resources folder.

### Pitfall 5: Placing `homework-log.md` inside a subfolder

**What goes wrong:** File created at `Cashea/30-weekly/homework-log.md` or similar, rather
than `Cashea/homework-log.md` at vault root.
**Why it happens:** Defaulting to numbered folder conventions from D-18.
**How to avoid:** D-03 explicitly locks this to vault root level. The point is persistence
across weeks — it does NOT live in `30-weekly/`.
**Warning signs:** Verify path is `Personal/Cashea/homework-log.md`, NOT inside any subfolder.

---

## MOC Files: Podcast/Video Linking (D-12)

The podcast/video recommendations go in the domain queue index files (`40-resources/`) as a
`## Podcasts & Videos` section. They do NOT require new notes — they are a curated list
section within the domain queue index.

CONTEXT.md D-12 says "linked from the relevant MOC file." However, the MOC files currently
contain only concept article links and Dataview queries. The cleanest implementation is:

**Option A (minimal change):** Add a `## Resources` link to the domain queue file in each
MOC (one line per MOC: `[[coding-patterns-queue|Coding Patterns Reading Queue]]`). The
podcast list lives in the queue file.

**Option B (MOC modification):** Add a `## Podcasts & Videos` section to each MOC directly.

Option A is recommended: it keeps MOCs as navigation-only files (consistent with D-03 from
Phase 1: "MOC files and tag taxonomy use English — they're navigation infrastructure") and
puts content in the resources folder where it belongs.

---

## Environment Availability

Step 2.6: SKIPPED (no external dependencies — this phase is Markdown file creation and
modification only, within an already-configured Obsidian vault).

All vault infrastructure confirmed present:
- Obsidian plugins installed: `obsidian-tasks-plugin`, `templater-obsidian`, `dataview` (verified by directory listing)
- `40-resources/` folder exists (empty, ready)
- `99-templates/learning-resource.md` exists with correct structure
- `99-templates/ticket-reflection.md` exists with placeholder to replace

---

## Validation Architecture

`nyquist_validation: true` in config.json — validation section required.

This phase has no test framework (it is Obsidian Markdown, not code). Validation is
performed via shell file and content checks. These commands are designed to run from the
macOS terminal after all three plans complete.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Shell grep + file existence checks (no test runner) |
| Config file | None — ad hoc commands listed below |
| Quick run command | See per-plan checks below |
| Full suite command | Run all checks listed in "Phase Gate" section |

### Phase Requirements → Validation Map

| Req ID | Behavior | Check Type | Command |
|--------|----------|-----------|---------|
| PRAC-01 | `## Pre-mortem` section in ticket-reflection.md | grep content | `grep -c "## Pre-mortem" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → expect `1` |
| PRAC-01 | Pre-mortem callout block present | grep content | `grep -c "\[!question\] ¿Cuál es el contexto del negocio?" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → expect `1` |
| PRAC-01 | Pre-mortem is BEFORE What Was Hard | section order | `grep -n "## Pre-mortem\|## What Was Hard" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → Pre-mortem line number must be lower |
| PRAC-05 | `## Assumptions` section present | grep content | `grep -c "## Assumptions" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → expect `1` |
| PRAC-05 | Old placeholder comment removed | grep absent | `grep -c "placeholder for Phase 3" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → expect `0` |
| PRAC-05 | Assumptions is BEFORE What Was Hard | section order | `grep -n "## Assumptions\|## What Was Hard" "...ticket-reflection.md"` → Assumptions line < What Was Hard line |
| LRNG-03 | homework-log.md exists at vault root | file exists | `test -f "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/homework-log.md" && echo PASS` |
| PRAC-02 | PR rewrite drill task present | grep content | `grep -c "PR rewrite drill" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/homework-log.md"` → expect `1` |
| PRAC-03 | Naked system design task present | grep content | `grep -c "Naked system design" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/homework-log.md"` → expect `1` |
| PRAC-04 | One-concept deepening task present | grep content | `grep -c "One-concept deepening" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/homework-log.md"` → expect `1` |
| LRNG-03 | All homework tasks have pending status `[ ]` | grep format | `grep -c "- \[ \]" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/homework-log.md"` → expect `4` |
| LRNG-01 | All 6 domain queue files exist | file exists | `for f in coding-patterns-queue system-design-queue gcp-infra-queue devops-queue observability-queue communication-queue; do test -f "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/40-resources/${f}.md" && echo "PASS: $f" || echo "FAIL: $f"; done` |
| LRNG-04 | 15 resource note files created | file count | `ls "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/40-resources/" | grep -v "\-queue\.md" | wc -l` → expect `15` |
| LRNG-04 | All resource notes have `author:` in frontmatter | grep all files | `grep -rL "^author:" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/40-resources/"` → expect empty output (no files missing author) |
| LRNG-02 | Each domain queue file has podcast/video section | grep content | `for f in coding-patterns-queue system-design-queue gcp-infra-queue devops-queue observability-queue communication-queue; do grep -c "Podcasts\|Videos" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/40-resources/${f}.md" || echo "MISSING in $f"; done` → all expect `>0` |
| LRNG-01 | Each domain queue has `## Active` section | grep content | `for f in coding-patterns-queue system-design-queue gcp-infra-queue devops-queue observability-queue communication-queue; do grep -c "## Active" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/40-resources/${f}.md" || echo "MISSING in $f"; done` |
| D-13 | `## Resources to Go Deeper` in hexagonal-architecture.md no longer has placeholder | grep absent | `grep -c "Phase 3 — leave empty" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/system-design/hexagonal-architecture.md"` → expect `0` |
| D-13 | Resources sections in 10 full articles updated (not all — spot check) | grep absent | `grep -rn "Phase 3 — leave empty" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts/"` → expect ≤35 results (43 total articles, 10 full ones seeded in Phase 3, stubs untouched) |
| Templater | Templater variables survive ticket-reflection.md edit | grep present | `grep -c "tp.date.now\|tp.file.title" "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/99-templates/ticket-reflection.md"` → expect `2` |

### Per-Plan Quick Check Commands

**After Plan 03-03 (templates):**
```bash
VAULT="/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea"
grep -n "## Pre-mortem\|## Assumptions\|## What Was Hard\|placeholder for Phase 3" "$VAULT/99-templates/ticket-reflection.md"
# Expected: Pre-mortem and Assumptions appear; "placeholder for Phase 3" does NOT appear
```

**After Plan 03-02 (homework log):**
```bash
VAULT="/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea"
test -f "$VAULT/homework-log.md" && echo "FILE EXISTS" || echo "MISSING"
grep "- \[ \]" "$VAULT/homework-log.md"
# Expected: 4 tasks with [ ] status
```

**After Plan 03-01 (domain resources):**
```bash
VAULT="/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea"
ls "$VAULT/40-resources/" | wc -l
# Expected: 21 files (6 queue indexes + 15 resource notes)
grep -rn "Phase 3 — leave empty" "$VAULT/10-concepts/" | wc -l
# Expected: ≤35 (43 articles minus 8-10 seeded full articles)
```

### Phase Gate (run all before marking phase complete)

```bash
VAULT="/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea"
TREF="$VAULT/99-templates/ticket-reflection.md"

echo "=== PRAC-01/05: ticket-reflection.md ==="
grep -n "## Pre-mortem\|## Assumptions\|## What Was Hard" "$TREF"
echo "Placeholder removed (expect 0):"
grep -c "placeholder for Phase 3" "$TREF"
echo "Templater vars intact (expect 2):"
grep -c "tp.date.now\|tp.file.title" "$TREF"

echo "=== LRNG-03 / PRAC-02/03/04: homework-log.md ==="
test -f "$VAULT/homework-log.md" && echo "PASS: file exists" || echo "FAIL: missing"
grep "- \[ \]" "$VAULT/homework-log.md"

echo "=== LRNG-01: domain queue files ==="
for f in coding-patterns-queue system-design-queue gcp-infra-queue devops-queue observability-queue communication-queue; do
  test -f "$VAULT/40-resources/${f}.md" && echo "PASS: $f" || echo "FAIL: $f"
done

echo "=== LRNG-04: resource notes count ==="
ls "$VAULT/40-resources/" | grep -v "\-queue\.md" | wc -l
# expect 15

echo "=== LRNG-04: all resource notes have author: ==="
grep -rL "^author:" "$VAULT/40-resources/" && echo "FAIL: above files missing author" || echo "PASS: all have author"

echo "=== D-13: Resources to Go Deeper seeded ==="
grep -rn "Phase 3 — leave empty" "$VAULT/10-concepts/" | wc -l
# expect ≤35 (was 43, should be ~33 after seeding 10 full articles)
```

### Wave 0 Gaps

None — this phase creates Markdown files, not code. No test files or fixtures are needed.
Validation is purely shell-based file and content inspection, runnable immediately.

---

## Open Questions

1. **MOC linking strategy for podcasts/videos**
   - What we know: D-12 says "linked from the relevant MOC file"
   - What's unclear: Whether MOC modification (adding a `## Resources` section) or a single
     wikilink to the queue file is the correct interpretation
   - Recommendation: Use Option A (add one wikilink to the domain queue file in each MOC).
     This satisfies "linked from MOC" without modifying MOC structure. Planner should pick
     one and document it.

2. **`clean-code.md` vs `clean-architecture.md` — one note or two?**
   - What we know: D-06 says "*Clean Code / Clean Architecture* — Robert Martin" as one entry
   - What's unclear: Whether to create one note (`clean-code.md`) covering both books or
     two separate notes
   - Recommendation: One note (`clean-code.md`) with both titles in the body. They share an
     author and philosophy; splitting into two notes adds overhead with minimal benefit at
     this stage.

3. **Resource note `url:` values for free-online books**
   - What we know: *Distributed Systems Observability* (Cindy Sridharan) and *SRE Book*
     are free online
   - What's unclear: Which exact URLs to use
   - Recommendation:
     - *Distributed Systems Observability*: `https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/` (O'Reilly free read)
     - *SRE Book*: `https://sre.google/sre-book/table-of-contents/` (Google's free official version)

---

## Sources

### Primary (HIGH confidence)
- Direct vault file inspection — `ticket-reflection.md`, `learning-resource.md`, all 10 full
  concept articles, all 6 MOC files, `40-resources/` (empty), 5 plugin `data.json` files
- `.planning/phases/03-habits-resources/03-CONTEXT.md` — all implementation decisions locked

### Secondary (MEDIUM confidence)
- Tasks plugin `main.js` source — recurring task keywords (`every week`, `every 2 weeks`, `every month`)
- WebSearch: obsidian tasks plugin recurring syntax — confirmed `🔁` emoji + `every X` format;
  confirmed due date required for automated recurrence

### Tertiary (LOW confidence)
- Podcast/video recommendations — based on knowledge of ecosystem as of April 2026.
  Verify episodes are still active before adding to notes.

---

## Metadata

**Confidence breakdown:**
- File modification targets: HIGH — all files read directly, current state confirmed
- Tasks plugin format: HIGH — verified from plugin source + web research
- Book selections: HIGH — locked decisions from CONTEXT.md D-06–D-11
- Podcast/video picks: MEDIUM — ecosystem knowledge, verify currency
- Concept article → resource link mapping: MEDIUM — logical mapping, not user-validated

**Research date:** 2026-04-13
**Valid until:** 2026-05-13 (vault structure frozen; content stable for 30 days)
