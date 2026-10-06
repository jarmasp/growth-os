---
framework: "Kirkpatrick Model + Klein's Accelerated Expertise"
source: "Donald L. Kirkpatrick, Evaluating Training Programs, 1994 (model dates to 1959); Gary Klein, Seeing What Others Don't, 2013 and related work on accelerated expertise"
tags: [framework, learning-science]
---

# Kirkpatrick Model + Klein Accelerated Expertise

> Most "I should learn more about X" statements are too vague to act on. A
> learning gap only becomes useful once it's a specific, answerable question —
> the kind you could paste into a search engine and get something back.

## Core Idea

Donald Kirkpatrick's four-level model evaluates training by asking
increasingly demanding questions: did people *react* well to it (Level 1), did
they actually *learn* something measurable (Level 2), did their *behavior*
change on the job (Level 3), and did it produce a *result* that mattered
(Level 4). The model's lasting contribution is less the four levels themselves
than the discipline it forces: "I learned a lot" (reaction) is a much weaker
claim than "I can now do X, demonstrated by Y" (behavior), and training that
never gets evaluated past Level 1 routinely produces no Level 3 or 4 change.

Gary Klein's research on accelerated expertise (part of the Naturalistic
Decision Making tradition) adds the mechanism: experts develop faster not by
accumulating more experience but by developing sharper, more specific
questions about the domain — a novice says "I don't fully understand
authentication," an expert on the way to mastery asks "why does this token
refresh silently fail when the clock skew exceeds 30 seconds?" The
specificity itself is the marker of progress: a gap bounded tightly enough to
be falsifiable or searchable is a gap someone can actually close. A gap stated
as a vague domain reference ("I need to learn more about Kubernetes") can't be
closed because it was never actually defined.

## How Growth OS Applies It

`agents/weekly-reviewer.md`'s **W3 — Gap Specificity** (0–2) runs the
"search test" directly from Klein's framework: a vague domain reference scores
0 ("need to learn more GCP"), a named-but-unbounded concept scores 1 ("I don't
fully understand Reflector" — what specifically?), and a gap stated as a
concrete, answerable question scores 2 — the rubric's own example is "Why does
Reflector.get() return undefined when the metadata key isn't registered — what
is the lookup chain?", which is exactly Klein's expert-level question, not the
novice-level domain name. The recommendation step for a low score rewrites the
stated gap into that searchable form, modeling the move directly.

## Further Reading

- Kirkpatrick, D. L. *Evaluating Training Programs: The Four Levels*, 1994.
- Klein, G. *Seeing What Others Don't: The Remarkable Ways We Gain Insights*,
  2013.
