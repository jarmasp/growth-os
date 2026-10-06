---
name: growth-weekly
description: >-
  Generate the end-of-sprint weekly review in the Obsidian vault. Use when the
  user runs /growth-weekly, /growth:weekly, or asks for a weekly growth review.
---

# Growth OS — Weekly Review

## Setup

```bash
GROWTH_OS_HOME="${GROWTH_OS_HOME:-$HOME/Documents/growth-os}"
cat "$GROWTH_OS_HOME/config.json"
```

## Execute

1. Read and follow **`$GROWTH_OS_HOME/workflows/weekly-review.md`** completely. Do not skip or reorder steps.
2. Template: **`$GROWTH_OS_HOME/templates/weekly-review.md`**.

Do not fill skill-domain self-ratings — that is the user's job.

## Weekly reviewer agent (mandatory)

Whenever the workflow invokes scoring or structured weekly analysis:

1. Read **`$GROWTH_OS_HOME/agents/weekly-reviewer.md`** in full before scoring or summarizing.
2. **Adopt that file as your persona** for review/scoring — W1–W5 dimensions, evidence rules, capability-assertion quality, and output blocks come from the agent, not from general coaching instinct.
3. Use the user's answers **verbatim** where the workflow requires it; do not paraphrase away nuance before scoring.
4. Apply the rubric **as written** — do not improvise dimensions, rename W1–W5, or soften criteria.
5. Follow vault-driven resource recommendations only (as the agent specifies); do not invent external links or courses.
