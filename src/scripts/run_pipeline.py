"""Regenerate all derived analysis outputs from the versioned raw datasets.

The ISTAT scraper is deliberately excluded: it accesses a live, undocumented
service and can change the versioned source data. Run 00_scrape_istat_contanomi.py
explicitly only when a data refresh is intended.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / "src" / "scripts"

PIPELINE = [
    "01_process_ssa.py",
    "01b_process_istat_contanomi.py",
    "01c_check_coverage_bias.py",
    "01d_check_cosine_bias.py",
    "02_mann_kendall_us.py",
    "03_us_italy_comparison.py",
    "06_find_us_spikes.py",
    "07_find_it_spikes.py",
    "08_us_italy_name_overlap.py",
    "08b_us_italy_distribution_similarity.py",
    "10_exhaustive_spike_table.py",
    "11_plot_it_coverage.py",
    "12_plot_coverage_bias.py",
    "04_plot_us_entropy.py",
    "05_plot_us_italy_comparison.py",
    "09_plot_convergence.py",
    "13_plot_spike_roster.py",
    "14_find_us_declines.py",
    "15_state_concentration_analysis.py",
    "16_find_it_declines.py",
    "17_plot_state_concentration.py",
    "18_generate_latex_tables.py",
]

EXPECTED_OUTPUTS = [
    ROOT / "dataset" / "processed" / "us_names_long.csv",
    ROOT / "dataset" / "processed" / "us_diversity_metrics.csv",
    ROOT / "dataset" / "processed" / "it_diversity_metrics.csv",
    ROOT / "dataset" / "processed" / "us_italy_comparison.csv",
    ROOT / "dataset" / "processed" / "state_concentration_results.csv",
    ROOT / "docs" / "paper" / "figures" / "fig2_us_entropy_1880_2025.png",
    ROOT / "docs" / "paper" / "figures" / "fig8_state_concentration.png",
    ROOT / "docs" / "paper" / "tables_tex" / "table16.tex",
]


def main() -> None:
    env = os.environ.copy()
    matplotlib_cache = ROOT / ".cache" / "matplotlib"
    matplotlib_cache.mkdir(parents=True, exist_ok=True)
    env["MPLCONFIGDIR"] = str(matplotlib_cache)

    for script in PIPELINE:
        print(f"\n>>> {script}", flush=True)
        subprocess.run([sys.executable, str(SCRIPTS_DIR / script)], cwd=ROOT, env=env, check=True)

    missing = [path.relative_to(ROOT) for path in EXPECTED_OUTPUTS if not path.is_file()]
    if missing:
        raise SystemExit(f"Pipeline completed but expected outputs are missing: {missing}")
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
