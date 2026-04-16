<purpose>

Score a completed ticket reflection against a multi-framework rubric derived from learning science.
Receives the four reflection answers and the git context inferred during the reflect workflow.
Returns a 10-point score with per-dimension breakdown and one actionable note per answer.

Frameworks applied:
- Bloom's Revised Taxonomy (Anderson & Krathwohl) — cognitive depth
- Kolb's Experiential Learning Cycle — cycle completeness
- Argyris & Schön Double-Loop Learning — assumption revision depth
- Ericsson Deliberate Practice — actionability quality
- Pennebaker / LIWC — linguistic markers of knowledge consolidation

</purpose>

<input>

The caller (reflect workflow) passes:
- `TICKET` — ticket ID and short description
- `PATTERN` — design pattern detected from git context (e.g. "guard chain composition")
- `FILES` — key modules changed
- `Q1` — user's answer to "¿Qué asumiste? ¿Qué pasaría si estuvieras mal?"
- `Q2` — user's answer to "¿Qué fue lo más difícil? ¿Cuál fue el blockeador real?"
- `Q3` — user's answer to "¿Qué aprendiste? Nombra el patrón o insight concreto."
- `Q4` — user's answer to "¿Qué cambiarías si lo hicieras de nuevo?"

</input>

<rubric>

Score the reflection as a whole on five dimensions. Each answer can contribute to any dimension —
read all four together before scoring. Total = 10 points.

---

## D1 — Cognitive Depth (0–3) | Bloom's L4–L6

Award points based on the highest cognitive level reached across all answers.

| Score | Level reached | What it looks like |
|-------|--------------|-------------------|
| 0 | L1–L2 (Remember / Understand) | Pure event description. "I added X. Y happened. I fixed it." No reasoning, no cause. |
| 1 | L3 (Apply) | Followed a known procedure. Named what they did but didn't explain why it works or what assumption was at play. |
| 2 | L4 (Analyze) | At least one causal chain: "X failed because Y led to Z." Cause is technical or structural, not "I wasn't careful." |
| 3 | L5–L6 (Evaluate / Create) | Judges the past decision ("I was wrong to assume X") AND derives a generalizable principle or process change. Not just "fix this bug differently" but "this class of bugs requires Y approach." |

**Anti-pattern to penalize:** Attributing failure to effort or attention ("I should have been more careful") instead of a structural cause. Cap at score 1 if the only cause offered is effort-based.

---

## D2 — Cycle Completeness (0–2) | Kolb

Check whether all four stages of the learning cycle are present across the answers:
- **CE** — Concrete Experience: describes what happened (floor, almost always present)
- **RO** — Reflective Observation: steps back and examines ("looking back", "what surprised me", "I hadn't expected")
- **AC** — Abstract Conceptualization: derives a principle or rule ("this means that X is generally true", "the pattern here is", "now I understand that")
- **AE** — Active Experimentation: states a concrete next action ("next time I will", "I'll add X to my checklist")

| Score | Stage coverage |
|-------|---------------|
| 0 | CE only — event described, nothing examined or derived |
| 1 | CE + one of: RO or AE. Stepping back without deriving a rule, or planning without understanding why. |
| 2 | All four stages present. AC is the critical gate — a generalizable principle must be explicitly stated, not implied. "Next time I'll test more" without stating WHY is AE without AC. |

**The AC test:** Can you extract a sentence from the answers that reads like a rule or a revised mental model, independent of this specific ticket? If yes, AC is present.

---

## D3 — Loop Depth (0–2) | Argyris / Schön

Determines whether the reflection revises a mental model (double-loop) or only adjusts behavior (single-loop).

| Score | Loop level |
|-------|-----------|
| 0 | Single-loop only. The fix adjusts an action ("I'll test more", "I'll check the docs") but the underlying assumption is unchanged. The governing belief about how the system works is never examined. |
| 1 | Implicit assumption questioning. The answer hints at a wrong assumption but doesn't name it explicitly. "I didn't realize X" without stating what prior belief X contradicted. |
| 2 | Double-loop. A specific prior belief is named AND revised: "I assumed X because [reason], but actually Y, which means my model of Z was wrong." The thermostat test: does the answer question why the setting was chosen, or just adjust the setting? |

**Schön bonus signal:** Any answer that surfaces tacit knowledge — "I always do X without thinking about it" or "I operate on the implicit rule that Y" — is double-loop even if the word "assumed" isn't present.

**Common false positive:** "I assumed the tests would catch this" scores 1, not 2, unless the answer also states what prior belief made that assumption reasonable and why it was wrong.

---

## D4 — Actionability (0–2) | Ericsson Deliberate Practice

Evaluates Q4 primarily ("What would you do differently") but also any commitment stated in Q3.

| Score | Actionability level |
|-------|-------------------|
| 0 | No next action, or a vague behavioral reminder: "be more careful", "remember to X", "do it earlier", "test more". Time or effort adjustment with no process change. |
| 1 | Specific skill gap identified but the practice target is vague: "I'll read the TypeORM docs" without saying which section, what question they're answering, or how they'll know they've internalized it. |
| 2 | Specific gap + concrete artifact or check. Names a thing that will exist after the practice: a checklist, a decision record template, a contract test, a specific doc to annotate, a question to answer before touching a class of files. The success criterion is implicit or explicit. |

**The artifact test:** Does the answer name something that will exist after the action is taken? If yes, score 2. If it's a mental note with no external artifact, score 1 at best.

**N/A handling:** If Q4 is "nothing, approach was correct" — award 1 if a clear rationale is given for why no change is needed (the reasoning demonstrates that the situation was correctly understood). Award 0 if no rationale is offered.

---

## D5 — Linguistic Quality (0–1) | Pennebaker / LIWC

Scan all four answers for:
- At least one **causal connector** where the subject is technical or structural: because, since, led to, caused, result, therefore, thus, consequently. ("Because I wasn't careful" does NOT count — the cause must be a system behavior or structural fact, not an effort attribution.)
- At least one **insight marker**: realize, understand, now I know, I see that, I recognize, I discovered, I learned that [+ specific proposition], I didn't know that.

| Score | Signal |
|-------|-------|
| 0 | Neither marker present, or only effort-attributed causal language |
| 1 | Both a structural causal connector AND an insight marker are present |

---

## Anti-Patterns (cap or penalize regardless of other scores)

| Anti-pattern | What it looks like | Effect |
|-------------|-------------------|---------| 
| Effort attribution | "I should have been more careful / more thorough / paid more attention" | Cap D1 at 1 |
| Circular causation | "It was hard because it was complex / complicated / difficult" | D1 cannot exceed 1 for that answer |
| Vague learning claim | "I learned a lot about X" / "X is important" | D2 AC stage not satisfied |
| Temporal resolution only | "Next time I'll do this earlier / sooner / at the start" | D4 = 0 |
| Other-attribution only | "The docs were wrong" / "The ticket was unclear" with no self-agency follow-up | D3 = 0 if no self-correction |
| Restating the fix | "I learned to always add migrations" — rule without supporting reasoning | D2 AC not satisfied |

</rubric>

<output_format>

Output the score block in this exact format:

```
─────────────────────────────────────────────────────────────────────────────
Reflection scored: {TICKET}

  D1 Cognitive Depth    {0–3}/3   {one-line specific feedback}
  D2 Cycle Completeness {0–2}/2   {one-line specific feedback}
  D3 Loop Depth         {0–2}/2   {one-line specific feedback}
  D4 Actionability      {0–2}/2   {one-line specific feedback}
  D5 Linguistic Quality {0–1}/1   {one-line specific feedback}
  ─────────────────────
  Total                 {X}/10

  {Band label}: {Reporting | Noticing | Analyzing | Internalizing | Mastering}

  {2–3 sentences: what was strongest, what to push deeper on next reflection.
   Be specific — reference the actual words or sentences from the answers.}
─────────────────────────────────────────────────────────────────────────────
```

**Score band labels:**

| Score | Label | Meaning |
|-------|-------|---------|
| 0–3 | Reporting | Recounted events. No learning encoded yet. |
| 4–5 | Noticing | Identified something interesting but didn't process it to a principle. |
| 6–7 | Analyzing | Found a cause and updated a behavior. Single-loop learning is happening. |
| 8–9 | Internalizing | Revised a mental model or implicit assumption. Double-loop reached. |
| 10 | Mastering | Extracted a generalizable principle with a concrete practice plan. Rare. |

**Tone:** Direct, not padded. Name specific sentences from the answers when giving feedback.
Don't praise vague answers. The score is feedback, not validation.

</output_format>

<rules>

- Score the reflection as a whole — don't average per-question. One great Q3 can carry D1 and D2.
- D1 ceiling is the highest level reached anywhere across all four answers.
- D2 AC gate is strict — "next time I'll test more" without an explicit rule is AE without AC.
- D3 double-loop requires a named prior belief, not just "I assumed X." The belief must be shown to be wrong.
- D4 artifact test is binary — does a concrete thing exist after the action? Yes = 2, no = 1 or 0.
- Never award points for length. A 2-sentence answer at L5 beats a 10-sentence answer at L1.
- If all answers are N/A or minimal, score honestly at 0–2. The score is only useful if it's calibrated.

</rules>
