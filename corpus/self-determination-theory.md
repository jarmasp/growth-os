---
framework: "Self-Determination Theory (SDT)"
source: "Edward L. Deci & Richard M. Ryan, Self-Determination Theory: Basic Psychological Needs in Motivation, Development, and Wellness, 2017 (research program dating to the 1980s)"
tags: [framework, motivation]
---

# Self-Determination Theory (SDT)

> Intrinsic motivation — doing something because it's genuinely satisfying,
> not because of an external reward or pressure — rests on three basic
> psychological needs: autonomy, competence, and relatedness. Satisfy them and
> motivation tends to sustain itself; thwart them and it has to be propped up
> externally.

## Core Idea

Deci and Ryan's decades-long research program distinguishes motivation by its
*source*, not just its presence: **extrinsic motivation** is driven by outcomes
separate from the activity itself — pay, approval, avoiding punishment, a
title. **Intrinsic motivation** is driven by the activity's own inherent
satisfaction — curiosity, mastery, enjoyment of the work itself. The theory's
central claim is that intrinsic motivation reliably emerges and persists when
three basic psychological needs are met: **autonomy** (feeling that one's
actions are self-endorsed, not controlled — having real say in how the work
gets done), **competence** (feeling effective and capable of growth, not stuck
or in over one's head), and **relatedness** (feeling connected to and valued
by others, not working in isolation or conflict).

A key, counterintuitive finding from this research program: external rewards
can actually *undermine* intrinsic motivation for an activity someone already
found satisfying (the "overjustification effect") — paying someone for a task
they loved doing for free can shift their reason for doing it from internal
to external, and the activity stops being pursued once the pay stops. The
practical implication isn't that extrinsic motivators are bad, but that they
can crowd out the more durable, self-sustaining kind if a person's basic needs
for autonomy, competence, and relatedness aren't otherwise being met by the
work itself.

## How Growth OS Applies It

`agents/onboarding-agent.md` uses SDT as a direct diagnostic lens in two
places: Phase 2 ("¿A dónde vas?") probes whether a stated 12–18 month goal is
intrinsic (mastery, craft, impact, autonomy) or extrinsic (salary, title,
recognition) — and if extrinsic, asks what would remain if the external
factor were already achieved, to surface the intrinsic layer underneath, if
any. Phase 5 ("¿Qué te importa?") maps directly onto the three pillars,
following up differently depending on whether the dominant driver sounds like
autonomy, competence (folded into mastery/craft), or relatedness/impact — each
with its own follow-up question designed to anchor that specific need in a
concrete lived example. The saved profile's `motivation_type` field is this
classification.

## Further Reading

- Deci, E. L., & Ryan, R. M. *Self-Determination Theory: Basic Psychological
  Needs in Motivation, Development, and Wellness*, 2017.
- Deci, E. L., with Flaste, R. *Why We Do What We Do: Understanding
  Self-Motivation*, 1995 (a more accessible entry point).
