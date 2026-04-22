<purpose>

Run BEFORE coding starts on a ticket. Captures business context, probable failure points,
design pattern, and key assumptions. Writes a draft reflection note to the vault with
status: in-progress.

When the ticket is resolved, run /growth:reflect. It detects the draft automatically,
preserves the pre-mortem content, and completes the reflection with a bridge question
that compares predictions to reality.

This is the first half of a two-step reflection cycle:
1. /growth:premortem → before coding → captures predictions
2. /growth:reflect   → after coding  → captures reality + scores the full loop

</purpose>

<process>

<step name="gather_context">

Ask the user upfront:

```
Pre-mortem: dame el contexto base del ticket:

Branch (el que usarás):
Ticket ID (e.g. CASH-1234):
Descripción corta del ticket:
```

Wait for the user's answers. Store as `{branch}`, `{ticket_id}`, `{short_description}`.

Resolve vault path:

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
TICKETS_DIR="$VAULT/$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault']['tickets'])")"
```

Check for any planning artifacts related to this ticket in the working directory:

```bash
find . -name "CONTEXT.md" -o -name "PLAN.md" -o -name "RESEARCH.md" 2>/dev/null | head -5
```

Read relevant sections silently (do not output). Extract business goal, risks, dependencies,
or edge cases if present. If nothing is found, proceed without planning context.

</step>

<step name="interview">

Ask each question ONE AT A TIME. Wait for the answer before asking the next.

**Q1 -- Business Context**
```
¿Cuál es el contexto del negocio? ¿Qué problema o necesidad resuelve este ticket exactamente?
No "agregar feature X" -- ¿qué problema del usuario o del negocio resuelve?
```

Wait for answer. Then:

**Q2 -- Failure Points**
```
¿Cuáles son los 3 puntos de falla más probables en este ticket?
¿Dónde puede salir mal esto? Sé específico -- no "errores de integración" sino
"el guard puede fallar si el token JWT no tiene el claim esperado".
```

Wait for answer. If the response is too vague (e.g. "puede fallar la integración"), ask once:
```
¿Puedes ser más específico? ¿Qué parte concreta del código o la lógica podría fallar?
```

Then:

**Q3 -- Design Pattern**
```
¿Qué patrón de diseño aplica? ¿Cuál es la decisión técnica más importante que tomarás?
```

Wait for answer. Then:

**Q4 -- Assumptions**
```
¿Qué estás asumiendo que podría estar mal?
¿Qué pasa si esa asunción es incorrecta?
(Si el ticket es muy claro y no hay ambigüedad real, di "N/A".)
```

Wait for answer.

After Q4, say: "Pre-mortem capturado -- escribiendo draft..."

</step>

<step name="write_draft">

Compose the draft note using this exact structure:

```markdown
---
date: {YYYY-MM-DD}
ticket: {TICKET-ID}
branch: {branch-name}
status: in-progress
tags: [ticket]
score:
score_d1:
score_d2:
score_d3:
score_d4:
score_d5:
---

# {TICKET-ID} -- {short description}

## Pre-mortem

**Contexto de negocio:** {Q1 answer}

**Puntos de falla probables:**
{Format Q2 answer as a numbered list of exactly 3 items}

**Patrón de diseño:** {Q3 answer}

## Assumptions

{Q4 answer. If "N/A", write: "No critical assumptions identified."}

## What Was Hard

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## What I Learned

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## Concepts Encountered

<!-- Completar con /growth:reflect después de resolver el ticket. -->

- [[]]

## What I'd Do Differently

<!-- Completar con /growth:reflect después de resolver el ticket. -->

## Reflection Score

<!-- Completar con /growth:reflect después de resolver el ticket. -->
```

**Filename**: `{TICKET-ID}-{slug}.md` -- slug from branch name, lowercase, hyphens.

Check for existing files:

```bash
find "$TICKETS_DIR/" -name "{ticket_id}*" 2>/dev/null
```

- Existing draft (status: in-progress): overwrite silently — updating a pre-mortem is always safe.
- Existing completed reflection (status: resolved): warn the user and ask to confirm before overwriting.
- Nothing found: create new file.

Write to: `$TICKETS_DIR/{filename}`

After writing, output:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pre-mortem escrito: 20-tickets/{filename}

Predicciones registradas. Ahora puedes codear.
Cuando termines el ticket, corre /growth:reflect --
el workflow detectará este draft y completará la nota automáticamente.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</step>

</process>

<rules>

- Ask questions ONE AT A TIME. Never dump all questions at once.
- Never use Templater syntax -- static dates and values only.
- Draft notes always use `status: in-progress` — this is how /growth:reflect detects them.
- Never invent planning context — only use what's actually found in planning artifacts.
- Do not score the reflection here — scoring happens only in /growth:reflect.
- Q2 failure points should be concrete and specific. Gently push back if the answer is generic.

</rules>
