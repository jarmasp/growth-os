# Engineering Growth OS

## What This Is

A personal engineering growth operating system built on top of daily work at cashea-backend.
Every ticket, bugfix, and architectural decision becomes a deliberate learning moment —
documented in an interconnected Obsidian knowledge graph, paired with curated resources
tied to real skill gaps, and executed through biweekly GSD sprints.

This is survival and ambition in the same motion: ship better work today while compounding
the capability to ship even better work tomorrow.

## Core Value

Every sprint leaves a knowledge artifact — so pattern gaps shrink, self-doubt reduces,
and the next sprint is faster and more confident than the last.

## Requirements

### Validated

- ✓ Vault folder structure + git sync — v1.0 (Phase 1: 11-dir structure, 7 notes migrated, git remote to cashea-knowledge-vault)
- ✓ All 8 Obsidian plugins installed and configured — v1.0 (Phase 1: data.json pre-written, all plugins confirmed active)
- ✓ Templater templates for ticket reflection, concept article, weekly review, survival review, learning resource — v1.0 (Phase 1: 5 templates + tag taxonomy + workflow rules)
- ✓ MOC navigation files (6 domains) with Dataview queries — v1.0 (Phase 1: MOC-Backend, Infra, System-Design, Cashea-Architecture, Observability, External-Services)
- ✓ `deslop` and `review-pr` Claude Code skills — v1.0 (Phase 1: both skill files verified present with meaningful content)
- ✓ Initial concept scan of cashea-backend — v1.0 (Phase 2: 39 stubs across backend/system-design/security/infra)
- ✓ Interconnected wiki: each concept article links to sub-concepts — v1.0 (Phase 2: all 43 files >= 2 wikilinks, 0 orphan nodes)
- ✓ Consistent article template with all 6 sections + real code snippets — v1.0 (Phase 2: 10 full articles)
- ✓ Resources organized by domain with contextual curation — v1.0 (Phase 3: 6 domain queues, 15 resource notes, podcast/video picks per domain)
- ✓ Homework log with recurring practice drills — v1.0 (Phase 3: PR rewrite, naked system design, one-concept deepening)
- ✓ Pre-mortem habit in ticket reflection template — v1.0 (Phase 3: Pre-mortem + Assumptions sections baked into template)

### Active

#### Sprint Habits (Next Milestone)

- [ ] One full sprint cycle completed using the system — pre-mortem before coding, reflection at ticket close, weekly review written
- [ ] System design improvement pathway (exercises, resources, applied practice)
- [ ] GCP/infra learning pathway (monitoring, deployment, cost management)
- [ ] Observability: metrics, logs, traces — detecting issues before they become incidents
- [ ] Communication improvement: team writing (PRs, tickets, comments), technical docs, non-technical docs

#### Domain Mastery

- [ ] GCP/ACE exam structured preparation path
- [ ] Advanced vault integrations when core habit is stable (QuickAdd, Advanced URI)

### Out of Scope

- Generic learning lists not tied to real work — resources must connect to actual skill gaps
- Theoretical learning without cashea-backend application as the anchor
- Separate personal project as practice vehicle — cashea-backend work IS the practice

## Context

**Who:** Jose — Venezuelan software engineer at cashea-backend. $1800/month.
Financial pressure is real and constant. Work is the escape and the lever. Survival
and professional growth are the same goal.

**Current bottlenecks (from self-assessment):**
- Upstream ambiguity — building technical solutions to conceptual problems because
  requirements aren't clear; having to ask and re-ask
- Pattern gaps — rediscovering patterns from scratch rather than drawing on a library
- Self-doubt — understanding the approach but hesitating mid-build
- Brittle design — shipping fast, then rebuilding when design breaks under real conditions

**Communication gaps:** team writing (PRs, tickets, comments), technical documentation
(architecture docs, ADRs), non-technical product and business documentation.

**Technical environment:** cashea-backend — NestJS/TypeScript, hexagonal architecture.
Obsidian vault at `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea`.

**External context:** GitHub MCP and Notion MCP for team/work context — colleagues,
superiors, work style, and sprint tracking.

## Constraints

- **Git:** `.claude/` and `.planning/` are never committed — local-only
- **Commits:** Conventional commits; scope = domain (e.g. `feat(stores):`) not phase numbers
- **Token economy:** Prefer efficient agents; don't burn tokens on redundant steps
- **Obsidian:** Full feature use — install plugins as needed (Dataview, Templater, Excalidraw, Tasks)
- **Tooling:** Default to existing codebase patterns before introducing new libraries

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Obsidian as knowledge graph | Richer linking + graph view + local-first; Notion handles team/sprint context | ✓ v1.0 — working well |
| Domain-scoped commits | Scope reveals which system is touched, not GSD internals | ✓ v1.0 |
| cashea-backend work as primary practice vehicle | No synthetic side project — real work IS the exercise | ✓ v1.0 |
| Weekly reflection baked into workflow | Process improvement can't be optional; must be a forcing function | ✓ v1.0 |
| Contextual curation over reading lists | Resources tied to real gaps land better than curated-in-advance lists | ✓ v1.0 — 6 domain queues + concept article backlinks |
| Vault frozen for 8 weeks post-setup | No structural changes during first two milestones — let habits form first | ✓ v1.0 — still in effect until v1.2 |
| D-01 stub format (minimal): frontmatter + one-liner + wikilinks only | Lightweight enough for bulk creation, invites expansion naturally | ✓ v1.0 — 39 stubs seeded successfully |
| Pre-mortem first in template (before-coding ritual) | Positions it as planning, not retrospective — changes usage pattern | ✓ v1.0 — baked into ticket-reflection.md |
| Git init at vault root, not cashea-backend subfolder | Keeps vault repo separate, clean history | ✓ v1.0 |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd:transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

## Context

**Current state (v1.0):** Obsidian vault at `Personal/Cashea/` with 82 .md files — 43 concept articles (39 stubs + 10 full), 5 templates, 6 MOC files, 6 domain resource queues, 15 book notes, 1 homework log. Knowledge graph connected with 0 orphan nodes. Pre-mortem ritual baked into ticket-reflection template. Git-synced to private `cashea-knowledge-vault` repo (jarmasp account).

**Next milestone (v2.0):** System must run for one full sprint cycle before planning domain mastery phases. Jose completes sprint using system — pre-mortem, reflection, weekly review — without it feeling like extra work. Then v2.0 activates domain learning paths.

---
*Last updated: 2026-04-14 after v1.0 milestone — Growth OS Live*
