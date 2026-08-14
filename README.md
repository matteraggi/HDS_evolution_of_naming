# The Evolution of Naming: Cultural Diversity, Media Influence, and Individualism in Baby Names (US vs. Italy)

Human Data Science course paper. See project plan for full research questions, methodology, and team split.

## Data sources

- **US**: SSA "Baby Names from Social Security Card Applications", national data, 1880-2025.
  `https://www.ssa.gov/oact/babynames/names.zip` (CC0). Raw files in `data/raw/ssa/` (gitignored, ~8MB zip + 146 yobYYYY.txt).
- **Italy**: ISTAT annual "Natalità e fecondità della popolazione residente" reports (CC-BY 3.0 IT), collected manually
  year by year since ISTAT does not publish a bulk name x year x count table. Raw PDFs and extracted CSV in `data/raw/istat/`.

## Repro steps

```bash
# 1. Download & extract SSA data into data/raw/ssa/ (names.zip -> yobYYYY.txt files)
python src/scripts/01_process_ssa.py       # long table + per-sex diversity metrics
python src/scripts/02_mann_kendall_us.py   # Mann-Kendall trend tests, US
python src/scripts/03_us_italy_comparison.py  # US vs Italy statistical comparison (needs istat_annual_top_names.csv)
python src/scripts/04_plot_us_entropy.py       # Figure 2: US entropy 1880-2025 (depth, non-comparative)
python src/scripts/05_plot_us_italy_comparison.py  # Figure 5: US vs Italy top-30 concentration, core RQ1 figure
```

## Outputs (Person A / data track)

- `data/processed/us_names_long.csv` — full name/year/sex/count/rel_freq table, 1880-2025 (gitignored, ~85MB, regenerate via script 01).
- `data/processed/us_diversity_metrics.csv` — per year/sex: total_births, distinct_names, shannon_entropy, top10_share, top30_share.
- `data/processed/us_mann_kendall_results.csv` — Mann-Kendall trend test per sex/window/metric (US).
- `data/raw/istat/istat_annual_top_names.csv` — ISTAT top-30 concentration % and top-5 names, 2004 + 2006-2024 (see `data/raw/istat/COLLECTION_NOTES.md` for source-by-source detail).
- `data/processed/us_italy_comparison.csv` — Mann-Kendall + Wilcoxon + bootstrap slope-CI comparison, US vs Italy, 2006-2024.
- `docs/paper/tables/` — Table 1 (dataset overview) and Table 13 (ISTAT vs SSA structure comparison).
- `docs/paper/figures/` — Figure 2 (US entropy depth chart) and Figure 5 (core RQ1 US/Italy comparison chart).
- `docs/paper/metodologie_dati_DRAFT.md` — ~1900-word Italian draft of the Metodologie/Dati section.

## Key findings so far

- **US**: name concentration falling, entropy rising, continuously and significantly (Mann-Kendall p < 0.001 across
  all sexes/windows/metrics) — top-10 male names covered ~44% of male births in 1880, ~8% in 2025.
- **US vs Italy (2006-2024 overlap)**: Italy is *systematically* more concentrated than the US in every single year
  for both sexes (Wilcoxon p < 0.0001). Male-name diversification speed is statistically indistinguishable between
  the two countries (Sen's slope CIs overlap); female-name diversification is significantly *faster* in Italy
  (non-overlapping CIs) — the gap is closing for girls' names but not for boys'.

## Two open decisions for the team before this is final

1. **Comparable window narrowed to 2006-2024** (not 1999-2025 as originally planned) — no ISTAT report or secondary
   compilation for 1999-2003 or 2005 could be found publicly, despite searching.
2. **15 of 19 comparable-window years for Italy rely on nomix.it**, a non-academic secondary site, for the exact
   top-30 %/top-5 counts (only 2011-2024 are verified against a directly-downloaded ISTAT PDF). Cross-checked
   successfully against ISTAT PDFs in 3 spot-checks (2020/2022/2024) but not verified year-by-year. Consider manual
   verification of a subset of 2004-2010 before submission if time allows.
