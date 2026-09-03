# Claim 2 — The cling curve

## CLAIM
After a rule shift accuracy drops immediately but confidence lags, and the gap is a
measurable per model scalar (cling time).

## STATUS
FOLDED into claim 1. Not an independent headline.

## VERSION
v0

## CODE
`cling.py`, fed by `analyze.py`

## EVIDENCE
n=30 episodes per overlap level.

  metric                    ov 0     ov 1     ov 2
  pre -> post accuracy      0.721 -> 0.208    0.725 -> 0.396    0.762 -> 0.588
  pre -> post agreement     0.638 -> 0.602    0.641 -> 0.638    0.641 -> 0.654
  agreement change          -0.037   -0.003   +0.013
  group confidence dip      CENSORED CENSORED CENSORED
  min post shift agreement  0.540    0.567    0.613
  episode cling time        3.10 [2.21, 4.03]  2.56 [1.85, 3.33]  3.48 [2.35, 4.65]
  episode censored rate     0.033    0.100    0.233

Traces: `traces/stage4b_overlap/ov{0,1,2}_cling_summary.csv`, `_cling_by_episode.csv`
Plots: `plots/stage4b_ov{0,1,2}_cling.svg`

## REGISTERED
1. Pilot's exactly 0.000 agreement change was an n=5 artifact; predicted small but nonzero
   at n=30. HELD (-0.037).
2. Censored rate materially above the pilot's 0.000. HELD, and harder than registered:
   total censoring at group level.
3. Cling time rises with overlap. FAILED. 3.10 / 2.56 / 3.48, non monotone, intervals
   fully overlapping.
4. Stop gate: censoring above 0.5 means report as censored. NOT TRIGGERED (max 0.233).

## WHY IT FOLDED
Confidence does not lag the collapse, it never arrives inside the window. The per episode
scalar exists but times a transient single episode dip below 0.5, not a sustained collapse,
and it does not vary with shift size — which is exactly what a real per model scalar should
do. Calling it "a measurable per model scalar" oversells what was measured.

Kept as claim 1's figure and number: two lines, one collapsing, one flat.

## KILLS IT / REVIVES IT
A model whose confidence DOES collapse after a shift would revive this as its own claim,
and would make cling time a genuine cross model discriminator. That is a cross scale
question, so this claim is worth re-opening at Stage 5 rather than closing for good.

## OPEN
- Re-test at cross scale. A larger model may actually break confidence, which would revive
  the claim.


## CROSS SCALE UPDATE (2026-08-20)

Confirmed at 3B, 8B and 70B: group confidence never reaches 0.5 at any scale (minimum
0.507 / 0.540 / 0.747), and agreement change stays inside 0.1 of zero everywhere (worst
-0.048). Confidence does not break after a rule shift at any scale tested. Claim 2 stays
FOLDED; the revival condition (a bigger model whose confidence does collapse) did not fire.

The 70B row is the best version of claim 1's figure in the project:
accuracy 1.000 -> 0.571, agreement 0.855 -> 0.807. A model that had the rule perfectly
becomes wrong on nearly half the steps and reports essentially unchanged confidence.

STOP GATE TRIGGERED at 70B. Censoring is 0.533 / 0.733 / 0.867, all above the registered
0.5, so 70B cling time is reported as CENSORED. Do not quote 4.07 / 4.88 / 1.75 as scalars;
they are means over the minority of episodes that dipped, and the 1.75 at overlap 2 is a
mean over roughly four episodes.

KNOWN DESIGN FAULT, to fix in the next registered run: the dip threshold is a fixed 0.5 but
baseline agreement scales with the model (0.578 / 0.638 / 0.855), so a 70B model must fall
much further to trip it. That is most of why its censoring is so high. The honest version is
a threshold relative to each model's own pre shift agreement. Not changed retroactively --
registering it first, then running it, with the fixed threshold numbers reported alongside.

## RELATIVE THRESHOLD RETEST (2026-08-23)

Using 0.8 times each episode's own pre-shift agreement reduces 70B censoring on RuleShift
from 0.600/0.800/0.867 to 0.200/0.233/0.367 across overlaps, and fact-stream censoring
from 0.033 to 0. The confidence curve still does not collapse, so Claim 2 remains folded
into Claim 1. Fixed-threshold results remain reported alongside this corrected analysis.
