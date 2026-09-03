# Axon — Research Campaign Roadmap (rewritten 2026-08-20)

Replaces the 2026-07-21 version, which was written before the locked five claims, before
the oracle confound was found, and before any of the gate work. That version described the
detector as perturbation divergence and numbered its stages so that they did not match the
trace directories on disk. Both are fixed here.

## What Axon is, in one line

A detector. Given an agent acting under a hidden rule that can change, it flags the steps
where the agent is confidently wrong. It costs zero model calls.

## The detector, as actually measured

Not perturbation divergence. That was the July design and it lost to simpler things.
What works is a deterministic gate over the agent's own trace:

  G0 cling          is the agent still answering the key its own past answers say it
                    believes? AUROC 0.776 at a full shift, inverts to 0.364 when most cues
                    keep their key.
  G1 contradicted   has this exact (cue, key) pair already earned reward 0? Flat at 0.75
                    across every overlap level, never inverts, but cannot fire until
                    something has already been missed.

Neither wins everywhere and no runtime rule was found to pick between them. That tradeoff
is a result, recorded under claim 5.

## Stage naming

Stage numbers here match the directories in traces/. The old roadmap's numbering did not,
which is what made it confusing.

  stage2_*            trace generation, the detector's raw input
  stage3_*            cling curve (claim 2)
  stage4_*            the detection contest (claim 1, claim 3)
  stage4b_overlap/    overlap sweep, gates, lead time (claims 3', 4, 5)

## Core principle, unchanged

Each stage answers: what question, what minimal experiment, what result kills it, what
evidence does it leave. Predictions are registered in RESEARCH_LOG.md BEFORE the run, and
failed predictions are recorded as failed rather than quietly widened. Four have failed so
far and all four are in the log.

---

# DONE

## Claim 1 — the blind spot. VALIDATED
Self consistency and semantic entropy go blind on a confidently wrong model. They sit near
0.40 where the gate reaches 0.776. Accuracy falls 0.721 to 0.208 after a shift while
agreement moves only 0.638 to 0.602.

## Claim 2 — the cling curve. MEASURED, FOLDED INTO CLAIM 1
Confidence does not lag the accuracy collapse, it never arrives. The group confidence curve
is censored at every overlap level, never reaching 0.5. The per episode scalar exists
(3.10 steps) but times a transient dip and does not vary with shift size. Kept as claim 1's
plot and number, dropped as a separate headline.

## Claim 3 — asking beats watching. FALSIFIED
The active probe is at chance at every overlap level (0.453, 0.495, 0.493). The model cannot
report on whether its own rule belief has gone stale. Reported as a negative result about
LLM self report, not dropped.

## Claim 3' — watching is enough, and it is free. VALIDATED, replaces claim 3
The whole detector is one deterministic check, zero model calls, AUROC 0.775 at n=236.

## Claim 4 — early warning with lead time. MEASURED
G0 gives mean lead +0.91 steps [+0.43, +1.39] at the full shift, interval clear of zero.
But its lead grows with overlap only because it fires on 95 percent of cues that never
fail. Lands as a precision versus earliness frontier, not a single number. Lead time is
meaningless without the false alarm rate printed beside it.

## Claim 5 — the detectability limit. MEASURED, carries two limits
AUROC decays THROUGH chance and inverts as overlap grows: 0.775, 0.515, 0.364. Second
limit: no runtime rule selects between G0 and G1. Six selector variants failed, and the
reason is structural rather than tuning — the selector needs to know whether all cues
shifted, and that evidence accumulates more slowly than the decision it informs.

---

# REMAINING

Every number above is ONE model (llama 3.1 8b instruct) on ONE synthetic environment
(RuleShift, three cues). That is the entire remaining risk and the whole remaining roadmap.
The claims are done; the external validity is not.

## Stage 5 — cross scale (C-C).  NEXT, needs API spend
Repeat the gate contest on two or three model sizes. Question: is the gate's advantage a
property of rule shift or of one small model? Kill: if the gate does not beat the
uncertainty baselines on a larger model, claim 1 is about 8B models, not about LLMs.
Cost: the pipeline now runs 90 episodes in about 7 minutes, so this is hours, not days.

## Stage 6 — a second testbed.  Largest single credibility gain
A fact update QA stream: the answer to a question changes partway through. Question: does
the gate survive outside a three cue toy? Kill: if it needs the toy's structure, Axon is a
case study. This is the item most likely to be attacked in review.

## Stage 7 — frontier spot check
One frontier model on the best result only. Confirmation, not experiment.

## Stage 8 — tie to PROBE
Feed the gate into PROBE's revision trigger and show revision fires earlier or more
reliably than the hand coded contradiction detector. Detector (Axon) -> revision (PROBE).
This is the applications section, not a claim.

## Stage 9 — write the paper
Shape: claims 1, 3', 4 are the wins. Claim 3 is the negative result. Claim 5 is the honest
limit and carries both the overlap decay and the unsolved selector. Claim 2 is claim 1's
figure.

## Cut first if over budget
Stage 7. Then Stage 8. Stages 5 and 6 are not cuttable — without them there is no paper,
only a case study.
