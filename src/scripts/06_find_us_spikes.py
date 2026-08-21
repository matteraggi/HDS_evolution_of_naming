"""
Scan the US SSA data for candidate "event spikes" - names with a large, sudden
year-over-year jump - to shortlist for the paper's spike-story section.

This is a candidate-finder, not a verifier: it flags statistical jumps; a human
(or a quick web search) still has to confirm each one actually maps to a real
movie/show/celebrity/event before it's usable in the paper.

Method: for each name/sex with count >= MIN_COUNT in year Y, compare against a
baseline (median of the prior 3 years, or the prior year if a name is new).
Flag ratio >= MIN_RATIO. Filters out tiny counts so we don't surface noise from
names jumping from 5 to 15 births.

Output: dataset/processed/us_spike_candidates.csv, ranked by (count_after * ratio)
so both "big and sudden" and "huge and dramatic" jumps surface near the top.
"""

import csv
import os
from collections import defaultdict

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_spike_candidates.csv")
# note: numbered 06 (not 04) to avoid clashing with the existing 04_plot_us_entropy.py

MIN_COUNT = 150          # ignore tiny-count noise
MIN_RATIO = 2.5          # at least 2.5x jump over baseline
BASELINE_YEARS = 3       # median of the prior N years as baseline


def main():
    by_name_sex = defaultdict(dict)  # (name, sex) -> {year: count}
    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_name_sex[(r["name"], r["sex"])][int(r["year"])] = int(r["count"])

    candidates = []
    for (name, sex), year_counts in by_name_sex.items():
        years_sorted = sorted(year_counts)
        for i, year in enumerate(years_sorted):
            count = year_counts[year]
            if count < MIN_COUNT:
                continue
            prior_years = [y for y in years_sorted if y < year][-BASELINE_YEARS:]
            if not prior_years:
                continue  # no baseline (name's first appearance) - not a "jump", just an entry
            baseline = sorted(year_counts[y] for y in prior_years)[len(prior_years) // 2]  # median
            if baseline <= 0:
                continue
            ratio = count / baseline
            if ratio >= MIN_RATIO:
                candidates.append(
                    {
                        "name": name,
                        "sex": sex,
                        "year": year,
                        "count": count,
                        "baseline": baseline,
                        "ratio": round(ratio, 2),
                        "score": round(count * ratio, 1),
                    }
                )

    candidates.sort(key=lambda c: -c["score"])

    fieldnames = ["name", "sex", "year", "count", "baseline", "ratio", "score"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(candidates)

    print(f"Wrote {len(candidates)} candidates -> {OUT_PATH}")
    print(f"\nTop 40 by score:")
    print(f"{'name':15s} {'sex':3s} {'year':5s} {'count':7s} {'baseline':9s} {'ratio':6s}")
    for c in candidates[:40]:
        print(f"{c['name']:15s} {c['sex']:3s} {c['year']:5d} {c['count']:7d} {c['baseline']:9d} {c['ratio']:6.2f}")


if __name__ == "__main__":
    main()
