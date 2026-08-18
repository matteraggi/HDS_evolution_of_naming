"""
Scan the Italy contanomi data for candidate "event spikes" - same idea as
06_find_us_spikes.py, applied to Italy.

Coverage caveat (not fully solved here, just flagged): each year only captures
that year's top-N names (N varies, see manifest.csv - as low as 137 in the
worst year, 2021). A name missing from a low-coverage year isn't necessarily
proof it had zero births - it may have just fallen outside that year's
captured rank. This script requires an actual baseline data point (not a
missing year treated as zero), which avoids the most obvious false positive,
but every candidate here still needs a manual cross-check against
manifest.csv (is the baseline year's coverage deep enough that this name
would have been captured if present at a similar rank?) before citing it.

Output: dataset/processed/it_spike_candidates.csv
"""

import csv
import os
from collections import defaultdict

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_spike_candidates.csv")

MIN_COUNT = 80
MIN_RATIO = 2.0
BASELINE_YEARS = 3


def main():
    by_name_sex = defaultdict(dict)  # (name, gender) -> {year: count}
    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            by_name_sex[(r["name"], r["gender"])][int(r["year"])] = int(r["count"])

    candidates = []
    for (name, gender), year_counts in by_name_sex.items():
        years_sorted = sorted(year_counts)
        for year in years_sorted:
            count = year_counts[year]
            if count < MIN_COUNT:
                continue
            prior_years = [y for y in years_sorted if y < year][-BASELINE_YEARS:]
            if not prior_years:
                continue
            baseline = sorted(year_counts[y] for y in prior_years)[len(prior_years) // 2]
            if baseline <= 0:
                continue
            ratio = count / baseline
            if ratio >= MIN_RATIO:
                candidates.append(
                    {
                        "name": name,
                        "gender": gender,
                        "year": year,
                        "count": count,
                        "baseline": baseline,
                        "ratio": round(ratio, 2),
                        "score": round(count * ratio, 1),
                    }
                )

    candidates.sort(key=lambda c: -c["score"])

    fieldnames = ["name", "gender", "year", "count", "baseline", "ratio", "score"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(candidates)

    print(f"Wrote {len(candidates)} candidates -> {OUT_PATH}")
    print("\nTop 40 by score:")
    print(f"{'name':15s} {'g':1s} {'year':5s} {'count':7s} {'baseline':9s} {'ratio':6s}")
    for c in candidates[:40]:
        print(f"{c['name']:15s} {c['gender']:1s} {c['year']:5d} {c['count']:7d} {c['baseline']:9d} {c['ratio']:6.2f}")


if __name__ == "__main__":
    main()
