# Axon — Research Workspace

This workspace is for the second paper in the line that started with PROBE.

Where PROBE proposes a *fix* (an explicit, revisable belief so a frozen model stops
confabulating), Axon proposes the *diagnostic*: a way to measure **where** a model's
reasoning stops holding together and **what** the failure looks like right at that edge.

The two papers are meant to be read as a pair. Axon measures the boundary; PROBE gives
the model a way to act safely near it.

## Working Research Direction

Current working direction (working thesis, not the final title). Updated 2026-07-21 after
the deep literature sweep — see `notes/DEEP_RESEARCH_2026-07-21.md`:

`Detecting the confident-wrong regime under rule shift, where standard uncertainty methods
fail — as the trigger for PROBE`

The pivot in plain terms: existing tools (semantic entropy, self-consistency) catch a model
when it is *unsure*. They break when the model is *confidently wrong* — it repeats the same
wrong answer, so it looks certain. That failure is worst exactly when the rules of the task
CHANGE: the model keeps confidently applying a rule that just became false. Axon detects
that "confidently wrong after a change" moment early, before the model acts on the stale
belief. That is precisely the moment PROBE is built to fix.

(The earlier framing — "branch until the tree stops reconverging" — turned out to be
largely published already, on static tasks. See DEEP_RESEARCH and RELATED_WORK. Branching /
divergence is kept as the *mechanism*, but the novel target is the confident-wrong,
rule-shift regime.)

## Project Name

- Repo / codename: `axon`
- System name: `Axon`
- One-line pitch: a step-level detector that fires when a frozen model becomes confidently
  wrong after the rules change — where semantic entropy and self-consistency go blind.

## Contributions (locked — detail in notes/CONTRIBUTIONS.md)

- **C-A — Confident-wrong detector under rule shift (headline).** A zero-call trace signal
  that is informative under broad shifts, while its G0 component can invert under partial
  shifts; this boundary is part of the result, alongside the comparison with semantic
  entropy and self-consistency.
- **C-B — Early warning / lead time (support).** The signal fires *before* the post-shift
  accuracy collapse, with measurable lead time. (Salvages the old early-warning idea, now on
  the novel regime.)
- **C-C — Cross-scale (support).** The blind spot and the Axon fix both hold across 2-3
  model sizes, so it is not a weak-model artifact.
- **C-D — Pressure cooker (optional robustness).** Sealed multi-model debate as a second,
  independent way to surface divergence; framed around "debate collapses to a confident
  majority." Cut first if over budget.
- Old *branch-structure* idea (C1) is demoted to a mechanism section, not a headline.

### Derived novelty claims (grown from the pivot, novelty-checked 2026-07-21)

- **N1 — Active probe beats passive monitoring (strongest new claim).** One targeted
  counterfactual probe step ("if the old rule still held, what would happen?") detects the
  confident-wrong crossing *earlier* than any passive signal. This operationalizes the word
  "probe" and is the tightest unification with PROBE. Comparative result confirmed missing
  from the literature.
- **N2 — The cling curve.** After a rule shift, accuracy drops immediately but confidence
  lags; measure the gap as a scalar "cling time." It is PROBE's motivating failure turned
  into a number, and it predicts how much PROBE helps per task.
- **N3 — (stretch) Detectability boundary.** Some rule shifts are intrinsically
  undetectable early (when the new rule agrees with the old on recent observations);
  characterize lead time vs old/new rule overlap. An honest limit result.

Paper in one sentence: existing uncertainty methods detect an *unsure* model but fail on a
*confidently wrong* one; Axon detects the confident-wrong crossing under rule shift — early,
actively (N1), and measurably (N2) — giving PROBE the trigger it needs.

## Why This Is Worth Doing (and is still open)

Confirmed by the deep sweep (`notes/DEEP_RESEARCH_2026-07-21.md`). What is already settled
(do NOT claim): reasoning collapses past a complexity threshold; semantic entropy /
self-consistency signal uncertainty; error can be predicted early from the trace on static
tasks (AUROC ~0.80). What is still OPEN (Axon's target):

1. The confident-wrong blind spot. Self-consistency and semantic entropy collapse when the
   model repeats the same wrong answer. Cross-model disagreement is the only proposed fix,
   and it is new and narrow.
2. Non-stationarity. The collapse / uncertainty literature uses static math/QA. Almost
   nobody studies early detection under a RULE SHIFT. STALE (2026) shows even the best model
   scores only 55.2% at noticing its belief is stale — open ground.
3. Detector-to-agent loop. No prior work pairs a boundary detector with a belief-revision
   agent (PROBE) on the same non-stationary tasks.

## Budget Philosophy (important, this is a student project)

Frontier models and GPU clusters are NOT required, and are arguably the wrong tool.

- Small open models (7B-8B: Llama 3.1 8B, Qwen, Mistral) break *sooner* and *more
  visibly*, so the whole collapse boundary can be mapped cheaply.
- Use 2-3 model sizes to get the "boundary scales with capacity, failure mode stays the
  same" story.
- A single frontier spot-check (via OpenRouter, on the best result only) is a confirmation
  at the very end, not the experiment.

The honest framing is a strength: *"we map the full boundary on small models where it is
reachable, and confirm the pattern persists on a frontier model."*

## Relationship to PROBE

- PROBE = the fix (explicit belief + contradiction detection + surgical revision).
- Axon = the diagnostic (detect the distribution boundary / collapse onset).
- Shared thesis: models fail on novel inputs because they cannot detect their own
  distribution boundary. Axon measures where that boundary is; PROBE lets the model act
  near it without confabulating.

## Status

Stage 4 pilot complete on Llama 3.1 8B. The active stale probe reached AUROC 0.950, 95
percent CI [0.875, 1.000], on shift steps 10 through 14. It beat reversed agreement by
0.150 AUROC, 95 percent CI [0.009, 0.340]. Caveat: the gap over cling timing was not clean,
0.200 with 95 percent CI [-0.018, 0.485], so cling timing remains a serious baseline.
