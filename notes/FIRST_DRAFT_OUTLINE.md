# Axon first-draft outline

## Central claim

Standard uncertainty signals can be confidently wrong after a rule shift. Axon is a zero-
model-call trace detector that reads whether the agent is still answering the key its own
history says it believes. G0 is informative under broad shifts, but can become an
anti-signal when many cues remain unchanged; G1 is a later contradiction signal. No single
runtime rule selects the right gate across shift breadth and environments.

## Main contributions

1. Blind spot: agreement and semantic entropy remain confident while accuracy collapses.
2. Free detector: G0 is a deterministic trace gate, validated across RuleShift, the fact
   stream, and independent benchmark content, with a lower-capacity and rare-item boundary.
3. Early warning: G0 fires before later cues fail, but earliness trades against false alarms.
4. Honest limit: G0 wins broad/full shifts, G0 can invert under partial shifts, G1 wins
   some partial-shift conditions, and tested selectors do not robustly choose between them.
5. Negative result: the active self-report probe does not beat passive watching.

## Recommended paper order

1. Introduction: stale confidence after rule change; why ordinary uncertainty fails.
2. Problem and protocol: hidden mappings, reward feedback, rule shift, objective labels.
   Open this section with the concrete `blue -> B`, `red -> C`, `green -> A` example and
   show the first post-shift `red -> C` answer receiving reward 0 while G0 fires and G1 is
   still silent. Then show an unchanged cue to make the partial-shift inversion intuitive.
3. Axon: belief-derived G0, contradiction-derived G1, and zero-call computation.
4. Blind-spot result: accuracy/agreement curves plus standard and trivial baseline contest.
5. Cross-scale and cross-environment validation: RuleShift, fact stream, TruthfulQA,
   TreeCut, HotpotQA.
6. Early-warning frontier: lead time and false alarms together.
7. Mechanism ablation: M1/M2/M3-M7/M5, with M4/M6/M8/M9 as rejected or environment-specific
   candidates, not hidden nulls.
8. Detectability limit: shift-fraction crossover and no robust runtime selector.
9. Discussion/application note: keep the PROBE connection to one self-contained paragraph,
   not a standalone results section. I3 is PROBE's single-factor rule-shift task; its
   existing result is a near tie between baseline and PROBE post-shift accuracy (0.390 vs
   0.393, 50 episodes). I6 is PROBE's mixed/multi-factor shift task; its existing result is
   0.509 baseline versus 0.750 with PROBE (40 episodes). These are imported PROBE results,
   not new Axon experiments. Axon diagnoses the stale-confidence regime; PROBE supplies
   the revision intervention. Put task definitions and provenance in a footnote or
   appendix, then move directly to limitations and future work.
10. Limitations and conclusion: belief formation, 3B fact-stream failure, binary answer
    spaces, and unresolved selector.

## Tables and figures

- Table 1: environments, models, shift fractions, and sample sizes.
- Figure 1: 70B RuleShift accuracy versus agreement around the full shift.
- Table 2: G0/G1/baselines on RuleShift scale ladder and fact stream.
- Figure 2: shift-fraction crossover on RuleShift, fact stream, and external benchmarks.
- Table 3: lead time with false-alarm rates.
- Table 4: four-mechanism ablation.
- Figure 3: fact-stream frequency boundary (rare, mid, frequent).
- Table 5: PROBE I3/I6 cross-paper evidence.

Every AUROC cell in Tables 2 and 4, and every cross-scale/cross-environment AUROC cell,
must be formatted as `point [95% bootstrap CI]` with `n`. The current results tables cited
by the review—Tables 6, 7, 8, and 10—must follow the same rule, even if their final table
numbers change during typesetting. Table 3 must show mean lead with its bootstrap interval
and place the false-alarm rate and denominator directly beside it. The paper must preserve
point-only status for any quantity whose interval was not actually bootstrapped rather than
silently manufacturing precision.

## Abstract wording and baseline requirements from the new review

The abstract must not say unconditionally that Axon “separates confidently-wrong rows.”
Use the scoped result: G0 is strong under broad/full shifts, can fall below chance and
invert under partial shifts, and G1 provides a reactive complement; no selector robustly
chooses between them. This makes the inversion a headline boundary result, not an
oblique “weakening” caveat.

The baseline contest must include, in addition to self-consistency and semantic entropy:

- step index or time since the registered shift;
- a naive answer-novelty/change indicator, defined separately from G0; and
- a token/sequence log-probability or calibration baseline only if the recorded backbone
  interface exposes those values.

These additions are registered in `notes/RESEARCH_LOG.md` before any new run. If logprobs
are unavailable, report an availability check and do not silently substitute a different
confidence measure.

## Sample-size convention for tables

Unless a caption explicitly says “pooled,” `n` means scored rows per listed condition. The
RuleShift count of 240 is per overlap condition, so the three overlap rows represent 240
each, not 240 split across the three. The fact-stream count of 600 is per changed-fraction
and per backbone; the three scale rows therefore represent 600 each, not 600 total. External
benchmark counts are likewise per benchmark and shift fraction. Captions must state both
the per-condition `n` and any derived pooled total, while all primary AUROCs remain
condition-wise.

## Final proofreading and table-normalization checklist

- Correct the Section 11 typo `70G0` to `70B G0`.
- Read the compiled source around every section boundary, especially the transition into
  Section 6, and split any sentences that appear merged by PDF extraction.
- Normalize Table 2's `Detects stale belief?` cells to the categorical values `No`,
  `Conditional`, or `No (falsified)`. Put the reason in a table note rather than mixing
  `yes`, `no`, `selective`, and `falsified in this study` as if they were the same kind of
  label. Proposed mapping: self-consistency = `No`; semantic entropy = `No`; active probe =
  `No (falsified)`; G0 = `Conditional`; G1 = `Conditional`.

## Numbers to cite carefully

- RuleShift 70B full shift: G0 0.976, self-consistency 0.492.
- Fact stream 70B long pre-shift: G0 0.805, baselines about 0.47.
- TruthfulQA full shift fresh: G0 0.676 in the fresh replication; prior matched run 0.628.
- G0 full-shift lead: +1.24 (3B), +0.91 (8B), +1.65 (70B) on RuleShift.
- Fact-stream G0: 0.761 full, 0.466 at 70% changed, 0.367 at 30% changed.
- Rare/frequent fact items at 70B: 0.387 versus 0.866.

## Model-family wording

Name the exact recorded backbones in the methods table: `meta-llama/llama-3.2-3b-instruct`,
`meta-llama/llama-3.1-8b-instruct`, and `meta-llama/llama-3.3-70b-instruct`. Describe the
3B/8B/70B results as a within-family Llama comparison: Llama 3.2 3B, Llama 3.1 8B, and
Llama 3.3 70B. Do not call this a clean scaling law or say that size alone is the causal
variable, because checkpoint generations differ. The supported statement is that the
blind spot and gate behaviour are observed across multiple Llama checkpoints, with a
lower-capacity boundary in the 3B fact-stream condition.

## Mechanism naming and final layout

Define M3 as the raw velocity statistic (new contradictions per step). Define M7 as the
deterministic selector that consumes M3 and chooses between G0 and G1; M7 is therefore
M3-as-selector, not a separate raw signal family. The inventory may retain the compact
label M3/M7, but the methods table and figure must state this relationship explicitly.

Move the accessibility glossary out of the main-text gap between Conclusion and References
and into an appendix or supplementary notation page. Keep the main text's notation table,
which is needed for the equations, but do not insert a second glossary-like block after
the conclusion.

## Must-not-claim

- Do not claim a working runtime selector.
- Do not claim active probing beats watching; Claim 3 is falsified.
- Do not claim M4/M6/M8 are intrinsically useless; they are non-robust and environment
  specific, with positive fact-stream cases.
- Do not quote lead time without false-alarm rate.
- Do not hide the 3B fact-stream failure or the binary-content degradation.

## PROBE cross-paper boundary

The PROBE paragraph must stand alone for a reader who has not seen the companion paper, but
it must not become a second results section. Define I3 as the single-factor rule-shift
benchmark and I6 as the mixed/multi-factor rule-shift benchmark before citing their
results. Label the numbers as existing PROBE evidence, not Axon runs: I3 baseline 0.390
versus PROBE 0.393; I6 baseline 0.509 versus PROBE 0.750. Explain that I3 is an honest near
tie and that the connection is diagnostic-to-intervention, not evidence that Axon itself
improves PROBE accuracy.

## Presentation decisions from review

- Present the current reaction lower-bound Proposition 1 as a **Remark**. Keep the
  information-boundary explanation in the notation section, but do not frame its direct
  definitional proof as a major theoretical proposition or use it to imply a deeper theorem.
- The remark should say only that G1 cannot fire before the first observed zero-reward
  occurrence of the same `(x,a)` pair. The substantive contribution remains empirical:
  detector ranking, lead-time/false-alarm tradeoffs, and the unresolved runtime selector.
- Before camera-ready export, search the source and extracted PDF text for the Section 11
  typo `70G0`; it must read `70B, G0`. This is a source/render verification task, not a new
  result.
