"""
Visualizes the coverage-bias sensitivity check from 01c_check_coverage_bias.py:
how much bias would truncating a complete year's data down to each depth we
actually hit introduce.

2026-08-24: simplified to a single-axis entropy-only plot. The earlier version
also plotted the top50 concentration bias on a twin y-axis, but that line is
flat at exactly zero across the whole range (see 01c's docstring for why) -
overlaying a constant-zero line against a curve that moves from -50% to -19%
added visual clutter without adding information, and a flat line sharing an
axis with a moving one reads as a strange pairing. The zero-bias result for
top10/top50/top100 is instead stated as a text annotation and left fully
detailed in Tabella 14. Also switched the x-axis from matplotlib's default
log-scale ticks (which picked oddly-spaced values like 200/300/400/600/1000/
2000/3000/4000/6000) to explicit round ticks for readability.
"""

import csv
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_coverage_bias_check.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig4_coverage_bias_check.png")


def main():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: int(r["depth"]))
    depths = [int(r["depth"]) for r in rows]
    entropy_bias_pct = [float(r["mean_entropy_bias_percent"]) for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    color1 = "#1f5aa8"
    ax.plot(depths, entropy_bias_pct, color=color1, marker="o", markersize=4)
    ax.set_xscale("log")
    ax.set_xticks([150, 200, 300, 500, 1000, 2000, 3000, 5000])
    ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(mticker.NullFormatter())
    ax.set_xlabel("Profondità di copertura (numero di nomi catturati, scala log)")
    ax.set_ylabel("Bias dell'entropia di Shannon (%)", color=color1)
    ax.tick_params(axis="y", labelcolor=color1)
    ax.axhline(0, color="gray", linestyle=":", linewidth=1)
    ax.annotate(
        "Per confronto: il bias sulla quota primi-10/50/100 è\nesattamente zero a ogni profondità (Tabella 14)",
        xy=(0.02, 0.06), xycoords="axes fraction", fontsize=8.5, color="#555",
        bbox=dict(boxstyle="round", fc="white", ec="#ccc", alpha=0.9),
    )

    fig.suptitle("Sensibilità dell'entropia di Shannon alla profondità di copertura")
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
