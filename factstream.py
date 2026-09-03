"""Second testbed: a fact update stream.

Same question as RuleShift -- can the detector see a confidently wrong agent after
the world changes under it -- but deliberately unlike RuleShift in the ways most
likely to break the gate:

  twelve entities instead of three cues        belief spread much thinner
  six answers instead of three                 larger space, weaker guessing
  zipf arrival instead of uniform              rare entities carry almost no evidence
  natural language items                       not colour cues

The agent is told nothing. It learns which answer belongs to which entity from
reward alone, and partway through the stream some entities change answer.

Emits exactly the columns run.py emits, with `cue` holding the entity name, so
gates.py, contest.py, cling.py and leadtime.py all run against it unchanged. If
the gate needed new code to work here, it would not have generalised.
"""

import argparse
import csv
import os
import random
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from model import chat_many

ENTITIES = [
    "Acme Corp", "Borealis Ltd", "Cascade Group", "Dovetail Inc",
    "Eastgate Trust", "Fairwind Co", "Granite Holdings", "Harbour Works",
    "Ivory Systems", "Junction Labs", "Keystone Partners", "Lantern Industries",
]
ANSWERS = ["Kim", "Lee", "Navarro", "Okafor", "Petrov", "Quinn"]


def zipf_weights(n):
    """1/rank. Head entities appear often, tail entities barely at all."""
    return [1.0 / (i + 1) for i in range(n)]


class FactStream:
    def __init__(self, seed=0, steps=40, shift_at=20, shift=True, changed_frac=1.0):
        self.rng = random.Random(seed)
        self.steps = steps
        self.shift_at = shift_at
        self.shift = shift
        self.weights = zipf_weights(len(ENTITIES))

        self.pre = {e: self.rng.choice(ANSWERS) for e in ENTITIES}
        self.post = dict(self.pre)
        if shift:
            n_changed = max(1, round(changed_frac * len(ENTITIES)))
            for e in self.rng.sample(ENTITIES, n_changed):
                self.post[e] = self.rng.choice([a for a in ANSWERS if a != self.pre[e]])

        self.step_i = 0
        self.current = None

    def truth(self):
        return self.pre if self.step_i < self.shift_at else self.post

    def reset(self):
        self.current = self.rng.choices(ENTITIES, weights=self.weights)[0]
        return self.current

    def step(self, chosen):
        correct = self.truth()[self.current]
        reward = int(chosen == correct)
        info = {
            "step": self.step_i,
            "phase": "pre" if self.step_i < self.shift_at else "post",
            "correct": correct,
        }
        self.step_i += 1
        if self.step_i >= self.steps:
            return None, reward, True, info
        self.current = self.rng.choices(ENTITIES, weights=self.weights)[0]
        return self.current, reward, False, info


SYSTEM = "Answer with exactly one name from the list. No other words."


def variants(entity, k, history):
    """k paraphrases of the same question, each carrying the same feedback history.

    Same role as shake.variants in RuleShift: the spread across them is the
    agreement signal the uncertainty baselines are built from."""
    seen = [h for h in history if h["cue"] == entity][-6:]
    log = "; ".join(f"{h['chosen']} was {'right' if int(h['reward']) else 'wrong'}"
                    for h in seen) or "no attempts yet"
    options = ", ".join(ANSWERS)
    stems = [
        f"Who leads {entity}? Options: {options}. Past attempts for {entity}: {log}.",
        f"Name the current head of {entity}. Choose one of: {options}. History for {entity}: {log}.",
        f"For {entity}, which of {options} is correct right now? Earlier: {log}.",
        f"{entity} -- pick the right name from {options}. Feedback so far: {log}.",
        f"Given the record ({log}), who currently leads {entity}? One of: {options}.",
    ]
    return [stems[i % len(stems)] for i in range(k)]


def parse_answer(text):
    t = (text or "").strip().lower()
    for a in ANSWERS:
        if a.lower() in t:
            return a
    return ANSWERS[0]


def run(seed, steps, shift_at, shift, k, model, out, changed_frac=1.0):
    env = FactStream(seed=seed, steps=steps, shift_at=shift_at, shift=shift,
                     changed_frac=changed_frac)
    entity = env.reset()
    rows, history = [], []
    while entity is not None:
        answers = [parse_answer(t) for t in chat_many(
            variants(entity, k, history), model, max_tokens=6, system=SYSTEM)]
        chosen = Counter(answers).most_common(1)[0][0]
        agreement = answers.count(chosen) / len(answers)
        asked = entity
        entity, reward, done, info = env.step(chosen)
        row = {
            "step": info["step"],
            "phase": info["phase"],
            "cue": asked,
            "chosen": chosen,
            "correct": info["correct"],
            "reward": reward,
            "agreement": round(agreement, 3),
            "branches": "|".join(answers),
        }
        rows.append(row)
        history.append(row)
    folder = os.path.dirname(out)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--steps", type=int, default=40)
    ap.add_argument("--shift_at", type=int, default=20)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--changed_frac", type=float, default=1.0)
    ap.add_argument("--model", default="meta-llama/llama-3.3-70b-instruct")
    ap.add_argument("--out_dir", default="traces/stage6_factstream")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    jobs = [(s, os.path.join(args.out_dir, f"shift_seed{s}.csv")) for s in range(args.seeds)]

    def one(job):
        seed, out = job
        run(seed, args.steps, args.shift_at, True, args.k, args.model, out,
            changed_frac=args.changed_frac)
        return out

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for i, done in enumerate(pool.map(one, jobs), 1):
            print(f"[{i}/{len(jobs)}] {done}", flush=True)


if __name__ == "__main__":
    main()
