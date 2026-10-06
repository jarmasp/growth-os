---
name: growth-premortem
description: >-
  Run a pre-mortem before coding on a ticket; writes a draft reflection to the
  vault. Use when the user runs /growth-premortem, /growth:premortem, or asks
  for a premortem before starting a ticket.
---

# Growth OS — Premortem

Standalone CLI now (v3.0). Tell the user to run this in a real terminal:

```bash
~/Documents/growth-os/growth premortem
```

Don't try to drive its interactive interview through Cursor's own tool calls — it
runs `input()` in a loop and expects a real terminal.

(Legacy path, no CLI available: read and follow `~/Documents/growth-os/workflows/premortem.md` completely.)
