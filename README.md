# Growth OS

A personal engineering growth operating system that turns daily work into compounding skill.

Every ticket becomes a reflection note. Every pattern encountered links to a concept article.
Every week surfaces gaps. The system runs on top of your actual work — no synthetic side projects,
no separate learning time. The work IS the practice.

---

## How It Works

```
Ticket opens
  → /reflect after coding: write What Was Hard, What I Learned, Concepts Encountered
  → /concept {name}: expand any concept that felt unclear into a full article
  → /weekly at sprint end: surface gaps, rate domains, write capability assertion
```

Over time: knowledge graph grows, pattern gaps shrink, self-doubt reduces.

---

## What It Builds On

- **Obsidian** — local-first knowledge graph with Dataview, Templater, Tasks plugins
- **Claude Code** — three slash commands that write directly to your vault
- **Your actual work** — every ticket is a learning artifact, not extra work

---

## Installation

**1. Clone**

```bash
git clone {repo-url} ~/Documents/growth-os
```

**2. Configure your vault path**

Edit `config.json`:

```json
{
  "vault_root": "/path/to/your/obsidian/vault/subfolder",
  ...
}
```

**3. Set up vault structure**

Your Obsidian vault needs these folders:

```
00-inbox/
10-concepts/
  backend/
  system-design/
  security/
  infra/
20-tickets/
30-weekly/
40-resources/
50-mocs/
99-templates/
homework-log.md
```

Copy templates from `templates/` into your vault's `99-templates/` directory.

**4. Install Claude Code commands**

```bash
bash install.sh
```

This symlinks `commands/*.md` into `~/.claude/commands/` so the slash commands are
available globally in Claude Code.

---

## Commands

| Command | When to use | Writes to |
|---------|-------------|-----------|
| `/reflect` | After resolving a ticket | `20-tickets/{ticket}.md` |
| `/concept {name}` | When a pattern felt unclear | `10-concepts/{domain}/{slug}.md` |
| `/weekly` | End of sprint / every Friday | `30-weekly/{YYYY-[W]WW}.md` |

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
commands/         — Claude Code slash commands (source of truth)
workflows/        — Full orchestration docs loaded by commands
templates/        — Reference copies of Obsidian note templates
.planning/        — Personal milestone planning (gitignored by default)
config.json       — Vault path and settings (edit per user)
install.sh        — Links commands to ~/.claude/commands/
```

---

## Philosophy

GSD handles building software. Growth OS handles building the engineer.

GSD owns: code execution, PR review, diff cleanup.
Growth OS owns: reflection, concept articulation, weekly synthesis.

The boundary is deliberate. Code-building and self-building use different rhythms.
