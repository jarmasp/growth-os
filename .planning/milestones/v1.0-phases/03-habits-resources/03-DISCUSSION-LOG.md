# Phase 3: Habits & Resources - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in CONTEXT.md — this log preserves the discussion.

**Date:** 2026-04-13
**Phase:** 03-habits-resources
**Mode:** discuss
**Areas discussed:** Pre-mortem template, Book selection, Homework log, Domain queue organization

---

## Gray Areas Presented

| Area | Selected for discussion? |
|------|--------------------------|
| Pre-mortem template design | ✓ |
| Book selection per domain | ✓ |
| Homework log structure | ✓ |
| Domain queue organization in 40-resources/ | ✓ |

---

## Decisions Made

### Pre-mortem Template Design
| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Format | Callout + Spanish prompts | Consistent with Phase 1 template style (D-05/D-06) |
| Position in template | First section (before What Was Hard) | Pre-mortem is before coding, not retrospective |
| 3 questions | Business context / 3 failure points / Design pattern | From PRAC-01 requirements exactly |

### Book Selections

| Domain | Queue Order |
|--------|-------------|
| Coding patterns | DDIA (active) → A Philosophy of Software Design → Clean Code/Clean Architecture |
| System design | System Design Interview Vol 1 (active) → Building Microservices |
| GCP/infra | Official GCP ACE Study Guide (active) → SRE Book → GCP in Action |
| DevOps | Accelerate (active) → The DevOps Handbook → The Phoenix Project |
| Observability | Distributed Systems Observability (active) → Observability Engineering |
| Communication | On Writing Well (active) → The Pyramid Principle |

**Notes:**
- DDIA placed in coding patterns (not system design) — José confirmed explicitly
- System design queue skips DDIA to avoid duplication; Alex Xu Vol 1 goes first
- DevOps, observability, communication queues: José deferred to Claude ("I know the least of DevOps")
- GCP order: ACE certification path first (1 → 3 → 2 per José's explicit ordering)

### Homework Log Location
| Decision | Choice |
|----------|--------|
| Location | Standalone `homework-log.md` at Cashea/ root |
| Rejected | Section inside weekly review (tasks wouldn't persist across weeks) |

### Domain Queue Organization
| Decision | Choice |
|----------|--------|
| Structure | Both: index file per domain + individual resource notes |
| Rejected options | Index only / resource notes only |

---

## Podcasts/Videos
Deferred to Claude's discretion — not discussed. Top 3 per domain to be curated during planning/execution.

---

## Scope Guardrail Notes

No scope creep detected. All decisions stayed within Phase 3 boundary (installing practices, not running them repeatedly over time).
