"""
A "full dataset" version of 08_us_italy_name_overlap.py. That script only asked
"do the exact same 30 names appear in both countries' top-30 lists" - a coarse
yes/no on 60 names total, blind to everything below the very top tier.

This script instead treats each country/year/sex as a probability distribution
over ALL names it captured that year (not just the top 30), and measures how
similar the two distributions are with cosine similarity - the standard way to
compare two frequency vectors. Concretely: build one vector per country where
each dimension is a name and the value is that name's share of all births
(US: rel_freq column: already exact. Italy: percent/100 column: already
normalized against that year's TRUE total births by ISTAT itself, so this
works correctly even in partial-coverage years - see 01b's docstring). Cosine
similarity = 1.0 means identical usage patterns, 0.0 means completely
non-overlapping name choices.

This is naturally robust to Italy's per-year coverage gaps (see manifest.csv):
cosine similarity is dominated by high-frequency names, and even the
worst-covered year (2021) still captures every name popular enough to matter
to the dot product - the missing tail consists of names with tiny individual
weight, so they barely move the result either way. (Same robustness argument
as the top10/top30 share metric in 01c_check_coverage_bias.py, just applied
to a similarity score instead of a concentration ratio.)

Also reports top-100 overlap (not just top-30) as a simpler complementary
number - broader than the elite-tier-only version, still easy to state in
one sentence.

Output: dataset/processed/us_italy_distribution_similarity.csv
    (year, sex, cosine_similarity, top100_overlap_count)
"""

import csv
import math
import os
import unicodedata
from collections import defaultdict

import pymannkendall as mk

US_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_names_long.csv")
IT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "dataset", "istat", "istat_contanomi_full.csv")
OUT_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "dataset", "processed", "us_italy_distribution_similarity.csv"
)

SEX_MAP = {"M": "m", "F": "f"}
TOP_N_OVERLAP = 100


def normalize(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    return "".join(ch for ch in name.upper() if ch.isalpha())


def load_us():
    # (year, sex) -> {name: rel_freq}, summed across any duplicate-after-normalization spellings
    vecs = defaultdict(lambda: defaultdict(float))
    with open(US_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            vecs[(int(r["year"]), r["sex"])][normalize(r["name"])] += float(r["rel_freq"])
    return vecs


def load_italy():
    # (year, gender) -> {name: share}, from `percent` (already a % of true yearly total)
    vecs = defaultdict(lambda: defaultdict(float))
    with open(IT_PATH, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            vecs[(int(r["year"]), r["gender"])][normalize(r["name"])] += float(r["percent"]) / 100.0
    return vecs


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    names = set(vec_a) | set(vec_b)
    dot = sum(vec_a.get(n, 0.0) * vec_b.get(n, 0.0) for n in names)
    norm_a = math.sqrt(sum(v * v for v in vec_a.values()))
    norm_b = math.sqrt(sum(v * v for v in vec_b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def top_n_overlap(vec_a: dict, vec_b: dict, n: int) -> int:
    top_a = set(sorted(vec_a, key=lambda k: -vec_a[k])[:n])
    top_b = set(sorted(vec_b, key=lambda k: -vec_b[k])[:n])
    return len(top_a & top_b)


def main():
    us_vecs = load_us()
    it_vecs = load_italy()

    it_years = sorted(set(y for y, _ in it_vecs))
    rows = []
    for year in it_years:
        for us_sex, it_gender in SEX_MAP.items():
            us_vec = us_vecs.get((year, us_sex))
            it_vec = it_vecs.get((year, it_gender))
            if not us_vec or not it_vec:
                continue
            sim = cosine_similarity(us_vec, it_vec)
            overlap100 = top_n_overlap(us_vec, it_vec, TOP_N_OVERLAP)
            rows.append(
                {
                    "year": year,
                    "sex": us_sex,
                    "cosine_similarity": round(sim, 6),
                    "top100_overlap_count": overlap100,
                }
            )

    fieldnames = ["year", "sex", "cosine_similarity", "top100_overlap_count"]
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT_PATH}")

    for sex in ("M", "F"):
        sim_series = [r["cosine_similarity"] for r in rows if r["sex"] == sex]
        overlap_series = [r["top100_overlap_count"] for r in rows if r["sex"] == sex]
        years = [r["year"] for r in rows if r["sex"] == sex]
        if len(sim_series) >= 4:
            res_sim = mk.original_test(sim_series)
            res_ov = mk.original_test(overlap_series)
            print(f"\nsex={sex}, {years[0]}-{years[-1]}, n={len(sim_series)}")
            print(f"  cosine similarity:  trend={res_sim.trend:12s} p={res_sim.p:.4g} "
                  f"tau={res_sim.Tau:.3f}  ({sim_series[0]:.4f} -> {sim_series[-1]:.4f})")
            print(f"  top-100 overlap:    trend={res_ov.trend:12s} p={res_ov.p:.4g} "
                  f"tau={res_ov.Tau:.3f}  ({overlap_series[0]} -> {overlap_series[-1]} of {TOP_N_OVERLAP})")


if __name__ == "__main__":
    main()
