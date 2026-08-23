"""
Plot Gender-Neutral (Unisex) Naming Trends for US vs Italy (RQ3).

Generates:
  - docs/paper/figures/fig9_gender_neutral.png
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "gender_neutral_metrics.csv")
OUT_PLOT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig9_gender_neutral.png")


def main():
    us_rows = []
    it_rows = []

    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["year"] = int(r["year"])
            r["unisex_share_pct"] = float(r["unisex_share_pct"])
            r["num_unisex_names"] = int(r["num_unisex_names"])
            if r["country"] == "US":
                us_rows.append(r)
            else:
                it_rows.append(r)

    us_rows.sort(key=lambda x: x["year"])
    it_rows.sort(key=lambda x: x["year"])

    years = [r["year"] for r in us_rows]
    us_shares = [r["unisex_share_pct"] for r in us_rows]
    it_shares = [r["unisex_share_pct"] for r in it_rows]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Panel A: Unisex Birth Share (%) Comparison
    ax1.plot(years, us_shares, "o-", color="#1e40af", linewidth=2.5, label="Stati Uniti (USA) — Mann-Kendall p < 0.001")
    ax1.plot(years, it_shares, "s-", color="#c2410c", linewidth=2.5, label="Italia (IT) — Stabile (<0.25%)")
    ax1.set_xlabel("Anno di Nascita")
    ax1.set_ylabel("Quota di Nascite con Nomi Unissex (%)")
    ax1.set_title("A: Quota di Neonati con Nomi Gender-Neutral (1999-2024)", fontsize=11, fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel B: Number of Distinct Unisex Names
    us_num = [r["num_unisex_names"] for r in us_rows]
    it_num = [r["num_unisex_names"] for r in it_rows]

    ax2.plot(years, us_num, "o--", color="#1e40af", linewidth=2.0, label="USA (Numero Nomi Unissex)")
    ax2.plot(years, it_num, "s--", color="#c2410c", linewidth=2.0, label="Italia (Numero Nomi Unissex)")
    ax2.set_xlabel("Anno di Nascita")
    ax2.set_ylabel("Numero di Nomi Unissex Distinti")
    ax2.set_title("B: Conteggio Nomi Gender-Neutral Distinti (0.10 <= p_F <= 0.90)", fontsize=11, fontweight="bold")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(loc="upper left")

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PLOT), exist_ok=True)
    plt.savefig(OUT_PLOT, dpi=300)
    plt.close()

    print(f"Saved Gender-Neutral Plot -> {OUT_PLOT}")


if __name__ == "__main__":
    main()
