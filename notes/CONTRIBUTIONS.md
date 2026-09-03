# Axon — Contributions (pivoted 2026-07-21)

Rewritten after the deep literature sweep (DEEP_RESEARCH_2026-07-21.md). The original
C1-C4 (branch structure, divergence-as-early-warning, cross-scale, debate) were found to be
mostly already published on STATIC tasks. The pivot keeps the branching/divergence
mechanism but aims it at a genuinely open target: the CONFIDENT-WRONG regime under RULE
SHIFT, where standard uncertainty methods are documented to fail — and which is exactly
PROBE's failure mode.

Each contribution: the claim, why it is novel, how to measure, validate/kill, PROBE tie-in.

---

## C-A — Confident-wrong detector under rule shift (HEADLINE)

### Claim
There is a zero-call step-level signal that is informative when a frozen model has crossed
from confidently right to confidently WRONG after a broad rule change. The paper also
records the important boundary: the G0 component can invert under partial shifts, so the
result is not an unconditional detector guarantee. Comparisons with semantic entropy and
self-consistency must be stated with that scope.

### Why it is novel
The whole uncertainty toolkit (semantic entropy, self-consistency, token log-prob, internal
probes) works when the model is UNSURE and breaks when it is CONFIDENTLY WRONG — it repeats
the same wrong answer, so "agreement" masquerades as confidence (documented: MIT 2026
cross-model work; GPT-4 gives max confidence to 87% of answers incl. wrong ones). That blind
spot is worst under NON-STATIONARITY (rules change), which the collapse/uncertainty
literature almost never tests. Attacking that specific regime is open.

### How to measure
- Signal is NOT plain resampling (stays confidently consistent on the stale rule). Use
  divergence under CONTROLLED PERTURBATION: cross-seed + light prompt/embedding perturbation
  + a small scale-matched cross-model ensemble.
- Hypothesis: after the rule shift, perturbation-divergence rises while plain
  self-consistency stays flat (falsely confident). That gap is the detector.

### Validates if
On rule-shift tasks, in the post-shift confident-wrong window, standard baselines drop
toward chance AUROC while Axon's perturbation/cross-model divergence still separates
soon-wrong from soon-right.

### Stage 2 status
Pilot evidence on 2026-07-23 shows the confident wrong window exists on Llama 3.1 8B:
shift post confident wrong rate 0.400, 95 percent CI [0.200, 0.600], versus 0.080 pre shift
and 0.000 steady post. Normal uncertainty direction fails: 1 minus agreement AUROC 0.200 and
semantic entropy AUROC 0.210 in the post shift window. Caveat: reversed confidence separates
wrong from right in this same window, with best direction AUROC 0.800 for agreement and
0.790 for entropy. Stage 4 must include that as a baseline.

### Stage 4 status (SUPERSEDED, see correction below)
The active stale probe beat reversed confidence on the same post shift window. Axon stale
probe AUROC was 0.950, 95 percent CI [0.875, 1.000], versus reversed agreement AUROC 0.800,
95 percent CI [0.620, 0.929], and reversed entropy AUROC 0.790, 95 percent CI [0.591,
0.927]. AUROC gap over reversed agreement was 0.150, 95 percent CI [0.009, 0.340]. Caveat:
gap over cling timing was 0.200, 95 percent CI [-0.018, 0.485], so cling timing remains a
serious baseline. **This entire result was measured under the oracle rule confound (see
2026-08-05 correction) and does not hold once fixed.**

### Stage 4 CORRECTED (2026-08-05, oracle confound removed)
Same protocol, same traces, probe rebuilt from the model's own inferred belief instead of
the ground truth rule. Axon stale probe AUROC dropped to 0.785, 95 percent CI [0.583,
0.929]. It still separates clearly from near-chance self-consistency (0.200) and semantic
entropy (0.210) -- claim 1 (blind spot) survives. But it now TIES every serious baseline:
gap over reversed agreement -0.015 [-0.270, 0.238], over reversed entropy -0.005
[-0.270, 0.272], over cling timing 0.035 [-0.159, 0.250], over raw probe rule change 0.275
[-0.106, 0.670] -- all CIs straddle zero. The "asking beats watching" win reported above
was an artifact of testing the probe against ground truth rather than the model's own
belief. Claim 3 is currently UNRESOLVED, not validated. Full numbers and next step in
RESEARCH_LOG.md, session "corrected Stage 4 numbers, oracle confound removed."

### Kills the idea if
Plain self-consistency already predicts the post-shift error just as well (no practical
blind spot), or perturbation adds no separation.

### PROBE tie-in
This IS PROBE's contradiction trigger, learned as a signal instead of hand-coded.

---

## C-B — Early warning / lead time (SUPPORT)

### Claim
The C-A signal fires a measurable number of steps BEFORE the post-shift accuracy/reward
collapse, so it predicts the failure rather than just detecting it after the fact.

### Why it is novel
Early prediction from traces exists (AUROC ~0.80 in first hundreds of tokens) but on STATIC
tasks where the model is often unsure. Lead time in the confident-wrong, post-shift regime
is not established.

### How to measure
Per episode, record the step the signal crosses threshold vs the step accuracy actually
collapses. Report precision, recall, and mean lead time. Pre-register the lead-time test so
a positive result is unambiguous.

### Validates / kills
Validates if positive mean lead time with useful precision/recall. Kills if the signal only
spikes at the same step the error appears (no warning).

### PROBE tie-in
Lead time = how many steps early PROBE can revise before committing to a confabulated action.

---

## C-C — Cross-scale generality (SUPPORT)

### Claim
The confident-wrong blind spot and the Axon trace gate can be compared across 2-3 checkpoints
within the Llama family; the observed signature is not confined to the 8B pilot. Because the
3B, 8B, and 70B checkpoints are from different Llama generations, this is evidence of
within-family transfer, not a causal scaling law.

### Why it is novel
Answers the "just an 8B artifact?" objection (the same defense PROBE needed) and turns a
single-model observation into a within-family comparison without overstating what the ladder
identifies.

### How to measure
Repeat C-A / C-B on Llama-3.1-8B + one mid + one larger (frontier spot-check at the very
end, one run, cheap).

### Validates / kills
Validates if signature holds across sizes with threshold shifting monotonically. Kills if
the failure looks qualitatively different per size.

---

## C-D — Pressure cooker (OPTIONAL robustness, cut first)

### Claim
A sealed multi-model debate is a second, independent way to surface the same divergence:
measure whether the debate reconverges on the correct answer or collapses to a confident
WRONG majority after a rule shift.

### Why it is novel / risky
Debate-as-diagnostic is a live, crowded, expensive area (debate can be a martingale;
collapses to majority; "The Confident Liar" already diagnoses it). Novelty is only the
rule-shift + confident-majority angle. Keep small (3 models, few rounds) or cut.

### PROBE tie-in
If divergence predicts confident-wrong in BOTH solo perturbation AND debate, the C-A/C-B
result is much harder to dismiss.

---

## Demoted: old C1 (branch structure)
Kept as a MECHANISM section only. Process reward models and inconsistency-score work already
study step-level tree divergence, so branch shape is not a standalone headline claim.

## Paper in one sentence
Existing uncertainty methods detect an unsure model but fail on a confidently wrong one;
Axon detects the confident-wrong crossing under rule shift, early and across model sizes,
and hands PROBE the trigger it needs.

---

# Derived novelty claims from the pivot (added 2026-07-21)

Two new claims that grow out of the confident-wrong / rule-shift pivot. Both were
novelty-checked against 2024-2026 literature (see DEEP_RESEARCH sources + notes below).
Both reuse PROBE infrastructure and run on small models.

## N1 — The active probe beats passive monitoring (STRONGEST new claim)

### Claim
Spending ONE step on a targeted counterfactual probe ("if the rule were still X, what would
happen here?") detects the confident-wrong crossing EARLIER — with more lead time — than any
passive signal (self-consistency, semantic entropy, log-prob, even Axon's own passive
perturbation-divergence). Actively poking the belief reveals staleness that passive watching
misses.

### Why it is novel (checked)
Counterfactual probing for hallucination exists (arXiv 2508.01862) and belief-injection
frameworks exist (Ask WhAI, MafiaScope). BUT no paper establishes the COMPARATIVE result:
that active counterfactual probing detects a false/stale belief EARLIER than passive
monitoring, specifically under rule shift. The search confirmed this comparison is missing.

### Why it matters / PROBE tie-in
This literally operationalizes the word "probe." It converts PROBE from a passive
contradiction detector into an ACTIVE hypothesis tester and gives a measurable reason to do
so (lead time gained per probe step). Strongest unification of the two papers.

### How to measure
Two conditions on the same rule-shift episodes: (a) passive signals only; (b) allow one
counterfactual probe action per step. Compare lead time and detection AUROC. Report the
lead-time delta and the token cost per probe (cheap-by-design).

### Validates / kills
Validates if the active probe gives a positive lead-time gain over the best passive signal.
Kills if probing adds cost with no earlier detection.

## N2 — The cling curve: confidence-accuracy hysteresis under rule shift

### Claim
After a rule shift, a model's ACCURACY drops immediately but its CONFIDENCE drops later,
producing a measurable lag ("cling time") and a hysteresis loop in (confidence, correctness)
space. Cling time is itself a diagnostic: longer cling = more dangerous confident-wrong
behavior = larger PROBE benefit.

### Why it is novel (checked)
Belief persistence / consistency-adaptability trade-offs are studied (BeliefShift 2026,
"From Confidence to Collapse in Factual Robustness"). BUT framing the accuracy-vs-confidence
LAG as a measurable hysteresis loop with a scalar "cling time," and using it to predict
where a revision loop helps, is not established. Position carefully against BeliefShift
(which benchmarks drift, not the hysteresis/lead-time diagnostic).

### Why it matters / PROBE tie-in
Cling time quantifies EXACTLY the failure PROBE was built to fix ("clinging to a rule after
it changes"). It turns PROBE's motivating anecdote into a measured quantity and predicts the
size of PROBE's win per task.

### How to measure
From per-step rule-shift traces: plot accuracy and confidence vs step around the shift;
measure steps between accuracy-collapse and confidence-collapse; area of the hysteresis
loop. Correlate cling time with PROBE's measured improvement per boss.

### Stage 3 status
Measured on 2026-07-23 using the Stage 2 Llama 3.1 8B traces. Group accuracy collapsed at
step 10 and the first group confidence dip came at step 12, giving a 2 step cling time.
Seed mean cling time was 1.800 steps, 95 percent CI [0.800, 3.000]. Caveat: the confidence
drop was not sustained. Mean agreement was 0.632 pre shift and 0.632 post shift, so this is
a short first-dip lag, not a clean monotone hysteresis curve.

### Validates / kills
Validates if a consistent positive cling time exists and correlates with PROBE benefit.
Kills if confidence tracks accuracy with no lag (no clinging to measure).

## N3 — (optional, ambitious) Detectability boundary of rule shifts
There is a class of rule shifts that NO behavioral monitor can catch early — those where the
new rule agrees with the old on the recent observation stream. Characterize early-detect
lead time as a function of old/new rule OVERLAP; show it degrades predictably to zero. An
honest limit result. Higher risk to prove; keep as a stretch section.

### Novelty note
Behavioral-shift detection and its limits exist generally ("a shift need not hurt
performance"; auditing tests; change-point martingales), but an overlap-parameterized
detectability boundary for LLM rule adaptation, tied to lead time, appears open.

---

# Sharpened aim (2026-07-21) — read this over the earlier C-A

After the second literature sweep, the headline is RE-POINTED. Axon is not "a better
confident-wrong detector" (NCB / cross-model already do that on static tasks). Axon is:

HEADLINE (revised): a LIVE TRIGGER for belief revision. In a task whose rules change
mid-episode, Axon watches perturbation/counterfactual divergence, flags the moment a held
belief goes stale BEFORE it costs reward, and hands that to a revision agent (PROBE) so it
adapts faster. Detection alone is solved for static QA; doing it live and ACTING on it is not.

- The detector itself = a USE of existing signals (NCB-style neighborhood consistency +
  counterfactual probe + cross-model), not a novelty claim.
- Novelty lives in: dynamic setting + closed loop (detect -> revise -> better adaptation) +
  lead time inside an episode + cling time metric (N2).
- Q1 corrected: divergence from SHAKING the input, not plain resampling.

---

# The locked five (2026-08-03, standalone identity)

Decision: Axon stands on its own; PROBE is one application in one section, not the
identity. The paper's one line: "PROBE needed Axon; Axon does not need PROBE." The five
claims below reorganize C-A/C-B/C-C and N1/N2/N3 into the final structure. Same shape as
PROBE's paper: claims 1 to 4 are wins, claim 5 is the honest limit.

1. THE BLIND SPOT. Standard uncertainty tools (semantic entropy, self consistency) catch
   an unsure model and go blind on a confidently wrong one, because a repeated wrong
   answer reads as agreement. We show exactly where and why they fail under rule shift.
   (from C-A; the negative result about the uncertainty literature)

2. THE CLING CURVE. After a rule shift, accuracy drops immediately but confidence lags;
   the gap is a measurable per model scalar (cling time), reported across models and
   tasks. Turns "stubbornness" into a number. (from N2; the named phenomenon.
   STATUS 2026-08-20: MEASURED at n=30 per overlap level, and it does not stand as an
   independent claim. Accuracy falls 0.721 -> 0.208 at the full shift while agreement moves
   0.638 -> 0.602, a change of -0.037. The group confidence curve is CENSORED at every
   overlap level: mean agreement never reaches 0.5, bottoming at 0.540 / 0.567 / 0.613.
   Confidence does not lag the collapse, it never arrives inside the window.
   The per episode scalar exists -- 3.10 steps [2.21, 4.03] at the full shift, against the
   n=5 pilot's 1.8, which underestimated it -- but it times the first transient single
   episode dip below 0.5, not a sustained collapse, and it does not vary with shift size
   (3.10 / 2.56 / 3.48, non monotone, intervals fully overlapping). Calling that a per model
   scalar oversells it.
   Placement: claim 2 folds into claim 1 as its visualisation and its number. Two lines, one
   collapsing and one flat, is the clearest single picture of the blind spot in the project.
   One fewer headline claim, a stronger claim 1.)

3. ASKING BEATS WATCHING. One active counterfactual probe ("would the old belief still
   predict this?") detects the confident wrong crossing earlier than any passive signal.
   The active vs passive comparison is confirmed missing from the literature. (from N1;
   was the method headline.
   STATUS 2026-08-20: FALSIFIED, and replaced by claim 3'. The oracle confound fix
   (2026-08-05) left this unresolved at n=25. The overlap sweep raised n to ~240 per
   condition and settled it the other way. Decomposing axon_probe into its two factors:

     signal                      overlap 0            overlap 1            overlap 2
     axon_probe (gate x probe)   0.769 [.712,.819]    0.500 [.430,.568]    0.376 [.309,.447]
     bare gate (chosen==old)     0.775 [.718,.827]    0.515 [.452,.577]    0.364 [.302,.428]
     probe alone (change_score)  0.453 [.366,.539]    0.495 [.426,.563]    0.493 [.423,.563]

   The probe question sits at chance at EVERY overlap level, and the bare gate matches or
   beats the full detector everywhere. The model cannot answer "has the rule changed?"
   about its own belief. Asking does not beat watching; asking contributes nothing, and
   the API calls spent on it are waste. This is a clean negative result about LLM
   self-report, and it is worth reporting as one.)

3'. WATCHING IS ENOUGH, AND IT IS FREE. The whole detector is one deterministic check:
   is the agent still answering the key its OWN past answers say it believes? At the full
   shift that separates confident wrong rows at AUROC 0.775 [0.718, 0.827] (n=236) with
   zero model calls, against 0.40 for self consistency and semantic entropy. It also
   explains why cling_timing was always the one baseline axon_probe could not beat
   (+0.087 [-0.011, 0.184]): cling timing is a crude proxy for the same gate. Replaces
   claim 3 as the method headline, and it is a stronger claim, because the detector is
   now free rather than one extra model call per step.

4. EARLY WARNING WITH LEAD TIME. The signal fires BEFORE the post shift accuracy
   collapse, with measurable lead time; prior early warning work is static task only.
   (from C-B.
   STATUS 2026-08-20: MEASURED, and it survives only for G0 and only at the full shift.
   Lead is defined as cross cue transfer -- a per cue lead cannot be positive, since the
   gate is evaluated on the same answer whose wrongness defines the failure. At overlap 0,
   G0 gives mean lead +0.91 steps [+0.43, +1.39], interval clear of zero, so the warning
   genuinely precedes the failure of cues that have not failed yet. G1 is structurally
   negative everywhere (-0.25, -0.51, -0.27) because it cannot fire until something has
   already been missed.
   The trap: G0's mean lead GROWS with overlap (+0.91, +1.76, +1.77), which read alone
   says early warning improves exactly where AUROC inverts. It does not. G0 buys that lead
   by firing on 95 percent of cues that never fail (false alarm 0.950 and 0.947 at overlap
   1 and 2, against G1's 0.050 and 0.053). Mean lead is uninterpretable without the false
   alarm rate beside it, and both must be reported together.
   C-B therefore lands as a precision versus earliness frontier, not a single number:
   G0 warns early and cries wolf, G1 never warns early and almost never does.)

5. THE DETECTABILITY LIMIT. When the new rule agrees with the old on everything observed
   so far, no detector can fire early; we characterize lead time against old/new rule
   overlap. An honest boundary result. (from N3.
   STATUS 2026-08-20: MEASURED, and the boundary is sharper than "it degrades". AUROC by
   number of cues that keep their pre shift key: 0 unchanged 0.775, 1 unchanged 0.515,
   2 unchanged 0.364. It does not decay to chance, it decays THROUGH chance and inverts.
   Mechanism, confirmed in the traces: the gate fires on "still answering the old belief",
   and once most cues keep their key, still answering the old belief is the CORRECT move.
   P(chosen==believed_old) on wrong vs right rows goes 0.652/0.102 at overlap 0, to
   0.662/0.632 at overlap 1, to 0.465/0.738 at overlap 2 -- separation, then none, then
   reversed. So the detector is not merely blind to small shifts, it is confidently
   backwards on them, which is the same failure it was built to catch. Any deployed
   version needs a per cue gate rather than one episode wide gate.
   UPDATE 2026-08-20, later same day: "needs a per cue gate" was wrong -- the gate is
   already per cue. The real defect is that it fires on CONSISTENCY WITH OWN BELIEF, and
   consistency is only dangerous once that belief has been contradicted. Fixing that gives
   G1, which is flat at 0.75 across every overlap level and never inverts.
   But G1 does not replace G0, it trades against it: G0 is 0.776 at the full shift and
   inverts at high overlap; G1 is 0.59 at the full shift and holds at 0.75 elsewhere. G0
   warns early (+0.91 lead) and cries wolf (0.95 false alarm once the shift is partial);
   G1 never warns early (negative lead by construction) and almost never cries wolf (0.05).
   Six selector variants were tried to pick between them at runtime -- contradiction
   density raw and confirmed, thresholds 2 and 3, and two blends. All failed. The reason is
   structural, not tuning: the selector needs to know whether ALL cues shifted, and that
   evidence accumulates strictly more slowly than the decision it informs.
   So claim 5 now carries two limits, not one: a detectability limit in overlap, AND a
   precision versus earliness frontier with no runtime rule to sit on it. Both measured,
   both honest, and the second is the more interesting of the two because it says a free
   detector exists but choosing the right one requires information the agent cannot have
   in time.)

Supporting, not headline: cross scale replication (C-C, two or three model sizes) and the
applications section, where detector consumers are demonstrated: refresh retrieval, hand
off to a human, and trigger PROBE's belief revision. Testbeds: Axon's own rule shift
environment first, a fact update QA stream second, PROBE's bench adaptation third as
borrowed hardware.

---

# Why rule shift is non-negotiable to the identity (2026-08-04)

Reaffirmed after re-checking whether "confidently wrong" alone (no shift) could carry the
paper. It cannot. Four reasons:

1. Without a shift, "confidently wrong" is just wrong. A model wrong from the start is
   ordinary error detection — already published (AUROC ~0.80 on static tasks, per the
   novelty sweep). Nothing new to claim.
2. The shift is what manufactures the interesting failure. A model that WAS right, whose
   belief then goes stale, keeps answering with full earned confidence. That is the blind
   spot no existing tool catches — and it only exists because something changed underneath
   the model.
3. Three of the five locked claims are literally defined in terms of the shift: the cling
   curve (claim 2) is the lag measured AFTER a change; lead time (claim 4) is measured FROM
   the shift step; the detectability limit (claim 5) is about old-rule/new-rule overlap. No
   shift means no curve, no lead time, no limit — three of five claims collapse.
4. Verification depends on it too: because Axon controls the shift, its exact step is known
   ground truth, and every detection claim (blind spot, lead time, detectability) is checked
   against that known step. Remove the shift and there is no ground truth to check against.
