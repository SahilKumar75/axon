import argparse
import csv
import glob
import os
import random
from collections import defaultdict

from contest import auc
from gates import cues_of, gates, mechanisms


def bootstrap(labels, scores, reps=5000, seed=4):
    base = auc(labels, scores)
    if base == "":
        return base, base, base
    rng = random.Random(seed)
    values = []
    for _ in range(reps):
        indices = [rng.randrange(len(labels)) for _ in labels]
        value = auc([labels[i] for i in indices], [scores[i] for i in indices])
        if value != "":
            values.append(value)
    values.sort()
    return base, values[int(0.025 * len(values))], values[int(0.975 * len(values))]


def score_file(path, shift_at, window):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row["step"]))
    cues = cues_of(rows)
    scored = []
    for index, row in enumerate(rows):
        step = int(row["step"])
        if row["phase"] != "post" or not (shift_at <= step < shift_at + window):
            continue
        past = rows[:index]
        values = {}
        values.update(gates(row, past, cues))
        values.update(mechanisms(row, past, cues))
        values["M7_velocity_selector"] = (values["G0_cling"]
                                           if values["M3_velocity"] >= 0.35
                                           else values["G1_contradicted"])
        values["M9_selector"] = (values["G1_contradicted"]
                                  if values["M8_bimodal_split"] else values["G0_cling"])
        values["wrong"] = int(row["reward"]) == 0
        scored.append(values)
    return scored


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--shift-at", type=int, default=60)
    parser.add_argument("--window", type=int, default=20)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    all_rows = []
    for path in sorted(glob.glob(args.pattern)):
        all_rows.extend(score_file(path, args.shift_at, args.window))
    labels = [row["wrong"] for row in all_rows]
    names = ["G0_cling", "G1_contradicted", "M7_velocity_selector", "M5_soft_blend",
             "M4_cross_item", "M6_agreement_drop", "M8_bimodal_split", "M9_selector"]
    output = []
    for name in names:
        base, low, high = bootstrap(labels, [row[name] for row in all_rows])
        output.append({"benchmark": args.label, "n": len(all_rows), "signal": name,
                       "auroc": base, "auroc_low": low, "auroc_high": high})
        print(f"{args.label:24} {name:22} {base:.3f} [{low:.3f}, {high:.3f}]")
    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    exists = os.path.exists(args.out)
    with open(args.out, "a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output[0]))
        if not exists:
            writer.writeheader()
        writer.writerows(output)


if __name__ == "__main__":
    main()
