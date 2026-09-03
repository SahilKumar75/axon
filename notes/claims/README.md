# Claim files

One file per claim. Each is the single place that claim's status lives, so a claim can be
picked up, re-tested and upgraded without reading the whole research log.

Each file carries the same sections:

  CLAIM          the sentence the claim defends
  STATUS         one of: UNRUN / MEASURED / VALIDATED / FALSIFIED / FOLDED
  VERSION        which Axon version this status was established at
  CODE           the scripts that test it
  EVIDENCE       the numbers, with n and interval, and the trace files they came from
  REGISTERED     predictions made BEFORE each run, and whether each held
  KILLS IT       what result would overturn the current status
  OPEN           what still has to be run before this claim is paper ready

Rules, carried over from PROBE's discipline:

- Predictions get written into REGISTERED before the run, never after.
- A failed prediction is recorded as failed. Bands are never widened afterwards to make a
  miss look like a hit.
- Anything run without a registered prediction is labelled POST HOC where it is reported.
- A claim is not VALIDATED until it survives on more than one model and more than one
  environment. Everything measured on RuleShift alone with llama 3.1 8b is provisional,
  however tight its interval.
- When a result is promoted into the paper, every AUROC point estimate must be shown as
  `AUROC [95% bootstrap CI]`, with `n` and the trace source in the table or caption. Lead
  time must show its interval beside the mean and must keep the false-alarm rate beside it;
  do not infer or invent an interval for a quantity that was not bootstrapped.
- For the current paper tables, this applies explicitly to Tables 6, 7, 8, and 10. Unless
  a caption says pooled, `n` is per listed condition.

Version history lives in notes/VERSIONS.md.
