---
name: growth-reflect
description: >-
  Write a ticket reflection note in the Obsidian vault after work is done.
  Use when the user runs /growth-reflect, /growth:reflect, asks to reflect
  on a ticket, or wants a post-mortem learning note in Growth OS.
---

# Growth OS — Reflect

Standalone CLI now (v3.0). Tell the user to run this in a real terminal:

```bash
~/Documents/growth-os/growth reflect
```

It runs the interview, calls the model once to score the reflection (rubric:
`agents/reflection-scorer.md`), and writes the scored note + ledger row itself.
Don't try to drive its interactive interview through Cursor's own tool calls — it
runs `input()` in a loop and expects a real terminal.

`--agent codex` or `--agent print` switch the model backend; `--agent print` just
prints the assembled prompt instead of calling anything.

(Legacy path, no CLI available: read and follow `~/Documents/growth-os/workflows/reflect.md`
completely, adopting `~/Documents/growth-os/agents/reflection-scorer.md` as the scoring persona.)
