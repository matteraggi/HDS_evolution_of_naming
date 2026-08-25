"""
Quantitative Event Study for the Sports category.

Evaluates the impact of NBA Champions/MVPs, World Cup Champions (FIGC/FIFA),
and Serie A stars (1999-2024, US & IT) on baby name frequencies by measuring pre-event vs post-event
relative frequency changes, comparing each exposed name against the median change of all unexposed
names of the same sex/country within +/-35% of its pre-event frequency (Difference-in-Differences),
and running an overall Wilcoxon signed-rank test.

Outputs:
  - dataset/processed/sports_event_study_results.csv
  - docs/paper/tables/table18c_sports_event_study.csv
"""

import csv
import os
import unicodedata
from collections import defaultdict

import scipy.stats as stats

DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "sports_events_dataset.csv")
US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")

OUT_RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "sports_event_study_results.csv")
TABLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables", "table18c_sports_event_study.csv")


def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def load_us_data():
    data = defaultdict(dict)
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name_norm = normalize(r["name"])
            sex = r["sex"].upper()
            year = int(r["year"])
            freq = float(r["rel_freq"]) * 100000.0  # per 100,000 births
            data[(name_norm, sex)][year] = freq
    return data


def load_it_data():
    data = defaultdict(dict)
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            name_norm = normalize(r["name"])
            sex = r["gender"].upper()
            year = int(r["year"])
            freq = float(r["percent"]) * 1000.0  # per 100,000 births
            data[(name_norm, sex)][year] = freq
    return data


def get_baseline_freq(time_series, event_year):
    pre_years = [y for y in (event_year - 3, event_year - 2, event_year - 1) if y in time_series]
    if not pre_years:
        return None
    return sum(time_series[y] for y in pre_years) / len(pre_years)


def get_post_freq(time_series, event_year):
    post_years = [y for y in (event_year + 1, event_year + 2) if y in time_series]
    if not post_years:
        if event_year in time_series:
            return time_series[event_year]
        return None
    return sum(time_series[y] for y in post_years) / len(post_years)


def find_control_change(all_series, exposed_name, sex, event_year, pre_freq):
    matches = []
    for (name_norm, s), time_series in all_series.items():
        if s != sex or name_norm == exposed_name:
            continue
        c_pre = get_baseline_freq(time_series, event_year)
        c_post = get_post_freq(time_series, event_year)
        if c_pre is None or c_post is None or c_pre <= 0.1:
            continue
        if abs(c_pre - pre_freq) / pre_freq <= 0.35:
            c_delta_pct = 100.0 * (c_post - c_pre) / c_pre
            matches.append(c_delta_pct)

    if not matches:
        return 0.0
    matches.sort()
    return matches[len(matches) // 2]


def main():
    us_data = load_us_data()
    it_data = load_it_data()

    sports_events = []
    with open(DATASET_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sports_events.append(r)

    results = []
    treated_deltas = []
    did_deltas = []

    for ev in sports_events:
        name = ev["character"]
        name_norm = normalize(name)
        sex = ev["sex"].upper()
        country = ev["country"].upper()
        event_year = int(ev["year"])
        title = ev["title"]

        series_db = us_data if country == "US" else it_data
        time_series = series_db.get((name_norm, sex), {})

        pre_freq = get_baseline_freq(time_series, event_year)
        post_freq = get_post_freq(time_series, event_year)

        if pre_freq is None or post_freq is None:
            continue

        raw_jump = post_freq / pre_freq if pre_freq > 0 else 1.0
        delta_pct = 100.0 * (post_freq - pre_freq) / pre_freq if pre_freq > 0 else 0.0

        control_delta_pct = find_control_change(series_db, name_norm, sex, event_year, pre_freq)
        did_effect = delta_pct - control_delta_pct

        treated_deltas.append(delta_pct)
        did_deltas.append(did_effect)

        results.append({
            "year": event_year,
            "country": country,
            "title": title,
            "character": name,
            "sex": sex,
            "pre_freq_per_100k": round(pre_freq, 2),
            "post_freq_per_100k": round(post_freq, 2),
            "jump_ratio": round(raw_jump, 2),
            "delta_pct": round(delta_pct, 2),
            "control_delta_pct": round(control_delta_pct, 2),
            "did_net_effect_pct": round(did_effect, 2),
            "notes": ev["notes"]
        })

    os.makedirs(os.path.dirname(OUT_RESULTS_PATH), exist_ok=True)
    fieldnames = [
        "year", "country", "title", "character", "sex",
        "pre_freq_per_100k", "post_freq_per_100k", "jump_ratio",
        "delta_pct", "control_delta_pct", "did_net_effect_pct", "notes"
    ]
    with open(OUT_RESULTS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)

    os.makedirs(os.path.dirname(TABLE_PATH), exist_ok=True)
    table_fieldnames = ["Anno", "Paese", "Evento Sportivo", "Atleta / Nome", "Sesso", "Freq Pre (per 100k)", "Freq Post (per 100k)", "Impatto Netto DiD (%)"]
    table_rows = []
    for r in results:
        table_rows.append({
            "Anno": r["year"],
            "Paese": r["country"],
            "Evento Sportivo": r["title"],
            "Atleta / Nome": r["character"],
            "Sesso": r["sex"],
            "Freq Pre (per 100k)": r["pre_freq_per_100k"],
            "Freq Post (per 100k)": r["post_freq_per_100k"],
            "Impatto Netto DiD (%)": f"{r['did_net_effect_pct']:+.1f}%"
        })
    with open(TABLE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=table_fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(table_rows)

    w_stat, p_val = stats.wilcoxon(did_deltas)

    print(f"Executed Sports Event Study on {len(results)} valid sports events.")
    print(f"  Mean Net DiD Effect: {sum(did_deltas)/len(did_deltas):+.2f}%")
    print(f"  Wilcoxon Signed-Rank Test vs Controls: W = {w_stat:.1f}, p-value = {p_val:.4e}")
    print(f"Saved results -> {OUT_RESULTS_PATH}")
    print(f"Saved paper table -> {TABLE_PATH}")


if __name__ == "__main__":
    main()
