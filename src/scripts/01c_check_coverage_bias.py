"""
Quantify the bias that ISTAT contanomi's per-year coverage limit (see 01b's docstring
and dataset/istat/contanomi_raw/manifest.csv) introduces into each Italy metric.

Method: 2023 and 2024 are the only years with the TRUE complete distribution. This
script artificially truncates their full name lists down to each depth that some
other year was actually capped at, recomputes top10_share/top30_share/shannon_entropy
on the truncated slice, and compares against the true (full-distribution) value. That
gives a real, empirical bias measurement per depth - not a theoretical guess - for
exactly the depths this project's data actually hits.

Output: dataset/processed/it_coverage_bias_check.csv
    (depth, mean_top10_share_bias, mean_top30_share_bias, mean_entropy_bias,
     mean_entropy_bias_percent)

Finding (see PROJECT_LOG.md): top10/top30 share bias is EXACTLY zero at every tested
depth (137-5577) - these metrics only depend on the top 30 ranks, which every year's
scrape reaches regardless of its cap, so they're safe to use across the full 1999-2024
window. Shannon entropy bias is severe and monotonic: -50% relative at depth=137
(2021, the worst year) down to -19% even at depth=5577 (2000, the best non-complete
year) - confirming entropy must stay restricted to the 2022-2024 rows flagged
entropy_reliable=True in it_diversity_metrics.csv; no partial-coverage year is safe
to use for entropy, even the best-covered ones.
"""

import csv
import math
import os
from collections import defaultdict

RAW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
MANIFEST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "istat", "contanomi_raw", "manifest.csv"
)
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_coverage_bias_check.csv"
)
REFERENCE_YEARS = ("2023", "2024")  # the only years with the true complete distribution


def entropy(percents):
    h = 0.0
    for pct in percents:
        p = pct / 100.0
        if p > 0:
            h -= p * math.log2(p)
    return h


def load_reference_distributions():
    by_year_sex = defaultdict(list)
    with open(RAW_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["year"] in REFERENCE_YEARS:
                by_year_sex[(r["year"], r["gender"])].append(float(r["percent"]))
    return {k: sorted(v, reverse=True) for k, v in by_year_sex.items()}


def load_actual_depths():
    depths = set()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["limit_used"] != "cached":
                depths.add(int(r["limit_used"]))
    return sorted(depths)


def main():
    depths = load_actual_depths()
    reference = load_reference_distributions()

    rows = []
    for depth in depths:
        top10_deltas, top30_deltas, h_biases, h_bias_pcts = [], [], [], []
        for percents_full in reference.values():
            full_top10 = sum(percents_full[:10]) / 100.0
            full_top30 = sum(percents_full[:30]) / 100.0
            full_h = entropy(percents_full)

            truncated = percents_full[:depth]
            trunc_top10 = sum(truncated[:10]) / 100.0
            trunc_top30 = sum(truncated[:30]) / 100.0
            trunc_h = entropy(truncated)

            top10_deltas.append(trunc_top10 - full_top10)
            top30_deltas.append(trunc_top30 - full_top30)
            h_biases.append(trunc_h - full_h)
            h_bias_pcts.append(100 * (trunc_h - full_h) / full_h)

        n = len(top10_deltas)
        rows.append(
            {
                "depth": depth,
                "mean_top10_share_bias": round(sum(top10_deltas) / n, 8),
                "mean_top30_share_bias": round(sum(top30_deltas) / n, 8),
                "mean_entropy_bias_bits": round(sum(h_biases) / n, 4),
                "mean_entropy_bias_percent": round(sum(h_bias_pcts) / n, 2),
            }
        )

    fieldnames = ["depth", "mean_top10_share_bias", "mean_top30_share_bias",
                  "mean_entropy_bias_bits", "mean_entropy_bias_percent"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")
    print(f"{'depth':>6} {'top10_bias':>12} {'top30_bias':>12} {'H_bias_bits':>12} {'H_bias_%':>10}")
    for r in rows:
        print(f"{r['depth']:6d} {r['mean_top10_share_bias']:12.8f} {r['mean_top30_share_bias']:12.8f} "
              f"{r['mean_entropy_bias_bits']:12.4f} {r['mean_entropy_bias_percent']:9.2f}%")


if __name__ == "__main__":
    main()
