# Axon versions

A version is cut when a claim's status changes on evidence, not on a date. v1 is the version
that goes in the paper, and it cannot be cut until every VALIDATED claim has survived on more
than one model AND more than one environment.

## v0 — 2026-08-20 (superseded)
Detector: deterministic gate over the agent's own trace, zero model calls.
Backbone: meta-llama/llama-3.1-8b-instruct only.
Environment: RuleShift only (three cues, shift at step 10).

Claims: 1 VALIDATED, 2 FOLDED, 3 FALSIFIED, 3' VALIDATED, 4 MEASURED, 5 MEASURED.
All statuses PROVISIONAL — one model, one environment.

## v0.1 — 2026-08-20, DONE: cross scale
Full overlap sweep on 3B, 8B and 70B (`meta-llama/llama-3.2-3b-instruct` /
`meta-llama/llama-3.1-8b-instruct` / `meta-llama/llama-3.3-70b-instruct`; Llama 3.2 3B /
Llama 3.1 8B / Llama 3.3 70B). The
checkpoints are from the same broad Llama family, but their generation labels differ, so
this is a within-family capacity comparison rather than a perfectly controlled scaling law.
90 episodes per model.

The gate IMPROVES with scale: 0.743 / 0.776 / 0.976 at overlap 0, while self consistency
stays at chance (0.492 at 70B). The blind spot widens rather than closing.

Also settled here:
- claim 3 is SCALE DEPENDENT with the sign inverted (70B probe 0.227 raw, 0.773 reversed)
- claim 2 stays folded; confidence never breaks at any scale
- claim 5's limit 2 was said to shrink to a small backbone artifact here, since G0 stops
  inverting at 70B on RuleShift. THIS NARROWING WAS RETRACTED in v0.2 (below) once external
  benchmarks showed G0 at chance at 70B too, on a comparable partial shift.

## v0.2 — 2026-08-20 to 2026-08-22, DONE: second environment and three external benchmarks (CURRENT)

### Second environment: the fact stream
12 entities, 6 answers, zipf arrival, natural language items. Shares nothing with RuleShift
but the CSV schema, so every scorer ran against it unchanged.

Gate 0.805 [0.777, 0.834] at 70B against 0.472 / 0.474 for the uncertainty baselines. The
kill condition did NOT fire: Axon is a method, not a RuleShift case study. Claims 1 and 3'
promoted from provisional to validated across three model sizes and two environments.

Measured limit: the gate is only as good as the belief it reads. Items seen 0-1 times score
exactly 0.500, items seen 5+ times score 0.899.

### External benchmarks: TruthfulQA, TreeCut, HotpotQA
First independent content the project has touched. Two tracks per benchmark: Track A is the
benchmark UNMODIFIED (one shot, no repeats, no feedback — gate reported N/A, never faked).
Track B is a MODIFIED repeated item stream built from the same questions/answers, with reward
feedback and a rule flip, labelled modified everywhere.

Track A (premise of claim 1, on independent data, all at 70B):
  TruthfulQA   baselines 0.566 [0.495, 0.642]   — weakly informative
  TreeCut      baselines 0.445 [0.375, 0.514]   — at chance
  HotpotQA     degenerate at first pass (constructed distractor too easy, 1/200 wrong);
               yes/no restricted re-run also underpowered (9/200 wrong) — not reported

Track B, FIRST PASS at changed_frac=1.0 (full shift, matched to the synthetic environments):
  TruthfulQA   G0 0.628 [0.545, 0.723]   G1 0.186 [0.135, 0.251]   baselines 0.347 (below chance)
  TreeCut      underpowered at n=300 (8 right / 292 wrong) — point estimate only, not reported
  HotpotQA     degenerate (299 wrong / 1 right) — not reported, distractor too easy

A mid run at changed_frac=0.5 produced a "pretrained prior" hypothesis (G0 failing on content
the model already knew) which was TESTED AND RETRACTED THE SAME DAY: splitting by pre shift
accuracy showed G0 was WORSE, not better, on items the model had to learn (0.331 vs a
degenerate 0.500 on items it already knew) — the opposite of the hypothesis. The real cause
was a confound: that run used a half shift while RuleShift and the fact stream both used a
full shift.

Track B, CALIBRATED at changed_frac=0.7 (chosen empirically to balance classes; all three
benchmarks land within a few points of 43% post-shift-wrong at this setting), n=300 each:
  TreeCut      G0 0.494 [.468,.521]   G1 0.644 [.610,.678]   baselines 0.504
  HotpotQA     G0 0.524 [.504,.548]   G1 0.633 [.596,.670]   baselines 0.481
  TruthfulQA   G0 0.521 [.493,.551]   G1 0.602 [.557,.646]   baselines 0.505

RESULT: the shift-fraction crossover first found on RuleShift (G0 wins at full shift, G1
wins at partial shift) REPRODUCES on all three independent benchmarks. G0 sits at chance on
all three at a partial shift; G1 clearly beats both G0 and the baselines on all three, no
interval overlap. This is the strongest cross-domain confirmation of claim 5 in the project.

CONSEQUENCE: v0.1's narrowing of limit 2 to "a small backbone artifact" is RETRACTED. These
benchmarks are also 70B, and G0 is still at chance at partial shift there. Scale alone does
not solve the missing-selector problem — confirmed now on five environments total (RuleShift
at 3B/8B/70B, the fact stream, and three external benchmarks), and it remains the single
most load-bearing open problem in the project.

### Deferred by decision, not by failure
PROBE I3/I6 (internal benchmark): NOT RUN. Decision 2026-08-22: internal benchmarks run last,
only once a final gate/selector design is chosen. Running them now against a design known to
be incomplete (no runtime selector) would mean rerunning them again later for no reason.

### Coverage table

  test                          RuleShift      fact stream   TruthfulQA   TreeCut   HotpotQA   PROBE I3/I6
  gate contest (claims 1, 3')   3B,8B,70B      70B           70B          70B       70B        deferred
  cling curve (claim 2)         3B,8B,70B      70B           not run      not run   not run    deferred
  lead time (claim 4)           8B only        not run       not run      not run   not run    deferred
  shift/overlap sweep (claim 5) 3B,8B,70B      not run        0.5,0.7,1.0  0.7,1.0*  0.7,1.0*   deferred

  * TreeCut and HotpotQA's changed_frac=1.0 points were run but are underpowered/degenerate
    and are not reported as results; only the calibrated 0.7 point counts for those two.

Claims 1 and 3' have the widest coverage (three model sizes, five environments). Claim 4 is
the narrowest: one environment, one scale, still a tradeoff rather than a clean win.

## v0.3 — IN PROGRESS: four mechanisms total, two new ones survived
TOP PRIORITY, ahead of the remaining coverage gaps. Confirmed on five environments: G0 wins
at full shift, G1 wins at partial shift, and no free signal tried so far (raw density,
confirmed density, two thresholds, two blends) picks correctly between them. The pretrained
prior explanation was tested and killed; the real variable is SHIFT FRACTION, exactly as
claim 5 already measured on RuleShift.

Axon now has FOUR mechanisms, not two:
  M1  cling (G0)              still answering the item's own believed key
  M2  contradicted (G1)       this exact (item, answer) pair already earned reward 0
  M3  velocity                rate of new contradictions per step, not their count.
                              cannot detect wrongness alone (AUROC 0.40-0.50) but DOES
                              separate shift breadth (0.448 at overlap 0 vs 0.289 at
                              overlap 2 on RuleShift). Used as the selector in M7: G0 if
                              velocity >= 0.35 else G1. Result 0.721 / 0.620 / 0.616 --
                              first selector that never inverts and does not just
                              collapse into one of the two gates.
  M5  soft blend              G0 * G1, no threshold, zero tuned parameters. Also never
                              inverts: 0.634 / 0.682 / 0.637.

DROPPED, with kill conditions triggered as registered:
  M4  cross item consensus    inverts even harder than G0 (0.497 / 0.418 / 0.339)
  M6  agreement drop          chance level (0.485 / 0.515 / 0.576), no better than the
                              uncertainty baselines it was meant to beat

M3/M7 and M5 are real progress but not a solved selector: neither dominates the other, and
neither beats simply picking the correct gate for the true shift fraction. The problem is
downgraded from "every attempt inverts or collapses" to "no attempt dominates."

- test M3/M7 and M5 on the external benchmarks: DONE 2026-08-22, both FAIL to transfer.
  M7's threshold (calibrated on RuleShift) lands at chance (0.507) on TruthfulQA's full
  shift instead of tracking G0's 0.628. M5 collapses to 0.302 (below chance) on the same
  benchmark because it inherits G1's own inversion there rather than cancelling it. The
  "never worst" property found on RuleShift was RuleShift-specific, not a property of
  either mechanism.
- SELECTOR SEARCH CLOSED, final count: 12 variants tried (G4-G9, M4, M6, M8/M9, M5, M7),
  none robust across environments. v0.3's contribution is the four-mechanism inventory and
  the account of why no selector works, not a working selector.

### Fifth mechanism search: CLOSED, per the plan agreed before it started (2026-08-22)
M8 (bimodal split: does the current step's runner-up vote equal the old believed key) was a
genuinely different signal type -- vote SHAPE within one step, not history across steps, the
first mechanism not built from a per-item tally or a rate. It failed on its own terms: it was
predicted to fire more at partial shift and instead fired most at full shift (0.300 vs 0.204
/ 0.250), and its selector (M9) inverts at overlap 2 (0.435), the same failure mode as every
density-based selector.

Per the agreement made before this search started -- try one new signal type, stop if it
fails rather than keep adding mechanisms -- no further mechanism is being designed. Axon's
final mechanism count for v0.3 is FOUR: M1 (cling), M2 (contradicted), M3/M7 (velocity
selector), M5 (soft blend). The missing runtime selector is reported as an open limit, not
solved, after eight attempts (G6, G7, G8, G9, M4, M6, M8, M9) across two search rounds.

## v0.3b — the coverage gaps
Minimum before v1 can be cut:
- claim 4 (lead time) on 3B and 70B for RuleShift, and on the fact stream and externals
- claim 2's relative dip threshold fix, registered before it is run, with the fixed
  threshold numbers reported alongside
- claim 5's overlap sweep on the fact stream
- fact stream at 3B and 8B, so the second environment has the same scale ladder as the first
- PROBE I3/I6, once the selector question above is settled

## v1 — the paper version
Cut only when claims 1, 3' and 4 hold across models and environments. Shape:
1, 3', 4 are the wins. 3 is the negative result. 5 is the honest limit. 2 is claim 1's figure.

## v0.3b progress update — 2026-08-23

The planned coverage work is complete. The four-mechanism ablation, relative cling
threshold, cross-scale/cross-environment lead time, fact-stream overlap sweep, fact-stream
scale ladder, frequency split, and PROBE I3/I6 cross-link are now recorded in the research
log.

The new fact-stream runs refine rather than simplify the story. G0 reproduces strongly at
8B/70B but is near chance at 3B. The shift-fraction crossover reproduces at 70B. M4/M6/M8
remain non-robust globally, but some become informative on the fact stream; they should be
reported as environment-specific signals, not as intrinsically null mechanisms.

v1 is not cut yet. The selector remains unresolved, the 3B fact-stream boundary must be
reported, and the paper needs its first complete draft assembled from the now-closed evidence
record.
