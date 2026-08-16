"""
Process the raw ISTAT "contanomi" scrape into per-year/sex diversity metrics,
mirroring 01_process_ssa.py's output shape so both countries can feed the same
downstream comparison/trend scripts.

Input:
  dataset/istat/istat_contanomi_full.csv          (year,name,gender,count,percent)
  dataset/istat/contanomi_raw/manifest.csv         (year,limit_used,...,percent_sum)
Output:
  dataset/processed/it_diversity_metrics.csv
    (year, sex, total_births, distinct_names_captured, shannon_entropy,
     top10_share, top30_share, coverage_percent, entropy_reliable)

COVERAGE CAVEAT (important): ISTAT's contanomi web service only returns each year's
top-N names by rank, and N is a real per-year server-side limit (found by binary
search, not something we chose) that varies from ~137 names (2021, worst) to the
full distribution (~25,000 names, 2022-2024). See PROJECT_LOG.md and manifest.csv.

top10_share/top30_share are UNAFFECTED by this: `percent` in the raw data is already
computed by ISTAT against that year's TRUE total births (confirmed: percentages sum
to ~100% in fully-covered years), so summing the top 10/30 captured names' percentages
gives the correct concentration ratio regardless of scrape depth. This is the primary
cross-year Italy metric, valid for the full 1999-2024 window.

shannon_entropy computed here is NOT reliable for partial-coverage years - it
systematically UNDERESTIMATES the true value, missing whatever entropy the untracked
long tail would contribute, and the missing share differs year to year (66-100%
coverage). Only rows with entropy_reliable=True (2022-2024, the only ~complete-
distribution years) should be used for any entropy-based comparison/trend claim.
"""

import csv
import math
import os
from collections import defaultdict

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
MANIFEST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "istat", "contanomi_raw", "manifest.csv"
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_diversity_metrics.csv")

ENTROPY_RELIABLE_MIN_COVERAGE = 99.0  # percent; only ~complete-distribution years are trustworthy for entropy
GENDER_MAP = {"m": "M", "f": "F"}


def shannon_entropy_from_percents(percents):
    h = 0.0
    for pct in percents:
        p = pct / 100.0
        if p <= 0:
            continue
        h -= p * math.log2(p)
    return h


def load_coverage():
    coverage = {}
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            coverage[int(r["year"])] = {
                "M": float(r["male_percent_sum"]),
                "F": float(r["female_percent_sum"]),
            }
    return coverage


def main():
    coverage = load_coverage()

    by_year_sex = defaultdict(list)  # (year, sex) -> list of (name, count, percent)
    with open(RAW_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sex = GENDER_MAP[r["gender"]]
            by_year_sex[(int(r["year"]), sex)].append((r["name"], int(r["count"]), float(r["percent"])))

    rows = []
    for (year, sex), entries in sorted(by_year_sex.items()):
        entries_desc = sorted(entries, key=lambda e: -e[2])  # rank by percent desc (== count desc)
        percents = [e[2] for e in entries_desc]
        counts = [e[1] for e in entries_desc]

        cov = coverage.get(year, {}).get(sex, sum(percents))
        # `percent` is already normalized against the true yearly total, so back out
        # that total from the captured counts and the fraction of it they represent.
        total_births = round(sum(counts) / (cov / 100.0)) if cov > 0 else sum(counts)

        top10_share = sum(percents[:10]) / 100.0
        top30_share = sum(percents[:30]) / 100.0
        h = shannon_entropy_from_percents(percents)
        entropy_reliable = cov >= ENTROPY_RELIABLE_MIN_COVERAGE

        rows.append(
            {
                "year": year,
                "sex": sex,
                "total_births": total_births,
                "distinct_names_captured": len(entries),
                "shannon_entropy": round(h, 6),
                "top10_share": round(top10_share, 6),
                "top30_share": round(top30_share, 6),
                "coverage_percent": round(cov, 4),
                "entropy_reliable": entropy_reliable,
            }
        )

    fieldnames = [
        "year", "sex", "total_births", "distinct_names_captured", "shannon_entropy",
        "top10_share", "top30_share", "coverage_percent", "entropy_reliable",
    ]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    years = sorted(set(r["year"] for r in rows))
    reliable_years = sorted(set(r["year"] for r in rows if r["entropy_reliable"]))
    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")
    print(f"Years covered: {years[0]}-{years[-1]}")
    print(f"Entropy-reliable years (>= {ENTROPY_RELIABLE_MIN_COVERAGE}% coverage): {reliable_years}")


if __name__ == "__main__":
    main()
