# Axon — Deep Research and Recommendation (2026-07-21)

Purpose: decide what Axon can claim that is truly novel AND achievable on a student budget.
This is the result of a literature sweep across seven angles: reasoning collapse, semantic
entropy, self-consistency uncertainty, internal-state probes, early hallucination
detection, process reward models, and multi-agent debate. Sources at the bottom.

Headline: the original four contributions (C1-C4) are, honestly, mostly already published.
But the research surfaced a real, open, cheap gap that is BETTER than the original plan and
sits exactly at the intersection of Axon and PROBE. Read the verdict, then the pivot.

---

## 1. What is already published (the landscape)

### Reasoning collapse is well established
Accuracy decays sharply/exponentially past a model-specific complexity ("reasoning
horizon"), even for frontier models, and it does NOT go away with scale. Multiple 2025-2026
works: SeqBench, GSM-Infinite, LongCoT, the Complexity Ceiling benchmark, Apple's "Illusion
of Thinking," and "Limited Reasoning Space." So "we show reasoning collapses past a
threshold" is a settled result, not a contribution.

### Sampling-based uncertainty is a solved, canonical method
Semantic entropy (Farquhar et al., Nature 2024) is the standard: sample many answers,
cluster by meaning, measure entropy over clusters. Self-consistency (answer agreement
across samples) is used everywhere as a confidence signal. So "divergence across samples
signals uncertainty" is the textbook method, not new.

### Early prediction of errors ALREADY exists — this is the big one
- "Tracing Uncertainty in Language Model Reasoning" reports uncertainty-trace profiles
  predict whether a trace ends correct with AUROC up to 0.801 using only the FIRST FEW
  HUNDRED TOKENS. It also names "silent divergence": traces drift from the right path while
  staying locally coherent, so nothing triggers self-correction.
- "On Early Detection of Hallucinations in Factual QA": tokens PRECEDING a hallucination
  already predict it (~0.80 AUROC) before it is generated.
- Early-exit work ("Stop When Reasoning Converges," "moment of insight") shows a sharp
  confidence jump marks commitment.

This means C2 as originally written — "branch divergence predicts collapse a few steps
before the wrong answer" — is LARGELY ALREADY DONE. Predicting the error early from the
trace is published, with numbers.

### Internal-state probes exist but have a known limit
Probes on hidden states predict hallucination risk (~84%) and whether a query was seen in
training. BUT they mostly reflect KNOWLEDGE RECALL, not truthfulness, and they FAIL when a
wrong answer comes from the same confident recall process as a right one.

### Multi-agent debate is being studied as a diagnostic already
Debate can be a "martingale" (no expected gain over rounds on identical inputs), collapses
toward the majority, and weak models correct only ~3.6% of stance biases. "The Confident
Liar" already diagnoses debate with log-probs and LLM-as-judge. So C4 (debate arena) is a
live, and expensive, research area — risky for a first solo budget paper.

### THE CRACK: everything above fails in the same place
Two independent lines converge on one blind spot:
- Self-consistency / semantic entropy COLLAPSES when the model is confidently wrong — it
  produces the SAME wrong answer across samples, so "agreement" looks like confidence.
  (MIT 2026 cross-model-disagreement work says this explicitly; GPT-4 gives max confidence
  to 87% of answers including wrong ones.)
- Internal probes fail on the same confident-recall failures.

So the entire uncertainty/early-warning toolkit works when the model is UNSURE and breaks
exactly when the model is CONFIDENTLY WRONG. That regime is under-served — and it is
precisely PROBE's failure mode (clinging to a confident, now-false rule).

### The adjacent open niche: belief staleness under change
"STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?" (2026) shows current
benchmarks only test STATIC recall and ignore belief REVISION; the best model scores just
55.2% at noticing a prior belief is outdated ("implicit conflict"). Almost nobody studies
collapse / early-warning under NON-STATIONARY rules. The collapse literature uses static
math/QA. This is open ground.

---

## 2. Honest verdict on the original C1-C4

- C1 (branch structure/shape at the break): mostly covered. Process reward models do
  step-level error detection over trees; inconsistency-score and uncertainty-trace work
  already study where traces diverge. Weak novelty alone.
- C2 (divergence as early-warning, headline): LARGELY DONE on static tasks. AUROC ~0.80
  early prediction is published. Cannot headline as-is.
- C3 (cross-scale invariance of the signature): under-explored but incremental. Good as a
  SUPPORTING result, not a headline.
- C4 (debate pressure cooker): a real but crowded and expensive area. Keep as an optional
  robustness experiment, not the core.

Blunt: if Axon ships C1-C4 on static math/QA, reviewers will say "semantic entropy /
uncertainty traces already do this." We must pivot.

---

## 3. The pivot: the one novel + achievable framing

### Thesis
Existing uncertainty and early-warning methods detect when a model is UNSURE, but fail when
it is CONFIDENTLY WRONG — the dominant failure when the environment's rules CHANGE. Axon is
a diagnostic that detects the moment a model crosses from "confidently right" to
"confidently wrong" under a rule shift, BEFORE it acts on the stale belief — the exact
trigger PROBE needs.

### Why this is genuinely novel (defensible against the closest prior work)
1. It targets the acknowledged BLIND SPOT (confident-wrong), where semantic entropy and
   self-consistency are documented to fail. We are not re-deriving them; we attack where
   they break.
2. It operates under NON-STATIONARITY (rule shift), which the collapse and uncertainty
   literature almost never test — they use static tasks. STALE shows this is open (best
   model 55.2%).
3. It closes the loop with PROBE: detection (Axon) -> revision (PROBE). No prior work pairs
   a boundary detector with a belief-revision agent on the same non-stationary tasks.

### The specific experiment (cheap, reuses PROBE)
Huge advantage: PROBE ALREADY HAS rule-shift environments and saved traces (I3 rule shift,
I6 mixed novelty, plus the traces in probe/traces/). Axon can be built ON TOP of them.

Setup:
- Tasks: PROBE's rule-shift bosses (rule flips mid-episode) — objective ground truth, and
  the confident-wrong regime is guaranteed by construction (the model holds a rule that
  becomes false). Add a static control task so the contrast is visible.
- Models: small open models (Llama-3.1-8B, Qwen, Mistral) via OpenRouter. 2-3 sizes.
- The signal to test (the Axon detector): at each step, measure divergence NOT from plain
  resampling (which stays confidently consistent on the stale rule) but under CONTROLLED
  PERTURBATION — e.g. cross-seed + light prompt/embedding perturbation + a small cross-model
  ensemble. Hypothesis: near the rule shift, perturbation divergence rises BEFORE the
  agent's reward/accuracy drops, even while plain self-consistency stays flat (falsely
  confident).

Primary result to chase:
- Lead time: does the Axon signal fire N steps before the accuracy/reward collapse at the
  shift? Report precision, recall, and mean lead time.
- Head-to-head: Axon perturbation-divergence vs the standard baselines (self-consistency,
  semantic entropy, token-logprob) SPECIFICALLY in the confident-wrong post-shift window.
  Prediction: baselines' AUROC drops toward chance there; Axon stays useful. THAT gap is
  the paper.

### Metrics
Detection AUROC / precision-recall for "about to be confidently wrong," mean lead time in
steps, and the delta between Axon and each baseline restricted to the post-shift
confident-wrong window. Confidence intervals like PROBE did (bootstrap, 95%).

### Baselines (must include, or reviewers reject)
Self-consistency agreement, semantic entropy, mean token log-prob / sequence entropy, and
verbalized confidence ("how sure are you"). These are the methods Axon must beat in the
confident-wrong regime.

### What validates it
On rule-shift tasks, in the post-shift window, standard uncertainty baselines collapse to
near-chance while Axon's perturbation/cross-model divergence still predicts the error with
positive lead time. Ideally the signature holds across 2-3 model sizes (this is where C3
gets folded in as support).

### What kills it
If plain self-consistency already predicts the post-shift error just as well (no blind spot
in practice), or if Axon's perturbation signal has no lead time over the moment of error.
Mitigation: pre-register the lead-time and the confident-wrong-window comparison so the
result is unambiguous either way.

---

## 4. Recommended contribution structure for the paper

- C-A (headline): a detector for the CONFIDENT-WRONG regime under rule shift, shown to beat
  self-consistency / semantic entropy exactly where those are documented to fail.
- C-B (support): early-warning / lead-time — divergence-under-perturbation fires before the
  post-shift collapse. (This is the salvage of old C2, but now on the novel regime.)
- C-C (support): cross-scale — the blind spot and the Axon fix both hold across model sizes.
  (old C3.)
- C-D (optional robustness, only if time/budget): the sealed debate arena as a second,
  independent way to generate divergence; frame around "debate collapses to confident
  majority" (old C4). Cut first if over budget.

Old C1 (branch structure) becomes a mechanism section, not a headline claim.

---

## 5. Novelty defense cheat-sheet (for the related-work section)

- vs Semantic Entropy / self-consistency: "these measure aleatoric uncertainty and are
  documented to fail on confident-wrong; we target exactly that regime under rule shift."
- vs uncertainty-trace early prediction (AUROC 0.80): "prior early-warning is on STATIC
  tasks where the model is often unsure; we test NON-STATIONARY tasks where the model is
  confidently committed to a now-false rule — a regime their signal does not cover."
- vs internal-state probes: "probes reflect knowledge recall, not truthfulness, and fail on
  confident recall; our signal is behavioral divergence under perturbation, not a recall
  probe."
- vs STALE: "STALE benchmarks WHETHER agents notice stale memory; we provide an EARLY,
  step-level detector and tie it to a revision loop (PROBE)."
- vs multi-agent debate: "we use divergence as a diagnostic of the boundary, not as an
  accuracy booster; debate is an optional second view, not the mechanism."

---

## 6. Bottom line

Do NOT ship the collapse/early-warning idea on static math (already done). DO pivot to:
"detecting confident-wrong under rule shift, where existing uncertainty methods fail, as the
trigger for PROBE." It is novel (attacks a known blind spot in an untested regime),
achievable (reuses PROBE's rule-shift envs and small models, cheap on OpenRouter), and it
makes Axon + PROBE a single coherent story instead of two loosely related papers.

Next decision: confirm the pivot, then answer OPEN_QUESTIONS Q1 (define the perturbation /
divergence metric) and Q2 (lock the rule-shift task + static control).

---

## Sources

- Reasoning collapse / horizon: https://arxiv.org/pdf/2509.09677 ,
  https://arxiv.org/html/2602.06176v1 , https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf ,
  https://arxiv.org/html/2606.29278v1
- Semantic entropy (Nature 2024): https://www.nature.com/nature-index/article/10.1038/s41586-024-07421-0
- Self-consistency / cross-model disagreement blind spot:
  https://arxiv.org/html/2604.17112v1 , https://news.mit.edu/2026/better-method-identifying-overconfident-large-language-models-0319
- Early error/hallucination prediction from traces:
  https://arxiv.org/html/2605.07776 , https://arxiv.org/pdf/2312.14183
- Internal-state probes and their limits:
  https://arxiv.org/html/2510.09033v2 , https://arxiv.org/html/2410.02707v4 , https://arxiv.org/html/2407.03282v1
- Process reward models (step-level tree error detection):
  https://arxiv.org/abs/2504.16828 , https://arxiv.org/pdf/2505.14391
- Multi-agent debate limits: https://arxiv.org/abs/2511.07784 , https://arxiv.org/pdf/2606.10296
- Belief staleness under change (STALE): https://arxiv.org/pdf/2605.06527
- Embedding-perturbation intermediate-step uncertainty: https://arxiv.org/pdf/2602.02427
- Early-exit / convergence: https://arxiv.org/html/2605.17672 , https://arxiv.org/pdf/2510.08146
