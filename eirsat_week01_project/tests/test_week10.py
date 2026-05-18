from pathlib import Path


def test_figures_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "paper_fig_tradeoff.png").exists()
    assert (root / "docs" / "paper_fig_faulttype_sweep.png").exists()
    assert (root / "docs" / "paper_fig_sensitivity.png").exists()


def test_tables_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "paper_table_main_results.csv").exists()
    assert (root / "docs" / "paper_table_ablation_summary.csv").exists()
    assert (root / "docs" / "paper_table_robustness_summary.csv").exists()


def test_runbook_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "RUNBOOK.md").exists()


def test_repro_manifest_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "repro_manifest.csv").exists()