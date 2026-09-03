import argparse
import csv
import glob
import os
import random
from statistics import mean


def ci(values, reps=5000, seed=3):
    if not values:
        return "", ""
    rng = random.Random(seed)
    samples = [mean(values[rng.randrange(len(values))] for _ in values) for _ in range(reps)]
    samples.sort()
    return samples[int(reps * 0.025)], samples[int(reps * 0.975)]


def episode(path, shift_at, window, pre_window, fraction):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row["step"]))
    pre = [row for row in rows if shift_at - pre_window <= int(row["step"]) < shift_at]
    post = [row for row in rows if shift_at <= int(row["step"]) < shift_at + window]
    pre_agreement = mean(float(row["agreement"]) for row in pre)
    collapse = next((int(row["step"]) for row in post if int(row["reward"]) == 0), None)
    fixed_threshold = 0.5
    relative_threshold = fraction * pre_agreement
    fixed_dip = next((int(row["step"]) for row in post
                      if collapse is not None and int(row["step"]) >= collapse
                      and float(row["agreement"]) <= fixed_threshold), None)
    relative_dip = next((int(row["step"]) for row in post
                         if collapse is not None and int(row["step"]) >= collapse
                         and float(row["agreement"]) <= relative_threshold), None)
    return {
        "episode": os.path.basename(path),
        "pre_agreement": pre_agreement,
        "post_agreement": mean(float(row["agreement"]) for row in post),
        "agreement_change": mean(float(row["agreement"]) for row in post) - pre_agreement,
        "fixed_cling": "" if fixed_dip is None or collapse is None else fixed_dip - collapse,
        "relative_cling": "" if relative_dip is None or collapse is None else relative_dip - collapse,
        "fixed_censored": int(fixed_dip is None),
        "relative_censored": int(relative_dip is None),
        "min_post_agreement": min(float(row["agreement"]) for row in post),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--shift-at", type=int, required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--pre-window", type=int, required=True)
    parser.add_argument("--fraction", type=float, default=0.8)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    rows = [episode(path, args.shift_at, args.window, args.pre_window, args.fraction)
            for path in sorted(glob.glob(args.pattern))]
    fixed = [float(row["fixed_cling"]) for row in rows if row["fixed_cling"] != ""]
    relative = [float(row["relative_cling"]) for row in rows if row["relative_cling"] != ""]
    fixed_low, fixed_high = ci(fixed)
    relative_low, relative_high = ci(relative)
    summary = {
        "label": args.label,
        "n": len(rows),
        "fixed_mean_cling": mean(fixed) if fixed else "CENSORED",
        "fixed_ci_low": fixed_low,
        "fixed_ci_high": fixed_high,
        "fixed_censored_rate": mean(row["fixed_censored"] for row in rows),
        "relative_mean_cling": mean(relative) if relative else "CENSORED",
        "relative_ci_low": relative_low,
        "relative_ci_high": relative_high,
        "relative_censored_rate": mean(row["relative_censored"] for row in rows),
        "mean_agreement_change": mean(row["agreement_change"] for row in rows),
        "min_group_post_agreement": min(row["min_post_agreement"] for row in rows),
    }
    print(summary)
    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.out, "a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary))
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerow(summary)


if __name__ == "__main__":
    main()
