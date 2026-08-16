"""
How complete the ISTAT contanomi scrape is, per year - visualizes
dataset/istat/contanomi_raw/manifest.csv (male_percent_sum / female_percent_sum:
what share of that year's TRUE total births are captured by the scraped names).

Companion to 01c_check_coverage_bias.py's numeric proof that this unevenness
doesn't bias the paper's primary Italy metric (top10/top30 share) - this figure
is the visual "here's what the gap actually looks like, year by year" that
motivates why that check was necessary in the first place.
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "istat", "contanomi_raw", "manifest.csv"
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig3_istat_coverage.png")

COLORS = {"M": "#1f5aa8", "F": "#c8447a"}


def main():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["year"]))
    years = [int(r["year"]) for r in rows]
    male_cov = [float(r["male_percent_sum"]) for r in rows]
    female_cov = [float(r["female_percent_sum"]) for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(years, male_cov, color=COLORS["M"], marker="o", markersize=3, label="Maschi")
    ax.plot(years, female_cov, color=COLORS["F"], marker="o", markersize=3, label="Femmine")
    ax.axhline(100, color="gray", linestyle=":", linewidth=1)
    ax.set_ylim(55, 105)
    ax.set_xlabel("Anno")
    ax.set_ylabel("Copertura dello scraping (% delle nascite catturate)")
    ax.set_title(
        "Completezza dei dati ISTAT contanomi per anno, 1999-2024\n"
        "(quota di nascite coperta dai nomi effettivamente recuperati)"
    )
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
