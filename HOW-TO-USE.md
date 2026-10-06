# Growth OS — How to Use

A personal engineering growth system that turns daily work into compounding skill.

Every ticket becomes a reflection note. Every pattern encountered links to a concept article.
Every week surfaces gaps. The system runs on top of your actual work — no synthetic side
projects, no separate learning time. The work IS the practice.

---

## Dependencies

### Required

| Dependency | Purpose | Install |
|------------|---------|---------|
| [Obsidian](https://obsidian.md) | Local-first knowledge graph | Free download |
| [Claude Code](https://claude.ai/code) **or** [Cursor](https://cursor.com) | Agent that runs the growth commands | `npm install -g @anthropic-ai/claude-code`, or Cursor's own installer |

### Obsidian Plugins

These are installed and configured by `/growth:onboard` — no manual setup needed.

| Plugin | Purpose |
|--------|---------|
| Templater | Auto-fill note templates on creation |
| Dataview | Query your notes like a database |
| Tasks | Track recurring practice drills |
| Obsidian Git | Auto-sync vault to a private GitHub repo |

---

## Installation

### 1. Clone

```bash
git clone git@github.com:jarmasp/growth-os.git ~/Documents/growth-os
```

### 2. Install commands

```bash
bash ~/Documents/growth-os/install.sh
```

This symlinks `commands/growth/*.md` into `~/.claude/commands/growth/` so the slash commands
are available globally in Claude Code as `/growth:*`.

**Output:**
```
Installing Growth OS commands...
  linking: growth/concept.md
  linking: growth/onboard.md
  linking: growth/reflect.md
  linking: growth/weekly.md

Done. Commands available in Claude Code:
  /growth:concept
  /growth:onboard
  /growth:reflect
  /growth:weekly

Next step: run /growth:onboard in Claude Code to set up your profile and scaffold your Obsidian vault.
```

Using Cursor instead (or as well)?

```bash
bash ~/Documents/growth-os/cursor/install-cursor.sh
```

Symlinks the five skills, the `growth-os` rule, and the slash commands into `~/.cursor/`.

### 3. Configure your vault path

Copy the example config, then edit it:

```bash
cp ~/Documents/growth-os/config.example.json ~/Documents/growth-os/config.json
```

```json
{
  "vault_root": "/path/to/your/obsidian/vault/subfolder",
  "vault_name": "YourVaultName",
  "project_name": "your-project-name"
}
```

`vault_root` must point to a folder **inside** your Obsidian vault, not the vault root itself.
For example: `/Users/you/Documents/obsidian/personal/Work`.

### 4. Run onboarding

Open Claude Code in any project directory and run:

```
/growth:onboard
```

This runs a 5-phase adaptive interview and scaffolds your vault automatically.

---

## Commands

All commands use the `growth:` namespace to avoid collisions with other Claude Code commands.

---

### `/growth:onboard`

**When:** Once on setup. Re-run when your context changes significantly.

Runs a coaching interview to build your user profile, then scaffolds your Obsidian vault:

- Creates folder structure (`00-inbox/`, `10-concepts/`, `20-tickets/`, `30-weekly/`, `40-resources/`, `50-mocs/`, `60-project/`, `99-templates/`)
- Installs all Templater templates into `99-templates/`
- Creates MOC files for each domain in `50-mocs/`
- Sets up `60-project/` with `adr/`, `modules/`, `domain/`, `business/`, `runbooks/`
- Saves your profile to `config.json`
- Idempotent — safe to re-run; never overwrites existing notes

**Profile fields captured:**
- Name, role, context
- Primary tools / medium
- Experience level (Dreyfus scale)
- Growth goals and competing commitments
- Priority skill domains

---

### `/growth:premortem`

**When:** Before coding starts on a ticket.

Writes a draft reflection note to `20-tickets/{ticket}.md` with `status: in-progress`:

1. Asks for branch name, ticket ID, and description
2. Scans for planning artifacts (CONTEXT.md, PLAN.md) if present
3. Runs 4 focused questions (one at a time):
   - Business context — what problem does this solve?
   - 3 probable failure points — where can this go wrong? (pushes for specifics)
   - Design pattern — what's the key technical decision?
   - Assumptions — what could be wrong?
4. Writes the Pre-mortem + Assumptions sections to a draft note
5. Remaining sections contain placeholders pointing to `/growth:reflect`

After writing, Claude outputs the draft path and reminds you to run `/growth:reflect` when done.

The draft note can be opened in Obsidian while coding — useful as a reference during implementation.

---

### `/growth:reflect`

**When:** After closing a ticket or resolving a branch.

If a pre-mortem draft exists for this ticket, it is detected automatically — the workflow
loads the pre-mortem content, skips the Assumptions question, and replaces it with a bridge
question: "did reality match your predictions?" The draft is then completed in-place.

Writes a structured reflection note to `20-tickets/{ticket}.md`:

1. Asks for branch name, ticket ID, and description upfront
2. Fills in Pre-mortem, What Was Hard, What I Learned, Concepts Encountered from conversation
3. Scores the reflection on 5 dimensions (0–10 total)
4. Writes score fields to the note's YAML frontmatter
5. Appends a row to `reflection-scores.md` at vault root

**Reflection score dimensions:**

| Frontmatter field | Dimension | Max |
|-------------------|-----------|-----|
| `score_d1` | Cognitive Depth | 3 |
| `score_d2` | Cycle Completeness | 2 |
| `score_d3` | Loop Depth | 2 |
| `score_d4` | Actionability | 2 |
| `score_d5` | Linguistic Quality | 1 |
| `score` | **Total** | **10** |

---

### `/growth:concept {name}`

**When:** When a pattern felt unclear during a ticket, or when `/growth:reflect` surfaces a wikilink with no article.

Writes or expands a concept article to `10-concepts/{domain}/{slug}.md` using the D-08 format:

1. What It Is
2. How It Works
3. How We Use It in Practice
4. Related Concepts
5. Resources to Go Deeper
6. Things to Learn / Reinforce

**Examples:**
```
/growth:concept nestjs-interceptors
/growth:concept TypeORM migrations
/growth:concept hexagonal-architecture
```

Detects the right domain from your `concept_domains` in `config.json`. Creates a new article
if none exists, or expands an existing stub.

---

### `/growth:weekly`

**When:** End of sprint — every Friday or at sprint close.

Writes a weekly review note to `30-weekly/{YYYY-[W]WW}.md`:

1. Runs an interview to gather highlights, struggles, and patterns
2. Scores the week on 5 dimensions (W1–W5) using a multi-framework rubric
3. Writes score fields to the note's YAML frontmatter (`weekly_score`, `w1`–`w5`)
4. Builds a per-domain skill rating table from your priority domains
5. Surfaces learning gaps from tagged concept articles
6. Processes `00-inbox/` — proposes categorization for any unprocessed notes

**Weekly score dimensions:**

| Frontmatter field | Dimension | Framework |
|-------------------|-----------|-----------|
| `w1` | Deliberate Practice Quality | Ericsson |
| `w2` | After-Action Review Depth | AAR |
| `w3` | Learning Transfer | Kirkpatrick |
| `w4` | Skill Level Progression | Dreyfus |
| `w5` | Behavioral Change Signal | Behavioral Science |

---

## Configuration Reference

`config.json` is the single source of truth for vault paths and user settings.

| Field | Purpose | When to edit |
|-------|---------|-------------|
| `vault_root` | Absolute path to your vault subfolder | Once, before `/growth:onboard` |
| `vault_name` | Vault name used in Dataview queries | Safe to change anytime |
| `project_name` | Your main codebase or project name | Safe to change anytime |
| `concept_domains` | Subdomain folders in `10-concepts/` | Set by `/growth:onboard` — do not edit manually |
| `vault.*` | Section subfolder names | Set once during onboarding, stable |
| `project_docs_subfolders` | Subfolders inside `60-project/` | Set by `/growth:onboard` |

> **Warning:** `concept_domains` maps directly to vault folder names. If you change it manually
> after `/growth:onboard` has run, you must also rename the corresponding folders in your vault.
> Re-run `/growth:onboard` instead — it handles the update safely.

---

## Repository Structure

```
commands/
  growth/
    reflect.md          — /growth:reflect command stub
    concept.md          — /growth:concept command stub
    weekly.md           — /growth:weekly command stub
    onboard.md          — /growth:onboard command stub
workflows/
  reflect.md            — Full reflect orchestration
  concept.md            — Full concept article orchestration
  weekly-review.md      — Full weekly review orchestration
  onboarding.md         — Full onboarding orchestration
agents/
  reflection-scorer.md  — 5-dimension reflection scoring rubric
  weekly-reviewer.md    — 5-dimension weekly review scoring rubric
  onboarding-agent.md   — Adaptive interview agent
templates/
  ticket-reflection.md  — Obsidian template for ticket notes
  concept-article.md    — Obsidian template for concept articles
  weekly-review.md      — Obsidian template for weekly reviews
  adr.md                — Obsidian template for ADRs
cursor/
  install-cursor.sh     — Installs skills/rule/commands into ~/.cursor/
  rules/growth-os.mdc    — Cursor rule pointing at the workflows
  skills/growth-*/       — One skill per command, same orchestration as commands/growth/
.planning/              — Milestone planning artifacts (gitignored)
config.json             — Vault path and user settings
install.sh              — Installs commands to ~/.claude/commands/growth/
HOW-TO-USE.md           — This file
README.md               — Quick project overview
```

---

## Deliberate Practice Loop

```
Ticket opens
  → /growth:reflect after coding
  → /growth:concept {name} for any unclear pattern
  → /growth:weekly at sprint end
```

Over time: reflection scores trend upward, knowledge graph grows, pattern gaps shrink.

The `homework-log.md` in your vault tracks three recurring drills:

| Drill | Frequency | What it builds |
|-------|-----------|----------------|
| PR rewrite | Once per sprint | Sees your own blind spots |
| Naked system design | Biweekly | Exposes what you think you know |
| One-concept deepening | Weekly | Converts shallow pattern-awareness into real understanding |

---

## Philosophy

**This repo builds the engineer. Other tools build the software.**

- Growth OS owns: reflection, concept articulation, weekly synthesis
- GSD / IDE tools own: code execution, PR review, diff cleanup

The boundary is deliberate. Code-building and self-building use different rhythms.
Every sprint leaves a knowledge artifact — so pattern gaps shrink, self-doubt reduces,
and the next sprint is faster and more confident than the last.
