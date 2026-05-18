from pathlib import Path
import pandas as pd


def test_final_config_set_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "FINAL" / "configs" / "final_injection_config.yaml").exists()
    assert (root / "FINAL" / "configs" / "final_eval_config.yaml").exists()
    assert (root / "FINAL" / "configs" / "final_proposed_config.yaml").exists()


def test_final_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "FINAL" / "artifacts" / "final_telemetry_inj.csv").exists()
    assert (root / "FINAL" / "artifacts" / "final_events.json").exists()
    assert (root / "FINAL" / "artifacts" / "final_main_results_table.csv").exists()
    assert (root / "FINAL" / "artifacts" / "final_tradeoff_plot.png").exists()
    assert (root / "FINAL" / "artifacts" / "final_faulttype_plot.png").exists()
    assert (root / "FINAL" / "artifacts" / "final_sensitivity_plot.png").exists()


def test_final_hashes_exist():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "FINAL" / "artifacts" / "final_hashes.csv")
    assert len(df) >= 6


def test_final_release_candidate_log():
    root = Path(__file__).resolve().parents[1]
    txt = (root / "docs" / "final_release_candidate_log.txt").read_text(encoding="utf-8")
    assert "STATUS=SUCCESS" in txt


def test_final_qa_pass():
    root = Path(__file__).resolve().parents[1]
    txt = (root / "docs" / "final_qa_summary.txt").read_text(encoding="utf-8")
    assert "STATUS=PASS" in txt


def test_final_runbook_exists():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "final_runbook.md").exists()
    assert (root / "docs" / "final_replication_checklist.md").exists()