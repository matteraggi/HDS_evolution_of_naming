"""
Visualizes the coverage-bias sensitivity check from 01c_check_coverage_bias.py:
how much bias would truncating a complete year's data down to each depth we
actually hit introduce, for two different metrics.

The point of this figure: top10/top30 concentration share stays flat at zero
bias regardless of depth (proving it's safe to use across the full 1999-2024
window), while Shannon entropy bias grows sharply as depth shrinks (proving
entropy must stay restricted to the 2022-2024 fully-covered years). Putting
both lines on one plot makes that contrast visually obvious.
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_coverage_bias_check.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig4_coverage_bias_check.png")


def main():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["depth"]))
    depths = [int(r["depth"]) for r in rows]
    top30_bias = [float(r["mean_top30_share_bias"]) * 100 for r in rows]  # already ~0, in pp
    entropy_bias_pct = [float(r["mean_entropy_bias_percent"]) for r in rows]

    fig, ax1 = plt.subplots(figsize=(9, 5.5))
    color1 = "#1f5aa8"
    ax1.plot(depths, entropy_bias_pct, color=color1, marker="o", markersize=4, label="Bias entropia di Shannon (%)")
    ax1.set_xscale("log")
    ax1.set_xlabel("Profondità di copertura (numero di nomi catturati, scala log)")
    ax1.set_ylabel("Bias dell'entropia di Shannon (%)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.axhline(0, color="gray", linestyle=":", linewidth=1)

    ax2 = ax1.twinx()
    color2 = "#c8447a"
    ax2.plot(depths, top30_bias, color=color2, marker="s", markersize=4, label="Bias quota primi 30 nomi (p.p.)")
    ax2.set_ylabel("Bias della quota primi 30 nomi (punti percentuali)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.set_ylim(-5, 5)

    fig.suptitle("Sensibilità delle metriche alla profondità di copertura")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="lower right", fontsize=8)
    ax1.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
