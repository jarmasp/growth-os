<div align="center">

# 🌱 Growth OS

**A personal engineering growth operating system that turns daily work into compounding skill.**

*The work IS the practice — no synthetic side projects, no separate study time.*

[![Built for Claude Code](https://img.shields.io/badge/Built%20for-Claude%20Code-d97757)](https://claude.com/claude-code)
[![Runs on Obsidian](https://img.shields.io/badge/Runs%20on-Obsidian-7c3aed)](https://obsidian.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

</div>

---

Every ticket becomes a reflection note. Every pattern you hit links to a concept article.
Every week surfaces the gaps. Growth OS runs *on top of* your real work — so the knowledge
graph grows, pattern gaps shrink, and each sprint leaves a permanent artifact behind.

> **GSD builds the software. Growth OS builds the engineer.**

---

## ✨ The Loop

```
 Ticket opens
   │
   ├─▶  /growth:premortem    before coding  ·  predict failure points, capture assumptions
   │
   ├─▶  /growth:reflect      after coding   ·  complete the draft, score prediction vs reality
   │
   ├─▶  /growth:concept {x}  any time       ·  expand an unclear pattern into a full article
   │
   └─▶  /growth:weekly       sprint end     ·  surface gaps, rate domains, assert capability
```

Over time: reflection scores trend up · the knowledge graph densifies · self-doubt drops.

---

## 🧩 What It's Built On

| Layer | Tool | Role |
|-------|------|------|
| Knowledge graph | [**Obsidian**](https://obsidian.md) | Local-first notes with Dataview, Templater & Tasks |
| Automation | [**Claude Code**](https://claude.com/claude-code) | Five slash commands that write straight into your vault |
| Fuel | **Your actual work** | Every ticket is a learning artifact, not extra work |

---

## 🚀 Quick Start

**1. Clone**

```bash
git clone <repo-url> ~/Documents/growth-os
```

**2. Install the commands**

```bash
bash ~/Documents/growth-os/install.sh
```

Symlinks `commands/growth/*.md` into `~/.claude/commands/growth/` so the commands are
available globally in Claude Code as `/growth:*`.

**3. Point it at your vault**

```bash
cp config.example.json config.json
```

Then edit `config.json` so `vault_root` points to a folder **inside** your Obsidian vault:

```json
{
  "vault_root": "/Users/you/Documents/obsidian/personal/Work",
  "vault_name": "YourVaultName",
  "project_name": "your-project-name"
}
```

**4. Onboard**

```
/growth:onboard
```

Runs a 5-phase adaptive interview, saves your profile to `config.json`, and scaffolds your
vault with every folder, template, and MOC file it needs. Idempotent — safe to re-run.

---

## 🛠️ Commands

| Command | When | Writes to |
|---------|------|-----------|
| `/growth:onboard` | Once on setup · re-run to update profile | `config.json` + vault scaffold |
| `/growth:premortem` | Before coding starts on a ticket | `20-tickets/{ticket}-draft.md` |
| `/growth:reflect` | After resolving a ticket | `20-tickets/{ticket}.md` |
| `/growth:concept {name}` | When a pattern felt unclear | `10-concepts/{domain}/{slug}.md` |
| `/growth:weekly` | End of sprint / every Friday | `30-weekly/{YYYY-[W]WW}.md` |

📖 Full command docs & configuration reference: **[HOW-TO-USE.md](./HOW-TO-USE.md)**

---

## 📊 Scored, Not Vibes

Reflections and weekly reviews are scored against established learning-science rubrics, and the
scores are written into each note's frontmatter so trends are queryable in Dataview.

**Ticket reflection** — 5 dimensions, 0–10 total:
Cognitive Depth · Cycle Completeness · Loop Depth · Actionability · Linguistic Quality

**Weekly review** — 5 dimensions across Ericsson, AAR, Kirkpatrick, Dreyfus & Behavioral Science:
Deliberate Practice · After-Action Depth · Learning Transfer · Skill Progression · Behavioral Change

---

## 🔁 Deliberate Practice

Three recurring drills tracked in `homework-log.md`:

| Drill | Frequency | What it builds |
|-------|-----------|----------------|
| PR rewrite | Once per sprint | Sees your own blind spots |
| Naked system design | Biweekly | Exposes what you only think you know |
| One-concept deepening | Weekly | Turns shallow pattern-awareness into real understanding |

---

## 📁 Repository Structure

```
commands/growth/   Claude Code slash commands (source of truth)
workflows/         Full orchestration docs loaded by each command
agents/            Scoring-rubric agents
templates/         Reference copies of the Obsidian note templates
install.sh         Links commands into ~/.claude/commands/growth/
config.example.json  Copy to config.json and edit (config.json is gitignored)
HOW-TO-USE.md      Full installation & usage guide
```

> **Privacy:** `config.json`, project-specific configs (`config.*.json`), `.planning/`, and
> `SESSION-*.md` notes are gitignored — your profile and work notes never leave your machine.

---

## 🧭 Philosophy

The boundary is deliberate. Code-building and self-building run on different rhythms.

- **Growth OS owns:** reflection, concept articulation, weekly synthesis.
- **GSD / IDE tools own:** code execution, PR review, diff cleanup.

Every sprint leaves a knowledge artifact — so pattern gaps shrink, self-doubt reduces, and the
next sprint is faster and more confident than the last.

---

## License

MIT — see [LICENSE](./LICENSE).
</content>
</invoke>
