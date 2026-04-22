<purpose>

Write a ticket reflection note to the Obsidian vault for the work done on the current branch.
Runs AFTER a ticket is resolved — reconstructs context from git, then runs an interactive
terminal interview. Claude asks one question at a time, waits for the answer, then asks the
next. After all answers are collected, writes the full note to the vault and scores the reflection.

If a pre-mortem draft exists for this ticket (written by /growth:premortem before coding),
this workflow detects it automatically, preserves the pre-mortem content, and replaces the
Assumptions question with a bridge question comparing predictions to reality.

</purpose>

<process>

<step name="gather_context">

Ask the user upfront — do NOT infer these from git:

```
Antes de empezar, dame el contexto base:

Branch (puede ser diferente a la actual):
Ticket ID (e.g. CASH-1234):
Descripción corta del ticket:
```

Wait for the user's answers. Store as `{branch}`, `{ticket_id}`, `{short_description}`.

Resolve vault paths and check for a pre-mortem draft:

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
TICKETS_DIR="$VAULT/$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault']['tickets'])")"

DRAFT_PATH=$(find "$TICKETS_DIR/" -name "{ticket_id}*" 2>/dev/null | head -1)
```

If `DRAFT_PATH` is non-empty, check its status:

```bash
python3 -c "
import pathlib, re
text = pathlib.Path('$DRAFT_PATH').read_text()
m = re.search(r'^status:\s*(.+)$', text, re.M)
print(m.group(1).strip() if m else '')
"
```

If status is `in-progress`, set `DRAFT_FOUND=true` and extract content:

```bash
python3 - <<'PY'
import pathlib, re
text = pathlib.Path("$DRAFT_PATH").read_text()
pm  = re.search(r'## Pre-mortem\n\n(.*?)(?=\n## )', text, re.DOTALL)
asm = re.search(r'## Assumptions\n\n(.*?)(?=\n## )', text, re.DOTALL)
print("PREMORTEM:", pm.group(1).strip() if pm else "")
print("ASSUMPTIONS:", asm.group(1).strip() if asm else "")
PY
```

Store extracted content as `{draft_premortem}` and `{draft_assumptions}`.

Then run git commands using the user-provided branch:

```bash
git log main...{branch} --oneline
git diff main...{branch} --stat | tail -10
```

Extract silently (do not output yet):
- **Files changed**: modules and patterns touched.
- **Design patterns used**: infer from files changed.
- **Business context**: infer from commits and `.planning/` files if present (only used when DRAFT_FOUND=false).
- **Failure points**: infer from planning artifacts (only used when DRAFT_FOUND=false).

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

Output a brief context block before the interview starts:

```
Branch: {branch}
Ticket: {ticket_id} -- {short_description}
Files changed: {list key modules, e.g. guards/, decorators/, controllers/}
Pattern detected: {e.g. guard chain composition, TypeORM migration}
```

If `DRAFT_FOUND=true`, add:

```
Pre-mortem encontrado -- cargando contexto pre-codeo...

Pre-mortem:
{draft_premortem}

Assumptions capturadas antes de codear:
{draft_assumptions}
```

Then: `Starting reflection interview -- answer each question, then I'll write the note.`

</step>

<step name="interview">

Ask each question ONE AT A TIME. Wait for the answer before asking the next.
Do not ask all questions at once. Do not skip questions.

---

**If DRAFT_FOUND=false (no pre-mortem draft):**

**Q1 -- Assumptions**
```
Que asumiste en este ticket? Que pasaria si alguna de esas asunciones estuviera mal?
(Si el ticket fue directo y no hubo ambiguedad real, di "N/A".)
```

Wait for answer. Then Q2, Q3, Q4.

---

**If DRAFT_FOUND=true (pre-mortem draft exists):**

**Q_BRIDGE -- Prediction Accuracy**
```
Tu pre-mortem anticipó estos puntos de falla:
{draft_premortem failure points}

¿Se cumplieron? ¿Qué fue diferente a lo que predijiste antes de codear?
```

Wait for answer. Store as `{bridge_answer}`. Then Q2, Q3, Q4.

---

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
score:
score_d1:
score_d2:
score_d3:
score_d4:
score_d5:
---

# {TICKET-ID} -- {short description}

## Pre-mortem

{If DRAFT_FOUND=true: use {draft_premortem} verbatim — written before coding started.}
{If DRAFT_FOUND=false: fill from git/plan context: business context, top 3 failure points,
 design pattern. Keep factual -- inferred from commits and planning artifacts, not invented.}

## Assumptions

{If DRAFT_FOUND=true: use {draft_assumptions} verbatim, then append on a new line:
 **Realidad:** {bridge_answer}}
{If DRAFT_FOUND=false: user's answer to Q1. If "N/A", write:
 "Ticket was unambiguous -- no critical assumptions identified."}

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

**File handling:**

If `DRAFT_FOUND=true`: overwrite `DRAFT_PATH` with the completed note. No confirmation needed
— completing a draft is the intended behavior. `NOTE_PATH=$DRAFT_PATH`.

If `DRAFT_FOUND=false`: filename is `{TICKET-ID}-{slug}.md` (slug from branch name, lowercase, hyphens).

```bash
# Check for existing completed reflection only when no draft was found
ls "$TICKETS_DIR/" | grep "{ticket-id}" 2>/dev/null
```

If an existing completed reflection (status: resolved) is found: show diff, ask before overwriting.

Write to: `$TICKETS_DIR/{filename}`. Set `NOTE_PATH="$TICKETS_DIR/{filename}"`.

</step>

<step name="score">

After writing the note, load and follow the scorer agent:
`~/Documents/growth-os/agents/reflection-scorer.md`

Pass to the scorer:
- `TICKET` -- ticket ID and short description
- `PATTERN` -- design pattern detected from git context
- `FILES` -- key modules changed
- `Q1` -- if DRAFT_FOUND=false: user's assumption answer; if DRAFT_FOUND=true: {draft_assumptions} + bridge_answer combined
- `Q2` through `Q4` -- the user's exact answers verbatim from the interview

Run the scorer rubric. Capture the six raw integer values before writing anything:
`D1` (0-3), `D2` (0-2), `D3` (0-2), `D4` (0-2), `D5` (0-1), `TOTAL` (D1+D2+D3+D4+D5, 0-10).
These are raw integers, never fractions -- Dataview `average()` requires pure numerics.

Then:

1. Output the score block to the terminal (exactly as specified by the scorer).

2. Fill the `## Reflection Score` section already written in the note file:
   - Fill the table rows with per-dimension scores and one-line feedback.
   - Fill the **Análisis** paragraph with the scorer's 2-3 sentence summary.
   - Edit the file in place -- do not rewrite the whole note.

3. Inject score fields into the YAML frontmatter block of the same note file. The
   write_note step already left empty placeholders (`score:`, `score_d1:` ... `score_d5:`)
   between `tags: [ticket]` and the closing `---`. Replace each empty placeholder with
   the raw integer captured above. Edit in place -- do not rewrite the whole note.

   Use Python to keep the YAML block robust (split at the second `---`, mutate the
   fields, rejoin):

   ```bash
   python3 - <<'PY'
   import re, pathlib
   note = pathlib.Path("$NOTE_PATH")
   text = note.read_text()
   parts = text.split("---\n", 2)  # ["", frontmatter, body]
   fm = parts[1]
   fm = re.sub(r"^score:\s*$",    f"score: $TOTAL",    fm, flags=re.M)
   fm = re.sub(r"^score_d1:\s*$", f"score_d1: $D1",    fm, flags=re.M)
   fm = re.sub(r"^score_d2:\s*$", f"score_d2: $D2",    fm, flags=re.M)
   fm = re.sub(r"^score_d3:\s*$", f"score_d3: $D3",    fm, flags=re.M)
   fm = re.sub(r"^score_d4:\s*$", f"score_d4: $D4",    fm, flags=re.M)
   fm = re.sub(r"^score_d5:\s*$", f"score_d5: $D5",    fm, flags=re.M)
   note.write_text("---\n" + fm + "---\n" + parts[2])
   PY
   ```

   After this substep the note's frontmatter must contain `score_d1: {D1}` etc. with
   raw integer values.

4. Append a row to the ledger at `$VAULT/reflection-scores.md`.

   Resolve the ledger path:
   ```bash
   VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
   LEDGER="$VAULT/reflection-scores.md"
   ```

   Create-if-missing safety (prevents appending to a non-existent file): if the ledger
   does not exist yet, create it with the canonical header before appending:

   ```bash
   if [ ! -f "$LEDGER" ]; then
     cat > "$LEDGER" <<'EOF'
   # Reflection Score Ledger

   Append a row after every scored reflection. One row per `/growth:reflect` run. Total = sum of D1..D5.

   Dimension maxima: D1 Cognitive Depth (3) · D2 Cycle Completeness (2) · D3 Loop Depth (2) · D4 Actionability (2) · D5 Linguistic Quality (1) · Total (10)

   | Date | Ticket | Total | D1 | D2 | D3 | D4 | D5 | Branch |
   |------|--------|-------|----|----|----|----|----|--------|
   EOF
   fi
   ```

   Then append exactly one row using the values captured from the scorer and the
   branch/ticket/date already resolved in earlier steps:

   ```bash
   echo "| $DATE | $TICKET_ID | $TOTAL | $D1 | $D2 | $D3 | $D4 | $D5 | $BRANCH |" >> "$LEDGER"
   ```

   Never truncate the ledger. Never rewrite existing rows. One `/growth:reflect` run = one new
   row. Do not emit a row if any of D1..D5 is empty (guard against scorer abort).

</step>

</process>

<rules>

- Ask questions ONE AT A TIME. Never dump all questions at once.
- If DRAFT_FOUND=true: Pre-mortem and Assumptions come from the draft verbatim — never re-ask or re-infer them.
- If DRAFT_FOUND=false: Pre-mortem is filled from git context — never asked interactively.
- Concepts Encountered is always filled from vault scan — never asked interactively.
- Never use Templater syntax -- static dates and values only.
- Always add at least 2 wikilinks. If no matching concepts exist, note them as candidates for `/growth:concept`.
- Score every reflection -- no exceptions. The score is feedback, not a grade.
- Completing a pre-mortem draft (DRAFT_FOUND=true) is always safe — never ask to confirm overwrite.

</rules>
