"""
Convergence figure: how similar the US and Italy naming pools have become over
time, per sex, 1999-2024. Two panels on the same time axis:
  top    - cosine similarity between the two countries' full name-frequency
           distributions (dataset/processed/us_italy_distribution_similarity.csv)
  bottom - top-100 overlap count, a simpler complementary number

See 08b_us_italy_distribution_similarity.py's docstring for why cosine
similarity is the "full dataset" version of the convergence question, and
PROJECT_LOG.md (2026-08-16) for why this replaced the top-30-only overlap as
the headline convergence metric.
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_italy_distribution_similarity.csv"
)
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig6_us_italy_convergence.png")

LABELS = {"M": "Maschi", "F": "Femmine"}
COLORS = {"M": "#1f5aa8", "F": "#c8447a"}


def load():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_sex = {"M": {}, "F": {}}
    for r in rows:
        by_sex[r["sex"]][int(r["year"])] = (float(r["cosine_similarity"]), int(r["top100_overlap_count"]))
    return by_sex


def main():
    data = load()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

    for sex, label in LABELS.items():
        years = sorted(data[sex])
        sims = [data[sex][y][0] for y in years]
        overlaps = [data[sex][y][1] for y in years]
        ax1.plot(years, sims, color=COLORS[sex], marker="o", markersize=3, label=label)
        ax2.plot(years, overlaps, color=COLORS[sex], marker="o", markersize=3, label=label)

    ax1.set_ylabel("Similarità coseno\n(distribuzione completa dei nomi)")
    ax1.set_title("Convergenza dei nomi USA-Italia, 1999-2024")
    ax1.legend(loc="upper left", fontsize=9)
    ax1.grid(alpha=0.3)

    ax2.set_xlabel("Anno")
    ax2.set_ylabel("Nomi in comune\n(primi 100 per paese)")
    ax2.set_ylim(0, 100)
    ax2.grid(alpha=0.3)

    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
