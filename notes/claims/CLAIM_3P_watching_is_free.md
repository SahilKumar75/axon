# Claim 3' — Watching is enough, and it is free

## CLAIM
The whole detector is one deterministic check over the agent's own trace: is the agent still
answering the key its own past answers say it believes? It needs no model calls.

## STATUS
VALIDATED across three model sizes, two synthetic environments and one independent
benchmark. Weaker on independent content (0.628) than on synthetic (0.805, 0.976).
The 2026-08-22 "pretrained prior" scope condition was RETRACTED the same day: it came from a
run configured at a half shift while its comparators ran at a full shift.
Replaces claim 3 as the method headline.

## VERSION
v0

## CODE
`gates.py`

## EVIDENCE
n≈240 per overlap level.

  gate                       ov 0                 ov 1                 ov 2
  G0 cling                   0.776 [.721,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  G1 contradicted            0.592 [.517,.668]    0.748 [.698,.796]    0.746 [.691,.798]
  G3 both                    0.634                0.682                0.637
  G4 either                  0.734                0.580                0.472
  G5 cling after any contra. 0.776                0.517                0.357
  G8 adaptive (confirmed)    0.596                0.748                0.746
  G9 blend                   0.697                0.688                0.671

Against ~0.40 for self consistency and semantic entropy, at zero API cost.

Also explains a long standing anomaly: cling_timing was the one baseline the old probe
never beat (+0.087 [-0.011, 0.184]). It is a crude proxy for the same gate, so it tied
because it was measuring the thing actually doing the work.

Traces: `traces/stage4b_gates.csv`

## THE TWO GATES
- G0 fires on consistency with own belief. Anticipatory, wins at a full shift, INVERTS when
  most cues keep their key (0.364), because there consistency means correct.
- G1 fires on contradiction: has this exact (cue, key) pair already earned reward 0. Flat at
  0.75 across every level, never inverts, but cannot fire until something has been missed.

Neither dominates. See CLAIM_5 for the unsolved selection problem.

## KILLS IT
- The gate failing to beat uncertainty baselines on a larger model.
- The gate needing RuleShift's three cue structure to be definable at all.

## OPEN
- Cross scale.
- A second environment. This is the claim most exposed to "it only works on your toy".


## SECOND TESTBED (2026-08-20) — generalisation confirmed, with a stated limit

On the fact update stream at 70B the gate scores 0.805 [0.777, 0.834] against 0.472 and
0.474 for the uncertainty baselines. The gate definition did not change; only the constant
listing the item set, which is now read off the trace. RuleShift results are byte identical
after that change.

THE LIMIT, measured rather than asserted. The gate is only as good as the belief it reads,
and belief needs observations. Splitting by how many times the item had been seen before:

  rare  0-1 sightings    0.500 [0.500, 0.500]    chance, no signal at all
  mid   2-4 sightings    0.664 [0.608, 0.721]
  freq  5+  sightings    0.899 [0.870, 0.928]    approaching RuleShift's 0.976

A longer observation phase does not fix the rare item case, it only moves more rows into
the frequent bucket. A deployed version needs a per item confidence floor and should refuse
to score items below it rather than emit a coin flip.


## EXTERNAL BENCHMARK (2026-08-22) — first reading RETRACTED, see below

TruthfulQA-stream (MODIFIED: real questions and answer pairs, presented as a repeated item
stream with reward feedback and a rule flip on half the items), 70B, n=300.

  G0 cling        0.476 [0.446, 0.504]     below chance
  G1 contradicted 0.621 [0.575, 0.665]
  unc_agreement   0.503 [0.469, 0.540]
  sem_entropy     0.503 [0.469, 0.540]

This was the registered pass/fail test for v0.2 and G0 failed it.

WHY, and it is a scope condition rather than a bug. Pre shift accuracy is 0.901: the 70B
model already knows these answers, so its belief comes from pretraining, not from anything
it learned in the episode. G0 asks whether the agent is still answering what its own past
answers say it believes; when the belief is a fixed pretrained prior that is true almost
everywhere, so G0 fires on nearly every row and carries no information. Half the items
flipped, so continuing to answer truthfully is right about half the time — hence 0.476.

  G0 requires the belief to have been LEARNED IN CONTEXT.
  Where the belief is a pretrained prior the agent will not revise, G0 has nothing to read.

G1 is grounded in observed reward rather than inferred belief — it only asks whether this
exact (item, answer) pair has already been punished — so it does not care where the belief
came from, and it is the only signal that works on all three environments.

Consequence for the paper: claim 3' must be stated WITH its scope condition, and G1 is
promoted from "the weaker gate" to the general one. The honest headline is that the free
detector works, but which free gate depends on the origin of the belief.


## RETRACTION AND CORRECTED EXTERNAL RESULT (2026-08-22)

The section above was written off a run with changed_frac=0.5 while RuleShift and the fact
stream both used a full shift. TruthfulQA-stream therefore landed on claim 5's already
documented partial shift inversion, and I misread it as a new phenomenon about pretrained
priors. The diagnosis was tested and refuted: splitting by pre shift accuracy, G0 was 0.331
on items the model had to LEARN and a degenerate 0.500 on items it already knew — the
opposite of what the prior story predicts.

Re-run at changed_frac=1.0, matching the other environments:

  G0 cling        0.628 [0.545, 0.723]
  G1 contradicted 0.186 [0.135, 0.251]     inverts in a binary answer space
  unc_agreement   0.347 [0.248, 0.442]     below chance
  sem_entropy     0.347 [0.248, 0.442]     below chance

G0 works on independent content and beats the baselines with no interval overlap. The
pretrained prior scope condition is withdrawn, and so is G1's promotion to "the general
gate" — both were artifacts of the same confounded run.

What survives as an honest caveat: G0 is materially WEAKER on this benchmark (0.628) than on
either synthetic environment (0.805, 0.976), even at a matched shift fraction. The likely
cause is the binary answer space, which makes "still answering the believed key" a coarser
signal than it is over three or six options. Untested, and deliberately not written into the
claim until it is.
