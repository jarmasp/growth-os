# Phase 2: Knowledge Seed - Context

**Gathered:** 2026-04-13
**Status:** Ready for planning

<domain>
## Phase Boundary

Create ~40 cashea-backend concept article stubs + top-10 full articles in the Obsidian vault,
fully wikilinked, so that no ticket reflection is ever orphaned because the concept article
doesn't exist yet. After this phase, the graph has enough nodes that every ticket reflection
can link to at least one existing concept.

This phase does NOT set up deliberate practice habits or domain reading queues (Phase 3).
It seeds the knowledge graph so Phase 3's reflections have nodes to link to.
</domain>

<decisions>
## Implementation Decisions

### Stub Format
- **D-01:** Stubs use a **partial template**: frontmatter + one-liner description + `## What It Is`
  callout block (the guiding question prompt) + `## Related Concepts` wikilinks only.
  No empty deeper sections. When a stub is fleshed out to a full article later, the remaining
  template sections (D-08 from Phase 1) are applied at that time.
  - Frontmatter: `date`, `tags: [#concept, #domain]`, `confidence: low`
  - File naming: slug format in English (`nestjs-guards.md`, `typeorm-migrations.md`) per D-04
  - Each stub must have at minimum 2 wikilinks in `## Related Concepts` (SEED-03 requirement)

### Codebase Scan (Plan 02-01)
- **D-02:** Use **SEED-01 list as the base** (~40 predefined concepts from REQUIREMENTS.md),
  then enrich via two MCP sources:
  - **GitHub MCP** (READ ONLY): Scan cashea-backend src files to (a) verify whether CQRS is
    actually used and whether to include it, (b) find 1-2 key file paths per concept so stubs
    have real anchors, (c) discover any significant patterns not captured in SEED-01.
  - **Notion MCP** (READ ONLY): Read the cashea engineering wiki to surface concepts the team
    has already formally documented and to understand team-level vocabulary for each pattern.
- **D-03:** CRITICAL CONSTRAINT — **GitHub MCP and Notion MCP are READ-ONLY tools.**
  - Do NOT push to any GitHub repo except `cashea-knowledge-vault`
  - Do NOT write anything to Notion
  - Reads only, unless Jose explicitly specifies a repo and action
- **D-04:** If MCP scan surfaces concepts clearly missing from SEED-01 (i.e., patterns
  heavily used in cashea-backend but not listed), add them. Keep total stub count near ~40-50.
  Do not expand indefinitely — if a concept is minor, skip it.

### Full Articles (Plan 02-02)
- **D-05:** The 10 full articles cover: hexagonal architecture, NestJS guards, TypeORM repository
  pattern, Apigee API gateway, GCP Pub/Sub, JWT authentication, RBAC/permissions, NestJS
  interceptors, TypeORM migrations, session guard pattern.
- **D-06:** `## How We Use It in cashea-backend` section uses **file paths + one key snippet**:
  - Name the relevant file(s)/module(s) where the pattern lives
  - Show ONE concise code snippet that demonstrates the pattern (not a full class dump)
  - Snippets will be pulled via GitHub MCP during 02-02 execution — read only
  - Trade-off accepted: snippets may get stale as code evolves; this is acceptable for
    10 core concepts that change infrequently
- **D-07:** Full articles apply the complete D-08 template from Phase 1 (all 6 sections).
  `## Resources to Go Deeper` section: leave as stub-level (empty with callout prompt) during
  Phase 2 — resources are curated in Phase 3 at the moment of felt need, not in advance.

### Subdirectory Mapping
- **D-08:** Assignment rule — "What concept is being illustrated?" wins over "Where is it used?"
  - `backend/` — NestJS/TypeORM-specific implementations: NestJS guards, NestJS interceptors,
    NestJS pipes, NestJS modules, NestJS decorators, TypeORM repository pattern, TypeORM
    migrations, transaction-op pattern, DTO pattern, dependency injection, monorepo structure,
    npm scripts reference, health checks
  - `system-design/` — Architectural/structural patterns: hexagonal architecture, port/adapter
    pattern, hexagonal ports, domain events, CQRS (if used), repository pattern (abstract),
    REST API (concept), API gateway (concept), microservices (concept), load balancer (concept),
    API vs load balancer
  - `security/` — Auth/authz patterns: JWT authentication, session guard pattern, RBAC/permissions,
    Firebase authentication
  - `infra/` — Infrastructure and platform: Apigee, Apigee XML proxy configs, GCP Pub/Sub,
    GCP Cloud Run, Firebase integration, CI/CD pipeline, environment configuration,
    secret management (GCP Secret Manager), database migrations (TypeORM), foreign keys and
    relations, SQL transactions, structured logging

### Graph Wiring (Plan 02-03)
- **D-09:** Audit pass after all stubs and full articles are created. Every article — stub or
  full — must have at least 2 wikilinks pointing to other concept articles. No orphan nodes.
- **D-10:** After audit, verify in Obsidian graph view that the graph is visually connected
  (no isolated clusters). Dense clusters are expected: backend/ ↔ system-design/ for
  hexagonal concepts; security/ ↔ backend/ for guard/auth concepts.

### Claude's Discretion
- Exact wording of the one-liner descriptions for each concept stub
- Which specific code snippet to show in each full article's "How We Use It" section
- Additional wikilinks beyond the required minimum 2 (more is better)
- Whether CQRS makes the cut (decide based on GitHub MCP scan evidence)
- Any concepts surfaced via MCP that are clearly significant additions to SEED-01
</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — SEED-01 (exact ~40 concept list), SEED-02 (top-10 for full
  articles), SEED-03 (wikilink/graph requirements), CAPT-04 (stub minimum definition)

### Phase 1 Decisions (carry-forward)
- `.planning/phases/01-vault-foundation/01-CONTEXT.md` — D-04 (file naming), D-08 (concept
  article template structure: 6 sections, frontmatter), D-18 (vault folder structure and
  subdirectory paths)

### Project Context
- `.planning/PROJECT.md` — Core value, constraints, vault location
- `.planning/research/SUMMARY.md` — System architecture section (note types, vault structure),
  Design Constraints section (rules that govern the system)

### MCP Tooling (READ-ONLY)
- GitHub MCP endpoint: `https://api.githubcopilot.com/mcp/` — scan cashea-backend src files
  for concept verification and key file path anchors. READ ONLY.
- Notion MCP endpoint: `https://mcp.notion.com/mcp` — read cashea engineering wiki for
  team-documented concepts. READ ONLY.
- Vault write target: `cashea-knowledge-vault` repo (the only repo where write operations
  are currently authorized)

No external specs or ADRs beyond the above — all requirements are captured in these files.
</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- Concept article template (D-08 from Phase 1) — already designed; stubs use partial version,
  full articles use the complete 6-section template
- Vault folder structure at `Personal/Cashea/10-concepts/` with four subdirectories:
  `backend/`, `infra/`, `system-design/`, `security/` — Phase 2 populates these

### Established Patterns
- Phase 1 template style: `[!question]` callout blocks with 1-2 Spanish guiding questions
  per section. Stubs use this for `## What It Is` only.
- File naming: slug format in English (`nestjs-guards.md`), NOT Spanish titles
- Frontmatter: `date`, `tags: [#concept, #domain]`, `confidence: low|medium|high`

### Integration Points
- Vault path: `/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/`
- Concept articles live in: `10-concepts/{backend|infra|system-design|security}/`
- cashea-backend codebase (source for GitHub MCP scan): `/Users/thyfus/Documents/cashea-backend/cashea-backend/src/`
- Obsidian wikilinks format: `[[concept-slug]]` or `[[concept-slug|Display Name]]`
</code_context>

<specifics>
## Specific Ideas

- "Both GitHub MCP and Notion MCP" — use both data sources during 02-01 concept scan.
  GitHub for code-grounded file path anchors; Notion for team vocabulary and formally
  documented patterns. Both are READ-ONLY — no writes except to `cashea-knowledge-vault`.
- "File paths + one key snippet" — the How We Use It section should be concrete but not
  a code dump. One snippet showing the pattern, not a whole class.
- Partial template for stubs — not bare minimum, not full template. Frontmatter + one-liner
  + What It Is callout + Related Concepts. Expandable later without restructuring.
</specifics>

<deferred>
## Deferred Ideas

- Resources curation in concept articles — Phase 3. `## Resources to Go Deeper` sections
  are left as empty callout prompts in Phase 2; filled at moment of felt need in Phase 3.
- QuickAdd, Advanced URI, Obsidian Spaced Repetition — v2 requirements (deferred from Phase 1)
- Team ADR adoption via Notion — separate conversation with the team; out of scope

None — discussion stayed within Phase 2 scope.
</deferred>

---

*Phase: 02-knowledge-seed*
*Context gathered: 2026-04-13*
