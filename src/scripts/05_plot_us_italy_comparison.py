"""
Core RQ1 comparative figure: US vs Italy top-30 concentration share, overlapping window (2006-2024),
one line per country per sex.
"""

import csv
import os

import matplotlib.pyplot as plt

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", "us_diversity_metrics.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw", "istat", "istat_annual_top_names.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig5_us_italy_top30_comparison.png")

SEX_MAP = {"M": ("top30_male_share", "Maschi"), "F": ("top30_female_share", "Femmine")}
COLORS = {"M": "#1f5aa8", "F": "#c8447a"}


def load_us():
    with open(US_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for r in rows:
        out.setdefault(r["sex"], {})[int(r["year"])] = float(r["top30_share"])
    return out


def load_italy():
    with open(IT_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = {"M": {}, "F": {}}
    for r in rows:
        year = int(r["year"])
        for sex, (col, _) in SEX_MAP.items():
            val = r.get(col, "").strip()
            if val:
                out[sex][year] = float(val) / 100.0
    return out


def main():
    us = load_us()
    it = load_italy()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for sex, (_, label) in SEX_MAP.items():
        it_years = sorted(it[sex])
        it_vals = [it[sex][y] * 100 for y in it_years]
        us_years = [y for y in it_years if y in us[sex]]
        us_vals = [us[sex][y] * 100 for y in us_years]

        ax.plot(it_years, it_vals, color=COLORS[sex], linestyle="-", marker="o", markersize=3,
                label=f"Italia - {label}")
        ax.plot(us_years, us_vals, color=COLORS[sex], linestyle="--", marker="s", markersize=3,
                label=f"USA - {label}")

    ax.set_xlabel("Anno")
    ax.set_ylabel("Quota primi 30 nomi (% delle nascite)")
    ax.set_title("Concentrazione dei nomi: USA vs Italia, 2006-2024\n(quota di nascite coperta dai primi 30 nomi, per sesso)")
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
