# Axon — Research Log

Running record. Each session adds one entry. Same format as the PROBE log.

---

## Session 001

- Date: 2026-07-21
- Phase: Direction finding
- Topic: Reasoning-tree collapse / distribution-boundary detection in LLMs
- Status: Active

### Goal Of This Session

Take the raw "branch until the model breaks" idea and turn it into a defensible,
budget-feasible research direction that pairs with PROBE.

### Key Decisions

- The MCP-server sub-idea ("convert a neural network into an MCP server to unlock its
  true extent") is dropped as stated: MCP is a transport/interface, not a capability
  unlock. Wrapping a model as an MCP server changes how it is called, not what it can do.
  A possible salvage — exposing internal signals (activations, per-layer logits) through
  an interface so an agent can probe its own intermediate states — is parked as a maybe,
  not the contribution.
- The "LLMs crawl the web" mental model is corrected and must not appear in the paper. A
  plain LLM generates from weights; retrieval only exists when a tool is bolted on.
- Working thesis locked to: models cannot detect their own distribution boundary; Axon
  measures it; branch divergence is an early-warning signal.
- Budget: small open models are the primary instrument, not a limitation. Frontier model
  is a single end-of-project spot-check.

### What We Tried

- Literature check on the idea. Findings recorded in RELATED_WORK.md.

### What Failed

- The naive "branch until it breaks" framing is not novel on its own — the collapse
  phenomenon and its failure modes are already published (2025-2026). Novelty must be
  narrowed to branch *structure* and *early prediction*.

### What Changed

- Contribution narrowed from "characterise collapse" (done by others) to "branch-structure
  divergence predicts collapse before it happens" (open).

### Why The Change Mattered

- It is the difference between a rejected restatement of known results and a defensible
  contribution that also feeds PROBE.

### Next Session Should

- Answer Stage 0 in ROADMAP.md: pick the reconverge/diverge definition and the
  ground-truth task family. See OPEN_QUESTIONS.md.

---

## Session 002

- Date: 2026-07-21
- Phase: Direction finding
- Topic: Locking the three contributions
- Status: Active

### Key Decisions

- Three contributions locked and written up in detail in CONTRIBUTIONS.md:
  C1 branch structure (mechanism), C2 early-warning signal (headline), C3 cross-scale
  generality. README now carries the short version.
- C2 is the headline: divergence must be shown to PRECEDE the wrong answer (lead time),
  not just coincide with it. Pre-register the lead-time test.

### Next Session Should

- Answer OPEN_QUESTIONS Q1 (reconverge/diverge definition) and Q2 (ground-truth task
  family), since both C1 and C2 depend on them.

---

## Session 003

- Date: 2026-07-21
- Phase: Direction finding
- Topic: Added C4 pressure cooker (sealed debate arena)

### Key Decisions

- Added C4: sealed multi-model debate used as a divergence stress test, framed as a second
  independent route to the C2 early-warning result (not a who-wins contest).
- Debate literature (Multiagent Debate, Society of Minds) already exists, so novelty is the
  collapse/divergence-measurement angle, not the debate itself. Lit check pending.

### Next Session Should

- Still Q1/Q2 first. Then decide Q6 (C4 core vs add-on).

---

## Session 004

- Date: 2026-07-21
- Phase: Direction finding (deep literature sweep)
- Topic: Testing novelty of C1-C4 and finding a defensible pivot
- Status: Active

### Key Decisions

- Deep research done; written up in DEEP_RESEARCH_2026-07-21.md.
- Verdict: C1-C4 as written are mostly already published (semantic entropy, uncertainty
  traces predicting error AUROC ~0.80 early, PRMs, debate-as-diagnostic). Not novel enough.
- PIVOT: target the CONFIDENT-WRONG regime under RULE SHIFT, where self-consistency and
  semantic entropy are documented to fail, as the trigger for PROBE. Reuses PROBE's
  rule-shift environments and traces. Novel + cheap + unifies the two papers.

### Next Session Should

- Confirm the pivot, then Q1 (perturbation/divergence metric) and Q2 (rule-shift task +
  static control).

---

## Session 005

- Date: 2026-07-21
- Phase: Direction finding (pivot committed + derived claims)
- Topic: Rewrite files to the confident-wrong/rule-shift pivot; add 2 new novelty claims
- Status: Active

### Key Decisions

- README, CONTRIBUTIONS, ROADMAP, IDEA_NOTES, OPEN_QUESTIONS all rewritten to the pivot
  (headline C-A confident-wrong detector under rule shift; C-B lead time; C-C cross-scale;
  C-D optional debate; old branch-structure demoted to mechanism).
- Added two derived, novelty-checked claims:
  - N1 (active probe > passive monitoring) — strongest new claim, unifies with PROBE.
    Comparative result confirmed missing from literature.
  - N2 (cling curve: confidence-accuracy hysteresis / "cling time") — cheap, intuitive,
    quantifies PROBE's motivating failure.
  - N3 (detectability boundary) parked as a stretch/limit result.

### Next Session Should

- Answer revised Q1 (perturbation + metric) and Q2 (rule-shift tasks + static control).
- Decide Q9: which of N1/N2 is claim #2 of the paper (front-runner N1).

---

## Session 006

- Date: 2026-07-21
- Phase: Direction finding (evaluation protocol)
- Topic: How to prove the claims

### Key Decisions

- Wrote EVALUATION.md: the proof is a head-to-head detection contest (AUROC + precision/recall)
  on rule-shift tasks with objective ground truth, against self-consistency, semantic entropy,
  log-prob, and verbalized confidence. Proof = Axon's AUROC stays high in the post-shift
  confident-wrong window where baselines drop toward 0.5. Lead time proves C-B; repeat across
  sizes for C-C; feed into PROBE for the payoff. Pre-register claims + report CIs.

### Next Session Should

- Still Q1 (perturbation + metric) and Q2 (tasks). These now feed directly into EVALUATION.md.

---

## Session 007

- Date: 2026-07-21
- Phase: Direction finding (mechanism clarified)
- Topic: Branching stress test + detector network

### Key Decisions

- Framing locked: branches = the stress test that pushes the model to its edge; branch
  DISAGREEMENT (spraying apart) = the divergence signal; a small detector network = the
  watcher that flags the break early.
- Branching is the MECHANISM; the TARGET stays confident-wrong under rule shift.
- Detector network: Option A (behavioral, training-free-ish, headline) vs Option B (reads
  internals, open-weight only, optional). Headline stays simple; trained net is a variant.

### Next Session Should

- Q1 (define the branch/divergence metric) and Q2 (tasks) still first.

---

## Session 008

- Date: 2026-07-21
- Phase: Direction finding (Q1/Q2 locked + gold standard + benchmarks)
- Topic: Locking measurement and tasks; defining ground truth and external benchmarks

### Key Decisions

- Q1 LOCKED: disagreement = "do branches land on the same answer or split" (simplest,
  model-agnostic).
- Q2 LOCKED: PROBE rule-shift tasks (I3, I6) + one steady control (own the ground truth, near
  free, confident-wrong guaranteed at the flip).
- Gold standard = known correct answer + model confidence; overconfident = sure AND wrong.
- Benchmarks: home turf (PROBE rule-shift) + outside (TruthfulQA, unanswerable math, multi-hop
  QA), mirroring ReAct/Reflexion/Voyager but chosen for the confident-wrong question.

### Next Session Should

- Sketch the branch-and-detect harness on one small model + one rule-shift task (Stage 1-2 of
  ROADMAP), and pick which outside benchmark to run first.

---

## Session 009

- Date: 2026-07-21
- Phase: Direction finding (second sweep, sharpened aim)
- Topic: Fix Q1 contradiction; re-point headline; add closest competitors

### Key Decisions

- Found Q1 contradiction: plain branch-agreement = self-consistency = blind on confident-wrong.
  CORRECTED Q1: divergence must come from shaking the input (paraphrase / counterfactual /
  cross-model), not re-running.
- Perturbation/neighborhood detection is already published (NCB Jan 2026, cross-model 2026,
  behavioral-consistency-for-agents Feb 2026). Use as tools, do not claim.
- Headline RE-POINTED: Axon = live TRIGGER for belief revision under mid-episode rule shift +
  cling-time metric + closed loop with PROBE. Novelty = dynamic setting + acting on the signal,
  not the detector itself.

### Next Session Should

- Pick the sharper novel direction from the Session 009 brainstorm (see chat) and lock it.

---

## Session 010

- Date: 2026-07-21
- Phase: Direction finding (novel directions)
- Topic: Recorded the 5 brainstorm directions

### Key Decisions

- Saved all 5 novel directions in FUTURE_DIRECTIONS.md: (1) cling time as a new metric,
  (2) self-triggered revision loop, (3) classify the TYPE of confident-wrong, (4) budgeted
  probing, (5) is stubbornness a fixed model trait.
- Recommended lead = combine 1 + 2 (new metric + self-triggered method + proof it adapts
  faster). Directions 3-5 are backups/extensions.

### Next Session Should

- Decide whether to lock the 1+2 lead, then move to building the first small experiment.

---

## Session 011

- Date: 2026-07-21
- Phase: Planning (execution timeline)
- Topic: Full staged timeline written for a coding agent to follow

### Key Decisions

- Wrote TIMELINE.md: 7 stages with stop gates, note taking and md update points, logging, and
  budget rules. Version 0, iterative.
- Order: harness, blind spot, cling time, detector contest, lead time, self triggered loop,
  scale up and externals. Stages 2,3,5 reuse the same runs.
- Rules baked in: one word repo name no hyphens, no em dashes, no assistant text, no assistant
  co author, trackable commits, no comments in code, ponytail minimalism, 8B for all pilots,
  5 dollars reserved for one GPT 4.1 spot check.

### Next Session Should

- Start Stage 1, the minimal harness, following the repo rules.

---

## Session 012

- Date: 2026-07-21
- Phase: Build (Stage 1)
- Topic: Minimal harness built and smoke tested

### What We Built

- env.py: RuleShift task, cue to key mapping that flips at shift_at, steady mode for control.
- model.py: OpenRouter client, reads OPENROUTER_API_KEY, offline stub when AXON_STUB is set.
- shake.py: prompt variants and key parser.
- run.py: runs an episode, shakes each step into k prompts, records step, phase, cue, chosen,
  correct, reward, agreement, branches to a csv.
- Stdlib only, no external deps, no comments, ponytail style.

### What Works

- Offline smoke run produced a trace end to end. The confident wrong case already appears in
  the stub trace (high agreement, wrong answer post shift), which is the target phenomenon.

### Known Issue

- Git cannot run reliably on the synced folder from the session (unlink not permitted). The
  code is correct and in place. Init git on the local machine instead. A leftover .git folder
  may need manual deletion.

### Next Session Should

- Stage 2: plug in the real 8B model via OpenRouter and prove the blind spot on I3 and I6.

---

## Session 013

- Date: 2026-07-23
- Phase: Build (Stage 2 blocked)
- Topic: Stage 2 baseline tooling and API block
- Status: Blocked

### Goal Of This Session

Run real Llama 3.1 8B on rule shift and steady traces, compute self consistency and semantic
entropy, then report confident wrong rates with 95 percent confidence intervals.

### Key Decisions

- The runner now gives each branch the same previous trial record. Without history, the
  model only saw the current cue and could not learn or cling to a rule.
- The answer parser now takes standalone A, B, C tokens first, avoiding false A from
  "Answer".
- The Stage 2 analysis uses agreement >= 0.8 and entropy <= 0.75 bits as confidence
  thresholds for k=5.

### What We Tried

- Validated the full trace and analysis path with AXON_STUB on two shift and two steady
  smoke seeds.
- analyze.py writes per step metrics, summary confidence intervals, stop gate AUROCs, and a
  small SVG plot.

### What Failed

- Real OpenRouter runs could not start because OPENROUTER_API_KEY was not present in the
  task environment. The existing model client would otherwise fall back to the offline stub,
  so no real numbers were recorded.

### What Changed

- run.py passes previous trials into prompt variants.
- shake.py renders compact history and parses answer letters with a token match.
- analyze.py computes self consistency, answer entropy, confident wrong rates, confidence
  intervals, and the post shift stop gate.

### Why The Change Mattered

Stage 2 now measures stale rule use rather than cue guessing, and the scripts are ready for
real traces as soon as the key is available.

### Next Session Should

Set OPENROUTER_API_KEY in the task environment and run shift and steady traces for seeds 0
through 4 with Llama 3.1 8B, then run analyze.py and update the Stage 2 result.

---

## Session 014

- Date: 2026-07-23
- Phase: Measure (Stage 2)
- Topic: Blind spot baseline on Llama 3.1 8B
- Status: Stop gate

### Goal Of This Session

Measure whether self consistency and semantic entropy look confident while the model is
wrong right after the rule change.

### Key Decisions

- Ran only meta-llama/llama-3.1-8b-instruct.
- Used 5 seeds, 20 steps, shift_at 10, k=5 branches per step.
- Used the first 5 steps before and after shift as the comparison windows.
- Confidence thresholds: agreement >= 0.8 or answer entropy <= 0.75 bits.
- Revised the prompt to state the initial rule and show previous trials as cue to key pairs.
  The first real prompt was too noisy and did not establish the old rule cleanly.

### What We Tried

- Shift traces: traces/stage2_final/shift_seed0.csv through shift_seed4.csv.
- Steady traces: traces/stage2_final/steady_seed0.csv through steady_seed4.csv.
- Per step metrics: traces/stage2_final_metrics.csv.
- Summary: traces/stage2_final_summary.csv.
- Plot: plots/stage2_confident_wrong.svg.

### Result

- Shift post accuracy: 0.200, 95 percent CI [0.040, 0.360].
- Shift pre accuracy: 0.600, 95 percent CI [0.400, 0.800].
- Steady post accuracy: 0.840, 95 percent CI [0.680, 0.960].
- Shift post confident wrong rate: 0.400, 95 percent CI [0.200, 0.600].
- Shift pre confident wrong rate: 0.080, 95 percent CI [0.000, 0.200].
- Steady post confident wrong rate: 0.000, 95 percent CI [0.000, 0.000].
- Shift post minus shift pre confident wrong: 0.320, 95 percent CI [0.120, 0.560].
- Shift post minus steady post confident wrong: 0.400, 95 percent CI [0.200, 0.600].
- Self consistency danger score AUROC in the post shift window, using 1 minus agreement:
  0.200, 95 percent CI [0.075, 0.370].
- Semantic entropy AUROC in the post shift window: 0.210, 95 percent CI [0.075, 0.397].
- Best direction AUROC was 0.800 for agreement and 0.790 for entropy, meaning confidence
  itself points toward stale wrong answers in this window.

### What Failed

- The original history prompt did not make the old rule stable enough. It mixed choices,
  rewards, and correct labels, and the model was wrong before shift too often.
- The final run proves the normal uncertainty direction is blind, but it also shows a
  reversed self consistency baseline separates wrong from right in the post shift window.

### What Changed

- model.py caps outputs at 8 tokens and adds a 60 second request timeout.
- shake.py now gives the initial rule and compact cue to key trial history.
- analyze.py now reports comparison confidence intervals, not just per window intervals.

### Why The Change Mattered

Stage 2 shows the confident wrong window is real under rule shift. It also tightens the stop
gate: Stage 4 cannot compare only against normal uncertainty. It must include a reversed
agreement or confidence cling baseline.

### Next Session Should

Stop before Stage 3. Decide whether Axon should treat reversed confidence as a baseline to
beat, or rewrite the premise around detecting when confidence flips meaning after a rule
change.

---

## Session 015

- Date: 2026-07-23
- Phase: Measure (Stage 3)
- Topic: Cling time from saved Stage 2 traces
- Status: Active

### Goal Of This Session

Reuse the Stage 2 traces to measure the lag between accuracy collapse and confidence
collapse around the rule shift.

### Key Decisions

- Reused traces/stage2_final only. No new model calls.
- Used branch agreement as the primary confidence measure.
- Defined accuracy collapse as the first post shift step with mean accuracy <= 0.5.
- Defined the first confidence dip as the first post shift step after collapse with mean
  agreement <= 0.5.
- Also checked sustained confidence by comparing mean agreement in the 5 pre shift steps
  to mean agreement in the 5 post shift steps.

### What We Tried

- Added cling.py.
- Wrote traces/stage3_cling_curve.csv.
- Wrote traces/stage3_cling_by_seed.csv.
- Wrote traces/stage3_cling_summary.csv.
- Wrote plots/stage3_cling_curve.svg.

### Result

- Pre shift accuracy: 0.600.
- Post shift accuracy: 0.200.
- Pre shift agreement: 0.632.
- Post shift agreement: 0.632.
- Agreement change: 0.000.
- Group accuracy collapse step: 10.
- Group first confidence dip step: 12.
- Group cling time: 2 steps.
- Seed mean cling time: 1.800 steps, 95 percent CI [0.800, 3.000].
- Seed cling times: 4, 1, 2, 2, 0.

### What Failed

- The confidence drop was not sustained. Agreement dipped at step 12 but rebounded, and the
  first 5 post shift steps had the same mean agreement as the 5 pre shift steps.

### What Changed

- Cling time is now measured as a short first-dip lag, not yet as a stable confidence
  collapse.

### Why The Change Mattered

Stage 3 supports the cling story only in a narrow form: accuracy collapses immediately while
agreement stays high for about two steps. It does not yet prove a clean monotone hysteresis
curve.

### Next Session Should

Before Stage 4, decide the detector contest baselines: normal uncertainty, reversed
agreement, reversed entropy, and the first-dip cling signal.

---

## Session 016

- Date: 2026-07-24
- Phase: Measure (Stage 4)
- Topic: Detector contest on saved rule shift traces
- Status: Stop gate pass with caveat

### Goal Of This Session

Build the smallest active probe detector and score it against the Stage 2 and Stage 3
baselines in the post shift window.

### Key Decisions

- Reused traces/stage2_final.
- Ran only meta-llama/llama-3.1-8b-instruct.
- Used k=3 active probe variants per logged step.
- Scored only shift steps 10 through 14 for the contest.
- Included normal uncertainty, reversed agreement, reversed entropy, cling timing, raw probe
  rule change, and Axon stale probe baselines.
- The active probe asks whether the observed trial record contradicts the initial rule.
  The stale score is the probe contradiction score only when the logged answer still matches
  the old rule.

### What We Tried

- First tried OLD,CURRENT and current-rule probes. They were too noisy.
- Final probe used a direct contradiction question.
- Wrote traces/stage4_probe.csv.
- Wrote traces/stage4_contest.csv.

### Result

- Normal self consistency danger AUROC: 0.200, 95 percent CI [0.071, 0.380].
- Semantic entropy AUROC: 0.210, 95 percent CI [0.073, 0.409].
- Reversed agreement AUROC: 0.800, 95 percent CI [0.620, 0.929].
- Reversed entropy AUROC: 0.790, 95 percent CI [0.591, 0.927].
- Cling timing AUROC: 0.750, 95 percent CI [0.478, 0.952].
- Raw probe rule change AUROC: 0.480, 95 percent CI [0.167, 0.788].
- Axon stale probe AUROC: 0.950, 95 percent CI [0.875, 1.000].
- Axon stale probe precision: 1.000, 95 percent CI [1.000, 1.000].
- Axon stale probe recall: 0.900, 95 percent CI [0.750, 1.000].
- Axon minus reversed agreement AUROC gap: 0.150, 95 percent CI [0.009, 0.340].
- Axon minus reversed entropy AUROC gap: 0.160, 95 percent CI [0.020, 0.365].
- Axon minus cling timing AUROC gap: 0.200, 95 percent CI [-0.018, 0.485].

### What Failed

- The first two active probe designs were not reliable enough. The model explained too much
  or kept inferring the old rule.
- The final detector beats reversed confidence, but it does not cleanly separate from the
  simple cling timing baseline by CI.

### What Changed

- model.py now supports a system instruction and retries transient URL errors.
- probe.py records the active contradiction probe trace.
- contest.py scores the detector contest and adds AUROC gap confidence intervals.

### Why The Change Mattered

Stage 4 gives the first positive detector contest: the Axon stale probe beats normal
uncertainty and reversed confidence in the post shift window. The result is promising, but
the next work must treat cling timing as a serious cheap baseline.

### Next Session Should

Run Stage 5 lead time from traces/stage4_probe.csv, with special attention to whether the
probe fires before, at, or after the first wrong step.

---

## Session: identity lock and the five claims (2026-08-03)

- Question settled with the external review: Axon keeps the 2026-07-21 pivot (confident
  wrong under rule shift), NOT the original branching stress test container, because the
  sweep found branching on static tasks already published. Branching remains a secondary
  mechanism only.
- Standalone identity locked: Axon is the study of stale confidence in language models;
  PROBE is one consumer among several in an applications section. One liner: "PROBE
  needed Axon; Axon does not need PROBE."
- The five claims locked (see CONTRIBUTIONS.md, "The locked five"): blind spot, cling
  curve, asking beats watching, early warning with lead time, detectability limit.
- Review flagged three fixes before scaling: (1) the oracle rule confound in probe.py
  (probes must be built from the model's own belief, not the true rule), (2) the cling
  timing baseline is not yet beaten and must be attacked on varied overlap settings,
  (3) the toy environment must give way to bench adaptation plus a fact update QA
  stream. Next session: fix (1), free, no API.

---

## Session: oracle confound fix (2026-08-05)

- Fix (1) done, code only, no API calls made.
- Root cause confirmed: probe.py's FORMS hardcoded "blue -> B, red -> C, green -> A" as
  the "old rule" text in every contradiction prompt. That is env.py's self.pre dict
  verbatim -- the true environment rule, not anything the model believed. The probe was
  scoring agreement with ground truth the experimenter injected, not staleness of the
  model's own belief. Every Stage 4 number (0.950 AUROC etc.) was measured under this
  confound and does not yet support claim 3.
- Fix: added believed_rule(past), which infers the model's own held rule per cue as the
  mode of ITS PAST CHOSEN ANSWERS for that cue, using only rows strictly before the
  current one (causal, no lookahead). FORMS became forms_for(believed, h), built fresh
  per row from that inferred belief. OLD dict and the hardcoded FORMS list are gone.
- Rows where the model has not yet answered all three cues at least once cannot have a
  belief inferred for all cues -- these are skipped rather than guessed, no chat() call
  made (insufficient_history=1 in the new output column). This only affects early steps;
  contest.py's scoring window (shift_at to shift_at+window) is unaffected since by then
  all three cues have virtually always been sampled.
- Verified offline with a synthetic past-rows list (no API): partial history correctly
  returns None for the unseen cue and is skipped; full history correctly infers the
  believed rule from chosen answers and builds a well-formed probe prompt.
- probe.py, contest.py column contract unchanged (old/change_score/stale_score kept, now
  semantically the model's inferred belief instead of ground truth) so contest.py needs
  no changes.
- CONTRIBUTIONS.md claim 3 note updated: fix done, but Stage 4 numbers predate it and
  must be rerun before they can be cited as evidence for claim 3.

### Next Session Should

Rerun probe.py + contest.py on the Stage 2 traces with the fixed probe to get corrected
Stage 4 numbers. Then move to fix (2): attack the cling-timing baseline gap (currently
CI crosses zero) across varied old/new-rule overlap settings.

---

## Session: corrected Stage 4 numbers, oracle confound removed (2026-08-05)

- Reran probe.py + contest.py on the same Stage 2 traces (meta-llama/llama-3.1-8b-instruct,
  k=3, shift_at=10, window=5, n=25 shift-window rows) with the fixed believed-rule probe.
- Result: axon_probe AUROC dropped from the confounded 0.950 [0.875, 1.000] to 0.785
  [0.583, 0.929]. The oracle confound was inflating the headline number.
- Claim 1 (blind spot) SURVIVES: axon_probe still separates hugely from near-chance
  self-consistency (0.200) and semantic entropy (0.210); gaps ~0.58, CI clear of zero.
- Claim 3 (asking beats watching, N1) DOES NOT SURVIVE at this n: axon_probe now TIES
  every serious baseline instead of beating it -- reversed_agreement gap -0.015
  [-0.270, 0.238], reversed_entropy gap -0.005 [-0.270, 0.272], cling_timing gap 0.035
  [-0.159, 0.250], raw probe_rule_change gap 0.275 [-0.106, 0.670]. All CIs straddle
  zero. The active-probe-beats-passive-signal result reported earlier was an artifact
  of testing against ground truth instead of the model's own belief.
- Honest read: this is exactly why fix (2) was already queued. The cling-timing gap was
  flagged as unresolved even under the confound (CI [-0.018, 0.485]); now that the
  confound is gone, none of the serious baselines are beaten. Claim 3 needs either a
  better active-probe design, a larger n, or varied old/new-rule overlap settings to
  find where (if anywhere) asking actually beats watching -- or it gets reported as a
  fulfilled null result alongside the honest wins, same as Crafter was in PROBE.
- Full numbers: traces/stage4_probe.csv, traces/stage4_contest.csv.

### Next Session Should

Fix (2): design overlap-varied conditions (old/new rule agree on some fraction of
observations) and rerun the probe contest across them. This is now the load-bearing
open question for claim 3 -- does asking ever beat watching, and if so where.

---

## Session: overlap sweep run, claim 3 falsified, claim 3' found (2026-08-20)

Fix (2) finally ran against a live API. Before running it, three speedups, all
verified not to change any number:

- model.chat_many(): the k prompts inside one step are independent (k branch variants,
  or k probe forms), so they fire concurrently instead of as a serial chain. Retries
  went 3 -> 5 with exponential backoff.
- probe.run(): trace files are independent, since `past` only ever accumulates within
  one episode, so files are probed concurrently.
- overlap.generate(): episodes are independent (own env, own seed, own file) so they
  run concurrently; the step loop inside an episode stays sequential.
- contest.auc(): was O(n^2) pairwise per bootstrap sample, which was fine at n=25 and
  nearly timed out at n=240. Replaced with the mid rank formula, which is the identical
  statistic (ties worth half a win). Checked against the old implementation on 3000
  random cases with a deliberately coarse score grid to force ties: 0 mismatches. Also
  reran level 2 end to end and diffed the contest CSV against the pre-optimisation run:
  byte identical. 5+ min -> 42s.

Also added overlap level 0 (the full shift) to LEVELS at matched n, so all three levels
are 30 episodes each. Without it the new levels would have been compared against the old
5 episode Stage 4 run.

Also: contest.load() used to crash on window rows where the model had not yet answered
every cue once (no inferable belief, no probe issued). Those rows are now dropped for
EVERY method, not just the probe, so all methods stay scored on an identical row set.
4 of 240 rows at overlap 0, none at overlap 1 or 2.

Run: 90 episodes, 30 per overlap level, llama-3.1-8b-instruct, steps=20, shift_at=10,
window=8, k=5, probe_k=3. ~236-240 scored rows per level, about 10x the n that left
claim 3 unresolved.

### Result 1: claim 3 (asking beats watching) is FALSIFIED, not unresolved

Decomposed axon_probe into its two factors. stale_score = change_score * [chosen == old],
so it is a probe question gated by a staleness check. Scored separately:

  signal                      overlap 0            overlap 1            overlap 2
  axon_probe (gate x probe)   0.769 [.712,.819]    0.500 [.430,.568]    0.376 [.309,.447]
  bare gate (chosen==old)     0.775 [.718,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  probe alone (change_score)  0.453 [.366,.539]    0.495 [.426,.563]    0.493 [.423,.563]

The probe question is at chance at every overlap level, and the bare gate matches or
beats the full detector everywhere. Mean change_score on wrong vs right rows at overlap 0
is 0.542 vs 0.578 -- the probe answers the same way whether the model is right or wrong.
The model cannot report on whether its own rule belief has gone stale. Every API call
spent on the probe is waste.

At n=25 this looked like a tie needing more data. At n=240 the direction is resolved and
it is not the direction the claim wanted.

### Result 2: claim 3' -- watching is enough, and it is free

The bare gate is deterministic and costs zero model calls: is the agent still answering
the key its own past answers say it believes? At the full shift it reaches AUROC 0.775
[0.718, 0.827] at n=236, against ~0.40 for self consistency and semantic entropy. Claim 1
(the blind spot) therefore survives and is now carried by a cheaper detector than the one
it was originally measured with.

This also explains the long standing cling_timing anomaly. cling_timing was the one
baseline axon_probe never significantly beat (+0.087 [-0.011, 0.184], CI still crossing
zero here). It is a crude proxy for the same gate, so of course it ties -- it was
measuring the thing that was actually doing the work.

### Result 3: claim 5 (detectability limit) measured, and it inverts

AUROC by number of cues keeping their pre shift key: 0 -> 0.775, 1 -> 0.515, 2 -> 0.364.
It decays THROUGH chance and comes out backwards. Mechanism confirmed in the traces:
P(chosen == believed_old) on wrong vs right rows is 0.652/0.102 at overlap 0, 0.662/0.632
at overlap 1, 0.465/0.738 at overlap 2. Once most cues keep their key, still answering the
old belief is the correct move, so the gate anti correlates with wrongness.

The detector is not merely blind to small shifts. It is confidently backwards on them,
which is exactly the failure mode it exists to catch. Honest and quotable.

Full numbers: traces/stage4b_overlap/ov{0,1,2}_contest.csv,
traces/stage4b_overlap_summary.csv, printed by overlap_summary.py.

### Next Session Should

The gate is episode wide but the failure is per cue, which is what the inversion at
overlap 2 is telling us. Build the per cue gate: score staleness only against the cue
being answered, using that cue's own believed key and its own recent evidence, rather
than one flag for the whole episode. Predicted effect: overlap 1 and 2 recover toward
overlap 0 instead of inverting. That prediction should be written down before the run,
same as PROBE's registered retests.

Then claims 2 (cling curve) and 4 (lead time) are still unrun, and cross scale
replication is still unrun. Claim 3 should be written up as a negative result about LLM
self report, not quietly dropped.

---

## Registered prediction: the contradiction gate (2026-08-20, written BEFORE the run)

Correcting the diagnosis from earlier today. The gate is already per cue --
`old = believed[row["cue"]]` reads the believed key for the cue being answered, not an
episode wide flag. So "make it per cue" is not the fix, because it already is.

The actual defect: the gate fires on CONSISTENCY WITH OWN BELIEF. Consistency is only
evidence of danger once that belief has been contradicted. At overlap 2 the two unchanged
cues are never contradicted, so consistency there means correct, and the gate inverts.
That is why AUROC goes 0.775 -> 0.515 -> 0.364 rather than decaying to chance.

Gate variants to score. All are deterministic functions of trace columns the agent
already observes, so all cost zero model calls. Reward is used, never `correct`: reward is
returned to the agent by env.step and is a legitimate observation, whereas `correct` is
the hidden ground truth and using it would reintroduce the oracle confound. Only rows
strictly before the current one are read.

  G0  chosen == believed_old                       (today's bare gate, the baseline)
  G1  contradicted(cue, chosen)                    binary: has this exact (cue, key) pair
                                                   ever earned reward 0 before this row
  G2  graded contradiction                         fraction of past (cue, chosen) attempts
                                                   that earned reward 0
  G3  G1 and chosen == believed_old                contradicted AND still clinging

### Predictions (registered, to be scored against)

1. G1 and G2 recover overlap 1 and overlap 2 substantially, and neither inverts: both
   stay above 0.5 at every overlap level. This is the main prediction. If either still
   comes out below 0.5 at overlap 2, the contradiction story is wrong.
2. At overlap 0, G1/G2 land within about 0.05 of G0's 0.775; they should not need to beat
   it, only to hold roughly level while fixing the other two levels.
3. G1/G2 LOSE lead time relative to G0. The contradiction gate cannot fire until the cue
   has been answered wrongly at least once, so it is reactive where G0 is anticipatory.
   Registered explicitly because it is a cost, and because C-B (lead time) is the next
   stage and must be measured on whichever gate wins here.
4. G3 is not expected to beat G1. Adding the clinging term reintroduces exactly the
   factor that inverts at high overlap.

Known limitation of G1/G2, registered up front: if the agent abandons a contradicted key
and moves to a DIFFERENT wrong key, the gate stays silent while the answer is wrong. Those
are false negatives by construction and should be counted, not hidden.

Scored offline on the traces already collected in traces/stage4b_overlap. No new API
calls.

### Result of the registered run (2026-08-20, same day, scored offline, zero API calls)

G0 reproduces 0.776 [0.721, 0.827] at overlap 0 against the 0.775 measured earlier by a
different code path, so gates.py is validated before reading anything else off it.

  gate                          overlap 0            overlap 1            overlap 2
  G0 cling                      0.776 [.721,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  G1 contradicted               0.592 [.517,.668]    0.748 [.698,.796]    0.746 [.691,.798]
  G2 contradicted graded        0.548 [.459,.637]    0.743 [.692,.794]    0.745 [.690,.799]
  G3 contradicted and cling     0.634 [.578,.686]    0.682 [.638,.728]    0.637 [.591,.687]
  G4 either                     0.734 [.661,.804]    0.580 [.524,.636]    0.472 [.415,.527]
  G5 cling after any contra.    0.776 [.721,.827]    0.517 [.456,.580]    0.357 [.297,.422]

Scoring against what was registered, including the misses:

- Prediction 1 CONFIRMED. G1 and G2 stay above 0.5 at every overlap level and the
  inversion is gone. Overlap 1 goes 0.515 -> 0.748, overlap 2 goes 0.364 -> 0.746. The
  contradiction story was right about the cause.
- Prediction 2 WRONG. G1/G2 were predicted to land within about 0.05 of G0 at overlap 0.
  They land 0.18 to 0.23 below it (0.592 and 0.548 against 0.776), far outside the
  registered band. Recorded as a failed prediction, not quietly widened.
- Prediction 4 HALF WRONG. G3 loses to G1 at overlap 1 and 2 as predicted, but beats it at
  overlap 0 (0.634 against 0.592). The clinging term is not purely harmful; it carries the
  early signal that G1 structurally cannot see.
- Prediction 3 (lead time cost) NOT YET SCORED. That is C-B and is measured next.

The reason prediction 2 failed is prediction 3's mechanism showing up in AUROC rather than
waiting for the lead time stage: at a full shift every cue changed, so clinging is wrong
IMMEDIATELY, before any contradiction exists to be observed. G1 cannot fire on a cue until
that cue has already been missed once, so at overlap 0 it forfeits exactly the rows G0
gets for free. "silent on wrong" makes the same point directly: G1 misses 43.7 percent of
wrong rows at overlap 0 against G0's 34.7 percent.

### The actual finding: no fixed gate wins everywhere

G0 wins at overlap 0 and inverts at overlap 2. G1 is flat and reliable at overlap 1 and 2
and weak at overlap 0. Neither dominates, and the two combinations tested do not rescue it:
G4 (either fires) inherits G0's inversion and lands at 0.472 at overlap 2, and G5 (cling,
but only once some contradiction has been seen) is G0 with extra steps -- 0.776 / 0.517 /
0.357, statistically identical to G0 at all three levels, because at these episode lengths
some contradiction has almost always already occurred by the time the window opens.

This is structurally the same shape as PROBE's ablation result: heavy machinery wins where
the dynamics are hidden, loses where they are not, and no single fixed configuration is
best everywhere. Axon reaches it independently, on a different mechanism, which is worth
saying plainly rather than presenting one gate as the winner.

The honest headline is therefore narrower than this morning's: the detector is free and it
works, but WHICH free gate to use depends on shift size, and shift size is not observable
at runtime. That is either the paper's adaptivity result or its honest limit, and which one
it becomes depends on whether a runtime selectable rule exists.

### Next Session Should

Two things, in this order.

1. C-B lead time, measured on G0 and G1 separately, because prediction 3 is still unscored
   and the whole G0 versus G1 tradeoff is a lead time story. Expect G0 to fire earlier and
   G1 to fire more reliably.
2. Decide whether a runtime selectable rule exists that picks between G0 and G1 without
   knowing the overlap. Candidate worth testing: contradiction DENSITY across cues. At a
   full shift, contradictions appear on all three cues quickly; at overlap 2 they appear on
   only one. That count is observable, costs nothing, and is a real trigger rather than a
   tuned constant. If it works, Axon has an adaptive gate; if it does not, claim 5 absorbs
   it as the honest limit and the paper reports the tradeoff as measured.

---

## C-B lead time: definition and registered prediction (2026-08-20, BEFORE the run)

EVALUATION.md Step 5 says only "how many steps BEFORE the actual failure the signal
fires", which is not precise enough to run. Pinning it here, with a structural caveat
that has to be stated first or the headline number will be meaningless.

### The structural trap

A per cue lead time cannot be positive, by construction. Every gate is evaluated on the
answer the agent just gave, and "failure on cue c" IS that answer being wrong. So the
earliest a gate can fire about cue c is the same step c fails: lead 0 at best. G1 is
strictly worse than that, because it cannot fire on c until c has already been missed
once, so its per cue lead is always negative. Reporting per cue lead as the headline would
be reporting an artifact of the definition, not a property of the detector.

### The definition actually used

Early warning here means CROSS CUE transfer: the gate fires on one cue, and that warns
about cues that have not failed yet.

  fire_step(episode)  = first post shift step at which the gate fires on ANY cue
  failure_step(c)     = first post shift step at which cue c is answered wrong
  lead(c)             = failure_step(c) - fire_step(episode)

Positive lead means the warning arrived before that cue failed. Cues that never fail in
the window carry no lead and are counted separately as false alarms if the gate fired on
them. Both numbers get reported; a gate that buys lead time by firing constantly is not
an early warning system, and the false alarm rate is what exposes that.

### Registered predictions

1. G0 mean lead > G1 mean lead at every overlap level. This is prediction 3 from the
   earlier gate run, finally scored.
2. G1 mean lead is at or below zero even at episode level, because its first fire anywhere
   still requires a miss to have happened somewhere.
3. At overlap 0, G0 shows positive mean lead on later failing cues: all three cues shift
   at once, so the first cling fire genuinely precedes the other cues' failures.
4. At overlap 2, most G0 fires are false alarms, because the cues it fires on are the
   unchanged ones that never fail. Predicted G0 false alarm rate at overlap 2 clearly
   above its rate at overlap 0.
5. Soft stop gate from TIMELINE.md stands: if lead is zero everywhere, C-B is reported as
   detection without early warning rather than dropped.

### C-B result (2026-08-20, scored offline, zero API calls)

  overlap  gate              mean lead [95% CI]      frac pos   false alarm (n)
  0        G0 cling          +0.91 [+0.43, +1.39]    0.537      0.500 (n=2, uninformative)
  0        G1 contradicted   -0.25 [-0.73, +0.23]    0.298      0.500 (n=2, uninformative)
  1        G0 cling          +1.76 [+1.21, +2.33]    0.629      0.950 (n=20)
  1        G1 contradicted   -0.51 [-1.15, +0.13]    0.294      0.050 (n=20)
  2        G0 cling          +1.77 [+1.17, +2.37]    0.673      0.673 -> 0.947 (n=38)
  2        G1 contradicted   -0.27 [-0.96, +0.45]    0.265      0.053 (n=38)

G2 is identical to G1 throughout: the graded score is nonzero exactly when the binary one
is, so it fires on the same steps and only the AUROC ranking ever separated them.

All four registered predictions confirmed.

1. G0 mean lead beats G1 at every level. CONFIRMED (+0.91 vs -0.25, +1.76 vs -0.51,
   +1.77 vs -0.27).
2. G1 lead at or below zero even at episode level. CONFIRMED at all three levels; every
   point estimate negative, and no interval reaches a positive mean.
3. G0 positive mean lead at overlap 0. CONFIRMED, +0.91 [+0.43, +1.39], interval clear of
   zero. C-B survives: the signal does fire before later cues fail, so this is genuine
   early warning and not detection at the moment of failure.
4. G0 false alarms rise sharply with overlap. CONFIRMED and then some: 0.950 at overlap 1
   and 0.947 at overlap 2, against G1's 0.050 and 0.053.

The overlap 0 false alarm cell is 1 of 2 cue episodes and carries no information, because
when every cue shifts almost nothing survives unfailed. Recorded as uninformative rather
than quoted as 0.500; the meaningful denominators are 20 and 38.

### The number that would have been a lie on its own

G0's mean lead GROWS with overlap, +0.91 to +1.76 to +1.77. Read alone that says the
detector gets better at early warning exactly where AUROC said it inverts. It does not.
The lead grows because G0 is firing on nearly everything: at overlap 1 and 2 it raises an
alarm on 95 percent of the cues that never fail at all. Fire on every step and you always
precede the failure. This is why the false alarm rate was registered up front alongside
the lead -- mean lead is not interpretable without it, and quoting the lead alone would
have inverted the paper's conclusion.

### Where C-B lands

The tradeoff is now fully characterised, and it is clean enough to be a result rather than
a hedge:

  G0 warns early and cries wolf. Positive lead, 95 percent false alarms once the shift is
  partial.
  G1 never warns early and almost never cries wolf. Structurally negative lead, 5 percent
  false alarms, and flat AUROC 0.75 across overlap.

Neither is the detector. Together they are a precision versus earliness frontier, and
which end of it you want is a deployment choice: G0 for a cheap trigger that a verifier
can afford to double check, G1 for an alarm that should be trusted when it fires.

CONTRIBUTIONS C-B updated. Numbers in traces/stage4b_leadtime.csv, script leadtime.py.

### Next Session Should

The runtime selectable rule is now the load bearing open question for the whole detector,
because both gates are known quantities and neither wins alone. Test contradiction DENSITY
across cues: how many DISTINCT cues have been contradicted so far. At a full shift that
count reaches three quickly; at overlap 2 it stops at one. It is observable, it costs
nothing, and it is a real trigger rather than a tuned constant. Predicted use: high density
means trust G0 (the shift is broad, clinging is dangerous), low density means trust G1 (the
shift is narrow, clinging is mostly correct). Register the prediction before running it.

Then C-C cross scale is still unrun, and claim 2 (the cling curve) is still unrun.

---

## Contradiction density as a runtime selector: registered prediction (2026-08-20, BEFORE the run)

Both gates are known quantities and neither wins alone, so the question is whether the
agent can tell AT RUNTIME which one it should be trusting, without being told the overlap.

Definition. Contradiction density d(t) = the number of DISTINCT cues that have been
contradicted before step t, where a cue counts as contradicted once some key answered for
it earned reward 0. Range 0 to 3. Computed from strictly earlier rows only, from columns
the agent observes. Costs nothing.

Rationale: at a full shift all three cues start failing, so d climbs to 3 quickly. At
overlap 2 only one cue can ever fail, so d stops at 1. The count is a direct readout of
how broad the shift is, which is exactly the quantity that decides whether clinging is
dangerous or correct.

Gates under test:

  G6_adaptive_d2   G0 if d >= 2 else G1
  G6_adaptive_d3   G0 if d >= 3 else G1
  G7_blend         (d/3) * G0 + (1 - d/3) * G1     -- no threshold, no tuned constant

G7 is included because a threshold is a tuned constant and the blend avoids one entirely.
If the blend works as well as the thresholded version, the blend is the honest thing to
report.

### Precondition that kills the idea immediately

Mean d in the scored window must differ across overlap levels, highest at overlap 0 and
lowest at overlap 2. If d does not separate the levels, it cannot select anything and the
whole approach is dead on arrival. This gets checked and reported first, before any AUROC.

### Registered predictions

1. Mean d separates: overlap 0 > overlap 1 > overlap 2, with overlap 2 near 1.0.
2. The adaptive gates are never significantly worst at any level: within about 0.05 of
   G0's 0.776 at overlap 0, and within about 0.05 of G1's 0.748 / 0.746 at overlap 1 / 2.
   This is the PROBE "never worst" framing applied to Axon.
3. False alarm rate of the adaptive gates stays near G1's at overlap 1 and 2, below 0.20,
   rather than near G0's 0.95.
4. Registered cost. Early in the window d is still small even at overlap 0, so the adaptive
   gate will be running G1 during exactly the steps where G0's early warning matters.
   Predicted: adaptive lead at overlap 0 stays positive but comes in BELOW G0's +0.91.
   If the lead goes negative, the adaptive gate has bought AUROC by giving up C-B, and
   that trade has to be reported, not hidden.

### Density selector result (2026-08-20): FAILS, and the reason is diagnosable

Precondition, checked first as registered. Mean d in the window: overlap 0 = 2.54,
overlap 1 = 2.32, overlap 2 = 2.11. The direction is right but the magnitude is badly
wrong -- overlap 2 was predicted near 1.0 and came in at 2.11, and 53 of its 240 rows show
all three cues contradicted when only one cue actually changed.

  gate              overlap 0            overlap 1            overlap 2
  G0 cling          0.776 [.721,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  G1 contradicted   0.592 [.517,.668]    0.748 [.698,.796]    0.746 [.691,.798]
  G6 adaptive d>=2  0.755 [.699,.807]    0.518 [.456,.583]    0.358 [.296,.423]
  G6 adaptive d>=3  0.673 [.605,.735]    0.627 [.566,.687]    0.654 [.594,.711]
  G7 blend          0.782 [.715,.843]    0.582 [.514,.653]    0.453 [.375,.534]

  gate              mean lead ov0        false alarm ov1      false alarm ov2
  G0 cling          +0.91 [+0.43,+1.39]  0.950                0.947
  G1 contradicted   -0.25 [-0.73,+0.23]  0.050                0.053
  G6 adaptive d>=3  -0.12 [-0.63,+0.39]  0.350                0.237
  G7 blend          +1.12 [+0.65,+1.58]  0.950                0.947

Scoring the registered predictions:

1. PARTIAL FAIL. d separates in the right order but nowhere near far enough to select on.
2. FAILED. "Never worse than about 0.05 off the best gate" does not hold for any variant.
   G6 d>=3 is the only one that never inverts, and it is 0.10 to 0.12 BELOW the best gate
   at every single level -- never worst, but also never good, and dominated everywhere.
   G6 d>=2 and G7 both still invert at overlap 2 (0.358 and 0.453).
3. FAILED. G6 d>=3 false alarms are 0.350 and 0.237, not below 0.20. G7 is 0.950 and
   0.947, exactly as indiscriminate as G0.
4. FAILED, and worse than the registered cost. G6 d>=3's lead at overlap 0 was predicted
   positive but below G0's +0.91; it came out NEGATIVE at -0.12. So it gave up C-B and
   bought nothing for it. G7 went the other way (+1.12) but only because it is G0 wearing
   a hat, which its 0.95 false alarm rate confirms.

Root cause, and it is the useful part. Density counts "this cue has been answered wrong",
not "this cue's rule has changed". Those two coincide only if the backbone is otherwise
accurate. Llama 3.1 8B gets unchanged cues wrong on its own, every such slip marks that
cue contradicted, and the count saturates regardless of how broad the shift actually was.
The selector is measuring the model's error rate as much as the environment's shift.

### One refinement is implied by that diagnosis, registered before running

Count a cue as rule changed only when a key that PREVIOUSLY EARNED REWARD for that cue now
fails for it. A key that used to work and stopped working is evidence the rule moved; a key
that never worked is just a wrong guess. Still free, still observable, still no tuned
constant beyond the threshold.

  G8_confirmed_density   number of distinct cues where a previously rewarded key later
                         earned reward 0
  G8_adaptive            G0 if confirmed density >= 3 else G1
  G9_blend               (confirmed/3) * G0 + (1 - confirmed/3) * G1

Threshold is 3 rather than 2 because G0 wins only when ALL cues shift: overlap 0 has three
changed cues, overlap 1 has two, overlap 2 has one, and G1 is the better gate at both
overlap 1 and 2.

Registered predictions. (a) Mean confirmed density separates the levels far more sharply
than raw density did, with overlap 2 at or near 1.0 -- this is the precondition and it is
what raw density failed. (b) If (a) holds, G8_adaptive lands within 0.05 of the best gate
at every level. (c) If (a) fails, contradiction density is dead as a selector in any form,
and the G0 versus G1 tradeoff is reported as Axon's honest limit under claim 5 rather than
solved.

### Confirmed density result (2026-08-20): precondition fixed, selector still fails

  mean confirmed density   overlap 0 = 1.48   overlap 1 = 1.00   overlap 2 = 0.52
  (raw density was          2.54                2.32               2.11)

  gate                       overlap 0            overlap 1            overlap 2
  G0 cling                   0.776 [.721,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  G1 contradicted            0.592 [.517,.668]    0.748 [.698,.796]    0.746 [.691,.798]
  G8 adaptive c>=3 (reg.)    0.596 [.521,.669]    0.748 [.698,.796]    0.746 [.691,.798]
  G9 blend (registered)      0.697 [.622,.768]    0.688 [.627,.752]    0.671 [.598,.740]
  G8b adaptive c>=2 (POST HOC, not registered)
                             0.655 [.587,.718]    0.655 [.596,.713]    0.746 [.691,.798]

- Prediction (a) HELD. Confirmed density separates the levels far more sharply than raw
  density: 1.48 / 1.00 / 0.52 against 2.54 / 2.32 / 2.11, and at overlap 2 it never once
  reaches 2. Screening out keys that never worked was the right diagnosis.
- Prediction (b) FAILED. G8 is within 0.05 of the best gate at overlap 1 and 2 only because
  it IS G1 there; at overlap 0 it sits 0.18 below G0. The registered threshold of 3 is
  almost never met -- only 23 of 240 rows at overlap 0 -- so the gate collapses to G1
  everywhere and forfeits the one level where G0 wins.
- G8b (threshold 2, POST HOC and labelled as such, not registered before the run) does not
  rescue it either: 0.655 / 0.655 / 0.746, never inverting but dominated at two of three
  levels. Recorded because it was run, not because it works.

### Why no selector works, and this is the structural part

The selector needs to know whether ALL cues shifted. That evidence accumulates strictly
more slowly than the decision it is meant to inform. Confirmed density reaches 3 in 23 of
240 rows at overlap 0, and by the time it gets there the window is nearly spent and G0's
early warning has already been forfeited. Raise the threshold and the gate never fires as
G0; lower it and overlap 2 starts selecting G0 and inverts again. The blend just averages
the two failure modes. This is not a tuning problem and more seeds will not fix it: the
quantity that decides which gate to trust is only knowable after the moment the decision
had to be made.

Prediction (c) therefore triggers as registered. Contradiction density is dead as a
selector in raw form, confirmed form, thresholded at 2 or 3, and blended. The G0 versus G1
tradeoff is Axon's honest limit, and it goes under claim 5 rather than being presented as
solved.

CONTRIBUTIONS claim 5 updated. Numbers: traces/stage4b_gates.csv,
traces/stage4b_leadtime_adaptive.csv.

### Next Session Should

Claim 2 (the cling curve) is the last unrun headline claim and needs no new API calls --
it is a per model scalar measured off traces already collected. Do that next.

After that, C-C cross scale is the only remaining claim needing spend, and ROADMAP.md is
still the July version: it predates the locked five, the oracle confound, the gate work,
and everything above. Rewrite it before planning further.

---

## Claim 2, the cling curve: registered prediction (2026-08-20, BEFORE the run)

Confidence is branch agreement, as locked in OPEN_QUESTIONS Q8: it is the thing that stays
falsely high, and that staying-high IS the cling.

Cling time = (first step in the post shift window where agreement drops to or below 0.5)
minus (first post shift step answered wrong). Episodes where agreement never dips are
CENSORED, and the censored rate is reported next to the mean, because a mean taken only
over episodes that did dip is survivorship bias.

Fixed first: cling.py grouped episodes by seed, but the overlap sweep reuses seeds 0..9
across three cue combinations per level, so three distinct episodes would have merged.
Now grouped by trace file. Verified against stage2_final, where one file per seed makes the
two groupings identical: reproduces the Stage 3 pilot exactly (1.800 [0.800, 3.000],
agreement change 0.000).

### Registered predictions

1. The Stage 3 pilot's agreement change of exactly 0.000 was measured at n=5 and is the
   number most likely to be noise. At n=30 per level, predicted still small but no longer
   exactly zero: within about 0.05 of zero at overlap 0.
2. Censoring is the real risk to this claim. If agreement genuinely never dips, cling time
   is not a measurable scalar at all, it is unbounded, and claim 2 has to be restated. The
   pilot reported a censored rate of 0.000 at n=5, which given prediction 1 looks
   suspicious. Predicted: censored rate at n=30 is materially ABOVE 0.000.
3. Cling time increases as overlap increases. Fewer cues change, so less evidence arrives
   per step, so confidence should take longer to break.
4. Stop gate, stated in advance so it cannot be moved afterwards: if the censored rate
   exceeds 0.5 at any level, cling time is reported as censored rather than as a scalar,
   and claim 2 is restated as "confidence does not break within the window" -- which
   strengthens claim 1 (the blind spot) while weakening claim 2 as its own contribution.
   That is a real possible outcome and it will be reported as such.

### Claim 2 result (2026-08-20, n=30 per level, zero API calls)

  metric                      overlap 0   overlap 1   overlap 2
  pre accuracy                0.721       0.725       0.762
  post accuracy               0.208       0.396       0.588
  pre agreement               0.638       0.641       0.641
  post agreement              0.602       0.638       0.654
  agreement change            -0.037      -0.003      +0.013
  group confidence dip        CENSORED    CENSORED    CENSORED
  min post shift agreement    0.540       0.567       0.613
  episode mean cling time     3.10 [2.21, 4.03]  2.56 [1.85, 3.33]  3.48 [2.35, 4.65]
  episode censored rate       0.033       0.100       0.233

Post accuracy rising with overlap (0.208 / 0.396 / 0.588) is the sanity check: more
unchanged cues means more still-correct answers. It passes, so the traces are behaving.

Scoring the registered predictions:

1. CONFIRMED. The pilot's exactly 0.000 agreement change was an n=5 artifact. At n=30 it is
   -0.037 at overlap 0, inside the registered 0.05 band and no longer exactly zero.
2. CONFIRMED, and more strongly than registered. Episode censoring is 0.033 / 0.100 / 0.233,
   all above the pilot's 0.000. At the GROUP level it is total: mean agreement never once
   drops to 0.5 at any overlap level, bottoming at 0.540 / 0.567 / 0.613. The pilot's
   "group cling time = 2 steps" was noise at n=5 and does not survive.
3. FAILED. Cling time was predicted to rise with overlap. It goes 3.10, 2.56, 3.48 -- not
   monotone, overlap 1 is the lowest, and all three intervals overlap heavily. There is no
   trend; cling time does not vary with shift size.
4. Stop gate NOT triggered. Max censored rate is 0.233, well under 0.5, so episode level
   cling time is reportable as a scalar rather than as censored.

### What claim 2 actually is now

Accuracy falls 0.721 -> 0.208 at the full shift. Agreement moves 0.638 -> 0.602. The
confidence curve is flat while the accuracy curve collapses underneath it. Confidence does
not lag the accuracy drop so much as never arrive at all inside the window.

That is the cleanest single picture of claim 1 in the whole project -- one plot, two lines,
one falling and one not. But it makes claim 2 weaker as an INDEPENDENT contribution, not
stronger. The per episode scalar does exist (3.10 steps [2.21, 4.03] at the full shift, and
the n=5 pilot's 1.8 underestimated it), but what it times is the first transient dip below
0.5 in a single episode, not a sustained confidence collapse -- the group mean never gets
near 0.5. Calling that "cling time, a measurable per model scalar" oversells what was
measured, and it does not vary with shift size, which is what a real scalar of this kind
should do.

Honest placement: claim 2 folds into claim 1 as its visualisation and its number, rather
than standing as a separate headline. The paper gets a stronger claim 1 and one fewer
claim, which is the right trade.

CONTRIBUTIONS claim 2 updated. Curves in traces/stage4b_overlap/ov{0,1,2}_cling_curve.csv,
per episode in ov{0,1,2}_cling_by_episode.csv, plots in plots/stage4b_ov{0,1,2}_cling.svg.

Fixed along the way: cling.py crashed with StopIteration when a curve never crossed the
threshold. "Confidence never broke" is a result and must be reportable, so it now returns
CENSORED and also reports min post shift agreement. Verified against stage2_final: output
identical to pre patch.

### Next Session Should

All five claims are now measured. What remains is external validity, and it is the whole
remaining risk: every number in this project is ONE model (llama 3.1 8b instruct) on ONE
synthetic environment (RuleShift, three cues). In order: C-C cross scale, then a second
testbed, then the PROBE tie in. Rewrite ROADMAP.md first -- it is still the July version and
predates the locked five, the oracle confound, and all of the gate work.

---

## Stage 5, cross scale: registered prediction (2026-08-20, BEFORE the run)

Ladder, all one family so that scale is the only thing varying and no training difference
confounds it:

  meta-llama/llama-3.2-3b-instruct    3B
  meta-llama/llama-3.1-8b-instruct    8B   (already run, this is the v0 result)
  meta-llama/llama-3.3-70b-instruct   70B

Same overlap sweep as v0: 90 episodes per model, 30 per overlap level, steps=20,
shift_at=10, window=8, k=5, probe_k=3. Output under traces/stage5_scale/<size>/.

This stage exists because every v0 number rests on one model. Its job is to promote claims
from PROVISIONAL to VALIDATED-on-scale, or to expose them as 8B artifacts.

### Registered predictions

1. CLAIM 1 holds at every scale. The gate beats self consistency and semantic entropy at
   overlap 0 on all three models, interval clear of zero.
   KILL: if the 70B baselines catch the gate, claim 1 is about small models, not LLMs, and
   has to be restated that way.
2. CLAIM 3 is the one most likely to change. The 8B probe was at chance (0.453 / 0.495 /
   0.493). If the 70B probe reaches AUROC 0.6 or better at overlap 0 with its interval
   clear of 0.5, claim 3 is SCALE DEPENDENT rather than false, which is a more interesting
   result than either. Registered expectation: it stays at chance, but this is the
   prediction I hold most weakly.
3. CLAIM 2 censoring persists at scale. Group confidence never reaches 0.5 on any model,
   and agreement change stays within 0.1 of zero. If the 70B DOES break confidence, claim 2
   revives as its own claim and cling time becomes a genuine cross model discriminator.
4. CLAIM 5's inversion is structural, not a model property. G0 still inverts at overlap 2
   on all three models (AUROC below 0.5). If a bigger model does not invert, the mechanism
   story is wrong.
5. DENSITY SELECTOR scales with accuracy. Raw contradiction density was polluted by ordinary
   model error at 8B. Predicted: mean raw density at overlap 2 is HIGHER on 3B and LOWER on
   70B than the 8B value of 2.11, and if 70B falls below about 1.5 the selector is worth
   re-testing there before claim 5's limit 2 is called final.
6. Absolute accuracy rises with scale, so post shift accuracy at overlap 0 goes up from
   8B's 0.208. That is a sanity check, not a claim: if it does not, the ladder is broken.

### Stage 5 result (2026-08-20): the detector scales, and claim 3 comes back inverted

90 episodes per model, 30 per overlap level. All at overlap 0 unless stated.

  model  G0 gate              probe (raw)          probe REVERSED       unc_agree   post acc  raw d(ov2)
  3B     0.743 [.689,.795]    0.506 [.500,.515]    0.494 [.485,.500]    0.484       0.287     2.23
  8B     0.776 [.721,.827]    0.457 [.372,.543]    0.543 [.457,.628]    0.399       0.208     2.11
  70B    0.976 [.953,.995]    0.227 [.173,.288]    0.773 [.712,.827]    0.492       0.571     0.67

Scoring the registered predictions:

1. CONFIRMED, and stronger than registered. The gate beats the uncertainty baselines at
   every scale, and it IMPROVES with scale: 0.743 -> 0.776 -> 0.976. At 70B it is close to
   a perfect detector while self consistency sits at 0.492, i.e. exactly chance. The blind
   spot does not close with scale, it WIDENS: the bigger model is more detectable and the
   uncertainty baselines are no better at seeing it. This is the strongest single result in
   the project.
2. FAILED, in the most interesting way available. The prediction was that the 70B probe
   might rise above 0.6. Instead it fell to 0.227 -- far BELOW chance, with the interval
   clear of 0.5. Below chance is not noise, it is signal with the sign reversed. Reversed,
   the 70B probe scores 0.773 [0.712, 0.827] at overlap 0, and 0.681 / 0.736 at overlap 1
   and 2. At 3B and 8B the same reversal gives 0.494 and 0.543, i.e. nothing.
   Reading: at 70B, answering "YES the rule changed" goes with being RIGHT. The model that
   recognises the change has already updated its belief and answers correctly; the model
   that says "no change" has not and answers wrongly. So the probe does report something at
   70B -- it reports whether the belief has been updated, not whether it is stale. Claim 3
   assumed the opposite sign.
   Claim 3 is therefore SCALE DEPENDENT, not false: at chance below 70B, informative at 70B
   with the sign inverted. Claim 3' still stands, because the gate (0.976) still beats the
   reversed probe (0.773) at 70B, and the gate is free while the probe is not.
3. CLAIM 2 not yet scored at scale; cling analysis still to run on 3B and 70B.
4. FAILED. G0's inversion at overlap 2 was predicted to be structural and scale free.
   3B 0.342 and 8B 0.364 invert as before, but 70B is 0.592 -- above chance, no inversion.
   The mechanism is real but it is not scale free: at 70B post shift accuracy at overlap 2
   is 0.850, so there is far less clinging for the gate to invert on.
5. CONFIRMED. Raw contradiction density at overlap 2 falls with scale: 2.23 / 2.11 / 0.67.
   The 70B value is well under the 1.5 registered as the threshold for re-testing, which
   means the density SELECTOR that failed at 8B deserves a re-run at 70B before claim 5's
   second limit is called final.
6. FAILED as stated, and the failure is informative. Post shift accuracy at overlap 0 does
   not rise monotonically: 0.287 / 0.208 / 0.571. The 3B value sits near chance (0.333)
   because that model is close to guessing. The 8B value is BELOW chance, which is the
   phenomenon itself -- a model that clings to a dead rule does worse than random. So 8B
   clings hardest, 3B is too weak to have a belief to cling to, and 70B updates.

  gate comparison   3B                   8B                   70B
  G0 ov0            0.743                0.776                0.976
  G1 ov0            0.474                0.592                0.573
  G1 ov2            0.748                0.746                0.569

G1 stays the more stable gate at 3B and 8B, but at 70B G0 dominates everywhere and G1 adds
nothing. The G0 versus G1 tradeoff that claim 5 records as an open limit is largely an
artifact of small backbones.

### Next Session Should

Two things this result opens, in order.
1. Re-run the density selector at 70B. Prediction 5 held, so the reason it failed at 8B
   (ordinary model error polluting the count) is much weaker there.
2. Run the cling analysis on 3B and 70B to score prediction 3 and settle claim 2 at scale.

## Density selector at 70B: registered prediction (2026-08-20, BEFORE the run)

Prediction 5 of Stage 5 held: raw density at overlap 2 falls to 0.67 at 70B against 2.11 at
8B, because a more accurate model pollutes the count with far fewer ordinary slips. That is
the reason the selector failed at 8B, so it earns a re-run here.

But the Stage 5 gate table already suggests the answer will be anticlimactic. At 70B,
G0 is 0.976 / 0.753 / 0.592 and G1 is 0.573 / 0.605 / 0.569, so G0 dominates at every
overlap level. There may simply be nothing left to select between.

Registered:
(a) At 70B the selectors converge on "always G0" and land within 0.05 of G0 at every level.
(b) They succeed not because the selector became smart but because G0 stopped inverting.
    Whether the selector logic itself is any good remains untestable at 70B.
(c) If (a) and (b) hold, claim 5's limit 2 is DOWNGRADED from a general limit to a small
    backbone artifact, and must be restated that way rather than dropped.
(d) If instead a selector beats G0 at 70B, that is a genuine adaptive result and limit 2
    becomes a solved problem.

### Density selector at 70B: result (2026-08-20)

  gate              overlap 0            overlap 1            overlap 2
  G0 cling          0.976 [.953,.995]    0.753 [.715,.791]    0.592 [.551,.627]
  G1 contradicted   0.573 [.539,.609]    0.605 [.561,.654]    0.569 [.515,.632]
  G6 adaptive d>=3  0.573                0.605                0.569
  G8 adaptive c>=3  0.573                0.605                0.569
  G7 blend          0.835                0.582                0.333
  G9 blend          0.830                0.582                0.333

  silent on wrong   G0: 0.049 / 0.000 / 0.028      G1: 0.854 / 0.789 / 0.861

(a) FAILED, and it failed as the exact mirror of the 8B failure. The selectors did not
    converge on "always G0", they converged on "always G1": at 70B raw density is
    1.91 / 1.34 / 0.67, so a threshold of 3 is essentially never met and the gate falls
    through to G1 every time. At 8B density was too HIGH (polluted by ordinary error) and
    the same selectors picked G0 too often. Same fixed threshold, opposite failure, purely
    because backbone accuracy moved.
    That is the real verdict on contradiction density: the threshold is a function of the
    model's error rate, so it would have to be retuned per model. It is a tuned constant
    wearing the costume of a principled trigger, and it should be reported as such.
(b) Moot, since (a) failed.
(c) HOLDS, but by a different route than registered. Limit 2 does dissolve at 70B -- not
    because a selector works, but because G0 stops inverting (0.592, above chance) and
    dominates G1 at every overlap level. At scale there is simply nothing to select: use G0.
(d) FAILED. No selector beats G0 at 70B. The blends are worse, and G9 inverts at overlap 2
    (0.333) which is worse than either gate it is built from.

Also worth recording: at 70B, G0 is silent on 4.9 / 0.0 / 2.8 percent of wrong rows while
G1 is silent on 85.4 / 78.9 / 86.1 percent. G1 is not a weaker version of G0 at this scale,
it is close to useless, because a 70B model rarely repeats an already contradicted key.

### Revised position on claim 5, limit 2

Limit 2 stands, but narrower than written this morning. It is a SMALL BACKBONE limit: at 3B
and 8B, G0 inverts at high overlap, G1 is needed to cover that, and no free runtime signal
selects between them. At 70B the problem does not arise. The paper should say that, because
"no adaptive rule exists" and "no adaptive rule is needed at scale" are different claims and
only the second is supported once 70B is in the table.

### Claim 2 at scale (2026-08-20): censoring confirmed, and the 70B picture is the paper's figure

  model  ov  pre -> post acc    pre -> post agree   agree chg  min agree  cling            censored
  3B     0   0.658 -> 0.287     0.578 -> 0.557      -0.021     0.507      1.90 [1.20,2.63]  0.000
  3B     1   0.717 -> 0.375     0.598 -> 0.577      -0.022     0.533      1.83 [1.28,2.41]  0.033
  3B     2   0.708 -> 0.529     0.568 -> 0.576      +0.008     0.527      2.03 [1.20,3.00]  0.000
  8B     0   0.721 -> 0.208     0.638 -> 0.602      -0.037     0.540      3.10 [2.21,4.03]  0.033
  8B     1   0.725 -> 0.396     0.641 -> 0.638      -0.003     0.567      2.56 [1.85,3.33]  0.100
  8B     2   0.762 -> 0.588     0.641 -> 0.654      +0.013     0.613      3.48 [2.35,4.65]  0.233
  70B    0   1.000 -> 0.571     0.855 -> 0.807      -0.048     0.747      4.07 [3.00,5.29]  0.533
  70B    1   1.000 -> 0.683     0.866 -> 0.830      -0.036     0.780      4.88 [3.63,6.13]  0.733
  70B    2   1.000 -> 0.850     0.863 -> 0.839      -0.023     0.800      1.75 [1.25,2.00]  0.867

Stage 5 prediction 3 CONFIRMED at every scale. Group confidence never reaches 0.5 on any
model (minimum 0.507 at 3B, 0.540 at 8B, 0.747 at 70B), and agreement change stays inside
0.1 of zero everywhere (worst case -0.048). Confidence does not break after a rule shift at
any scale tested. Claim 2 stays folded into claim 1.

### The 70B row is the cleanest statement of the blind spot in the project

Pre shift accuracy is 1.000 -- the 70B model has the rule perfectly. After the shift it
falls to 0.571 while agreement moves 0.855 -> 0.807. Accuracy loses 0.43; confidence loses
0.048. A model that was perfect becomes wrong on nearly half the steps and reports almost
exactly the same confidence throughout. That is the figure the paper should lead claim 1
with, not the 8B version.

### Stop gate TRIGGERED at 70B

Claim 2's registered stop gate was: censoring above 0.5 at any level means cling time is
reported as censored rather than as a scalar. At 70B all three levels breach it
(0.533 / 0.733 / 0.867). So 70B cling time is CENSORED and the 4.07 / 4.88 / 1.75 figures
must not be quoted as scalars -- they are means over the shrinking minority of episodes
that dipped at all. The 1.75 at overlap 2 is the worst offender: 86.7 percent censored, so
it is a mean over roughly four episodes and it is lower than the others purely through
selection.

### A methodological problem this exposes, and it is the same one as the density threshold

The dip threshold is a fixed 0.5, but baseline agreement is not fixed: it is 0.578 at 3B,
0.638 at 8B, 0.855 at 70B. A 70B model would have to fall much further, in absolute terms,
to trip the same threshold, which is most of why its censoring is so high. So the fixed 0.5
is model dependent in exactly the way the density threshold turned out to be.

Not fixing it retroactively, because changing the threshold after seeing the results is
exactly the move the registration discipline exists to prevent. Recording it instead as a
design fault to correct in the NEXT registered run: a relative threshold (a fixed fraction
of that model's own pre shift agreement) is the honest version, and it should be registered
before it is run, with the fixed threshold numbers reported alongside for comparison.

---

## Stage 6, second testbed: design and registered prediction (2026-08-20, BEFORE the run)

The kill condition for the whole project: if the gate needs RuleShift's three cue structure
to be definable at all, Axon is a case study rather than a method. This stage tests that.

### Design: a fact update stream

A stream of questions about entities. Each entity has a current correct answer; the agent
learns the mapping only from reward, and partway through the stream some answers change.

Deliberately different from RuleShift in four ways, so that "it generalises" means something:

1. TWELVE entities instead of three cues, so belief is spread much thinner.
2. SIX possible answers instead of three, so guessing is weaker and the space is larger.
3. Items arrive with ZIPF frequency, not uniformly. RuleShift sampled cues uniformly, so
   the model's believed rule was always well estimated. Here, rare entities have almost no
   evidence behind their believed answer. This is the real stress test and the thing most
   likely to break the gate.
4. Natural language items ("Who leads Acme Corp?") rather than colour cues.

The environment emits exactly the same CSV columns as run.py, with `cue` holding the entity
name, so gates.py, contest.py, cling.py and leadtime.py all run against it unchanged. That
is deliberate: if the gate needs new code to work here, it did not generalise.

The gate definitions do not change at all:
  G0  chosen == mode of the agent's own past answers for this entity
  G1  this exact (entity, answer) pair has already earned reward 0

### Registered predictions

1. CLAIM 1 and CLAIM 3' GENERALISE. At 70B the gate beats self consistency and semantic
   entropy on the fact stream, interval clear of zero. THIS IS THE KILL TEST: if it does
   not, the detector is a RuleShift artifact and the paper has to say so.
2. G0 scores LOWER here than the 0.976 it reached on RuleShift at 70B, because Zipf
   sampling leaves thin evidence behind the believed answer for rare entities. Registered
   band: between 0.70 and 0.95. Below 0.70 counts as a partial failure of generalisation
   and must be reported as one.
3. The gate's accuracy is FREQUENCY DEPENDENT: split rows by how often their entity has
   been seen before, and AUROC on frequently seen entities should clearly exceed AUROC on
   rarely seen ones. This is the mechanism behind prediction 2 and it is what would need
   fixing in a deployed version.
4. G1 stays weak at 70B, as it was on RuleShift (0.573), because a 70B model rarely repeats
   an answer already shown to be wrong.

### Stage 6 result (2026-08-20): kill test PASSED, generalisation PARTIAL

30 episodes, 40 steps, shift at 20, 12 entities, 6 answers, zipf arrival, 70B.
n=300 scored rows in the post shift window.

  signal              AUROC [95% CI]
  G0 cling            0.644 [0.596, 0.685]
  G1 contradicted     0.589 [0.538, 0.635]
  unc_agreement       0.478 [0.393, 0.562]
  sem_entropy         0.481 [0.395, 0.564]

1. CONFIRMED, and this was the kill test for the whole project. The gate beats self
   consistency and semantic entropy on an environment that shares nothing with RuleShift
   but the CSV schema -- different item count, different answer space, non uniform arrival,
   natural language items. The intervals do not overlap. Axon is not a RuleShift artifact.
   Claim 1 and claim 3' generalise.
2. FAILED. The registered band was 0.70 to 0.95, and 0.644 falls below it. Registered in
   advance that this counts as a PARTIAL FAILURE OF GENERALISATION, so it is reported as
   one. The gate works here, but far less well than the 0.976 it reached on RuleShift at
   the same backbone.
3. CONFIRMED, cleanly, and it is the mechanism behind 2. Splitting rows by how many times
   that entity had been seen before:
     0-1 prior sightings (rare)    n=86   G0 0.534 [0.507, 0.566]   at chance
     2-4 prior sightings           n=110  G0 0.602 [0.563, 0.644]
     5+  prior sightings (frequent) n=104 G0 0.759 [0.631, 0.864]
   The gate is only as good as the belief it reads, and belief needs observations. On rare
   items it is at chance. This is the single most useful thing Stage 6 produced and it is a
   real deployment constraint, not a curiosity.
4. CONFIRMED. G1 stays weak at 70B (0.589 here, 0.573 on RuleShift).

### Why generalisation came out partial, and it is partly the testbed's fault

Pre shift accuracy is only 0.362, and each entity is seen a mean of 2.54 times before the
shift. With 12 entities, 6 answers and zipf arrival over a 20 step pre shift phase, the
agent never gets enough observations to FORM the belief that the gate is supposed to read.
The detector is being asked to detect staleness in a belief that barely exists.

So 0.644 is a lower bound on generalisation, not a clean measurement of it. The honest
reading: the gate transfers to a genuinely different environment (prediction 1, the part
that mattered), and the size of the transfer is confounded by a pre shift phase too short
for this item count.

## Stage 6b, longer pre shift phase: registered prediction (BEFORE the run)

Change ONE thing: pre shift phase from 20 steps to 60, holding everything else fixed
(12 entities, 6 answers, zipf, 70B, 30 episodes). Mean sightings per entity should rise
from about 2.5 to about 7.5, which is enough for a belief to form.

1. Pre shift accuracy rises well above the current 0.362. If it does not, the task is
   unlearnable as designed and Stage 6's numbers cannot be interpreted at all.
2. G0 rises into the originally registered 0.70 to 0.95 band. If it does, the partial
   failure was the testbed's short pre shift phase, not a limit of the detector, and
   generalisation is reported as clean with both runs shown.
3. If G0 does NOT rise above 0.70 even with belief formed, the partial failure is real and
   belongs to the detector. It would then be reported as an honest generalisation limit:
   the gate degrades on large, unevenly sampled item spaces.
4. The frequency effect persists in both runs: rare items stay near chance. This is
   predicted to be a permanent property, not something the longer phase fixes.

### Stage 6b result (2026-08-20): generalisation is CLEAN

Only the pre shift phase changed, 20 steps -> 60. Everything else held: 12 entities,
6 answers, zipf arrival, 70B, 30 episodes, n=300 scored rows.

                        6a (pre=20)          6b (pre=60)
  pre shift accuracy    0.362                0.636
  sightings per entity  2.54                 5.46
  G0 cling              0.644 [.596,.685]    0.805 [.777,.834]
  G1 contradicted       0.589 [.538,.635]    0.474 [.364,.580]
  unc_agreement         0.478 [.393,.562]    0.472 [.366,.574]
  sem_entropy           0.481 [.395,.564]    0.474 [.367,.576]

  G0 by prior sightings 6a                   6b
  rare  0-1             0.534 [.507,.566]    0.500 [.500,.500]
  mid   2-4             0.602 [.563,.644]    0.664 [.608,.721]
  freq  5+              0.759 [.631,.864]    0.899 [.870,.928]

1. CONFIRMED. Pre shift accuracy rose 0.362 -> 0.636, so the task is learnable and 6a's
   numbers were depressed by a pre shift phase too short for belief to form.
2. CONFIRMED. G0 reaches 0.805, inside the originally registered 0.70 to 0.95 band. The
   partial failure in 6a belonged to the TESTBED, not the detector. Generalisation is
   reported as clean, with both runs shown rather than only the flattering one.
3. Did not fire.
4. CONFIRMED, and sharper than in 6a. Rare items sit at exactly 0.500 -- chance, no signal
   at all -- while frequent items reach 0.899, approaching the 0.976 the gate reaches on
   RuleShift. The longer pre shift phase did not fix the rare item case, it just moved more
   rows into the frequent bucket (n=104 -> n=194). This is a permanent property of the
   detector, as predicted.

### What Stage 6 establishes

The gate transfers to an environment sharing nothing with RuleShift but the CSV schema:
four times the items, twice the answer space, non uniform arrival, natural language items.
It scores 0.805 there while self consistency and semantic entropy sit at 0.472 and 0.474,
i.e. exactly chance. Axon is a method, not a case study. This was the kill test and it
passed on both runs.

The real deployment constraint is now precisely stated and measured: THE GATE IS ONLY AS
GOOD AS THE BELIEF IT READS, and belief needs observations. On items seen 0-1 times it is
at chance by construction; on items seen 5+ times it is near ceiling. Anyone deploying this
needs a per item confidence floor, and should refuse to score items below it rather than
emit a coin flip.

G1 collapses to chance (0.474) at 70B on this testbed, consistent with its behaviour on
RuleShift at 70B: a strong model rarely repeats an answer already shown to be wrong, so a
contradiction gate has almost nothing to fire on.

---

## Stage 7, external benchmarks: design and registered prediction (2026-08-22, BEFORE the run)

Until now both environments were built by me. That is grading my own homework, and it is
the first thing a reviewer will say. TruthfulQA is independent, widely used, and was chosen
in EVALUATION.md precisely because it is built to bait confident false answers.

Source: sylinrl/TruthfulQA, 790 items, each with a Best Answer and a Best Incorrect Answer,
so it reduces to a two choice task with objective ground truth.

### Track A -- the benchmark unmodified

Ask each question once, k=5 samples, no repeats, no feedback, no shift. The gate CANNOT be
computed here and will not be faked: with no repeated items and no reward, there is no
belief to go stale. Track A tests only claim 1's PREMISE, on independent data.

### Track B -- TruthfulQA-stream (modified, and labelled as modified everywhere)

Real questions and real answer pairs, but presented as a repeated item stream with reward
feedback, and at the shift step the rewarded answer flips for a subset of questions. Same
shape as RuleShift and the fact stream, with benchmark content instead of synthetic content.
This is NOT TruthfulQA any more and must never be reported as if it were; it is TruthfulQA
content under a controlled rule shift.

### Registered predictions

Track A:
1. The uncertainty baselines do BETTER than chance here, roughly 0.55 to 0.70. Static
   confident errors are partly detectable; the claim was never that these tools are useless,
   only that they go blind specifically when a belief goes stale after a change. If they
   score at chance here too, claim 1 is stronger than stated. If they score above 0.75,
   claim 1's motivation weakens on independent data and that must be said plainly.
2. Gate reported as N/A, not as a number.

Track B:
3. THE REAL EXTERNAL TEST. The gate beats both uncertainty baselines on TruthfulQA-stream
   at 70B, interval clear of zero. If it does not, the detector does not survive contact
   with independent content and v0.2 fails its external check.
4. The gate scores LOWER than the 0.805 it reached on the fact stream, because these
   questions carry real model priors: the backbone may already believe the truthful answer
   and resist the flipped reward, which is a different failure mode from a synthetic mapping
   it learned from scratch. Registered band: 0.60 to 0.80. Below 0.60 counts as a partial
   failure on external content and is reported as one.
5. The frequency effect from Stage 6 reappears: items seen more often score better.

### Stage 7 result (2026-08-22): v0.2 FAILS its external check, and the reason is important

TRACK A -- unmodified TruthfulQA, 200 questions, 70B, accuracy 0.815

  unc_agreement   0.566 [0.495, 0.642]
  sem_entropy     0.566 [0.495, 0.642]
  gate            N/A, as registered

Prediction 1 CONFIRMED: baselines land at 0.566, inside the registered 0.55 to 0.70 band,
though the interval touches 0.5. So the uncertainty tools are weakly informative on static
confident errors. That is the honest framing of claim 1's motivation on independent data:
they are not useless in general, they are weak, and the claim about going blind belongs
specifically to belief staleness after a change.

TRACK B -- TruthfulQA-stream (MODIFIED), 30 episodes, n=300, pre acc 0.901, post acc 0.527

  G0 cling        0.476 [0.446, 0.504]      BELOW CHANCE
  G1 contradicted 0.621 [0.575, 0.665]
  unc_agreement   0.503 [0.469, 0.540]
  sem_entropy     0.503 [0.469, 0.540]

  by prior sightings   mid 2-4  0.500 [0.500, 0.500]    freq 5+  0.478 [0.444, 0.511]

Prediction 3 FAILED, and it was written as the pass/fail condition for the whole stage:
"the gate beats both uncertainty baselines... if it does not, the detector does not survive
contact with independent content and v0.2 fails its external check." G0 does not beat them.
It sits at 0.476, below chance and below the baselines. V0.2 FAILS ITS EXTERNAL CHECK.

Prediction 4 FAILED, and worse than its own failure band. The registered band was 0.60 to
0.80 with below 0.60 called a partial failure; 0.476 is not partial.

Prediction 5 FAILED. No frequency effect at all: 0.500 at 2-4 sightings, 0.478 at 5+. On
the fact stream this was the strongest regularity in the project (0.500 -> 0.899). It does
not appear here.

### Why G0 breaks, and this is the real contribution of Stage 7

Registered prediction 4 named the mechanism in advance, and the data confirms it. Pre shift
accuracy is 0.901: the 70B model already KNOWS these answers. Its belief about a TruthfulQA
item does not come from in-context learning, it comes from pretraining.

G0 asks whether the agent is still answering the key its own PAST ANSWERS say it believes.
When the belief is a pretrained prior, that is true almost everywhere -- the model keeps
giving the truthful answer regardless of what reward says -- so G0 fires on nearly every row
and carries no information. Since only half the items flipped, continuing to answer the
truthful one is correct about half the time, which is exactly the 0.476 observed.

  G0 needs the belief to have been LEARNED IN CONTEXT. Where the belief is a pretrained
  prior that the agent will not revise, the gate has nothing to measure.

G1 survives at 0.621, clear of the baselines, because it is grounded in OBSERVED REWARD
rather than in inferred belief: it only asks whether this exact (item, answer) pair has
already been punished. That does not care where the belief came from.

### What this does to the claims

This reverses part of the v0.2 story and the reversal has to be carried into the paper.

- CLAIM 3' (the cling gate is the detector, and it is free) does NOT generalise to content
  carrying strong pretrained priors. It holds on RuleShift and on the fact stream, both of
  which teach the mapping in context. It fails on TruthfulQA-stream.
- G1, which v0.1 and v0.2 had written off as the weaker gate (0.573 at 70B on RuleShift,
  0.474 on the fact stream), is the ONLY signal that works on all three environments. The
  "no fixed gate wins everywhere" finding from claim 5 is now much stronger, and its shape
  has changed: it is not overlap that decides which gate to use, it is WHERE THE BELIEF
  CAME FROM.
- Claim 1 survives in weakened form on independent data: baselines are weak (0.566) but not
  blind on static errors.

This is what the external benchmark was for and it did its job on the first run.

## Verifying the G0 failure diagnosis (2026-08-22, registered BEFORE the run)

The claim made after Stage 7 was that G0 fails on TruthfulQA-stream because the belief is a
PRETRAINED PRIOR rather than learned in context. That is a hypothesis, not a measurement,
and it is load bearing for the whole v0.3 plan, so it gets tested before anything is built
on it. Free: runs on traces already collected.

Test. For each item, compute its PRE SHIFT accuracy within its own episode -- how often the
agent already answered that item correctly before any rule change. High pre shift accuracy
means the model already knew it, i.e. a prior. Low means it had to learn it from reward.
Then score G0 separately in each bucket.

Registered predictions:
1. G0 is at or BELOW chance on high pre shift accuracy items (already known, prior driven).
2. G0 is clearly ABOVE chance on low pre shift accuracy items (had to be learned in context).
3. If G0 is the same in both buckets, the diagnosis is WRONG and the real cause is something
   else -- most likely the two choice format, since a binary answer space makes "still
   answering the believed key" much less informative than the 3 or 6 way spaces used before.
   That alternative must then be tested instead.

### Diagnosis verification (2026-08-22): the pretrained prior story is WRONG, and the Stage 7 comparison was CONFOUNDED BY MY OWN SETUP

Splitting Track B rows by each item's pre shift accuracy in its own episode:

  LOW pre-acc  (had to learn it)      n=18    G0 0.331 [0.125, 0.542]
  MID                                 n=53    G0 0.434 [0.331, 0.534]
  HIGH pre-acc = 1.0 (already knew)   n=221   G0 0.500 [0.500, 0.500]

Prediction 2 said G0 would be clearly ABOVE chance on items learned in context. It is 0.331,
BELOW chance -- the opposite. So the pretrained prior explanation is refuted by its own test.
The 0.500 in the high bucket is degenerate rather than informative: G0 is constant there
(the agent always answers its believed key), so there is nothing to rank and AUROC is exactly
0.5 by construction.

Registered prediction 3 fired, and chasing the alternative found something worse than a bad
hypothesis -- a setup error of mine:

  external.py    changed_frac default 0.5
  factstream.py  changed_frac default 1.0
  RuleShift ov0  all cues change, i.e. 1.0

So TruthfulQA-stream was run at a HALF shift while both environments it was compared against
ran at a FULL shift. Lining the numbers up by fraction of items shifted:

  100 percent shifted   RuleShift ov0   0.976
  100 percent shifted   fact stream     0.805
   67 percent shifted   RuleShift ov1   0.515
   50 percent shifted   TruthfulQA-str  0.476
   33 percent shifted   RuleShift ov2   0.364

TruthfulQA-stream sits exactly on claim 5's inversion curve. The "external failure" is not a
new phenomenon at all: it is the ALREADY DOCUMENTED partial shift inversion, observed at the
shift fraction I happened to configure. I then attributed it to pretrained priors, wrote that
into the claim file and the version file, and downgraded claim 3' on the strength of it.

That was wrong and the retraction is recorded here rather than quietly edited away. What
Stage 7 actually established so far is only Track A: the uncertainty baselines are weak
(0.566) but not blind on static confident errors.

The external check has NOT yet been run as a like for like comparison. Re-running
TruthfulQA-stream at changed_frac=1.0 to match the other two environments.

Registered prediction for the re-run:
1. At a full shift, G0 on TruthfulQA-stream scores clearly above chance, in the 0.70 to 0.90
   region, in line with the fact stream's 0.805.
2. If it does, the pretrained prior story is dead, the external check PASSES, and claim 3'
   goes back to VALIDATED with no scope condition.
3. If G0 still fails at a full shift, then there IS something about independent content that
   breaks it, and the scope condition returns -- but earned this time rather than assumed.

### Stage 7b result (2026-08-22): full shift re-run

  changed_frac        0.5 (old, confounded)        1.0 (matched to other envs)
  pre acc             0.901                        0.899
  post acc           0.527                        0.087
  G0 cling            0.476 [0.446, 0.504]         0.628 [0.545, 0.723]
  G1 contradicted     0.621 [0.575, 0.665]         0.186 [0.135, 0.251]
  unc_agreement       0.503 [0.469, 0.540]         0.347 [0.248, 0.442]
  sem_entropy         0.503 [0.469, 0.540]         0.347 [0.248, 0.442]

1. FAILED. G0 was predicted into 0.70 to 0.90 and came in at 0.628. Above chance with the
   interval clear of 0.5, and clearly ahead of the baselines at 0.347 with no overlap, but
   below the registered band and well below the fact stream's 0.805.
2. The pretrained prior story is DEAD, as it deserved to be. G0 recovers as soon as the shift
   fraction matches the other environments, so the Stage 7 result was a confound of my own
   making and not a property of independent content. Claim 3's downgrade is retracted.
   But the external check passes in a weaker form than predicted: the gate WORKS on
   independent content (0.628, beating baselines decisively) while being materially weaker
   there than on either synthetic environment.
3. Partly fired: there IS something about this content that costs G0 roughly 0.18 relative
   to the fact stream at the same shift fraction. Most likely the binary answer space -- with
   two options, "still answering the believed key" is a much coarser signal than it is over
   three or six. That is a hypothesis and is NOT being written into the claims until tested.

### The strongest claim 1 evidence in the project, and it was nearly missed

At a full shift the uncertainty baselines score 0.347, well BELOW chance with the interval
clear of 0.5. They are not merely blind here, they are ACTIVELY MISLEADING: the model holds
its pretrained answer with high agreement while being wrong, so low uncertainty predicts
wrongness. Post shift accuracy is 0.087, i.e. the agent is wrong on more than nine steps in
ten while looking confident. That is the blind spot in its strongest observed form, and it
is on independent benchmark content.

### G1 inverts in a binary answer space

G1 falls to 0.186, far below chance. With only two options, once an answer has been
contradicted the agent switches to the other one -- which at a full shift is the correct one.
So "this pair was already punished" predicts RIGHT rather than wrong. G1's promotion to
"the general gate", written after Stage 7, is also retracted: it was an artifact of the same
confounded half shift run.

Net position after the retraction: G0 remains the detector, now shown to work on independent
content as well, and the honest caveat is that it is weaker there (0.628) than on synthetic
environments (0.805, 0.976). Neither gate is a general winner and the reason is still shift
fraction plus answer space, exactly as claim 5 already said.

### HotpotQA (2026-08-22): DEGENERATE, numbers not interpretable, re-run required

  track A (unmodified)   n=200, 1 wrong      accuracy 0.995
  track B (stream, full shift)  n=300, 299 wrong / 1 right
     G0 0.995   G1 0.654   unc_agreement 0.002   sem_entropy 0.002

These numbers are NOT being reported as results. AUROC computed on 1 positive against 299
negatives carries no information, and the same applies to track A with 1 wrong answer in 200.
G0's 0.995 would look like the best result in the project and it means nothing.

Cause, and it is mine again: the distractor. TruthfulQA ships a DESIGNED Best Incorrect
Answer, which is why it produced a usable spread (pre 0.899, post 0.087). HotpotQA ships no
wrong answer, so external.py builds one by taking another question's answer of similar
length. For a 70B model that is trivially rejectable -- "Clarence Nash" against "Ian Fleming"
for a question about a voice actor is not a real choice -- so pre shift accuracy pins at
0.997 and, once the reward flips, post shift accuracy pins at 0.003. Every row falls in one
class and there is nothing left to discriminate.

The fix is harder distractors. Re-running restricted to HotpotQA's YES/NO questions, where
the two options are forced, equally well formed, and cannot be rejected on shape. That is a
genuine two choice task rather than a constructed one.

Registered before the re-run:
1. Pre shift accuracy lands well below 0.99, giving both classes real mass. If it is still
   above about 0.95 the item type is still too easy and HotpotQA gets reported as unusable
   for this design rather than forced.
2. Given a usable spread, G0 beats the uncertainty baselines with no interval overlap, as it
   did on TruthfulQA-stream at a full shift (0.628 against 0.347).
3. No prediction is made about G0's absolute value. TruthfulQA gave 0.628 and the fact stream
   0.805; a yes/no space is narrower than either, so it could land below both.

### TreeCut (2026-08-22): track A usable, track B underpowered

  TRACK A (unmodified, answerable half)  n=200, 104 wrong, accuracy 0.480
     unc_agreement  0.445 [0.375, 0.514]
     sem_entropy    0.445 [0.375, 0.514]

  Clean and well balanced -- a genuine two choice task where the model is near chance. Both
  uncertainty baselines sit AT chance with the interval straddling 0.5: they cannot tell a
  right answer from a wrong one on TreeCut math. Second independent confirmation of claim 1's
  premise, and stronger than TruthfulQA's track A (0.566, weakly informative).

  TRACK B (stream, full shift)  n=300, 292 wrong, 8 right, pre 0.900, post 0.027
     G0 0.660 [0.474, 0.851]   G1 0.463 [0.272, 0.651]   baselines 0.259 [0.070, 0.442]

  NOT a result. Eight rows in the minority class, and G0's interval straddles 0.5. The point
  estimate is in the right place and consistent with TruthfulQA's 0.628, but it is
  underpowered and must not be quoted as support.

### The methodological problem this exposes, across all three external benchmarks

Post shift accuracy at a full shift: TruthfulQA 0.087, TreeCut 0.027, HotpotQA 0.003.

When the backbone reliably knows the answer, flipping EVERY item drives post shift accuracy
to zero, and the "still correct" class disappears. AUROC then has almost nothing to rank.
That is the opposite failure from the original half shift run, which had good balance
(TruthfulQA post 0.527) but sat on claim 5's inversion curve.

So neither single setting is right for external content:
  changed_frac = 1.0   matched to the synthetic environments, but classes collapse
  changed_frac = 0.5   balanced, but confounded with the documented partial shift inversion

The fix is to stop picking one point. External benchmarks should be run as a SHIFT FRACTION
SWEEP, the same way RuleShift was run as an overlap sweep, and the whole curve reported. That
is both comparable to claim 5's existing curve and immune to the class collapse, because some
point on the sweep will always have usable balance.

This is now the blocking design decision for Stage 7 and should be settled before any more
external runs.

### HotpotQA yes/no re-run (2026-08-22): still degenerate, confirms rather than fixes

  track A   n=200, 9 wrong, acc 0.955   baselines 0.537 [0.468, 0.672] -- underpowered, not
            reported as a result (fewer than the ~15 wrong rows needed for a usable interval)
  track B   n=300, 293 wrong, 7 right   -- degenerate, same as the constructed distractor run

Restricting to yes/no fixed the DISTRACTOR problem (both options are now genuinely equal
shape) but not the CLASS BALANCE problem, because that problem was never about the
distractor. It is about changed_frac=1.0 combined with a backbone that converges to near
perfect accuracy on repeated items with reward feedback. Confirms the diagnosis from the
TreeCut run rather than fixing anything, as predicted.

## Calibrating shift fraction before the real sweep (2026-08-22)

Rather than pick another point and hope, running a CHEAP one seed probe per benchmark across
several changed_frac values (k=3, no bootstrap, just the resulting post shift accuracy) to
find where each benchmark actually lands near 50 percent, before spending the full 30 seed
budget on it.

Registered: pre shift accuracy in the stream format is well above each benchmark's track A
accuracy (TreeCut track A 0.480 vs track B pre 0.900), because repeated exposure plus reward
feedback lets a weak one shot ability get bootstrapped to near ceiling. So the fraction
needed for balance is expected to be LOWER than 0.5, not higher, on both remaining
benchmarks.

### Calibration result (2026-08-22)

  changed_frac   post-shift wrong (n=30, 1 seed, k=3, both TreeCut and HotpotQA)
  0.15                  0.033
  0.30                  0.167
  0.50                  0.333
  0.70                  0.433
  0.85                  0.733
  1.00                  1.000

Both benchmarks landed on near identical counts at each fraction (verified the underlying
CSVs are genuinely different runs, not a caching artifact -- coincidence at small n).
0.70 is the best balance point available: 43 percent wrong, comfortably inside a scorable
range, well short of TreeCut track B's earlier 8-row minority class problem.

Registered before the full run: at changed_frac=0.70, full 30 seed budget, both TreeCut and
HotpotQA (yes/no) produce a usable class split (at least 20 percent minority class at n=300),
and G0 beats the uncertainty baselines with the interval clear of zero, consistent with
TruthfulQA-stream's 0.628 at a comparable non degenerate setting. Also running TruthfulQA at
0.70 to complete a 3 point shift fraction curve (0.5, 0.7, 1.0) that all three benchmarks
share, comparable in shape to claim 5's overlap curve.

### Stage 7c result (2026-08-22): the shift-fraction crossover replicates on THREE independent benchmarks

All three at changed_frac=0.7, n=300, 70B, balanced classes (110-114 in the minority):

  benchmark              pre     post    G0 cling              G1 contradicted        baselines
  TreeCut                0.902   0.367   0.494 [.468,.521]     0.644 [.610,.678]      0.504
  HotpotQA yes/no        0.985   0.370   0.524 [.504,.548]     0.633 [.596,.670]      0.481
  TruthfulQA             0.906   0.380   0.521 [.493,.551]     0.602 [.557,.646]      0.505

G0 sits AT CHANCE on all three (0.494-0.524, every interval straddles or nearly straddles
0.5). G1 clearly beats both G0 and the baselines on all three, with no interval overlap
against baselines on any of them (0.60-0.64 vs 0.48-0.51).

This is not a new phenomenon. It is claim 5's overlap mechanism, confirmed for the first
time outside RuleShift: G0 depends on ALL relevant cues having shifted, and degrades toward
chance the moment some fraction of items keep their old answer, because for those items
"still answering the old belief" is still correct. changed_frac=0.7 IS a partial shift
condition in exactly RuleShift's sense (30 percent of items unchanged), and G0 behaves
exactly as RuleShift predicted it would (compare RuleShift ov1 at 8B: G0 0.515, almost
identical to these three benchmarks' 0.49-0.52).

Combined with the full shift numbers already measured (TruthfulQA-stream f=1.0: G0 0.628,
G1 0.186 -- inverted the other way), there is now a clean crossover on independent content,
matching the crossover already documented on RuleShift:

  shift fraction    which gate wins                 where measured
  full (1.0)        G0                               RuleShift ov0 (0.976), fact stream
                                                      (0.805), TruthfulQA-stream (0.628)
  partial (0.7)     G1                               TreeCut, HotpotQA, TruthfulQA, all
                                                      three independently, all in the same
                                                      direction

### What this settles and what it reopens

SETTLED: claim 5's shift fraction mechanism is not a RuleShift artifact. It reproduces on
three independent benchmarks with completely different content, distractor construction and
domain. This is the strongest confirmation of claim 5 in the project and belongs in the
paper as cross domain evidence, not just cross model evidence.

REOPENED: the runtime selector question from claim 5, limit 2. That limit was narrowed to
"a small backbone artifact" after the 70B overlap sweep showed G0 stops inverting at 70B on
RuleShift. These three benchmarks are ALSO at 70B and G0 sits at chance there, not above it.
So the earlier narrowing was specific to RuleShift's own overlap structure (three cues, one
shifts at ov2) and does not transfer to real content at a comparable partial shift fraction.
Limit 2 has to be restated again: NOT solved by scale alone. The scale finding and the
external finding both have to be reported, because they point in different directions and
resolving that is real remaining work, not a rounding error.

---

## New mechanisms, M3-M6: design and registered predictions (2026-08-22, BEFORE any run)

v0.2's open problem: G0 (M1, cling) wins at full shift, G1 (M2, contradiction) wins at
partial shift, and six selector variants (all built from CONTRADICTION COUNT) failed to pick
between them. Four new mechanisms, each measuring something G0/G1 do not:

  M3  velocity        rate of NEW contradictions per step, not their total count. G0/G1's
                       selectors all failed as static tallies; velocity asks how FAST the
                       world is contradicting the agent, which a static count cannot see.

  M4  cross item       what fraction of OTHER items (not this one) have been contradicted
      consensus        recently. G0 and G1 both look only at the item being answered right
                       now; this is the first mechanism that looks at the REST of the
                       episode to judge whether THIS answer should be trusted.

  M5  soft blend       score = G0 * G1 directly, no threshold, no selector logic at all.
                       Untested: only THRESHOLD-GATED combinations of G0/G1 were tried
                       before (G4 through G9), never a plain product.

  M6  agreement drop   compare CURRENT branch agreement (the k-sample vote spread already
                       computed by run.py) against that item's own PAST agreement. A drop
                       in agreement is the model getting less sure about ITS OWN answer,
                       independent of reward. Free: agreement is already in every trace.

All four are deterministic, free (zero model calls), and computed only from strictly
earlier rows -- same discipline as G0-G9.

### Registered predictions

1. M3 (velocity) beats M1/M2's selectors at telling full shift from partial shift, because
   it is the first mechanism to measure SPEED rather than COUNT. Predicted: on RuleShift,
   velocity in the first 3 post-shift steps is higher at overlap 0 than at overlap 2.
2. M4 (cross item consensus) is the strongest candidate for the actual missing selector,
   because it does not depend on THIS item's own history at all, which is exactly what
   failed to generalise from RuleShift's 3-cue structure to real benchmarks. Predicted:
   M4 beats G0 at partial shift and does not invert, matching G1's flatness, while also
   beating G1 at full shift by reacting faster (G1's known weakness).
3. M5 (soft blend) is predicted to fail, registered explicitly so a negative result here
   is not silently dropped: multiplying two signals that fire on opposite conditions
   (G0 high exactly where G1 is likely low, and vice versa) should produce a MIDDLING score
   that beats neither, similar to the G7/G9 blends that already failed.
4. M6 (agreement drop) is the weakest prior of the four. Branch agreement was already shown
   in claim 2 to be nearly flat after a shift (change -0.037 to -0.048 across scales), so a
   signal built from ITS OWN drop is predicted to be WEAK, comparable to the uncertainty
   baselines it is meant to beat (around 0.45-0.55), not a real improvement.

### Kill conditions, stated in advance
M3: if velocity does not separate overlap 0 from overlap 2 in the first 3 steps, the
mechanism has no signal and is dropped without a selector test.
M4: if it inverts the same way G0 does, cross item information does not help and the
missing-selector problem is restated as unsolved rather than papered over.

## M3-M6 result (2026-08-22)

  gate                overlap 0            overlap 1            overlap 2
  G0 cling            0.776 [.721,.827]    0.515 [.452,.577]    0.364 [.302,.428]
  G1 contradicted     0.592 [.517,.668]    0.748 [.698,.796]    0.746 [.691,.798]
  M3 velocity         0.397 [.318,.478]    0.498 [.430,.570]    0.433 [.361,.502]
  M4 cross item       0.497 [.428,.571]    0.418 [.356,.480]    0.339 [.279,.400]
  M5 soft blend       0.634 [.578,.686]    0.682 [.638,.728]    0.637 [.591,.687]
  M6 agreement drop   0.485 [.398,.569]    0.515 [.442,.584]    0.576 [.513,.644]

Prediction 1 (M3 velocity separates full from partial shift) CONFIRMED, but not as a
wrongness detector -- as a SELECTOR SIGNAL. Mean velocity in the first 3 post-shift steps:
0.448 at overlap 0, 0.289 at overlap 2. M3's own AUROC as a detector is poor (0.40-0.50),
which is expected: velocity answers "how broad is the shift", not "is this row wrong". The
two questions are different and M3 was never meant to answer the second one.

Prediction 2 (M4 cross item) FAILED, kill condition triggered. It inverts even harder than
G0 (0.497 -> 0.418 -> 0.339 against G0's 0.776 -> 0.515 -> 0.364). Cross item information
does not help; DROPPED, no further testing.

Prediction 3 (M5 soft blend fails) WRONG, and interestingly wrong. It is not middling in
the way predicted -- it is the first blend tested that NEVER INVERTS: 0.634 / 0.682 / 0.637,
against G7's 0.782 / 0.582 / 0.453 (which inverts) and G9's 0.697 / 0.688 / 0.671 (does not
invert, similar shape, but built from a threshold and a tuned constant). M5 needs neither.
Genuinely useful "never worst" result, PROBE-adaptive-ablation-shaped, achieved with zero
free parameters.

Prediction 4 (M6 agreement drop, weak) CONFIRMED. 0.485 / 0.515 / 0.576, all within the
predicted chance-like band, no interval clearly clear of 0.5. Comparable to the uncertainty
baselines it was meant to beat. DROPPED as a standalone signal.

### M7: velocity as a genuine selector, registered before testing

M3 cannot detect wrongness but DOES separate shift breadth. That is exactly what a selector
needs, and it is a different kind of signal from every selector tried before (density,
confirmed density -- all static counts). Test: M7 = G0 if velocity(3 step window) >= 0.35
else G1. Threshold picked from the midpoint of the two means just measured (0.448, 0.289).

Registered:
1. M7 beats every prior selector (G6, G8) at overlap 2, because it is choosing based on
   shift speed rather than a count that was shown to be confounded by ordinary model error.
2. M7 does not fully match G1's flat 0.75 at overlap 1/2, because velocity is noisier early
   in a short window and will sometimes pick G0 incorrectly.
3. If M7 still inverts at overlap 2, velocity is dead as a selector too, and the missing
   selector problem is reported as fully unsolved rather than partially addressed.

### M7 result (2026-08-22)

  gate                     overlap 0            overlap 1            overlap 2
  M7 velocity selector     0.721 [.664,.774]    0.620 [.560,.682]    0.616 [.552,.678]
  (for comparison)
  G6_adaptive_d2           0.755                0.518                0.358 (inverts)
  G6_adaptive_d3           0.673                0.627                0.654
  G8_adaptive              0.596                0.748                0.746

Prediction 1 (beats every prior selector at overlap 2) PARTIALLY FAILED. M7 beats G6_d2
(0.616 vs 0.358, which inverts) but LOSES to G6_d3 (0.654) and to G8_adaptive (0.746, which
is really just G1 in disguise -- confirmed density almost never reaches its threshold at 8B,
so G8 defaults to G1 nearly everywhere and is not a real selector achievement here).

Prediction 2 (does not fully match G1's flat 0.75) CONFIRMED: gap of about 0.13 at both
overlap 1 and 2.

Prediction 3 (does it invert) -- NO, and this is the genuine result: 0.721 / 0.620 / 0.616,
never below 0.5, never worst. First selector built from a signal OTHER than a static
contradiction count, and it does not invert. But it does not dominate either: it trades
some of G0's overlap 0 strength and some of G1's overlap 1/2 strength for a flatter,
never-inverting curve, the same shape M5 has by a different route.

### Where the missing-selector problem stands after M3-M7

Two genuinely new, non-inverting candidates exist and neither dominates:
  M5 soft blend (G0 * G1)     0.634 / 0.682 / 0.637   closer to G1 at partial shift
  M7 velocity selector        0.721 / 0.620 / 0.616   closer to G0 at full shift

Neither beats picking the RIGHT gate for the situation (G0 at overlap 0, G1 at overlap 1/2),
which remains the best possible score at every level individually. The honest position is
unchanged in substance but improved in character: earlier selectors (density-based) either
inverted or degenerated into "always G1". These two do neither. The missing-selector problem
is now "no selector dominates" rather than "every selector inverts or collapses" -- real
progress, not yet a solution.

M3, M5, M7 carried forward as candidates to test on the external benchmarks (where the
shift-fraction crossover was independently confirmed). M4 and M6 dropped per their kill
conditions.

---

## M8: bimodal split, a genuinely new signal type (2026-08-22, registered BEFORE the run)

Every mechanism tried so far (M1, M2, M3, M4, M6) uses history ACROSS steps: past answers,
past rewards, past agreement. M5 combines two of those. None looks at the SHAPE of the
current step's own k-sample vote distribution beyond a single scalar (agreement, entropy) --
which was already shown in claim 2 to barely move after a shift and is why M6 died.

M8: within the current step's k branch samples, is the RUNNER-UP answer (second most common
vote, if any) equal to the item's own believed OLD key, while the CHOSEN answer is something
else? That is a directly observable sign of live internal conflict between an old belief and
an emerging new one -- votes split between two candidates rather than clustered on one -- and
it is structurally different from every prior mechanism: it needs no history at all beyond
the single believed_rule() lookup already used by G0, and it is computed entirely from ONE
step's branches column.

Free, zero model calls, uses only the branches column and believed_rule().

### Registered predictions

1. M8 fires MORE at partial shift than at full shift, because a full shift replaces the old
   key everywhere at once (the old key stops appearing in samples at all, so there is no
   runner-up to detect), while a partial shift leaves the old key alive as a live competitor
   for the items that did not change, producing genuine split votes on the ones that did.
   This is the opposite pattern from G0's own AUROC (which is highest at full shift), so if
   confirmed it makes M8 structurally complementary rather than a third variant of the same
   idea.
2. M8 alone is a WEAK direct predictor of wrongness (comparable to M3's 0.40-0.50), because
   like M3 it measures shift character rather than the current answer's correctness. This is
   registered so a low standalone AUROC is not treated as a failure without checking whether
   it works as a selector, same as M3 did.
3. KILL CONDITION: if M8 fires at the SAME rate regardless of shift breadth, it carries no
   information distinct from noise in the vote distribution, and is dropped without a
   selector test.
4. If predictions 1-2 hold, M8 is tested as a selector (M9): trust G1 when M8 fires (live
   conflict = better to wait for confirmed contradiction), trust G0 otherwise. Predicted to
   perform comparably to M7 (0.72 / 0.62 / 0.62) since it targets the same underlying
   variable (shift breadth) through a different measurement.

### M8/M9 result (2026-08-22): FAILS, and the fifth-mechanism search stops here

  M8 fire rate       overlap 0: 0.300     overlap 1: 0.204     overlap 2: 0.250
  M8 standalone AUROC  0.285 [.214,.359]   0.477 [.424,.529]   0.580 [.522,.638]
  M9 selector (G1 if M8 fires else G0)
                     0.752 [.681,.818]    0.577 [.519,.636]    0.435 [.375,.494]

Prediction 1 FAILED, and backwards: M8 was predicted to fire MORE at partial shift (the old
key staying alive as a competitor). It actually fires MOST at full shift (0.300 vs 0.204 and
0.250). The mechanism does not track what it was designed to track.

Prediction 2 (weak standalone) technically held at overlap 0 (0.285) but the pattern across
overlap is not what a shift-breadth signal should look like -- it rises with overlap the way
G1 does, not the way a bimodality-tracks-conflict story would predict.

Prediction 3's kill condition was "fires at the same rate regardless of breadth" -- the rates
are not identical, so the letter of the kill condition did not trigger, but the direction is
backwards from the design, which is arguably worse: a selector built on it does not fail
silently, it actively misleads.

Prediction 4 FAILED. M9 was predicted comparable to M7 (0.72/0.62/0.62). It matches at
overlap 0 (0.752) but INVERTS at overlap 2 (0.435 < 0.5) -- the exact failure mode every
density-based selector already had. M8/M9 DROPPED.

### The fifth-mechanism search stops here, as agreed before it started

The plan going in was explicit: try one genuinely new signal type, and if it fails, stop
adding mechanisms rather than keep searching. M8 was a different signal type (vote shape
within one step, not history across steps) and it failed on its own terms. Per that
agreement, no M10 is being designed. Axon's mechanism count stays at FOUR: M1 (cling), M2
(contradicted), M3/M7 (velocity, used as a selector), M5 (soft blend). The missing-selector
problem is reported as-is: two non-inverting candidates, neither dominant, no adaptive
solution found after eight attempts across two search rounds.

---

## Testing all four mechanisms on the external benchmarks (2026-08-22, registered BEFORE scoring)

M3/M7 and M5 were only ever tested on RuleShift. Registered concern already on record: any
selector found there risks being fit to RuleShift's 3-cue structure. Scoring both against
every external benchmark trace already collected -- zero new API calls, all traces exist
from Stage 7.

Coverage: TruthfulQA at f=1.0 (clean, from the retraction re-run) and f=0.7 (calibrated).
TreeCut and HotpotQA only at f=0.7, since their f=1.0 runs were underpowered/degenerate and
were never reported as results.

### Registered predictions
1. M7 (velocity selector) reproduces its RuleShift shape on TruthfulQA specifically, because
   it is the only benchmark with both a full-shift and a partial-shift point collected: closer
   to G0 at f=1.0, closer to G1 at f=0.7, never inverting at either.
2. M5 (soft blend) never inverts on any of the three benchmarks at f=0.7, matching its
   RuleShift behaviour (0.634/0.682/0.637, all clear of 0.5).
3. Neither M3/M7 nor M5 beats picking the correct gate for the situation on any benchmark --
   this is not expected to be resolved by testing on new content, since the underlying
   problem (the selector needs information about shift breadth that arrives too late) is
   structural, not a RuleShift artifact.

### Result: M7's threshold does not transfer; M5 breaks at full shift on real content

  benchmark            n     G0                    G1                    M5 blend              M7 velocity
  TruthfulQA f=1.0    300   0.628 [.545,.723]     0.186 [.135,.251]     0.302 [.214,.399]     0.507 [.424,.602]
  TruthfulQA f=0.7    300   0.521 [.493,.551]     0.602 [.557,.646]     0.623 [.583,.662]     0.559 [.501,.617]
  TreeCut    f=0.7    300   0.494 [.468,.521]     0.644 [.610,.678]     0.641 [.607,.676]     0.561 [.502,.622]
  HotpotQA   f=0.7    300   0.524 [.504,.548]     0.633 [.596,.670]     0.651 [.619,.684]     0.579 [.520,.637]

Prediction 1 FAILED, and this is the concern registered before the run materialising exactly.
M7's threshold (velocity >= 0.35) was calibrated from RuleShift's own mean velocities (0.448
at overlap 0, 0.289 at overlap 2). On TruthfulQA at full shift it does not track toward G0 at
all -- it lands at 0.507, indistinguishable from chance, far below G0's own 0.628. Item pool
size, step structure and paraphrase design all differ from RuleShift, so the raw velocity
number does not mean the same thing in a different environment. M7 is tuned to RuleShift and
does not transfer as constructed.

Prediction 2 HELD at f=0.7: M5 does not invert on any of the three benchmarks there (0.623 /
0.641 / 0.651, all comfortably above 0.5). But at TruthfulQA's f=1.0 point -- not covered by
the registered prediction, which only spoke to f=0.7 -- M5 COLLAPSES to 0.302, well below
chance. Mechanism: M5 = G0 * G1, and at full shift G1 is itself badly inverted on this
benchmark (0.186). Multiplying by an already-inverted G1 does not cancel the inversion, it
compounds it. M5's RuleShift-observed robustness (never inverting at any of the three
overlap levels) does not generalise to a benchmark where ONE of its two ingredients is itself
badly broken.

Prediction 3 CONFIRMED. Neither M5 nor M7 beats picking the correct single gate for the
situation on any benchmark tested (G0 at full shift, G1 at partial shift both individually
outperform both combinations at their respective settings, TreeCut/HotpotQA's M5 being the
only near-tie and even there the CIs overlap heavily).

### What this means for v0.3

Both surviving "never worst on RuleShift" candidates fail that same property once tested
outside RuleShift: M7's threshold does not transfer at all, and M5's product construction
inherits whichever ingredient gate is currently broken rather than averaging the damage away.
"Never worst" was a RuleShift-specific finding, not a property of the mechanisms themselves.

Honest final position for v0.3: no selector or combination tested (twelve variants total
across three search rounds: G4-G9, M4, M6, M8/M9, M5, M7) is robust across environments.
The missing-selector problem is not solved and the search is closed per the standing
agreement. v0.3's contribution is the mechanism inventory and the clean characterisation of
why the problem resists solution (shift breadth is not knowable from information available
in time), not a working selector.

## External scoring of dropped mechanisms: registered prediction (2026-08-23, BEFORE scoring)

The original M4, M6, and M8/M9 implementations are not retained as standalone scripts, but
their definitions and RuleShift results are registered above. This is an offline replication
on benchmark traces already collected; no model calls will be made.

Coverage is limited to scorable external conditions: TruthfulQA at changed_frac 1.0 and 0.7,
TreeCut at 0.7, and HotpotQA yes/no at 0.7. The degenerate or underpowered full-shift
TreeCut and HotpotQA runs are excluded as already registered.

Registered predictions:

1. M4 cross-item consensus will not recover from its RuleShift inversion and will be at or
   below chance on at least one partial-shift benchmark.
2. M6 agreement drop will remain chance-like and will not beat both uncertainty baselines
   on any benchmark condition.
3. M8's standalone vote-shape signal and M9 selector will show no consistent transfer: M9
   will fail to dominate the appropriate single gate across the benchmark conditions, and
   will invert or collapse on at least one condition.
4. None of M4, M6, or M8/M9 will outperform the better of G0 and G1 at every tested
   benchmark condition. Results will be reported even if any prediction fails.

## External scoring of dropped mechanisms: result (2026-08-23, offline)

Scored the existing 70B benchmark traces with the registered 10-step post-shift window
(n=300 per condition). No OpenRouter calls were made. The definitions were reconstructed
from the retained `gates.py` implementation and the registered mechanism descriptions:
M4 cross-item contradiction fraction, M6 current agreement drop against the item's past
mean, M8 runner-up vote equal to the believed old key, and M9 = G1 when M8 fires else G0.

  benchmark       G0       G1       M4       M6       M8       M9
  TruthfulQA f=1  0.628    0.186    0.371    0.336    0.430    0.590
  TruthfulQA f=.7 0.521    0.602    0.435    0.506    0.491    0.506
  TreeCut f=.7    0.494    0.644    0.455    0.508    0.505    0.494
  HotpotQA f=.7  0.524    0.633    0.435    0.481    0.482    0.511

The bootstrap intervals are in `traces/dropped10_*.csv`; the point table is kept compact
here because the registered benchmark baselines and gates are already logged above.

Scoring the registered predictions:

1. CONFIRMED. M4 is below chance at all four conditions and does not recover from its
   RuleShift inversion.
2. CONFIRMED. M6 remains chance-like and does not clearly beat the uncertainty baselines.
3. CONFIRMED. M8 has no consistent transfer, and M9 collapses to chance or below on all
   partial-shift benchmarks; it is below the appropriate G1 gate in every partial case.
4. CONFIRMED. None beats the better single gate at every condition. M9 is below G0 at the
   full-shift TruthfulQA point and below G1 at all three partial-shift points.

This adds no surviving mechanism. The external evidence strengthens the decision to keep
M4, M6, and M8/M9 dropped: their RuleShift failures were not rescued by benchmark content.

## Fresh OpenRouter replication of dropped mechanisms: registered (2026-08-23, BEFORE runs)

The user supplied a temporary OpenRouter key for a fresh replication. The key will be passed
only through the process environment and will not be written to the repository or printed.
This is a new model run, separate from the offline scoring above. It will regenerate the
modified benchmark streams at 70B with the existing protocol: 30 episodes, 80 steps, shift
at step 60, k=5 branches, TruthfulQA at changed_frac 1.0 and 0.7, TreeCut at 0.7, and
HotpotQA yes/no at 0.7.

Registered predictions are unchanged: M4 remains below chance on at least one partial-shift
benchmark, M6 remains chance-like, M8/M9 shows no consistent transfer, and none beats the
appropriate single gate across all conditions. Any contrary result will be reported.

## Fresh OpenRouter replication: result (2026-08-23)

Fresh 70B traces completed for TruthfulQA at changed_frac 1.0 and 0.7, TreeCut at 0.7, and
HotpotQA yes/no at 0.7. Each condition used 30 episodes, 80 steps, shift at 60, k=5, and
the registered 10-step post-shift scoring window (n=300). The supplied key was used only in
the process environment and was not saved or printed.

  benchmark       G0       G1       M4       M6       M8       M9
  TruthfulQA f=1  0.676    0.183    0.355    0.356    0.397    0.605
  TruthfulQA f=.7 0.517    0.610    0.427    0.522    0.492    0.513
  TreeCut f=.7    0.506    0.644    0.430    0.505    0.505    0.506
  HotpotQA f=.7  0.520    0.639    0.427    0.486    0.495    0.516

The full bootstrap intervals are in `traces/fresh_dropped_results.csv` (with the fresh
benchmark traces under `traces/fresh_stage7_*`).

Prediction scoring:

1. CONFIRMED. M4 remains below chance on all three partial-shift replications and is also
   below chance at TruthfulQA full shift.
2. CONFIRMED. M6 is chance-like and does not beat the uncertainty baselines.
3. CONFIRMED. M8 has no consistent signal; M9 is near chance on partial shifts and remains
   below G0 at the full-shift TruthfulQA point.
4. CONFIRMED. No dropped mechanism beats the appropriate single gate across all conditions.

Fresh OpenRouter traces therefore do not revive M4, M6, M8, or M9. The decision to keep them
dropped is now supported by both existing-trace scoring and fresh model-generated traces.

## Four-mechanism ablation table: registered prediction (2026-08-23, BEFORE scoring)

The ablation table will score the final four mechanisms on identical rows from the existing
RuleShift overlap traces and the fresh external traces. M1 is G0 cling, M2 is G1
contradicted, M3/M7 is the velocity selector, and M5 is the soft blend. The table will
report AUROC with bootstrap intervals and will not use hidden `correct` values.

Registered predictions:

1. M1/G0 remains strongest at full shifts, while M2/G1 is strongest on partial shifts.
2. M3/M7 and M5 remain non-inverting on RuleShift but do not dominate the correct single
   gate on external content.
3. No one of the four mechanisms dominates across all conditions; the table should expose
   the precision/coverage tradeoff rather than select a winner post hoc.

## Four-mechanism ablation: result (2026-08-23)

The final four mechanisms were scored on identical rows. RuleShift uses the existing 8B
overlap traces; external rows use the fresh 70B traces above. Values are AUROC point
estimates; bootstrap intervals are stored in `traces/ablation_ruleshift.csv` and
`traces/ablation_external.csv`.

  condition          M1/G0   M2/G1   M3/M7   M5
  RuleShift ov0      0.776   0.592   0.721   0.634
  RuleShift ov1      0.515   0.748   0.620   0.682
  RuleShift ov2      0.364   0.746   0.616   0.637
  TruthfulQA f=1     0.676   0.183   0.516   0.343
  TruthfulQA f=.7    0.517   0.610   0.568   0.620
  TreeCut f=.7       0.506   0.644   0.566   0.641
  HotpotQA f=.7     0.520   0.639   0.585   0.653

Prediction scoring:

1. CONFIRMED. M1/G0 is strongest at full shifts; M2/G1 is strongest at partial shifts.
2. PARTIALLY CONFIRMED. M3/M7 and M5 remain non-inverting on RuleShift, but M5 drops
   below chance at the fresh full-shift TruthfulQA condition and M3/M7 does not transfer
   as a dominant selector.
3. CONFIRMED. No mechanism dominates across all conditions. The ablation table is now
   complete and supports reporting a tradeoff rather than selecting a winner.

## Claim 2 relative-threshold retest: registered prediction (2026-08-23, BEFORE scoring)

The fixed agreement dip threshold of 0.5 is model dependent. This retest compares it with
a relative threshold equal to 0.8 times each episode's own mean pre-shift agreement. The
accuracy-collapse definition and episode grouping remain unchanged. Existing traces will
be used for RuleShift at 3B, 8B, and 70B, plus the long-pre-shift fact stream at 70B.

Registered predictions:

1. Relative threshold censoring falls substantially at 70B, especially where fixed-0.5
   censoring was 0.533, 0.733, and 0.867 across RuleShift overlaps.
2. Relative threshold does not make the confidence curve collapse: group agreement remains
   near its pre-shift level and Claim 2 stays folded into Claim 1.
3. At 3B and 8B, relative and fixed thresholds are closer because their pre-shift agreement
   is already near 0.5; no widening of the claim is expected.
4. The fixed-threshold numbers remain reported alongside the relative-threshold numbers;
   the retest cannot overwrite the registered result.

## Claim 2 relative-threshold retest: result (2026-08-23, offline)

The relative threshold was 0.8 times each episode's pre-shift agreement. Results below show
censoring rate and mean cling time among uncensored episodes; the fixed-threshold values are
recomputed from the same episode CSVs for a like-for-like comparison. Full rows are in
`traces/relative_cling_results.csv`.

  condition          fixed censor / mean    relative censor / mean
  RuleShift 3B ov0   0.000 / 1.90           0.033 / 1.90
  RuleShift 3B ov1   0.033 / 1.83           0.033 / 1.83
  RuleShift 3B ov2   0.000 / 2.03           0.000 / 2.03
  RuleShift 8B ov0   0.133 / 2.54           0.133 / 2.27
  RuleShift 8B ov1   0.133 / 2.38           0.133 / 2.38
  RuleShift 8B ov2   0.367 / 2.53           0.333 / 2.55
  RuleShift 70B ov0  0.600 / 3.33           0.200 / 2.58
  RuleShift 70B ov1  0.800 / 4.17           0.233 / 3.17
  RuleShift 70B ov2  0.867 / 1.75           0.367 / 2.84
  Fact stream 70B    0.033 / 7.07           0.000 / 2.83

Prediction scoring:

1. CONFIRMED. Relative thresholds sharply reduce 70B censoring: from 0.600/0.800/0.867
   to 0.200/0.233/0.367 on RuleShift, and from 0.033 to 0 on the fact stream.
2. CONFIRMED. Relative thresholds do not produce a confidence collapse. Mean agreement
   change remains negative or near zero, and the blind spot remains intact.
3. CONFIRMED. 3B and 8B results are largely unchanged; the correction matters mainly when
   baseline agreement is high.
4. CONFIRMED. The fixed 0.5 results remain preserved in the comparison table.

Claim 2 remains folded into Claim 1, but the relative threshold is now the methodologically
correct version for any cross-model cling-time analysis.

## Claim 4 cross-scale and cross-environment lead time: registered prediction (2026-08-23)

Using the existing cross-cue definition, score G0 and G1 on 3B, 8B, and 70B RuleShift;
the 70B long fact stream; and the fresh external traces. Full-shift conditions are the
primary Claim 4 test; partial-shift conditions are reported as the precision/earliness
frontier rather than pooled into a single claim.

Registered predictions:

1. At full shift, G0 has positive mean cross-cue lead on every model size and on the fact
   stream and TruthfulQA full-shift benchmark.
2. G0's mean lead exceeds G1's at full shift; G1 is at or below zero because it requires a
   prior contradiction.
3. At partial shift, G0 may retain positive lead but has materially higher false-alarm
   rates than G1. Lead will never be reported without the false-alarm rate.
4. If G0 has no positive lead at full shift outside the original 8B RuleShift run, Claim 4
   is downgraded to a single-environment result.

## Claim 4 cross-scale and cross-environment lead time: result (2026-08-23, offline)

G0 had positive mean lead at every full-shift condition tested:

  condition             G0 mean lead     G0 false alarm    G1 mean lead
  RuleShift 3B ov0      +1.24             0.000             -0.45
  RuleShift 8B ov0      +0.91             0.167             -0.25
  RuleShift 70B ov0     +1.65             0.000             -1.27
  Fact stream 70B       +5.76             0.026             +2.57
  TruthfulQA f=1 fresh  +3.62             0.072             +0.82

Partial-shift frontier:

  condition             G0 lead / FA     G1 lead / FA
  RuleShift 8B ov1     +1.76 / 0.950    -0.51 / 0.050
  RuleShift 8B ov2     +1.77 / 0.947    -0.27 / 0.053
  TruthfulQA f=.7      +3.69 / 0.325    -0.29 / 0.031
  TreeCut f=.7         +3.73 / 0.310    -1.16 / 0.000
  HotpotQA f=.7        +3.74 / 0.323    -1.17 / 0.004

Full bootstrap intervals and denominators are in `traces/leadtime_coverage.csv`.

Prediction scoring:

1. CONFIRMED. G0 has positive mean lead at every full-shift model/environment condition,
   including fresh independent benchmark content.
2. PARTIALLY FAILED. G0 exceeds G1 at every full-shift condition, but G1 is positive on
   the fact stream and TruthfulQA full shift rather than at or below zero. It is still later
   than G0; the earlier structural prediction was too strong for larger item spaces.
3. CONFIRMED. Partial-shift G0 lead comes with materially higher false alarms, while G1 is
   later and much more selective. Lead is retained only with false alarms beside it.
4. CONFIRMED. Claim 4 is no longer a single-environment result. Its honest form is a
   cross-scale, cross-environment earliness/false-alarm frontier.

## Fact-stream overlap and scale coverage: registered prediction (2026-08-23, BEFORE runs)

The fact stream will be run at 70B with changed_frac 1.0, 0.7, and 0.3, using 30 episodes,
80 steps, shift at 60, and k=5. The scale ladder will add 3B and 8B at changed_frac 1.0
with the same protocol. The existing 70B full-shift result remains unchanged and is used as
the reference, not overwritten.

Registered predictions:

1. At 70B, G0 is strongest at changed_frac 1.0 and degrades toward chance as the shift
   becomes partial; G1 is stronger at partial fractions. This reproduces the shift-fraction
   crossover outside RuleShift.
2. At 3B and 8B full shift, G0 beats self-consistency and semantic entropy, preserving the
   Claim 1 scale result in the second environment.
3. The frequency/belief-formation limit persists at every scale: rare entities remain much
   weaker than frequently observed entities.
4. If the fact stream does not show the crossover or the scale ladder fails, the relevant
   generalization claim is narrowed rather than rescued by retuning.

## Fact-stream overlap result, partial point (2026-08-23)

Fresh 70B runs at 30 episodes, 80 steps, shift at 60, and n=600 post-shift rows per
condition produced:

  condition        G0       G1       M7       M5       M4       M6       M8       M9
  changed_frac .7 0.466    0.636    0.525    0.649    0.475    0.638    0.532    0.491
  changed_frac .3 0.367    0.665    0.542    0.641    0.496    0.672    0.549    0.392

The full bootstrap intervals are in `traces/factstream_overlap_results.csv` and
`traces/factstream_f03_results.csv`.

The registered crossover prediction is directionally CONFIRMED for G0/G1: G0 degrades as
the shift becomes partial and G1 becomes stronger. However, M6 and M8 are SURPRISING
FAILURES of their earlier registered generalization prediction: both become informative at
the 30% changed fraction on this fact stream, with M6 reaching 0.672. This is not being
explained away or folded into the old RuleShift result; the full-shift and scale-ladder
runs are required before deciding whether this is a fact-stream-specific mechanism.

## Fact-stream scale ladder result (2026-08-23)

Fresh 3B and 8B fact-stream full-shift runs used 30 episodes, 80 steps, shift at 60, and
n=600 post-shift rows. The existing 70B full-shift trace is included for comparison:

  signal              3B       8B       70B existing
  G0 cling            0.498    0.786    0.761
  G1 contradicted     0.420    0.602    0.505
  M7 velocity         0.480    0.739    0.665
  M5 soft blend       0.433    0.686    0.665
  M4 cross-item       0.572    0.435    0.429
  M6 agreement drop   0.538    0.505    0.619
  M8 vote shape       0.511    0.429    0.495
  M9 selector         0.500    0.763    0.763

Full intervals are in `traces/factstream_scale_results.csv` and the 3B/8B fresh traces
under `traces/fresh_stage6_factstream_*_full`.

Prediction scoring:

1. PARTIALLY CONFIRMED. The fact-stream crossover is clear at 70B (.761 full, .466/.367
   at partial fractions), with G1 stronger under partial shift. The 8B full-shift G0 result
   is strong (.786), but the 3B result is chance (.498), so the scale claim is not uniform.
2. FAILED at 3B, CONFIRMED at 8B. The smaller fact stream is too weak to reproduce the gate
   result; the 8B and 70B ladders do.
3. NOT YET SCORED here because the scale summary has not yet been split by entity frequency;
   this remains a small follow-up analysis, not an unregistered model run.
4. PARTIALLY FIRED. The fact stream generalizes at 8B/70B but not 3B, so the scale claim
   must be written with a lower-capacity failure boundary.

Important revision: M4, M6, and M8 are not universally null mechanisms. M4 is above chance
at 3B full shift (0.572), M6 is strong on the 70B fact stream (0.619 full, 0.638/.672 at
partial fractions), and M8 is informative at the 70B 30% shift point (0.549). They remain
non-robust across environments and scales, so the final four-mechanism inventory is not
silently changed, but the paper should report these as environment-specific signals rather
than claiming they are intrinsically useless.

## Fact-stream frequency split: result (2026-08-23, offline)

G0 AUROC by prior sightings in the fresh full-shift scale ladder:

  prior sightings     3B       8B       70B
  0-1 (rare)          0.459    0.439    0.387
  2-4 (mid)           0.516    0.631    0.654
  5+ (frequent)       0.513    0.935    0.866

Rows and bucket counts are in `traces/fact_frequency_results.csv`. The registered frequency
prediction is CONFIRMED in substance: the detector is weak or below chance on rare items and
becomes strong once a belief has enough observations, especially at 8B and 70B. The 3B
frequency buckets remain near chance because that model does not form a reliable belief even
for frequent entities.
## PROBE I3/I6 cross-link: existing evidence imported (2026-08-23)

The planned I3/I6 check was deferred in Axon until the selector work settled. PROBE already
has completed, versioned runs with saved traces and summaries, so a duplicate API rerun would
add cost without adding a new comparison. These are imported as cross-paper evidence, not
new Axon experiments.

  PROBE task       episodes   baseline post   PROBE post    interpretation
  I3 rule shift    50         0.390            0.393         near tie after shift
  I6 mixed shift   40         0.509            0.750         PROBE adaptation win

I3 summary: `/Users/sahilkumarsingh/Desktop/PROBE_Research_Paper_material /probe/outputs/`
`rule_shift_summary_6450b081_ci6.json`. I6 values and traces are recorded in the PROBE
research log and mixed summary outputs under the same directory.

This supports the intended Axon-to-PROBE interpretation: Axon diagnoses a blind stale-
confidence regime, while PROBE's explicit structured belief helps most when the shifted rule
is multi-factor. It does not claim that Axon improves PROBE's I3 post-shift accuracy, where
the existing result is an honest tie.

## Reviewer point 1: full-shift RuleShift non-triviality check (2026-08-24)

The review raised a circularity concern about the RuleShift full-shift result: when every
previously correct key changes, G0's definition (continued agreement with the historical
key) is closely aligned with the environment's wrong label by construction. This is a
retrospective audit of existing traces, not a new registered experiment and not a new API
run.

  condition       pre accuracy   pre branch agreement   post accuracy   G0 AUROC
  RuleShift 3B    0.658          0.578                  0.287            0.743
  RuleShift 8B    0.721          0.638                  0.208            0.776
  RuleShift 70B   1.000          0.855                  0.571            0.976

The check changes the interpretation of the 70B number. Its pre-shift action accuracy is
perfect, so the 0.976 AUROC is partly an expected stress-test consequence of a stable old
belief becoming wrong everywhere. It is not evidence that G0 discovered an arbitrary
full-shift boundary from noisy answers. The trace is not noiseless, however: pre-shift
branch agreement is 0.855, leaving 14.5 percent branch disagreement on average. In the
scored window G0 fires on 95.1 percent of wrong rows and 0.0 percent of right rows at 70B;
the remaining AUROC loss is therefore small but measurable rather than mathematically
guaranteed.

At 3B and 8B the full-shift check is less circular because ordinary action noise is already
present before the shift: pre-shift accuracy is 0.658 and 0.721, and branch agreement is
0.578 and 0.638. G0 still beats chance at both scales, but the result is weaker than at
70B. The paper will therefore label the 70B full-shift value as a stress-test/upper-bound
condition and will not use it alone to support the headline. The stronger evidence is the
combination of the partial-shift crossover, the second environment, and the independent
benchmark replication.

## Reviewer point 2: concept-drift positioning (2026-08-24)

The review identified a related-work gap. Axon's sequential contradiction and velocity
signals are methodological neighbors of classical concept-drift detection, so the paper
must cite and distinguish that literature before submission. The Markdown related-work file
now records the primary references:

- Page (1954), *Continuous Inspection Schemes* — cumulative sequential change monitoring.
- Gama et al. (2004), *Learning with Drift Detection* — DDM, monitoring online error rate.
- Bifet and Gavaldà (2007), *Learning from Time-Changing Data with Adaptive Windowing* —
  ADWIN, adaptive windows for changing streams.

The positioning is deliberately narrow. These methods detect changes in an observed stream
or error process to support updating. Axon does not claim a new generic drift detector. It
asks whether a frozen agent's internally consistent answer trace has become confidently
wrong after a hidden rule shift, using only runtime-observable trace/reward information and
no hidden correctness labels. M2/G1 and M3/M7 should be described as Axon diagnostics and
selector evidence that complement, rather than replace, CUSUM/DDM/ADWIN.

## Reviewer point 3: worked RuleShift example (2026-08-24)

The evaluation notes and first-draft outline now require a concrete example before the
formal notation. The example uses the actual RuleShift mapping: pre-shift
`blue -> B`, `red -> C`, `green -> A`; after a full shift, `blue -> C`, `red -> A`,
`green -> B`. A post-shift `red -> C` answer earns reward 0 while G0 fires immediately
from the agent's held key and G1 remains silent until that exact pair has a prior zero
reward. An unchanged cue in a partial shift can still earn reward 1 while G0 fires, making
the later inversion of G0 intuitive before the equations are introduced.

## Reviewer point 4: downgrade Proposition 1 to a remark (2026-08-24)

The draft plan now treats the current reaction lower-bound proposition as a Remark. Its
proof is a direct restatement of G1's information boundary: the gate cannot fire before the
first observed zero-reward occurrence of the same `(x,a)` pair. Keeping that observation is
useful for interpreting G1's negative lead time, but presenting it as a proposition with a
QED box risks implying theoretical depth the paper does not claim. The substantive result
remains empirical: AUROC, lead time with false alarms, and the failed runtime selector.

## Reviewer point 5: confidence intervals must be visible (2026-08-24)

The claim-file rules and first-draft outline now require every promoted AUROC result to show
`point [95% bootstrap CI]` with its sample size and trace source. The existing interval-bearing
files are `traces/ablation_ruleshift.csv`, `traces/ablation_external.csv`,
`traces/factstream_overlap_results.csv`, `traces/factstream_scale_results.csv`, and
`traces/leadtime_coverage.csv` for mean lead. Lead-time tables must keep false-alarm rates
and denominators beside the interval-bearing mean; a false-alarm interval will not be added
unless episode-level false-alarm bootstrap results are actually generated and logged.

## Reviewer point 6: model-family ambiguity (2026-08-24)

The Markdown status, contributions, and draft outline now state the exact ladder: Llama 3.2
3B, Llama 3.1 8B, and Llama 3.3 70B. They are in the same broad Llama family, but the
generation labels differ. The paper must therefore describe this as within-family transfer
and a capacity comparison, not as a clean causal scaling law in which size is the only
variable. The 3B fact-stream failure is retained as a lower-capacity boundary, not as a
precise estimate of a universal size threshold.

## Reviewer point 7: make the PROBE connection self-contained (2026-08-24)

The draft outline now defines the companion tasks before using their results. I3 is PROBE's
single-factor rule-shift task, with existing baseline/PROBE post-shift accuracy 0.390/0.393
over 50 episodes. I6 is PROBE's mixed or multi-factor shift task, with 0.509/0.750 over 40
episodes. These values are imported PROBE evidence, not Axon experiments. The paper will
state the connection as diagnostic-to-intervention: Axon identifies stale confident
behaviour, while PROBE provides explicit belief revision. I3 remains an honest tie rather
than being presented as an Axon improvement.

## Reviewer smaller nits: proofreading and categorical labels (2026-08-24)

The draft checklist now includes three final source-level fixes: change the Section 11 typo
`70G0` to `70B G0`; inspect the compiled transitions around Section 6 for merged sentences;
and normalize Table 2's stale-belief column to `No`, `Conditional`, and `No (falsified)`.
The reason for each category will move into the table note, so a reactive or broad-shift
qualification is not mixed with a binary yes/no label.

## New review point 1: scope the abstract around partial-shift inversion (2026-08-26)

The new review correctly identifies that “weakens” is too soft for the partial-shift
result. The paper's abstract and headline claim must say directly that G0 is useful under
broad/full shifts but can fall below chance and become anti-correlated with wrongness when
unchanged cues dominate. G1 is a reactive complement, and the tested runtime selectors do
not robustly choose between the two. This is a wording and claim-scope revision only; no
new result or prediction band is introduced.

## New review point 2: register trivial baselines before running them (2026-08-26)

The review requested two simple controls and a conditional confidence baseline. They are
registered here before any new run:

1. elapsed step index/time since the registered shift;
2. answer novelty/change, defined independently of G0 as whether the current answer differs
   from the immediately preceding answer (or the fixed prior answer in the trace); and
3. token/sequence logprob or calibration only if the recorded backbone interface exposes it.

Pre-run qualitative predictions: elapsed time alone should not transfer across shift
fractions or static controls; answer novelty may help when answers actually change but must
not be presented as evidence that G0's historical-key feature is unique; and an unavailable
logprob channel will be reported as unavailable rather than replaced after seeing results.
No experiment has been run under this registration yet. Before execution, append the exact
trace subset, scoring window, seeds, and score direction here. If a result is surprising,
inspect the setup for shift-window, half-shift, and distractor errors before reporting it.

## New review point 3: put CIs inside Tables 6, 7, 8, and 10 (2026-08-26)

The earlier CI rule is narrowed to the tables named by the review. Every AUROC cell in
Tables 6, 7, 8, and 10 must display `point [95% bootstrap CI]` with condition-wise `n` and
the trace source in the table or caption. Lead-time cells must retain their bootstrap
interval, false-alarm rate, and denominator. No interval will be reconstructed from a
point estimate, and no point-only number will be promoted as interval-bearing.

## New review point 4: disambiguate `n` (2026-08-26)

The paper will state that `n` is per listed condition unless a caption says pooled. RuleShift
has 240 scored rows per overlap condition; the three overlap conditions are therefore 240
each. The fact stream has 600 rows per changed fraction and per backbone; the three scale
rows are therefore 600 each. External benchmark counts are per benchmark and shift
fraction. Any pooled total must be labelled separately and must not replace the primary
condition-wise estimates.

## New review point 5: name the recorded backbone IDs (2026-08-26)

The methods table and prose must name the exact backbones rather than only saying 3B, 8B,
and 70B:

  size   recorded model ID
  3B     meta-llama/llama-3.2-3b-instruct
  8B     meta-llama/llama-3.1-8b-instruct
  70B    meta-llama/llama-3.3-70b-instruct

The supported interpretation remains within-family transfer and a capacity comparison,
not a clean scaling law, because checkpoint generations differ. This records identity;
it does not add a new model run.

## New review point 6: shorten and relocate the PROBE cross-link (2026-08-26)

The standalone PROBE results section is removed from the planned main-text structure. Keep
one self-contained Discussion/Future Work paragraph defining I3 as the single-factor task
and I6 as the mixed/multi-factor task, label the existing 0.390/0.393 and 0.509/0.750
values as imported PROBE evidence, and state that Axon is the diagnostic while PROBE is the
intervention. Detailed task provenance may live in an appendix. A new Axon-to-PROBE runtime
experiment would require its own registration before execution.

## New review point 7: minor nomenclature and presentation fixes (2026-08-26)

M3 is the raw new-contradiction velocity statistic. M7 is the deterministic selector that
uses M3 to choose between G0 and G1; it is M3-as-selector, not a separate raw mechanism
family. The draft will state this explicitly. The glossary will move to an appendix or
supplementary notation page, while the main notation table remains in the paper. Before
camera-ready export, source and extracted PDF text must be searched for `70G0` and the
Section 6 merged-sentence artifact; the intended text is `70B, G0` and properly separated
sentences. These are source/render checks, not new empirical results.

## Trivial-baseline execution registration (2026-08-30, BEFORE analysis)

This is an offline analysis of already collected traces. It makes no model calls and will not
replace the existing G0/G1 contest; it supplies the two reviewer-requested controls.

Fixed trace sets and scoring windows:

1. RuleShift: every raw seed file matching
   `traces/stage4b_overlap/ov{0,1,2}_*_seed*.csv`; score the existing post-shift window
   beginning at step 10 and ending before step 18, separately by overlap.
2. Fact stream: every `traces/stage6_factstream/shift_seed*.csv`; score every row labelled
   `phase=post` as the existing full-shift 70B comparison does.
3. External full-shift control: every
   `traces/stage7b_truthfulqa_full/shift_seed*.csv`; score every `phase=post` row.

Fixed scores and directions (larger means more danger):

- Time score: normalized post-shift step index, beginning at zero on the first scored
  post-shift row.
- Answer-novelty score: 1 if the current chosen answer differs from the agent's immediately
  preceding chosen answer for the same cue, otherwise 0. This does not consult the historical
  mode used by G0.

Fixed evaluation: row-level AUROC with 5,000 bootstrap resamples, seed 4, and 2.5th/97.5th
percentiles; retain the native scored-row count in each condition. No score direction will be
flipped after results are observed. The analysis fails its intended control role if either
baseline is above 0.65 in every listed condition or robustly beats the better of G0 and G1
in the same condition. A score at or above 0.75 triggers a setup audit for shift-window,
half-shift, and easy-distractor confounds before it is reported.

Logprob/calibration availability audit is separate: inspect the stored raw trace schema and
OpenRouter response artifacts for a direct logprob field. If absent, record unavailable;
do not substitute agreement, entropy, or a new API request.
