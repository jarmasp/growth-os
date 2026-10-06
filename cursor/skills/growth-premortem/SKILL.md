---
name: growth-premortem
description: >-
  Run a pre-mortem before coding on a ticket; writes a draft reflection to the
  vault. Use when the user runs /growth-premortem, /growth:premortem, or asks
  for a premortem before starting a ticket.
---

# Growth OS — Premortem

## Setup

```bash
GROWTH_OS_HOME="${GROWTH_OS_HOME:-$HOME/Documents/growth-os}"
cat "$GROWTH_OS_HOME/config.json"
```

## Execute

1. Read and follow **`$GROWTH_OS_HOME/workflows/premortem.md`** completely.
2. Writes draft with `status: in-progress` in the vault tickets folder.
3. After the ticket is done, user should run **growth-reflect** (detects the draft automatically).
