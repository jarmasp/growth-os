---
name: growth-reflect
description: >-
  Write a ticket reflection note in the Obsidian vault after work is done.
  Use when the user runs /growth-reflect, /growth:reflect, asks to reflect
  on a ticket, or wants a post-mortem learning note in Growth OS.
---

# Growth OS — Reflect

## Setup

```bash
GROWTH_OS_HOME="${GROWTH_OS_HOME:-$HOME/Documents/growth-os}"
cat "$GROWTH_OS_HOME/config.json"
```

## Execute

1. Read and follow **`$GROWTH_OS_HOME/workflows/reflect.md`** completely (interactive interview, then vault write). Do not skip or reorder steps.
2. Template reference: **`$GROWTH_OS_HOME/templates/ticket-reflection.md`**.

Ask for branch, ticket ID, and short description upfront — do not infer from git alone.

## Scoring agent (mandatory)

When the workflow reaches the `score` step:

1. Read **`$GROWTH_OS_HOME/agents/reflection-scorer.md`** in full before scoring.
2. **Adopt that file as your persona** for scoring only — tone, rubric, dimension definitions (D1–D5), score ranges, and output format are defined there, not by you.
3. Pass the scorer exactly what `reflect.md` specifies (`TICKET`, `PATTERN`, `FILES`, `Q1`–`Q4` verbatim).
4. Apply the rubric **as written** — do not improvise dimensions, weights, or feedback style.
5. Write scores to the vault and terminal **exactly** as the scorer and workflow require (raw integers D1–D5, `TOTAL` 0–10, no fractions).
