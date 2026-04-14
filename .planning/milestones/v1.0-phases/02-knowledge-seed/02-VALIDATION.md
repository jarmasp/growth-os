---
phase: 2
slug: knowledge-seed
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-13
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual inspection (no automated tests for Markdown file authoring) |
| **Config file** | N/A — this phase writes Markdown files, not executable code |
| **Quick run command** | `find "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/10-concepts" -name "*.md" | wc -l` |
| **Full suite command** | Visual Obsidian graph view check (Dimension 10) |
| **Estimated runtime** | ~30 seconds (file count) + manual graph check |

---

## Sampling Rate

- **After every task commit:** Run quick file count command
- **After every plan wave:** Manual review of created articles in Obsidian
- **Before `/gsd:verify-work`:** Full graph check must show connected graph with no isolated nodes
- **Max feedback latency:** 60 seconds (file count + spot read)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 02-01-01 | 01 | 1 | SEED-01 | File count | `find ".../10-concepts" -name "*.md" \| wc -l` ≥ 39 | ✅ | ⬜ pending |
| 02-01-02 | 01 | 1 | SEED-01 | Manual sample | Read 5 random stubs, verify only D-01 sections present | ❌ Wave 0 | ⬜ pending |
| 02-02-01 | 02 | 2 | SEED-02 | Manual | Open each top-10 article, verify 6 sections populated | ❌ Wave 0 | ⬜ pending |
| 02-03-01 | 03 | 3 | SEED-03 | Script check | `grep -rl "\[\[" ".../10-concepts" \| wc -l` == total file count | ❌ Wave 0 | ⬜ pending |
| 02-03-02 | 03 | 3 | SEED-03 | Visual | Obsidian graph view — no isolated nodes | ❌ Wave 0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] Manual checklist for stub structure validation (D-01 only: What It Is + Related Concepts)
- [ ] Manual checklist for full article completeness (all 6 sections present and populated)
- [ ] Script for wikilink presence check across all concept files

*No automated test framework — this phase produces Markdown files in an Obsidian vault.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| All 6 sections populated in top-10 articles | SEED-02 | Obsidian vault content, no test runner | Open each in Obsidian, verify `## What It Is`, `## How It Works`, `## When to Use It`, `## Cashea Examples`, `## Gotchas`, `## Related Concepts` |
| No orphan nodes in graph | SEED-03 | Graph topology requires Obsidian graph view | Open Obsidian → Graph view → zoom out → no isolated nodes |
| Stubs are strict subsets (D-01 template only) | SEED-01 | Structure enforcement | Random sample 5 stubs, confirm absence of `## How It Works` and other full-article headers |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
