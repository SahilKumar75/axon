import argparse
import csv
import os
import random
from collections import defaultdict


def load(path):
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            row["step"] = int(row["step"])
            row["reward"] = int(row["reward"])
            row["agreement"] = float(row["agreement"])
            row["entropy"] = float(row["entropy"])
            rows.append(row)
    return rows


def mean(xs):
    return sum(xs) / len(xs) if xs else 0


def ci(values, reps=5000):
    rng = random.Random(3)
    vals = []
    for _ in range(reps):
        vals.append(mean([values[rng.randrange(len(values))] for _ in values]))
    vals.sort()
    return vals[int(0.025 * reps)], vals[int(0.975 * reps)]


def by_step(rows):
    groups = defaultdict(list)
    for r in rows:
        groups[(r["condition"], r["step"])].append(r)
    out = []
    for condition, step in sorted(groups):
        rs = groups[(condition, step)]
        out.append({
            "condition": condition,
            "step": step,
            "n": len(rs),
            "accuracy": mean([r["reward"] for r in rs]),
            "agreement": mean([r["agreement"] for r in rs]),
            "entropy": mean([r["entropy"] for r in rs]),
        })
    return out


def seed_rows(rows, shift_at, low_agreement):
    groups = defaultdict(list)
    for r in rows:
        if r["condition"] == "shift":
            # one episode is one trace file, not one seed: the overlap sweep reuses
            # seeds 0..9 across three cue combinations per level, so grouping by seed
            # would silently merge three separate episodes into one.
            groups[r["path"]].append(r)
    out = []
    for seed in sorted(groups):
        rs = sorted(groups[seed], key=lambda r: r["step"])
        wrong = [r for r in rs if r["step"] >= shift_at and r["reward"] == 0]
        acc_step = wrong[0]["step"] if wrong else ""
        dips = [r for r in rs if acc_step != "" and r["step"] >= acc_step and r["agreement"] <= low_agreement]
        conf_step = dips[0]["step"] if dips else ""
        cling = conf_step - acc_step if conf_step != "" else ""
        out.append({
            "seed": os.path.basename(seed).replace(".csv", ""),
            "accuracy_collapse_step": acc_step,
            "confidence_dip_step": conf_step,
            "cling_time": cling,
            "censored": int(conf_step == ""),
        })
    return out


def summary(rows, curves, seeds, shift_at, window):
    shift = [r for r in rows if r["condition"] == "shift"]
    pre = [r for r in shift if shift_at - window <= r["step"] < shift_at]
    post = [r for r in shift if shift_at <= r["step"] < shift_at + window]
    cling = [r["cling_time"] for r in seeds if r["cling_time"] != ""]
    low, high = ci(cling) if cling else ("", "")
    shift_curve = [r for r in curves if r["condition"] == "shift"]
    # Either curve may never cross the threshold in the window. That is censoring, not an
    # error: "confidence never broke" is a result and has to be reportable, not a crash.
    acc_step = next((r["step"] for r in shift_curve
                     if r["step"] >= shift_at and r["accuracy"] <= 0.5), "")
    conf_step = "" if acc_step == "" else next(
        (r["step"] for r in shift_curve
         if r["step"] >= acc_step and r["agreement"] <= 0.5), "")
    out = [
        {"metric": "pre_accuracy", "value": mean([r["reward"] for r in pre]), "ci_low": "", "ci_high": ""},
        {"metric": "post_accuracy", "value": mean([r["reward"] for r in post]), "ci_low": "", "ci_high": ""},
        {"metric": "pre_agreement", "value": mean([r["agreement"] for r in pre]), "ci_low": "", "ci_high": ""},
        {"metric": "post_agreement", "value": mean([r["agreement"] for r in post]), "ci_low": "", "ci_high": ""},
        {"metric": "agreement_change", "value": mean([r["agreement"] for r in post]) - mean([r["agreement"] for r in pre]), "ci_low": "", "ci_high": ""},
        {"metric": "group_accuracy_collapse_step", "value": acc_step, "ci_low": "", "ci_high": ""},
        {"metric": "group_confidence_dip_step",
         "value": conf_step if conf_step != "" else "CENSORED", "ci_low": "", "ci_high": ""},
        {"metric": "group_cling_time",
         "value": (conf_step - acc_step) if "" not in (acc_step, conf_step) else "CENSORED",
         "ci_low": "", "ci_high": ""},
        {"metric": "seed_mean_cling_time",
         "value": mean(cling) if cling else "CENSORED",
         "ci_low": low, "ci_high": high},
        {"metric": "min_post_shift_agreement",
         "value": min([r["agreement"] for r in shift_curve if r["step"] >= shift_at]),
         "ci_low": "", "ci_high": ""},
        {"metric": "seed_censored_rate", "value": mean([r["censored"] for r in seeds]), "ci_low": "", "ci_high": ""},
    ]
    return out


def write(path, rows, fields):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def fmt_rows(rows):
    for row in rows:
        for key, val in list(row.items()):
            if isinstance(val, float):
                row[key] = f"{val:.3f}"


def plot(curves, path, shift_at):
    rows = [r for r in curves if r["condition"] == "shift" and shift_at - 5 <= r["step"] < shift_at + 10]
    w = 700
    h = 380
    left = 56
    right = 656
    top = 34
    bottom = 320
    sx = (right - left) / (len(rows) - 1)
    def xy(i, y):
        return left + i * sx, bottom - y * (bottom - top)
    acc = []
    agr = []
    for i, r in enumerate(rows):
        x, y = xy(i, r["accuracy"])
        acc.append(f"{x:.1f},{y:.1f}")
        x, y = xy(i, r["agreement"])
        agr.append(f"{x:.1f},{y:.1f}")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="700" height="380" fill="white"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222"/>',
        '<text x="350" y="22" text-anchor="middle" font-family="Arial" font-size="16">Accuracy and agreement around shift</text>',
        '<polyline fill="none" stroke="#222f8f" stroke-width="3" points="' + " ".join(acc) + '"/>',
        '<polyline fill="none" stroke="#c43c35" stroke-width="3" points="' + " ".join(agr) + '"/>',
        '<text x="570" y="54" font-family="Arial" font-size="12" fill="#222f8f">accuracy</text>',
        '<text x="570" y="74" font-family="Arial" font-size="12" fill="#c43c35">agreement</text>',
    ]
    for tick in [0, 0.5, 1.0]:
        y = bottom - tick * (bottom - top)
        parts.append(f'<line x1="{left - 4}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#222"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="10">{tick:.1f}</text>')
    for i, r in enumerate(rows):
        x, y = xy(i, 0)
        parts.append(f'<text x="{x:.1f}" y="{bottom + 18}" text-anchor="middle" font-family="Arial" font-size="10">{r["step"]}</text>')
        if r["step"] == shift_at:
            parts.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="#777" stroke-dasharray="4 4"/>')
    parts.append("</svg>")
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(parts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="traces/stage2_final_metrics.csv")
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=5)
    ap.add_argument("--low_agreement", type=float, default=0.5)
    ap.add_argument("--curve", default="traces/stage3_cling_curve.csv")
    ap.add_argument("--seeds", default="traces/stage3_cling_by_seed.csv")
    ap.add_argument("--summary", default="traces/stage3_cling_summary.csv")
    ap.add_argument("--plot", default="plots/stage3_cling_curve.svg")
    args = ap.parse_args()
    rows = load(args.metrics)
    curves = by_step(rows)
    seeds = seed_rows(rows, args.shift_at, args.low_agreement)
    sums = summary(rows, curves, seeds, args.shift_at, args.window)
    fmt_rows(curves)
    fmt_rows(seeds)
    fmt_rows(sums)
    write(args.curve, curves, ["condition", "step", "n", "accuracy", "agreement", "entropy"])
    write(args.seeds, seeds, ["seed", "accuracy_collapse_step", "confidence_dip_step", "cling_time", "censored"])
    write(args.summary, sums, ["metric", "value", "ci_low", "ci_high"])
    plot(by_step(rows), args.plot, args.shift_at)


if __name__ == "__main__":
    main()
