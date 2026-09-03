import os
import csv
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from env import RuleShift
from model import chat_many
from shake import variants, parse_key


def run(seed, steps, shift_at, shift, k, model, out, unchanged_cues=frozenset()):
    env = RuleShift(seed=seed, steps=steps, shift_at=shift_at, shift=shift, unchanged_cues=unchanged_cues)
    cue = env.reset()
    rows = []
    history = []
    while cue is not None:
        answers = [parse_key(t) for t in chat_many(variants(cue, k, history), model)]
        chosen = Counter(answers).most_common(1)[0][0]
        agreement = answers.count(chosen) / len(answers)
        cue_now = cue
        cue, reward, done, info = env.step(chosen)
        row = {
            "step": info["step"],
            "phase": info["phase"],
            "cue": cue_now,
            "chosen": chosen,
            "correct": info["correct"],
            "reward": reward,
            "agreement": round(agreement, 3),
            "branches": "|".join(answers),
        }
        rows.append(row)
        history.append(row)
    write(out, rows)
    return rows


def write(path, rows):
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_many(seeds, steps, shift_at, shift, k, model, out_dir, unchanged_cues=frozenset(),
             workers=6, tag="run"):
    """Generate several episodes concurrently, one file each.

    Episodes are fully independent -- own env, own seed, own output file -- so only the
    step loop inside an episode has to stay sequential. Needed for cross scale, where the
    same sweep gets repeated per model."""
    os.makedirs(out_dir, exist_ok=True)
    jobs = [(seed, os.path.join(out_dir, f"{tag}_seed{seed}.csv")) for seed in seeds]

    def one(job):
        seed, out = job
        run(seed, steps, shift_at, shift, k, model, out, unchanged_cues=unchanged_cues)
        return out

    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(one, jobs))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--seeds", type=int, default=0,
                    help="generate this many episodes (seeds 0..n-1) into --out_dir")
    ap.add_argument("--out_dir", default="traces/run")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--steady", action="store_true")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--model", default="meta-llama/llama-3.1-8b-instruct")
    ap.add_argument("--out", default="traces/run.csv")
    ap.add_argument("--unchanged", default="", help="comma-separated cues held fixed at shift, e.g. blue,green")
    a = ap.parse_args()
    unchanged = frozenset(c for c in a.unchanged.split(",") if c)
    if a.seeds:
        paths = run_many(range(a.seeds), a.steps, a.shift_at, not a.steady, a.k, a.model,
                         a.out_dir, unchanged_cues=unchanged, workers=a.workers,
                         tag="steady" if a.steady else "shift")
        print(len(paths), "episodes ->", a.out_dir)
    else:
        rows = run(a.seed, a.steps, a.shift_at, not a.steady, a.k, a.model, a.out,
                   unchanged_cues=unchanged)
        print(len(rows), "steps ->", a.out)
