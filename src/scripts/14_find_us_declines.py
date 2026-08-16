"""
Mirror of 06_find_us_spikes.py, but for the opposite phenomenon: names that
suffered a large, sudden year-over-year COLLAPSE, plausibly due to a negative
event tainting the name (a criminal, a scandal, a disaster, a villain).

Significance requires a real pre-collapse baseline (MIN_BASELINE), not just a
big ratio - a name dropping from 3 births to 1 is a 66% "decline" but means
nothing; a name dropping from 2,000 to 400 is a real cultural signal. This is
the mirror-image safeguard of 06's MIN_COUNT filter (there, the post-jump
value had to be substantial; here, the pre-collapse value does).

Output: data/processed/us_decline_candidates.csv, ranked by (baseline * (1-ratio))
so both "big and sudden" and "already-huge-then-cratered" surface near the top.
"""

import csv
import os
from collections import defaultdict

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_decline_candidates.csv")

MIN_BASELINE = 300       # must have been a real, established name before the collapse
MAX_RATIO = 0.5           # lost at least half its births vs. baseline
BASELINE_YEARS = 3


def main():
    by_name_sex = defaultdict(dict)
    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_name_sex[(r["name"], r["sex"])][int(r["year"])] = int(r["count"])

    candidates = []
    for (name, sex), year_counts in by_name_sex.items():
        years_sorted = sorted(year_counts)
        for year in years_sorted:
            count = year_counts[year]
            prior_years = [y for y in years_sorted if y < year][-BASELINE_YEARS:]
            if not prior_years:
                continue
            baseline = sorted(year_counts[y] for y in prior_years)[len(prior_years) // 2]
            if baseline < MIN_BASELINE:
                continue
            ratio = count / baseline
            if ratio <= MAX_RATIO:
                candidates.append(
                    {
                        "name": name,
                        "sex": sex,
                        "year": year,
                        "count": count,
                        "baseline": baseline,
                        "ratio": round(ratio, 3),
                        "births_lost": baseline - count,
                        "score": round(baseline * (1 - ratio), 1),
                    }
                )

    candidates.sort(key=lambda c: -c["score"])

    fieldnames = ["name", "sex", "year", "count", "baseline", "ratio", "births_lost", "score"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"Wrote {len(candidates)} candidates -> {OUT_PATH}")
    print("\nTop 40 by score:")
    print(f"{'name':15s} {'sex':3s} {'year':5s} {'count':7s} {'baseline':9s} {'ratio':6s} {'lost':7s}")
    for c in candidates[:40]:
        print(f"{c['name']:15s} {c['sex']:3s} {c['year']:5d} {c['count']:7d} {c['baseline']:9d} "
              f"{c['ratio']:6.3f} {c['births_lost']:7d}")


if __name__ == "__main__":
    main()
