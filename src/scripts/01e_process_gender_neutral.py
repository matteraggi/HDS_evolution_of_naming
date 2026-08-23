"""
Process US SSA and Italy ISTAT data to compute Gender-Neutral (Unisex) name metrics (RQ3).

Defines a unisex name in year Y as one where:
  0.10 <= p_female <= 0.90  (and total births >= threshold)

Computes per-country annual metrics (1999-2024):
  - Number of distinct unisex names
  - Total births receiving unisex names
  - Share of total national births receiving unisex names (%)
  - Top 10 unisex names per country

Executes Mann-Kendall trend tests for US vs Italy unisex name growth.

Outputs:
  - dataset/processed/gender_neutral_metrics.csv
  - dataset/processed/top_unisex_names.csv
  - docs/paper/tables/table19_gender_neutral.csv
"""

import csv
import os
import unicodedata
from collections import defaultdict

import numpy as np
import pymannkendall as mk

US_LONG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_LONG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")

OUT_METRICS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "gender_neutral_metrics.csv")
OUT_TOP_NAMES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "top_unisex_names.csv")
TABLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables", "table19_gender_neutral.csv")


def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def process_us_gender_neutral():
    # year -> {name_norm: {'F': count, 'M': count}}
    by_year = defaultdict(lambda: defaultdict(lambda: {"F": 0, "M": 0}))
    total_births_by_year = defaultdict(int)

    with open(US_LONG_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            year = int(r["year"])
            if year < 1999 or year > 2024:
                continue
            name_norm = normalize(r["name"])
            sex = r["sex"].upper()
            cnt = int(r["count"])

            by_year[year][name_norm][sex] += cnt
            total_births_by_year[year] += cnt

    metrics = []
    top_names_agg = defaultdict(int)

    for year in sorted(by_year):
        tot_births = total_births_by_year[year] // 2  # Total births is sum of male + female births
        unisex_names = []
        unisex_births = 0

        for name_norm, counts in by_year[year].items():
            f_cnt = counts["F"]
            m_cnt = counts["M"]
            tot = f_cnt + m_cnt
            if tot < 50 or f_cnt == 0 or m_cnt == 0:
                continue

            p_f = f_cnt / tot
            if 0.10 <= p_f <= 0.90:
                unisex_names.append((name_norm, tot, p_f))
                unisex_births += tot
                top_names_agg[name_norm] += tot

        unisex_share_pct = 100.0 * unisex_births / (tot_births * 2)
        metrics.append({
            "country": "US",
            "year": year,
            "num_unisex_names": len(unisex_names),
            "unisex_births": unisex_births,
            "total_births": tot_births * 2,
            "unisex_share_pct": round(unisex_share_pct, 3)
        })

    return metrics, top_names_agg


def process_it_gender_neutral():
    by_year = defaultdict(lambda: defaultdict(lambda: {"F": 0, "M": 0}))
    total_births_by_year = defaultdict(int)

    with open(IT_LONG_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            year = int(r["year"])
            if year < 1999 or year > 2024:
                continue
            name_norm = normalize(r["name"])
            gender = r["gender"].upper()
            cnt = int(r["count"])

            by_year[year][name_norm][gender] += cnt
            total_births_by_year[year] += cnt

    metrics = []
    top_names_agg = defaultdict(int)

    for year in sorted(by_year):
        tot_births = total_births_by_year[year]
        unisex_names = []
        unisex_births = 0

        for name_norm, counts in by_year[year].items():
            f_cnt = counts["F"]
            m_cnt = counts["M"]
            tot = f_cnt + m_cnt
            if tot < 15 or f_cnt == 0 or m_cnt == 0:
                continue

            p_f = f_cnt / tot
            if 0.10 <= p_f <= 0.90:
                unisex_names.append((name_norm, tot, p_f))
                unisex_births += tot
                top_names_agg[name_norm] += tot

        unisex_share_pct = 100.0 * unisex_births / tot_births if tot_births > 0 else 0.0
        metrics.append({
            "country": "IT",
            "year": year,
            "num_unisex_names": len(unisex_names),
            "unisex_births": unisex_births,
            "total_births": tot_births,
            "unisex_share_pct": round(unisex_share_pct, 3)
        })

    return metrics, top_names_agg


def main():
    us_metrics, us_top = process_us_gender_neutral()
    it_metrics, it_top = process_it_gender_neutral()

    all_metrics = us_metrics + it_metrics

    # Save metrics CSV
    os.makedirs(os.path.dirname(OUT_METRICS_PATH), exist_ok=True)
    fieldnames = ["country", "year", "num_unisex_names", "unisex_births", "total_births", "unisex_share_pct"]
    with open(OUT_METRICS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(all_metrics)

    # Save top unisex names
    top_rows = []
    for name, cnt in sorted(us_top.items(), key=lambda x: x[1], reverse=True)[:15]:
        top_rows.append({"country": "US", "name": name, "total_unisex_births": cnt})
    for name, cnt in sorted(it_top.items(), key=lambda x: x[1], reverse=True)[:15]:
        top_rows.append({"country": "IT", "name": name, "total_unisex_births": cnt})

    with open(OUT_TOP_NAMES_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["country", "name", "total_unisex_births"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(top_rows)

    # Statistical Mann-Kendall tests
    us_shares = [r["unisex_share_pct"] for r in us_metrics]
    it_shares = [r["unisex_share_pct"] for r in it_metrics]

    us_mk = mk.original_test(us_shares)
    it_mk = mk.original_test(it_shares)

    # Save summary table 19
    os.makedirs(os.path.dirname(TABLE_PATH), exist_ok=True)
    summary_table_rows = [
        {
            "Paese": "Stati Uniti (USA)",
            "Finestra Temporale": "1999-2024",
            "Quota Iniziale 1999 (%)": f"{us_shares[0]:.2f}%",
            "Quota Finale 2024 (%)": f"{us_shares[-1]:.2f}%",
            "Trend Mann-Kendall": us_mk.trend,
            "Tau di Kendall": f"{us_mk.Tau:.3f}",
            "p-value": f"{us_mk.p:.4e}",
            "Esito Statistico": "Crescita Significativa (p < 0.001)" if us_mk.p < 0.001 else "Non Significativo"
        },
        {
            "Paese": "Italia (IT)",
            "Finestra Temporale": "1999-2024",
            "Quota Iniziale 1999 (%)": f"{it_shares[0]:.2f}%",
            "Quota Finale 2024 (%)": f"{it_shares[-1]:.2f}%",
            "Trend Mann-Kendall": it_mk.trend,
            "Tau di Kendall": f"{it_mk.Tau:.3f}",
            "p-value": f"{it_mk.p:.4e}",
            "Esito Statistico": "Crescita Significativa (p < 0.001)" if it_mk.p < 0.001 else "Stabile / Controllato"
        }
    ]

    t19_fieldnames = ["Paese", "Finestra Temporale", "Quota Iniziale 1999 (%)", "Quota Finale 2024 (%)", "Trend Mann-Kendall", "Tau di Kendall", "p-value", "Esito Statistico"]
    with open(TABLE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=t19_fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_table_rows)

    print(f"Processed Gender-Neutral metrics:")
    print(f"  US Unisex Share 1999 -> 2024: {us_shares[0]:.2f}% -> {us_shares[-1]:.2f}% (Mann-Kendall Tau={us_mk.Tau:.3f}, p={us_mk.p:.4e})")
    print(f"  IT Unisex Share 1999 -> 2024: {it_shares[0]:.2f}% -> {it_shares[-1]:.2f}% (Mann-Kendall Tau={it_mk.Tau:.3f}, p={it_mk.p:.4e})")
    print(f"Saved metrics -> {OUT_METRICS_PATH}")
    print(f"Saved table19 -> {TABLE_PATH}")


if __name__ == "__main__":
    main()
