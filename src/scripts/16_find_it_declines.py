"""
Mirror of 14_find_us_declines.py, applied to Italy - same logic (year-over-year
collapse vs. 3-year median baseline, with a minimum pre-collapse baseline count
so we're not catching noise), scaled down to Italy's smaller population and
the contanomi scrape's coverage limits.

Output: dataset/processed/it_decline_candidates.csv
"""

import csv
import os
from collections import defaultdict

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_decline_candidates.csv")

MIN_BASELINE = 100
MAX_RATIO = 0.5
BASELINE_YEARS = 3


def main():
    by_name_sex = defaultdict(dict)
    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_name_sex[(r["name"], r["gender"])][int(r["year"])] = int(r["count"])

    candidates = []
    for (name, gender), year_counts in by_name_sex.items():
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
                        "gender": gender,
                        "year": year,
                        "count": count,
                        "baseline": baseline,
                        "ratio": round(ratio, 3),
                        "births_lost": baseline - count,
                        "score": round(baseline * (1 - ratio), 1),
                    }
                )

    candidates.sort(key=lambda c: -c["score"])

    fieldnames = ["name", "gender", "year", "count", "baseline", "ratio", "births_lost", "score"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(candidates)

    print(f"Wrote {len(candidates)} candidates -> {OUT_PATH}")
    print("\nTop 40 by score:")
    print(f"{'name':15s} {'g':1s} {'year':5s} {'count':7s} {'baseline':9s} {'ratio':6s} {'lost':6s}")
    for c in candidates[:40]:
        print(f"{c['name']:15s} {c['gender']:1s} {c['year']:5d} {c['count']:7d} {c['baseline']:9d} "
              f"{c['ratio']:6.3f} {c['births_lost']:6d}")


if __name__ == "__main__":
    main()
