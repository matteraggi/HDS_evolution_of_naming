"""
Bonus depth figure: full US Shannon entropy, 1880-2025, "both" (pooled M+F) series.
Non-comparative -- Italy has no pre-1999 name-level data, so this is shown separately
as "what a complete distribution reveals" (see plan RQ1 pivot, section 3).
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "us_diversity_metrics.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig2_us_entropy_1880_2025.png")


def main():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["sex"] == "both"]
    rows.sort(key=lambda r: int(r["year"]))
    years = [int(r["year"]) for r in rows]
    entropy = [float(r["shannon_entropy"]) for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(years, entropy, color="#1f5aa8", linewidth=1.8)
    ax.axvspan(1999, 2025, color="#1f5aa8", alpha=0.08, label="Finestra comparabile con l'Italia (1999-2025)")
    ax.set_xlabel("Anno")
    ax.set_ylabel("Entropia di Shannon (bit)")
    ax.set_title("Entropia di Shannon dei nomi alla nascita negli USA, 1880-2025\n(figura di approfondimento, non comparativa)")
    ax.legend(loc="lower right", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
