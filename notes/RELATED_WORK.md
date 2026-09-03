# Axon — Related Work and Where Axon Is Still Novel

Survey done Session 001 (2026-07-21). The area is active as of mid-2026, so the
contribution has to be narrow. This file records what is already claimed and stakes out
the gap.

## Directly overlapping — read these first

- Limited Reasoning Space: The cage of long-horizon reasoning in LLMs.
  Argues every model has an intrinsic upper bound on effective reasoning horizon; past it
  accuracy collapses suddenly and noise is amplified into hallucination. This is our
  Yggdrasil-tangle point, already formalised. https://arxiv.org/html/2602.19281v2

- The Reasoning Trap: How Enhancing LLM Reasoning Amplifies Tool Hallucination.
  Deeper reasoning can CAUSE more hallucination. Directly counters "more thinking is
  better." https://arxiv.org/abs/2510.22977

- seqBench: A Tunable Benchmark to Quantify Sequential Reasoning Limits of LLMs.
  A tunable benchmark built to find where sequential reasoning breaks. Strong candidate
  for our ground-truth task family (Q2). https://arxiv.org/pdf/2509.16866

- TreeCut: A Synthetic Unanswerable Math Word Problem Dataset for LLM Hallucination
  Evaluation. Unanswerable-by-construction problems, so a confident answer = hallucination
  objectively. Second candidate task family. https://arxiv.org/pdf/2502.13442

- LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and
  Directions. Taxonomy background. https://arxiv.org/pdf/2509.18970

## The branching machinery (tool, not contribution)

- Tree-of-Thoughts and Demystifying Chains, Trees, and Graphs of Thoughts.
  Branching reasoning is a standard, well-studied tool. We USE it; we do not claim it.
  https://arxiv.org/html/2401.14295v3

## What is already known (so DO NOT claim it)

- Reasoning accuracy collapses past a model-specific complexity (sharp, near-exponential
  decay). Known.
- Deeper chains do not always help and can introduce new hallucinations. Known.
- Collapse has recurring failure modes (incoherence, hallucination spirals, repetition,
  topic drift, degenerate loops); occurs in ~50-83% of wrong answers and rises with
  difficulty. Known.

## Where Axon is still open (the contribution)

1. Branch STRUCTURE at the break point. Existing work measures chain LENGTH / depth.
   Almost nobody studies the tree's SHAPE (width, reconvergence rate, divergence) right at
   the collapse. Open.
2. EARLY prediction. Existing work characterises collapse AFTER it happens. A structural
   divergence signal that predicts collapse a few steps EARLY is not established. Open,
   and it is the trigger PROBE's contradiction detector wants.
3. CROSS-SCALE boundary map with a stable failure signature. Show the threshold moves with
   model capacity while the failure mode stays the same. Under-explored.

## Honest risk

The phenomenon is crowded. If Stage 3 finds that structural divergence only appears at the
same time as the accuracy collapse (no early signal), the novel claim weakens to "another
way to see a known collapse." Mitigation: pre-register the early-warning test (predict N
steps before) so a positive result is unambiguous.

## Sources

- https://arxiv.org/html/2602.19281v2
- https://arxiv.org/abs/2510.22977
- https://arxiv.org/pdf/2509.16866
- https://arxiv.org/pdf/2502.13442
- https://arxiv.org/html/2401.14295v3
- https://arxiv.org/pdf/2509.18970

---

# Closest competitors found in the second sweep (2026-07-21) — READ THESE

The perturbation/neighborhood idea is largely PUBLISHED on static tasks. Do not claim it as
new; use it as a tool and differentiate on the dynamic + closed-loop setting.

- Illusions of Confidence? Neighborhood Consistency (NCB), Jan 2026: facts with "perfect
  self-consistency collapse under mild interference"; measures belief across a conceptual
  neighborhood. This is basically our perturbation detector, on static facts.
  https://arxiv.org/abs/2601.05905
- When Agents Disagree With Themselves (Feb 2026): behavioral consistency as an uncertainty
  signal for LLM AGENTS. Closest agent-side neighbor. https://arxiv.org/html/2602.11619v2
- Cross-Model Disagreement for Uncertainty (2026): cross-model disagreement flags confidently
  wrong where self-consistency (aleatoric) misses. https://arxiv.org/html/2604.17112
- Flip-Flop Consistency (robustness to prompt perturbations). https://arxiv.org/pdf/2510.14242
- Counterfactual Debating with Preset Stances (hallucination). https://arxiv.org/pdf/2406.11514

## What this means for Axon's novelty
- CROWDED (use, don't claim): perturbation/neighborhood consistency, cross-model disagreement,
  counterfactual probing, self-consistency, semantic entropy, internal probes.
- STILL OPEN (claim here): (1) the DYNAMIC / rule-shift, mid-episode setting; (2) CLOSING THE
  LOOP — acting on the early warning to revise a belief and improve adaptation, not just an
  AUROC number; (3) CLING TIME as a new metric.

---

# Concept-drift and sequential change detection — closest methodological neighbors

The paper must position Axon against the classical streaming-detection literature, not only
against LLM uncertainty methods. The closest foundations are:

- Page (1954), *Continuous Inspection Schemes* ([Biometrika, DOI
  10.1093/biomet/41.1-2.100](https://doi.org/10.1093/biomet/41.1-2.100)). Page's cumulative
  monitoring procedure detects a change in an observable sequential process and is the
  classical ancestor of CUSUM-style change detection.
- Gama, Medas, Castillo, and Rodrigues (2004), *Learning with Drift Detection*
  ([SBIA publication page](https://pages.up.pt/~up367273/pub2004.html), [Springer DOI
  10.1007/978-3-540-28645-5_29](https://doi.org/10.1007/978-3-540-28645-5_29)). DDM monitors
  the online error rate and signals when the generating process has changed.
- Bifet and Gavaldà (2007), *Learning from Time-Changing Data with Adaptive Windowing*
  ([SIAM DOI 10.1137/1.9781611972771.42](https://doi.org/10.1137/1.9781611972771.42),
  [author manuscript](https://www.cs.upc.edu/~Gavalda/papers/adwin06.pdf)). ADWIN changes
  the size of an online window when the observed stream changes and provides false-positive
  and false-negative guarantees for its change tests.

These methods are close to M2/G1 and M3/M7 because they use sequential evidence and can
support a change-triggered response. The distinction is the observable target and the
decision being made. Classical drift detectors detect a change in the data-generating
process or in prediction error, usually to support model updating. Axon evaluates whether a
frozen agent's own answer trace has become stale after a hidden rule shift, without reading
the hidden correctness column or asking the model for a self-report. Axon's M2/G1 is a
reward-grounded contradiction signal; M3/M7 is a trace-only velocity statistic used to
choose between two diagnostic gates. Neither is claimed as a new drift detector.

The correct novelty boundary is therefore: concept-drift methods establish the general
problem of sequential change detection, while Axon studies the narrower confident-wrong
regime in which the agent's answers remain coherent after the rule changes. Axon measures
the precision/earliness tradeoff of stale-belief diagnostics and tests whether a runtime
selector can choose the appropriate gate. The selector failure is part of the result, not a
claim that Axon replaces CUSUM, DDM, or ADWIN.

## Required positioning language for the paper

Add one paragraph to Related Work stating that Page/CUSUM, DDM, and ADWIN detect changes in
an observed stream or error process, whereas Axon detects stale confidence in a frozen
agent's trace under a hidden mid-episode rule shift. State explicitly that Axon is
complementary to drift detection: a drift alarm may indicate that revision is needed, while
Axon asks whether the agent is confidently wrong before a reliable post-shift error-rate
estimate is available.
