# Growth OS

Personal engineering growth system. Jose IS the project.

## Config

```bash
cat ~/Documents/growth-os/config.json
```

Vault path and section names live in config.json — always read it before writing to the vault.

## What This Is

Turns daily cashea-backend work into compounding skill growth.
Every ticket → reflection → concept wikilinks → knowledge graph grows.

**Core value:** Every sprint leaves a knowledge artifact.

## Commands

- `/reflect` — ticket reflection after resolving a branch
- `/concept {name}` — write or expand a concept article  
- `/weekly` — end-of-sprint review

Commands load their full workflow from `workflows/`. Read those files for full orchestration details.

## Planning

Active state: `.planning/STATE.md`
Roadmap: `.planning/ROADMAP.md`
Milestone history: `.planning/milestones/`

## Separation of Concerns

This repo: building Jose.
GSD (cashea-backend): building software.

Do not mix concerns. `/reflect` belongs here. `/deslop` and `/review-pr` belong to GSD.
