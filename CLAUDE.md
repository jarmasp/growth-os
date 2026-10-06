# Growth OS

Personal engineering growth system. You are the project.

## Config

```bash
cat ~/Documents/growth-os/config.json
```

Vault path and section names live in config.json — always read it before writing to the vault.

### Config Fields

| Field | Purpose | Edit? |
|-------|---------|-------|
| `vault_root` | Absolute path to vault subfolder | Once, before `/growth:onboard` |
| `vault_name` | Vault display name used in Dataview queries | Safe to change |
| `project_name` | Main codebase/project name | Safe to change |
| `concept_domains` | Subdomain folders in `10-concepts/` | Set by `/growth:onboard` — do not edit manually; changing it requires renaming vault folders |
| `vault.*` | Section subfolder names (tickets, concepts, etc.) | Set once, stable |
| `project_docs_subfolders` | Subfolders in `60-project/` | Set by `/growth:onboard` |

> `concept_domains` is managed by `/growth:onboard`. If you change it manually after
> initial setup, you must also rename the corresponding folders in your vault.

## What This Is

Turns daily work into compounding skill growth.
Every ticket → reflection → concept wikilinks → knowledge graph grows.

**Core value:** Every sprint leaves a knowledge artifact.

## Commands

As of v3.0, all five run as a standalone Python CLI (`growthos/`), not inline Claude
Code workflows — `commands/growth/*.md` are now one-line pointers at it:

- `growth onboard` — run once to set up profile and scaffold vault; re-run to update. The
  one multi-turn command — adaptive interview, persona in `agents/onboarding-agent.md`
- `growth premortem` — run BEFORE coding starts on a ticket; captures predictions, writes a draft note
- `growth reflect` — run AFTER ticket resolves; detects a pre-mortem draft if one exists and completes the note
- `growth concept "{name}"` — write or expand a concept article
- `growth weekly` — end-of-sprint review, then triages `00-inbox/`

The workflows in `workflows/` and the rubrics/personas in `agents/` are still the actual
asset — `growthos/` reads them at call time rather than duplicating them. Read those
files for full orchestration detail; read `growthos/cli.py` for how each one is run.
If you're asked to help with `growth-os` itself (not a `/growth:*` command on someone's
own ticket), this is the entry point, not `workflows/`.

## Separation of Concerns

This repo: building you.
Your project codebase: building software.

Do not mix concerns. `/growth:reflect` belongs here. Code-focused commands belong to your project repo.
