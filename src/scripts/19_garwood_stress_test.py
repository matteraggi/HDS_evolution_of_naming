"""
Garwood exact-Poisson "stress test" (Roccetti 2026, Front. Artif. Intell.
9:1961525, doi:10.3389/frai.2026.1961525) applied to RQ2.

Motivation: our spike/crash case studies and the confirmatory Event Study
compare rates computed as name-count / total-births, exactly the "rare event
count n over a massive population denominator N" structure that Roccetti's
paper warns about: naive Wald-style reasoning about such rates is
overconfident, because the huge denominator makes the estimate look far more
precise than the sparse numerator n actually justifies.

Roccetti's fix is a stress test where the null benchmark is not zero but the
exact lower limit of the Garwood/Poisson confidence interval built from the
same count n. The key algebraic fact (his Eq. 5-6) is that the population
denominator N cancels out completely: the resulting Z-score is a pure,
scale-invariant function of the observed count n alone:

    Z(n) = (n - 0.5 * chi2.ppf(alpha/2, df=2n)) / sqrt(n)

Z(n) -> 1.96 as n -> infinity; for small n it sits (sometimes well) below
1.96, which is the "structural fragility" signal: a count too sparse to
trust even though the resulting percentage swing looks dramatic.

We apply Z(n) to two places in RQ2:
  (A) the 17 hand-verified spike/crash stories (Tables "positive_spikes" and
      "negative_spikes" in the paper) - using the exact pre-event baseline
      count and post-event count already reported in the paper's tables
      (cross-checked here against the underlying raw SSA/ISTAT rows);
  (B) the N=152 Event Study roster - recomputing, for each exposed name, the
      summed raw count over the pre-event window (up to 3 years) and the
      post-event window (up to 2 years), then Z-testing the post-event count.

Outputs:
  - dataset/processed/garwood_stress_test_spikes.csv
  - dataset/processed/garwood_stress_test_event_study.csv
  - docs/paper/tables/table21_garwood_stress_test.csv (paper-ready summary)
"""

import csv
import math
import os
import unicodedata
from collections import defaultdict

from scipy.stats import chi2

BASE = os.path.join(os.path.dirname(__file__), "..", "..")
US_PATH = os.path.join(BASE, "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(BASE, "dataset", "istat", "istat_contanomi_full.csv")

MOVIE_PATH = os.path.join(BASE, "dataset", "movie_events_dataset.csv")
MUSIC_PATH = os.path.join(BASE, "dataset", "music_events_dataset.csv")
SPORTS_PATH = os.path.join(BASE, "dataset", "sports_events_dataset.csv")

OUT_SPIKES = os.path.join(BASE, "dataset", "processed", "garwood_stress_test_spikes.csv")
OUT_EVENTS = os.path.join(BASE, "dataset", "processed", "garwood_stress_test_event_study.csv")
OUT_TABLE = os.path.join(BASE, "docs", "paper", "tables", "table21_garwood_stress_test.csv")

ALPHA = 0.05
Z_THRESHOLD = 1.96

# --- 17 hand-verified spike/crash stories -----------------------------------
# (category, country, name, sex, event_year, n_pre, n_post)
# n_pre/n_post cross-checked directly against dataset/processed/us_names_long.csv,
# dataset/istat/istat_contanomi_full.csv, and the candidate CSVs
# (us_spike_candidates.csv, it_spike_candidates.csv, us_decline_candidates.csv,
# it_decline_candidates.csv) that back Tables "positive_spikes"/"negative_spikes".
SPIKE_ROSTER = [
    ("positivo", "USA", "Shirley", "F", 1935, 14476, 42366),
    ("positivo", "USA", "Tammy", "F", 1957, 193, 4365),
    ("positivo", "USA", "Nakia", "F", 1974, 7, 1135),
    ("positivo", "USA", "Jaime", "F", 1976, 259, 7838),
    ("positivo", "USA", "Devante", "M", 1991, 10, 131),
    ("positivo", "USA", "Mariah", "F", 1990, 423, 1103),
    ("positivo", "USA", "Nevaeh", "F", 2001, 8, 1199),
    ("positivo", "USA", "Jaslene", "F", 2007, 6, 501),
    ("positivo", "Italia", "Karol", "M", 2005, 2, 156),
    ("positivo", "Italia", "Chanel", "F", 2007, 8, 63),
    ("positivo", "Italia", "Adele", "F", 2012, 449, 1075),
    ("positivo", "Italia", "Elodie", "F", 2017, 13, 135),
    ("positivo", "Italia", "Soleil", "F", 2022, 98, 474),
    ("negativo", "USA", "Hillary", "F", 1993, 2520, 1064),
    ("negativo", "USA", "Kobe", "M", 2004, 1392, 625),
    ("negativo", "USA", "Alexa", "F", 2021, 2002, 708),
    ("negativo", "Italia", "Erica", "F", 2002, 863, 416),
]


def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def garwood_z(n: int, alpha: float = ALPHA) -> float:
    """Roccetti (2026) Eq. 6: pure count-based stress-test Z-score. N cancels out."""
    if n <= 0:
        return float("nan")
    ll_count = chi2.ppf(alpha / 2.0, df=2 * n) / 2.0
    se = math.sqrt(n)
    return (n - ll_count) / se


def load_us_counts():
    data = defaultdict(dict)
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name_norm = normalize(r["name"])
            sex = r["sex"].upper()
            year = int(r["year"])
            data[(name_norm, sex)][year] = int(r["count"])
    return data


def load_it_counts():
    data = defaultdict(dict)
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name_norm = normalize(r["name"])
            sex = r["gender"].upper()
            year = int(r["year"])
            data[(name_norm, sex)][year] = int(round(float(r["count"])))
    return data


def sum_pre_count(time_series, event_year, window=3):
    years = [y for y in range(event_year - window, event_year) if y in time_series]
    if not years:
        return None
    return sum(time_series[y] for y in years)


def sum_post_count(time_series, event_year, window=2):
    years = [y for y in (event_year + 1, event_year + 2)[:window] if y in time_series]
    if not years:
        if event_year in time_series:
            return time_series[event_year]
        return None
    return sum(time_series[y] for y in years)


def run_spike_roster():
    rows = []
    for category, country, name, sex, year, n_pre, n_post in SPIKE_ROSTER:
        z_pre = garwood_z(n_pre)
        z_post = garwood_z(n_post)
        rows.append({
            "categoria": category,
            "paese": country,
            "nome": name,
            "sesso": sex,
            "anno": year,
            "n_pre": n_pre,
            "n_post": n_post,
            "Z_pre": round(z_pre, 3),
            "Z_post": round(z_post, 3),
            "supera_pre": z_pre >= Z_THRESHOLD,
            "supera_post": z_post >= Z_THRESHOLD,
        })

    os.makedirs(os.path.dirname(OUT_SPIKES), exist_ok=True)
    fieldnames = ["categoria", "paese", "nome", "sesso", "anno", "n_pre", "n_post",
                  "Z_pre", "Z_post", "supera_pre", "supera_post"]
    with open(OUT_SPIKES, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n=== Roster 17 casi picco/crollo (RQ2) -> {OUT_SPIKES} ===")
    print(f"{'nome':10s} {'paese':7s} {'anno':5s} {'n_pre':7s} {'n_post':7s} {'Z_pre':7s} {'Z_post':7s} post>=1.96?")
    n_clear_post = 0
    n_clear_pre = 0
    for r in rows:
        flag = "SI" if r["supera_post"] else "no"
        if r["supera_post"]:
            n_clear_post += 1
        if r["supera_pre"]:
            n_clear_pre += 1
        print(f"{r['nome']:10s} {r['paese']:7s} {r['anno']:<5d} {r['n_pre']:<7d} {r['n_post']:<7d} "
              f"{r['Z_pre']:<7.3f} {r['Z_post']:<7.3f} {flag}")
    print(f"\n{n_clear_post}/{len(rows)} superano Z>=1.96 sul conteggio POST-evento; "
          f"{n_clear_pre}/{len(rows)} sul conteggio PRE-evento (baseline).")
    return rows


def run_event_study():
    us_data = load_us_counts()
    it_data = load_it_counts()

    all_events = []
    for path, category in ((MOVIE_PATH, "Cinema & Serie TV"), (MUSIC_PATH, "Musica & Pop Culture"),
                            (SPORTS_PATH, "Sport")):
        with open(path, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                r["_category"] = category
                all_events.append(r)

    rows = []
    for ev in all_events:
        name = ev["character"]
        name_norm = normalize(name)
        sex = ev["sex"].upper()
        country = ev["country"].upper()
        event_year = int(ev["year"])
        category = ev["_category"]

        series_db = us_data if country == "US" else it_data
        time_series = series_db.get((name_norm, sex), {})

        n_pre = sum_pre_count(time_series, event_year)
        n_post = sum_post_count(time_series, event_year)
        if n_pre is None or n_post is None:
            continue

        z_post = garwood_z(n_post)
        rows.append({
            "categoria": category,
            "anno": event_year,
            "paese": country,
            "titolo": ev["title"],
            "nome": name,
            "sesso": sex,
            "n_pre_somma": n_pre,
            "n_post_somma": n_post,
            "Z_post": round(z_post, 3) if not math.isnan(z_post) else "",
            "supera_post": (z_post >= Z_THRESHOLD) if not math.isnan(z_post) else False,
        })

    os.makedirs(os.path.dirname(OUT_EVENTS), exist_ok=True)
    fieldnames = ["categoria", "anno", "paese", "titolo", "nome", "sesso",
                  "n_pre_somma", "n_post_somma", "Z_post", "supera_post"]
    with open(OUT_EVENTS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n=== Event Study (N={len(rows)} eventi validi) -> {OUT_EVENTS} ===")
    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["categoria"]].append(r)

    summary = []
    for category in ("Cinema & Serie TV", "Musica & Pop Culture", "Sport"):
        cat_rows = by_cat[category]
        n_total = len(cat_rows)
        n_clear = sum(1 for r in cat_rows if r["supera_post"])
        median_n_post = sorted(r["n_post_somma"] for r in cat_rows)[n_total // 2] if n_total else 0
        pct_clear = 100.0 * n_clear / n_total if n_total else 0.0
        print(f"{category:25s}: {n_clear}/{n_total} eventi ({pct_clear:.1f}%) con Z_post>=1.96 "
              f"(mediana n_post={median_n_post})")
        summary.append({
            "categoria": category,
            "n_eventi": n_total,
            "n_clear_1_96": n_clear,
            "pct_clear": round(pct_clear, 1),
            "mediana_n_post": median_n_post,
        })

    n_total_all = len(rows)
    n_clear_all = sum(1 for r in rows if r["supera_post"])
    print(f"{'TOTALE':25s}: {n_clear_all}/{n_total_all} eventi ({100.0*n_clear_all/n_total_all:.1f}%) con Z_post>=1.96")
    summary.append({
        "categoria": "TOTALE",
        "n_eventi": n_total_all,
        "n_clear_1_96": n_clear_all,
        "pct_clear": round(100.0 * n_clear_all / n_total_all, 1),
        "mediana_n_post": sorted(r["n_post_somma"] for r in rows)[n_total_all // 2],
    })

    os.makedirs(os.path.dirname(OUT_TABLE), exist_ok=True)
    table_fieldnames = ["categoria", "n_eventi", "n_clear_1_96", "pct_clear", "mediana_n_post"]
    with open(OUT_TABLE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=table_fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary)
    print(f"Saved paper summary table -> {OUT_TABLE}")
    return rows, summary


def main():
    run_spike_roster()
    run_event_study()


if __name__ == "__main__":
    main()
