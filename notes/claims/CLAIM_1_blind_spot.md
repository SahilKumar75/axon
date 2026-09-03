# Claim 1 — The blind spot

## CLAIM
Standard uncertainty tools (self consistency, semantic entropy) catch an unsure model and
go blind on a confidently wrong one, because a repeated wrong answer reads as agreement.

## STATUS
VALIDATED across three model sizes and two environments

## VERSION
v0

## CODE
`contest.py` (the head to head), `analyze.py` (metrics), `cling.py` (the two line picture)

## EVIDENCE
Overlap 0, n=236 scored rows in the post shift window, llama 3.1 8b instruct.

  signal                        AUROC [95% CI]
  gate (G0 cling)               0.776 [0.721, 0.827]
  uncertainty_agreement         ~0.40
  semantic_entropy              ~0.40

Gap over both baselines is roughly +0.37 with the interval clear of zero.

The direct picture, n=30 episodes per level:
accuracy falls 0.721 -> 0.208 after the shift, while agreement moves only 0.638 -> 0.602
(change -0.037). Group agreement never reaches 0.5 at any overlap level, bottoming at
0.540 / 0.567 / 0.613. The confidence line is flat while the accuracy line collapses.

Traces: `traces/stage4b_overlap/ov0_contest.csv`, `ov{0,1,2}_cling_curve.csv`

## FULL-SHIFT CIRCULARITY CHECK (2026-08-24)

The 70B full-shift AUROC must not be read as a surprising result by itself. At overlap 0,
every previously correct key changes, so continued agreement with the historical key is
partly aligned with wrongness by construction. Existing-trace audit values are:

  condition       pre accuracy   pre branch agreement   post accuracy   G0 AUROC
  RuleShift 3B    0.658          0.578                  0.287            0.743
  RuleShift 8B    0.721          0.638                  0.208            0.776
  RuleShift 70B   1.000          0.855                  0.571            0.976

The 70B result is therefore a stress-test/upper-bound condition, not the sole evidence for
the blind spot. Its pre-shift branch agreement is 0.855, so 14.5 percent of branch votes
still disagree despite perfect pre-shift action accuracy. In the scored window G0 fires on
95.1 percent of wrong rows and 0.0 percent of right rows. At 3B and 8B, pre-shift action
noise is larger and G0 remains above chance, at 0.743 and 0.776 respectively.

The claim is consequently supported by the full-shift stress test together with the
partial-shift crossover, the fact-stream replication, and the independent benchmark
replication. The paper should state explicitly that the high 70B full-shift number is
expected under a stable learned key; the contribution is the confident-wrong blind spot
and its measured boundary, not the numerical magnitude alone.

## REGISTERED
- The blind spot must reproduce or the whole premise dies (Stage 1 gate). HELD.
- Survived the oracle confound fix: when the probe stopped reading ground truth, claim 1
  held while claim 3 did not.

## KILLS IT
- Uncertainty baselines matching the gate on a larger model. That would make this a claim
  about 8B models, not about LLMs.
- The blind spot failing to appear outside a hand built rule shift.

## OPEN
- Cross scale: 2 to 3 model sizes.
- A second environment. Every number above is RuleShift only.


## SECOND TESTBED (2026-08-20) — generalisation confirmed

Fact update stream: 12 entities, 6 answers, zipf arrival, natural language items, 70B,
n=300. Shares nothing with RuleShift but the CSV schema.

  G0 gate         0.805 [0.777, 0.834]
  unc_agreement   0.472 [0.366, 0.574]    chance
  sem_entropy     0.474 [0.367, 0.576]    chance

The blind spot reproduces in a second environment and at a second scale. Claim 1 is no
longer provisional on environment or on model size.

## FACT-STREAM SCALE BOUNDARY (2026-08-23)

The second environment was extended to 3B and 8B. G0 scored 0.498 at 3B, 0.786 at 8B,
and 0.761 at 70B under the full shift. The blind spot therefore reproduces cleanly at 8B
and 70B, while 3B is a lower-capacity boundary where the model does not form a reliable
enough belief for the gate to read.

On the fact stream, G0 is strongly frequency dependent: at 70B it scores 0.387 on items
seen 0-1 times before the shift and 0.866 on items seen 5+ times. This is a deployment
constraint, not a hidden success: the detector is only as good as the belief it reads.

## CI PRESENTATION REQUIREMENT

The abstract and headline claim must be scoped by shift breadth. G0 is strong under broad
or full shifts, but can fall below chance and invert under partial shifts; the paper must
not summarize this as merely “weaker” performance. Every promoted AUROC must appear with
its point estimate, 95% bootstrap CI, condition-wise `n`, and trace source in the relevant
results table.

The final results tables must show the stored bootstrap interval beside every AUROC point,
including the cross-scale and cross-environment rows. The source files are
`traces/ablation_ruleshift.csv`, `traces/ablation_external.csv`,
`traces/factstream_overlap_results.csv`, and `traces/factstream_scale_results.csv`.
The compact claim summary above is not a substitute for those intervals.
