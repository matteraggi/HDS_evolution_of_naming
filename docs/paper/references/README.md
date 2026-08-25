# Fonti citate: cosa c'è qui e cosa manca

Tutte le fonti effettivamente citate (`\cite{}`) nel paper sono coperte da un PDF, tranne Mann (1945),
Kendall (1975) e Wilcoxon (1945), che sono citazioni di paternità del metodo statistico (come si cita
Fisher per l'ANOVA) e non richiedono di aver letto il testo originale.

## Scaricate qui (open access)

- **`ogihara2025a_popularity_diversity_uk_names.pdf`** — Ogihara (2025), F1000Research, CC-BY,
  completamente open access.
- **`ons2015_pop_culture_baby_names.html`** — pagina ONS (UK), pubblicamente accessibile.
- **`fan2025_name_uniqueness_individualism.pdf`** — Fan, Thouzeau, de Dampierre, Chevallier &
  Baumard (2025), "Name Uniqueness and the Rise of Individualism in the Western Hemisphere
  (1500-2000)", *Current Research in Ecological and Social Psychology*, vol. 9, art. 100235.
  Open access (rivista Elsevier interamente OA); ScienceDirect blocca il download automatico dei
  PDF open access, quindi è stato scaricato a mano: https://doi.org/10.1016/j.cresp.2025.100235

  **Nota importante**: la bibliografia del paper citava questo articolo come di "Y. Ogihara", ma
  l'autore reale è Fan et al. (Ogihara non è tra gli autori). Ho corretto la voce in
  `bozza_paper.tex` e `bozza_paper.md` (verificato incrociando ricerca web + ResearchGate +
  risoluzione del DOI). **Il riferimento non è comunque mai citato nel testo del paper** (`\cite{}`),
  solo in bibliografia — da valutare se aggiungere una citazione in-text o rimuovere la voce.

## Scaricate in `closed_source_references/` (accesso istituzionale, gitignored)

Consultazione personale soltanto: non finiscono mai nel repo pubblico, per rispetto del copyright
degli editori.

- **Lieberson & Bell (1992)**, "Children's First Names", *American Journal of Sociology* —
  `lieberson_bell1992_childrens_first_names.pdf`
- **Twenge, Abebe & Campbell (2010)**, "Fitting In or Standing Out", *Social Psychological and
  Personality Science* — `twenge2010_fitting_in_or_standing_out.pdf`
- **Twenge, Dawson & Campbell (2016)**, "Still Standing Out", *Journal of Applied Social Psychology*
  — `twenge2016_still_standing_out.pdf`. **Anche questo non è mai citato nel testo del paper**
  (`\cite{}`), solo in bibliografia — stesso discorso di Fan et al. sopra.

## Citate solo per attribuzione del metodo (nessun PDF necessario)

- **Mann (1945)**, "Nonparametric Tests Against Trend", *Econometrica* — JSTOR:
  https://www.jstor.org/stable/1907187
- **Kendall (1975)**, *Rank Correlation Methods*, 4th ed., Charles Griffin — libro, nessun PDF
  gratuito esiste.
- **Wilcoxon (1945)**, "Individual Comparisons by Ranking Methods", *Biometrics Bulletin* — JSTOR:
  https://www.jstor.org/stable/10.2307/3001968

Questi tre sono citati solo per dare il nome ai test statistici (Mann-Kendall, Wilcoxon a coppie
appaiate) usati nel paper, non per un'idea o un dato specifico preso dal testo — pratica standard,
non serve averli letti per difendere la citazione.
