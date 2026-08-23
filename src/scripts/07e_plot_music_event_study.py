"""
Plot the Event Study results for the Music & Pop Culture category.

Generates:
  - docs/paper/figures/fig7c_music_event_study.png
"""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np

IN_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "music_event_study_results.csv")
OUT_PLOT = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig7c_music_event_study.png")


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

    bp = ax1.boxplot(clipped_effects, orientation="vertical", patch_artist=True, boxprops=dict(facecolor="#6b21a8", color="#4c1d95"))
    ax1.axhline(0, color="red", linestyle="--", linewidth=1.5, label="Nessun effetto vs Controlli (0%)")
    ax1.set_ylabel("Impatto Netto DiD (%) rispetto ai Controlli")
    ax1.set_title("A: Distribuzione Impatto Netto Musica & Pop Culture\n(Wilcoxon Signed-Rank Test)", fontsize=11, fontweight="bold")
    ax1.set_xticklabels(["Eventi Musica/Pop (N={})".format(len(rows))])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel B: Top Positive Music Shocks vs Control Examples
    sorted_rows = sorted(rows, key=lambda x: x["did_net_effect_pct"], reverse=True)
    top_pos = sorted_rows[:8]
    null_controls = [r for r in sorted_rows if abs(r["did_net_effect_pct"]) < 25][:3]

    plot_items = top_pos + null_controls
    labels = [f"{r['character']} ({r['country']}, {r['year']})" for r in plot_items]
    values = [r["did_net_effect_pct"] for r in plot_items]
    colors = ["#15803d" if v > 20 else "#6b7280" for v in values]

    y_pos = np.arange(len(labels))
    ax2.barh(y_pos, values, color=colors, align="center")
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(labels)
    ax2.invert_yaxis()
    ax2.set_xlabel("Variazione Relativa Netta DiD (%)")
    ax2.set_title("B: Casi di Picco Musicale vs Nomi a Trend Stabile", fontsize=11, fontweight="bold")
    ax2.axvline(0, color="black", linewidth=0.8)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PLOT), exist_ok=True)
    plt.savefig(OUT_PLOT, dpi=300)
    plt.close()

    print(f"Saved Music Event Study Plot -> {OUT_PLOT}")


if __name__ == "__main__":
    main()
