# Claim 5 — The detectability limit

## CLAIM
When the new rule agrees with the old on much of what is observed, no detector can fire
early. An honest boundary result.

## STATUS
MEASURED. Carries TWO limits. Limit 2 NARROWED at cross scale (2026-08-20): it is a small
backbone limit, not a general one.

## VERSION
v0

## CODE
`overlap.py` (generates the conditions), `overlap_summary.py`, `gates.py`

## LIMIT 1 — decay through chance, and inversion
AUROC by number of cues keeping their pre shift key:

  overlap 0 (all shift)      0.775 [0.718, 0.827]
  overlap 1 (one unchanged)  0.515 [0.452, 0.577]
  overlap 2 (two unchanged)  0.364 [0.302, 0.428]

It does not decay TO chance, it decays THROUGH chance and inverts.

Mechanism, confirmed in the traces. P(chosen == believed_old) on wrong vs right rows:
  overlap 0   0.652 / 0.102   separated
  overlap 1   0.662 / 0.632   none
  overlap 2   0.465 / 0.738   reversed

Once most cues keep their key, still answering the old belief is the CORRECT move, so the
gate anti correlates with wrongness. The detector is not blind to small shifts, it is
confidently backwards on them — the same failure it exists to catch.

## LIMIT 2 — no runtime rule selects between the two gates
G0 wins at a full shift and inverts at high overlap. G1 is flat at 0.75 and never inverts
but is weak at a full shift and never warns early. Six selector variants were tried:

  raw contradiction density, threshold 2       0.755 / 0.518 / 0.358   inverts
  raw contradiction density, threshold 3       0.673 / 0.627 / 0.654   dominated everywhere
  raw density blend                            0.782 / 0.582 / 0.453   inverts
  confirmed density, threshold 3 (registered)  0.596 / 0.748 / 0.746   collapses to G1
  confirmed density blend                      0.697 / 0.688 / 0.671   dominated
  confirmed density, threshold 2 (POST HOC)    0.655 / 0.655 / 0.746   dominated

Raw density barely separates the levels (mean 2.54 / 2.32 / 2.11) because it counts "cue
answered wrong", not "cue's rule changed", and an 8B model gets unchanged cues wrong on its
own. Screening to keys that previously earned reward then failed sharpens it a lot
(1.48 / 1.00 / 0.52) — but still does not fix the outcome.

WHY, and this is structural rather than tuning: the selector needs to know whether ALL cues
shifted, and that evidence accumulates strictly more slowly than the decision it informs.
Confirmed density reaches 3 in only 23 of 240 rows at overlap 0, by which point the window
is nearly spent and G0's early warning is already forfeited. Raise the threshold and the
gate never acts as G0; lower it and overlap 2 selects G0 and inverts again. More seeds will
not fix this.

Traces: `traces/stage4b_gates.csv`, `stage4b_overlap_summary.csv`

## REGISTERED
Density selector, run 2026-08-20:
- Precondition (raw density separates the levels): PARTIAL FAIL, direction right, magnitude
  far too weak.
- Never worse than ~0.05 off the best gate: FAILED for every variant.
- False alarm below 0.20 at overlap 1/2: FAILED (0.350, 0.237).
- Adaptive lead positive but below G0's: FAILED, went negative (-0.12).
Confirmed density refinement:
- Precondition (sharper separation): HELD.
- Within 0.05 of best gate at every level: FAILED.

## KILLS IT / SOLVES IT
A selector that works would move limit 2 from "honest limit" to "adaptive detector" and is
the single biggest available upgrade to the paper. It would have to use information that
arrives FASTER than confirmed density. Untried idea: the rate of change of contradictions
rather than their count.

## OPEN
- One more selector idea before declaring limit 2 final.
- Cross scale: a more accurate model would pollute raw density less, so density might
  separate better on a bigger backbone. Worth re-testing there before closing.


## CROSS SCALE UPDATE (2026-08-20)

Limit 1, the inversion, is scale sensitive. G0 at overlap 2: 3B 0.342, 8B 0.364, 70B 0.592.
It inverts on small backbones and stops inverting at 70B, where post shift accuracy at
overlap 2 reaches 0.850 and there is far less clinging to invert on.

Limit 2 does not survive as a general claim. At 70B, G0 is 0.976 / 0.753 / 0.592 and
dominates G1 at every level, so there is nothing to select between. Re-running all six
selectors at 70B: every one is WORSE than plain G0, and the blends invert at overlap 2
(0.333).

The selectors also failed at 70B as the exact mirror of their 8B failure. Raw density at
70B is 1.91 / 1.34 / 0.67, so a threshold of 3 is never met and everything falls through to
G1; at 8B density was inflated by ordinary error and the same threshold picked G0 too often.
The threshold tracks the model's error rate, which makes contradiction density a tuned
constant rather than the principled trigger it was proposed as.

Restated limit 2: on small backbones G0 inverts, G1 is needed to cover it, and no free
runtime signal picks between them. At scale the problem does not arise. "No adaptive rule
exists" and "no adaptive rule is needed at scale" are different claims, and only the second
is supported once 70B is in the table.


## EXTERNAL BENCHMARK CONFIRMATION (2026-08-22)

The shift fraction mechanism reproduces on three independent benchmarks (TreeCut, HotpotQA
yes/no, TruthfulQA), all at changed_frac=0.7, 70B, n=300, balanced classes:

  benchmark         G0 cling              G1 contradicted        baselines
  TreeCut           0.494 [.468,.521]     0.644 [.610,.678]      0.504
  HotpotQA          0.524 [.504,.548]     0.633 [.596,.670]      0.481
  TruthfulQA        0.521 [.493,.551]     0.602 [.557,.646]      0.505

G0 sits at chance on all three; G1 beats baselines on all three, no interval overlap. This
matches RuleShift's ov1 (G0 0.515 at 8B) almost exactly, and confirms the crossover found
on RuleShift is a property of shift fraction generally, not a RuleShift artifact.

## LIMIT 2, RESTATED AGAIN

The 2026-08-20 cross scale update said G0 stops inverting at 70B on RuleShift and narrowed
limit 2 to "a small backbone artifact." That narrowing does NOT survive contact with these
three benchmarks: they are also 70B, and G0 sits at chance there, not above it. So scale
alone does not dissolve the problem -- RuleShift's own overlap structure (only one of three
cues shifts at its highest overlap level) was doing some of the work, and it does not
transfer to real content at a comparable partial shift fraction.

Current honest position: no runtime rule selects between G0 and G1, on any model size tested
so far, once real content is included. This is now confirmed on five environments (RuleShift
at 3B/8B/70B, the fact stream, and three external benchmarks) and is the most load bearing
open problem in the project.

## FACT-STREAM OVERLAP AND SCALE UPDATE (2026-08-23)

The shift-fraction crossover reproduces on the fact stream at 70B:

  changed fraction       G0       G1
  1.0                    0.761    0.505
  0.7                    0.466    0.636
  0.3                    0.367    0.665

The scale ladder is not uniform: G0 is 0.498 at 3B, 0.786 at 8B, and 0.761 at 70B under
the full shift. This establishes a lower-capacity boundary in the second environment while
preserving the crossover at 70B.

The new runs also show that M4, M6, and M8 are not intrinsically null: M4 reaches 0.572 at
3B full shift, M6 reaches 0.619 at 70B full shift and 0.638/0.672 at partial shifts, and
M8 reaches 0.549 at the 30% fact-stream shift. They remain non-robust across environments
and scales, so the robust mechanism inventory stays at four; the paper should describe the
dropped mechanisms as environment-specific candidates rather than universally useless.


## NEW MECHANISMS M3-M7 (2026-08-22)

Terminology lock: M3 is the raw new-contradiction velocity statistic. M7 is the
deterministic selector built from that statistic to choose G0 versus G1, so M7 is
M3-as-selector rather than an independent raw mechanism family. Report the pair as M3/M7
only when this distinction is explicit.

Four new mechanisms tested against the missing-selector problem: M3 velocity (rate of new
contradictions), M4 cross-item consensus, M5 soft blend (G0*G1, no threshold), M6 agreement
drop. M4 and M6 killed per registered kill conditions (M4 inverts harder than G0; M6 is
chance-level, comparable to the uncertainty baselines it should beat).

M3 cannot detect wrongness on its own (AUROC 0.40-0.50) but DOES separate shift breadth
(mean velocity 0.448 at overlap 0 vs 0.289 at overlap 2), so it was turned into a selector:
M7 = G0 if velocity >= 0.35 else G1. Result: 0.721 / 0.620 / 0.616 -- the first selector that
never inverts and is not just G1 wearing a disguise (unlike G8, which rarely crosses its
threshold and defaults to G1 almost everywhere at 8B).

M5 (plain product, zero tuned parameters) is the other non-inverting candidate: 0.634 / 0.682
/ 0.637.

Neither dominates: M7 is closer to G0 at full shift, M5 is closer to G1 at partial shift.
Both beat every prior selector's WORST-CASE behavior (no inversion, no full collapse to one
gate) without beating picking the correct gate for the situation. Carried forward to the
external benchmarks as the two live candidates; the missing-selector problem is downgraded
from "every attempt inverts or collapses" to "no attempt dominates," which is real but
partial progress.


## M8/M9, FIFTH MECHANISM: FAILED, SEARCH CLOSED (2026-08-22)

M8 (does the current step's runner-up vote equal the old believed key -- vote shape, not
history) was tested as the one additional genuinely-new signal type agreed on after M3-M6.
It failed on its own predictions: fires MOST at full shift (0.300) rather than at partial
shift (0.204/0.250) as designed to. Its selector M9 inverts at overlap 2 (0.435 < 0.5), the
same failure as every density-based selector before it.

Per the plan agreed before this test ran, the search stops here rather than continuing to
add mechanisms. FINAL STATE: no runtime selector found after eight attempts (G6, G7, G8, G9,
M4, M6, M8, M9). M3/M7 and M5 remain the two live non-inverting candidates, and neither
dominates. This is Axon's final honest limit for v0.3 unless a fundamentally different
approach (not another per-item or per-step statistic) is found later.


## M5 AND M7 TESTED ON EXTERNAL BENCHMARKS (2026-08-22) — neither transfers

  benchmark            G0        G1        M5 blend   M7 velocity
  TruthfulQA f=1.0     0.628     0.186     0.302      0.507
  TruthfulQA f=0.7     0.521     0.602     0.623      0.559
  TreeCut    f=0.7     0.494     0.644     0.641      0.561
  HotpotQA   f=0.7     0.524     0.633     0.651      0.579

M7 (velocity selector, threshold calibrated on RuleShift) does not transfer: on TruthfulQA
at full shift it lands at 0.507, indistinguishable from chance, instead of tracking toward
G0's 0.628. The threshold is tuned to RuleShift's own velocity scale and does not carry over
to different item pool sizes and step structures.

M5 (soft blend, G0*G1) holds its "never inverts" property at partial shift on all three
benchmarks (0.62-0.65), but COLLAPSES at TruthfulQA's full shift (0.302, well below chance)
because it inherits G1's own inversion there (0.186) rather than cancelling it. The RuleShift
finding that M5 never inverts was specific to RuleShift, where G1 never dropped that low.

## FINAL STATE FOR v0.3

Twelve selector/combination variants tested across three search rounds (G4-G9, M4, M6,
M8/M9, M5, M7). None is robust across environments. The search is closed per the standing
agreement (try new signal types, stop when they fail rather than keep adding). v0.3's honest
contribution is the mechanism inventory (M1, M2, M3, M5) and a clear account of why no
selector has worked: it needs to know the shift's breadth, and that information is not
available in time from anything tried so far, on any environment tested.
