---
framework: "Kolb's Experiential Learning Cycle"
source: "David A. Kolb, Experiential Learning: Experience as the Source of Learning and Development, 1984"
tags: [framework, learning-science]
---

# Kolb's Experiential Learning Cycle

> Learning from experience is a four-stage loop — having the experience,
> reflecting on it, drawing a general principle, then testing that principle in
> action — and most people habitually skip at least one stage without noticing.

## Core Idea

Kolb's model has four stages that form a cycle, not a line: **Concrete
Experience** (something happens — you ship the thing, it breaks, you fix it),
**Reflective Observation** (you step back and examine what happened, from
multiple angles, without yet jumping to conclusions), **Abstract
Conceptualization** (you form a general rule or mental model from that
reflection — not "this bug" but "this *class* of bug"), and **Active
Experimentation** (you test the new rule by doing something differently next
time, which produces a new Concrete Experience and restarts the cycle).

The cycle's real diagnostic value isn't the four stages themselves — it's that
people have a dominant *style* and reliably skip the stage furthest from it.
Someone oriented toward doing skips Reflective Observation (they ship fast,
reflect never, and the same mistake recurs). Someone oriented toward theory
skips Concrete Experience or Active Experimentation (they can explain a pattern
perfectly and never apply it). The useful move isn't to force someone into a
style that isn't theirs — it's to notice which stage is structurally missing
and scaffold specifically that one.

## How Growth OS Applies It

`agents/reflection-scorer.md`'s **D2 — Cycle Completeness** (0–2) checks whether
all four stages show up across a reflection's answers: CE is the event
description (almost always present — it's the floor), RO is stepping back
("looking back, what surprised me"), AC is the generalizable principle, and AE
is a concrete next action. The rubric's strict gate is AC: "next time I'll test
more" without a stated *rule* is AE without AC, and scores no higher than 1.

`agents/onboarding-agent.md`'s Phase 4 ("¿Cómo aprendes?") asks directly for a
learning story and listens for which stage the person's own account skips —
that becomes the `kolb_skipped_stage` field in the saved profile, carried
forward so later reflections can be read against *that specific person's* known
blind spot rather than a generic rubric.

## Further Reading

- Kolb, D. A. *Experiential Learning: Experience as the Source of Learning and
  Development*, 1984.
- Kolb, A. Y., & Kolb, D. A. "Learning Styles and Learning Spaces", *Academy of
  Management Learning & Education*, 2005 (the later elaboration of styles).
