"""
Plot the Event Study results for the Movie & TV Series category.

Generates:
  - docs/paper/figures/fig7b_movie_event_study.png:
    (Left panel: Boxplot / Distribution of Net DiD Effects vs Controls;
     Right panel: Bar chart of top positive movie character shocks vs null controls)
"""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "movie_event_study_results.csv")
OUT_PLOT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig7b_movie_event_study.png")


def main():
    rows = []
    with open(IN_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["did_net_effect_pct"] = float(r["did_net_effect_pct"])
            r["pre_freq_per_100k"] = float(r["pre_freq_per_100k"])
            r["post_freq_per_100k"] = float(r["post_freq_per_100k"])
            rows.append(r)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Net DiD Effect Distribution
    did_effects = [r["did_net_effect_pct"] for r in rows]
    # Cap extreme visual outliers for plot readability
    clipped_effects = [min(max(x, -100), 500) for x in did_effects]

    bp = ax1.boxplot(clipped_effects, vert=True, patch_artist=True, boxprops=dict(facecolor="#2b5c8f", color="#1a365d"))
    ax1.axhline(0, color="red", linestyle="--", linewidth=1.5, label="Nessun effetto vs Controlli (0%)")
    ax1.set_ylabel("Impatto Netto DiD (%) rispetto ai Controlli")
    ax1.set_title("A: Distribuzione Impatto Netto Film & Serie TV\n(Wilcoxon p = 5.62e-05)", fontsize=11, fontweight="bold")
    ax1.set_xticklabels(["Eventi Film/Serie (N=71)"])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel B: Top 10 Positive Shocks vs Control Examples
    # Sort by did_net_effect_pct
    sorted_rows = sorted(rows, key=lambda x: x["did_net_effect_pct"], reverse=True)
    top_pos = sorted_rows[:8]
    null_controls = [r for r in sorted_rows if abs(r["did_net_effect_pct"]) < 20][:3]

    plot_items = top_pos + null_controls
    labels = [f"{r['character']} ({r['country']}, {r['year']})" for r in plot_items]
    values = [r["did_net_effect_pct"] for r in plot_items]
    colors = ["#2e7d32" if v > 20 else "#757575" for v in values]

    y_pos = np.arange(len(labels))
    ax2.barh(y_pos, values, color=colors, align="center")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()  # top-down
    ax2.set_xlabel("Variazione Relativa Netta DiD (%)")
    ax2.set_title("B: Casi di Picco Mediatico vs Controlli ad Effetto Nullo", fontsize=11, fontweight="bold")
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PLOT), exist_ok=True)
    plt.savefig(OUT_PLOT, dpi=300)
    plt.close()

    print(f"Saved Movie Event Study Plot -> {OUT_PLOT}")


if __name__ == "__main__":
    main()
