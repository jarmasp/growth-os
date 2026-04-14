---
week: <% tp.date.now("YYYY-[W]WW") %>
date: <% tp.date.now("YYYY-MM-DD") %>
tags: [weekly]
---

# Week <% tp.date.now("YYYY-[W]WW") %> Review

## Tickets This Week

```dataview
TABLE ticket, date
FROM "Cashea/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

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

## Resources in Queue

```dataview
LIST
FROM "Cashea/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
LIMIT 5
```

## ¿Qué se repitió esta semana que debería convertirse en skill o automatización?

> [!question] Escribe un patrón repetido o una fricción. Si aplica, crea un skill en `.claude/get-shit-done/skills/`.

## Esta semana puedo

> [!success] Puedo hacer X que antes no podía.
