import argparse
import csv
import math
import os
import random
from collections import Counter

from parallel import pmap


def entropy(branches):
    counts = Counter(branches)
    n = len(branches)
    out = 0
    for c in counts.values():
        p = c / n
        out -= p * math.log2(p)
    return out


def auc(labels, scores):
    """Same statistic as the pairwise count (ties worth half a win), computed
    from mid ranks so a 5000 rep bootstrap at n in the hundreds finishes.

    The pairwise form is O(n^2) per bootstrap sample, which stopped being
    affordable once the overlap sweep pushed n from 25 to 240."""
    n_pos = sum(1 for y in labels if y)
    n_neg = len(labels) - n_pos
    if not n_pos or not n_neg:
        return ""
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        mid = (i + j) / 2 + 1  # ranks are 1 based; ties share their mid rank
        for k in range(i, j + 1):
            ranks[order[k]] = mid
        i = j + 1
    rank_sum = sum(r for y, r in zip(labels, ranks) if y)
    return (rank_sum - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)


def pr(labels, preds):
    tp = sum(1 for y, p in zip(labels, preds) if y and p)
    fp = sum(1 for y, p in zip(labels, preds) if not y and p)
    fn = sum(1 for y, p in zip(labels, preds) if y and not p)
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    return precision, recall


def ci(rows, fn, reps=5000):
    if not rows:
        return "", "", ""
    base = fn(rows)
    rng = random.Random(4)
    vals = []
    for _ in range(reps):
        sample = [rows[rng.randrange(len(rows))] for _ in rows]
        v = fn(sample)
        if v != "":
            vals.append(v)
    vals.sort()
    if not vals:
        return base, "", ""
    return base, vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def load(path, shift_at, window):
    rows = []
    skipped = 0
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            step = int(row["step"])
            if row["condition"] == "shift" and shift_at <= step < shift_at + window:
                if row.get("insufficient_history") == "1" or row["change_score"] == "":
                    # the model had not yet answered every cue once, so its own
                    # belief could not be inferred and no probe was issued. The
                    # row is dropped for every method, not just the probe, so all
                    # methods stay scored on an identical row set.
                    skipped += 1
                    continue
                branches = row["branches"].split("|")
                agreement = float(row["agreement"])
                ent = entropy(branches)
                offset = step - shift_at
                row["wrong"] = int(row["reward"]) == 0
                row["agreement_score"] = agreement
                row["entropy_score"] = ent
                row["uncertainty_agreement"] = 1 - agreement
                row["semantic_entropy"] = ent
                row["reversed_agreement"] = agreement
                row["reversed_entropy"] = -ent
                row["cling_timing"] = max(0, (window - offset) / window)
                row["probe_rule_change"] = float(row["change_score"])
                row["axon_probe"] = float(row["stale_score"])
                rows.append(row)
    if skipped:
        print(f"dropped {skipped} window rows with no inferable belief "
              f"(kept {len(rows)})")
    return rows


def score(rows, name, threshold):
    labels = [r["wrong"] for r in rows]
    scores = [r[name] for r in rows]
    preds = [s >= threshold for s in scores]
    p, r = pr(labels, preds)
    return auc(labels, scores), p, r


def _ci_task(arg):
    """Top level so it pickles into a worker. The closures are built inside the
    child process, so nothing unpicklable ever crosses the boundary."""
    rows, name, threshold, metric, is_gap = arg
    if is_gap:
        def fn(rs):
            a = score(rs, "axon_probe", 0.3)[metric]
            b = score(rs, name, threshold)[metric]
            return "" if a == "" or b == "" else a - b
    else:
        def fn(rs):
            return score(rs, name, threshold)[metric]
    return ci(rows, fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", default="traces/stage4_probe.csv")
    ap.add_argument("--out", default="traces/stage4_contest.csv")
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=5)
    args = ap.parse_args()
    rows = load(args.probe, args.shift_at, args.window)
    specs = [
        ("uncertainty_agreement", 0.5),
        ("semantic_entropy", 0.75),
        ("reversed_agreement", 0.8),
        ("reversed_entropy", -0.75),
        ("cling_timing", 0.6),
        ("probe_rule_change", 0.3),
        ("axon_probe", 0.3),
    ]
    # every (method, metric) bootstrap is independent and seeds its own rng, so they
    # run across processes without changing a single number.
    plain = [(rows, name, thr, m, False) for name, thr in specs for m in (0, 1, 2)]
    gaps = [(rows, name, thr, m, True)
            for name, thr in specs if name != "axon_probe" for m in (0, 1, 2)]
    done = pmap(_ci_task, plain + gaps)
    plain_res = {(specs[i // 3][0], i % 3): done[i] for i in range(len(plain))}
    gap_specs = [(n, t) for n, t in specs if n != "axon_probe"]
    gap_res = {(gap_specs[i // 3][0], i % 3): done[len(plain) + i] for i in range(len(gaps))}

    out = []
    for name, threshold in specs:
        (au, au_l, au_h) = plain_res[(name, 0)]
        (prc, prc_l, prc_h) = plain_res[(name, 1)]
        (rec, rec_l, rec_h) = plain_res[(name, 2)]
        out.append({
            "method": name,
            "n": len(rows),
            "threshold": threshold,
            "auroc": au,
            "auroc_low": au_l,
            "auroc_high": au_h,
            "precision": prc,
            "precision_low": prc_l,
            "precision_high": prc_h,
            "recall": rec,
            "recall_low": rec_l,
            "recall_high": rec_h,
        })
    for name, threshold in specs:
        if name == "axon_probe":
            continue
        (au, au_l, au_h) = gap_res[(name, 0)]
        (prc, prc_l, prc_h) = gap_res[(name, 1)]
        (rec, rec_l, rec_h) = gap_res[(name, 2)]
        out.append({
            "method": "axon_probe_minus_" + name,
            "n": len(rows),
            "threshold": "",
            "auroc": au,
            "auroc_low": au_l,
            "auroc_high": au_h,
            "precision": prc,
            "precision_low": prc_l,
            "precision_high": prc_h,
            "recall": rec,
            "recall_low": rec_l,
            "recall_high": rec_h,
        })
    folder = os.path.dirname(args.out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    fields = list(out[0].keys())
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in out:
            for k, v in list(row.items()):
                if isinstance(v, float):
                    row[k] = f"{v:.3f}"
            w.writerow(row)


if __name__ == "__main__":
    main()
