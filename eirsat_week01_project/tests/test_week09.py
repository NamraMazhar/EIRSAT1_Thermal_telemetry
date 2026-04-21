from pathlib import Path
import pandas as pd


def test_stress_results_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week09_stress_results.csv").exists()


def test_main_table_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week09_main_results_table.csv").exists()


def test_four_methods_present():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week09_main_results_table.csv")
    assert df["method"].nunique() >= 4


def test_stress_dimensions_present():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week09_main_results_table.csv")
    assert df["stress_dimension"].nunique() >= 3


def test_tradeoff_plots_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week09_eventf1_vs_fab.png").exists()
    assert (root / "data" / "runs" / "week09_mdd_vs_fab.png").exists()