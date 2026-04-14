<purpose>

Generate and write the weekly review note. Surfaces what was done, what gaps emerged,
what's pending in the homework log, and prompts the capability assertion.
Runs at end of sprint or every Friday.

</purpose>

<process>

<step name="setup">

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
WEEK=$(date +"%Y-[W]%V")
DATE=$(date +"%Y-%m-%d")
WEEKLY_DIR="$VAULT/30-weekly"
TICKETS_DIR="$VAULT/20-tickets"
```

Check if this week's file already exists:
```bash
ls "$WEEKLY_DIR/$WEEK.md" 2>/dev/null && echo "EXISTS"
```

If exists: read it, offer to append a "mid-week update" section rather than overwrite.

</step>

<step name="gather_tickets">

```bash
# Recent ticket notes by modification time
ls -lt "$TICKETS_DIR/" | grep "\.md" | head -10
```

Read frontmatter of each recent ticket (last ~7 days by mtime):
```bash
head -10 "$TICKETS_DIR/{recent-file}.md"
```

Extract per ticket: ID, date, and concepts encountered (the `[[wikilinks]]` from the note).

</step>

<step name="gather_homework">

```bash
cat "$VAULT/homework-log.md"
```

From the homework log, extract:
- `[ ]` tasks (pending)
- `[/]` tasks (in progress)
- Note which recurring drills are overdue (PR rewrite: once per sprint, naked system design: biweekly, one-concept deepening: weekly)

</step>

<step name="compose_review">

Write the note using this exact structure:

```markdown
---
week: {YYYY-[W]WW}
date: {YYYY-MM-DD}
tags: [weekly]
---

# Week {YYYY-[W]WW} Review

## Tickets This Week

```dataview
TABLE ticket, date
FROM "Cashea/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

{Below the dataview block, add a human-readable summary:}

| Ticket | What I Did |
|--------|------------|
| {ID} | {one sentence} |

## Skill Domain Self-Rating

| Domain | Score (1-5) | Trend | Note |
|--------|-------------|-------|------|
| Coding patterns | | → | |
| System design | | → | |
| GCP / Infra | | → | |
| DevOps | | → | |
| Observability | | → | |
| Communication | | → | |

## Learning Gaps This Week

```dataview
LIST
FROM "Cashea/10-concepts"
WHERE econtains(file.etags, "#learning-gap")
SORT file.mtime DESC
LIMIT 10
```

{From concepts encountered this week, flag any that felt unclear as learning gaps:}
- #learning-gap: [[{concept}]] — {why it felt unclear}

## Resources in Queue

```dataview
LIST
FROM "Cashea/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
LIMIT 5
```

## Homework Log Status

{Summarize pending/overdue drills from homework-log.md:}
- PR rewrite: {done this sprint / overdue}
- Naked system design: {done this sprint / overdue}
- One-concept deepening: {done this week / overdue}

## ¿Qué se repitió esta semana que debería convertirse en skill o automatización?

> [!question] Escribe un patrón repetido o una fricción. Si aplica, crea un skill en `~/.claude/commands/`.

## Esta semana puedo

> [!success] Puedo hacer X que antes no podía.
```

</step>

<step name="write_and_report">

Write to: `$WEEKLY_DIR/$WEEK.md`

Report:
```
Weekly review written: 30-weekly/{WEEK}.md
Tickets summarized: {N}
Overdue drills: {list or "none"}
Open in Obsidian to fill in skill ratings and capability assertion.
```

</step>

</process>

<rules>

- Dataview blocks are intentional — leave them verbatim, Obsidian renders them.
- Do NOT fill in skill domain scores — that's Jose's job.
- Leave the capability assertion prompt — it requires human reflection.
- If no tickets were found in the last 7 days, note "No ticket reflections this week" — still write the review.

</rules>
