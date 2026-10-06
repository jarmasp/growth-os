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
| Automation | A standalone Python CLI (`growth <command>`) | Runs in any terminal — Claude Code / Cursor slash commands still work, pointing at the same CLI |
| Fuel | **Your actual work** | Every ticket is a learning artifact, not extra work |

---

## 🚀 Quick Start

**1. Clone**

```bash
git clone git@github.com:jarmasp/growth-os.git ~/Documents/growth-os
```

**2. Install the commands**

```bash
bash ~/Documents/growth-os/install.sh
```

Symlinks `commands/growth/*.md` into `~/.claude/commands/growth/` so the commands are
available globally in Claude Code as `/growth:*`.

Using Cursor instead (or as well)? Also run:

```bash
bash ~/Documents/growth-os/cursor/install-cursor.sh
```

Symlinks the five skills, the `growth-os` rule, and the slash commands into `~/.cursor/`.

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

**4. Onboard, premortem, reflect, concept, weekly — all run from a plain terminal**

```bash
~/Documents/growth-os/growth onboard
~/Documents/growth-os/growth premortem
~/Documents/growth-os/growth reflect
~/Documents/growth-os/growth concept "nestjs interceptors"
~/Documents/growth-os/growth weekly
```

All five are a standalone Python CLI (stdlib only) as of v3.0. Claude Code / Cursor are
no longer required for any of them — only `growth onboard`'s interview is genuinely
multi-turn (the model picks each next question); the rest call the model at most once,
statelessly. Add `growth-os` to your `PATH` and it's just `growth <command>`.
`--agent claude|codex|print` picks the backend (`print` dumps the assembled prompt to
stdout instead of calling anything — paste it into any model, anywhere; not available
for `onboard`, which needs a real back-and-forth). `growth doctor` checks your config,
backends, and index; `growth init` writes `~/.growth-os/config.json` for you.

**`growth index` / `growth search "{query}"`** build and query a local hybrid
(keyword + semantic) store over your vault — `pip install -r requirements-index.txt`
for the semantic half, or skip it and get keyword search alone. `reflect` uses it
internally to pick relevant `[[concept]]` links instead of guessing from filenames.

The `/growth:*` slash commands still work in Claude Code / Cursor — each one now just
points you at the CLI instead of running the workflow inline.

---

## 🛠️ Commands

| Command | When | Writes to |
|---------|------|-----------|
| `growth onboard` | Once on setup · re-run to update profile | `config.json` + vault scaffold |
| `growth premortem` | Before coding starts on a ticket | `20-tickets/{ticket}-draft.md` |
| `growth reflect` | After resolving a ticket | `20-tickets/{ticket}.md` |
| `growth concept "{name}"` | When a pattern felt unclear | `10-concepts/{domain}/{slug}.md` |
| `growth weekly` | End of sprint / every Friday | `30-weekly/{YYYY-[W]WW}.md` |
| `growth index` | After new notes, or anytime | `~/.growth-os/index.db` |
| `growth search "{query}"` | When you want to find something | terminal output only |

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
growth             CLI entry point — `growth premortem` / `growth reflect`
growthos/          CLI implementation (stdlib only): config, interview, backend, vault I/O
commands/growth/   Claude Code slash commands — now one-line pointers at the CLI
workflows/         Full orchestration docs — the actual asset; growthos/ just runs them
agents/            Scoring-rubric agents — read verbatim by growthos/prompt.py, never duplicated
templates/         Reference copies of the Obsidian note templates
cursor/            Cursor integration — skills, rule, slash commands, installer
install.sh         Links commands into ~/.claude/commands/growth/
config.example.json  Copy to config.json and edit (config.json is gitignored)
requirements-index.txt  Optional: sqlite-vec + fastembed, for semantic search
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
