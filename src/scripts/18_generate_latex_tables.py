r"""
Generate LaTeX table snippets from the paper's CSV tables, so numbers in the
.tex document are pulled directly from the data rather than hand-transcribed
(same reasoning as everywhere else in this project: avoid manual transcription
errors on numbers that already exist in a clean source file).

Output: docs/paper/tables_tex/tableN.tex, one \begin{table*}...\end{table*}
(or \begin{table} for narrower ones) per input CSV, ready for \input{}.

2026-08-17: reworked after real Overleaf compile warnings came back
(table14/table15 overflowing the page width, table13/table16 producing
underfull-hbox warnings inside p{} columns). Fixes:
  - table14: was single-column (wide=False), too narrow for 5 numeric
    columns at any reasonable font -> now table* (full width).
  - table15: was dumping raw snake_case CSV headers verbatim as column
    headers (e.g. "percento\_stati\_concordanti") across 12 columns - the
    headers alone blew the width budget. Now uses a `columns` allowlist to
    pick a short display header per column and drops two columns that were
    redundant with others already shown (raw concordant-state count,
    duplicate of the percentage already shown; median ratio, secondary
    to the top/bottom range already shown).
  - p{} columns now default to ragged-right instead of fully justified -
    justification inside a narrow column is what was producing the
    underfull-hbox warnings on long unbroken Italian sentences.
"""

import csv
import os

TABLES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "paper", "tables_tex")
os.makedirs(OUT_DIR, exist_ok=True)


def esc(s: str) -> str:
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"), ("$", r"\$"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}")]:
        s = s.replace(a, b)
    return s


def P(width: str) -> str:
    """Ragged-right paragraph column of the given width (e.g. '3cm') - avoids the
    underfull-hbox warnings that plain p{} (fully justified) produces on narrow columns."""
    return f">{{\\raggedright\\arraybackslash}}p{{{width}}}"


def write_table(csv_name, tex_name, caption, label, colspec, wide=True, fontsize="\\footnotesize",
                 columns=None):
    """
    columns: optional list of (csv_field_name, display_header) to select, rename, and
    reorder columns from the source CSV. If omitted, uses every CSV column verbatim
    (fine for CSVs whose headers are already short/human-readable).
    """
    path = os.path.join(TABLES_DIR, csv_name)
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if columns:
        field_order = [c for c, _ in columns]
        display_headers = [h for _, h in columns]
    else:
        field_order = list(rows[0].keys()) if rows else []
        display_headers = field_order

    ncols = len(field_order)
    env = "table*" if wide else "table"
    lines = []
    lines.append(f"\\begin{{{env}}}[t]")
    lines.append("\\centering")
    lines.append(fontsize)
    lines.append(f"\\caption{{{esc(caption)}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append(f"\\begin{{tabular}}{{{colspec}}}")
    lines.append("\\toprule")
    lines.append(" & ".join(f"\\textbf{{{esc(h)}}}" for h in display_headers) + " \\\\")
    lines.append("\\midrule")
    for r in rows:
        cells = [r.get(f, "") for f in field_order]
        lines.append(" & ".join(esc(c) for c in cells) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append(f"\\end{{{env}}}")

    out_path = os.path.join(OUT_DIR, tex_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path} ({len(rows)} rows x {ncols} cols)")


def main():
    write_table(
        "table1_dataset_overview.csv", "table1.tex",
        "Confronto delle fonti dati USA (SSA) e Italia (ISTAT contanomi)",
        "tab:dataset_overview", wide=True, fontsize="\\scriptsize",
        colspec=f"{P('3.2cm')} {P('6.3cm')} {P('6.3cm')}",
    )
    write_table(
        "table14_coverage_bias_check.csv", "table14.tex",
        "Distorsione delle metriche in funzione della profondità di copertura (troncamento artificiale dei dati 2023/2024)",
        "tab:coverage_bias", wide=True, fontsize="\\footnotesize",
        colspec="r r r r r r",
        columns=[
            ("profondita_copertura", "Profondità (nomi)"),
            ("bias_quota_primi10", "Bias top-10 (p.p.)"),
            ("bias_quota_primi50", "Bias top-50 (p.p.)"),
            ("bias_quota_primi100", "Bias top-100 (p.p.)"),
            ("bias_entropia_bit", "Bias entropia (bit)"),
            ("bias_entropia_percento", "Bias entropia (%)"),
        ],
    )
    write_table(
        "table15_state_concentration.csv", "table15.tex",
        "Uniformità geografica dei casi-studio RQ2 (dati per stato, solo USA; \"stato top\"/\"stato min\" = quello con il rapporto più alto/più basso vs. baseline)",
        "tab:state_concentration", wide=True, fontsize="\\scriptsize",
        colspec="l c c c r r c r c r",
        columns=[
            ("nome", "Nome"),
            ("sesso", "Sesso"),
            ("anno_evento", "Anno"),
            ("tipo", "Tipo"),
            ("stati_con_dati", "N stati"),
            ("percento_stati_concordanti", "% concordi"),
            ("stato_top", "Top"),
            ("rapporto_stato_top", "Rapp. top"),
            ("stato_minimo", "Min"),
            ("rapporto_stato_minimo", "Rapp. min"),
        ],
    )
    write_table(
        "table16_negative_spikes.csv", "table16.tex",
        "Roster finale dei crolli onomastici verificati (\"anti-spike\")",
        "tab:negative_spikes", wide=True, fontsize="\\footnotesize",
        colspec=f"l {P('2cm')} c {P('3cm')} {P('6cm')} c",
    )
    write_table(
        "table20_positive_spikes.csv", "table20.tex",
        "Roster finale delle tredici storie di salto onomastico verificate",
        "tab:positive_spikes", wide=True, fontsize="\\footnotesize",
        colspec=f"l {P('2cm')} c {P('3cm')} {P('6cm')} c",
    )
    write_table(
        "table17_formal_hypotheses.csv", "table17.tex",
        "Sintesi delle ipotesi statistiche formali per RQ1 (dettagli di H0/H1 nel testo)",
        "tab:formal_hypotheses", wide=True, fontsize="\\footnotesize",
        colspec=f"{P('5cm')} {P('4.5cm')} {P('3.5cm')} c",
    )
    write_table(
        "table18_event_study_summary.csv", "table18.tex",
        "Sintesi dell'Event Study quantitativo confermativo (RQ2): Impatto netto DiD per categoria mediatica",
        "tab:event_study_summary", wide=True, fontsize="\\footnotesize",
        colspec=f"{P('4cm')} c c c c c c",
    )
    write_table(
        "table19_gender_neutral.csv", "table19.tex",
        "Nomi Gender-Neutral / Unissex, USA vs Italia, 1999-2024 (RQ3)",
        "tab:gender_neutral", wide=True, fontsize="\\footnotesize",
        colspec=f"{P('2.3cm')} c c c c c {P('2.2cm')}",
    )





if __name__ == "__main__":
    main()
