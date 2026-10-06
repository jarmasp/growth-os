---
name: growth-onboard
description: >-
  Run the Growth OS onboarding interview; builds user profile and scaffolds the
  Obsidian vault. Use when the user runs /growth-onboard, /growth:onboard, or
  sets up Growth OS for the first time.
---

# Growth OS — Onboard

## Setup

```bash
GROWTH_OS_HOME="${GROWTH_OS_HOME:-$HOME/Documents/growth-os}"
cat "$GROWTH_OS_HOME/config.json"
```

## Execute

1. Read **`$GROWTH_OS_HOME/agents/onboarding-agent.md`** in full **before** the first question.
2. **Adopt that file as your persona** for the entire session — interview tone, 5-phase structure, frameworks (SDT, Ikigai, Immunity to Change, Kolb, Dreyfus, Flow), and what to probe vs skip are defined there.
3. Read and follow **`$GROWTH_OS_HOME/workflows/onboarding.md`** completely in lockstep with the agent. Do not skip phases or merge them unless the agent allows it.
4. Save profile to `config.json` and scaffold vault sections exactly as the workflow specifies.

Do not run a generic onboarding chat — if a step is not in the agent + workflow, do not add it.

Run once for initial setup; re-run only when the user wants to refresh their profile.
