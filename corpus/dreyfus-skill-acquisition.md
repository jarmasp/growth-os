---
framework: "Dreyfus Model of Skill Acquisition"
source: "Stuart E. Dreyfus & Hubert L. Dreyfus, 'A Five-Stage Model of the Mental Activities Involved in Directed Skill Acquisition', 1980"
tags: [framework, learning-science]
---

# Dreyfus Model of Skill Acquisition

> Skill develops through five qualitatively different stages — Novice to
> Expert — distinguished not by how much someone knows but by *how* they
> relate to rules, context, and judgment.

## Core Idea

The Dreyfus brothers' model describes five stages, each a different mode of
operating, not just more of the same mode: **Novice** needs explicit,
context-free rules and can't yet judge when a rule doesn't apply. **Advanced
Beginner** starts recognizing recurring situational patterns ("aspects") from
experience, but still largely follows rules. **Competent** can plan
deliberately, choosing among approaches based on goals, and feels the weight of
responsibility for those choices — this stage is often experienced as the most
effortful and mentally taxing, since judgment hasn't become automatic yet.
**Proficient** perceives
situations holistically rather than as a checklist of features, intuitively
sees what matters most, but still reasons deliberately about *how to act* on
that perception. **Expert** no longer reasons about situations at all in the
normal case — perception and action are fused, intuitive, and fast, with
deliberate analysis reserved for genuinely novel situations.

The model's practical bite: the stages aren't just a ladder of "knowing more."
A Competent practitioner forcing themselves to follow Novice-level rules in a
familiar situation is operating below their actual level; an Expert who can't
explain *why* they made a call (because the judgment is intuitive, not
rule-based) isn't necessarily failing to communicate — they may be accurately
describing how expertise actually works at that stage.

## How Growth OS Applies It

`agents/onboarding-agent.md` asks directly for a `dreyfus_level` in the saved
profile — "en su práctica principal" — so later feedback is calibrated to where
someone actually is, not a generic bar.

`agents/weekly-reviewer.md`'s **W4 — Capability Assertion Quality** (0–2) uses
the model's stage transitions as a check on self-reported progress: "I can
follow the pattern now" implies Novice→Advanced Beginner, "I can recognize when
to apply it" implies Advanced Beginner→Competent, "I can see tradeoffs and
deviate when needed" implies Competent→Proficient — an assertion at Competent
or above, backed by evidence, scores the maximum. The weekly note's Skill
Domain table also uses the five-stage scale directly as its rating axis.

## Further Reading

- Dreyfus, S. E., & Dreyfus, H. L. "A Five-Stage Model of the Mental Activities
  Involved in Directed Skill Acquisition", University of California Berkeley
  Operations Research Center, 1980.
- Dreyfus, H. L., & Dreyfus, S. E. *Mind Over Machine*, 1986 (the
  book-length treatment, including the Expert stage's implications for AI).
