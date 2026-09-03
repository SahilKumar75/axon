# Claim 3 — Asking beats watching

## CLAIM
One active counterfactual probe ("would the old belief still predict this?") detects the
confident wrong crossing earlier than any passive signal.

## STATUS
FALSIFIED. Reported as a negative result about LLM self report, not dropped.

## VERSION
v0

## CODE
`probe.py` (builds and issues the probe), `contest.py` (scores it)

## EVIDENCE
Decomposing the detector into its two factors. `stale_score = change_score * [chosen==old]`,
so it is a probe question gated by a staleness check. Scored separately, n≈240 per level:

  signal                      ov 0                 ov 1                 ov 2
  axon_probe (gate x probe)   0.769 [.712,.819]    0.500 [.430,.568]    0.376 [.309,.447]
  bare gate (chosen==old)     0.775 [.718,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  probe alone (change_score)  0.453 [.366,.539]    0.495 [.426,.563]    0.493 [.423,.563]

The probe question is at chance at EVERY overlap level. The bare gate matches or beats the
full detector everywhere. Mean change_score on wrong vs right rows at overlap 0 is 0.542 vs
0.578 — the probe answers the same way whether the model is right or wrong.

Traces: `traces/stage4b_overlap/ov{0,1,2}_probe.csv`, `_contest.csv`

## HISTORY
- Originally measured at 0.950 AUROC. That was the ORACLE CONFOUND: probe prompts hardcoded
  the environment's true pre shift rule, so the probe scored agreement with ground truth the
  experimenter injected, not staleness of the model's own belief.
- Fixed 2026-08-05: `believed_rule()` infers the model's own held key per cue from the mode
  of its own past answers, using only strictly earlier rows. Corrected number: 0.785
  [0.583, 0.929] at n=25, which left the claim UNRESOLVED, tied with every baseline.
- Settled 2026-08-20 at n≈240: falsified.

## WHAT IT MEANS
The model cannot report on whether its own rule belief has gone stale. Every API call spent
on the probe is waste. This is the paper's negative result and it is worth stating plainly:
self report does not work for this, and the free passive signal does.

## KILLS IT / REVIVES IT
A larger model might be able to answer the question about itself. If a frontier model's
probe rises clearly above chance, the claim becomes scale dependent rather than false, which
is a more interesting result than either. Worth one frontier spot check.

## OPEN
- One frontier spot check before writing this up as flatly false.
