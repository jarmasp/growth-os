---
framework: "Argyris & Schön's Double-Loop Learning"
source: "Chris Argyris & Donald Schön, Organizational Learning II: Theory, Method, and Practice, 1996 (concept introduced 1978)"
tags: [framework, learning-science]
---

# Double-Loop Learning

> Fixing the action without questioning the belief that produced it is
> single-loop learning. Revising the belief itself — admitting the thermostat
> was set wrong, not just that the room is cold — is double-loop, and it's rarer
> and more valuable.

## Core Idea

Argyris and Schön's classic image is a thermostat: a thermostat that notices the
room is too cold and turns on the heat is doing single-loop learning — it
corrects an error within a fixed goal (the set temperature) without questioning
the goal itself. A thermostat that asked "why is 68°F the right target at all?"
would be doing double-loop learning — revising the governing variable, not just
the action taken to satisfy it.

Applied to people: single-loop learning changes *what you do* in response to an
error ("I'll test more," "I'll check the docs first"). Double-loop learning
changes *what you believed* that made the error possible in the first place
("I assumed the framework retried failed requests automatically — it doesn't —
so my mental model of how this client behaves under network failure was
wrong"). Single-loop is necessary and common. Double-loop is rarer because it
requires naming a belief you didn't know you were operating on, and admitting
it was wrong — which is uncomfortable in a way that "I'll be more careful" is
not.

Argyris's related concept of "theories-in-use" vs. "espoused theories" matters
here too: people are often unaware of the actual belief that drove their
decision, defaulting instead to the first repair at hand (add a test, add a
rule) because surfacing the underlying belief takes more effortful reflection.

## How Growth OS Applies It

`agents/reflection-scorer.md`'s **D3 — Loop Depth** (0–2) is this distinction
directly: 0 is single-loop only (the fix adjusts an action, the belief is never
examined), 1 is implicit assumption-questioning ("I didn't realize X" without
naming what prior belief X contradicted), and 2 requires a *named* prior belief
that's shown to be wrong — "I assumed X because [reason], but actually Y, which
means my model of Z was wrong." The rubric's "thermostat test" asks directly:
does the answer question why the setting was chosen, or just adjust the
setting?

## Further Reading

- Argyris, C., & Schön, D. A. *Organizational Learning II: Theory, Method, and
  Practice*, 1996.
- Argyris, C. "Teaching Smart People How to Learn", *Harvard Business Review*,
  1991 — the shorter, more accessible version of the same argument.
