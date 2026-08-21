"""
Quantify the bias that ISTAT contanomi's per-year coverage limit introduces into
the US-Italy cosine similarity score.

Method: 2022, 2023 and 2024 have the TRUE complete distribution for Italy. This
script computes the true cosine similarity between US and Italy for those reference
years, then artificially truncates the Italy distributions down to each actual depth
limit observed in manifest.csv (e.g. 137, 375, 377, 5577), recomputes the cosine
similarity against the full US distribution, and measures the empirical bias.

Output: dataset/processed/it_cosine_bias_check.csv
    (depth, mean_cosine_bias, mean_cosine_bias_percent)
"""

import csv
import math
import os
import unicodedata
from collections import defaultdict

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
MANIFEST_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "istat", "contanomi_raw", "manifest.csv"
)
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "it_cosine_bias_check.csv"
)
REFERENCE_YEARS = (2022, 2023, 2024)
SEX_MAP = {"M": "m", "F": "f"}


def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def load_us():
    vecs = defaultdict(lambda: defaultdict(float))
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            y = int(r["year"])
            if y in REFERENCE_YEARS:
                vecs[(y, r["sex"])][normalize(r["name"])] += float(r["rel_freq"])
    return vecs


def load_italy_reference():
    # returns (year, gender) -> dict of name -> share (sorted by share descending)
    raw = defaultdict(lambda: defaultdict(float))
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            y = int(r["year"])
            if y in REFERENCE_YEARS:
                raw[(y, r["gender"])][normalize(r["name"])] += float(r["percent"]) / 100.0
    
    sorted_vecs = {}
    for key, name_map in raw.items():
        sorted_vecs[key] = dict(sorted(name_map.items(), key=lambda item: item[1], reverse=True))
    return sorted_vecs


def load_actual_depths():
    depths = set()
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["limit_used"] != "cached":
                depths.add(int(r["limit_used"]))
    return sorted(depths)


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    names = set(vec_a) | set(vec_b)
    dot = sum(vec_a.get(n, 0.0) * vec_b.get(n, 0.0) for n in names)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def main():
    depths = load_actual_depths()
    us_vecs = load_us()
    it_ref_vecs = load_italy_reference()

    rows = []
    for depth in depths:
        bias_list = []
        bias_pct_list = []
        for year in REFERENCE_YEARS:
            for us_sex, it_gender in SEX_MAP.items():
                us_vec = us_vecs.get((year, us_sex))
                it_full_vec = it_ref_vecs.get((year, it_gender))
                if not us_vec or not it_full_vec:
                    continue

                full_sim = cosine_similarity(us_vec, it_full_vec)

                # truncate Italy vector to 'depth' top items
                truncated_items = list(it_full_vec.items())[:depth]
                it_trunc_vec = dict(truncated_items)

                trunc_sim = cosine_similarity(us_vec, it_trunc_vec)

                bias = trunc_sim - full_sim
                bias_pct = 100.0 * bias / full_sim if full_sim != 0 else 0.0

                bias_list.append(bias)
                bias_pct_list.append(bias_pct)

        n = len(bias_list)
        mean_bias = sum(bias_list) / n if n > 0 else 0.0
        mean_bias_pct = sum(bias_pct_list) / n if n > 0 else 0.0

        rows.append({
            "depth": depth,
            "mean_cosine_bias": round(mean_bias, 6),
            "mean_cosine_bias_percent": round(mean_bias_pct, 4)
        })

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    fieldnames = ["depth", "mean_cosine_bias", "mean_cosine_bias_percent"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")
    print(f"{'depth':>6} {'cosine_bias':>14} {'cosine_bias_%':>14}")
    for r in rows:
        print(f"{r['depth']:6d} {r['mean_cosine_bias']:14.6f} {r['mean_cosine_bias_percent']:13.4f}%")


if __name__ == "__main__":
    main()
