<purpose>

Write a ticket reflection note to the Obsidian vault for the work done on the current branch.
Runs AFTER a ticket is resolved — reconstructs context from git, then runs an interactive
terminal interview. Claude asks one question at a time, waits for the answer, then asks the
next. After all answers are collected, writes the full note to the vault and scores the reflection.

</purpose>

<process>

<step name="gather_context">

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
TICKETS_DIR="$VAULT/$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault']['tickets'])")"

git branch --show-current
git log main...HEAD --oneline
git diff main...HEAD --stat | tail -10
```

Extract silently (do not output yet):
- **Ticket ID**: from branch name. If no ticket ID, use branch slug.
- **Short description**: from branch name or first commit subject.
- **Files changed**: modules and patterns touched.
- **Design patterns used**: infer from files changed.
- **Business context**: infer from commits and `.planning/` files if present.
- **Failure points**: infer from planning artifacts (CONTEXT.md, PLAN.md, RESEARCH.md).

Also run concept scan:
```bash
ls "$VAULT/10-concepts/backend/" 2>/dev/null
ls "$VAULT/10-concepts/security/" 2>/dev/null
ls "$VAULT/10-concepts/system-design/" 2>/dev/null
ls "$VAULT/10-concepts/infra/" 2>/dev/null
```

Identify 2-4 concept slugs relevant to this ticket. Hold these for the final note.

</step>

<step name="present_context">

Output a brief context block so the user knows what Claude inferred before the interview starts:

```
Branch: {branch}
Ticket: {TICKET-ID} -- {short description}
Files changed: {list key modules, e.g. guards/, decorators/, controllers/}
Pattern detected: {e.g. guard chain composition, TypeORM migration}

Starting reflection interview -- answer each question, then I'll write the note.
```

</step>

<step name="interview">

Ask each question ONE AT A TIME. Wait for the answer before asking the next.
Do not ask all questions at once. Do not skip questions.

**Q1 -- Assumptions**
```
Que asumiste en este ticket? Que pasaria si alguna de esas asunciones estuviera mal?
(Si el ticket fue directo y no hubo ambiguedad real, di "N/A".)
```

Wait for answer. Then:

**Q2 -- What Was Hard**
```
Que fue lo mas dificil? Cual fue el blockeador real -- no el sintoma, sino la causa raiz?
```

Wait for answer. Then:

**Q3 -- What I Learned**
```
Que aprendiste hoy? Nombra el patron, la decision tecnica, o el insight concreto.
No "aprendi sobre guards" -- algo especifico como "aprendi que X causa Y porque Z."
```

Wait for answer. Then:

**Q4 -- What I'd Do Differently**
```
Si lo hicieras de nuevo desde cero, que cambiarias? Puede ser el approach, el orden,
una investigacion que harias antes, o nada.
```

Wait for answer.

After Q4, say: "Gracias -- escribiendo la nota..."

</step>

<step name="write_note">

Compose the note using the answers collected. Use this exact structure:

```markdown
---
date: {YYYY-MM-DD}
ticket: {TICKET-ID}
branch: {branch-name}
status: resolved
tags: [ticket]
---

# {TICKET-ID} -- {short description}

## Pre-mortem

{Fill from git/plan context: business context, top 3 failure points, design pattern.
 Keep factual -- inferred from commits and planning artifacts, not invented.}

## Assumptions

{User's answer to Q1. If "N/A", write: "Ticket was unambiguous -- no critical assumptions identified."}

## What Was Hard

{User's answer to Q2.}

## What I Learned

{User's answer to Q3.}

## Concepts Encountered

{Matched wikilinks from vault scan.}

- [[{concept-slug}]]
- [[{concept-slug}]]

## What I'd Do Differently

{User's answer to Q4. If "nada", write: "No changes -- approach was correct."}

## Reflection Score

**{X}/10 -- {Band label}**

| Dimension | Score | Feedback |
|---|---|---|
| D1 Cognitive Depth | {0-3}/3 | {one-line feedback} |
| D2 Cycle Completeness | {0-2}/2 | {one-line feedback} |
| D3 Loop Depth | {0-2}/2 | {one-line feedback} |
| D4 Actionability | {0-2}/2 | {one-line feedback} |
| D5 Linguistic Quality | {0-1}/1 | {one-line feedback} |

**Análisis:** {2-3 sentences: strongest point, what to push deeper on next reflection.}
```

**Filename**: `{TICKET-ID}-{slug}.md` -- slug from branch name, lowercase, hyphens.

```bash
# Check for existing reflection
ls "$TICKETS_DIR/" | grep "{ticket-id}" 2>/dev/null
```

If exists: show diff, ask before overwriting.

Write to: `$TICKETS_DIR/{filename}`

</step>

<step name="score">

After writing the note, load and follow the scorer agent:
`~/Documents/growth-os/agents/reflection-scorer.md`

Pass to the scorer:
- `TICKET` -- ticket ID and short description
- `PATTERN` -- design pattern detected from git context
- `FILES` -- key modules changed
- `Q1` through `Q4` -- the user's exact answers verbatim from the interview

Run the scorer rubric. Then:
1. Output the score block to the terminal (exactly as specified by the scorer).
2. Append the score into the `## Reflection Score` section already written in the note file:
   - Fill the table rows with per-dimension scores and one-line feedback.
   - Fill the **Análisis** paragraph with the scorer's 2-3 sentence summary.
   - Edit the file in place -- do not rewrite the whole note.

</step>

</process>

<rules>

- Ask questions ONE AT A TIME. Never dump all questions at once.
- Pre-mortem is filled from git context -- never asked interactively.
- Concepts Encountered is filled from vault scan -- never asked interactively.
- Never use Templater syntax -- static dates and values only.
- Always add at least 2 wikilinks. If no matching concepts exist, note them as candidates for `/concept`.
- Score every reflection -- no exceptions. The score is feedback, not a grade.

</rules>
