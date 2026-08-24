"""
Core RQ1 comparative figure: US vs Italy top-50 concentration share, overlapping window (1999-2024),
one line per country per sex.

Italy source updated to the full contanomi scrape (it_diversity_metrics.csv, from
01b_process_istat_contanomi.py) rather than the old manual top-30 collection - see
PROJECT_LOG.md decision log, 2026-08-14: verified strict superset coverage, extends
the window back to 1999 instead of 2006.

2026-08-24: switched from top30_share to top50_share (decision in PROJECT_LOG.md).
"""

import csv
import os

import matplotlib.pyplot as plt

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_diversity_metrics.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_diversity_metrics.csv")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "figures", "fig5_us_italy_top50_comparison.png")

LABELS = {"M": "Maschi", "F": "Femmine"}
COLORS = {"M": "#1f5aa8", "F": "#c8447a"}


def load_us():
    with open(US_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = {}
    for r in rows:
        out.setdefault(r["sex"], {})[int(r["year"])] = float(r["top50_share"])
    return out


def load_italy():
    with open(IT_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    out = {"M": {}, "F": {}}
    for r in rows:
        out[r["sex"]][int(r["year"])] = float(r["top50_share"])
    return out


def main():
    us = load_us()
    it = load_italy()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for sex, label in LABELS.items():
        it_years = sorted(it[sex])
        it_vals = [it[sex][y] * 100 for y in it_years]
        us_years = [y for y in it_years if y in us[sex]]
        us_vals = [us[sex][y] * 100 for y in us_years]

        ax.plot(it_years, it_vals, color=COLORS[sex], linestyle="-", marker="o", markersize=3,
                label=f"Italia - {label}")
        ax.plot(us_years, us_vals, color=COLORS[sex], linestyle="--", marker="s", markersize=3,
                label=f"USA - {label}")

    ax.set_xlabel("Anno")
    ax.set_ylabel("Quota primi 50 nomi (% delle nascite)")
    ax.set_title("Concentrazione dei nomi: USA vs Italia, 1999-2024\n(quota di nascite coperta dai primi 50 nomi, per sesso)")
    ax.legend(loc="upper right", fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fig.savefig(OUT_PATH, dpi=150)
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
