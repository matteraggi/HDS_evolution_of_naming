# Project Log

A plain-language running log of this project: what we're trying to do, what's been tried, and what's
still open. For the full academic plan (research questions, methodology, citations, course
requirements) see the original plan doc; for repro steps see `README.md`. This file is the quick
"where are we, what's next" reference.

---

## Main objective

Course paper for "Human Data Science" (exam paper, written in Italian, ≥5000 words, ≥10 figures/tables,
sent to the professor by email, at least a week before the exam).

**Topic**: how baby-name diversity and naming trends have evolved over time in the US and Italy —
comparing the two countries, and looking at whether specific cultural events / famous people /
media moments produce measurable spikes in specific names.

Three research angles:
1. **Diversity over time** — is name diversity increasing? (fewer parents picking the same handful
   of names)
2. **Event-driven spikes** — do movies, TV shows, celebrities produce visible jumps in a name's
   popularity?
3. **Gender-neutral naming** — is the use of unisex names increasing?

**Current framing direction (updated 2026-08-14)**: if the contanomi scrape gives Italy a dataset
that's genuinely comparable in depth to the US SSA data (not just top-30), the paper goes **50/50
US/Italy** rather than US-led-with-Italy-as-garnish — a general "here's what studying this data
shows us" paper, not a US case study with an Italy footnote. The required exam sections
(Metodologie/Dati, Risultati, Discussione Finale, etc.) still have to be there, but the paper needs
one overarching theme tying the findings together rather than reading as three disconnected RQs.
Candidate theme (from the original plan's Fattore Umano framing, §7): naming as an intimate
individual choice that's nonetheless systematically shaped by external forces (media, celebrity,
generational values, institutional data transparency) — still needs to be picked/refined once we
see what the full data actually shows. Event-driven spike-hunting (US finds → check if Italy shows
the same pattern) stays as a component, not necessarily the spine.

---

## What's been tried

### US data — done, solid
- Downloaded the full SSA "Baby Names from Social Security Card Applications" dataset, 1880–2025
  (`data/raw/ssa/`, one file per year).
- Processed into a long name/year/sex/count table and per-year diversity metrics (Shannon entropy,
  top-10/top-30 concentration share) — `src/scripts/01_process_ssa.py`.
- Ran Mann-Kendall trend tests on those metrics — `src/scripts/02_mann_kendall_us.py`.
- Finding: US name concentration has been falling and entropy rising continuously and significantly
  (p < 0.001) since 1880.
- A few event-driven spikes are already validated as real and citable: **Elsa** (Frozen, 2013),
  **Khaleesi** (Game of Thrones), **Isabella** (Twilight) — see the plan doc §12 for the exact numbers.

### Italy data — first attempt: manual collection (done, but now partly superseded)
- ISTAT has no bulk name×year×count download. Only (a) a single-name lookup tool ("contanomi") and
  (b) annual PDF press releases with top-30/top-5 name tables.
- Manually collected top-30 concentration data for 2004, 2006–2024 from 14 downloaded ISTAT PDFs
  plus nomix.it (a secondary site citing ISTAT), spot-checked in 3 places — `data/raw/istat/
  istat_annual_top_names.csv`, full detail in `data/raw/istat/COLLECTION_NOTES.md`.
- Limitation this left us with: comparable window narrowed to **2006–2024** (not the full
  1999–2025 hoped for), and 15 of 19 years relied on a secondary source, not a primary PDF.
- Ran the US/Italy statistical comparison on this data anyway (Wilcoxon, bootstrap slope CIs) —
  `src/scripts/03_us_italy_comparison.py`. Finding: Italy is systematically more concentrated than
  the US every year 2006–2024; female-name diversification is faster in Italy, male is statistically
  tied.

### Checked ISTAT's "High Value Datasets" page — no names data there
- User found a mortality-rate XML file when trying to get ISTAT name data; investigated why.
- Confirmed: ISTAT's official High Value Dataset list (27 entries) has no baby-names dataset. The
  "fertilità" and "mortalità" entries are both just slices of one generic demographic-indicators
  dataset (birth rate, death rate, TFR, life expectancy, migration, age structure by region) — no
  name-level content either way. Dead end, as expected.

### Found a real bulk API behind the "contanomi" tool (big find, 2026-08-14)
- Read the tool's JS (`birthName.js`) and found it calls an unauthenticated JSONP web service:
  `https://www.istat.it/wp-content/themes/EGPbs5-child/contanomi/nati/index2022.php`
- The UI only shows top 10-50, but the API's `limit` parameter isn't actually capped there. Tested
  `limit=99999` for 2023: returned the **entire** distribution — 25,197 distinct male names, 24,126
  distinct female names, percentages summing to ~100%, no privacy-suppression floor (unlike SSA's
  ≥5-births threshold).
- This means we can get an SSA-equivalent full name×year×gender×count table for Italy, 1999–2024,
  directly from the primary source — no more relying on PDFs/nomix.it for the backbone numbers.
- Checked `robots.txt` — no restrictions.
- Built a scraper (`src/scripts/00_scrape_istat_contanomi.py`). Went through a few rounds of
  debugging real quirks in ISTAT's service, not our code:
  1. JSONP wrapper name differs between query types (`callback` vs `callbackY`) — fixed the parser
     to match any wrapper name.
  2. High `limit` values (e.g. 99999) don't fail *consistently* — they work for some years (full
     distribution) and return an empty response for others, and **the breaking point isn't a fixed
     number**: 1999 broke above limit≈377, but 2018 already broke at 375. Confirmed via direct
     testing this isn't transient/rate-limiting (repeated identical requests give identical
     results) — it's a real per-year server-side quirk, most likely triggered when the requested
     range exceeds that year's actual record count.
  3. Fix: scraper now probes a descending ladder of limits per year (99999, 20000, ... down to 10)
     and keeps the largest one that actually returns data, recording what it got in
     `data/raw/istat/contanomi_raw/manifest.csv` (so we can see, per year, whether we captured the
     full distribution or only a top-N slice).
- Currently re-running with the adaptive version across all 26 years (1999–2024).

---

## What we want to achieve next

- [ ] **Finish the full Italy scrape** (`data/raw/istat/istat_contanomi_full.csv`, 1999–2024) —
      running now with the adaptive (per-year ladder) version.
- [ ] **Check coverage against `manifest.csv`** — confirm which years got the full distribution vs.
      a top-N slice, and specifically confirm the scrape covers every name/year the manual
      `istat_annual_top_names.csv` comparison used (2004, 2006–2024, top-30/top-5). **Decided
      2026-08-14**: if coverage checks out, the scraped data replaces the manual comparison as the
      backbone source (keep the manual CSV + `COLLECTION_NOTES.md` as a corroboration/citation
      trail, not delete it).
- [ ] **Recompute Italy's diversity metrics on the full distribution** — full Shannon entropy
      becomes possible for Italy now (previously only top-N concentration ratio was), and the
      comparable window can extend back to 1999 instead of stopping at 2006.
- [ ] **Decided 2026-08-14: aim for a 50/50 US/Italy paper**, not US-led — contingent on the Italy
      scrape actually being comparable in depth to the US SSA data (see coverage check above).
- [ ] **Pick the overarching theme** tying the RQs together (see candidate in Main Objective above)
      — needed so the paper doesn't read as three disconnected mini-studies.
- [ ] **Mine the US data for "fun" spike candidates** beyond the three already validated (Elsa,
      Khaleesi, Isabella) — look for other pop-culture-linked jumps worth telling as a story, then
      check whether Italy shows analogous spikes using the full dataset.
- [ ] **Research Italian cultural-event/celebrity candidates** (Sanremo moments, TV/telenovela
      characters, footballers' kids, etc.) independently of the US findings too, not just as
      US-driven lookups — now cheap to check since the full dataset covers any name directly.
- [ ] **Update README / methodology draft / project plan** to reflect the new data source and
      50/50 framing once the above settles — intentionally not done yet, to avoid rewriting docs
      before the underlying data situation is finalized.

---

## Open questions for the team

1. ~~Once the full Italy scrape lands, do we fully replace the 2006–2024 manual-data comparison?~~
   **Answered 2026-08-14**: yes, replace it, conditional on the scrape actually covering what the
   manual comparison used — needs a coverage check once the scrape finishes.
2. ~~How much space goes to the "fun US events" narrative vs. the formal diversity/entropy
   backbone?~~ **Answered 2026-08-14**: reframed — not US-narrative-led at all if Italy's data
   turns out comparable; aim for a balanced 50/50 comparative paper with one overarching theme,
   required exam sections still present regardless of framing.
3. **New**: what exactly is the overarching theme? Candidate is the Fattore Umano framing from the
   original plan (naming as intimate-yet-externally-shaped choice) — needs to be confirmed or
   replaced once we see what stands out in the full data.
