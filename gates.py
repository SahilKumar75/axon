"""Score gate variants offline, straight off already collected traces.

Every gate here is a deterministic function of columns the agent itself observes
(cue, chosen, reward), so none of them costs a model call. `correct` is never
read: that is the environment's hidden ground truth and using it would put the
oracle confound back. Only rows strictly before the scored row are consulted.

See the registered prediction in notes/RESEARCH_LOG.md (2026-08-20).
"""

import argparse
import csv
import glob
import os
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contest import auc  # noqa: E402
from parallel import pmap  # noqa: E402

# The item set is read off the trace rather than hardcoded, so the same gate code runs on
# RuleShift's three colour cues and on the fact stream's twelve entities. The gate
# DEFINITION is unchanged -- this is only the constant that lists what the items are.
CUES = ("blue", "red", "green")


def cues_of(rows):
    return sorted({r["cue"] for r in rows})


def believed_rule(past, cues=None):
    """The model's own currently held key per item: the mode of what it has
    answered for that item so far. Same definition probe.py uses."""
    per_cue = defaultdict(list)
    for r in past:
        per_cue[r["cue"]].append(r["chosen"])
    cues = CUES if cues is None else cues
    return {c: (Counter(v).most_common(1)[0][0] if v else None)
            for c, v in ((c, per_cue.get(c)) for c in cues)}


def gates(row, past, cues=None):
    """All gate variants for one row, given only strictly earlier rows."""
    cue, chosen = row["cue"], row["chosen"]
    # the item being answered is always in scope, whatever the environment's item set is
    believed = believed_rule(past, cues=(cues or (cue,)))
    old = believed.get(cue)

    tried = [r for r in past if r["cue"] == cue and r["chosen"] == chosen]
    misses = sum(1 for r in tried if int(r["reward"]) == 0)

    g0 = float(old is not None and chosen == old)
    g1 = float(misses > 0)
    g2 = (misses / len(tried)) if tried else 0.0
    g3 = float(g1 and g0)
    # G0 is anticipatory but inverts on small shifts; G1 is flat across overlap
    # but cannot fire before the cue has been missed once. G4/G5 ask whether
    # anything combines the two without inheriting the inversion.
    g4 = max(g0, g1)
    any_contradiction = any(int(r["reward"]) == 0 for r in past)
    g5 = g0 if any_contradiction else 0.0

    # Contradiction density: how many DISTINCT cues have been contradicted so far.
    # A direct readout of how broad the shift is, which is the quantity that decides
    # whether clinging is dangerous (broad shift) or correct (narrow shift). Observable,
    # free, and not a tuned constant.
    density = len({r["cue"] for r in past if int(r["reward"]) == 0})
    # Confirmed density: a cue counts only when a key that ONCE EARNED REWARD for it later
    # failed for it. A key that used to work and stopped is evidence the rule moved; a key
    # that never worked is just a wrong guess. Raw density conflates the two, which is why
    # it saturated at overlap 2 where only one cue had actually changed.
    worked, confirmed = set(), set()
    for r in past:
        pair = (r["cue"], r["chosen"])
        if int(r["reward"]) > 0:
            worked.add(pair)
        elif pair in worked:
            confirmed.add(r["cue"])
    confirmed_density = len(confirmed)
    n_items = len(cues) if cues else len(CUES)
    g6_d2 = g0 if density >= 2 else g1
    g6_d3 = g0 if density >= n_items else g1
    # threshold free version: let the density weight the two gates directly
    w = min(1.0, density / n_items)
    g7 = w * g0 + (1 - w) * g1

    g8 = g0 if confirmed_density >= n_items else g1
    wc = min(1.0, confirmed_density / n_items)
    g9 = wc * g0 + (1 - wc) * g1

    # M5: plain product, no threshold, no selector logic at all -- the one combination
    # not yet tried (G4-G9 all gated on a threshold or a linear blend weight).
    m5_soft_blend = g0 * g1

    return {"G8_adaptive": g8, "G9_blend": g9,
            "confirmed_density": float(confirmed_density),
            "G0_cling": g0, "G1_contradicted": g1,
            "G2_contradicted_graded": g2, "G3_contradicted_and_cling": g3,
            "G4_either": g4, "G5_cling_after_any_contradiction": g5,
            "G6_adaptive_d2": g6_d2, "G6_adaptive_d3": g6_d3, "G7_blend": g7,
            "density": float(density), "M5_soft_blend": m5_soft_blend}


def mechanisms(row, past, cues, window=3):
    """M3 (velocity), M4 (cross item consensus), M6 (agreement drop).

    Kept separate from gates() because these three need the FULL episode history
    with agreement/step context, not just the current row's own cue -- gates()
    is called once per row inside a loop and does not carry that around."""
    cue = row["cue"]

    # M3: contradictions in the last `window` steps, across ALL items, per step.
    # Velocity, not count: two failed selectors (G6, G8) were static tallies of the
    # same underlying signal and both failed, so speed is the untested alternative.
    recent = [r for r in past[-window:]]
    m3_velocity = (sum(1 for r in recent if int(r["reward"]) == 0) / window) if recent else 0.0

    # M4: of items OTHER than the one being answered, what fraction have been
    # contradicted at least once so far. Does not depend on this item's own history,
    # which is what M1/M2 both do -- and what failed to transfer past RuleShift's
    # 3 cue structure into real benchmarks with 6-12 items.
    other_cues = [c for c in cues if c != cue]
    if other_cues:
        contradicted_others = {r["cue"] for r in past
                               if r["cue"] in other_cues and int(r["reward"]) == 0}
        m4_cross_item = len(contradicted_others) / len(other_cues)
    else:
        m4_cross_item = 0.0

    # M6: this item's own current branch agreement against its own past mean agreement.
    # A drop means the model is less sure of ITS OWN answer, independent of reward --
    # the only mechanism here that uses the agreement column at all.
    own_past = [float(r["agreement"]) for r in past if r["cue"] == cue]
    if own_past:
        past_mean = sum(own_past) / len(own_past)
        m6_agreement_drop = max(0.0, past_mean - float(row["agreement"]))
    else:
        m6_agreement_drop = 0.0

    # M8: does the CURRENT step's runner-up vote equal the item's own believed old key,
    # while the chosen answer is something else? A genuinely different signal type from
    # M1-M6: it uses no history beyond the single believed_rule() lookup, and looks at the
    # SHAPE of one step's own branch votes rather than a scalar (agreement/entropy, which
    # M6 already tried and which failed) or a tally across steps (M1-M4).
    believed = believed_rule(past, cues=cues)
    old_key = believed.get(cue)
    branches = row.get("branches", "")
    votes = branches.split("|") if branches else []
    if votes and old_key is not None:
        counts = Counter(votes)
        chosen = row["chosen"]
        ranked = counts.most_common()
        runner_up = ranked[1][0] if len(ranked) > 1 else None
        m8_bimodal_split = float(runner_up == old_key and chosen != old_key)
    else:
        m8_bimodal_split = 0.0

    return {"M3_velocity": m3_velocity, "M4_cross_item": m4_cross_item,
            "M6_agreement_drop": m6_agreement_drop, "_m3_raw": m3_velocity,
            "M8_bimodal_split": m8_bimodal_split}


def boot(labels, scores, reps=5000, seed=4):
    base = auc(labels, scores)
    if base == "":
        return "", "", ""
    rng = random.Random(seed)
    vals = []
    for _ in range(reps):
        idx = [rng.randrange(len(labels)) for _ in labels]
        v = auc([labels[i] for i in idx], [scores[i] for i in idx])
        if v != "":
            vals.append(v)
    vals.sort()
    return base, vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def window_rows(path, shift_at, window):
    """Rebuild each episode's history in order, then keep only the scored window."""
    kept = []
    by_episode = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            by_episode[row["path"]].append(row)
    for _, rows in sorted(by_episode.items()):
        rows.sort(key=lambda r: int(r["step"]))
        cues = cues_of(rows)
        for i, row in enumerate(rows):
            step = int(row["step"])
            if row["condition"] != "shift" or not (shift_at <= step < shift_at + window):
                continue
            row = dict(row)
            row.update(gates(row, rows[:i], cues=cues))
            row.update(mechanisms(row, rows[:i], cues))
            # M7: velocity-gated selector between the two gates. Threshold is the midpoint
            # of the two mean velocities measured separately at overlap 0 (0.448) and
            # overlap 2 (0.289) on RuleShift -- fixed before this row loop runs, not fit to
            # these rows.
            row["M7_velocity_selector"] = (row["G0_cling"] if row["M3_velocity"] >= 0.35
                                           else row["G1_contradicted"])
            row["wrong"] = int(row["reward"]) == 0
            kept.append(row)
    return kept


def missed(rows, name):
    """Wrong rows the gate stayed silent on -- the registered false negatives."""
    wrong = [r for r in rows if r["wrong"]]
    if not wrong:
        return float("nan")
    return sum(1 for r in wrong if r[name] == 0) / len(wrong)


def _boot_task(arg):
    """Top level so it survives pickling into a worker process."""
    labels, scores = arg
    return boot(labels, scores)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="traces/stage4b_overlap")
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=8)
    ap.add_argument("--out", default="traces/stage4b_gates.csv")
    args = ap.parse_args()

    paths = sorted(glob.glob(os.path.join(args.dir, "ov*_probe.csv")))
    names = ["G0_cling", "G1_contradicted", "G2_contradicted_graded",
             "G3_contradicted_and_cling", "G4_either",
             "G5_cling_after_any_contradiction",
             "G6_adaptive_d2", "G6_adaptive_d3", "G7_blend",
             "G8_adaptive", "G9_blend", "M5_soft_blend",
             "M3_velocity", "M4_cross_item", "M6_agreement_drop", "M7_velocity_selector",
             "M8_bimodal_split"]

    out_rows = []
    print(f"{'overlap':<9}{'gate':<28}{'AUROC [95% CI]':<26}{'silent on wrong'}")
    for path in paths:
        level = int(re.search(r"ov(\d+)_probe", os.path.basename(path)).group(1))
        rows = window_rows(path, args.shift_at, args.window)
        labels = [r["wrong"] for r in rows]
        # one bootstrap per gate, run across processes. Each seeds its own rng, so the
        # results do not depend on the pool at all.
        results = pmap(_boot_task, [(labels, [r[n] for r in rows]) for n in names])
        for name, (base, lo, hi) in zip(names, results):
            cell = "n/a" if base == "" else f"{base:.3f} [{lo:.3f}, {hi:.3f}]"
            print(f"{level:<9}{name:<28}{cell:<26}{missed(rows, name):.3f}")
            out_rows.append({"overlap": level, "gate": name, "n": len(rows),
                             "auroc": base, "auroc_low": lo, "auroc_high": hi,
                             "silent_on_wrong": round(missed(rows, name), 3)})
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
