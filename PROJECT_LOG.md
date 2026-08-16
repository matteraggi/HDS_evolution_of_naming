# Project Log

A plain-language running log of this project: what we're trying to do, what's been tried, and what's
still open. For the full academic plan (research questions, methodology, citations, course
requirements) see the original plan doc; for repro steps see `README.md`. This file is the quick
"where are we, what's next" reference.

---

## Main objective

Course paper for "Human Data Science" (exam paper, written in Italian, ≥5000 words, ≥10 figures/tables,
sent to the professor by email, at least a week before the exam).

**In plain terms**: a paper about US and Italian baby names, built around two things:

1. **A short, solid backbone**: are people spreading out across more different names over time, or
   sticking to the same few? Answer already confirmed with real statistics for both countries,
   1999–2024 — a supporting section, not the main event.
2. **The main event — spike stories**: specific movies, TV shows, celebrities, or news events that
   caused a name to visibly jump in popularity, in the US and/or Italy. **This is the paper's main
   draw** (decided 2026-08-16, when time pressure eased and scope was deliberately widened).

**Why put the two together**: names are a very personal choice, yet they're clearly pulled around
by things outside any one parent's control — slow generational shifts (the backbone) and sudden
cultural moments (the spikes). Comparing US and Italy shows whether that pull works the same way
in different cultures, and — new angle, added 2026-08-16 — whether the two countries' naming pools
are converging or diverging over time as media/culture globalizes.

**Writeup structure note (user, 2026-08-16)**: the backbone diversity finding (item 1) and the
convergence/divergence finding probably belong in the *same* section of the paper when writing —
both are really answering "how are the US and Italy's name distributions related to each other,"
just from different angles (each country's own concentration vs. how similar the two countries are
to each other). Kept as separate figures (fig5 vs fig6) since they're each already clear on their
own, but pair them narratively in the text.

Required exam sections (Metodologie/Dati, Risultati, Discussione Finale, etc.) still have to be
there regardless of this framing — the spike stories are the content, not a replacement for the
paper's structure.

---

## What's been tried

### US data — done, solid
- Downloaded the full SSA "Baby Names from Social Security Card Applications" dataset, 1880–2025
  (`dataset/names/`, one file per year).
- Processed into a long name/year/sex/count table and per-year diversity metrics (Shannon entropy,
  top-10/top-30 concentration share) — `src/scripts/01_process_ssa.py`.
- Ran Mann-Kendall trend tests on those metrics — `src/scripts/02_mann_kendall_us.py`.
- Finding: US name concentration has been falling and entropy rising continuously and significantly
  (p < 0.001) since 1880.

### Italy data — first attempt: manual collection (done, now superseded as the backbone source)
- ISTAT has no bulk name×year×count download on its official Open Data / High Value Datasets page
  (checked directly — confirmed the "fertilità"/"mortalità" entries there are just generic
  demographic-rate indicators, no name-level content, dead end as expected).
- Manually collected top-30 concentration data for 2004, 2006–2024 from 14 downloaded ISTAT PDFs
  plus nomix.it (a secondary site citing ISTAT), spot-checked in 3 places — `dataset/istat/
  istat_annual_top_names.csv`, full detail in `dataset/istat/COLLECTION_NOTES.md`. Kept as a
  corroboration/citation trail, not deleted, even though superseded as the main source (see below).

### Found and scraped a real bulk API behind ISTAT's "contanomi" tool (2026-08-14)
- Read the tool's JS (`birthName.js`) and found it calls an unauthenticated JSONP web service:
  `https://www.istat.it/wp-content/themes/EGPbs5-child/contanomi/nati/index2022.php`. No
  `robots.txt` restrictions.
- The public UI only shows top 10-50, but the `limit` query param isn't hard-capped there — for
  some years it returns the entire distribution (confirmed for 2023: 25,197 male / 24,126 female
  names, ~100% of births, no privacy-suppression floor unlike SSA's ≥5-births threshold).
- Building the scraper (`src/scripts/00_scrape_istat_contanomi.py`) surfaced a real, non-obvious
  server quirk, not a bug in our code: high `limit` values fail unpredictably per year (1999 broke
  above ~377, 2018 already broke at 375, 2021 broke as low as 137) — confirmed via repeated
  identical requests that this is a **stable, deterministic per-year ceiling**, not
  rate-limiting/caching flakiness. Final approach: binary-search each year's actual maximum working
  limit. Final coverage: 66-100% of births per year depending on year (2022-2024 got the full
  distribution; worst year 2021 only reached rank 137) — see `dataset/istat/contanomi_raw/
  manifest.csv`. Decided **2026-08-16 (with user)**: this is the real ceiling, not something more
  retrying fixes; settled here rather than continuing to chase ISTAT's service.
- **Validated thoroughly before trusting it**: cross-checked scraped 2024 top counts (Leonardo 6580,
  Sofia 4636) and a computed top-30 share (42.94%) against the manually-collected data — exact
  match both ways.
- **Quantified the coverage-gap bias empirically** (`01c_check_coverage_bias.py`): used the two
  fully-covered years (2022-2024) as ground truth, artificially truncated them to every other year's
  actual cutoff depth, and measured real bias. Result: **top10/top30 concentration share bias is
  exactly zero at every depth tested** (proven, not assumed) — safe to use across the full
  1999-2024 window. **Shannon entropy bias is severe** (-50% relative at the worst depth, still -19%
  even at the *best* non-complete year) — entropy is only trustworthy for 2022-2024.
- Processed into Italy's own diversity-metrics table (`src/scripts/01b_process_istat_contanomi.py`
  → `dataset/processed/it_diversity_metrics.csv`), with an `entropy_reliable` flag per row so this
  distinction can't be silently lost downstream.
- **Replaced** the manual top-30 comparison as the backbone source in `03_us_italy_comparison.py`
  and the comparison figure `05_plot_us_italy_comparison.py` (now spans 1999-2024, not 2006-2024).
  Current finding: both countries show significant decreasing concentration since 1999 (p<1e-11
  both sexes); Italy's female-name diversification is significantly *faster* than the US's
  (p≈3e-5 on the difference-trend test); male trends are statistically indistinguishable between
  countries.

### Spike-story hunt (2026-08-16)
Built two candidate-finder scripts — `06_find_us_spikes.py` and `07_find_it_spikes.py` — that flag
names with a large year-over-year jump (ratio ≥2.5x/2x over a 3-year median baseline, with a
minimum-count floor to avoid tiny-number noise). These are candidate finders, not verifiers: every
candidate was then checked with a web search before being trusted. Final roster (see below) all
came from this process.

### Convergence/divergence analysis (2026-08-16, reworked once already)
First version (`08_us_italy_name_overlap.py`): checked whether the exact same name appears in both
countries' **top-30** lists per year — a coarse same/different tally on 60 names, blind to anything
outside the elite tier. Found significant convergence for female names only (male trend not
detectable at that resolution).

**Reworked per user's request** to use "the complete dataset" rather than just the top tier
(`08b_us_italy_distribution_similarity.py`): cosine similarity between the two countries' full
name-frequency distributions per year/sex (every captured name, weighted by its real birth share).
Naturally robust to Italy's coverage gaps for the same reason the concentration-ratio metric is
(dominated by high-frequency names, which every year's scrape reaches regardless of its depth
ceiling). Result: **significant convergence for both sexes**, and much stronger than the top-30
version suggested — male cosine similarity 0.066→0.176 (1999→2024, p=2.4e-12, tau=0.98), female
0.119→0.302 (p=2.8e-11). Concrete example: Liam and Noah both newly entered Italy's top-30 by 2024,
absent in 1999.

---

## Spike story roster (final selection, 2026-08-16)

**US (8):**
| Name | Year | Jump | Cause |
|---|---|---|---|
| Shirley | 1935 | mass rise | Shirley Temple's child stardom |
| Tammy | 1958 | 255→9,987 (39x) | "Tammy and the Bachelor" (1957), #1 hit song |
| Nakia | 1974 | 7→1,135 (162x) | ABC series *Nakia* (1974) — tightest timing of the set, flagged as lower-confidence |
| Jaime | 1976 | 259→7,838 (30x) | *The Bionic Woman* debut (Jan 1976) |
| Devante | 1992 | 12→1,565 (130x) | Jodeci's DeVanté Swing, *Forever My Lady* (1991) |
| Mariah | 1991 | 423→5,192 (12x) | Mariah Carey's debut album (1990) |
| Nevaeh | 2001 | 8→1,199 (150x) | Sonny Sandoval (P.O.D.) naming his daughter on MTV, 2000 |
| Jaslene | 2008 | 6→872 (145x) | *America's Next Top Model* Cycle 8 winner (aired Feb-May 2007) |

Cut (user call, 2026-08-16): Aaliyah, Bentley — both were solid, cut for roster length/focus, not
weak evidence (Bentley in particular had an independently-reported figure, 3,768 babies in 2010,
that matched our detected number almost exactly).

**Italy (5):**
| Name | Year | Jump | Cause |
|---|---|---|---|
| Karol | 2005 | 2→156 (78x) | Death of Pope John Paul II (Karol Wojtyła), 2 April 2005 |
| Chanel | 2007-08 | single digits→158, then a **decade-long plateau at 150-220/year** | Chanel Totti born 13 May 2007 (daughter of AS Roma captain Francesco Totti and Ilary Blasi). Confirmed by checking the *full* year-by-year trajectory, not just the flagged spike year: the jump starts in 2007 itself (her birth year), a full year before the initial theory (a 2008 Coco Chanel TV miniseries) even aired, and the sustained decade-long plateau afterward is the signature of a "celebrity legitimizes a name" effect, not a broadcast blip. **Framed as a combined cause** per user's note: the Chanel *brand* itself (elegant, French, fashion-coded) is plausibly a background enabling factor too, not celebrity-baby alone. |
| Adele | 2012-13 | +2-2.4x | *21* dominates Italian charts — only hit #1 in Italy Oct 2011, was the best-selling album of *both* 2011 and 2012, so Italy's adoption genuinely lagged the US's, matching the delayed birth-year spike |
| Elodie | 2017 | 13→135 (10x) | Elodie Di Patrizi's Sanremo breakthrough with "Tutta colpa mia," Feb 2017 |
| Soleil | 2022-23 | up to 4.8x | Soleil Sorge's *Grande Fratello Vip* fame (2021 season) — timing fits a ~9-12 month conception-to-birth lag from peak exposure |

Cut (user call, 2026-08-16): Francesco Pio (Padre Pio's canonization, June 2002) — solid finding
(verified), cut for roster length, not weak evidence.

**Common/shared stories** (the cross-country angle specifically wanted):
- **Celine Dion**: gradual US rise (614→1,466, 2018-2025) accelerating after her Dec 2022 diagnosis
  reveal and June 2024 documentary; the same two events caused a much sharper jump in Italy (up to
  6x) — same cause, very different magnitude. Good comparative material.
- **Elsa/Frozen**: real in both countries, but delayed ~1 year in Italy (film released there Dec
  2013) and far smaller in absolute terms (flat ~52-56 in Italy through 2013, jumps to 130 by 2015).
- **Khaleesi/Game of Thrones**: US-only — never appears in Italy's captured data at all.
- **Isabella/Twilight**: rises in both countries, but in Italy the rise predates Twilight (already
  climbing 2004-2007) and continues smoothly through it — Isabella is already a classic Italian
  name, so this is likely two different underlying causes producing a similar-looking curve, not
  one shared cause. Useful as a contrast case, not a clean "common story."

---

## Negative-spike ("anti-spike") roster (2026-08-16, trimmed same day)

Mirror of the positive-spike hunt: `14_find_us_declines.py` (US) / `16_find_it_declines.py` (Italy)
flag names with a sudden large **collapse** instead of a jump (ratio ≤0.5 vs. 3-year median
baseline), requiring a substantial pre-collapse baseline (≥300 US / ≥100 Italy) so we're catching
real established names cratering, not noise. Working hypothesis: a negative event (scandal,
controversy, a public figure becoming disliked) can "burn" a name the same way a positive event
launches one.

Initial US hunt found 5 verified cases; **user trimmed to 3** (Hillary, Kobe, Alexa) for focus,
cutting Woodrow (Wilson's 1919 stroke) and Jase (Duck Dynasty cancellation) — both solid, not weak
evidence. Italy hunt found one strong case (Erica) plus one weaker "echo" candidate (Enrica) that
**user cut** — the decline continued linearly well past the supposed trigger year, more consistent
with an already-underway long-term fade than a clean single-event story, so honest to drop it rather
than force a second data point. Final table: `docs/paper/tables/table16_negative_spikes.csv`.

| Country | Name | Year | Drop | Cause |
|---|---|---|---|---|
| US | Hillary/Hilary | 1993 | 58% drop 1992→1993, one of the most documented name-collapses in the literature | Hillary Clinton becomes First Lady, immediately polarizing (healthcare reform fight, 69% favorable among women vs. 51% among men from day one) |
| US | Kobe | 2004 | ratio 0.37-0.45 | Kobe Bryant's 2003 sexual assault charges (case dismissed Sept 2004, but reputational damage already done) |
| US | Alexa | 2020-21 | ratio ~0.35-0.42, part of a longer decline starting 2015 | The well-documented "Alexa effect" — Amazon Echo (2014-15) made the name synonymous with a voice-assistant/servant, parents actively avoiding it, kids reportedly bullied |
| Italy | Erica | 2001-02 | 863(1999)→416(2002), nearly halved | *Delitto di Novi Ligure* — Erika De Nardo, 16, murders her mother and brother with her boyfriend, Feb 2001, one of the most notorious Italian crime cases of the era; timing matches exactly (decline starts the murder year, deepens through the Dec 2001 trial and May 2002 appeal) |

**Data-quality catch worth keeping**: the Italy decline hunt initially flagged "Nicolò" and "Desirè"
as huge collapses (ratio as low as 0.02) — checked before trusting, and both turned out to be pure
ISTAT recording-convention artifacts (e.g. `NICOLO` counts collapse in 2011 exactly as `NICOLO'`
appears with almost the offsetting count the same year — the underlying name barely changed, ISTAT
just changed how it records the accent). Excluded, not reported as real declines.

## Geographic robustness check (2026-08-16, updated same day)

For the strongest cases in both rosters (positive and negative), checked whether the national jump/
collapse was geographically uniform or concentrated in a few states, using SSA's state-level data
(`dataset/namesbystate/`, bonus data from Person B's repo we hadn't used before) —
`15_state_concentration_analysis.py` → Table 15, `fig8_state_concentration.png` (new figure,
horizontal bar chart, sorted, color-coded positive/negative). Logic: a genuine national media event
should move most states together; a "spike" driven almost entirely by one or two states would be a
red flag for a regional cause or data artifact instead. US-only (no Italian regional data available,
so Erica isn't in this check). After trimming the negative roster to 3, **8 of 9 cases show >90% of
states moving the same direction** as the national effect (e.g. Jaime 100%, Kobe 97%, Alexa 97%). The
one notable exception, Jaslene (79%), is plausibly explained by an initially Hispanic-population-
skewed adoption pattern (she was ANTM's first Hispanic winner) rather than uniform national spread —
an interesting detail, not a weakness in the method. Not a formal hypothesis test (no real null to
reject), but a
genuine plausibility check now written up as such in the methodology draft.

---

## Exhaustive spike table (2026-08-16)

Alongside the 13 hand-curated, cause-verified stories above, `10_exhaustive_spike_table.py` builds
a *mechanically* filtered supplementary table — every name/year crossing a fixed growth threshold,
no hand-picking. Output: `dataset/processed/exhaustive_spike_table.csv`.

Thresholds (tuned by checking how many rows different cutoffs produce — see conversation; **easy to
retune**, both are just constants at the top of the script): US ratio≥6.0x AND count≥2000 (48 rows);
Italy ratio≥2.5x AND count≥150 (39 rows). **87 rows total.** Point of this table for the paper: shows
the 13 curated stories aren't cherry-picked exceptions, there's a broader mechanical base underneath.

## Figures built so far
- `fig2_us_entropy_1880_2025.png` — US Shannon entropy, full history (non-comparative depth figure).
- `fig3_istat_coverage.png` — new 2026-08-16, ISTAT scrape completeness per year (from
  `manifest.csv`) — the visual companion to the coverage-bias numeric proof.
- `fig4_coverage_bias_check.png` — new 2026-08-16, dual-axis: Shannon entropy bias (grows sharply as
  coverage depth shrinks) vs top-30 share bias (flat at zero regardless of depth) — makes the case
  for why entropy is restricted to 2022-2024 but concentration ratio isn't.
- `fig5_us_italy_top30_comparison.png` — core backbone figure, US vs Italy top-30 concentration
  share. Updated 2026-08-16 to use the full contanomi data and the full 1999-2024 window (was
  2006-2024 on the old manual data).
- `fig6_us_italy_convergence.png` — new 2026-08-16, two-panel: cosine similarity (top) and top-100
  overlap count (bottom), both by sex, 1999-2024.
- `fig7_spike_roster.png` — new 2026-08-16, all 13 curated spike stories on one figure (US top,
  Italy bottom), each indexed to its own pre-event level and plotted on "years relative to the
  event" so wildly different scales (Tammy ~10,000 vs Chanel ~150) are comparable. Log-scale y-axis
  — first linear-scale attempt was unreadable, a few near-zero baselines (Nevaeh, Karol) blew their
  index up into the tens of thousands and flattened every other line.
- Not yet built: individual before/after mini-figures for the single strongest 2-3 stories, if the
  writeup ends up wanting them — optional, the roster figure may already cover this need.

7 figures + 1 exhaustive table now exist, comfortably past the ≥10 figures/tables exam requirement
once the existing statistical-results tables (Mann-Kendall, US/Italy comparison) are counted too.

---

## Repo merge with Person B (2026-08-16)

Person B set up his own repo (`matteraggi/HDS_evolution_of_naming`) independently, with raw SSA data
(national + a state-level breakdown we hadn't used) and empty scaffold files, no analysis code yet.
Merged cleanly (`git merge --allow-unrelated-histories`, zero conflicts), then reorganized: dropped
our redundant gitignored SSA copy in favor of his already-committed one (verified byte-identical via
md5sum first), moved all our data under his `dataset/` convention, updated every script's paths
accordingly, smoke-tested the full pipeline end to end. Origin now points to his repo; our old repo
(`fri3erg/names-project`) is untouched but no longer used. His state-level bonus data
(`dataset/namesbystate/`) turned out genuinely useful — it's what powers the new geographic
robustness check above.

## Null-hypothesis rewrite (2026-08-16)

Professor specifically wants explicit H₀/p-value/significance treatment. Rewrote §4 of the
methodology draft to separate two categories clearly: formal hypothesis tests (Mann-Kendall,
Wilcoxon — each now states H₀/H₁/α=0.05 explicitly) vs. robustness/sensitivity checks (coverage-bias
truncation test, geographic concentration check) that don't have a real null to reject and are now
labeled as such rather than blurred together with the formal tests. Also flagged explicitly that the
bootstrap slope-CI comparison is an informal heuristic, not a rigorous two-sample test — the actual
formal test for "does the US/Italy gap change over time" is the Mann-Kendall on the difference series.

---

## What we want to achieve next

- [ ] **Write the paper.** Italian, ≥5000 words, ≥10 figures/tables, required exam sections
      (Metodologie/Dati, Risultati, Discussione Finale). Content is now fully assembled: backbone
      diversity comparison, spike-story roster (13 positive + 4 negative curated + 87-row exhaustive
      table + 4 common/shared cases), convergence analysis, geographic robustness check, 8 figures,
      5 result tables. This is the only remaining task, along with RQ3 (still untouched, see
      `HANDOFF_TO_PERSON_B.md`).
- [x] **Update README / methodology draft** to match the final data source and spike-led framing —
      done 2026-08-16.

---

## Decisions made so far (dated, so we don't relitigate them)

- **2026-08-14** — Replace the manual top-30 Italy comparison with the full contanomi scrape as the
  backbone source. Confirmed safe: every scraped year is a strict superset of what the manual
  comparison used, and cross-checked numbers match exactly.
- **2026-08-14** — Concentration ratio (top10/top30 share) is the primary Italy metric across the
  full 1999–2024 window; full Shannon entropy only valid for 2022–2024 — proven via
  `01c_check_coverage_bias.py`, not assumed.
- **2026-08-14** — Settled on the scraped per-year coverage as final (66–100%, see `manifest.csv`)
  rather than continuing to chase more from ISTAT's contanomi service — confirmed the per-year
  ceiling is a hard, stable limit.
- **2026-08-16** — Reframed the paper: spike stories are the main draw, not a side note next to the
  diversity-trend backbone.
- **2026-08-16** — Final spike roster locked in (8 US, 5 Italy, 4 common/shared cases).
- **2026-08-16** — Chanel's cause revised from "2008 TV miniseries" to "Chanel Totti born May 2007,"
  after checking the full count trajectory rather than just the flagged year — framed as a combined
  cause (celebrity baby + brand cachet) per user's note.
- **2026-08-16** — Convergence metric reworked from top-30-only overlap to full-distribution cosine
  similarity, per user's request to use "the complete dataset" — now the paper's convergence
  backbone; top-30/top-100 overlap kept as a simpler complementary number.
- Still open: reaching out to ISTAT's contact center for possibly better/official data (user doing
  this independently) — treated as a possible future upgrade, not something the paper depends on.
- **2026-08-16** — Merged with Person B's repo, adopted his `dataset/` convention and committed SSA
  files project-wide, origin now points to `matteraggi/HDS_evolution_of_naming`.
- **2026-08-16** — Added a negative-spike ("anti-spike") roster (5 verified US cases) and a
  geographic robustness check (state-level data) alongside the positive-spike roster, per user's
  request to study the "opposite of peaks" and to add a keep-it-to-strong-cases-only state analysis.
- **2026-08-16** — Metodologie §4 rewritten to explicitly separate formal hypothesis tests (H₀/H₁/α
  stated per test) from robustness/sensitivity checks, per the professor's specific emphasis on
  null-hypothesis/p-value rigor.
