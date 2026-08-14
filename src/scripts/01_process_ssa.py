"""
Process raw SSA yobYYYY.txt files into:
  - data/processed/us_names_long.csv        (year, name, sex, count, total_births_sex, rel_freq)
  - data/processed/us_diversity_metrics.csv (year, sex, shannon_entropy, top10_share, top30_share)

Metrics are computed PER SEX (not combined) to match ISTAT's published breakdown,
which reports top-N concentration separately for male/female births (see plan §4).
A "both" row per year is also included (M+F pooled) as a secondary reference figure.

Source: https://www.ssa.gov/oact/babynames/names.zip
Format: one yobYYYY.txt per year, comma-delimited, columns name,sex,count (no header).
Threshold caveat: only names with >=5 births in a given year/sex are included (privacy suppression).
"""

import glob
import math
import os
import re
from collections import defaultdict

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "ssa")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed")
os.makedirs(OUT_DIR, exist_ok=True)


def shannon_entropy(counts):
    total = sum(counts)
    h = 0.0
    for c in counts:
        if c <= 0:
            continue
        p = c / total
        h -= p * math.log2(p)
    return h


def top_n_share(sorted_counts_desc, total, n):
    return sum(sorted_counts_desc[:n]) / total


def metrics_for_group(rows):
    """rows: list of (name, count) for one year/sex group."""
    total = sum(c for _, c in rows)
    counts_desc = sorted((c for _, c in rows), reverse=True)
    h = shannon_entropy(counts_desc)
    top10 = top_n_share(counts_desc, total, 10)
    top30 = top_n_share(counts_desc, total, 30)
    return total, len(rows), h, top10, top30


def main():
    files = sorted(glob.glob(os.path.join(RAW_DIR, "yob*.txt")))
    if not files:
        raise SystemExit(f"No yobYYYY.txt files found in {RAW_DIR}")

    long_rows = []
    metric_rows = []

    for path in files:
        m = re.search(r"yob(\d{4})\.txt$", path)
        year = int(m.group(1))

        by_sex = defaultdict(list)  # sex -> list of (name, count)
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                name, sex, count = line.split(",")
                by_sex[sex].append((name, int(count)))

        sex_totals = {}
        for sex, rows in sorted(by_sex.items()):
            total, distinct, h, top10, top30 = metrics_for_group(rows)
            sex_totals[sex] = total
            metric_rows.append((year, sex, total, distinct, h, top10, top30))
            for name, count in rows:
                long_rows.append((year, name, sex, count, total, count / total))

        # pooled M+F reference row
        pooled_rows = [(name, count) for rows in by_sex.values() for name, count in rows]
        total, distinct, h, top10, top30 = metrics_for_group(pooled_rows)
        metric_rows.append((year, "both", total, distinct, h, top10, top30))

    long_path = os.path.join(OUT_DIR, "us_names_long.csv")
    with open(long_path, "w", encoding="utf-8") as f:
        f.write("year,name,sex,count,total_births_sex,rel_freq\n")
        for year, name, sex, count, total_births_sex, rel_freq in long_rows:
            f.write(f"{year},{name},{sex},{count},{total_births_sex},{rel_freq:.10f}\n")

    metrics_path = os.path.join(OUT_DIR, "us_diversity_metrics.csv")
    with open(metrics_path, "w", encoding="utf-8") as f:
        f.write("year,sex,total_births,distinct_names,shannon_entropy,top10_share,top30_share\n")
        for year, sex, total_births, distinct_names, h, top10, top30 in metric_rows:
            f.write(f"{year},{sex},{total_births},{distinct_names},{h:.6f},{top10:.6f},{top30:.6f}\n")

    years = sorted(set(r[0] for r in metric_rows))
    print(f"Wrote {len(long_rows)} rows -> {long_path}")
    print(f"Wrote {len(metric_rows)} rows -> {metrics_path}")
    print(f"Years covered: {years[0]}-{years[-1]}")


if __name__ == "__main__":
    main()
