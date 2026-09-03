# Axon — Idea Notes

Raw thinking, kept deliberately informal. This is where the metaphors and half-formed
versions live before they get promoted into the roadmap.

## The Origin Metaphor (keep this, it is good)

From Loki / Yggdrasil: a timeline branches, then each branch branches again, and past a
point the branching can no longer be managed — it grows into an uncontrollable tree
instead of staying a manageable line.

Mapped to a language model: the model "debates itself", spawning branches of reasoning.
In a healthy case the branches reconverge on a single answer. Past a certain problem
complexity the tree fans out combinatorially and never collapses back — the model loops,
contradicts itself across branches, or picks a confident-but-arbitrary branch. That last
one is hallucination.

The non-convergence point = the Yggdrasil-tangle point = the collapse boundary.

## What The Idea Is Really About (reviewer-safe phrasing)

Not: "LLMs crawl the web and fail on new things." (This is wrong — a plain LLM does not
retrieve anything at inference; it generates from patterns compressed into its weights.
Only tools/RAG add retrieval. Do not write the crawl version in the paper.)

Yes: a model performs well near its training distribution and degrades on genuinely novel
inputs. When pushed past what it knows it does not say "I don't know" — it produces
fluent, confident, wrong output. Root cause: the model cannot represent its own
uncertainty and has no mechanism to detect when it has left the region it actually knows.
Hallucination is the symptom; missing self-knowledge of the distribution boundary is the
cause.

## Refined Thesis (the sentence the whole paper defends)

"Models fail on novel inputs because they cannot detect their own distribution boundary.
Axon measures where that boundary is and characterises how reasoning collapses at it;
branch-structure divergence provides an early-warning signal that precedes the visible
hallucination."

## Two Framings — Pick One (see OPEN_QUESTIONS.md)

- Measurement framing: find *where* the boundary is (threshold as a function of task
  difficulty and model size).
- Failure-characterisation framing: describe *what the model does* once it crosses
  (branch shapes, failure-mode taxonomy, early-warning signal).

These are different experiments. The early-warning-signal version is the most novel and
the most useful for PROBE, so it is the current front-runner.

## The One Definition Everything Depends On

What makes a branch "reconverge" vs "diverge"?

Candidate A — self-consistency: two branches reconverge if they reach the *same* final
answer. Divergence = branches disagree.

Candidate B — stability: a branch converges if it reaches *any* stable answer at all
(no looping, no drift). Divergence = no branch settles.

This choice determines the entire measurement. Decide before writing any code.

## Cheap Detection Signals To Try (no human labelling)

- self-consistency divergence across branches (answer disagreement rate)
- entropy / logprob spikes at the token level
- ground-truth tasks where wrong = wrong (so "hallucination" is objective)
- verifier model scoring each branch
- structural: branching factor over depth, reconvergence rate, tree width at collapse

---

## Pivot + derived claims (2026-07-21)

Pivot: stop chasing "reasoning tree collapse" (published). Target CONFIDENT-WRONG under RULE
SHIFT, where uncertainty methods go blind. See DEEP_RESEARCH_2026-07-21.md.

Two derived novelty claims grown from the pivot:
- N1 active probe > passive monitoring: one counterfactual probe step detects the stale
  belief earlier than any passive signal. Operationalizes the word "probe"; strongest
  unifier with PROBE.
- N2 cling curve: accuracy drops at the shift but confidence lags; measure the lag as
  "cling time"; it is exactly PROBE's motivating failure, now a number.
- N3 (stretch): some rule shifts are intrinsically undetectable early (overlap-parameterized
  detectability boundary). Honest limit.

Metaphor bridge: the Yggdrasil branching is still the mechanism (divergence under
perturbation / debate), but the target is now the confident-wrong edge under change, not
generic collapse.

---

## The picture in plain words (2026-07-21)

Two parts working together:

1. The branches = the stress test. We keep splitting the model's answers into more and more
   branches, pushing it toward its edge, until it can no longer hold together. That
   "can't hold together" moment is the break.

2. The detector network = the watcher. As the branches spread out, a small trained network
   watches them and calls out "it's breaking now" — ideally BEFORE the model gives its
   confident wrong answer.

The break shows up as the branches DISAGREEING: they stop landing on the same answer and
spray in different directions. That spraying-apart is the signal the detector learns to
catch. This is the "divergence" the whole paper is built on.

How this fits the pivot: branching is the MECHANISM that generates divergence; the novel
TARGET is still the confident-wrong moment after a rule change, where the usual tools go
blind. The detector network is an optional upgrade over a plain formula (see NN note below).

## Neural network note (the detector)
- Job: one small network that watches the branch signals and predicts "about to be
  confidently wrong."
- Option A (easy, headline): trained on behavioral signals (branch disagreement, confidence).
  Works on any model, including API-only frontier ones.
- Option B (stronger, optional): reads the open-weight model's internal activations. Only
  works on small local models; more crowded research area.
- Tradeoff: a trained detector breaks PROBE's "no training" rule. That is fine for Axon (the
  detector is not the agent), but it is a deliberate choice, not an accident.
- Plan: keep the headline detector simple/training-free so it runs everywhere; add the
  trained network as a stronger variant / ablation.
