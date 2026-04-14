---
phase: 03-habits-resources
plan: "01"
subsystem: obsidian-vault
tags: [resources, reading-queues, concept-articles, mocs]
dependency_graph:
  requires: [02-03]
  provides: [domain-reading-queues, resource-notes, moc-resource-links, concept-article-backfills]
  affects: [03-02, 03-03]
tech_stack:
  added: []
  patterns: [domain-queue-index, learning-resource-note, moc-resources-section]
key_files:
  created:
    - "Cashea/40-resources/coding-patterns-queue.md"
    - "Cashea/40-resources/system-design-queue.md"
    - "Cashea/40-resources/gcp-infra-queue.md"
    - "Cashea/40-resources/devops-queue.md"
    - "Cashea/40-resources/observability-queue.md"
    - "Cashea/40-resources/communication-queue.md"
    - "Cashea/40-resources/designing-data-intensive-applications.md"
    - "Cashea/40-resources/a-philosophy-of-software-design.md"
    - "Cashea/40-resources/clean-code.md"
    - "Cashea/40-resources/system-design-interview-vol-1.md"
    - "Cashea/40-resources/building-microservices.md"
    - "Cashea/40-resources/google-cloud-ace-study-guide.md"
    - "Cashea/40-resources/site-reliability-engineering.md"
    - "Cashea/40-resources/google-cloud-platform-in-action.md"
    - "Cashea/40-resources/accelerate.md"
    - "Cashea/40-resources/the-devops-handbook.md"
    - "Cashea/40-resources/the-phoenix-project.md"
    - "Cashea/40-resources/distributed-systems-observability.md"
    - "Cashea/40-resources/observability-engineering.md"
    - "Cashea/40-resources/on-writing-well.md"
    - "Cashea/40-resources/the-pyramid-principle.md"
  modified:
    - "Cashea/10-concepts/system-design/hexagonal-architecture.md"
    - "Cashea/10-concepts/backend/typeorm-repository-pattern.md"
    - "Cashea/10-concepts/backend/nestjs-guards.md"
    - "Cashea/10-concepts/backend/nestjs-interceptors.md"
    - "Cashea/10-concepts/infra/gcp-pubsub.md"
    - "Cashea/10-concepts/security/jwt-authentication.md"
    - "Cashea/10-concepts/security/rbac-permissions.md"
    - "Cashea/10-concepts/security/session-guard-pattern.md"
    - "Cashea/10-concepts/infra/apigee.md"
    - "Cashea/10-concepts/infra/structured-logging.md"
    - "Cashea/50-mocs/MOC-Backend.md"
    - "Cashea/50-mocs/MOC-System-Design.md"
    - "Cashea/50-mocs/MOC-Infra.md"
    - "Cashea/50-mocs/MOC-Observability.md"
    - "Cashea/50-mocs/MOC-Cashea-Architecture.md"
decisions:
  - "D-06/D-11: Book selections locked in CONTEXT.md applied as specified — DDIA in coding-patterns, SDI Vol 1 in system-design"
  - "hexagonal-architecture.md is at system-design/ not backend/ — correct path used without plan correction"
  - "structured-logging.md is a stub with no ## Resources to Go Deeper — section added inline (Rule 2: missing critical functionality)"
metrics:
  duration: "~15min"
  completed_date: "2026-04-14"
  tasks_completed: 2
  files_created: 21
  files_modified: 15
---

# Phase 03 Plan 01: Domain Resource Infrastructure Summary

**One-liner:** 6 prioritized domain reading queues + 15 book resource notes + podcast/video picks across all domains, linked from 10 concept articles and 5 MOC files.

## What Was Built

### Task 1: Domain Queue Indices + Individual Resource Notes (21 new files)

Created 6 domain queue index files in `Cashea/40-resources/`:
- `coding-patterns-queue.md` — DDIA active; A Philosophy of Software Design + Clean Code queued
- `system-design-queue.md` — System Design Interview Vol 1 active; Building Microservices queued
- `gcp-infra-queue.md` — Google Cloud ACE Study Guide active; SRE Book + GCP in Action queued
- `devops-queue.md` — Accelerate active; DevOps Handbook + Phoenix Project queued
- `observability-queue.md` — Distributed Systems Observability active; Observability Engineering queued
- `communication-queue.md` — On Writing Well active; The Pyramid Principle queued

Each queue index includes: active book, ordered queue, Done section (empty), Podcasts & Videos section with 3 picks (2 podcast + 1 video or mixed).

Created 15 individual resource notes — one per book — all following the `learning-resource.md` template structure with actual values (no Templater variables), full frontmatter (`date`, `tags`, `type`, `author`, `url`), `## Why This Resource` with a surfaced-by wikilink, `## What It Covers` with 2-3 bullets, `## Key Takeaways` (fill-later placeholder), `## Concepts This Deepened` with wikilinks, and `## Rating`.

### Task 2: Concept Article Backfills + MOC Links (15 files modified)

Replaced `(Phase 3 — leave empty)` placeholder in 10 concept articles with wikilinks to relevant resource notes:
- `hexagonal-architecture.md` → `[[a-philosophy-of-software-design]]`
- `typeorm-repository-pattern.md`, `nestjs-guards.md`, `nestjs-interceptors.md`, `gcp-pubsub.md`, `jwt-authentication.md`, `rbac-permissions.md` → `[[designing-data-intensive-applications]]`
- `session-guard-pattern.md`, `apigee.md` → `[[system-design-interview-vol-1]]`
- `structured-logging.md` → `[[distributed-systems-observability]]` (added section — see deviations)

Added `## Resources` section to 5 MOC files linking each to its domain queue index.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] hexagonal-architecture.md path correction**
- **Found during:** Task 2
- **Issue:** Plan listed `backend/hexagonal-architecture.md` but file lives at `system-design/hexagonal-architecture.md`
- **Fix:** Used correct path `system-design/hexagonal-architecture.md` for the Edit
- **Files modified:** `Cashea/10-concepts/system-design/hexagonal-architecture.md`
- **Commit:** 1a50db3

**2. [Rule 2 - Missing Critical Functionality] structured-logging.md is a stub without ## Resources to Go Deeper**
- **Found during:** Task 2
- **Issue:** `structured-logging.md` is a Phase 2 stub (only has `## What It Is` + `## Related Concepts`) — no `## Resources to Go Deeper` placeholder to replace
- **Fix:** Added `## Resources to Go Deeper` section with `[[distributed-systems-observability]]` wikilink after `## Related Concepts`
- **Files modified:** `Cashea/10-concepts/infra/structured-logging.md`
- **Commit:** 1a50db3

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| Task 1 | cf16e5f | feat(resources): create 6 domain queue indices and 15 resource notes |
| Task 2 | 1a50db3 | feat(resources): backfill concept article resource sections and link MOCs to queues |

## Known Stubs

None — all resource notes are complete for their intended purpose. The `## Key Takeaways` sections contain `*(Fill after consuming)*` placeholders, which is by design (books not yet read). The `## Rating` fields contain `/5 —` placeholders, also by design.

## Self-Check: PASSED
