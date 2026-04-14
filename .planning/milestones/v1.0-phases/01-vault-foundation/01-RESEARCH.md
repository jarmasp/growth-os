# Phase 1: Vault Foundation - Research

**Researched:** 2026-04-13
**Domain:** Obsidian vault setup — folder structure, Templater templates, Dataview queries, Obsidian Git, MOC files
**Confidence:** HIGH (vault state verified live; plugin versions confirmed; syntax verified against official docs)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

- **D-01:** 7 existing notes in `Personal/` root migrate into `Cashea/` as part of Phase 1 (not discarded)
- **D-02:** Bilingual — section headers in English, guiding questions/prompts in Spanish
- **D-03:** MOC files and tag taxonomy use English
- **D-04:** File names use English slug format: `nestjs-guards.md`, `employee-guard.md`
- **D-05:** Templates use Obsidian callout blocks with guiding questions. Format: `## What Was Hard` / `> [!question] ¿Qué fue lo más difícil?`
- **D-06:** 1-2 guiding questions per section (Spanish), not a wall of prompts
- **D-07:** Ticket reflection sections: Pre-mortem placeholder, What Was Hard, What I Learned, Concepts Encountered, What I'd Do Differently. Frontmatter: `date`, `ticket`, `branch`, `status`, `tags`
- **D-08:** Concept article sections: What It Is, How It Works, How We Use It in cashea-backend, Related Concepts, Resources to Go Deeper, Things to Learn/Reinforce. Frontmatter: `date`, `tags`, `confidence`
- **D-09:** Weekly review uses both Score (1-5) AND Trend (↑→↓) in the same skill-domain table
- **D-10:** Weekly review Dataview queries: tickets this week, learning-gap concepts, to-read resources
- **D-11:** Weekly review ends with mandatory `## Esta semana puedo` capability assertion (`> [!success]`)
- **D-12:** Plugin install order is strict — Templater first, then Dataview, Tasks, Obsidian Git, Periodic Notes, Excalidraw, Omnisearch, Linter
- **D-13:** Vault git repo is a separate private GitHub repo named `cashea-knowledge-vault`. Must be created manually BEFORE git push plan runs.
- **D-14:** Git repo initialized at vault root `/Users/thyfus/Documents/obsidian vaults/personal/`, NOT inside cashea-backend
- **D-15:** `deslop.md` at `.claude/get-shit-done/skills/deslop.md` — ready, no changes needed
- **D-16:** `review-pr.md` at `.claude/get-shit-done/skills/review-pr.md` — ready, no changes needed
- **D-17:** SKILL-03 (weekly skill retrospective) is the standing question in weekly review template, not a separate file
- **D-18:** Vault structure at `Personal/Cashea/` with folders: 00-inbox, 10-concepts (with backend/infra/system-design/security subfolders), 20-tickets, 30-weekly, 40-resources, 50-mocs, 99-templates

### Claude's Discretion

- Exact Dataview query syntax (test against real vault data during Phase 1)
- Linter rules specifics (enforce what already exists in the vault)
- Obsidian graph view color group configuration
- MOC file prose descriptions (brief — these are navigation, not content)

### Deferred Ideas (OUT OF SCOPE)

- Breadcrumbs plugin (`parent:` frontmatter hierarchy)
- Advanced URI / VS Code integration
- Obsidian Spaced Repetition plugin
- Readwise Reader integration
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| VAULT-01 | Folder structure created at `Personal/Cashea/` with numbered prefixes | Folder creation is fully automatable via `mkdir -p`. Cashea/ does not exist yet — confirmed live. |
| VAULT-02 | Core plugins installed and configured in strict order | 4 of 8 plugins already installed (Templater 2.19.0, Dataview 0.5.68, Tasks 7.23.1, Excalidraw). Missing: Obsidian Git, Periodic Notes, Omnisearch, Linter. Plugin config requires Obsidian UI for initial install; data.json can be written for pre-existing plugins. |
| VAULT-03 | Vault git repo initialized as private `cashea-knowledge-vault` | Repo does NOT exist. SSH key confirmed (`jarmasp` account). Must be created on GitHub manually before `git push`. Git init at vault root is automatable. |
| VAULT-04 | 6 MOC files created | MOC files are plain markdown — fully automatable. |
| VAULT-05 | Dataview queries built into MOC files | Query syntax verified against official Dataview 0.5.68 docs. Tag syntax pitfall documented (see Pitfalls). |
| VAULT-06 | Tag taxonomy documented | Tag taxonomy lives in a reference note — fully automatable. |
| CAPT-01 | Concept article template in Templater | Template content fully specifiable. Exact Templater syntax verified. |
| CAPT-02 | Ticket reflection template in Templater | Template content fully specifiable. Callout block syntax verified. |
| CAPT-03 | Ticket reflection written before closing any branch | Behavioral rule — no file to create. Documents as standing rule in inbox or MOC note. |
| CAPT-04 | New concept stub created before session ends | Behavioral rule — documented in workflow note or inbox. |
| CAPT-05 | Each concept article embeds 3-5 resources | Structural requirement enforced by template design (Resources to Go Deeper section). |
| CAPT-06 | `#learning-gap` tag applied to weak-knowledge concepts | Tag taxonomy + Dataview query coverage. |
| REFL-01 | Weekly review template with all components | Template content fully specifiable per D-09, D-10, D-11. |
| REFL-02 | Survival mode version of weekly review | Second template file, 3 questions only. Fully automatable. |
| REFL-03 | Dataview queries in weekly review auto-pull tickets/gaps/resources | Verified query syntax documented below. |
| REFL-04 | Weekly reflection happens every week | Behavioral rule — enforced by template existence + Periodic Notes plugin. |
| SKILL-01 | `deslop` skill exists | Already exists at `.claude/get-shit-done/skills/deslop.md` — confirmed. No action needed. |
| SKILL-02 | `review-pr` skill exists | Already exists at `.claude/get-shit-done/skills/review-pr.md` — confirmed. No action needed. |
| SKILL-03 | Weekly skill retrospective question in weekly review | Embedded as standing question in weekly review template (D-17). No separate file. |
</phase_requirements>

---

## Summary

This phase scaffolds an Obsidian knowledge vault for cashea-backend engineering learning. The key technical insight is the division between what is automatable (file creation, template content, git init) and what requires manual Obsidian UI steps (installing missing plugins, configuring plugin settings). Four of the eight required plugins are already installed; the other four must be installed through the Obsidian community plugin browser. Plugin configuration — folder paths, auto-trigger settings, backup intervals — can be pre-written as JSON files for some plugins, but installing the plugin binaries themselves always requires the UI.

The most technically precise section is the Dataview query syntax. Tags stored in YAML frontmatter WITHOUT the `#` prefix are still accessible via `file.etags` WITH the `#` prefix. The correct syntax for filtering by tag in a WHERE clause is `WHERE econtains(file.etags, "#learning-gap")`, not `contains(tags, "#learning-gap")`. This is the single most common source of broken queries in new vaults.

The vault does not yet have a Cashea/ subfolder — everything must be created from scratch. The GitHub repo `cashea-knowledge-vault` does not exist under either `jarmasp` or `thyfus` — it must be created manually before any git push plan runs.

**Primary recommendation:** Create all files and folder structure programmatically (mkdir + Write tools). Configure plugin data.json for already-installed plugins. Separate manual steps (plugin installs, Obsidian UI configuration) into a dedicated plan step with explicit instructions.

---

## Vault State (Live Audit)

### What Exists
| Path | State |
|------|-------|
| `/Users/thyfus/Documents/obsidian vaults/personal/` | Vault root — exists |
| `.../Personal/` | The actual vault folder — exists |
| `.../Personal/.obsidian/` | Obsidian config dir — exists |
| `.../Personal/Cashea/` | Target subfolder — DOES NOT EXIST |
| `.../Personal/*.md` (7 notes) | Existing notes in root — need migration to Cashea/ |

### Currently Installed Plugins
| Plugin ID | Name | Version | Status |
|-----------|------|---------|--------|
| `templater-obsidian` | Templater | 2.19.0 | Installed — no data.json yet (not configured) |
| `dataview` | Dataview | 0.5.68 | Installed — no data.json |
| `obsidian-tasks-plugin` | Tasks | 7.23.1 | Installed — no data.json |
| `obsidian-excalidraw-plugin` | Excalidraw | (present) | Installed with data.json — config partial |

### Plugins NOT Yet Installed (Require Obsidian UI)
| Plugin ID | Name | Required For |
|-----------|------|-------------|
| `obsidian-git` | Obsidian Git | VAULT-03 auto-backup |
| `periodic-notes` | Periodic Notes | REFL-04 weekly auto-create |
| `omnisearch` | Omnisearch | VAULT-02 |
| `obsidian-linter` | Linter | VAULT-02 |

### Git State
- Vault root: NOT a git repo (confirmed)
- `cashea-knowledge-vault` GitHub repo: DOES NOT EXIST (confirmed via GitHub API)
- SSH key: authenticated as `jarmasp` on GitHub

---

## Automation vs. Manual Boundary

This is the most important architectural distinction for the plan.

### Fully Automatable (Write tool / mkdir / git commands)
- Creating all folders under `Personal/Cashea/`
- Writing all template files to `99-templates/`
- Writing all MOC files to `50-mocs/`
- Writing tag taxonomy reference note
- Writing survival mode weekly review template
- Writing `data.json` for already-installed plugins (Templater, Dataview, Tasks)
- Running `git init` at vault root
- Running `git remote add origin`
- Migrating 7 existing notes (copy + update frontmatter)

### Requires Obsidian UI (Manual Steps)
- Installing the 4 missing plugins (Obsidian Git, Periodic Notes, Omnisearch, Linter)
- Enabling "Community Plugins" in Settings if not already enabled
- Setting Templater folder location via Settings → Templater (or via data.json pre-write)
- Configuring Obsidian Git auto-backup interval (or via data.json pre-write after install)
- Configuring Periodic Notes weekly folder and format (or via data.json pre-write after install)
- Initial `git push` after repo is created on GitHub (must be manual because repo doesn't exist yet)
- Graph view color groups (Settings → Graph)
- Linter rules configuration

### Hybrid (Pre-write data.json, then reload in Obsidian)
Plugin configuration can be pre-written to `.obsidian/plugins/<plugin-id>/data.json` BEFORE installing (the file will be read once the plugin is installed and Obsidian restarts). This is the recommended approach for: Templater folder path, Dataview JS queries enabled, Tasks custom statuses, Obsidian Git backup interval.

---

## Standard Stack

### Already Installed (Confirmed)
| Plugin | Version | Purpose |
|--------|---------|---------|
| Templater | 2.19.0 | Template processing, auto-trigger on folder |
| Dataview | 0.5.68 | Query-driven views in MOC and weekly review notes |
| Tasks | 7.23.1 | Task tracking with custom statuses (`[/]`, `[-]`) |
| Excalidraw | (installed) | Architecture diagrams in concept articles |

### Must Be Installed via Obsidian UI
| Plugin ID | Purpose | Install Step |
|-----------|---------|-------------|
| `obsidian-git` | Auto-commit vault to GitHub every 30 min | Settings → Community Plugins → Browse |
| `periodic-notes` | Auto-create weekly notes in 30-weekly/ | Settings → Community Plugins → Browse |
| `omnisearch` | Replaces native search with semantic search | Settings → Community Plugins → Browse |
| `obsidian-linter` | Enforce frontmatter consistency on save | Settings → Community Plugins → Browse |

---

## Templater Syntax (Verified: v2.19.0)

### Template Syntax Rules
- Commands wrapped in `<% %>` delimiters
- Dynamic expressions: `<% tp.date.now("YYYY-MM-DD") %>`
- Static text outside delimiters is passed through verbatim
- Frontmatter YAML is processed as normal text — Templater commands work inside it

### Key Functions Used in These Templates

```
<% tp.date.now("YYYY-MM-DD") %>          — Current date as YYYY-MM-DD
<% tp.date.now("YYYY-[W]WW") %>          — ISO week format e.g. 2026-W15
<% tp.file.title %>                       — File name without extension
<% tp.file.creation_date("YYYY-MM-DD") %> — File creation date
```

### data.json for Templater (pre-write before install)

Write to `.obsidian/plugins/templater-obsidian/data.json`:

```json
{
  "templates_folder": "Personal/Cashea/99-templates",
  "trigger_on_file_creation": true,
  "enable_folder_templates": true,
  "folder_templates": [
    {
      "folder": "Personal/Cashea/20-tickets",
      "template": "Personal/Cashea/99-templates/ticket-reflection.md"
    },
    {
      "folder": "Personal/Cashea/10-concepts",
      "template": "Personal/Cashea/99-templates/concept-article.md"
    },
    {
      "folder": "Personal/Cashea/40-resources",
      "template": "Personal/Cashea/99-templates/learning-resource.md"
    }
  ],
  "syntax_highlighting": true,
  "auto_jump_to_cursor": false,
  "enable_system_commands": false
}
```

**Important:** `templates_folder` path is relative to the vault root. The vault root here is the `Personal/` folder (where `.obsidian/` lives), so the path starts with `Personal/Cashea/...`.

---

## Dataview Query Syntax (Verified: v0.5.68)

### Critical Tag Syntax Finding

Tags in YAML frontmatter MUST be written WITHOUT the `#` prefix:
```yaml
tags: [concept, backend, learning-gap]
```

In Dataview queries, `file.etags` stores tags WITH the `#` prefix automatically. Use `econtains()` for exact tag matching:

```
WHERE econtains(file.etags, "#learning-gap")    ← CORRECT
WHERE contains(tags, "#learning-gap")            ← WILL FAIL (tags array has no #)
WHERE contains(tags, "learning-gap")             ← WORKS but less precise
```

**Recommendation:** Use `econtains(file.etags, "#tag-name")` consistently. It handles both frontmatter and inline tags, and the `e` prefix prevents substring false positives.

### Verified Query Patterns

**Tickets closed this week:**
```dataview
TABLE ticket, date, file.link as "Note"
FROM "Personal/Cashea/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

**Concepts tagged as learning gaps:**
```dataview
TABLE file.mtime as "Flagged"
FROM "Personal/Cashea/10-concepts"
WHERE econtains(file.etags, "#learning-gap")
SORT file.mtime ASC
```

**Resources to read:**
```dataview
TABLE type, author
FROM "Personal/Cashea/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
```

**Unlinked concepts (orphan check for MOCs):**
```dataview
TABLE tags, file.mtime as "Last Updated"
FROM "Personal/Cashea/10-concepts"
WHERE !contains(moc, "[[")
SORT file.mtime ASC
```

**Recently updated concepts in a domain:**
```dataview
TABLE file.mtime as "Last Updated"
FROM "Personal/Cashea/10-concepts/backend"
SORT file.mtime DESC
LIMIT 10
```

**Tickets that touched this concept (embed inside concept article):**
```dataview
TABLE ticket, date
FROM "Personal/Cashea/20-tickets"
WHERE contains(file.outlinks, this.file.link)
SORT date DESC
```

### data.json for Dataview

Write to `.obsidian/plugins/dataview/data.json`:
```json
{
  "enableDataviewJs": true,
  "enableInlineDataviewJs": true,
  "refreshInterval": 500,
  "defaultDateFormat": "YYYY-MM-DD",
  "defaultDateTimeFormat": "YYYY-MM-DD HH:mm:ss"
}
```

---

## Template Content Specifications

### Ticket Reflection Template (`99-templates/ticket-reflection.md`)

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

### Concept Article Template (`99-templates/concept-article.md`)

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [concept]
confidence: low
moc: "[[]]"
---

# <% tp.file.title %>

> One-sentence definition.

## What It Is

> [!question] ¿Qué es esto en una oración?

## How It Works

> [!question] ¿Cómo funciona internamente? ¿Cómo fluye el control o los datos?

## How We Use It in cashea-backend

> [!question] ¿Dónde lo usamos en el código? Pon rutas de archivos o patrones concretos.

## Related Concepts

**Broader:** [[]]
**Narrower:** [[]]
**Sibling:** [[]]

## Resources to Go Deeper

- 1 official doc:
- 1 deep resource:
- 1 quick mental model:

## Things to Learn / Reinforce

- [ ] 
```

### Weekly Review Template (`99-templates/weekly-review.md`)

```markdown
---
week: <% tp.date.now("YYYY-[W]WW") %>
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [weekly]
---

# Week <% tp.date.now("YYYY-[W]WW") %> Review

## Tickets This Week

```dataview
TABLE ticket, date
FROM "Personal/Cashea/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

## Skill Domain Self-Rating

| Domain | Score (1-5) | Trend | Note |
|--------|-------------|-------|------|
| Coding patterns | | → | |
| System design | | → | |
| GCP / Infra | | → | |
| DevOps | | → | |
| Observability | | → | |
| Communication | | → | |

## Learning Gaps This Week

```dataview
LIST
FROM "Personal/Cashea/10-concepts"
WHERE econtains(file.etags, "#learning-gap")
SORT file.mtime DESC
LIMIT 10
```

## Resources in Queue

```dataview
LIST
FROM "Personal/Cashea/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
LIMIT 5
```

## ¿Qué se repitió esta semana que debería convertirse en skill o automatización?

> [!question] Escribe un patrón repetido o una fricción. Si aplica, crea un skill en `.claude/get-shit-done/skills/`.

## Esta semana puedo

> [!success] Puedo hacer X que antes no podía.
```

### Survival Mode Weekly Review Template (`99-templates/weekly-review-survival.md`)

```markdown
---
week: <% tp.date.now("YYYY-[W]WW") %>
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [weekly]
---

# Week <% tp.date.now("YYYY-[W]WW") %> — Survival Mode

## 3 Questions

1. ¿Qué cerré esta semana? (Una línea por ticket)
2. ¿Qué aprendí que no sabía el lunes?
3. ¿Qué haría diferente la semana que viene?

## Esta semana puedo

> [!success] Puedo hacer X que antes no podía.
```

### Learning Resource Template (`99-templates/learning-resource.md`)

```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [resource, to-read]
type: book
author: 
url: 
---

# <% tp.file.title %>

## Why This Resource

> [!question] ¿Qué gap o ticket llevó a este recurso?

Surfaced by: [[]]

## What It Covers

- 
- 

## Key Takeaways

*(Fill after consuming)*

## Concepts This Deepened

- [[]]

## Rating

/5 — 
```

---

## MOC File Structure

### Pattern (per ARCHITECTURE.md, with Dataview query)

Each MOC contains:
1. Brief one-line description of the domain
2. Manually curated link sections (grouped by sub-topic)
3. A Dataview query showing recently modified concepts in the domain

```markdown
# MOC: Backend Engineering

Entry point for all NestJS and TypeScript backend concepts in the Cashea wiki.

## Core Architecture
- [[hexagonal-architecture]] — ports and adapters as used in cashea-backend
- [[nestjs-modules]] — module system and DI container

## HTTP Layer
- [[nestjs-guards]] — session extraction and route protection
- [[nestjs-interceptors]] — request pipeline (logging, response transform)

## Data Layer
- [[typeorm-repository-pattern]] — ORM and repository abstraction

---

```dataview
TABLE file.mtime as "Last Updated"
FROM "Personal/Cashea/10-concepts/backend"
SORT file.mtime DESC
LIMIT 10
```
```

### 6 MOCs to Create
| File | Domain Covered |
|------|---------------|
| `MOC-Backend.md` | NestJS, TypeORM, guards, interceptors, events |
| `MOC-Infra.md` | GCP (Pub/Sub, Firestore, BigQuery, GCS, Secret Manager), Redis, Docker |
| `MOC-System-Design.md` | Architecture patterns, database patterns, messaging |
| `MOC-Cashea-Architecture.md` | How cashea-backend specifically works — living architecture doc |
| `MOC-Observability.md` | Datadog, Sentry, Pino, correlation IDs, tracing |
| `MOC-External-Services.md` | Algolia, LaunchDarkly, Talon.One, SendGrid, Twilio, Segment, Incode |

---

## Obsidian Git Configuration (Verified: Plugin ID `obsidian-git`)

The plugin must be installed via Obsidian UI first. The `data.json` can be pre-written so settings are applied on first launch after install.

Write to `.obsidian/plugins/obsidian-git/data.json` (create folder before install):
```json
{
  "autoSaveInterval": 30,
  "autoPullOnBoot": true,
  "autoPush": true,
  "commitMessage": "vault backup: {{date}}",
  "autoCommitMessage": "vault auto-backup: {{date}}",
  "pullBeforePush": true,
  "syncMethod": "rebase",
  "gitPath": "",
  "customMessageOnAutoBackup": false,
  "commitDateFormat": "YYYY-MM-DD HH:mm:ss",
  "autoBackupAfterFileChange": false,
  "differentIntervalCommitAndPush": false
}
```

**Note on `autoSaveInterval`:** This field is in **minutes** based on plugin documentation (30 = 30 min auto-commit). Verify after first install — the UI label reads "minutes."

### Git Init Commands (Automatable)

```bash
cd "/Users/thyfus/Documents/obsidian vaults/personal"
git init
git add .
git commit -m "chore: initialize vault with Cashea structure"
git remote add origin git@github.com:jarmasp/cashea-knowledge-vault.git
```

The push step (`git push -u origin main`) requires the remote repo to exist first. This is a blocker documented in STATE.md and must be a manual prerequisite.

---

## Note Migration Map

7 existing notes in `Personal/` root → target locations in `Personal/Cashea/`:

| Current Note | Target Location | Rationale |
|-------------|----------------|-----------|
| `Cashea — Employee Guard Mechanism.md` | `10-concepts/security/employee-guard.md` | Architectural concept — guard mechanism |
| `Cashea — Employee Scope Guard — Decisiones de Diseño.md` | `10-concepts/security/employee-scope-guard-decisions.md` | Design decisions = concept knowledge |
| `Cashea — Employee Scope Guard — Referencia Técnica.md` | `10-concepts/security/employee-scope-guard-reference.md` | Technical reference = concept knowledge |
| `Admin Audit Events - Pub Sub.md` | `10-concepts/backend/admin-audit-events-pubsub.md` | Pub/Sub architecture concept |
| `Cashea backend — Cursor rules & GSD.md` | `00-inbox/cursor-rules-and-gsd.md` | Meta-tooling — process inbox first |
| `Force Password Change Decisions.md` | `20-tickets/force-password-change-decisions.md` | Ticket/feature decisions |
| `Suggest password change.md` | `20-tickets/suggest-password-change.md` | Ticket reflection (already has ticket-like structure) |

**Migration action per note:**
1. Copy file to target path with new slug filename
2. Add frontmatter if missing (`date`, `tags`, `status`/`confidence` as appropriate)
3. Preserve all existing content — no rewriting
4. Delete original from `Personal/` root

---

## Common Pitfalls

### Pitfall 1: Tag Syntax Mismatch in Dataview
**What goes wrong:** `WHERE contains(tags, "#learning-gap")` returns zero results even though notes are clearly tagged.
**Why it happens:** YAML frontmatter stores tags without `#` (`tags: [learning-gap]`). The `tags` field in Dataview holds the raw array. Only `file.etags` auto-adds the `#` prefix.
**How to avoid:** Always use `econtains(file.etags, "#tag-name")` for file-level tag filtering.
**Warning signs:** Query returns 0 results; note has the tag visually but query misses it.

### Pitfall 2: Templater Folder Path Relative to Vault Root
**What goes wrong:** Templater can't find templates; auto-trigger doesn't fire.
**Why it happens:** The `templates_folder` in data.json must be relative to the vault root (the `Personal/` folder where `.obsidian/` lives), not to `Cashea/`.
**How to avoid:** Write `"templates_folder": "Personal/Cashea/99-templates"` not `"Cashea/99-templates"`.
**Warning signs:** Templater settings show the folder as red/invalid in the UI.

### Pitfall 3: Pre-writing data.json Without Plugin Installed
**What goes wrong:** data.json is written but settings are ignored or overwritten on install.
**Why it happens:** When Obsidian installs a plugin for the first time, it writes a fresh data.json with defaults if none exists. If one exists, it reads it.
**How to avoid:** Create the plugin folder AND data.json BEFORE installing. Obsidian will read the existing data.json on first activation. Confirm settings in Obsidian UI after install.
**Warning signs:** After install, settings don't match what was written.

### Pitfall 4: Git Init at Wrong Path
**What goes wrong:** Vault git repo ends up inside `cashea-backend` or inside `Cashea/` subfolder only.
**Why it happens:** Running `git init` in the wrong directory.
**How to avoid:** Per D-14, init at `/Users/thyfus/Documents/obsidian vaults/personal/` (the vault root containing the `Personal/` folder). This means the entire vault (including `.obsidian/`) is versioned.
**Warning signs:** `git status` from vault root shows "not a git repository."

### Pitfall 5: Renaming Files Outside Obsidian
**What goes wrong:** Wikilinks to migrated notes break silently.
**Why it happens:** Obsidian's rename function updates all backlinks. Filesystem rename (mv command) does not.
**How to avoid:** After copying migrated notes to new locations, open Obsidian and let it detect the new files. The old wikilinks in other notes will show as unresolved — update them using Obsidian's link panel, not manually. Alternatively: write new files at new paths, then delete originals — wikilinks in existing notes pointing to old filenames will show as unresolved (visible, fixable).
**Warning signs:** Graph view shows broken (unresolved) link nodes.

### Pitfall 6: Callout Block Syntax
**What goes wrong:** Callouts don't render — show as plain blockquotes.
**Why it happens:** Callout type must be on the first line immediately after `>`. No blank line between `>` and content.
**How to avoid:**
```markdown
> [!question] Title text here
> Body text on this line or next
```
NOT:
```markdown
> [!question]
>
> Body text (blank line breaks the callout)
```
**Warning signs:** Callout shows as regular `>` blockquote in reading mode.

### Pitfall 7: Obsidian Git Push Requires Existing Remote
**What goes wrong:** `git push` fails with "remote: Repository not found."
**Why it happens:** `cashea-knowledge-vault` does not exist on GitHub yet.
**How to avoid:** Create the private repo on GitHub manually BEFORE running any plan that does `git push`. GitHub handle is `jarmasp` (confirmed via SSH key).
**Warning signs:** `git remote -v` shows the remote URL but push fails with 403/404.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| git | VAULT-03 vault repo init | Yes | 2.48.1 | — |
| GitHub SSH key | VAULT-03 git push | Yes | jarmasp account | — |
| `cashea-knowledge-vault` GitHub repo | VAULT-03 git push | NO — must be created | — | Create manually before push plan |
| Obsidian (running) | Plugin installation | Yes (implied) | Desktop | — |
| Templater plugin | CAPT-01, CAPT-02, REFL-01 | Installed (2.19.0) | 2.19.0 | — |
| Dataview plugin | VAULT-04, VAULT-05, REFL-03 | Installed (0.5.68) | 0.5.68 | — |
| Tasks plugin | LRNG-03 (Phase 3) | Installed (7.23.1) | 7.23.1 | — |
| Obsidian Git plugin | VAULT-03 | NOT installed | — | Must install via UI |
| Periodic Notes plugin | REFL-04 | NOT installed | — | Must install via UI |
| Omnisearch plugin | VAULT-02 | NOT installed | — | Must install via UI |
| Linter plugin | VAULT-02 | NOT installed | — | Must install via UI |

**Missing dependencies with no fallback:**
- `cashea-knowledge-vault` GitHub repo — blocks git push step; all preceding steps can complete first

**Missing dependencies with UI fallback:**
- Obsidian Git, Periodic Notes, Omnisearch, Linter — installable via Settings → Community Plugins

---

## Code Examples

### Ticket Reflection Frontmatter (Verified Templater Syntax)
```markdown
---
date: <% tp.date.now("YYYY-MM-DD") %>
ticket: GROWTH-
branch: 
status: resolved
tags: [ticket, backend]
---
```

### Callout Block Pattern (D-05 spec)
```markdown
## What Was Hard

> [!question] ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?
```

### Capability Assertion Callout (D-11 spec)
```markdown
## Esta semana puedo

> [!success] Puedo hacer X que antes no podía.
```

### MOC Dataview Query (Verified Syntax)
```dataview
TABLE file.mtime as "Last Updated"
FROM "Personal/Cashea/10-concepts/backend"
SORT file.mtime DESC
LIMIT 10
```

### Weekly Review — Tickets Query (Verified Syntax)
```dataview
TABLE ticket, date
FROM "Personal/Cashea/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

---

## Validation Architecture

Nyquist validation does not apply to this phase. There is no test suite for Obsidian vault setup. Verification is functional/behavioral:

### Manual Verification Checklist (Post-Phase)

**Folder structure:**
```bash
ls "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/"
# Must show: 00-inbox, 10-concepts, 20-tickets, 30-weekly, 40-resources, 50-mocs, 99-templates
```

**Template trigger test:**
1. Create a new note inside `20-tickets/` folder in Obsidian
2. Verify the ticket-reflection template is auto-applied (frontmatter appears, callout sections appear)

**Dataview query test:**
1. Open any MOC file in Obsidian reading mode
2. Verify the Dataview block renders as a table (not as raw code)
3. If it shows "Dataview: No results" — that's correct for an empty vault. If it shows a parse error, the query syntax is wrong.

**Git test:**
```bash
cd "/Users/thyfus/Documents/obsidian vaults/personal"
git status
# Must show: "On branch main" or "On branch master", clean state or staged files
git remote -v
# Must show: origin git@github.com:jarmasp/cashea-knowledge-vault.git
```

**Callout render test:**
Open any template in Obsidian reading mode. `> [!question]` callouts must render as styled blocks, not plain blockquotes.

**Migration test:**
Verify the 7 original notes no longer exist in `Personal/` root and exist with correct frontmatter in their new locations.

---

## Sources

### Primary (HIGH confidence)
- Live vault inspection — plugin versions, folder state, git state verified directly
- Dataview official docs (blacksmithgu.github.io/obsidian-dataview) — query syntax, functions
- Templater official docs (silentvoid13.github.io/Templater) — function signatures, settings field names
- Templater plugin manifest.json — confirmed version 2.19.0

### Secondary (MEDIUM confidence)
- Obsidian Forum: Tags in frontmatter and Dataview (forum.obsidian.md/t/tags-in-front-matter-dataview-and-search-confused) — tag/etags distinction
- Obsidian Forum: Nested tags and econtains (forum.obsidian.md/t/nested-tags-in-combination-with-contains) — correct function recommendation
- Obsidian Git GitHub README (github.com/Vinzent03/obsidian-git) — settings interface field names
- DeepWiki Templater (deepwiki.com/SilentVoid13/Templater) — data.json field names for folder_templates

### Tertiary (LOW confidence — verify in Obsidian UI after install)
- `autoSaveInterval` unit (minutes vs seconds) — confirmed as minutes from docs but verify in UI after Obsidian Git install
- Periodic Notes `data.json` field names — not directly verified; configure via UI then inspect written file

---

## Metadata

**Confidence breakdown:**
- Vault current state (what exists/doesn't): HIGH — verified live
- Template syntax (Templater): HIGH — official docs + version confirmed
- Dataview query syntax: HIGH — official docs + community forum cross-verified
- data.json field names (Templater): MEDIUM — deepwiki cross-reference, verify in UI
- data.json field names (Obsidian Git): MEDIUM — GitHub types.ts, not directly verified
- Note migration targets: HIGH — based on content review of actual notes
- Plugin install boundary (what requires UI): HIGH — fundamental Obsidian behavior

**Research date:** 2026-04-13
**Valid until:** 2026-06-01 (Obsidian plugin APIs are stable; Dataview 0.5.x syntax unlikely to change)
