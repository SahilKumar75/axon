# Axon — Novel Directions Brainstorm (Session 009, 2026-07-21)

Fresh directions aimed at "never built before," found after the second literature sweep.
The crowded parts (perturbation/neighborhood detection, cross-model disagreement, self-
consistency, semantic entropy, internal probes) are tools, not claims. These five are where
Axon can be genuinely new. Ordered simplest first.

## Direction 1 — "Cling time" as a brand-new measuring stick  [top pick]
Invent a standard number for HOW STUBBORNLY a model holds onto a dead rule after it changes.
Call it the model's "adaptivity half-life." Rank many models by it.
- Why novel: nobody has a standard metric for stubbornness / adaptivity under rule change.
- Why good: cheap, small, reusable by others, metrics get cited for years. It is ours.

## Direction 2 — The model watches its own confusion and fixes itself  [top pick]
The agent notices ITS OWN branches spraying apart and thinks "I'm confused, let me test
before I commit." Detection and action become one loop, inside the agent.
- Why novel: most work bolts an external detector on; a self-triggered loop inside an acting
  agent, under changing rules, is open.

## Direction 3 — Don't just say "wrong", say WHAT KIND of wrong
Classify the flavor of confident-wrong: (a) clinging to an old rule, (b) jumping to a
conclusion too early, (c) fixating on one clue. Each type needs a different fix.
- Why novel: everyone outputs one danger number; naming the failure TYPE (and routing it to
  the right repair) is new. Can reuse the old branch-shape idea here with a purpose.

## Direction 4 — Spend probes only when it is worth it
Shaking the question (probing) costs tokens. Teach the agent WHEN to bother: probe near a
suspected rule change, stay quiet otherwise. A "probing budget" that pays for itself.
- Why novel: cost-aware / budgeted probing under rule shift is barely explored, and practical.

## Direction 5 — Is stubbornness a fixed trait of a model?
Test whether a model's cling time on one task predicts its cling time on a totally different
task. If yes, stubbornness is a stable trait ("this model is rigid, that one adapts").
- Why novel: nobody has shown cling time transfers across tasks as a model-intrinsic property.

---

## Recommended lead: combine Direction 1 + Direction 2
Paper in one sentence:
"We introduce CLING TIME, a new measure of how long a model clings to a dead rule, and a
SELF-TRIGGERED loop that watches its own confusion and revises early; on tasks where the
rules change, this cuts cling time and adapts faster than PROBE alone."

Why this triad is unbuilt: a NEW METRIC (cling time) + a SELF-TRIGGERED METHOD (watch own
divergence, revise) + PROOF it adapts faster. The detector parts are borrowed; the metric and
the live loop are the novelty. Directions 3-5 are backups / extensions.
