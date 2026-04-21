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

<step name="process_inbox">

Final step of /weekly. Reads all files in `00-inbox/`, proposes categorization for
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
- Do NOT fill in skill domain scores — that's Jose's job.
- Leave the capability assertion prompt — it requires human reflection.
- If no tickets were found in the last 7 days, note "No ticket reflections this week" — still write the review.

</rules>
