---
framework: "Ericsson's Deliberate Practice"
source: "K. Anders Ericsson, Ralf Th. Krampe & Clemens Tesch-Römer, 'The Role of Deliberate Practice in the Acquisition of Expert Performance', Psychological Review, 1993"
tags: [framework, learning-science]
---

# Deliberate Practice

> Years of experience doesn't reliably produce expertise — only a specific kind
> of effortful, feedback-rich practice aimed at a precise weak point does, and
> most people doing a job for a long time are not doing that.

## Core Idea

Ericsson's research on expert performers (originally musicians, later chess
players, athletes, and professionals of many kinds) found that raw years of
experience correlates weakly with actual expertise. What does correlate is
*deliberate practice*: practice that (1) targets a specific, well-defined
weakness just beyond current ability, not generic repetition of what's already
comfortable; (2) is effortful and requires full concentration, not autopilot;
(3) comes with immediate, specific feedback on what was right or wrong; and (4)
involves repetition with refinement — trying again differently based on that
feedback, not just trying again.

The crucial contrast is with "naive practice" — doing the activity repeatedly
without a specific target, which plateaus quickly because the same errors go
uncorrected. A developer who has shipped tickets for five years without ever
targeting a specific gap (how transactions actually isolate, how a particular
class of race condition arises) has accumulated experience, not necessarily
expertise in that gap. The gap only closes when it's named, practiced on
purpose, and checked against feedback.

A second useful piece from the same research program: experts build rich
mental representations that let them recognize patterns and anticipate
problems — these representations are themselves built through deliberate
practice, not received as a side effect of time served.

## How Growth OS Applies It

`agents/reflection-scorer.md`'s **D4 — Actionability** (0–2) applies the
"artifact test" from this framework: does the answer name something concrete
that will *exist* after the stated action, not just a vague intention? "I'll
read the docs" scores 1 (a named gap, no concrete practice target); "I'll add a
contract test for this edge case" scores 2 (a specific artifact tied to the
actual gap).

`agents/weekly-reviewer.md`'s **W1 — Learning Velocity** (0–3) scores the whole
week against this same bar, from "task completion only" (0) up to "deliberate
practice loop closed" (3) — the top score requires evidence that a gap *named
in a prior week* was specifically targeted and practiced this week, which is
deliberate practice's defining feature: a feedback loop that actually closes,
not just activity.

## Further Reading

- Ericsson, K. A., Krampe, R. Th., & Tesch-Römer, C. "The Role of Deliberate
  Practice in the Acquisition of Expert Performance", *Psychological Review*,
  1993.
- Ericsson, K. A., & Pool, R. *Peak: Secrets from the New Science of Expertise*,
  2016 (the popular-audience synthesis).
