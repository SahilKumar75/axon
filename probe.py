import argparse
import csv
import glob
import os
import re
from collections import Counter, defaultdict

from concurrent.futures import ThreadPoolExecutor

from model import chat_many


KEYS = ("A", "B", "C")
CUES = ("blue", "red", "green")
SYSTEM = "Output exactly YES or NO. No other words."


def believed_rule(past):
    """Infer the model's OWN currently-held rule per cue from its past chosen
    answers (mode), using only rows strictly before the current one. Never
    reads the environment's true rule -- that was the oracle confound."""
    per_cue = defaultdict(list)
    for r in past:
        per_cue[r["cue"]].append(r["chosen"])
    believed = {}
    for cue in CUES:
        votes = per_cue.get(cue)
        believed[cue] = Counter(votes).most_common(1)[0][0] if votes else None
    return believed


def forms_for(believed, h):
    b, r, g = believed["blue"], believed["red"], believed["green"]
    bv = "/".join(k for k in KEYS if k != b)
    rv = "/".join(k for k in KEYS if k != r)
    gv = "/".join(k for k in KEYS if k != g)
    bv2 = " or ".join(k for k in KEYS if k != b)
    rv2 = " or ".join(k for k in KEYS if k != r)
    gv2 = " or ".join(k for k in KEYS if k != g)
    return [
        f"Believed rule: blue -> {b}, red -> {r}, green -> {g}. A contradiction is blue not {b}, red not {r}, or green not {g}.\nTrials:\n{h}\nDoes any trial contradict the believed rule. YES or NO.",
        f"Check every trial against believed rule blue {b}, red {r}, green {g}. If any line has blue -> {bv}, red -> {rv}, or green -> {gv}, answer YES.\n{h}\nYES or NO.",
        f"Believed rule violations: blue -> {bv2}, red -> {rv2}, green -> {gv2}.\nTrials:\n{h}\nIs there any violation. YES or NO.",
    ]


def condition(path):
    name = os.path.basename(path).lower()
    return "steady" if "steady" in name else "shift"


def seed(path):
    m = re.search(r"seed(\d+)", os.path.basename(path))
    return m.group(1) if m else ""


def history(rows):
    if not rows:
        return "none"
    return "\n".join([f"{r['step']}: {r['cue']} -> {r['correct']}" for r in rows])


def changed(text):
    t = text.upper()
    if re.search(r"\bYES\b", t):
        return "YES"
    if re.search(r"\bNO\b", t):
        return "NO"
    return ""


def row_probe(row, past, k, model):
    believed = believed_rule(past)
    if any(v is None for v in believed.values()):
        # not enough history to know the model's own belief for every cue yet --
        # skip rather than guess (and skip the API call entirely: free).
        return None, [], "", "", [], True
    h = history(past)
    forms = forms_for(believed, h)
    picks = [forms[i % len(forms)] for i in range(k)]
    texts = chat_many(picks, model, temperature=0, max_tokens=8, system=SYSTEM)
    old = believed[row["cue"]]
    votes = [changed(text) for text in texts if changed(text)]
    change_score = sum(v == "YES" for v in votes) / len(votes) if votes else 0
    stale = change_score if row["chosen"] == old else 0
    return old, votes, change_score, stale, texts, False


def _file_rows(path, k, model):
    """Probe one trace file; returns its output rows in step order.

    Files are independent of each other -- `past` only ever accumulates within
    a single episode -- so files can be probed concurrently."""
    cond = condition(path)
    sd = seed(path)
    past = []
    rows_out = []
    with open(path, newline="") as in_file:
        for row in csv.DictReader(in_file):
            old, currents, changed, stale, texts, insufficient = row_probe(row, past, k, model)
            rows_out.append({
                "path": path,
                "condition": cond,
                "seed": sd,
                "step": row["step"],
                "phase": row["phase"],
                "cue": row["cue"],
                "chosen": row["chosen"],
                "correct": row["correct"],
                "insufficient_history": int(insufficient),
                "reward": row["reward"],
                "agreement": row["agreement"],
                "branches": row["branches"],
                "old": old if old is not None else "",
                "currents": "|".join(currents),
                "change_score": "" if changed == "" else f"{changed:.3f}",
                "stale_score": "" if stale == "" else f"{stale:.3f}",
                "probe_pairs": "|".join(currents),
                "probe_text": "|".join([text.replace("\n", " ") for text in texts]),
            })
            past.append(row)
    return rows_out


def run(paths, out, k, model, workers=6):
    fields = [
        "path", "condition", "seed", "step", "phase", "cue", "chosen", "correct",
        "reward", "agreement", "branches", "old", "currents", "change_score",
        "stale_score", "probe_pairs", "probe_text", "insufficient_history",
    ]
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    if workers > 1 and len(paths) > 1:
        with ThreadPoolExecutor(max_workers=min(workers, len(paths))) as pool:
            per_file = list(pool.map(lambda p: _file_rows(p, k, model), paths))
    else:
        per_file = [_file_rows(p, k, model) for p in paths]
    with open(out, "w", newline="") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=fields)
        writer.writeheader()
        for rows_out in per_file:
            writer.writerows(rows_out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--out", default="traces/stage4_probe.csv")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--model", default="meta-llama/llama-3.1-8b-instruct")
    args = ap.parse_args()
    paths = args.paths or sorted(glob.glob("traces/stage2_final/*.csv"))
    run(paths, args.out, args.k, args.model)


if __name__ == "__main__":
    main()
