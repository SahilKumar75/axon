"""Collapse the per level contest CSVs into one table across overlap levels.

Overlap = how many of the three cues keep their pre shift key, so level 0 is the
full shift and level 2 is a shift that touches only one cue. Two questions get
answered here: does the detector degrade smoothly as the shift shrinks (claim 5,
the detectability limit), and does asking ever beat watching at any overlap
level (claim 3, still unresolved after the oracle confound was removed).
"""

import argparse
import csv
import glob
import os
import re


BASELINES = [
    "uncertainty_agreement",
    "semantic_entropy",
    "reversed_agreement",
    "reversed_entropy",
    "cling_timing",
    "probe_rule_change",
]


def level_of(path):
    m = re.search(r"ov(\d+)_contest", os.path.basename(path))
    return int(m.group(1)) if m else -1


def read(path):
    with open(path, newline="") as f:
        return {row["method"]: row for row in csv.DictReader(f)}


def fmt(row, key="auroc"):
    if not row or row[key] == "":
        return "n/a"
    return f"{float(row[key]):.3f} [{float(row[key + '_low']):.3f}, {float(row[key + '_high']):.3f}]"


def beats(row):
    """A gap row wins only if its whole interval sits above zero."""
    if not row or row["auroc_low"] == "":
        return False
    return float(row["auroc_low"]) > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="traces/stage4b_overlap")
    ap.add_argument("--out", default="traces/stage4b_overlap_summary.csv")
    args = ap.parse_args()

    paths = sorted(glob.glob(os.path.join(args.dir, "ov*_contest.csv")), key=level_of)
    if not paths:
        raise SystemExit("no contest CSVs in " + args.dir + "; run contest.py per level first")

    tables = [(level_of(p), read(p)) for p in paths]

    print("\n=== axon_probe AUROC by overlap level ===")
    print(f"{'overlap':<9}{'n':<6}{'axon_probe AUROC [95% CI]':<32}")
    for level, t in tables:
        row = t.get("axon_probe")
        print(f"{level:<9}{row['n']:<6}{fmt(row):<32}")

    print("\n=== gap: axon_probe minus baseline (positive = asking beats watching) ===")
    header = f"{'baseline':<22}" + "".join(f"ov{level:<21}" for level, _ in tables)
    print(header)
    for name in BASELINES:
        cells = ""
        for _, t in tables:
            row = t.get("axon_probe_minus_" + name)
            mark = " *" if beats(row) else "  "
            cells += f"{fmt(row) + mark:<23}"
        print(f"{name:<22}{cells}")
    print("\n* = whole 95% interval above zero (a real win, not a tie)")

    out_rows = []
    for level, t in tables:
        for method, row in t.items():
            out_rows.append({
                "overlap": level,
                "method": method,
                "n": row["n"],
                "auroc": row["auroc"],
                "auroc_low": row["auroc_low"],
                "auroc_high": row["auroc_high"],
                "precision": row["precision"],
                "recall": row["recall"],
            })
    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)
    print("\nwrote", args.out)


if __name__ == "__main__":
    main()
