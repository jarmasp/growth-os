---
phase: 3
slug: habits-resources
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-13
---

# Phase 3 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Shell grep + file existence checks (no test runner — Obsidian Markdown phase) |
| **Config file** | None — ad hoc commands listed below |
| **Quick run command** | Per-plan quick checks (see below) |
| **Full suite command** | Phase Gate script in RESEARCH.md `## Validation Architecture` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run the per-plan quick check for that plan's tasks
- **After every plan wave:** Run the full phase gate checks for completed plans
- **Before `/gsd:verify-work`:** All phase gate checks must pass
- **Max feedback latency:** ~5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | Status |
|---------|------|------|-------------|-----------|-------------------|--------|
| 03-01-* | 01 | 1 | LRNG-01,02,04 | file+grep | `ls "$VAULT/40-resources/" \| wc -l` → expect 21 | ⬜ pending |
| 03-02-* | 02 | 2 | LRNG-03,PRAC-02,03,04 | file+grep | `test -f "$VAULT/homework-log.md" && grep -c "\- \[ \]" "$VAULT/homework-log.md"` → expect 4 | ⬜ pending |
| 03-03-* | 03 | 3 | PRAC-01,05 | grep | `grep -n "## Pre-mortem\|## Assumptions\|## What Was Hard" "$VAULT/99-templates/ticket-reflection.md"` | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

No Wave 0 required — this phase creates Markdown files only. No test framework installation needed.

*Existing infrastructure covers all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Pre-mortem runs in < 10 min on a real ticket | PRAC-01 | Requires human judgment on a real ticket | Run pre-mortem on one actual Jira ticket; time it; confirm it fits under 10 min |
| Podcast/video recs are high quality and domain-relevant | LRNG-02 | Subjective quality judgment | Review top-3 recommendations per domain in queue files |
| Wikilinks resolve in Obsidian | LRNG-04 | Requires Obsidian app to resolve links | Open vault in Obsidian; click resource note links from queue files and concept articles |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or file-check commands
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 not applicable (Markdown-only phase)
- [ ] No watch-mode flags
- [ ] Feedback latency < 10s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
