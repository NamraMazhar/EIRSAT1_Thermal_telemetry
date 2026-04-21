from pathlib import Path
import pandas as pd


def test_grid_results_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week08_grid_results.csv").exists()


def test_grid_coverage():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week08_grid_results.csv")
    assert df["run_id"].nunique() >= 18


def test_threshold_tuning_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week08_threshold_tuning.csv").exists()


def test_plot_files_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week08_eventf1_vs_magnitude.png").exists()
    assert (root / "data" / "runs" / "week08_mdd_vs_duration.png").exists()
    assert (root / "data" / "runs" / "week08_fab_vs_threshold.png").exists()