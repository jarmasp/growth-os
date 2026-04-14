---
phase: 1
slug: vault-foundation
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-04-13
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Manual + bash verification (no test suite — Obsidian vault setup) |
| **Config file** | none |
| **Quick run command** | `ls "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/"` |
| **Full suite command** | See Manual-Only Verifications below |
| **Estimated runtime** | ~5 minutes manual |

---

## Sampling Rate

- **After every task commit:** Run folder-exists check (see quick run command)
- **After every plan wave:** Run full manual verification checklist
- **Before `/gsd:verify-work`:** All manual verifications must pass
- **Max feedback latency:** N/A (manual verification, no automated suite)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-* | 01-01 | 1 | VAULT-01, VAULT-02, VAULT-06 | manual + bash | `ls "...Personal/Cashea/"` | ✅ | ⬜ pending |
| 1-02-* | 01-02 | 2 | VAULT-03 | manual | Obsidian UI plugin check | N/A | ⬜ pending |
| 1-03-* | 01-03 | 3 | CAPT-01–06, REFL-01–04 | manual | Obsidian template trigger test | ✅ | ⬜ pending |
| 1-04-* | 01-04 | 4 | SKILL-01, SKILL-02, SKILL-03 | bash | `ls .claude/get-shit-done/skills/` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

None — no test framework required for vault setup. Verification is purely functional/behavioral.

*Existing infrastructure: bash + manual Obsidian UI checks cover all phase requirements.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Folder structure exists | VAULT-01 | Filesystem — verifiable via bash | `ls "/Users/thyfus/Documents/obsidian vaults/personal/Personal/Cashea/"` — must show 7 directories: 00-inbox, 10-concepts, 20-tickets, 30-weekly, 40-resources, 50-mocs, 99-templates |
| Git repo initialized and remote set | VAULT-02 | Git state | `cd "/Users/thyfus/Documents/obsidian vaults/personal" && git remote -v` — must show `origin git@github.com:jarmasp/cashea-knowledge-vault.git` |
| Plugins installed (all 8) | VAULT-03 | Obsidian UI only | Open Obsidian Settings → Community plugins → verify all 8 present and enabled |
| Obsidian Git auto-backup 30 min | VAULT-03 | Obsidian plugin config | Settings → Obsidian Git → Backup interval must show 30 |
| Templater folder trigger active | VAULT-04 | Obsidian plugin config | Create new note in `20-tickets/` → verify ticket-reflection template auto-applied |
| Ticket reflection template exists | CAPT-01 | File existence | `ls ".../Personal/Cashea/99-templates/"` must include `ticket-reflection.md` |
| Concept article template exists | CAPT-03 | File existence | `ls ".../Personal/Cashea/99-templates/"` must include `concept-article.md` |
| Templates use callout+question format | CAPT-01, CAPT-03 | Visual render | Open template in Obsidian reading mode — `[!question]` callouts must render as styled blocks |
| Weekly review template (full) exists | REFL-03 | File existence | `ls ".../Personal/Cashea/99-templates/"` must include `weekly-review.md` |
| Weekly review template (survival) exists | REFL-04 | File existence | `ls ".../Personal/Cashea/99-templates/"` must include `weekly-review-survival.md` |
| Dataview queries render | REFL-03 | Obsidian rendering | Open a MOC file in reading mode → Dataview table renders (not raw code block) |
| Existing notes migrated | VAULT-05 | File state | 7 original notes must NOT exist at `Personal/` root; must exist with correct frontmatter in new locations |
| deslop skill active | SKILL-01 | File existence | `ls .claude/get-shit-done/skills/deslop.md` → exists |
| review-pr skill active | SKILL-02 | File existence | `ls .claude/get-shit-done/skills/review-pr.md` → exists |
| Weekly retrospective question in template | SKILL-03 | Content check | `grep "skill" ".../Personal/Cashea/99-templates/weekly-review.md"` → question present |
| Real ticket reflection under 2 min | VAULT-06 | Timed user test | Jose writes one real reflection using template — must take under 2 minutes |

---

## Validation Sign-Off

- [ ] All tasks have manual verify instructions or bash checks
- [ ] Folder structure verified after Plan 01-01
- [ ] Plugins verified after Plan 01-02
- [ ] Templates verified after Plan 01-03
- [ ] Skills verified after Plan 01-04
- [ ] Real ticket reflection timed test passed
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
