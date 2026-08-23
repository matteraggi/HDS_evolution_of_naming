"""
Plot the Event Study results for the Sports category.

Generates:
  - docs/paper/figures/fig7d_sports_event_study.png
"""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "sports_event_study_results.csv")
OUT_PLOT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig7d_sports_event_study.png")


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
    clipped_effects = [min(max(x, -100), 500) for x in did_effects]

    bp = ax1.boxplot(clipped_effects, orientation="vertical", patch_artist=True, boxprops=dict(facecolor="#1e40af", color="#1e3a8a"))
    ax1.axhline(0, color="red", linestyle="--", linewidth=1.5, label="Nessun effetto vs Controlli (0%)")
    ax1.set_ylabel("Impatto Netto DiD (%) rispetto ai Controlli")
    ax1.set_title("A: Distribuzione Impatto Netto Sport\n(Wilcoxon p = 0.1898 - Non Significativo)", fontsize=11, fontweight="bold")
    ax1.set_xticklabels(["Eventi Sportivi (N={})".format(len(rows))])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel B: Top Sports Shocks vs Stable Examples
    sorted_rows = sorted(rows, key=lambda x: x["did_net_effect_pct"], reverse=True)
    top_pos = sorted_rows[:8]
    null_controls = [r for r in sorted_rows if abs(r["did_net_effect_pct"]) < 15][:3]

    plot_items = top_pos + null_controls
    labels = [f"{r['character']} ({r['country']}, {r['year']})" for r in plot_items]
    values = [r["did_net_effect_pct"] for r in plot_items]
    colors = ["#1d4ed8" if v > 20 else "#6b7280" for v in values]

    y_pos = np.arange(len(labels))
    ax2.barh(y_pos, values, color=colors, align="center")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlabel("Variazione Relativa Netta DiD (%)")
    ax2.set_title("B: Confronto tra Atleti con Picco vs Atleti ad Effetto Nullo", fontsize=11, fontweight="bold")
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PLOT), exist_ok=True)
    plt.savefig(OUT_PLOT, dpi=300)
    plt.close()

    print(f"Saved Sports Event Study Plot -> {OUT_PLOT}")


if __name__ == "__main__":
    main()
