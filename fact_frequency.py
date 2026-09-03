import argparse
import csv
import glob
from collections import Counter, defaultdict

from contest import auc
from gates import gates, cues_of


def score(path, shift_at, window):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row["step"]))
    cues = cues_of(rows)
    seen = Counter()
    buckets = defaultdict(lambda: [[], []])
    for index, row in enumerate(rows):
        step = int(row["step"])
        if step < shift_at:
            seen[row["cue"]] += 1
            continue
        if step >= shift_at + window:
            continue
        past = rows[:index]
        values = gates(row, past, cues)
        prior = seen[row["cue"]]
        bucket = "rare_0_1" if prior <= 1 else "mid_2_4" if prior <= 4 else "freq_5_plus"
        buckets[bucket][0].append(int(row["reward"]) == 0)
        buckets[bucket][1].append(values["G0_cling"])
    return buckets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--shift-at", type=int, required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    combined = defaultdict(lambda: [[], []])
    for path in sorted(glob.glob(args.pattern)):
        for bucket, values in score(path, args.shift_at, args.window).items():
            combined[bucket][0].extend(values[0])
            combined[bucket][1].extend(values[1])
    rows = []
    for bucket in ["rare_0_1", "mid_2_4", "freq_5_plus"]:
        labels, scores = combined[bucket]
        value = auc(labels, scores) if labels else ""
        row = {"label": args.label, "bucket": bucket, "n": len(labels), "auroc": value}
        rows.append(row)
        print(row)
    with open(args.out, "a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
