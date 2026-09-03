import argparse
import csv
import glob
import os
import random
from collections import defaultdict
from statistics import mean

from gates import gates, cues_of


def boot(values, reps=5000, seed=4):
    if not values:
        return "", "", ""
    rng = random.Random(seed)
    samples = [mean(values[rng.randrange(len(values))] for _ in values) for _ in range(reps)]
    samples.sort()
    return mean(values), samples[int(reps * 0.025)], samples[int(reps * 0.975)]


def one_episode(path, shift_at, window, name):
    with open(path, newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: int(row["step"]))
    cues = cues_of(rows)
    scored = []
    for index, row in enumerate(rows):
        values = gates(row, rows[:index], cues)
        values["step"] = int(row["step"])
        values["cue"] = row["cue"]
        values["reward"] = int(row["reward"])
        values["phase"] = row.get("phase", "")
        scored.append(values)
    post = [row for row in scored if row["step"] >= shift_at and row["step"] < shift_at + window]
    fires = [row["step"] for row in post if row[name] > 0]
    fire_step = min(fires) if fires else None
    leads, false_alarms, unfailing = [], 0, 0
    for cue in cues:
        cue_rows = [row for row in post if row["cue"] == cue]
        wrong = [row["step"] for row in cue_rows if row["reward"] == 0]
        if wrong:
            if fire_step is not None:
                leads.append(min(wrong) - fire_step)
        else:
            unfailing += 1
            if any(row[name] > 0 for row in cue_rows):
                false_alarms += 1
    return leads, false_alarms, unfailing, int(fire_step is not None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--pattern", required=True)
    parser.add_argument("--shift-at", type=int, required=True)
    parser.add_argument("--window", type=int, required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    paths = sorted(glob.glob(args.pattern))
    output = []
    for name in ["G0_cling", "G1_contradicted"]:
        leads, false_alarms, unfailing, fired = [], 0, 0, 0
        for path in paths:
            current, alarms, never_failed, did_fire = one_episode(
                path, args.shift_at, args.window, name)
            leads.extend(current)
            false_alarms += alarms
            unfailing += never_failed
            fired += did_fire
        value, low, high = boot(leads)
        row = {
            "label": args.label, "gate": name, "episodes": len(paths),
            "episodes_fired": fired, "n_leads": len(leads),
            "mean_lead": value, "lead_low": low, "lead_high": high,
            "frac_positive_lead": (sum(x > 0 for x in leads) / len(leads)) if leads else "",
            "false_alarm_rate": (false_alarms / unfailing) if unfailing else "",
            "unfailing_cues": unfailing,
        }
        output.append(row)
        print(row)
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
