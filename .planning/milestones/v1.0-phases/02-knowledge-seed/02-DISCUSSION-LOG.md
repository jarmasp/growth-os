# Phase 2: Knowledge Seed - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in CONTEXT.md — this log preserves the Q&A trail.

**Date:** 2026-04-13
**Phase:** 02-knowledge-seed
**Mode:** discuss
**Areas discussed:** Stub format, Codebase scan scope, Code reference depth, Subdirectory mapping

---

## Gray Areas Presented

| Area | Questions Covered | Selected by user |
|------|-------------------|-----------------|
| Stub format | Bare min vs. partial template vs. full template with blanks | Yes |
| Codebase scan scope | SEED-01 only vs. +GitHub MCP vs. +GitHub+Notion MCP | Yes |
| Code reference depth | Prose only vs. file paths only vs. file paths + snippet | Yes |
| Subdirectory mapping | Backend-default rule vs. architecture-in-system-design rule | Yes |

---

## Carrying Forward from Phase 1

- D-02–D-04: Bilingual strategy (English headers, Spanish callouts) — applies to concept articles
- D-04: File naming: slug format in English
- D-08: Concept article template (6 sections, frontmatter) — Phase 2 uses partial version for stubs
- D-18: Vault folder structure with `10-concepts/{backend|infra|system-design|security}/` subdirs

---

## Discussion Q&A

### Stub format
- **Question:** What should a Phase 2 stub contain? Bare min, partial template, or full template with blanks?
- **Options presented:** Bare minimum (recommended) / Partial template / Full template with blanks
- **User selected:** Partial template
- **Decision captured:** Frontmatter + one-liner + `## What It Is` callout + `## Related Concepts` wikilinks

### Codebase scan scope
- **Question:** How should the executor source concept data for 02-01?
- **Options presented:** SEED-01 only / SEED-01 + GitHub MCP (recommended) / SEED-01 + GitHub + Notion MCP
- **User selected:** SEED-01 + GitHub + Notion MCP
- **User notes:** GitHub MCP available at `https://api.githubcopilot.com/mcp/`; Notion MCP at `https://mcp.notion.com/mcp`; Postman MCP also available but not relevant
- **Decision captured:** Both MCP sources used for enrichment — READ ONLY on both

### Code reference depth
- **Question:** For 10 full articles, how specific should "How We Use It in cashea-backend" be?
- **Options presented:** File paths + one key snippet (recommended) / File paths only / Prose only
- **User selected:** File paths + one key snippet (recommended)
- **Decision captured:** One concise snippet showing the pattern, not a full class

### Subdirectory mapping
- **Question:** Tiebreaker rule for cross-domain concepts across backend/, infra/, system-design/, security/?
- **Options presented:** Architecture in system-design (recommended) / Backend default for app code
- **User selected:** Architecture in system-design (recommended)
- **Decision captured:** Architectural/structural concepts → system-design/; NestJS/TypeORM implementations → backend/; auth/authz → security/; GCP/DevOps/Apigee → infra/

---

## Critical Constraint (from user notes during discussion)

**GitHub MCP and Notion MCP are READ-ONLY tools for this project.**
- Do NOT push to any GitHub repo except `cashea-knowledge-vault`
- Do NOT write anything to Notion
- This constraint applies to ALL downstream agents (researcher, planner, executor)
- Source: User's explicit instruction during gray area discussion (2026-04-13)

---

## No Corrections Made

All 4 decisions were first-selection picks with no revisions.

---

## No External Research Performed

Codebase scout was lightweight — primary sources were REQUIREMENTS.md (SEED-01 list),
Phase 1 CONTEXT.md (template decisions), and ROADMAP.md (phase plan breakdown).
