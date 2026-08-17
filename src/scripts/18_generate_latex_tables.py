"""
Generate LaTeX table snippets from the paper's CSV tables, so numbers in the
.tex document are pulled directly from the data rather than hand-transcribed
(same reasoning as everywhere else in this project: avoid manual transcription
errors on numbers that already exist in a clean source file).

Output: docs/paper/tables_tex/tableN.tex, one \begin{table*}...\end{table*}
(or \begin{table} for narrower ones) per input CSV, ready for \input{}.
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


def write_table(csv_name, tex_name, caption, label, wide=True, fontsize="\\footnotesize", colspec=None):
    path = os.path.join(TABLES_DIR, csv_name)
    with open(path, encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[1:]
    ncols = len(header)
    if colspec is None:
        colspec = "l" * ncols

    env = "table*" if wide else "table"
    lines = []
    lines.append(f"\\begin{{{env}}}[t]")
    lines.append("\\centering")
    lines.append(fontsize)
    lines.append(f"\\caption{{{esc(caption)}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append(f"\\begin{{tabular}}{{{colspec}}}")
    lines.append("\\toprule")
    lines.append(" & ".join(f"\\textbf{{{esc(h)}}}" for h in header) + " \\\\")
    lines.append("\\midrule")
    for r in body:
        r = r + [""] * (ncols - len(r))  # pad short rows
        lines.append(" & ".join(esc(c) for c in r[:ncols]) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append(f"\\end{{{env}}}")

    out_path = os.path.join(OUT_DIR, tex_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote {out_path} ({len(body)} rows x {ncols} cols)")


def main():
    write_table(
        "table1_dataset_overview.csv", "table1.tex",
        "Confronto delle fonti dati USA (SSA) e Italia (ISTAT contanomi)",
        "tab:dataset_overview", wide=True, fontsize="\\scriptsize",
        colspec="p{3.2cm} p{6.3cm} p{6.3cm}",
    )
    write_table(
        "table13_istat_vs_ssa_structure.csv", "table13.tex",
        "Confronto strutturale tra il formato dati SSA e quello ISTAT",
        "tab:istat_vs_ssa", wide=True, fontsize="\\scriptsize",
        colspec="p{3.2cm} p{6.3cm} p{6.3cm}",
    )
    write_table(
        "table14_coverage_bias_check.csv", "table14.tex",
        "Distorsione delle metriche in funzione della profondità di copertura (troncamento artificiale dei dati 2023/2024)",
        "tab:coverage_bias", wide=False, fontsize="\\footnotesize",
        colspec="r r r r r",
    )
    write_table(
        "table15_state_concentration.csv", "table15.tex",
        "Uniformità geografica dei casi-studio RQ2 (dati per stato, solo USA)",
        "tab:state_concentration", wide=True, fontsize="\\scriptsize",
        colspec="l c c c c r c r c r c r",
    )
    write_table(
        "table16_negative_spikes.csv", "table16.tex",
        "Roster finale dei crolli onomastici verificati (\"anti-spike\")",
        "tab:negative_spikes", wide=True, fontsize="\\footnotesize",
        colspec="l p{2cm} c p{3cm} p{6cm} c",
    )


if __name__ == "__main__":
    main()
