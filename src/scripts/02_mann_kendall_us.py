"""
Mann-Kendall trend test on US diversity metrics (Shannon entropy, top10/top50 share),
run separately per sex, over two windows:
  - full history (1880-2025)
  - the comparable window with Italy (1999-2025)

Input: dataset/processed/us_diversity_metrics.csv (from 01_process_ssa.py)
Output: dataset/processed/us_mann_kendall_results.csv

Reference: Mann, H.B. (1945), Econometrica 13(3); Kendall, M.G. (1975), Rank Correlation Methods.
"""

import csv
import os

import pymannkendall as mk

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_diversity_metrics.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_mann_kendall_results.csv")

METRICS = ["shannon_entropy", "top10_share", "top50_share"]
WINDOWS = {"full_1880_2025": (1880, 2025), "comparable_1999_2025": (1999, 2025)}


def load_rows():
    with open(IN_PATH, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_rows()
    results = []

    for sex in ("M", "F", "both"):
        sex_rows = sorted((r for r in rows if r["sex"] == sex), key=lambda r: int(r["year"]))
        for window_name, (start, end) in WINDOWS.items():
            window_rows = [r for r in sex_rows if start <= int(r["year"]) <= end]
            for metric in METRICS:
                series = [float(r[metric]) for r in window_rows]
                if len(series) < 4:
                    continue
                res = mk.original_test(series)
                results.append({
                    "sex": sex,
                    "window": window_name,
                    "metric": metric,
                    "n_years": len(series),
                    "trend": res.trend,
                    "p_value": res.p,
                    "tau": res.Tau,
                    "sens_slope": res.slope,
                })

    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sex", "window", "metric", "n_years", "trend", "p_value", "tau", "sens_slope"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    print(f"Wrote {len(results)} rows -> {OUT_PATH}")
    for r in results:
        print(f"{r['sex']:5s} {r['window']:22s} {r['metric']:16s} trend={r['trend']:12s} p={r['p_value']:.4g} tau={r['tau']:.3f} slope={r['sens_slope']:.6f}")


if __name__ == "__main__":
    main()
