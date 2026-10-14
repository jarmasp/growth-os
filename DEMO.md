# Demo script — presenting Growth OS to the team

A ~12-minute live walkthrough, plus a no-model fallback if a live model call misbehaves on
stage. Targets an engineering team that already knows GSD/Claude Code — the pitch is "this is
the same discipline, pointed at you instead of the code."

## Before the demo

Use a **throwaway demo vault + config**, never your real one — your real reflections are
personal (candor about what you got wrong, team friction, etc.) and shouldn't be read live.

```bash
mkdir -p /tmp/growth-os-demo/vault
GROWTH_OS_CONFIG=/tmp/growth-os-demo/config.json
export GROWTH_OS_CONFIG
cp ~/Documents/growth-os/config.example.json "$GROWTH_OS_CONFIG"
# edit $GROWTH_OS_CONFIG: vault_root -> /tmp/growth-os-demo/vault, vault_name -> "Demo",
# project_name -> whatever the team's actual project is called (makes it feel real)
~/Documents/growth-os/growth onboard      # do this once, beforehand, off-stage
~/Documents/growth-os/growth index --corpus
```

`GROWTH_OS_CONFIG` overrides config resolution for every command in this shell — nothing
touches `~/.growth-os` or your real vault. Open the demo vault in Obsidian ahead of time so
the note appears live when you write it.

**Rehearse once end-to-end before presenting** — `growth reflect`'s interview has no
undo once it writes a note. Have a second ticket ready in case the first run needs a retry.

## Script

**1. Open with the problem (1 min)**
> "We leave GSD's planning discipline behind on day one — a sprint ends, nobody wrote down
> what they actually learned, and the same mistake repeats in three months. Growth OS is the
> same `.planning/`-style discipline, pointed at the engineer instead of the code."

**2. The loop, on the whiteboard/slide (1 min)** — use the diagram from `README.md`'s
"The Loop" section: premortem → code → reflect → concept → weekly.

**3. Live: `growth reflect` on a real-shaped ticket (4 min)**

```bash
growth reflect
```

Answer the four questions **with a genuinely mediocre first answer** on purpose (e.g. "I
should have been more careful" for the "what would you change" question) — the score comes
back low, and that's the point: it's live proof the rubric isn't a participation trophy.
Walk through the score breakdown as it prints, then open the written note in Obsidian so
they see the frontmatter + the `[[concept]]` wikilinks it picked automatically.

**4. Live: a second reflection with a sharper answer (3 min)**

Same ticket shape, but this time give a real structural cause and a concrete next action.
Show the score jump and read the one `GROUNDING` line where the rubric cites a framework by
name (Argyris/Kolb/whichever one actually matched) — this is the moment to say:

> "It only cites a framework when it actually retrieved a real passage — never free-associated
> psychology. Same guardrail against inventing a source that GSD's own docs use against
> inventing a fact."

**5. `growth weekly` — the trend (2 min)**

```bash
growth weekly
```

Skip to the output once the interview's answered — point at the recommendations block and
the score trend table in the written note. This is the "compounding" argument: show that a
second scored week visibly references the first week's gap.

**6. Close (1 min)**
> "Stdlib-only CLI, runs in your own terminal, your own `~/.growth-os/`, your own vault —
> nothing shared, no server. `bash install.sh` and you're onboarding in two minutes."

## Fallback: no live model call

If the model backend is unreachable or rate-limited mid-demo, don't debug live — switch to
`--agent print`:

```bash
growth reflect --agent print
```

This prints the exact assembled prompt (rubric + your answers + grounding) instead of calling
a model. Narrate it as "here's exactly what gets sent — no black box" and paste it into
whatever model you have open as a recovery, or just talk through the rubric file
(`agents/reflection-scorer.md`) directly.

## Anticipated questions

- **"Does this read my code?"** No — `growth concept` greps the *current directory* only
  when you explicitly ask it to write an article, and only to ground that one article.
  Nothing is indexed or uploaded automatically.
- **"Where does my reflection text go?"** Wherever `--agent` points: `claude -p` / `codex
  exec` as a subprocess on your machine, or nowhere at all with `--agent print`. No growth-os
  server exists.
- **"Can I use this without Obsidian?"** Not today — the vault structure (`20-tickets/`,
  `10-concepts/`, Dataview queries) is Obsidian-shaped. The CLI itself doesn't require Claude
  Code or Cursor, but it does write Markdown into an Obsidian vault layout.
- **"Is my score visible to anyone else?"** No — it's a file in your own vault. Nothing is
  aggregated or reported anywhere unless you choose to share it.
