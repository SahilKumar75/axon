# Claim 4 — Early warning with lead time

## CLAIM
The signal fires BEFORE the post shift accuracy collapse, with measurable lead time.

## STATUS
MEASURED. Survives for G0 at the full shift. Lands as a frontier, not a single number.

## VERSION
v0

## CODE
`leadtime.py`

## DEFINITION (this had to be pinned before it could be run)
A PER CUE lead cannot be positive by construction: the gate is evaluated on the same answer
whose wrongness defines the failure, so the earliest it can fire about cue c is the step c
fails. Lead is therefore defined as CROSS CUE transfer:

  fire_step(episode) = first post shift step the gate fires on ANY cue
  failure_step(c)    = first post shift step cue c is answered wrong
  lead(c)            = failure_step(c) - fire_step(episode)

Cues that never fail carry no lead; a fire on them is a false alarm, reported alongside.

## EVIDENCE
n=30 episodes per level.

  overlap  gate              mean lead [95% CI]      false alarm (n)
  0        G0 cling          +0.91 [+0.43, +1.39]    n=2, uninformative
  0        G1 contradicted   -0.25 [-0.73, +0.23]    n=2, uninformative
  1        G0 cling          +1.76 [+1.21, +2.33]    0.950 (n=20)
  1        G1 contradicted   -0.51 [-1.15, +0.13]    0.050 (n=20)
  2        G0 cling          +1.77 [+1.17, +2.37]    0.947 (n=38)
  2        G1 contradicted   -0.27 [-0.96, +0.45]    0.053 (n=38)

Traces: `traces/stage4b_leadtime.csv`, `stage4b_leadtime_adaptive.csv`

## REGISTERED
1. G0 lead beats G1 at every level. HELD.
2. G1 lead at or below zero even at episode level. HELD at all three.
3. G0 positive lead at overlap 0. HELD, +0.91 with interval clear of zero. This is what
   makes the claim survive at all.
4. G0 false alarms rise sharply with overlap. HELD, 0.950 and 0.947 against G1's 0.050.

## THE TRAP, RECORDED SO IT IS NEVER QUOTED ALONE
G0's mean lead GROWS with overlap (+0.91, +1.76, +1.77). Read on its own that says early
warning improves exactly where AUROC inverts. It does not. The lead grows because G0 fires
on 95 percent of cues that never fail — fire on everything and you always precede the
failure. MEAN LEAD IS NOT INTERPRETABLE WITHOUT THE FALSE ALARM RATE BESIDE IT. Both must
appear together in every table and every figure.

The overlap 0 false alarm cell is 1 of 2 cue episodes and carries no information; when
every cue shifts, almost nothing survives unfailed. The meaningful denominators are 20 and 38.

## KILLS IT
- G0's lead at overlap 0 losing its separation from zero at larger n or on another model.
- A false alarm rate at overlap 0 that, once measurable, turns out to be as bad as at
  overlap 1. The current n=2 leaves this genuinely unknown.

## OPEN
- The overlap 0 false alarm rate needs a design that produces unfailing cues at a full
  shift, otherwise it stays unmeasurable. Longer episodes, or a shift where one cue's new
  key coincides with its old answer.
- Cross scale.

## CROSS-SCALE AND CROSS-ENVIRONMENT UPDATE (2026-08-23)

G0 has positive cross-cue mean lead at full shift on RuleShift 3B (+1.24), 8B (+0.91),
and 70B (+1.65), the 70B fact stream (+5.76), and fresh TruthfulQA content (+3.62).
The result is therefore not a single-environment effect.

The honest result is a frontier: at partial shifts G0 remains early but raises false alarms
(about 0.31-0.95 in the tested partial conditions), while G1 is later and selective. Mean
lead must never be quoted without its false-alarm rate.

## CI PRESENTATION REQUIREMENT

The final lead-time table must show the bootstrap interval for every mean lead from
`traces/leadtime_coverage.csv`, together with the false-alarm rate and its denominator.
False-alarm rates are currently stored as point estimates plus denominators; no interval is
to be added unless a separate bootstrap of the episode-level false-alarm indicator is
performed and recorded.
