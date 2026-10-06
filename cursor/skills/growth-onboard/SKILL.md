---
name: growth-onboard
description: >-
  Run the Growth OS onboarding interview; builds user profile and scaffolds the
  Obsidian vault. Use when the user runs /growth-onboard, /growth:onboard, or
  sets up Growth OS for the first time.
---

# Growth OS — Onboard

Standalone CLI now (v3.0). Tell the user to run this in a real terminal:

```bash
~/Documents/growth-os/growth onboard
```

The interview is genuinely adaptive — the model picks each next question from the
conversation so far (persona: `agents/onboarding-agent.md`) — so it needs a real
back-and-forth in a terminal. Don't try to conduct it through Cursor's tool calls.

(Legacy path, no CLI available: read `~/Documents/growth-os/agents/onboarding-agent.md`
in full, adopt it as persona, then read and follow `~/Documents/growth-os/workflows/onboarding.md`.)
