"""
"Whole roster" figure: one line per curated spike-story name, all on comparable
terms despite wildly different absolute scales (e.g. Tammy peaks near 10,000
births, Chanel near 150). Each name's series is indexed to 100 at 5 years before
its spike year, and the x-axis is "years relative to the event" rather than the
calendar year, so every story's rise lines up at x=0 regardless of when it
actually happened. Two panels: US roster on top, Italy roster on bottom.

Roster and spike years are the hand-curated, cause-verified list from
PROJECT_LOG.md (2026-08-16), not the mechanical candidate list.
"""

import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig7_spike_roster.png")

WINDOW_BEFORE, WINDOW_AFTER = 5, 6

# (name, sex/gender, spike_year, label with cause)
US_ROSTER = [
    ("Shirley", "F", 1935, "Shirley (Shirley Temple)"),
    ("Tammy", "F", 1958, "Tammy (Tammy and the Bachelor)"),
    ("Nakia", "F", 1974, "Nakia (serie TV Nakia)"),
    ("Jaime", "F", 1976, "Jaime (The Bionic Woman)"),
    ("Devante", "M", 1992, "Devante (Jodeci)"),
    ("Mariah", "F", 1991, "Mariah (Mariah Carey)"),
    ("Nevaeh", "F", 2001, "Nevaeh (P.O.D./MTV)"),
    ("Jaslene", "F", 2008, "Jaslene (ANTM)"),
]
IT_ROSTER = [
    ("KAROL", "m", 2005, "Karol (morte Giovanni Paolo II)"),
    ("CHANEL", "f", 2007, "Chanel (Chanel Totti)"),
    ("ADELE", "f", 2012, "Adele (album 21)"),
    ("ELODIE", "f", 2017, "Elodie (Sanremo)"),
    ("SOLEIL", "f", 2022, "Soleil (GF Vip)"),
]


def load_us_series():
    series = defaultdict(dict)
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            series[(r["name"], r["sex"])][int(r["year"])] = int(r["count"])
    return series


def load_it_series():
    series = defaultdict(dict)
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            series[(r["name"], r["gender"])][int(r["year"])] = int(r["count"])
    return series


def plot_panel(ax, roster, series_lookup, color_cycle):
    # Names like Nevaeh/Karol were essentially unused before their event (baseline
    # count near 0-2), so indexing to "value 5 years before" sends their index into
    # the tens of thousands and would flatten every other line on a linear axis.
    # Log-scale y-axis is the standard fix: it keeps huge and modest multiples both
    # readable on the same plot without distorting any single line's shape.
    for i, (name, sex, spike_year, label) in enumerate(roster):
        full = series_lookup.get((name, sex), {})
        pre_spike_vals = [full[y] for y in range(spike_year - WINDOW_BEFORE, spike_year) if y in full and full[y] > 0]
        if not pre_spike_vals:
            continue
        ref_val = pre_spike_vals[0]  # earliest available pre-spike value
        xs, ys = [], []
        for offset in range(-WINDOW_BEFORE, WINDOW_AFTER + 1):
            year = spike_year + offset
            if year in full and full[year] > 0:
                xs.append(offset)
                ys.append(100 * full[year] / ref_val)
        ax.plot(xs, ys, marker="o", markersize=3, label=label, color=color_cycle[i % len(color_cycle)])
    ax.axvline(0, color="gray", linestyle=":", linewidth=1)
    ax.axhline(100, color="gray", linestyle="-", linewidth=0.6, alpha=0.5)
    ax.set_yscale("log")
    ax.set_ylabel("Indice, scala log (100 = livello pre-evento)")
    ax.legend(loc="upper left", fontsize=7, ncol=2)
    ax.grid(alpha=0.3, which="both")


def main():
    us_series = load_us_series()
    it_series = load_it_series()

    us_colors = plt.cm.tab10.colors
    it_colors = plt.cm.Dark2.colors

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True)
    plot_panel(ax1, US_ROSTER, us_series, us_colors)
    ax1.set_title("USA")
    plot_panel(ax2, IT_ROSTER, it_series, it_colors)
    ax2.set_title("Italia")
    ax2.set_xlabel("Anni relativi all'evento (0 = anno del picco)")

    fig.suptitle("Traiettorie dei nomi \"evento\", indicizzate (100 = 5 anni prima del picco)")
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
