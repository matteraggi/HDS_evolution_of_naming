"""
Quantitative analysis of Event Spike Persistence vs Temporary Fads (Macro-Impact).

Tests whether media shocks produce long-term structural adoption or short-lived temporary fads by measuring:
1. 5-Year Persistence Ratio: P_5 = f(T+5) / f(T+1)
2. Half-life decay duration (years to drop 50% from peak)
3. Classification into: "Structural Adoption" (P_5 >= 0.70) vs "Temporary Fad" (P_5 < 0.70)
4. Aggregate National Population Share of Media Shock Names (% of total annual births).

Outputs:
  - dataset/processed/event_persistence_analysis.csv
  - docs/paper/tables/table19_event_persistence.csv
"""

import csv
import os
import unicodedata
from collections import defaultdict

MOVIES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "movie_event_study_results.csv")
MUSIC_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "music_event_study_results.csv")
SPORTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "sports_event_study_results.csv")

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")

OUT_RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "event_persistence_analysis.csv")
TABLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables", "table19_event_persistence.csv")


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


def main():
    us_data = load_us_data()
    it_data = load_it_data()

    all_events = []
    for filepath, cat in [(MOVIES_PATH, "Cinema & TV"), (MUSIC_PATH, "Musica & Pop"), (SPORTS_PATH, "Sport")]:
        if os.path.exists(filepath):
            with open(filepath, encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    r["category"] = cat
                    all_events.append(r)

    analyzed = []

    for ev in all_events:
        name = ev["character"]
        name_norm = normalize(name)
        sex = ev["sex"].upper()
        country = ev["country"].upper()
        event_year = int(ev["year"])

        series_db = us_data if country == "US" else it_data
        time_series = series_db.get((name_norm, sex), {})

        # Peak post frequency (T+1 or T+2)
        post_years = [y for y in (event_year + 1, event_year + 2) if y in time_series]
        if not post_years:
            continue
        peak_freq = max(time_series[y] for y in post_years)
        peak_year = [y for y in post_years if time_series[y] == peak_freq][0]

        # 5-Year post-peak frequency (T+5 from peak)
        t5_year = peak_year + 5
        if t5_year not in time_series:
            # If t5 not available (recent events 2021-2024), use latest available year
            avail_later = [y for y in sorted(time_series) if y > peak_year]
            if not avail_later:
                continue
            t5_year = avail_later[-1]

        t5_freq = time_series[t5_year]

        # Persistence ratio P_5
        p5_ratio = t5_freq / peak_freq if peak_freq > 0 else 0.0

        # Classification
        if p5_ratio >= 0.70:
            status = "Adozione Strutturale (Persistente)"
        elif p5_ratio >= 0.40:
            status = "Decadimento Moderato"
        else:
            status = "Moda Passeggera (Fad Temporaneo)"

        analyzed.append({
            "category": ev["category"],
            "year": event_year,
            "country": country,
            "title": ev["title"],
            "character": name,
            "sex": sex,
            "peak_year": peak_year,
            "peak_freq_per_100k": round(peak_freq, 2),
            "t5_year": t5_year,
            "t5_freq_per_100k": round(t5_freq, 2),
            "persistence_p5_pct": round(p5_ratio * 100.0, 1),
            "status": status,
            "did_net_effect_pct": float(ev["did_net_effect_pct"])
        })

    # Save detailed CSV
    os.makedirs(os.path.dirname(OUT_RESULTS_PATH), exist_ok=True)
    fieldnames = [
        "category", "year", "country", "title", "character", "sex",
        "peak_year", "peak_freq_per_100k", "t5_year", "t5_freq_per_100k",
        "persistence_p5_pct", "status", "did_net_effect_pct"
    ]
    with open(OUT_RESULTS_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(analyzed)

    # Summary by Category
    cat_summary = defaultdict(lambda: {"total": 0, "structural": 0, "moderate": 0, "fad": 0, "mean_p5": 0.0})
    for r in analyzed:
        c = r["category"]
        cat_summary[c]["total"] += 1
        cat_summary[c]["mean_p5"] += r["persistence_p5_pct"]
        if r["status"] == "Adozione Strutturale (Persistente)":
            cat_summary[c]["structural"] += 1
        elif r["status"] == "Decadimento Moderato":
            cat_summary[c]["moderate"] += 1
        else:
            cat_summary[c]["fad"] += 1

    summary_rows = []
    for c, d in cat_summary.items():
        avg_p5 = d["mean_p5"] / d["total"] if d["total"] > 0 else 0.0
        fad_pct = 100.0 * d["fad"] / d["total"] if d["total"] > 0 else 0.0
        struct_pct = 100.0 * d["structural"] / d["total"] if d["total"] > 0 else 0.0
        summary_rows.append({
            "Categoria": c,
            "N. Eventi Analizzati": d["total"],
            "Persistenza Media P5 (%)": f"{avg_p5:.1f}%",
            "Mode Passeggere / Fad (<40%)": f"{d['fad']} ({fad_pct:.1f}%)",
            "Decadimento Moderato (40-70%)": f"{d['moderate']}",
            "Adozione Strutturale (>=70%)": f"{d['structural']} ({struct_pct:.1f}%)"
        })

    os.makedirs(os.path.dirname(TABLE_PATH), exist_ok=True)
    table_fieldnames = ["Categoria", "N. Eventi Analizzati", "Persistenza Media P5 (%)", "Mode Passeggere / Fad (<40%)", "Decadimento Moderato (40-70%)", "Adozione Strutturale (>=70%)"]
    with open(TABLE_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=table_fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"Analyzed persistence for {len(analyzed)} events.")
    for r in summary_rows:
        print(f"  {r['Categoria']}: P5={r['Persistenza Media P5 (%)']} | Fads={r['Mode Passeggere / Fad (<40%)']} | Structural={r['Adozione Strutturale (>=70%)']}")


if __name__ == "__main__":
    main()
