from pathlib import Path
import pandas as pd


def test_ablation_results_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week07_ablation_results.csv").exists()


def test_fault_type_coverage():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "runs" / "week07_ablation_results.csv")
    assert df["fault_type"].nunique() >= 5


def test_failure_cases_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week07_failure_cases.csv").exists()


def test_results_index_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "data" / "runs" / "week07_results_index.csv").exists()