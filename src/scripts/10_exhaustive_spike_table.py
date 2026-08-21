"""
Exhaustive (mechanically-filtered, not hand-picked) table of every name/year with
a large year-over-year jump, at a fixed threshold - a supplementary appendix table
alongside the hand-curated, cause-verified roster in PROJECT_LOG.md. This is the
"here's the full evidence base, not just our favorite 13 stories" table.

Thresholds (picked by checking how many rows they produce - see conversation,
2026-08-16 - both meaningfully above noise level and small enough for a paper table):
  US:    ratio >= 6.0x AND post-jump count >= 2000  -> 48 rows
  Italy: ratio >= 2.5x AND post-jump count >= 150    -> 39 rows

Input: dataset/processed/us_spike_candidates.csv, dataset/processed/it_spike_candidates.csv
       (from 06_find_us_spikes.py / 07_find_it_spikes.py)
Output: dataset/processed/exhaustive_spike_table.csv
    (country, name, sex, year, count, baseline, ratio)
"""

import csv
import os

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_spike_candidates.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_spike_candidates.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "exhaustive_spike_table.csv")

US_MIN_RATIO, US_MIN_COUNT = 6.0, 2000
IT_MIN_RATIO, IT_MIN_COUNT = 2.5, 150


def main():
    rows = []
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if float(r["ratio"]) >= US_MIN_RATIO and int(r["count"]) >= US_MIN_COUNT:
                rows.append(
                    {
                        "country": "US", "name": r["name"], "sex": r["sex"], "year": r["year"],
                        "count": r["count"], "baseline": r["baseline"], "ratio": r["ratio"],
                    }
                )
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if float(r["ratio"]) >= IT_MIN_RATIO and int(r["count"]) >= IT_MIN_COUNT:
                rows.append(
                    {
                        "country": "IT", "name": r["name"], "sex": r["gender"], "year": r["year"],
                        "count": r["count"], "baseline": r["baseline"], "ratio": r["ratio"],
                    }
                )

    rows.sort(key=lambda r: (-float(r["ratio"])))

    fieldnames = ["country", "name", "sex", "year", "count", "baseline", "ratio"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    us_n = sum(1 for r in rows if r["country"] == "US")
    it_n = sum(1 for r in rows if r["country"] == "IT")
    print(f"Wrote {len(rows)} rows ({us_n} US, {it_n} IT) -> {OUT_PATH}")
    print(f"Thresholds: US ratio>={US_MIN_RATIO}x count>={US_MIN_COUNT} | IT ratio>={IT_MIN_RATIO}x count>={IT_MIN_COUNT}")


if __name__ == "__main__":
    main()
