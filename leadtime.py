"""C-B: does the gate warn about a cue before that cue fails?

Lead is measured as cross cue transfer, not per cue. A per cue lead cannot be
positive by construction -- the gate is evaluated on the same answer whose
wrongness defines the failure -- so the question worth asking is whether a fire
on one cue precedes failures on the cues that have not failed yet.

  fire_step(episode) = first post shift step the gate fires on ANY cue
  failure_step(c)    = first post shift step cue c is answered wrong
  lead(c)            = failure_step(c) - fire_step(episode)

Cues that never fail carry no lead; if the gate fired on them anyway that is a
false alarm, reported alongside, because a gate that buys lead by firing
constantly is not an early warning system.

See the registered prediction in notes/RESEARCH_LOG.md (2026-08-20).
"""

import argparse
import csv
import glob
import os
import random
import re
import statistics as st
from collections import defaultdict

from gates import gates

CUES = ("blue", "red", "green")


def episodes(path, shift_at, window):
    by_episode = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            by_episode[row["path"]].append(row)
    for _, rows in sorted(by_episode.items()):
        rows.sort(key=lambda r: int(r["step"]))
        scored = []
        for i, row in enumerate(rows):
            row = dict(row)
            row.update(gates(row, rows[:i]))
            scored.append(row)
        lo, hi = shift_at, shift_at + window
        yield [r for r in scored if r["condition"] == "shift" and lo <= int(r["step"]) < hi]


def episode_stats(rows, name):
    """Leads for cues that fail, plus a false alarm flag per cue that never fails."""
    fires = [int(r["step"]) for r in rows if r[name] > 0]
    fire_step = min(fires) if fires else None

    leads, false_alarms, unfailing = [], 0, 0
    for cue in CUES:
        cue_rows = [r for r in rows if r["cue"] == cue]
        if not cue_rows:
            continue
        wrong = [int(r["step"]) for r in cue_rows if int(r["reward"]) == 0]
        if wrong:
            if fire_step is not None:
                leads.append(min(wrong) - fire_step)
        else:
            unfailing += 1
            if any(r[name] > 0 for r in cue_rows):
                false_alarms += 1
    return leads, false_alarms, unfailing, fire_step is not None


def boot_mean(vals, reps=5000, seed=4):
    if not vals:
        return float("nan"), float("nan"), float("nan")
    rng = random.Random(seed)
    means = []
    for _ in range(reps):
        means.append(st.mean(vals[rng.randrange(len(vals))] for _ in vals))
    means.sort()
    return st.mean(vals), means[int(0.025 * reps)], means[int(0.975 * reps)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="traces/stage4b_overlap")
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=8)
    ap.add_argument("--gates", default="G0_cling,G1_contradicted")
    ap.add_argument("--out", default="traces/stage4b_leadtime.csv")
    args = ap.parse_args()

    names = args.gates.split(",")
    out_rows = []
    print(f"{'overlap':<9}{'gate':<20}{'mean lead [95% CI]':<28}"
          f"{'fired':<8}{'pos lead':<10}{'false alarm'}")
    for path in sorted(glob.glob(os.path.join(args.dir, "ov*_probe.csv"))):
        level = int(re.search(r"ov(\d+)_probe", os.path.basename(path)).group(1))
        eps = list(episodes(path, args.shift_at, args.window))
        for name in names:
            leads, fa, unf, fired = [], 0, 0, 0
            for rows in eps:
                l, f, u, did = episode_stats(rows, name)
                leads += l
                fa += f
                unf += u
                fired += int(did)
            m, lo, hi = boot_mean(leads)
            pos = sum(1 for x in leads if x > 0) / len(leads) if leads else float("nan")
            fa_rate = fa / unf if unf else float("nan")
            print(f"{level:<9}{name:<20}{f'{m:+.2f} [{lo:+.2f}, {hi:+.2f}]':<28}"
                  f"{fired}/{len(eps):<5}{pos:<10.3f}"
                  f"{'n/a' if unf == 0 else f'{fa_rate:.3f}'}")
            out_rows.append({
                "overlap": level, "gate": name, "episodes": len(eps),
                "episodes_fired": fired, "n_leads": len(leads),
                "mean_lead": round(m, 3), "lead_low": round(lo, 3),
                "lead_high": round(hi, 3),
                "frac_positive_lead": round(pos, 3) if leads else "",
                "unfailing_cues": unf,
                "false_alarm_rate": round(fa_rate, 3) if unf else "",
            })
        print()

    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print("wrote", args.out)


if __name__ == "__main__":
    main()
