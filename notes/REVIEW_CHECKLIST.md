# Axon — Consolidated review checklist

Three substantive reviews have been received: 2026-08-24, 2026-08-26, and 2026-08-30.
This checklist keeps their requests visible without treating documentation edits as
completed experiments.

## Claims, framing, and abstract

- [x] State that stale confidence is distinct from ordinary uncertainty.
- [x] Frame the zero-model-call / zero-extra-call nature of G0 and G1 as a central benefit.
- [x] State the negative selector result honestly: no runtime selector robustly chooses
  between G0 and G1 across environments.
- [x] Revise the headline wording: G0 is strong under broad/full shifts but can invert
  below chance under partial shifts; do not describe this only as “weaker.”
- [x] Apply this scoped wording to the actual paper abstract and introduction.
- [x] Treat the 70B full-shift number as a stress-test/upper-bound condition, not the sole
  headline proof; retain the circularity audit and noise explanation.
- [x] Add the full-shift circularity caveat beside the corresponding paper result.

## Problem setup and theory

- [x] Require an early worked RuleShift example, including an unchanged-cue partial-shift
  case that explains G0 inversion.
- [x] Add the worked example to the paper source.
- [x] Downgrade the G1 reaction lower bound from a formal proposition to a Remark.
- [x] Replace the proposition/QED treatment in the paper source.
- [x] Clarify terminology: M3 is raw contradiction velocity; M7 is M3 used as a selector
  between G0 and G1, not an independent raw signal family.
- [x] Make the M3/M7 distinction explicit in the methods text, table, and figure.

## Baselines and experiments

- [x] Keep self-consistency and semantic entropy as mandatory baselines.
- [x] Register the requested simple controls before any new run: elapsed step/time since
  shift, answer novelty/change, and logprob/calibration only when directly exposed.
- [x] Before running those baselines, append the fixed trace subset, window, seeds, and
  score direction to `RESEARCH_LOG.md`.
- [ ] Run the registered trivial-baseline comparison and report the result honestly.
- [ ] Audit logprob availability; report unavailable rather than substituting a post-hoc
  confidence score.
- [x] Record classical concept-drift positioning (Page/CUSUM, DDM, ADWIN) and distinguish
  Axon from generic drift detection.
- [x] Add the concept-drift discussion and citations to the paper's related-work section.

## Results, uncertainty, and sample sizes

- [x] Require every promoted AUROC to include a 95% bootstrap CI, condition-wise `n`, and
  trace source.
- [x] Require inline intervals specifically in the current Tables 6, 7, 8, and 10.
- [ ] Populate those actual paper tables with stored intervals; do not fabricate any.
- [x] Require lead-time tables to display mean-lead CI, false-alarm rate, and denominator.
- [x] Verify the actual lead-time table follows that requirement.
- [x] Define `n` as per listed condition unless explicitly labelled pooled.
- [x] Update every relevant table caption: RuleShift = 240 per overlap condition;
  fact stream = 600 per changed fraction and backbone; external benchmarks = per benchmark
  and shift fraction.
- [x] Check whether close mechanism differences remain distinguishable once CIs are shown;
  write ties as ties when intervals overlap.

## Models, transfer, and limitations

- [x] Record exact backbone identities: Llama 3.2 3B, Llama 3.1 8B, and Llama 3.3 70B,
  with their full model IDs.
- [x] Name those exact models in the paper methods and results tables.
- [x] State that the ladder is within-family transfer, not a clean causal scaling law,
  because checkpoint generations differ.
- [x] Preserve the 3B fact-stream and rare-item boundaries in the limitations section.

## PROBE connection, layout, and proofing

- [x] Move the PROBE tie-in from a standalone results section to a short, self-contained
  Discussion/Future Work application note.
- [x] Apply that move in the paper source; label I3/I6 numbers as imported PROBE evidence,
  not Axon results.
- [x] Plan to move the glossary to an appendix while retaining the necessary notation table
  in the main text.
- [x] Move the glossary in the paper source.
- [x] Record source/render checks for the `70G0` typo and merged Section 6 sentences.
- [x] Compile/render the paper and verify those source-level fixes in the output.
- [x] Normalize the planned Table 2 status categories to `No`, `Conditional`, and
  `No (falsified)`.
- [x] Apply the normalized category labels and explanatory table note in the paper source.

## Final submission gate

- [ ] No new experiment is reported without a prior registration in `RESEARCH_LOG.md`.
- [ ] Every headline number has a source trace, condition-wise `n`, and valid bootstrap CI.
- [ ] Broad-shift success, partial-shift inversion, G0/G1 complementarity, and the failed
  runtime selector are all visible in the abstract, results, and conclusion.
- [ ] Render and proofread the final PDF page by page before submission.

## Third review (2026-08-30)

- [x] Add the Page (1954), Gama et al. (2004), and Bifet--Gavald\`a (2007) bibliography
  entries and cite them from Related Work.
- [ ] Run the complete LaTeX--BibTeX--LaTeX--LaTeX build sequence and verify that the final
  upload has rendered citations rather than literal `(?)` placeholders.
- [ ] Expand the concept-drift comparison: explain that CUSUM/DDM/ADWIN normally consume an
  observed error/change stream, whereas Axon cannot read hidden correctness at runtime.
- [ ] Define precisely what ``registered'' means in the paper: which predictions, trace
  subsets, scoring choices, and thresholds were locked, where the dated record lives, and
  that this is a project research log rather than an external preregistration unless an
  immutable public record is created.
- [ ] Use one primary gate name throughout prose and results (`G_0` cling and `G_1`
  contradiction); reserve M1/M2 for the ablation inventory and add an explicit equivalence
  note there.
- [ ] Add a public, persistent code/data artifact URL before submission, or remove the
  availability claim that implies external access.
- [ ] State in the lead-time discussion that cells with small eligible-pair denominators are
  underpowered and should be read through their wide CIs.
- [ ] Add a multiple-comparisons caveat: the contribution is the preregistered pattern of
  complementarity and failure modes, not significance hunting over isolated cells.
- [ ] State in Limitations that all tested backbones are Llama-family checkpoints and that
  cross-family generalization remains untested.
- [ ] Add one quantitative crossover plot (AUROC vs. changed fraction / overlap for
  `G_0` and `G_1`) from already registered trace results; do not invent or selectively
  smooth data.
- [ ] Trim the abstract after the scientific fixes, retaining problem, zero-call method,
  broad-vs-partial result, and selector boundary.
- [ ] Define Track A and Track B when first mentioned in the introduction or protocol.
