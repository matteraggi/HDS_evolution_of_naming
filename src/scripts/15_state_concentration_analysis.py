"""
For the curated national spike/decline stories only (not the broader candidate
lists - state-level counts are noisy enough that this only makes sense applied
to already-strong, already-verified stories), check whether the jump/collapse
was geographically UNIFORM across states or concentrated in a few.

This doubles as a validation check: a genuine national media event (a movie,
a national TV show, national news) should move most states together; if a
"spike" turns out to be almost entirely one or two states, that's reason to
distrust the national-media explanation - it might be a regional cause, or a
data artifact.

Method: for each story, build a per-state ratio (event-year count / 3-year-
median baseline count), for every state where SSA reports the name in both
periods (small states will be missing for rare names - suppression threshold
applies per state too, so this naturally narrows to states large enough to
have reportable counts). Report: how many states show a comparable jump
(ratio within a factor of 3 of the national ratio), the strongest state, and
the weakest/most-absent state, as evidence for or against a uniform national
effect.

Input: dataset/namesbystate/*.TXT (state,sex,year,name,count)
Output: dataset/processed/state_concentration_results.csv
"""

import csv
import glob
import os
from collections import defaultdict

STATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "namesbystate")
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "state_concentration_results.csv"
)

BASELINE_YEARS = 3

# (name, sex, event_year, label) - the curated, already-verified stories worth this deeper look.
# Positive spikes (national media/celebrity events) and negative declines (scandals) alike.
STORIES = [
    ("Tammy", "F", 1958, "positive"),
    ("Jaime", "F", 1976, "positive"),
    ("Devante", "M", 1992, "positive"),
    ("Mariah", "F", 1991, "positive"),
    ("Nevaeh", "F", 2001, "positive"),
    ("Jaslene", "F", 2008, "positive"),
    ("Hillary", "F", 1993, "negative"),
    ("Kobe", "M", 2004, "negative"),
    ("Alexa", "F", 2020, "negative"),
]


def load_state_series(name: str, sex: str) -> dict:
    """state -> {year: count} for this name/sex, across all state files."""
    series = defaultdict(dict)
    for path in glob.glob(os.path.join(STATE_DIR, "*.TXT")):
        state = os.path.basename(path).replace(".TXT", "")
        with open(path, encoding="utf-8") as f:
            for line in f:
                st, sx, yr, nm, ct = line.strip().split(",")
                if nm == name and sx == sex:
                    series[state][int(yr)] = int(ct)
    return series


def main():
    results = []
    for name, sex, event_year, kind in STORIES:
        series = load_state_series(name, sex)
        state_ratios = {}
        for state, year_counts in series.items():
            prior = [year_counts[y] for y in range(event_year - BASELINE_YEARS, event_year) if y in year_counts]
            if not prior or event_year not in year_counts:
                continue
            baseline = sorted(prior)[len(prior) // 2]
            if baseline <= 0:
                continue
            state_ratios[state] = year_counts[event_year] / baseline

        if not state_ratios:
            print(f"{name} ({event_year}): no usable state-level data, skipping")
            continue

        ratios = list(state_ratios.values())
        national_like_ratio = sorted(ratios)[len(ratios) // 2]  # median across states as a robust central value
        states_moving_same_direction = sum(
            1 for r in ratios if (r > 1.3 if kind == "positive" else r < 0.75)
        )
        top_state = max(state_ratios, key=state_ratios.get)
        bottom_state = min(state_ratios, key=state_ratios.get)

        results.append(
            {
                "name": name,
                "sex": sex,
                "event_year": event_year,
                "kind": kind,
                "n_states_with_data": len(state_ratios),
                "states_moving_same_direction": states_moving_same_direction,
                "pct_states_moving_same_direction": round(100 * states_moving_same_direction / len(state_ratios), 1),
                "median_state_ratio": round(national_like_ratio, 3),
                "top_state": top_state,
                "top_state_ratio": round(state_ratios[top_state], 3),
                "bottom_state": bottom_state,
                "bottom_state_ratio": round(state_ratios[bottom_state], 3),
            }
        )

    fieldnames = list(results[0].keys())
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows -> {OUT_PATH}\n")
    print(f"{'name':10s} {'year':5s} {'kind':9s} {'states':7s} {'same-dir%':10s} {'top':4s} {'bottom':6s}")
    for r in results:
        print(f"{r['name']:10s} {r['event_year']:5d} {r['kind']:9s} {r['n_states_with_data']:7d} "
              f"{r['pct_states_moving_same_direction']:9.1f}% {r['top_state']:4s} {r['bottom_state']:6s}")


if __name__ == "__main__":
    main()
