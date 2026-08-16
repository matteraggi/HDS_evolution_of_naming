"""
Figure for the geographic robustness check (15_state_concentration_analysis.py):
horizontal bar chart of "% of states moving in the same direction as the
national effect," one bar per curated story, sorted, colored by positive vs
negative spike. High % = the national story is corroborated by broad
geographic spread, not driven by one or two states.
"""

import csv
import os

import matplotlib.pyplot as plt

IN_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "state_concentration_results.csv"
)
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig8_state_concentration.png"
)

COLORS = {"positive": "#1f5aa8", "negative": "#c8447a"}
LABELS = {"positive": "Spike positivo", "negative": "Crollo (anti-spike)"}


def main():
    with open(IN_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    rows.sort(key=lambda r: float(r["pct_states_moving_same_direction"]))

    names = [f"{r['name']} ({r['event_year']})" for r in rows]
    pcts = [float(r["pct_states_moving_same_direction"]) for r in rows]
    kinds = [r["kind"] for r in rows]
    n_states = [int(r["n_states_with_data"]) for r in rows]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(names, pcts, color=[COLORS[k] for k in kinds])
    for bar, n in zip(bars, n_states):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f"n={n} stati",
                va="center", fontsize=8, color="#555")

    ax.axvline(90, color="gray", linestyle=":", linewidth=1)
    ax.set_xlim(0, 115)
    ax.set_xlabel("% di stati che si muovono nella stessa direzione dell'effetto nazionale")
    ax.set_title("Uniformità geografica dei casi-studio RQ2\n(quota di stati concordanti con l'effetto nazionale)")

    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[k]) for k in ("positive", "negative")]
    ax.legend(handles, [LABELS[k] for k in ("positive", "negative")], loc="lower right", fontsize=9)
    ax.grid(alpha=0.3, axis="x")
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
