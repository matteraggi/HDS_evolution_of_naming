# Handoff to Person B (2026-08-16)

Short version of what changed and what's left. Full detail in `PROJECT_LOG.md` (dated log),
`README.md` (repro steps + outputs), `docs/paper/metodologie_dati_DRAFT.md` (methodology writeup).

## What changed from the original plan

The plan (§4) assumed ISTAT had no bulk name data and budgeted manual PDF collection as real,
unavoidable work. That held briefly (see `data/raw/istat/COLLECTION_NOTES.md`), but a real bulk
data service was then found hidden behind ISTAT's own "contanomi" tool (undocumented, found by
reading the tool's JavaScript). After resolving several real server-side quirks, it now backs the
Italy dataset for the full 1999-2024 window (not just 2006-2024), from a primary source (not
nomix.it), with the coverage-completeness caveat empirically proven not to bias the paper's main
metric. Practical effect: the plan's single biggest flagged risk — "§10.1, do first: RQ2 Italy is an
open task, no candidate spike confirmed yet" — is resolved. The paper's focus also shifted: spike
stories (movies/shows/celebrities causing a name to jump) are now the main draw, not a side note next
to the diversity-trend backbone, with a new convergence/divergence angle added (are US and Italy
naming pools becoming more alike over time — yes, significantly, for both sexes).

## What's done (Person A's scope, and most of Person B's)

- Full US SSA data (1880-2025) and full Italy contanomi data (1999-2024), both validated.
- Backbone diversity comparison, 1999-2024, statistically significant both sexes.
- Convergence/divergence analysis (cosine similarity, full distribution).
- **8 US + 5 Italy cause-verified spike stories**, plus 4 cross-country common/shared cases — see the
  roster in `PROJECT_LOG.md`. This was your §10.1 task ("test contanomi against 3-5 candidate
  Italian name/event pairs") — done, exceeded (5 solid Italy stories + a mechanically-generated
  87-row supplementary table beyond the curated ones).
- 7 figures, 3 result tables, all in `docs/paper/figures/` and `docs/paper/tables/`.

## What's NOT done — needs you

1. **RQ3 (gender-neutral name tracking) — completely untouched.** No code, no data, nothing. This
   was in your original scope and still needs to happen for both countries.
2. **The actual paper prose.** Risultati is your section per the original split; Introduzione,
   Discussione Finale, and Abstract are joint. All the data/figures/stats exist as inputs — nothing
   has been written up as paper text yet.
3. (Optional) Individual before/after mini-figures for the 2-3 strongest spike stories, if the
   consolidated roster figure (fig7) doesn't cover what the writeup needs.

## What we expect

Read `PROJECT_LOG.md` top to bottom for the full story (it's written plainly, not just for me).
Start with RQ3 since it's the one gap nothing else depends on you clearing first. Ping back before
changing any of the locked-in decisions in the log (data source, spike roster, thresholds) rather
than redoing work already validated — most of them have real reasoning behind them, not just
convenience.
