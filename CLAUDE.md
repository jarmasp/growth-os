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

- `/growth:onboard` — run once to set up profile and scaffold vault
- `/growth:premortem` — run BEFORE coding starts on a ticket; captures predictions and writes a draft note
- `/growth:reflect` — run AFTER ticket resolves; detects pre-mortem draft if one exists and completes the note
- `/growth:concept {name}` — write or expand a concept article
- `/growth:weekly` — end-of-sprint review

Commands load their full workflow from `workflows/`. Read those files for full orchestration details.

## Planning

Active state: `.planning/STATE.md`
Roadmap: `.planning/ROADMAP.md`
Milestone history: `.planning/milestones/`

## Separation of Concerns

This repo: building you.
Your project codebase: building software.

Do not mix concerns. `/growth:reflect` belongs here. Code-focused commands belong to your project repo.
