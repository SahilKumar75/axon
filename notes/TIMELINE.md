# Axon Timeline (version 0)

This file is the plan of record. It is written to be handed to a coding agent and followed
top to bottom. It is Axon version 0. We do not know the final version. The goal is not to
finish, it is to improve Axon one stage at a time and to report failures honestly.

Read these notes before starting: README.md, notes/IDEA_NOTES.md, notes/CONTRIBUTIONS.md,
notes/EVALUATION.md, notes/FUTURE_DIRECTIONS.md, notes/RELATED_WORK.md,
notes/DEEP_RESEARCH_2026-07-21.md, notes/OPEN_QUESTIONS.md.

## The idea in one paragraph
When the rules of a task change partway through, a language model often keeps applying the
old rule with full confidence and gets it wrong. The usual ways to catch a shaky answer
(self consistency, semantic entropy) go blind here, because the model repeats the same wrong
answer, so it looks sure. Axon shakes the question (rephrase it, ask a counterfactual, use a
second model) to make the branches spray apart, watches that spray, and flags the stale
belief before it costs reward. That flag is then handed to a revision loop so the agent
adapts faster.

## Direction and headline
Axon is not sold as a better detector. Detection on static questions is already published.
Axon is sold as a live trigger for belief revision under changing rules, plus a new metric
called cling time. The detector borrows known signals. The novelty is the dynamic setting,
acting on the signal, lead time inside an episode, and cling time.

## Claims we are testing
- C-A headline: the shake based signal catches confident wrong after a rule change where
  self consistency and semantic entropy go blind.
- C-B: the signal fires before the failure (lead time).
- C-C: the pattern holds across model sizes.
- N1: one counterfactual probe step catches the stale belief earlier than passive watching.
- N2 cling time: after a shift, accuracy drops now but confidence lags, measured as a number.
- Lead directions (see FUTURE_DIRECTIONS): 1 cling time metric, 2 self triggered loop.

## Tests
Internal (home turf, we own the truth): PROBE rule shift tasks I3 and I6, plus one steady no
change control. These give perfect ground truth and guarantee confident wrong at the flip.
External (independent, only after home turf works): TruthfulQA, unanswerable math word
problems, multi hop question answering. Chosen because they have known answers and are famous
for confident wrong answers.

## Rules of work
Repo: name is one word, no hyphens. No em dashes anywhere. No text that reads like it was
written by an assistant. No assistant co author line on any commit.
Commits: small and trackable, read like a real research history. Examples:
  add rule shift env
  log i3 traces seed 0
  measure cling time
  self consistency baseline
  detector first pass
  fix seed handling
  add lead time script
Code style: follow the ponytail principle, least code possible, no clever abstractions. No
comments and no messages inside code files.
Budget: 36.33 dollars on OpenRouter. Do all building and pilots on Llama 3.1 8B, which costs
pennies. Spend on the 70B model only for final tables. Reserve about 5 dollars for a single
GPT 4.1 spot check at the very end. If a stage fails its stop gate, do not spend more until
it is fixed or the claim is rewritten.
Notes discipline: after every stage, add a RESEARCH_LOG entry (use SESSION_TEMPLATE), update
any md file the result changes, and record numbers with confidence intervals. Save raw runs
so later stages can reuse them.

## Efficiency note
Stages 2, 3, and 5 read the same recorded runs. Collect the runs once, then analyze them
three ways. Do not re run the model for each analysis.

---

# The staged timeline with stop gates

Each stage lists: goal, do, model and cost, stop gate, log, update, commit.

## Stage 1. Minimal harness
Goal: be able to branch or shake a model on a task and record every step.
Do: build the smallest loop that runs a task, shakes the question, and writes a per step
trace (step, phase, chosen answer, correct answer, reward, confidence, branch answers).
Model and cost: none, no API spend for wiring, tiny 8B smoke run only.
Stop gate: none, this is plumbing. Move on when a trace file is produced.
Log: RESEARCH_LOG stage 1 entry, note the trace format.
Update: EVALUATION if the trace fields change.
Commit: add task runner, add trace logger, add rule shift env.

## Stage 2. Prove the blind spot
Goal: show plain self consistency goes blind on confident wrong after a rule change.
Do: on I3 and I6, record runs. Measure self consistency and semantic entropy in the post
shift window. Show they look confident while the model is wrong.
Model and cost: Llama 3.1 8B, cheap.
STOP GATE: if self consistency already catches the post shift failure well, the premise is
dead. Stop and rethink the whole idea before spending more.
Log: RESEARCH_LOG with the numbers and the plot.
Update: RELATED_WORK or CONTRIBUTIONS if the result changes the framing.
Commit: self consistency baseline, semantic entropy baseline, blind spot plot.

## Stage 3. Measure cling time
Goal: turn PROBE motivation into a number. Reuse Stage 2 runs.
Do: around the shift, measure the gap between accuracy dropping and confidence dropping. That
gap is cling time. Report it with a confidence interval.
Model and cost: none new, reuse Stage 2 runs.
Stop gate: soft. If confidence tracks accuracy with no lag, there is nothing to cling, note
it and lean on the detector claims instead.
Log: RESEARCH_LOG with cling time values.
Update: CONTRIBUTIONS N2 with the measured result.
Commit: measure cling time, add cling curve plot.

## Stage 4. Build the detector and run the contest
Goal: prove C-A. Build the shake based detector (paraphrase, counterfactual probe, second
model) and race it against the baselines.
Do: each method outputs a danger score per step. Score with AUROC and precision recall,
restricted to the post shift confident wrong window.
Model and cost: Llama 3.1 8B.
STOP GATE: if the detector does not beat the baselines in the danger window, fix the detector
or the signal before going on. Do not proceed on a losing detector.
Log: RESEARCH_LOG with the contest table.
Update: EVALUATION and CONTRIBUTIONS C-A with results.
Commit: detector first pass, counterfactual probe, detection contest table.

## Stage 5. Lead time
Goal: prove C-B. Reuse Stage 4 runs.
Do: measure how many steps before the failure the signal fires. Report mean lead time and
precision recall.
Model and cost: none new, reuse Stage 4 runs.
Stop gate: soft. If lead time is zero, report detection without early warning.
Log: RESEARCH_LOG with lead time.
Update: CONTRIBUTIONS C-B.
Commit: add lead time script, lead time results.

## Stage 6. Self triggered loop
Goal: the payoff. The agent watches its own spray and revises early.
Do: feed the detector signal into a revision step. Compare adaptation speed and task success
against PROBE without the trigger and against the plain baseline.
Model and cost: Llama 3.1 8B, then 70B for the final table.
STOP GATE: if acting on the signal does not adapt faster than PROBE alone, the loop adds
nothing, report it honestly and keep Axon as a detector only result.
Log: RESEARCH_LOG with the adaptation comparison.
Update: CONTRIBUTIONS, README headline if the payoff lands.
Commit: self triggered revision, adaptation comparison.

## Stage 7. Scale up and externals
Goal: prove C-C and add independent evidence.
Do: rerun the key results on a mid model, then one tiny GPT 4.1 spot check on the single best
result. Only after home turf works, run one external benchmark (start with unanswerable math
or TruthfulQA).
Model and cost: 70B for tables, about 5 dollars reserved for one GPT 4.1 run. Keep external
runs small first.
Stop gate: soft. Report ties and non significant externals plainly, the way PROBE did.
Log: RESEARCH_LOG with cross scale and external numbers.
Update: CONTRIBUTIONS C-C, README, EVALUATION.
Commit: cross scale run, external benchmark run, final tables.

---

# After the stages
Only draft the paper after the stop gates are passed or the failures are recorded. Testing
comes first so failures reshape Axon before any draft. When a stage changes the idea, update
the md files first, then continue. This is version 0. Expect to loop back and improve.

# Definition of done for version 0
A trace harness that works, the blind spot shown, cling time measured, a detector that beats
the baselines in the danger window with a confidence interval, a lead time number, and one
self triggered loop result, all on 8B, with honest notes on anything that failed.
