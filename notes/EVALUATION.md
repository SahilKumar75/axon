# Axon — How We Prove It Works (evaluation protocol)

The plan for turning the claims into proof. Core idea: a head-to-head detection contest on
tasks with objective ground truth, in the specific window where the standard tools are known
to fail. Written 2026-07-21.

## The proof in one line
On tasks where we know the true answer, Axon's warning predicts the confident-wrong failure
— earlier and more reliably than every standard method — exactly in the window where those
methods go blind.

## Step 1 — Tasks with objective ground truth
Use PROBE's rule-shift tasks (I3 rule shift, I6 mixed). We set the hidden rule, so at every
step we KNOW whether the model is about to be right or wrong. That ground-truth label is what
lets us score any method. Add one static-rule control task for contrast. No ground truth = no
proof.

## Worked RuleShift example for the paper's early setup section

Use this concrete example before introducing the general notation. Before the hidden shift,
the environment maps `blue -> B`, `red -> C`, and `green -> A`. The agent sees these cues
repeatedly, receives reward feedback, and its trace therefore supports the held key
`b_t(red) = C`. At the shift time, the full-shift rule rotates every mapping, so the new
correct answers are `blue -> C`, `red -> A`, and `green -> B`.

  time       cue    agent answer   correct answer   reward   G0 cling   G1 contradicted
  t < tau    red    C              C                1        1          0
  t = tau    red    C              A                0        1          0
  t+1        red    C              A                0        1          1

At `t = tau`, G0 fires immediately because the answer still matches the agent's own held
key, while G1 is silent because no contradiction has yet been observed for that exact
`(red, C)` pair. At `t+1`, G1 can fire because the earlier zero reward is now part of the
observable history. This is the anticipatory-versus-reactive distinction behind the lead-
time tradeoff.

The partial-shift case is essential to the interpretation. If `blue` is unchanged while
`red` and `green` rotate, then a post-shift answer `blue -> B` earns reward 1 but still
matches the held key, so G0 fires on a correct unchanged item. That is why G0 is strong at
broad shifts but can invert when most cues remain unchanged; it is not a bookkeeping detail
and should be visible before the formal definitions.

## Step 2 — Turn every method into a "danger score"
At each step, Axon and every competitor output one number: probability the model is about to
be confidently wrong. Then we test whether that number actually predicts the failure. Primary
measure = AUROC (how well the score separates soon-wrong from soon-right; 1.0 perfect, 0.5 =
coin flip). Also report precision/recall.

## Step 3 — Baselines Axon must beat (mandatory)
- self-consistency (answer agreement across samples)
- semantic entropy
- token / sequence log-prob confidence, when exposed by the recorded interface
- verbalized confidence ("how sure are you?")

Add two trivial controls that a skeptical reviewer can reproduce:

- step index / elapsed time since the registered shift; and
- naive answer novelty/change, defined as whether the current answer differs from the
  immediately preceding answer (or the pre-registered prior answer), without consulting
  the historical mode used by G0.

The time and answer-change baselines test whether the reported signal is merely episode
position or answer movement rather than a stale-key diagnostic. Log-probability remains
conditional: first audit whether the stored backbone interface exposes token or sequence
logprobs; if it does not, record that absence and do not replace it post hoc with another
score.

### Reviewer baseline registration — no runs yet

Before any new baseline run, register the exact trace subset, scoring window, seed set,
and score direction in `notes/RESEARCH_LOG.md`. The pre-run qualitative predictions are:

1. elapsed time alone should not transfer across shift fractions or static controls;
2. answer novelty should be informative in conditions with an actual answer transition,
   but should not be treated as evidence that the historical-key G0 feature is unique; and
3. logprob/calibration will be reported only when directly available from the recorded
   interface, with no substitute if unavailable.

These are predictions, not results. No experiment should be run until the corresponding
trace source and fixed evaluation window are written into the research log.
These controls are what reviewers will expect to see in the comparison table.

## Step 4 — The proof is the gap in the danger zone
Zoom into the post-shift confident-wrong window. Thesis: the baselines break there. Show
their AUROC falls toward 0.5 (blind) while Axon's stays high. THAT gap is the proof.
Kill condition: if the baselines predict the post-shift failure as well as Axon (no blind
spot in practice), the idea failed — and we report that.

## Stage 2 pilot result (2026-07-23)
Llama 3.1 8B, 5 seeds, 20 steps, shift_at 10, k=5.

- Shift post confident wrong: 0.400, 95 percent CI [0.200, 0.600].
- Shift pre confident wrong: 0.080, 95 percent CI [0.000, 0.200].
- Steady post confident wrong: 0.000, 95 percent CI [0.000, 0.000].
- Shift post minus shift pre: 0.320, 95 percent CI [0.120, 0.560].
- Shift post minus steady post: 0.400, 95 percent CI [0.200, 0.600].
- Normal self consistency danger score, 1 minus agreement, had post shift AUROC 0.200,
  95 percent CI [0.075, 0.370].
- Semantic entropy had post shift AUROC 0.210, 95 percent CI [0.075, 0.397].
- Best direction AUROC was 0.800 for agreement and 0.790 for entropy. This means ordinary
  uncertainty points the wrong way, but reversed confidence is a strong baseline.

Stop gate note: do not proceed to detector claims until the next stage includes reversed
agreement or confidence cling as a baseline.

## Stage 3 pilot result (2026-07-23)
Same traces, no new model calls. Confidence = branch agreement.

- Accuracy collapse step: 10.
- First group confidence dip step: 12.
- Group cling time: 2 steps.
- Seed mean cling time: 1.800 steps, 95 percent CI [0.800, 3.000].
- Pre shift agreement: 0.632.
- Post shift agreement: 0.632.
- Agreement change: 0.000.

Interpretation: there is a short first-dip cling time, but no sustained confidence collapse
in the 5 step post shift window. Stage 4 must beat normal uncertainty, reversed agreement,
reversed entropy, and this simple cling signal.

## Stage 4 pilot result (2026-07-24)
Same traces plus an active contradiction probe. Scored on shift steps 10 through 14.

- Axon stale probe AUROC: 0.950, 95 percent CI [0.875, 1.000].
- Reversed agreement AUROC: 0.800, 95 percent CI [0.620, 0.929].
- Reversed entropy AUROC: 0.790, 95 percent CI [0.591, 0.927].
- Cling timing AUROC: 0.750, 95 percent CI [0.478, 0.952].
- Normal self consistency danger AUROC: 0.200, 95 percent CI [0.071, 0.380].
- Semantic entropy AUROC: 0.210, 95 percent CI [0.073, 0.409].
- Axon minus reversed agreement AUROC gap: 0.150, 95 percent CI [0.009, 0.340].
- Axon minus reversed entropy AUROC gap: 0.160, 95 percent CI [0.020, 0.365].
- Axon minus cling timing AUROC gap: 0.200, 95 percent CI [-0.018, 0.485].

Stop gate note: passes on point estimate and beats reversed confidence with positive AUROC
gap intervals. The gap over cling timing is not clean, so cling timing remains a mandatory
baseline.

## Step 5 — Lead time proves "early" (C-B)
Record how many steps BEFORE the actual failure Axon's signal fires. Positive mean lead time
over many runs = the early-warning claim proven. Kill: signal only spikes at the same step
the error appears (no warning).

## Step 6 — Cross-scale (C-C)
Repeat Steps 4-5 on the recorded backbones `meta-llama/llama-3.2-3b-instruct`,
`meta-llama/llama-3.1-8b-instruct`, and `meta-llama/llama-3.3-70b-instruct`. Same signature
across sizes would support transfer across checkpoints, not a clean causal scaling law,
because the generations differ.

## Step 7 — PROBE connection (application note, not a primary result)
Keep the main Axon paper self-contained and state the diagnostic-to-intervention connection
briefly in Discussion/Future Work. Existing PROBE I3/I6 numbers are imported evidence, not
new Axon runs. A future integrated experiment may feed Axon's signal into PROBE's revision
trigger, but it must be registered separately before execution.

## Table reporting and sample-size convention

Tables 6, 7, 8, and 10 must display each AUROC as `point [95% bootstrap CI]` with the
condition-wise `n` in the table or caption. Table 3's lead-time cells must show the mean
lead interval, false-alarm rate, and false-alarm denominator together. Do not create an
interval for a quantity whose bootstrap has not been run.

Unless a caption says “pooled,” `n` is per listed condition: RuleShift has 240 scored rows
per overlap condition; the fact stream has 600 per changed fraction and per backbone; and
external benchmark counts are per benchmark and shift fraction. If a pooled total is shown,
label it separately from the primary condition-wise estimate.

## What makes it proof and not cherry-picking
- Confidence intervals on every number (bootstrap 95 percent, like PROBE).
- Pre-register each claim BEFORE running: write down "Axon wins if AUROC gap > X and mean lead
  time > 0; it fails otherwise." Then whatever happens, the result is honest.

## Claim -> test map (quick reference)
- C-A confident-wrong detector: Steps 2-4, the AUROC gap in the post-shift window.
- C-B early warning: Step 5, positive lead time.
- C-C cross-scale: Step 6.
- N1 active probe > passive: add a condition that spends one counterfactual probe step;
  compare its lead time / AUROC against the best passive signal.
- N2 cling curve: plot accuracy and confidence vs step around the shift; measure the lag
  ("cling time"); correlate with PROBE's benefit per task.
- C-D debate (optional): run the sealed arena on the same tasks; check debate divergence
  predicts the confident-wrong group answer, matching the C-A signal.

---

## The gold standard: what we compare responses against
To catch WRONG and OVERCONFIDENT answers we need two things per response:
1. the known correct answer (to label right vs wrong), and
2. the model's confidence (how sure it was).
Overconfident = SURE + WRONG at the same time. That combo is the target the detector must
catch.

## Benchmarks (our answer to "ReAct/Reflexion/Voyager use external benchmarks")
Two layers, so we are not only grading our own homework:

Home turf (controlled, perfect ground truth):
- PROBE rule-shift tasks (I3, I6). We set the hidden rule, so we always know the truth, and
  confident-wrong is guaranteed at the rule flip.

Outside benchmarks (independent, known answers, famous for confident errors):
- TruthfulQA — built to bait confident false answers.
- Unanswerable math word problems (e.g. TreeCut) — a confident answer is overconfident by
  construction.
- Multi-hop QA (HotpotQA-style) — gold answers, models often confidently wrong.

Same strategy as ReAct / Reflexion / Voyager (prove it on outside benchmarks too), but the
benchmarks are chosen for OUR question — catching confident-wrong — not general task success.
