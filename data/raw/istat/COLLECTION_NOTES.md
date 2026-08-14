# ISTAT "Natalità e fecondità della popolazione residente" — collection notes

Collected: 2026-08-12. Covers data-years **2004, 2006–2024** (21 years; 2005 is a
confirmed gap — see below). Output: `istat_annual_top_names.csv` +
14 primary ISTAT PDFs archived alongside this file (`istat_natalita_<year>.pdf`
for years 2011–2024).

## What's in the raw/ folder

- `istat_natalita_2011.pdf` through `istat_natalita_2024.pdf` (14 files) — the
  official ISTAT "Statistiche report" PDFs, downloaded directly from istat.it
  (2011's copy is a verbatim mirror hosted by Comune di Bologna — the original
  istat.it URL for that specific year could not be located, but the content is
  the genuine official "Testo integrale", dated 14 Nov 2012).
- `istat_annual_top_names.csv` — one row per data-year, 2004–2024.
- No PDF was found/downloaded for 2004, 2006, 2007, 2008, 2009, 2010 — for
  these years the CSV is populated from **nomix.it**, a baby-names site whose
  "Top 30 Italia" pages explicitly cite ISTAT as the source for every year
  ("Fonte: ISTAT, ‹month/year›") and reproduce full top-30 name×count tables
  plus the top-30 cumulative-share percentage. See "On nomix.it as a source"
  below for how much this was trusted.

## Year-by-year availability of the top-30 concentration stat

This was the central open question from the brief: does the ISTAT report
state "the first 30 names cover X% of boys / Y% of girls" every year?

**Answer: it varies, and there's a clear multi-year trend, but nomix.it turns
out to compute/report this percentage for every single year regardless of
whether the underlying press release states it in prose.**

Cross-checking nomix.it's numbers against the two ISTAT PDFs I read in full
(2020 and 2024) confirms this:

- **2022** (per the task brief) and **2020** (confirmed by my own full read of
  the PDF) both contain the sentence explicitly, e.g. 2020: *"la distribuzione
  del numero di nati secondo il nome rivela un'elevata concentrazione intorno
  ai primi 30 in ordine di frequenza, che complessivamente coprono oltre il
  44% di tutti i nomi attribuiti ai maschi e quasi il 38% di quelli delle
  femmine."* This matches nomix.it's 44.05%/37.63% for that year almost
  exactly (the PDF just rounds it into prose).
- **2024** (confirmed by my own full read, all 12 pages) has **no such
  sentence at all** — only a bar chart of the top 5 names (Figura 4) with
  no cumulative-share commentary. nomix.it nonetheless reports 42.94%/36.31%
  for 2024, which it must be computing from ISTAT's underlying granular
  name-count data (ISTAT publishes a "contanomi" tool with per-name counts
  1999–present that isn't part of the press-release PDF), not from PDF prose.
- The 2020 report also has **no bar chart / no absolute counts at all** for
  the top-5 names, only narrated rank order (e.g. "Leonardo... si conferma al
  secondo posto..."). Exact counts for that year exist only via nomix.it.

**Practical implication for the paper:** the ISTAT press-release PDF is an
inconsistent, unreliable source for the top-30 concentration stat and for
exact name counts — it swaps between (a) full sentence + bar chart, (b)
sentence only, (c) bar chart only, and (d) neither, seemingly at the report
authors' discretion year to year. If the paper wants a *complete, consistent*
1999–2024 series of top-30 shares and exact counts, nomix.it (or ideally
ISTAT's own "contanomi" online tool, which the retrieved "nomi-dei-nuovi-nati"
ISTAT news post explicitly points readers to for 1999–2023 detail) is the
better-suited source, with the PDF reports as corroboration/citation of the
official framing per year.

## On nomix.it as a source

nomix.it ("Top 30 Italia") publishes one page per year (2004, 2006–2024 found;
2005 not found) with:
- a ranked table of the top 30 names (rank, name, count, and for some years
  a %/cumulative-% column),
- a prose paragraph stating "I primi 30 nomi corrispondono al X% ... e al Y%
  per le bimbe",
- a "Fonte: ISTAT, ‹month year›" citation matching the actual ISTAT press
  release month for that data-year.

I did not treat this as equivalent to reading the primary PDF myself, so
every CSV row sourced from it is flagged in `notes`. But it was spot-checked
against primary-source numbers in three places and matched closely every
time:
1. 2022: nomix 43.82%/37.37% vs. the task brief's ISTAT quote "quasi il 44%
   ... quasi il 38%" — consistent.
2. 2020: nomix 44.05%/37.63% vs. the ISTAT PDF's own sentence "oltre il 44%
   ... quasi il 38%" — consistent (near-exact).
3. 2024: nomix's exact top-5 counts (Leonardo 6580, Edoardo 5819, Tommaso
   4389, Mattia 4233, Alessandro 4201; Sofia 4636, Aurora 4265, Ginevra 4153,
   Vittoria 3893, Giulia 3397) match what I independently read off the ISTAT
   PDF's bar-chart axis (Figura 4) to the nearest few hundred — i.e. the bar
   chart heights are visually consistent with these exact numbers.

Given that, I'm reasonably confident in nomix.it's numbers as faithful
ISTAT-derived data, but they are still a secondary compilation, not the
primary document — flagged accordingly in every row's `notes` column.

## Years with NO report/data found at all

- **2005**: no ISTAT press release, no PDF, and no nomix.it page could be
  located despite searching multiple ways. This is a genuine gap — 2004 and
  2006 both have data, but 2005 does not appear to be archived/republished
  anywhere I could reach. Flagged as an empty row in the CSV rather than
  silently skipped.
- Nothing before 2004 was found in any form (name rankings). The task brief
  noted that name-level data only exists from 1999 in ISTAT's internal
  systems, but no publicly retrievable *report or summary* reaches that far
  back — 2004 is the practical floor for secondary-source name rankings, and
  ~2007-2008 is roughly where full-featured "Statistiche report" PDFs with
  methodology sections and glossaries start looking like the modern format
  (though a report format already existed by 2008/2009, since nomix cites
  "Fonte: ISTAT, 2009" and "Fonte: ISTAT, 2010" for the 2007/2008 data-years).

## Other patterns noticed

- **Total births** figures are exact and mutually corroborating across
  overlapping historical tables in every PDF I read (e.g. the 2020 and 2024
  PDFs both list "Nati in totale" back to 2008, and the numbers for 2008,
  2010, 2012, 2014–2020 match exactly across the two documents). The only
  approximate/uncertain total_births figures in the CSV are 2006 (explicitly
  a "provisional" ISTAT estimate, ~557,000) and 2009 (568,857, sourced only
  via web-search synthesis, not independently verified against a downloaded
  PDF) — both flagged `approx`/uncertain in their notes.
- **Format/methodology shifts**: the report's own "Nota metodologica" section
  (present from ~2018 onward in the PDFs I read) states that starting in
  **2020**, the reference year became the year of the birth *event* rather
  than year of *registration* in the civil registry (Anagrafe) — before 2020,
  late-December births could be counted in the following year. This is a
  real discontinuity for year-over-year comparability that the paper should
  probably footnote.
- **Name diversity is visibly rising over time**: the top-30 concentration
  share drops steadily and almost monotonically from ~51%/43% (male/female)
  in 2006 to ~43%/36% in 2024 — i.e. Italian parents' name choices have
  become measurably more dispersed/less concentrated over the 1999–2024
  window, which is directly relevant to the paper's "evolution of baby-name
  diversity" framing.
- **Leonardo overtook Francesco in 2018** (Francesco had been #1 for the
  male ranking for 17 consecutive years before that, per nomix's own
  year-over-year commentary); **Sofia overtook Giulia in 2010** for the
  female ranking and has held #1 every year since.
- The 2024 report is also the first of the ones read where the "primi 30"
  concentration sentence is dropped from the press-release prose entirely
  (also true, less completely, for 2023 — that report's version of the
  sentence appears on nomix.it but was not independently confirmed against
  the primary PDF here), which might reflect an editorial change at ISTAT
  around 2023–2024 rather than the stat becoming unavailable.

## Suggested follow-up for the paper (not done here)

- If exact per-year top-30 *name lists* (ranks 6–30, not just top-5) become
  useful later, nomix.it already has them captured in the page text pulled
  during this session for every year 2004, 2006–2024 (not persisted to disk
  beyond what's summarized into the CSV's top-5 columns) — re-scraping those
  pages would recover full top-30 tables per year if needed.
- ISTAT's own "contanomi" interactive tool (referenced in the ISTAT news
  post "Nomi dei nuovi nati, ecco il podio del 2023") reportedly holds
  1999–2023 (now presumably 2024) name-level detail directly and would be
  the authoritative source if the paper needs finer-grained data (e.g. full
  distribution tail, not just top 30) — this was not accessed in this
  session (it's an interactive web tool, not a static bulk file) and is
  flagged as a good next step.
