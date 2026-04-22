<purpose>

Score a completed weekly review against a multi-framework rubric derived from learning science.
Receives the four interview answers and the gathered context from the weekly workflow.
Returns a 10-point score with per-dimension breakdown, one actionable note per answer,
AND specific resource recommendations to improve the lowest-scoring dimensions before
the next weekly review.

Frameworks applied:
- Ericsson Deliberate Practice — learning velocity and practice quality
- After Action Review (US Army / NATO) — pattern recognition and systemic causation
- Kirkpatrick Model + Klein Accelerated Expertise — gap specificity and actionability
- Dreyfus Model of Skill Acquisition — capability assertion quality and evidence
- Behavioral Science / Habit Tracking — drill adherence and commitment concreteness

</purpose>

<input>

The caller (weekly-review workflow) passes:
- `WEEK` — week identifier (e.g. "2026-[W]17")
- `TICKETS` — list of ticket IDs and one-sentence summaries from this week
- `CONCEPTS` — wikilink slugs encountered in ticket reflections this week
- `DRILLS_OVERDUE` — list of overdue drills from homework-log.md
- `W_Q1` — user's answer to "¿Qué patrón se repitió esta semana?"
- `W_Q2` — user's answer to "¿Qué brecha de skill quedó expuesta?"
- `W_Q3` — user's answer to "¿Qué puedes hacer esta semana que antes no podías?"
- `W_Q4` — user's answer to drills — done or scheduled with specific date/time

</input>

<rubric>

Score the review as a whole on five dimensions. Each answer can contribute to any dimension —
read all four together before scoring. Total = 10 points.

---

## W1 — Learning Velocity (0–3) | Ericsson Deliberate Practice

Does this week represent deliberate practice (targeting a specific skill edge with feedback
and repetition) or just task completion?

| Score | Level | What it looks like |
|-------|-------|--------------------|
| 0 | Task completion only | "Did tickets, moved on." No evidence that skill edge was targeted. Answers describe what happened, not what was practiced. |
| 1 | Incidental learning | Something new was noticed but not actively practiced. "I learned about X" without specifics. Skill moved because of exposure, not deliberate effort. |
| 2 | Targeted practice | One skill demonstrably advanced. User can articulate before/after state on a specific dimension. Drill done OR concept article written/deepened. |
| 3 | Deliberate practice loop closed | Specific gap from a prior week targeted + practiced + feedback received. Evidence that the growth system is compounding: this week's practice was informed by last week's gap. |

**The compound test:** Is there evidence that a prior-week gap was closed this week? If yes, score 3. "I had noted X as a gap last week and this week I deepened it by doing Y" is the signal.

---

## W2 — Pattern Recognition (0–2) | After Action Review + Argyris Double-Loop

Did a recurring theme surface across tickets this week — traced to a structural cause, not a
one-off event?

| Score | Level | What it looks like |
|-------|-------|--------------------|
| 0 | Each ticket in isolation | No cross-ticket patterns named. Events described but not connected. W-Q1 is "N/A" or describes a single-ticket event. |
| 1 | Pattern noticed, cause not traced | A theme is named ("same guard issue again") but the structural reason is not identified. What property of these tickets makes them share this theme? Not answered. |
| 2 | Pattern + structural cause named | A recurring theme named AND traced to a structural cause: "X keeps happening because Y is a property of this domain / codebase / team dynamic." The cause is structural (a design decision, a team process, a knowledge gap), not effort-based ("I keep forgetting"). |

**The cross-ticket test:** Can the named pattern be extracted from the answer as a rule that would apply to FUTURE tickets — not just the ones this week? If yes, score 2.

**Anti-pattern:** "Same kind of ticket again" without explaining WHY these tickets share a property → score 1.

---

## W3 — Gap Specificity (0–2) | Kirkpatrick + Klein Accelerated Expertise

Are the learning gaps specific enough to act on without further clarification?

| Score | Level | What it looks like |
|-------|-------|--------------------|
| 0 | No gap identified, or vague domain reference | "Need to learn more GCP." "I don't fully understand auth." Unactionable without further narrowing. |
| 1 | Gap named, not bounded | Concept identified but the specific question is not stated: "I don't fully understand Reflector." What specifically? What can't you do that you need to do? |
| 2 | Gap bounded by a specific answerable question | The gap is a sentence that could go directly into a Google search or a concept article title: "Why does Reflector.get() return undefined when the metadata key isn't registered — what is the lookup chain?" OR "What is the difference between @SetMetadata and a custom decorator for Reflector in terms of DI scope?" |

**The search test:** Could the gap statement be pasted into a search engine and return useful results? If yes, score 2. If it's too vague to search, score 1.

**N/A handling:** If W-Q2 is "N/A" and the user has a reasonable rationale (week was consolidation, no new territory), award 1. If N/A with no rationale, award 0.

---

## W4 — Capability Assertion Quality (0–2) | Dreyfus Skill Model

Does "Esta semana puedo" make a specific, evidence-backed capability claim that signals
progression on the Dreyfus scale?

| Score | Level | What it looks like |
|-------|-------|--------------------|
| 0 | Empty, vague, or missing | "I improved this week." "Got better at X." No specific skill named. No evidence cited. |
| 1 | Skill named but not grounded | "I can compose NestJS guard chains now." Missing either: the evidence (which ticket?), or the deployment context (when would I use this?), or both. |
| 2 | Skill + evidence + deployment context | "I can compose NestJS guard chains with Reflector-based skip logic (ALDS-2607). I can now review or propose similar patterns in code review without needing to look up the mechanism." Three elements present: specific skill, ticket evidence, forward deployment signal. |

**Dreyfus progression check:** Does the assertion imply movement on the scale?
- Novice → Advanced Beginner: "I can follow the pattern now" (needs explicit example to apply)
- Advanced Beginner → Competent: "I can recognize when to apply it" (context-dependent judgment)
- Competent → Proficient: "I can see tradeoffs and deviate when needed"
Assertions at Competent or above score 2 automatically if they have evidence.

---

## W5 — System Health (0–1) | Behavioral Science / Habit Tracking

Are recurring drills tracked and actioned — either done this week or committed to with a
specific scheduled time?

| Score | Signal |
|-------|--------|
| 0 | Drills noted as overdue with no action taken and no specific schedule committed. "I'll do it soon" or "next week" without a day and approximate time. |
| 1 | Either: (a) at least one drill was completed this week, OR (b) every overdue drill has a concrete scheduled slot this sprint ("PR rewrite: Thursday 7–8 pm" is acceptable; "this week sometime" is not). |

**The calendar test:** Does the answer name a specific day? If yes, score 1. If it names a week or "soon", score 0.

---

## Anti-Patterns (cap or penalize regardless of other scores)

| Anti-pattern | What it looks like | Effect |
|-------------|-------------------|---------| 
| Effort attribution | "I need to be more disciplined / focused / careful" | Cap W1 at 1 |
| Other-attribution only | "The tickets were unclear / the team didn't communicate" with no self-agency follow-up | W2 = 0 for that signal |
| Vague learning claim | "I learned a lot" / "It was a busy week" | W4 cannot exceed 0 |
| Restating what was done | "I did tickets X and Y" as the capability assertion | W4 = 0 |

</rubric>

<output_format>

Output the score block AND the resource recommendations in this exact format:

```
─────────────────────────────────────────────────────────────────────────────
Weekly review scored: {WEEK}

  W1 Learning Velocity     {0–3}/3   {one-line specific feedback}
  W2 Pattern Recognition   {0–2}/2   {one-line specific feedback}
  W3 Gap Specificity       {0–2}/2   {one-line specific feedback}
  W4 Capability Assertion  {0–2}/2   {one-line specific feedback}
  W5 System Health         {0–1}/1   {one-line specific feedback}
  ─────────────────────
  Total                    {X}/10

  {Band label}: {Logging | Noticing | Growing | Accelerating | Compounding}

  {2–3 sentences: what was strongest, what to push deeper on next week.
   Reference specific words from the answers — no generic feedback.}

📚 Para la próxima semana:
  {One bullet per low-scoring dimension (score < max). Rules:}

  · [W1] If low: name a specific practice target from the user's own domain —
    a drill from DRILLS_OVERDUE, or a concept from CONCEPTS to deepen actively
    (not just read — write a summary, teach it, apply it).
    Never recommend external books or courses by name — the user's vault and
    homework log are the practice ground.

  · [W2] If low: suggest revisiting 2 tickets from TICKETS together to find
    the cross-ticket structural cause. Name the specific tickets.

  · [W3] If low: rewrite the gap from W-Q2 as a specific searchable question.
    Show the rewrite. Example: "Tu brecha era '{W_Q2}' — reformulada: '¿Por qué X
    ocurre cuando Y, dado Z?' Esa es la pregunta que puedes llevar a un recurso."
    If a slug from CONCEPTS matches the gap, name it: [[{slug}]] — qué sección falta.

  · [W4] If low: give the user the exact sentence structure for a strong assertion —
    fill it with their actual work: "Puedo {skill from W_Q3} — lo demuestré en
    {ticket/project from TICKETS} — lo aplicaría en {deployment context}."

  · [W5] If low (and W-Q4 has no specific slot): "Agenda un bloque específico antes
    del viernes: '{overdue drill}' — 30 min es suficiente para empezar."
    If W-Q4 already has a specific day, W5 = 1 and skip this bullet.

  Never invent domain-specific resources (books, courses, tools) not already present
  in the user's vault. The only resources to name are:
  - concept slugs from CONCEPTS that were encountered this week
  - drills from DRILLS_OVERDUE
  - the user's own tickets from TICKETS (for W2 cross-analysis)
─────────────────────────────────────────────────────────────────────────────
```

**Score band labels:**

| Score | Label | Meaning |
|-------|-------|---------|
| 0–3 | Logging | Recorded what happened. No growth signal in the review itself. |
| 4–5 | Noticing | Identified friction or a gap but didn't process it to a principle or practice. |
| 6–7 | Growing | Deliberate practice patterns emerging. Gaps specific enough to act on. |
| 8–9 | Accelerating | Prior gaps closing, patterns named with structural causes, capability advancing. |
| 10 | Compounding | Growth system fully active: prior gaps → this week's practice → next gap identified. Rare. |

**Tone:** Direct. Reference specific sentences from the answers. Don't praise vague answers.
The score is a calibration tool, not a grade. Resource recommendations must derive only
from what the user passed in (CONCEPTS, TICKETS, DRILLS_OVERDUE) — never from assumed
domain knowledge. A painter and a software engineer should get equally useful recommendations.

</output_format>

<rules>

- Score the review as a whole — one great W-Q3 can carry W4.
- W3 search test is binary: specific answerable question → 2, anything else → 1 or 0.
- W4 requires all three elements (skill + evidence + deployment) for score 2.
- W5 calendar test is binary: specific day → 1, anything vague → 0.
- Resource recommendations are ONLY for dimensions that scored below max.
- Never recommend a resource for a dimension that scored max — it wastes the user's attention.
- Never invent domain-specific books, courses, or tools. Recommendations come only from CONCEPTS, TICKETS, and DRILLS_OVERDUE passed by the caller.
- If a concept slug from CONCEPTS matches the gap in W-Q2, name it explicitly in recommendations.
- If drills are overdue but W-Q4 gives a specific schedule, W5 = 1 and do NOT add a drill reminder — it's already handled.
- The framework is domain-agnostic. A painter, an architect, and a software engineer all get scored on the same W1–W5 dimensions.

</rules>
