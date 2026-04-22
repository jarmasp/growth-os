# Growth OS

A personal engineering growth operating system that turns daily work into compounding skill.

Every ticket becomes a reflection note. Every pattern encountered links to a concept article.
Every week surfaces gaps. The system runs on top of your actual work — no synthetic side projects,
no separate learning time. The work IS the practice.

---

## How It Works

```
Ticket opens
  → /growth:premortem before coding: predict failure points, capture assumptions
  → /growth:reflect after coding: completes the draft; scores the prediction vs reality loop
  → /growth:concept {name}: expand any concept that felt unclear into a full article
  → /growth:weekly at sprint end: surface gaps, rate domains, write capability assertion
```

Over time: knowledge graph grows, pattern gaps shrink, self-doubt reduces.

---

## What It Builds On

- **Obsidian** — local-first knowledge graph with Dataview, Templater, Tasks plugins
- **Claude Code** — four slash commands that write directly to your vault
- **Your actual work** — every ticket is a learning artifact, not extra work

---

## Installation

**1. Clone**

```bash
git clone {repo-url} ~/Documents/growth-os
```

**2. Install commands**

```bash
bash install.sh
```

This symlinks `commands/growth/*.md` into `~/.claude/commands/growth/` so the slash commands
are available globally in Claude Code as `/growth:*`.

**3. Configure your vault path**

Edit `config.json`:

```json
{
  "vault_root": "/path/to/your/obsidian/vault/subfolder",
  "vault_name": "YourVaultName",
  "project_name": "your-project-name"
}
```

**4. Run onboarding**

```
/growth:onboard
```

Runs a 5-phase adaptive interview, saves your profile to `config.json`, and scaffolds
your Obsidian vault with all required folders, templates, and MOC files.

---

## Commands

| Command | When to use | Writes to |
|---------|-------------|-----------|
| `/growth:onboard` | Once on setup, re-run to update profile | `config.json` + vault scaffolding |
| `/growth:premortem` | Before coding starts on a ticket | `20-tickets/{ticket}-draft.md` (status: in-progress) |
| `/growth:reflect` | After resolving a ticket | `20-tickets/{ticket}.md` (completes draft if one exists) |
| `/growth:concept {name}` | When a pattern felt unclear | `10-concepts/{domain}/{slug}.md` |
| `/growth:weekly` | End of sprint / every Friday | `30-weekly/{YYYY-[W]WW}.md` |

See [HOW-TO-USE.md](./HOW-TO-USE.md) for full command documentation and configuration reference.

---

## Deliberate Practice (homework-log.md)

Three recurring drills tracked in `homework-log.md`:

| Drill | Frequency | What it builds |
|-------|-----------|----------------|
| PR rewrite | Once per sprint | Sees your own blind spots |
| Naked system design | Biweekly | Exposes what you think you know |
| One-concept deepening | Weekly | Converts shallow pattern awareness into real understanding |

---

## Repository Structure

```
commands/
  growth/       — Claude Code slash commands (source of truth)
workflows/      — Full orchestration docs loaded by commands
agents/         — Scoring rubric agents
templates/      — Reference copies of Obsidian note templates
.planning/      — Personal milestone planning (gitignored by default)
config.json     — Vault path and settings (edit per user)
install.sh      — Links commands to ~/.claude/commands/growth/
HOW-TO-USE.md   — Full installation and usage guide
```

---

## Philosophy

GSD handles building software. Growth OS handles building the engineer.

GSD owns: code execution, PR review, diff cleanup.
Growth OS owns: reflection, concept articulation, weekly synthesis.

The boundary is deliberate. Code-building and self-building use different rhythms.
