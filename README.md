# The Evolution of Naming: Cultural Diversity, Media Influence, and Individualism in Baby Names (US vs. Italy)

Human Data Science course paper. See `docs/project_plan_baby_names.md` for the original research
plan and `PROJECT_LOG.md` for a plain-language, dated log of what's changed since then and why.

## Data sources

- **US**: SSA "Baby Names from Social Security Card Applications", national data, 1880-2025.
  `https://www.ssa.gov/oact/babynames/names.zip` (CC0). Raw files in `dataset/names/` (gitignored, ~8MB
  zip + 146 `yobYYYY.txt` files).
- **Italy**: ISTAT, via an unauthenticated JSONP web service discovered behind the "contanomi" tool
  (`https://www.istat.it/wp-content/themes/EGPbs5-child/contanomi/nati/index2022.php`), scraped for all
  years 1999-2024. **Not the original plan** — see below. Per-year coverage varies (66-100% of births,
  see `dataset/istat/contanomi_raw/manifest.csv`); this is proven *not* to bias the paper's primary
  concentration-ratio metric (`docs/paper/tables/table14_coverage_bias_check.csv`, `fig4`). The earlier
  manual PDF/nomix.it collection (`dataset/istat/istat_annual_top_names.csv`, CC-BY 3.0 IT) is kept as
  a corroboration/citation trail, not deleted, but is no longer the backbone data source.

## Repro steps

```bash
# --- Data acquisition ---
# 1. Download & extract SSA data into dataset/names/ (names.zip -> yobYYYY.txt files)
python src/scripts/00_scrape_istat_contanomi.py    # scrapes ISTAT contanomi, 1999-2024

# --- Processing ---
python src/scripts/01_process_ssa.py               # US long table + per-sex diversity metrics
python src/scripts/01b_process_istat_contanomi.py  # Italy diversity metrics (with coverage/entropy-reliability flags)
python src/scripts/01c_check_coverage_bias.py       # proves top10/30 share is coverage-bias-free; entropy is not

# --- Statistical tests ---
python src/scripts/02_mann_kendall_us.py            # Mann-Kendall trend tests, US
python src/scripts/03_us_italy_comparison.py        # US vs Italy statistical comparison (Wilcoxon, bootstrap CIs)

# --- Spike-story hunting ---
python src/scripts/06_find_us_spikes.py             # candidate US year-over-year name jumps
python src/scripts/07_find_it_spikes.py             # candidate Italy year-over-year name jumps
python src/scripts/10_exhaustive_spike_table.py     # mechanical (non-curated) spike table, appendix

# --- Convergence/divergence ---
python src/scripts/08_us_italy_name_overlap.py             # top-30 overlap (superseded by 08b, kept for reference)
python src/scripts/08b_us_italy_distribution_similarity.py # full-distribution cosine similarity - primary metric

# --- Figures ---
python src/scripts/04_plot_us_entropy.py            # fig2: US entropy 1880-2025 (depth, non-comparative)
python src/scripts/11_plot_it_coverage.py           # fig3: ISTAT scrape completeness per year
python src/scripts/12_plot_coverage_bias.py         # fig4: coverage-depth sensitivity (entropy vs concentration ratio)
python src/scripts/05_plot_us_italy_comparison.py   # fig5: US vs Italy top-30 concentration, core RQ1 figure
python src/scripts/09_plot_convergence.py           # fig6: US/Italy name-pool convergence
python src/scripts/13_plot_spike_roster.py          # fig7: all curated spike stories, indexed & comparable
```

Scripts are numbered by pipeline stage, not strict run order; `01b`/`01c`/`08b` are follow-ons to `01`/`08`.

## Outputs

- `dataset/processed/us_names_long.csv` — full US name/year/sex/count/rel_freq table, 1880-2025 (gitignored,
  regenerate via script 01).
- `dataset/processed/us_diversity_metrics.csv` — US per year/sex: total_births, distinct_names,
  shannon_entropy, top10_share, top30_share.
- `dataset/istat/istat_contanomi_full.csv` — Italy name/year/gender/count/percent, 1999-2024
  (~219,000 rows).
- `dataset/processed/it_diversity_metrics.csv` — Italy per year/sex, with `entropy_reliable` flag
  (True only for 2022-2024).
- `dataset/processed/it_coverage_bias_check.csv` — the bias-sensitivity proof behind that flag.
- `dataset/processed/us_mann_kendall_results.csv`, `dataset/processed/us_italy_comparison.csv` — trend and
  cross-country statistical test results.
- `dataset/processed/us_spike_candidates.csv`, `dataset/processed/it_spike_candidates.csv` — mechanical
  year-over-year jump candidates (unverified; source for the curated roster below).
- `dataset/processed/exhaustive_spike_table.csv` — 87-row mechanically-filtered spike table (US
  ratio≥6x/count≥2000, Italy ratio≥2.5x/count≥150), appendix material.
- `dataset/processed/us_italy_distribution_similarity.csv` — full-distribution cosine similarity + top-100
  overlap, US vs Italy, by sex, 1999-2024.
- `docs/paper/tables/` — table1 (dataset overview), table13 (ISTAT vs SSA structure), table14 (coverage
  bias check).
- `docs/paper/figures/` — fig2, fig3, fig4, fig5, fig6, fig7 (see script list above).
- `docs/paper/metodologie_dati_DRAFT.md` — Italian draft of the Metodologie/Dati section.

## Key findings so far

- **US**: name concentration falling, entropy rising, continuously and significantly (Mann-Kendall
  p < 0.001 across all sexes/windows/metrics) — top-10 male names covered ~44% of male births in 1880,
  ~8% in 2025.
- **US vs Italy (1999-2024, full window)**: Italy is *systematically* more concentrated than the US in
  every single year for both sexes (Wilcoxon p < 0.0001). Male-name diversification speed is
  statistically indistinguishable between the two countries; female-name diversification is
  significantly *faster* in Italy — the gap is closing for girls' names but not for boys'.
- **Convergence**: the two countries' full name-frequency distributions are becoming significantly more
  similar over time (cosine similarity, both sexes p < 3e-11) — not just at the elite top-30 tier.
  Concrete example: Liam and Noah both newly entered Italy's top-30 by 2024, absent in 1999.
- **Spike stories**: 8 US + 5 Italy cause-verified event-driven name spikes, plus 4 cross-country
  common/shared cases (Celine Dion, Elsa/Frozen, Khaleesi, Isabella/Twilight) — see `PROJECT_LOG.md`
  for the full roster with sources.

## What changed from the original plan (see PROJECT_LOG.md for the full dated history)

The original plan (§4) stated ISTAT had no bulk name data and budgeted **manual PDF collection** as
real, unavoidable acquisition work. That held for a while — `dataset/istat/COLLECTION_NOTES.md`
documents the manual effort, and it got the comparable window to 2006-2024 with 15/19 years relying on
a secondary source (nomix.it). **That constraint no longer holds**: a real bulk API was found behind
ISTAT's own "contanomi" tool (undocumented, reverse-engineered from its JavaScript), and after
resolving several real server-side quirks (see `PROJECT_LOG.md`, 2026-08-14/16 entries), it now backs
the paper's entire Italy dataset — extending the comparable window to the full 1999-2024, removing the
secondary-source dependency, and (bonus) resolving the plan's flagged "RQ2 Italy: open task, no
candidate spike confirmed yet" — 5 solid Italy-specific spike stories now exist. **Not yet done**: RQ3
(gender-neutral name tracking, US and Italy) — no work has started on this.

## Open items before submission

1. RQ3 (gender-neutral naming) has not been started — the original plan scoped this to Person B.
2. Individual before/after mini-figures for the 2-3 strongest spike stories are optional/not yet built
   (the consolidated roster figure, fig7, may already cover this need).
3. The paper write-up itself (Italian, ≥5000 words, ≥10 figures/tables, required exam sections) hasn't
   started — all data/analysis/figures are ready as inputs to it.
