<purpose>

Generate and write the weekly review note. Runs an interactive interview (4 questions),
surfaces ticket context, scores the week with a multi-framework rubric (W1–W5), and
recommends specific resources to improve before the next weekly review.
Runs at end of sprint or every Friday.

</purpose>

<process>

<step name="setup">

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
VAULT_NAME=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_name'])")
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

<step name="gather_scores">

Compute per-dimension score averages for the current 7-day window and the prior 7-day
window. Do NOT rely on Dataview for the trend — Dataview cannot cross-compare two
windows in a single block (see Phase 4 research Pattern 3). Instead, compute averages
in the workflow and pass them to `compose_review` as variables.

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
TICKETS="$VAULT/20-tickets"

python3 - <<'PY'
import os, re, datetime, json, pathlib
tickets = pathlib.Path(os.environ.get("TICKETS", ""))
today = datetime.date.today()
curr_start = today - datetime.timedelta(days=7)
prior_start = today - datetime.timedelta(days=14)

def parse_fm(path):
    txt = path.read_text(errors="ignore")
    if not txt.startswith("---"):
        return None
    end = txt.find("\n---", 3)
    if end == -1:
        return None
    fm = {}
    for line in txt[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm

curr = {k: [] for k in ["score", "score_d1","score_d2","score_d3","score_d4","score_d5"]}
prior = {k: [] for k in curr}

for p in tickets.glob("*.md"):
    fm = parse_fm(p)
    if not fm or "score_d1" not in fm or not fm.get("score_d1"):
        continue
    try:
        d = datetime.date.fromisoformat(fm.get("date", ""))
    except Exception:
        continue
    bucket = None
    if curr_start <= d <= today:
        bucket = curr
    elif prior_start <= d < curr_start:
        bucket = prior
    if bucket is None:
        continue
    for k in bucket:
        v = fm.get(k)
        if v and v.lstrip("-").isdigit():
            bucket[k].append(int(v))

def avg(xs):
    return round(sum(xs)/len(xs), 1) if xs else None

report = {
    "curr": {k: avg(v) for k, v in curr.items()},
    "prior": {k: avg(v) for k, v in prior.items()},
    "curr_count": len(curr["score_d1"]),
    "prior_count": len(prior["score_d1"]),
}
print(json.dumps(report))
PY
```

Export the JSON result to variables (for example `SCORES_JSON`) so `compose_review` can
read it. Determine the trend arrow per dimension:

- current avg > prior avg → ↑
- current avg < prior avg → ↓
- current avg == prior avg → →
- prior avg is null (<1 scored reflection in prior window) → → and flag "insufficient data"

If `curr_count + prior_count < 2`, flag `INSUFFICIENT_DATA=true` — `compose_review` will
append the note "_Insufficient data for trend — keep reflecting._" under the table.

Hold these values until compose_review runs.

</step>

<step name="interview">

Ask each question ONE AT A TIME. Wait for the answer before asking the next.
Do not ask all questions at once. Do not skip questions.

**W-Q1 — Patrón de la semana**
```
¿Qué patrón se repitió esta semana? Puede ser una fricción, un concepto que apareció
en varios tickets, o un problema estructural. No lo límites a un ticket específico.
(Si no hubo patrón claro, di "N/A".)
```

Wait for answer. Then:

**W-Q2 — Brecha de skill**
```
¿Qué brecha de skill quedó expuesta esta semana? Sé concreto: no "necesito aprender más X",
sino la pregunta exacta que no puedes responder.
(Ej: "No sé por qué Reflector.get() retorna undefined cuando la key no está registrada."
Si no hubo brecha, di "N/A".)
```

Wait for answer. Then:

**W-Q3 — Capability assertion**
```
¿Qué puedes hacer esta semana que antes no podías? Nombra la skill específica
+ el ticket o concepto que lo demuestra.
(Ej: "Puedo componer guard chains con skip decorators en NestJS, demostrado en ALDS-2607.")
```

Wait for answer. Then:

**W-Q4 — Drills**
```
¿Hiciste algún drill esta semana? Si no, ¿cuándo exactamente lo harás?
(Día + hora aproximada — "el jueves a las 7pm". "Pronto" o "esta semana" no cuentan.)
```

Wait for answer. Then say: "Gracias — escribiendo la nota..."

Store answers as `W_Q1`, `W_Q2`, `W_Q3`, `W_Q4`.

</step>

<step name="compose_review">

Write the note using this exact structure:

```markdown
---
week: {YYYY-[W]WW}
date: {YYYY-MM-DD}
tags: [weekly]
weekly_score:
w1:
w2:
w3:
w4:
w5:
---

# Week {YYYY-[W]WW} Review

## Tickets This Week

```dataview
TABLE ticket, date
FROM "{VAULT_NAME}/20-tickets"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
```

Substitution rule: replace `{VAULT_NAME}` with the value of `vault_name` from config.json (resolved in setup step).

{Below the dataview block, add a human-readable summary:}

| Ticket | What I Did |
|--------|------------|
| {ID} | {one sentence} |

## Reflection Score Trend

| Dimension | This Week | Prior Week | Trend |
|-----------|-----------|------------|-------|
| D1 Cognitive Depth | {curr_d1} | {prior_d1} | {arrow_d1} |
| D2 Cycle Completeness | {curr_d2} | {prior_d2} | {arrow_d2} |
| D3 Loop Depth | {curr_d3} | {prior_d3} | {arrow_d3} |
| D4 Actionability | {curr_d4} | {prior_d4} | {arrow_d4} |
| D5 Linguistic Quality | {curr_d5} | {prior_d5} | {arrow_d5} |
| **Total** | **{curr_total}** | **{prior_total}** | {arrow_total} |

{if INSUFFICIENT_DATA: append on the next line: "_Insufficient data for trend — keep reflecting._"}

Substitution rules:
- Values come from the `gather_scores` JSON output.
- Null averages render as `—` (em dash), not `None` or blank.
- Arrows render as single characters (↑ ↓ →), never as words.

## Skill Domain Self-Rating

| Domain | Score (1-5) | Trend | Note |
|--------|-------------|-------|------|
{Generate one row per domain. Source: read `user_profile.priority_domains` from config.json.
 If `user_profile` is not set, use ["Core practice", "Adjacent skills"].
 Always add "Communication" as the last row regardless of the list.
 Format: `| {domain} | | → | |`}

_Dreyfus scale: 1 Novice (needs rules) · 2 Advanced Beginner (recognizes patterns) · 3 Competent (deliberate choices) · 4 Proficient (sees big picture) · 5 Expert (intuitive)_

## Learning Gaps This Week

```dataview
LIST
FROM "{VAULT_NAME}/10-concepts"
WHERE econtains(file.etags, "#learning-gap")
SORT file.mtime DESC
LIMIT 10
```

Substitution rule: replace `{VAULT_NAME}` with `vault_name` from config.json.

{From concepts encountered this week, flag any that felt unclear as learning gaps:}
- #learning-gap: [[{concept}]] — {why it felt unclear}

## Resources in Queue

```dataview
LIST
FROM "{VAULT_NAME}/40-resources"
WHERE econtains(file.etags, "#to-read")
SORT file.mtime ASC
LIMIT 5
```

Substitution rule: replace `{VAULT_NAME}` with `vault_name` from config.json.

## Homework Log Status

{Summarize pending/overdue drills from homework-log.md. Then append W-Q4 answer:}
- PR rewrite: {done this sprint / overdue}
- Naked system design: {done this sprint / overdue}
- One-concept deepening: {done this week / overdue}

**Compromiso:** {W_Q4 answer verbatim — drill done or specific scheduled slot}

## ¿Qué se repitió esta semana?

{W_Q1 answer verbatim. If "N/A", write: "Sin patrón cross-ticket esta semana."}

## Brecha de skill

{W_Q2 answer verbatim. If "N/A", write: "Sin brecha nueva identificada esta semana."}

## Esta semana puedo

{W_Q3 answer verbatim.}

## Weekly Score

**{X}/10 — {Band label}**
```

</step>

<step name="write_and_report">

Write to: `$WEEKLY_DIR/$WEEK.md`

Report:
```
Weekly review written: 30-weekly/{WEEK}.md
Tickets summarized: {N}
Overdue drills: {list or "none"}
Open in Obsidian to fill in skill domain ratings.
```

</step>

<step name="score">

After writing the note, load and follow the weekly reviewer agent:
`~/Documents/growth-os/agents/weekly-reviewer.md`

Pass to the reviewer:
- `WEEK` — week identifier
- `TICKETS` — list of ticket IDs + one-sentence summaries gathered in gather_tickets
- `CONCEPTS` — all wikilink slugs found in ticket reflections this week
- `DRILLS_OVERDUE` — overdue drills from gather_homework
- `W_Q1` through `W_Q4` — the user's exact answers verbatim from the interview

Run the reviewer rubric. Capture five raw integer values:
`W1` (0-3), `W2` (0-2), `W3` (0-2), `W4` (0-2), `W5` (0-1), `WEEKLY_TOTAL` (W1+W2+W3+W4+W5, 0-10).
Raw integers only — Dataview `average()` requires pure numerics.

Then:

1. Output the full score block + resource recommendations to the terminal
   (exactly as specified by the reviewer agent output format).

2. Fill the `## Weekly Score` section already written in the note file:
   Replace the placeholder line with the full score block rendered as markdown.
   Edit in place — do not rewrite the whole note.

3. Inject score fields into the YAML frontmatter block of the same note file.
   The compose_review step already left empty placeholders (`weekly_score:`, `w1:` ... `w5:`).
   Replace each with the raw integer captured above. Edit in place using Python:

   ```bash
   python3 - <<'PY'
   import re, pathlib
   note = pathlib.Path("$NOTE_PATH")
   text = note.read_text()
   parts = text.split("---\n", 2)
   fm = parts[1]
   fm = re.sub(r"^weekly_score:\s*$", f"weekly_score: $WEEKLY_TOTAL", fm, flags=re.M)
   fm = re.sub(r"^w1:\s*$", f"w1: $W1", fm, flags=re.M)
   fm = re.sub(r"^w2:\s*$", f"w2: $W2", fm, flags=re.M)
   fm = re.sub(r"^w3:\s*$", f"w3: $W3", fm, flags=re.M)
   fm = re.sub(r"^w4:\s*$", f"w4: $W4", fm, flags=re.M)
   fm = re.sub(r"^w5:\s*$", f"w5: $W5", fm, flags=re.M)
   note.write_text("---\n" + fm + "---\n" + parts[2])
   PY
   ```

Do not emit scores if any of W1..W5 is empty (guard against reviewer abort).

</step>

<step name="process_inbox">

Final step of /growth:weekly. Reads all files in `00-inbox/`, proposes categorization for
each, presents the full plan, waits for a single confirmation, then executes moves
and reports counts.

```bash
VAULT=$(cat ~/Documents/growth-os/config.json | python3 -c "import sys,json; c=json.load(sys.stdin); print(c['vault_root'])")
INBOX="$VAULT/00-inbox"
```

**1. Read** — list every file in `$INBOX` (exclude hidden files like `.DS_Store`).
For each file, read its frontmatter + first ~20 lines of body:

```bash
for f in "$INBOX"/*.md; do
  [ -f "$f" ] && head -25 "$f"
done
```

**2. Categorize** each file using these rules (in order — first match wins):

| Signal | Destination |
|--------|-------------|
| frontmatter `tags:` contains `moc` | `50-mocs/` |
| frontmatter `tags:` contains `ticket` | `20-tickets/` |
| frontmatter `tags:` contains `#to-read` OR body describes a book/article/video/podcast | `40-resources/` |
| content is a concept/explanation doc | `10-concepts/` (choose subfolder from `concept_domains` in config.json — backend, system-design, security, infra) |
| content is redundant vs an existing vault note (by slug or topic) | PROPOSE DELETION |
| no clear category | PROPOSE as concept stub candidate for `10-concepts/` (default per CONTEXT.md Claude's Discretion) |

Do not move anything yet.

**3. Present** the full plan as a numbered list before any moves. Format:

```
Inbox triage plan — {N} files found:

1. {filename}.md → {ACTION: MOVE to {dest}/ | DELETE | STUB in 10-concepts/{domain}/} ({reason})
2. ...

Proceed? (reply `proceed` to execute all, `skip N` or `skip N M` to exclude items, anything else aborts.)
```

**4. Wait** for a single confirmation message. Parse the reply:
- Exactly `proceed` → execute every item in the plan.
- `skip N` or `skip N M P` → execute every item EXCEPT the listed numbers.
- Any other reply → abort with `Aborted — nothing moved.` and exit the step.

**5. Execute** the confirmed moves in order. For each item:
- MOVE: `mv "$INBOX/{filename}" "$VAULT/{dest}/"`
- DELETE: `rm "$INBOX/{filename}"`
- STUB: `mv "$INBOX/{filename}" "$VAULT/10-concepts/{domain}/"` (same as MOVE to a concept subfolder)

Never use `rm -rf`. Operate file-by-file.

**6. Report** counts using this exact format:

```
Inbox triage complete.
  Moved:   {N} ({comma-separated filenames or "none"})
  Skipped: {M} ({comma-separated filenames or "none"})
  Deleted: {K} ({comma-separated filenames or "none"})
```

If the inbox was empty at step 1, skip straight to a report: `Inbox is empty — nothing to triage.`

</step>

</process>

<rules>

- Dataview blocks are intentional — leave them verbatim, Obsidian renders them.
- Do NOT fill in skill domain scores — that's the user's job.
- Interview answers (W_Q1–W_Q4) replace the former callout prompts — write them verbatim into the note.
- If no tickets were found in the last 7 days, note "No ticket reflections this week" — still run the interview and write the review.
- Score every weekly review — no exceptions. The score is calibration, not a grade.
- Resource recommendations are terminal-only — do not write them into the vault note.

</rules>
