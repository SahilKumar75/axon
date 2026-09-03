# Axon — Open Questions (things that block progress)

Ordered by how much they block. Answer top-down.

## Q1 (BLOCKING) — Reconverge vs diverge definition

Does a branch "reconverge" when it reaches the SAME answer as its siblings
(self-consistency), or when it reaches ANY stable answer at all (stability)?
Everything downstream depends on this. Recommendation: start with self-consistency
because it is measurable without a verifier.

## Q2 (BLOCKING) — Ground-truth task family

Need tasks where "wrong" is objective, so hallucination is not a judgement call.
Candidates: tunable synthetic sequential-reasoning tasks (known path length),
unanswerable math word problems (a wrong confident answer = hallucination by
construction), multi-hop QA with gold answers. Pick one primary + one secondary.

## Q3 — Which framing is the paper?

Measurement (where is the boundary) vs failure characterisation (what happens at it) vs
early-warning (predict it before it happens). Front-runner: early-warning, because it is
the most novel and it is the trigger PROBE needs.

## Q4 — First model

One 7B-8B open model to build against (Llama 3.1 8B is the natural choice — already used
in PROBE via OpenRouter). Scale to 2-3 sizes only after Stage 3 works.

## Q5 — Is the "expose internal signals via an interface" sub-idea worth reviving?

Parked. Only revisit if token-level logprob/entropy turns out to be a weak divergence
signal and richer internals are needed. Not the contribution either way.

## Q6 — Is the pressure cooker (C4) a core contribution or a robustness add-on?

Front-runner: robustness add-on that independently reproduces C2. Promote to core only if
solo-branching C2 is weaker than hoped. Needs a multi-agent-debate lit check first.

---

# Updated for the pivot + derived claims (2026-07-21)

## Q1 (BLOCKING, revised) — Define the perturbation set and divergence metric
What perturbations generate divergence: cross-seed only, + prompt paraphrase, + embedding
perturbation, + small cross-model ensemble? And the metric on top (answer-disagreement rate,
semantic-cluster entropy). Recommendation: start cross-seed + paraphrase + a 2-model
ensemble; metric = semantic-cluster disagreement.

## Q2 (BLOCKING, revised) — Lock tasks
Confident-wrong regime = PROBE rule-shift bosses (I3, I6) — already built. Add ONE static
control (a stable-rule task) so the blind-spot contrast is visible. Confirm objective
ground truth for "about to be confidently wrong."

## Q7 — N1: what is the counterfactual probe action, concretely?
A single injected question testing the held rule ("assuming rule X, predict this outcome"),
scored against the observation. Need to define its token budget and how its answer is turned
into a signal.

## Q8 — N2: how is "confidence" measured for the cling curve?
Options: verbalized confidence, max token prob of the answer, self-consistency agreement.
Pick one primary (recommend self-consistency agreement, since it is the thing that stays
falsely high — that IS the cling).

## Q9 — Which new claim is claim #2 of the paper (after C-A)?
Front-runner: N1 (active probe), because it is the most clearly novel and most PROBE-unifying.
N2 (cling curve) is the cheapest and most intuitive. Could run both; N1 headlines the second half.

## Q10 — Stage 2 stop gate: what to do with reversed confidence?
The 2026-07-23 Stage 2 pilot found that normal uncertainty fails after the shift, but
reversed agreement separates wrong from right in that same window. Decide whether this is a
baseline Axon must beat, or whether the claim should move toward detecting when confidence
changes meaning under rule shift.

Answer after Stage 4: treat reversed agreement and reversed entropy as mandatory baselines.
The active stale probe beat both on AUROC in the post shift contest. Cling timing remains
open because the AUROC gap was positive but its confidence interval crossed zero.

---

# LOCKED ANSWERS (2026-07-21)

## Q1 — LOCKED: measure disagreement as "same answer or not"
Run the model a few times / branch it, then check whether the branches land on the SAME
answer or split. Reason: simplest to measure, works on any model (behavioral, no internals
needed). Fancier signals (does it settle at all, entropy, internals) come later as variants.

## Q2 — LOCKED: PROBE rule-shift tasks + one steady control
Primary testbed = PROBE's rule-change tasks (I3, I6). Reason: already built (near free), we
own the true rule (perfect ground truth), and the rule flip is exactly where the model goes
confidently wrong. Add ONE steady/no-change task as the contrast, to show the problem only
appears when rules change.

Principle behind both: start with the cheapest, clearest option that still proves the point;
add harder tasks and smarter signals only after the simple version works.

---

# Q1 CORRECTED (2026-07-21) — important fix

Earlier Q1 was locked as "do the branches land on the same answer" = plain self-consistency.
That is WRONG for our target: when a model is confidently wrong the branches AGREE on the
wrong answer, so plain agreement goes blind exactly where we need it. This is the documented
self-consistency blind spot (NCB, cross-model disagreement papers).

CORRECTED Q1: the divergence signal must come from SHAKING the question, not re-running it:
- rephrase / paraphrase the prompt (neighborhood consistency, NCB style)
- ask a counterfactual probe ("if the old rule still held, what then?") = our N1
- use a second model (cross-model disagreement)
Plain branch-agreement (self-consistency) is now a BASELINE we must beat, not our detector.
