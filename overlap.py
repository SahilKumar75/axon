import argparse
import glob
import os
from concurrent.futures import ThreadPoolExecutor

import probe
import run as run_mod


# overlap level = how many of the three cues keep their pre-shift key.
# 0 is the full shift (the original Stage 2/4 condition), included here so every
# level is measured at the same n instead of being compared to the old 5-episode run.
LEVELS = {
    0: [set()],
    1: [{"blue"}, {"red"}, {"green"}],
    2: [{"blue", "red"}, {"blue", "green"}, {"red", "green"}],
}


def label(combo):
    return "-".join(sorted(combo)) if combo else "none"


def generate(seeds, steps, shift_at, k, model, out_dir, workers=6):
    os.makedirs(out_dir, exist_ok=True)
    jobs = []
    paths_by_level = {}
    seeds = list(seeds)
    # every level gets the same episode count, so a level with fewer cue
    # combinations simply spreads more seeds over the ones it has.
    per_level = len(seeds) * max(len(c) for c in LEVELS.values())
    for level, combos in LEVELS.items():
        paths = []
        n_seeds = per_level // len(combos)
        for combo in combos:
            for seed in range(n_seeds):
                out = os.path.join(out_dir, f"ov{level}_{label(combo)}_seed{seed}.csv")
                jobs.append((seed, combo, out))
                paths.append(out)
        paths_by_level[level] = paths

    # episodes are fully independent (own env, own seed, own file), so they run
    # concurrently; the step loop inside one episode stays sequential.
    def one(job):
        seed, combo, out = job
        run_mod.run(seed, steps, shift_at, True, k, model, out, unchanged_cues=frozenset(combo))
        return out

    with ThreadPoolExecutor(max_workers=workers) as pool:
        for i, done in enumerate(pool.map(one, jobs), 1):
            print(f"[{i}/{len(jobs)}] {done}", flush=True)
    return paths_by_level


def probe_and_score(paths_by_level, out_dir, probe_k, model, shift_at, window, workers=6):
    for level, paths in paths_by_level.items():
        probe_out = os.path.join(out_dir, f"ov{level}_probe.csv")
        probe.run(sorted(paths), probe_out, probe_k, model, workers=workers)
        print(level, "probed ->", probe_out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=10)
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--shift_at", type=int, default=10)
    ap.add_argument("--window", type=int, default=8)
    ap.add_argument("--k", type=int, default=5, help="branch samples per run step")
    ap.add_argument("--probe_k", type=int, default=3, help="probe variants per row")
    ap.add_argument("--model", default="meta-llama/llama-3.1-8b-instruct")
    ap.add_argument("--out_dir", default="traces/stage4b_overlap")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--skip_generate", action="store_true", help="reuse existing trace files in out_dir")
    args = ap.parse_args()

    if args.skip_generate:
        paths_by_level = {
            level: sorted(glob.glob(os.path.join(args.out_dir, f"ov{level}_*_seed*.csv")))
            for level in LEVELS
        }
    else:
        paths_by_level = generate(range(args.seeds), args.steps, args.shift_at, args.k, args.model, args.out_dir, args.workers)

    for level, paths in paths_by_level.items():
        print(level, "episodes:", len(paths))

    probe_and_score(paths_by_level, args.out_dir, args.probe_k, args.model, args.shift_at, args.window, args.workers)
    print("Next: run contest.py per level, e.g.")
    for level in LEVELS:
        print(f"  python3 contest.py --probe {args.out_dir}/ov{level}_probe.csv "
              f"--out {args.out_dir}/ov{level}_contest.csv --shift_at {args.shift_at} --window {args.window}")


if __name__ == "__main__":
    main()
