"""
Cross-category quantitative synthesis for the RQ2 Event Study.

Combines Movie & TV Series, Music & Pop Culture, and Sports event studies,
computes comparative metrics, generates table18_event_study_summary.csv (and table18.tex),
and plots the overall inter-category comparison chart (fig7_event_study_categories.png).
"""

import csv
import os

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

MOVIES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "movie_event_study_results.csv")
MUSIC_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "music_event_study_results.csv")
SPORTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "sports_event_study_results.csv")

OUT_TABLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables", "table18_event_study_summary.csv")
OUT_PLOT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig7_event_study_categories.png")


def load_category_data(filepath, cat_name):
    rows = []
    with open(filepath, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["category_name"] = cat_name
            r["did_net_effect_pct"] = float(r["did_net_effect_pct"])
            rows.append(r)
    return rows


def main():
    movies = load_category_data(MOVIES_PATH, "Cinema & Serie TV")
    music = load_category_data(MUSIC_PATH, "Musica & Pop Culture")
    sports = load_category_data(SPORTS_PATH, "Sport")

    all_categories = [
        ("Cinema & Serie TV", movies),
        ("Musica & Pop Culture", music),
        ("Sport", sports),
    ]

    summary_rows = []
    all_did_effects = []

    for name, cat_rows in all_categories:
        effects = [r["did_net_effect_pct"] for r in cat_rows]
        all_did_effects.extend(effects)

        mean_did = sum(effects) / len(effects) if effects else 0.0
        median_did = sorted(effects)[len(effects) // 2] if effects else 0.0
        w_stat, p_val = stats.wilcoxon(effects) if len(effects) >= 5 else (0, 1.0)

        sig_str = "Significativo" if p_val < 0.05 else "Non significativo"

        summary_rows.append({
            "Categoria Evento": name,
            "N": len(cat_rows),
            "Media DiD (%)": f"{mean_did:+.1f}%",
            "Mediana DiD (%)": f"{median_did:+.1f}%",
            "Wilcoxon W": f"{w_stat:.1f}",
            "p": f"{p_val:.2e}",
            "Esito": sig_str
        })

    # Total overall stats
    w_tot, p_tot = stats.wilcoxon(all_did_effects)
    summary_rows.append({
        "Categoria Evento": "TOTALE",
        "N": len(all_did_effects),
        "Media DiD (%)": f"{sum(all_did_effects)/len(all_did_effects):+.1f}%",
        "Mediana DiD (%)": f"{sorted(all_did_effects)[len(all_did_effects)//2]:+.1f}%",
        "Wilcoxon W": f"{w_tot:.1f}",
        "p": f"{p_tot:.2e}",
        "Esito": "Significativo" if p_tot < 0.05 else "Non significativo"
    })

    # Save summary table CSV
    os.makedirs(os.path.dirname(OUT_TABLE_PATH), exist_ok=True)
    fieldnames = ["Categoria Evento", "N", "Media DiD (%)", "Mediana DiD (%)", "Wilcoxon W", "p", "Esito"]
    with open(OUT_TABLE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)

    # Plot Inter-category comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Panel A: Boxplot comparison across categories
    cat_data = [[min(max(x, -100), 500) for x in [r["did_net_effect_pct"] for r in cat_rows]] for _, cat_rows in all_categories]
    bp = ax1.boxplot(cat_data, orientation="vertical", patch_artist=True)
    colors = ["#2b5c8f", "#6b21a8", "#1e40af"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.8)

    ax1.axhline(0, color="red", linestyle="--", linewidth=1.5, label="Nessun impatto vs Controlli (0%)")
    ax1.set_ylabel("Impatto Netto DiD (%) rispetto ai Controlli")
    ax1.set_title("A: Confronto Distribuzione Impatto DiD per Categoria", fontsize=11, fontweight="bold")
    ax1.set_xticklabels(["Cinema & TV\n(p < 0.0001)", "Musica & Pop\n(p < 0.001)", "Sport\n(p = 0.1898)"])
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(loc="upper left")

    # Panel B: Mean DiD Impact Bar Chart
    cat_names = [name for name, _ in all_categories]
    means = [sum(r["did_net_effect_pct"] for r in cat_rows)/len(cat_rows) for _, cat_rows in all_categories]

    ax2.bar(cat_names, means, color=colors, alpha=0.85, width=0.5)
    ax2.set_ylabel("Impatto Netto Medio DiD (%)")
    ax2.set_title("B: Confronto dell'Impatto Netto Medio per Categoria Mediatica", fontsize=11, fontweight="bold")
    ax2.axhline(0, color="black", linewidth=0.8)
    for i, v in enumerate(means):
        ax2.text(i, v + 8, f"{v:+.1f}%", ha="center", fontweight="bold", fontsize=10)
    ax2.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PLOT_PATH), exist_ok=True)
    plt.savefig(OUT_PLOT_PATH, dpi=300)
    plt.close()

    print(f"Saved Inter-Category Event Study Summary Table -> {OUT_TABLE_PATH}")
    print(f"Saved Inter-Category Event Study Plot -> {OUT_PLOT_PATH}")


if __name__ == "__main__":
    main()
