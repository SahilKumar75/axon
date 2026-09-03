import argparse
import csv
import glob
import math
import os
import random
import re
from collections import Counter, defaultdict


def branch_stats(branches):
    counts = Counter(branches)
    n = len(branches)
    agreement = max(counts.values()) / n
    entropy = 0
    for c in counts.values():
        p = c / n
        entropy -= p * math.log2(p)
    return agreement, entropy


def condition(path):
    name = os.path.basename(path).lower()
    if "steady" in name:
        return "steady"
    return "shift"


def seed(path):
    m = re.search(r"seed(\d+)", os.path.basename(path))
    return m.group(1) if m else ""


def load(paths, shift_at, window, agreement_threshold, entropy_threshold):
    rows = []
    for path in paths:
        cond = condition(path)
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                branches = row["branches"].split("|")
                agreement, entropy = branch_stats(branches)
                step = int(row["step"])
                reward = int(row["reward"])
                wrong = 1 - reward
                if shift_at - window <= step < shift_at:
                    band = "pre"
                elif shift_at <= step < shift_at + window:
                    band = "post"
                else:
                    band = "other"
                high_agreement = agreement >= agreement_threshold
                low_entropy = entropy <= entropy_threshold
                rows.append({
                    "path": path,
                    "condition": cond,
                    "seed": seed(path),
                    "step": step,
                    "phase": row["phase"],
                    "cue": row["cue"],
                    "chosen": row["chosen"],
                    "correct": row["correct"],
                    "reward": reward,
                    "wrong": wrong,
                    "agreement": agreement,
                    "entropy": entropy,
                    "high_agreement": int(high_agreement),
                    "low_entropy": int(low_entropy),
                    "confident_wrong_agreement": int(wrong and high_agreement),
                    "confident_wrong_entropy": int(wrong and low_entropy),
                    "confident_wrong": int(wrong and (high_agreement or low_entropy)),
                    "window": band,
                    "branches": row["branches"],
                })
    return rows


def ci(values, reps=5000):
    if not values:
        return "", ""
    if len(values) == 1:
        return values[0], values[0]
    rng = random.Random(0)
    means = []
    n = len(values)
    for _ in range(reps):
        s = 0
        for _ in range(n):
            s += values[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    return means[int(0.025 * reps)], means[int(0.975 * reps)]


def auc(labels, scores):
    pos = [s for y, s in zip(labels, scores) if y == 1]
    neg = [s for y, s in zip(labels, scores) if y == 0]
    if not pos or not neg:
        return None
    wins = 0
    total = len(pos) * len(neg)
    for p in pos:
        for n in neg:
            if p > n:
                wins += 1
            elif p == n:
                wins += 0.5
    return wins / total


def auc_ci(labels, scores, reps=5000):
    base = auc(labels, scores)
    if base is None:
        return "", "", ""
    rng = random.Random(1)
    vals = []
    n = len(labels)
    for _ in range(reps):
        sample_y = []
        sample_s = []
        for _ in range(n):
            i = rng.randrange(n)
            sample_y.append(labels[i])
            sample_s.append(scores[i])
        v = auc(sample_y, sample_s)
        if v is not None:
            vals.append(v)
    vals.sort()
    return base, vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def diff_ci(a, b, key, reps=5000):
    if not a or not b:
        return "", "", ""
    base = sum(r[key] for r in a) / len(a) - sum(r[key] for r in b) / len(b)
    rng = random.Random(2)
    vals = []
    for _ in range(reps):
        av = sum(a[rng.randrange(len(a))][key] for _ in range(len(a))) / len(a)
        bv = sum(b[rng.randrange(len(b))][key] for _ in range(len(b))) / len(b)
        vals.append(av - bv)
    vals.sort()
    return base, vals[int(0.025 * reps)], vals[int(0.975 * reps)]


def summarize(rows):
    out = []
    groups = defaultdict(list)
    for row in rows:
        if row["window"] != "other":
            groups[f"{row['condition']}_{row['window']}"].append(row)
    specs = [
        ("accuracy", "reward"),
        ("wrong", "wrong"),
        ("agreement", "agreement"),
        ("entropy", "entropy"),
        ("high_agreement_wrong", "confident_wrong_agreement"),
        ("low_entropy_wrong", "confident_wrong_entropy"),
        ("confident_wrong", "confident_wrong"),
    ]
    for group in sorted(groups):
        for name, key in specs:
            values = [r[key] for r in groups[group]]
            low, high = ci(values)
            out.append({
                "group": group,
                "metric": name,
                "n": len(values),
                "value": sum(values) / len(values),
                "ci_low": low,
                "ci_high": high,
            })
    for group, a, b in [
        ("shift_post_minus_shift_pre", groups["shift_post"], groups["shift_pre"]),
        ("shift_post_minus_steady_post", groups["shift_post"], groups["steady_post"]),
    ]:
        for name, key in specs:
            value, low, high = diff_ci(a, b, key)
            out.append({
                "group": group,
                "metric": name,
                "n": min(len(a), len(b)),
                "value": value,
                "ci_low": low,
                "ci_high": high,
            })
    post = [r for r in rows if r["condition"] == "shift" and r["window"] == "post"]
    labels = [r["wrong"] for r in post]
    sc_scores = [1 - r["agreement"] for r in post]
    ent_scores = [r["entropy"] for r in post]
    for name, scores in [("self_consistency_auroc", sc_scores), ("semantic_entropy_auroc", ent_scores)]:
        value, low, high = auc_ci(labels, scores)
        if value != "":
            best = max(value, 1 - value)
            best_low = min(low, 1 - high)
            best_high = max(high, 1 - low)
            out.append({
                "group": "shift_post",
                "metric": name,
                "n": len(labels),
                "value": value,
                "ci_low": low,
                "ci_high": high,
            })
            out.append({
                "group": "shift_post",
                "metric": name + "_best_direction",
                "n": len(labels),
                "value": best,
                "ci_low": best_low,
                "ci_high": best_high,
            })
    return out


def write_csv(path, rows, fields):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def fmt(x):
    if x == "":
        return ""
    return f"{x:.3f}"


def plot(rows, path, shift_at, window):
    vals = []
    for i in range(window):
        here = [r for r in rows if r["condition"] == "shift" and r["step"] == shift_at + i]
        n = len(here)
        rate = sum(r["confident_wrong"] for r in here) / n if n else 0
        vals.append((i, rate, n))
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    w = 640
    h = 360
    left = 58
    bottom = 306
    top = 34
    right = 610
    plot_h = bottom - top
    bar_w = 62
    gap = 24
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        '<rect width="640" height="360" fill="white"/>',
        f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#222"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" stroke="#222"/>',
        '<text x="320" y="22" text-anchor="middle" font-family="Arial" font-size="16">Confident wrong after shift</text>',
        '<text x="320" y="344" text-anchor="middle" font-family="Arial" font-size="12">steps after shift</text>',
        '<text x="16" y="174" text-anchor="middle" font-family="Arial" font-size="12" transform="rotate(-90 16 174)">rate</text>',
    ]
    for tick in [0, 0.25, 0.5, 0.75, 1.0]:
        y = bottom - tick * plot_h
        parts.append(f'<line x1="{left - 4}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#222"/>')
        parts.append(f'<text x="{left - 8}" y="{y + 4:.1f}" text-anchor="end" font-family="Arial" font-size="10">{tick:.2f}</text>')
    start = left + 28
    for i, rate, n in vals:
        x = start + i * (bar_w + gap)
        bar_h = rate * plot_h
        y = bottom - bar_h
        parts.append(f'<rect x="{x}" y="{y:.1f}" width="{bar_w}" height="{bar_h:.1f}" fill="#c43c35"/>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{bottom + 18}" text-anchor="middle" font-family="Arial" font-size="11">{i}</text>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{max(y - 6, top + 12):.1f}" text-anchor="middle" font-family="Arial" font-size="11">{rate:.2f}</text>')
        parts.append(f'<text x="{x + bar_w / 2}" y="{bottom + 34}" text-anchor="middle" font-family="Arial" font-size="9">n={n}</text>')
    parts.append("</svg>")
    with open(path, "w") as f:
        f.write("\n".join(parts))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=5)
    ap.add_argument("--agreement_threshold", type=float, default=0.8)
    ap.add_argument("--entropy_threshold", type=float, default=0.75)
    ap.add_argument("--metrics", default="traces/stage2_final_metrics.csv")
    ap.add_argument("--summary", default="traces/stage2_final_summary.csv")
    ap.add_argument("--plot", default="plots/stage2_confident_wrong.svg")
    args = ap.parse_args()
    paths = args.paths or sorted(glob.glob("traces/stage2_final/*.csv")) or sorted(glob.glob("traces/stage2/*.csv"))
    rows = load(paths, args.shift_at, args.window, args.agreement_threshold, args.entropy_threshold)
    summary = summarize(rows)
    metric_fields = [
        "path", "condition", "seed", "step", "phase", "cue", "chosen", "correct",
        "reward", "wrong", "agreement", "entropy", "high_agreement", "low_entropy",
        "confident_wrong_agreement", "confident_wrong_entropy", "confident_wrong",
        "window", "branches",
    ]
    summary_fields = ["group", "metric", "n", "value", "ci_low", "ci_high"]
    for row in rows:
        row["agreement"] = fmt(row["agreement"])
        row["entropy"] = fmt(row["entropy"])
    for row in summary:
        row["value"] = fmt(row["value"])
        row["ci_low"] = fmt(row["ci_low"])
        row["ci_high"] = fmt(row["ci_high"])
    write_csv(args.metrics, rows, metric_fields)
    write_csv(args.summary, summary, summary_fields)
    plot(load(paths, args.shift_at, args.window, args.agreement_threshold, args.entropy_threshold), args.plot, args.shift_at, args.window)


if __name__ == "__main__":
    main()
