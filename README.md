<div align="center">

# 🌱 Growth OS

**A personal engineering growth operating system that turns daily work into compounding skill.**

*The work IS the practice — no synthetic side projects, no separate study time.*

[![Standalone CLI](https://img.shields.io/badge/Runs%20as-standalone%20CLI-2ea44f)](#-quick-start)
[![Runs on Obsidian](https://img.shields.io/badge/Runs%20on-Obsidian-7c3aed)](https://obsidian.md)
[![Claude Code / Cursor optional](https://img.shields.io/badge/Claude%20Code%20%2F%20Cursor-optional-d97757)](#optional-editor-integration)
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
   ├─▶  growth premortem       before coding  ·  predict failure points, capture assumptions
   │
   ├─▶  growth reflect         after coding   ·  complete the draft, score prediction vs reality
   │
   ├─▶  growth concept "{x}"   any time       ·  expand an unclear pattern into a full article
   │
   └─▶  growth weekly          sprint end     ·  surface gaps, rate domains, assert capability
```

Runs as a plain CLI in any terminal — no editor required. `/growth:*` slash commands still
work in Claude Code / Cursor if you want them (see [Optional editor integration](#optional-editor-integration)).

Over time: reflection scores trend up · the knowledge graph densifies · self-doubt drops.

---

## 🧩 What It's Built On

| Layer | Tool | Role |
|-------|------|------|
| Knowledge graph | [**Obsidian**](https://obsidian.md) | Local-first notes with Dataview, Templater & Tasks |
| Automation | A standalone Python CLI (`growth <command>`), stdlib only | Runs in any terminal. Each command calls a model backend at most once (`--agent claude\|codex\|print`, or a custom one from `config.json`) — `claude`/Claude Code is one supported backend, not a requirement |
| Fuel | **Your actual work** | Every ticket is a learning artifact, not extra work |

---

## 🚀 Quick Start

**1. Clone**

```bash
git clone git@github.com:jarmasp/growth-os.git ~/Documents/growth-os
```

**2. Install**

```bash
bash ~/Documents/growth-os/install.sh
```

Writes `~/.growth-os/config.json` (`growth init`), runs `growth doctor` so you can see
what's active (backends found, vector search available or not), and links `growth` onto
your `PATH` if `~/.local/bin` is on it. Stdlib only — no `pip install` required for this step.

**3. Point it at your vault**

Edit the config path `install.sh` printed (`~/.growth-os/config.json`) so `vault_root`
points to a folder **inside** your Obsidian vault:

```json
{
  "vault_root": "/Users/you/Documents/obsidian/personal/Work",
  "vault_name": "YourVaultName",
  "project_name": "your-project-name"
}
```

**4. Onboard, premortem, reflect, concept, weekly**

```bash
growth onboard
growth premortem
growth reflect
growth concept "nestjs interceptors"
growth weekly
```

(No PATH link from step 2? Call `~/Documents/growth-os/growth <command>` instead.)

Only `growth onboard`'s interview is genuinely multi-turn (the model picks each next
question); the rest call the model at most once, statelessly, or not at all
(`growth premortem` is pure templating). `--agent claude|codex|print` picks the backend
per call — `print` dumps the assembled prompt to stdout instead of calling anything, so
you can paste it into any model anywhere (not available for `onboard`, which needs a
real back-and-forth).

**`growth index` / `growth search "{query}"`** build and query a local hybrid
(keyword + semantic) store over your vault — `pip install -r requirements-index.txt`
for the semantic half, or skip it and get keyword search alone. `reflect`/`weekly` use
it internally to pick relevant `[[concept]]` links and to ground scoring feedback in
your own past sessions (see Grounding below).

**`growth index --corpus` / `growth ask "{query}"`** add a corpus: 16 original
writeups of the frameworks the agents already apply (Kolb, Ericsson, SDT,
Immunity to Change, Dreyfus...) shipped with the repo — distilled and cited,
never the source books' own text, same delivery as `workflows/`/`agents/` — plus
whatever you point `personal_corpus_dir` at (your own books/docs, `.epub`/`.pdf`
supported, gitignored, local only). See [HOW-TO-USE.md](./HOW-TO-USE.md) for the
full design.

**Grounding (v3.0 Phase 4):** `reflect`/`weekly` retrieve relevant corpus passages and
your own past sessions before scoring, and the rubric cites them by name only when
genuinely relevant — never a fabricated citation. Both rubrics also carry an explicit
scope boundary: this is a work-reflection tool, not a mental health one, and says so if
a conversation drifts there. Full detail in [HOW-TO-USE.md](./HOW-TO-USE.md).

**Multi-user:** everything lives under your own `~/.growth-os/` (config, index, logs)
and your own vault — nothing shared, no server, no telemetry. A teammate running
`install.sh` on their machine gets their own isolated setup from the same clone.

### Optional: editor integration

Growth OS works entirely from the terminal — this is optional, for `/growth:*` slash
commands inside an editor:

```bash
bash ~/Documents/growth-os/install-claude-code.sh   # Claude Code
bash ~/Documents/growth-os/cursor/install-cursor.sh  # Cursor
```

Each slash command is a one-line pointer at the same CLI — no separate logic to keep in sync.

---

## 🛠️ Commands

| Command | When | Writes to |
|---------|------|-----------|
| `growth onboard` | Once on setup · re-run to update profile | `config.json` + vault scaffold |
| `growth premortem` | Before coding starts on a ticket | `20-tickets/{ticket}-draft.md` |
| `growth reflect` | After resolving a ticket | `20-tickets/{ticket}.md` |
| `growth concept "{name}"` | When a pattern felt unclear | `10-concepts/{domain}/{slug}.md` |
| `growth weekly` | End of sprint / every Friday | `30-weekly/{YYYY-[W]WW}.md` |
| `growth index [--corpus]` | After new notes, or anytime | `~/.growth-os/index.db` |
| `growth search "{query}"` | When you want to find something | terminal output only |
| `growth ask "{query}"` | When you want a grounded coaching passage | terminal output only |

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
corpus/            Shipped framework writeups (scope: shared) — see HOW-TO-USE.md
cursor/            Cursor integration — skills, rule, slash commands, installer
install.sh         Primary installer — growth init + growth doctor + PATH link
install-claude-code.sh  Optional: links commands into ~/.claude/commands/growth/
config.example.json  Template for ~/.growth-os/config.json (written by `growth init`)
requirements-index.txt   Optional: sqlite-vec + fastembed, for semantic search
requirements-corpus.txt  Optional: ebooklib + pypdf, for .epub/.pdf in your personal corpus
HOW-TO-USE.md      Full installation & usage guide
DEMO.md            Live walkthrough script for presenting growth-os to a team
```

> **Privacy:** `config.json`, project-specific configs (`config.*.json`), `.planning/`, and
> `SESSION-*.md` notes are gitignored — your profile and work notes never leave your machine.
> `personal_corpus_dir` points at a folder of your own choosing, outside this repo entirely —
> nothing about your personal corpus is ever written here.

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
