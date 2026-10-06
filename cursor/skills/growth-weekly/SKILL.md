---
name: growth-weekly
description: >-
  Generate the end-of-sprint weekly review in the Obsidian vault. Use when the
  user runs /growth-weekly, /growth:weekly, or asks for a weekly growth review.
---

# Growth OS — Weekly Review

Standalone CLI now (v3.0). Tell the user to run this in a real terminal:

```bash
~/Documents/growth-os/growth weekly
```

It runs the interview, scores the week (rubric: `agents/weekly-reviewer.md`), writes
the note, and finishes by triaging `00-inbox/` (shows a plan, waits for confirmation).
Don't try to drive its interview or the inbox confirmation through Cursor's tool calls.

(Legacy path, no CLI available: read and follow `~/Documents/growth-os/workflows/weekly-review.md`
completely, adopting `~/Documents/growth-os/agents/weekly-reviewer.md` as the scoring persona.)
