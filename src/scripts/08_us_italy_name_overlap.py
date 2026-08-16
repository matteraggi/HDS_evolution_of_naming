"""
Quantify how much the US and Italy's popular-name pools have converged or
diverged over time: for each year 1999-2024 and each sex, compute what
fraction of the two countries' top-30 name lists overlap, then trend that
fraction over time (converging = increasing overlap, diverging = decreasing).

Also prints the actual overlapping names for the first and last years in the
window, as concrete "border-crossing" examples to cite alongside the trend
number (e.g. "Sophia/Sofia top-30 in both countries by 2024" is a much better
sentence than just the percentage).

Requires:
  dataset/processed/us_names_long.csv           (from 01_process_ssa.py)
  dataset/istat/istat_contanomi_full.csv    (from 00_scrape_istat_contanomi.py)

Output: dataset/processed/us_italy_name_overlap.csv (year, sex, overlap_count, overlap_pct, shared_names)
"""

import csv
import os
import unicodedata
from collections import defaultdict

import pymannkendall as mk

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_italy_name_overlap.csv")

SEX_MAP = {"M": "m", "F": "f"}  # US sex code -> Italy gender code
TOP_N = 30


def normalize(name: str) -> str:
    # Strip accents/apostrophes/spacing so e.g. "NICOLO'" (Italy) and "Nicolo" (US) can match,
    # and Italian compound names like "FRANCESCO PIO" collapse consistently.
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def load_us_top30_by_year_sex():
    counts = defaultdict(lambda: defaultdict(int))  # (year, sex) -> name -> count
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            counts[(int(r["year"]), r["sex"])][normalize(r["name"])] += int(r["count"])
    top30 = {}
    for key, name_counts in counts.items():
        ranked = sorted(name_counts.items(), key=lambda kv: -kv[1])
        top30[key] = set(n for n, _ in ranked[:TOP_N])
    return top30


def load_it_top30_by_year_gender():
    counts = defaultdict(lambda: defaultdict(int))  # (year, gender) -> name -> count
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            counts[(int(r["year"]), r["gender"])][normalize(r["name"])] += int(r["count"])
    top30 = {}
    for key, name_counts in counts.items():
        ranked = sorted(name_counts.items(), key=lambda kv: -kv[1])
        top30[key] = set(n for n, _ in ranked[:TOP_N])
    return top30


def main():
    us_top30 = load_us_top30_by_year_sex()
    it_top30 = load_it_top30_by_year_gender()

    it_years = sorted(set(y for y, _ in it_top30))
    rows = []
    for year in it_years:
        for us_sex, it_gender in SEX_MAP.items():
            us_set = us_top30.get((year, us_sex))
            it_set = it_top30.get((year, it_gender))
            if not us_set or not it_set:
                continue
            shared = us_set & it_set
            overlap_pct = len(shared) / TOP_N
            rows.append(
                {
                    "year": year,
                    "sex": us_sex,
                    "overlap_count": len(shared),
                    "overlap_pct": round(overlap_pct, 4),
                    "shared_names": ";".join(sorted(shared)),
                }
            )

    fieldnames = ["year", "sex", "overlap_count", "overlap_pct", "shared_names"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")

    for sex in ("M", "F"):
        series = [r["overlap_count"] for r in rows if r["sex"] == sex]
        years = [r["year"] for r in rows if r["sex"] == sex]
        if len(series) >= 4:
            res = mk.original_test(series)
            print(f"\nsex={sex}: Mann-Kendall on top-30 overlap count, {years[0]}-{years[-1]}, n={len(series)}")
            print(f"  trend={res.trend} p={res.p:.4g} tau={res.Tau:.3f} sens_slope={res.slope:.4f} names/year")

        first = next(r for r in rows if r["sex"] == sex and r["year"] == years[0])
        last = next(r for r in rows if r["sex"] == sex and r["year"] == years[-1])
        print(f"  {years[0]}: {first['overlap_count']}/{TOP_N} shared -> {first['shared_names']}")
        print(f"  {years[-1]}: {last['overlap_count']}/{TOP_N} shared -> {last['shared_names']}")


if __name__ == "__main__":
    main()
