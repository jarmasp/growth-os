<purpose>

Write a ticket reflection note to the Obsidian vault for the work done on the current branch.
Runs AFTER a ticket is resolved — reconstructs context from git, fills what can be inferred,
leaves prompts for what requires human reflection.

</purpose>

<process>

<step name="gather_context">

```bash
# Read config
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
TICKETS_DIR="$VAULT/$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault']['tickets'])")"

# Get branch context
git branch --show-current
git log main...HEAD --oneline
git diff main...HEAD --stat | tail -10
```

Extract:
- **Ticket ID**: from branch name (e.g. `GROWTH-1219` from `feat/GROWTH-1219-...`). If no ticket ID, use branch slug.
- **Short description**: from branch name or first commit subject.
- **Files changed**: from diff stat — what modules/patterns were touched.
- **Design patterns used**: infer from files (guard → NestJS guards pattern, migration → TypeORM migrations pattern, etc.)

</step>

<step name="match_concepts">

```bash
ls "$VAULT/10-concepts/backend/" 2>/dev/null
ls "$VAULT/10-concepts/security/" 2>/dev/null
ls "$VAULT/10-concepts/system-design/" 2>/dev/null
ls "$VAULT/10-concepts/infra/" 2>/dev/null
```

From the files changed and patterns detected, identify 2–4 concept article slugs that are relevant.
These become the `[[wikilinks]]` in the Concepts Encountered section.

</step>

<step name="compose_note">

Write the note using this exact structure (no Templater syntax — static values only):

```markdown
---
date: {YYYY-MM-DD}
ticket: {TICKET-ID}
branch: {branch-name}
status: resolved
tags: [ticket]
---

# {TICKET-ID} — {short description}

## Pre-mortem

> [!question] ¿Cuál es el contexto del negocio?
> ¿Cuáles son los 3 puntos de falla más probables?
> ¿Qué patrón de diseño aplica?

{If business context can be inferred from commits/branch, fill it in. Otherwise leave callout.}

## Assumptions

> [!question] Para tickets ambiguos: ¿Qué estás asumiendo? ¿Qué pasa si estás equivocado?

## What Was Hard

> [!question] ¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?

## What I Learned

{If a clear pattern was used (guard, migration, interceptor), name it here. Otherwise leave prompt.}

> [!question] ¿Qué aprendí hoy? ¿Qué patrón usé o descubrí?

## Concepts Encountered

{List matched concept wikilinks.}

- [[{concept-slug}]]
- [[{concept-slug}]]

## What I'd Do Differently

> [!question] Si lo hiciera de nuevo, ¿qué cambiaría?
```

</step>

<step name="write_and_report">

**Filename**: `{TICKET-ID}-{slug}.md` — slug from branch name, lowercase, hyphens.

```bash
# Check for existing reflection
ls "$TICKETS_DIR/" | grep "{ticket-id}" 2>/dev/null
```

If exists: show diff, ask before overwriting.

Write to: `$TICKETS_DIR/{filename}`

Report:
```
Reflection written: 20-tickets/{filename}
Concepts linked: [[x]], [[y]]
Open in Obsidian or fill in the callout prompts before closing the branch.
```

</step>

</process>

<rules>

- Fill what can be extracted from git. Leave callout prompts for what requires human judgment.
- Never use Templater `<% %>` syntax — Claude writes static dates and values.
- Always add at least 2 wikilinks. If no matching concepts exist, create stubs with `/concept`.
- Pre-mortem section stays even if empty — it's a ritual prompt, not a retrospective.

</rules>
