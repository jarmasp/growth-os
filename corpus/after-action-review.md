---
framework: "After Action Review (AAR)"
source: "U.S. Army training doctrine, formalized from the 1970s onward; adopted widely by NATO forces and later by civilian organizations"
tags: [framework, team-learning]
---

# After Action Review (AAR)

> A structured, blame-free debrief run after every significant event — not just
> failures — built around four questions: what was supposed to happen, what
> actually happened, why was there a difference, and what should we sustain or
> improve.

## Core Idea

The After Action Review was developed by the U.S. Army as a fast, disciplined
way to extract lessons from training exercises and operations, run immediately
after the event while memory is fresh, with every participant present
regardless of rank. Its four core questions are deliberately simple: *What was
supposed to happen?* (the plan or expectation), *What actually happened?* (the
observed reality, facts not interpretations), *Why was there a difference?*
(the causal analysis — this is where the actual learning lives), and *What
will we sustain, and what will we improve?* (concrete forward commitments).

Three design choices make AAR work where informal "lessons learned" discussions
often don't. First, it runs after *every* significant event, not just failures
— a success analyzed well is as instructive as a failure, and makes the
practice routine rather than punitive. Second, it's explicitly not
performance evaluation: the goal is extracting a transferable lesson, not
assigning blame, which is what lets people name their own errors honestly.
Third, the "why was there a difference" question is pushed past the first
answer — a surface cause ("the plan was unclear") is usually a symptom of a
deeper, structural one ("we never schedule time to clarify ambiguous
specs before starting"), and AAR facilitators are trained to keep asking why
until the structural layer surfaces.

## How Growth OS Applies It

`agents/weekly-reviewer.md`'s **W2 — Pattern Recognition** (0–2) is AAR's "why
was there a difference" question applied across a week's tickets instead of a
single event: a recurring theme named without a traced cause scores 1 ("same
guard issue again" — so what makes these tickets share that property?); a
theme traced to a *structural* cause — a design decision, a team process, a
knowledge gap, not an effort attribution — scores 2. The rubric's "cross-ticket
test" mirrors AAR's push past the first, surface-level answer: can the named
pattern be stated as a rule that would predict *future* tickets, not just
explain the ones already seen?

## Further Reading

- U.S. Army, *A Leader's Guide to After-Action Reviews*, Training Circular
  25-20 (the Army's own doctrinal publication, widely available and
  frequently adapted by non-military organizations).
- Darling, M., Parry, C., & Moore, J. "Learning in the Thick of It", *Harvard
  Business Review*, 2005 (a civilian-sector treatment of AAR in practice).
