"""
Statistical comparison of the US vs Italy concentration-ratio trend, 1999-2025 overlap window.

Requires:
  - dataset/processed/us_diversity_metrics.csv       (from 01_process_ssa.py)
  - dataset/processed/it_diversity_metrics.csv       (from 01b_process_istat_contanomi.py, built from
                                                     the ISTAT contanomi scrape)

Italy's share metrics now come from the full 1999-2024 contanomi scrape rather than the manual
top-30-table collection (dataset/istat/istat_annual_top_names.csv, kept for corroboration/citation
- see COLLECTION_NOTES.md) that could only reach 2006-2024 with gaps. Coverage varies by year
(66-100%, see dataset/istat/contanomi_raw/manifest.csv) but top10/top50 share is unaffected by that
- see 01b's docstring for why. Years missing from either country's file are dropped from the paired
comparison; this script reports how many usable year-pairs remain per sex.

2026-08-24: runs the full comparison for BOTH top10_share and top50_share (decision in
PROJECT_LOG.md - both are primary reported metrics now, not just one). Output rows are
now keyed by (sex, metric) instead of just sex.

Tests run, per (sex, metric):
  1. Mann-Kendall trend test on each country's series over the years both have data (sanity check that
     the reduced/paired sample still shows the same direction as the full-sample MK results).
  2. Mann-Kendall trend test on the DIFFERENCE series (US - Italy) -- tests whether the US/Italy gap in
     concentration is itself significantly widening or narrowing over time.
  3. Wilcoxon signed-rank test on paired annual values -- tests whether US concentration is systematically
     higher or lower than Italy's across the overlap (a level comparison, not a trend comparison).
  4. Percentile-bootstrap 95% CI on each country's Sen's slope (resample residuals around the Theil-Sen
     fit, refit, 2000 iterations) -- non-overlapping CIs are reported as an informal signal that the two
     trend slopes differ.

Reference: Mann (1945), Kendall (1975) for MK; Wilcoxon (1945) for the signed-rank test.
"""

import csv
import os
import random

import pymannkendall as mk
from scipy.stats import wilcoxon, theilslopes

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_diversity_metrics.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_diversity_metrics.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_italy_comparison.csv")

N_BOOTSTRAP = 2000
random.seed(42)
METRICS = ["top10_share", "top50_share"]


def load_us(metric):
    with open(US_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {(int(r["year"]), r["sex"]): float(r[metric]) for r in rows}


def load_italy(metric):
    if not os.path.exists(IT_PATH):
        return {}
    with open(IT_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return {(int(r["year"]), r["sex"]): float(r[metric]) for r in rows}


def bootstrap_slope_ci(years, values):
    slope, intercept, _, _ = theilslopes(values, years)
    fitted = [intercept + slope * y for y in years]
    residuals = [v - f for v, f in zip(values, fitted)]
    boot_slopes = []
    n = len(years)
    for _ in range(N_BOOTSTRAP):
        resampled_resid = [random.choice(residuals) for _ in range(n)]
        boot_values = [f + r for f, r in zip(fitted, resampled_resid)]
        s, *_ = theilslopes(boot_values, years)
        boot_slopes.append(s)
    boot_slopes.sort()
    lo = boot_slopes[int(0.025 * N_BOOTSTRAP)]
    hi = boot_slopes[int(0.975 * N_BOOTSTRAP)]
    return slope, lo, hi


def main():
    results = []
    for metric in METRICS:
        us = load_us(metric)
        it = load_italy(metric)

        if not it:
            print(f"No Italy data found at {IT_PATH} yet -- run 00_scrape_istat_contanomi.py then "
                  f"01b_process_istat_contanomi.py first.")
            return

        for sex in ("M", "F"):
            paired_years = sorted(y for (y, s) in us if s == sex and (y, sex) in it and 1999 <= y <= 2025)
            if len(paired_years) < 4:
                print(f"metric={metric} sex={sex}: only {len(paired_years)} paired years available, skipping (need >=4).")
                continue

            us_vals = [us[(y, sex)] for y in paired_years]
            it_vals = [it[(y, sex)] for y in paired_years]
            diff_vals = [u - i for u, i in zip(us_vals, it_vals)]

            us_mk = mk.original_test(us_vals)
            it_mk = mk.original_test(it_vals)
            diff_mk = mk.original_test(diff_vals)
            w_stat, w_p = wilcoxon(us_vals, it_vals)

            us_slope, us_lo, us_hi = bootstrap_slope_ci(paired_years, us_vals)
            it_slope, it_lo, it_hi = bootstrap_slope_ci(paired_years, it_vals)
            ci_overlap = not (us_hi < it_lo or it_hi < us_lo)

            results.append({
                "metric": metric, "sex": sex, "n_years": len(paired_years),
                "years_range": f"{paired_years[0]}-{paired_years[-1]}",
                "us_trend": us_mk.trend, "us_p": us_mk.p, "us_sen_slope": us_slope,
                "us_slope_ci_lo": us_lo, "us_slope_ci_hi": us_hi,
                "it_trend": it_mk.trend, "it_p": it_mk.p, "it_sen_slope": it_slope,
                "it_slope_ci_lo": it_lo, "it_slope_ci_hi": it_hi,
                "diff_trend": diff_mk.trend, "diff_p": diff_mk.p,
                "wilcoxon_stat": w_stat, "wilcoxon_p": w_p,
                "slopes_ci_overlap": ci_overlap,
            })

    if not results:
        print("No metric/sex combination had enough paired year-data to compare. Check istat_annual_top_names.csv coverage.")
        return

    fieldnames = list(results[0].keys())
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows -> {OUT_PATH}")
    for r in results:
        print(f"\nmetric={r['metric']} sex={r['sex']} n={r['n_years']} years={r['years_range']}")
        print(f"  US:    trend={r['us_trend']:12s} p={r['us_p']:.4g} sen_slope={r['us_sen_slope']:.6f} "
              f"CI=[{r['us_slope_ci_lo']:.6f}, {r['us_slope_ci_hi']:.6f}]")
        print(f"  Italy: trend={r['it_trend']:12s} p={r['it_p']:.4g} sen_slope={r['it_sen_slope']:.6f} "
              f"CI=[{r['it_slope_ci_lo']:.6f}, {r['it_slope_ci_hi']:.6f}]")
        print(f"  Diff-series (US-IT) trend: {r['diff_trend']} (p={r['diff_p']:.4g})")
        print(f"  Wilcoxon paired-level test: stat={r['wilcoxon_stat']:.3f} p={r['wilcoxon_p']:.4g}")
        print(f"  Slope 95% CIs overlap: {r['slopes_ci_overlap']} "
              f"({'no significant difference detected' if r['slopes_ci_overlap'] else 'slopes plausibly differ'})")


if __name__ == "__main__":
    main()
