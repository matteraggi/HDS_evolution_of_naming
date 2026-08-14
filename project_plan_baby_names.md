# Project Plan — "Human Data Science" Course Paper

## Title (working)
**The Evolution of Naming: Cultural Diversity, Media Influence, and Individualism in Baby Names (US vs. Italy)**

> **Status update (2026-08-11)**: Research phase complete. Project is confirmed **doable**, with one required pivot (RQ1 metric, see §3/§5) and one open task (RQ2 Italian case study, see §10). Everything below reflects that pivot — this is the version to hand off.

---

## 1. Exam / Course Requirements (must respect)

- **Topic**: free choice — this plan covers the topic already chosen.
- **Structure required**: Abstract, Introduzione, Metodologie/Dati, Risultati, Discussione Finale, Bibliografia. Must also include **links to the data and software repositories used**.
- **Language**: paper must be written in **Italian**.
- **Submission**: sent to the professor **exclusively via email**.
- Since this is for an **Appello Ordinario** (not the end-of-course discussion in May):
  - **Minimum 5000 words** (text body)
  - **At least 10** tables/figures combined
  - Deliver the paper **at least one week before** the chosen exam date
- Four required focus areas the methodology must explicitly hit:
  1. **Gestione dei Dati** — dataset analysis with explicit source citation
  2. **Tecniche di Elaborazione** — deep discussion of data processing/methodology used
  3. **Validazione Scientifica** — techniques used to scientifically validate conclusions drawn from data
  4. **Fattore Umano** — analysis of the role/impact of human beings within the topic studied

---

## 2. Why This Topic

- Free of the two more "done before" risks discussed and rejected:
  - Recommendation-system bias (idea 5) — solid but generic/heavily tutorial-covered territory (MovieLens bias projects are extremely common).
  - Political ideology / cultural omnivore theory using GSS data — risks reading as a direct replication of a famous 1996 sociology paper (Peterson & Kern) using the exact dataset everyone uses for it.
- Baby-name data is less commonly used in coursework, gives full control over an original analysis, and still has real academic grounding to cite for validation (see §7).
- **Comparative US vs. Italy angle** is the key originality lever — most similar student projects only look at one country's data.
- Confirmed bonus: **no peer-reviewed paper on Italian name-diversity trends was found** during research — this is a genuine literature gap the paper can credibly claim to address, not just replicate.

---

## 3. Research Questions

- **RQ1 (diversity/concentration over time)**: How has naming diversity evolved over time in the US and in Italy, and do the two countries show similar or divergent trends?
  - **PIVOTED**: Italy's public data does not support full-distribution Shannon entropy (see §4). Use **top-N concentration ratio** (share of births covered by the top 10/30 names each year) as the primary cross-country metric — this is a validated approach in the literature (see §7, Ogihara 2025). Compute full Shannon entropy for the **US only** as a bonus "what complete data reveals" depth figure, not as the comparative metric.
  - **Comparable time window is 1999–2025 only** (~26 years) — Italy has no name-level data before 1999. Show full US 1880–2025 entropy separately for historical context, but don't claim a matched comparison outside 1999–2025.
- **RQ2 (media/event influence)**: Do identifiable cultural events (movies, TV shows, celebrities) produce measurable, quantifiable spikes in specific name frequencies, and are these spikes structurally different between the two countries?
  - US side is de-risked — strong validated case studies exist (see §10, §12).
  - **Italy side is an open task** — no candidate name/event pair confirmed yet. Must be found using ISTAT's per-name lookup tool ("contanomi") since bulk data doesn't exist (see §4, §10).
- **RQ3 (gender norms)**: Has the use of gender-neutral names increased over time, and does this trend differ between the US and Italy?
  - US: straightforward with SSA full data (existing prior art confirms this is a well-trodden, well-understood computation — see §12).
  - Italy: also constrained to whatever the "contanomi"/annual-report data allows per name; may need to build the male/female-split check only for the top-N names actually available, not the full population.

RQ1 and RQ3 remain the "backbone." RQ2 remains the "flashy" part but now has a **confirmed feasibility path** for the US and an **open task** for Italy (see §10, item 1).

---

## 4. Datasets (confirmed)

### US data — SSA (solid, no open issues)

- **Source**: U.S. Social Security Administration, "Baby Names from Social Security Card Applications."
- **Download**: national data at `https://www.ssa.gov/oact/babynames/names.zip` — one `yobYYYY.txt` file per year (1880–2025), comma-delimited, columns `name,sex,count` (year comes from the filename). Format documented in the zip's `NationalReadMe.pdf`.
- Optional bonus: state-level file at `https://www.ssa.gov/oact/babynames/state/namesbystate.zip`, format `state,sex,year,name,count`, coverage from 1910.
- **Coverage**: 1880–2025 (most recent SSA release, published spring 2026).
- **Threshold caveat**: only names given to ≥5 babies in a state/year are included (privacy suppression) — true diversity is slightly undercounted, especially for early decades and small states. Worth one sentence in Metodologie/Dati and Discussione Finale (limitations).
- **License**: CC0 / public domain, confirmed via [Data.gov catalog](https://catalog.data.gov/dataset/baby-names-from-social-security-card-applications-national-data).
- **Recommendation**: use the raw SSA zip as the primary source (authoritative, current, trivial to cite). A Kaggle mirror (e.g. `robikscube/us-baby-name-popularity`) can be used only as a quick sanity-check cross-validation — Kaggle mirrors are often stale (capped ~2017-2021).

### Italian data — ISTAT (harder, confirmed limitation — read carefully)

- **Portals**: `esploradati.istat.it` (dataset code `DCIS_NATI1`, "Nati - Serie storica"), `demo.istat.it` (app `FE3`, "Nascite" section), and the **"contanomi"** interactive tool at `https://www.istat.it/it/data/interactive-contents/baby-names/`.
- **⚠️ Critical limitation**: there is **no bulk downloadable name×year×sex×count table**, unlike SSA. What's actually available publicly:
  1. **"contanomi"** — a single-name lookup tool. You type one name + sex, get its yearly count series for **1999–2023/2024**. No way to enumerate all ~26,000 male / ~25,000 female distinct names through it in bulk.
  2. **Annual "Natalità e fecondità della popolazione residente" reports** (PDF/Excel, e.g. `istat.it/it/files/2017/11/Report-Nascite-e-fecondità.pdf`) — publish **top-30 (sometimes top-10) most frequent names per year**, nationally and by region, plus aggregate concentration stats (e.g. "top 30 names cover ~44-45% of male births, ~38-40% of female births").
- **Coverage**: name-level data starts **1 January 1999** — no pre-1999 name-level data exists at all. This is the hard floor that caps the comparative time window (see §3).
- **Regional breakdown**: exists in the annual reports (top name per region) but not confirmed as bulk-downloadable — treat as bonus-only if time allows, don't plan around it.
- **License**: CC-BY 3.0 IT (confirmed via `istat.it/en/data/open-data/`) — attribution to ISTAT required, not IODL 2.0.
- **Practical implication for methodology**: build the Italian time series manually from (a) the top-N tables in the annual reports across as many years 1999–2024 as can be found, and (b) individual "contanomi" lookups for specific candidate names needed for RQ2. This is **manual data-acquisition work**, not a scraping/API job — budget real time for it.
- **Supplementary resource**: [genderNamesITA](https://github.com/mrblasco/genderNamesITA) — ~32,000 Italian first names with gender (from local-administrator registries 1985–2014). Useful as a name→gender lookup dictionary, **not** a birth-year time series — do not use it as a substitute for the ISTAT counts.
- **No existing Kaggle dataset** with full Italian name/year/count data was found — confirms this really is manual-acquisition territory.

---

## 5. Methodology / Data Processing Techniques

1. **Cleaning & normalization**: aggregate raw yearly counts into name/year/sex/count tables per country (US: full table from SSA; Italy: top-N table built manually from annual reports + targeted contanomi lookups). Normalize by total births per year (relative frequency, not raw counts) to avoid population-size bias.
2. **Diversity metric** (pivoted, see §3):
   - **US**: full Shannon entropy (or Simpson's index) computable directly from the complete distribution — use as the deep/bonus metric.
   - **Both countries, primary comparative metric**: **top-N concentration ratio** — share of births covered by the top 10 and top 30 names per year. This is what's actually comparable given Italy's data ceiling, and is a validated approach in the literature (Ogihara 2025, UK study — see §7).
3. **Spike/anomaly detection**: year-over-year percentage change per name; flag statistically significant spikes (e.g. z-score threshold) for RQ2 case studies.
   - US: run on the full SSA distribution.
   - Italy: run only on the top-N names available per year, plus any specific candidate names pulled individually via contanomi.
4. **Case-study cross-referencing**: manually cross-reference top spikes against known cultural events/media releases. US-side candidates already validated (§10, §12). Italy-side candidates are an **open task** (§10).
5. **Gender-neutral name tracking**: for each year, compute share of names given to both sexes above a threshold (e.g. ≥25%/75% split) — straightforward for US (full data), constrained to top-N names for Italy.
6. **Comparative analysis**: align both countries on the **1999–2025 overlapping window only**; compare concentration-ratio trends, spike magnitude/frequency, and gender-neutral share trends side by side. Show US 1880–2025 entropy as a separate, clearly-labeled non-comparative depth figure.

Keep it in pandas/Python — no ML required, purely statistical/time-series techniques.

---

## 6. Validation Techniques (Validazione Scientifica)

- **Mann-Kendall trend test**: test whether the concentration-ratio / entropy series shows a statistically significant monotonic trend over time (per country). Standard citations: Mann, H.B. (1945), "Nonparametric Tests Against Trend," *Econometrica*, 13(3), 163-171; Kendall, M.G. (1975), *Rank Correlation Methods*, Charles Griffin. Originated in economics/hydrology but documented in social-science/demographic trend use as well — legitimate to cite here.
- **Sanity-check of the spike-detection method**: verify it correctly flags known, documented real-world cases (see §12 for a ready-made validation set: Elsa/Frozen, Khaleesi/Game of Thrones, Isabella/Twilight). If the method finds these using SSA data, it validates the detection approach before trusting it on Italian data (where the input is more limited).
- **Statistical comparison between countries**: appropriate test (e.g. comparing trend slopes, or a non-parametric test) to determine if US and Italy concentration-ratio trends are significantly different from each other over the 1999-2025 window, not just visually different.
- **Caveat/limitation discussion**: explicitly address correlation vs. causation when linking spikes to cultural events, **and** explicitly address the US/Italy data-asymmetry (full distribution vs. top-N only) as a methodological limitation — this is a genuine, defensible point for Discussione Finale, not a weakness to hide.

---

## 7. Human Factor Framing (Fattore Umano) — with confirmed citations

- Naming a child is one of the most intimate, individual human decisions — yet this analysis shows it is systematically shaped by external, collective forces (mass media, celebrity culture, generational shifts in values).
- **Bibliografia-ready citations**:
  - Lieberson, S. (2000). *A Matter of Taste: How Names, Fashions, and Culture Change*. Yale University Press. ISBN 0-300-08385-8. Foundational: naming as a "pure" fashion/diffusion case, internally-driven taste change (habituation/satiation) rather than pure event-reaction.
  - Lieberson, S. & Bell, E.O. (1992). "Children's First Names: An Empirical Study of Social Taste." *American Journal of Sociology*, 98(3), 511-554. Quantitative precursor to the 2000 book; girls' names change faster than boys' — relevant to RQ3 framing.
  - Twenge, J.M., Abebe, E.M., & Campbell, W.K. (2010). "Fitting In or Standing Out: Trends in American Parents' Choices for Children's Names, 1880-2007." *Social Psychological and Personality Science*, 1(1), 19-25. https://doi.org/10.1177/1948550609349515 — uses SSA data directly, near-identical methodology to RQ1/RQ3, links declining common-name usage to rising individualism.
  - Twenge, J.M. et al. (2016). "Still Standing Out: Children's Names in the United States During the Great Recession and Correlations with Economic Indicators." *Journal of Applied Social Psychology*. https://onlinelibrary.wiley.com/doi/10.1111/jasp.12409
  - Ogihara, Y. (2025). "Popularity and Diversity: The Negative Relationship in Baby Names in the United Kingdom." *F1000Research*, 14, 424. https://doi.org/10.12688/f1000research.162476.3 — **direct methodological precedent** for using top-name concentration as a diversity proxy (r ≈ -0.96 to -0.99 vs. name-variety ratio, UK 1996-2016). Cite this explicitly when justifying the RQ1 pivot.
  - Ogihara, Y. (2025). "Name Uniqueness and the Rise of Individualism in the Western Hemisphere (1500-2000)." *Current Research in Ecological and Social Psychology*. https://www.sciencedirect.com/science/article/pii/S266662272500022X
- Frame the gender-neutral naming trend (RQ3) as a direct marker of evolving human social norms around gender.
- Frame the US/Italy comparison as evidence of how globalized media does or doesn't override local/national naming traditions.
- **New framing point from research**: the very fact that Italy's public data infrastructure only supports partial (top-N) analysis while the US supports full-distribution analysis is itself worth a sentence in Fattore Umano/Discussione — it says something about differing institutional transparency/data culture, a "human factor" one level up from naming itself.

---

## 8. Target Figures/Tables (aim for 12-15 to comfortably clear the 10 minimum)

1. Table: dataset overview (sources, years covered, records, overlap window, **and the US/Italy data-granularity asymmetry**)
2. Line chart: full Shannon entropy over time — US only (1880-2025, depth/bonus figure)
3. Line chart: top-N concentration ratio over time — US (1999-2025, comparative metric)
4. Line chart: top-N concentration ratio over time — Italy (1999-2024/2025)
5. Combined line chart: US vs Italy concentration ratio, overlapping years (the core RQ1 comparison figure)
6. Bar chart: top 10 names' share of total births per decade/period, both countries
7. Case-study chart #1: a specific US name spike with annotated event (from validated set, §12)
8. Case-study chart #2: a specific Italian name spike with annotated event (**pending — open task**, §10)
9. Bar/line chart: gender-neutral name share over time, US vs Italy
10. Table: Mann-Kendall trend test results (both countries, all key metrics)
11. Table: top spike detections per decade/period (both countries) with candidate real-world cause
12. Table/summary: statistical comparison of trend significance between countries
13. Table: ISTAT vs SSA data-structure comparison (methodological transparency, doubles as a Metodologie/Dati table)
14. (Optional bonus) Heatmap: name popularity rank by decade, top names, US
15. (Optional bonus) Map or regional breakdown: top Italian name by region (if the regional data turns out usable)

---

## 9. Suggested Outline & Word Budget (target ~5500-7000 words)

- Abstract — ~150 words
- Introduzione — ~650 words (context, prior literature, research questions)
- Metodologie/Dati — ~1700 words (data sources, the US/Italy asymmetry and why the metric pivoted, cleaning, normalization, concentration-ratio calc, spike detection method, validation methodology) — most tables live here
- Risultati — ~1800-2200 words (present RQ1, RQ2, RQ3 findings in turn, most figures live here)
- Discussione Finale — ~1100-1300 words (interpretation, human factor discussion incl. the data-asymmetry point, US/Italy comparison meaning, limitations, correlation-vs-causation caveat)
- Bibliografia — not counted in word limit, separate

Calibration note (from inspecting two prior UniBo Human Data Science exam repos): both landed at 4,500-7,000 words in dense two-column IEEE PDF format with only 5-6 figures each — below the 10-figure minimum. Treat 10 figures as a floor to clear, not a peer benchmark; 12-15 is the safer target.

---

## 10. Next Steps (updated, prioritized)

1. **[Person B, do first]** Test ISTAT's "contanomi" tool (`istat.it/it/data/interactive-contents/baby-names/`) against 3-5 candidate Italian name/cultural-event pairs (popular Italian TV show or telenovela character, a footballer's or celebrity's child's name, a Sanremo moment, etc.) to find whether a real, quantifiable RQ2 spike exists for Italy. **This determines whether RQ2 is fully achievable or needs to be scoped down to US-only with Italy discussed qualitatively.** Do this early — it was already flagged as a feasibility risk in the original plan and is now the single most important open task.
2. **[Person A, do first]** Manually collect ISTAT's annual "Natalità e fecondità" top-N tables for as many years 1999-2024 as available (PDF/Excel), building a clean top-10/top-30-concentration-by-year CSV. This is the actual data-acquisition bottleneck for Italy — budget real time, it's manual, not scriptable via a bulk API.
3. **[Person A]** Download raw SSA `names.zip`, compute both full Shannon entropy and the same top-N concentration metric on US data for apples-to-apples comparability with Italy.
4. **[Both]** Once §10.1-3 confirm what's really usable, finalize the Metodologie/Dati section language around the concentration-ratio pivot **before** writing Risultati, so the limitation reads as an upfront methodological choice, not a mid-paper discovery.
5. Find the specific academic citations already confirmed in §7 (Lieberson, Twenge, Ogihara) plus any additional Italian-specific naming literature if it surfaces during the ISTAT manual collection.
6. Set up the GitHub repo early (required deliverable) — see §12 for two prior-year UniBo exam repos to use as structural templates, especially `gabb-OS/war-shock-oil-profit-analysis` for section structure and `papum20/...Olympics-hosting-advantage` for code organization (`src/scripts` by technique, `docs/paper` for the LaTeX report).

---

## 11. Team Split Suggestion (2 people)

- **Person A**: data acquisition (SSA download + manual ISTAT top-N table collection) + cleaning + concentration-ratio/entropy computation + validation tests (Mann-Kendall, statistical comparison) → owns Metodologie/Dati section.
- **Person B**: contanomi-based Italian spike-candidate research (§10.1) + US spike detection + case-study research + gender-neutral trend analysis + figures → owns most of Risultati section.
- Both: co-write Introduzione, Discussione Finale (incl. the data-asymmetry human-factor point), and reconcile Abstract together at the end.

---

## 12. Research Findings — Sources & Prior Art (for citations and repo links)

### Confirmed dataset URLs
- SSA national: `https://www.ssa.gov/oact/babynames/names.zip` (CC0)
- SSA state-level: `https://www.ssa.gov/oact/babynames/state/namesbystate.zip`
- ISTAT contanomi: `https://www.istat.it/it/data/interactive-contents/baby-names/`
- ISTAT databrowser: `https://esploradati.istat.it/databrowser/` (dataset `DCIS_NATI1`)
- ISTAT demo portal: `https://demo.istat.it/app/?i=FE3&l=it`

### Prior-art GitHub repos (US baby names, Python/pandas)
- [PhantomInsights/baby-names-analysis](https://github.com/PhantomInsights/baby-names-analysis) — full SSA ETL 1880-2020, gender-neutral name identification.
- [dcadata/gender-neutral-names](https://github.com/dcadata/gender-neutral-names) — female:male ratio per name/year, directly matches RQ3 methodology.
- [YilunCai627/US-Popular-Baby-Names-Trend-Analysis-using-Python](https://github.com/YilunCai627/US-Popular-Baby-Names-Trend-Analysis-using-Python)
- [combax/EDA-of-US-baby-names](https://github.com/combax/EDA-of-US-baby-names)
- [genderNamesITA](https://github.com/mrblasco/genderNamesITA) — Italian names + gender dictionary (not time series).
- Stat Significant articles (data journalism, useful for spike methodology inspiration): [Celebrities](https://www.statsignificant.com/p/which-celebrities-popularized-or), [Movies](https://www.statsignificant.com/p/which-movies-popularized-or-tarnished)

### Validated US spike case studies (for RQ2 + spike-detection sanity check)
- **Elsa** (Frozen, 2013): 566 (2013) → 1,140 births (2014), rank 527→286, first top-500 since 1917.
- **Khaleesi** (Game of Thrones): 0 births 1880-2011 → entered top 1000 by 2014, rank 757→549 by 2018.
- **Isabella** (Twilight): #48 (2000) → #1 US girls' name (2009-2010).
- Official precedent for this kind of analysis: UK ONS, ["10 Pop Culture Influences on Baby Names"](https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/articles/10popcultureinfluencesonbabynamesgameofthronesmarvelfrozenandmore/2015-08-17) (2015) — a national statistics agency doing exactly this kind of quantified spike analysis, good methodological citation.

### Italian naming trend commentary (not academic, but useful context)
- Il Post, ["È più originale chiamarla Isabel o Martina?"](https://www.ilpost.it/2025/05/29/nomi-neonati-italia-moda/) (2025)
- Il Post, ["Quali sono i nomi più usati in Italia?"](https://www.ilpost.it/2015/11/27/nomi-piu-usati-in-italia-istat/) (2015)
- ISTAT annual news release example: ["Nomi dei nuovi nati, ecco il podio del 2023"](https://www.istat.it/news-dati-alla-mano/nomi-dei-nuovi-nati-ecco-il-podio-del-2023/)

### Calibration repos (prior UniBo Human Data Science exam projects, same course)
- [papum20/unibo__projects__Olympics-hosting-advantage](https://github.com/papum20/unibo__projects__Olympics-hosting-advantage/tree/master) — 3-person team, 14-page IEEE report (~6,000-7,000 words), 5 figures/tables, methods: Sign test, Spearman, Bayesian changepoint detection, ADF, OLS+VIF, ZINB regression. Good template for `src/` code organization.
- [gabb-OS/war-shock-oil-profit-analysis](https://github.com/gabb-OS/war-shock-oil-profit-analysis) — smaller team, 7-page IEEE report (~4,500-5,500 words), 6 figures/tables, methods: OLS, ARIMA, Theil-Sen+bootstrap, Bayesian AR(1) (PyMC), Wilcoxon, Fisher/Stouffer triangulation. **Best template for section structure** (Abstract/Introduzione/Dati e Metodologie/Risultati/Discussione Finale + "La dimensione umana" + "Limiti e avvertenze" + Bibliografia maps almost exactly onto exam requirements).
- **Takeaway**: both examples fall below the 10-figure minimum — don't calibrate down to them. Target 4-8 scripts/notebooks, 12-15 figures/tables, 2-4 distinct statistical methods, 5,500-7,000 words.
