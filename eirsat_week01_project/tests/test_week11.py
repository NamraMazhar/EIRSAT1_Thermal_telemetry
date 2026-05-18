from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import yaml


def run_validator_with_temp_configs(inject_payload, eval_payload):
    root = Path(__file__).resolve().parents[1]

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        cfg_dir = tmp / "configs"
        cfg_dir.mkdir(parents=True, exist_ok=True)

        with open(cfg_dir / "injection_v2_R001.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(inject_payload, f, sort_keys=False)

        with open(cfg_dir / "eval_config.yaml", "w", encoding="utf-8") as f:
            yaml.safe_dump(eval_payload, f, sort_keys=False)

        helper = tmp / "run_validator.py"
        helper.write_text(textwrap.dedent("""
            from pathlib import Path
            import sys
            import yaml

            INJECT_REQUIRED = [
                "run_id", "seed", "split_to_inject", "schema_version",
                "fault_types", "magnitude_tiers", "duration_tiers", "allowed_channels"
            ]
            EVAL_REQUIRED = [
                "run_id_default", "seed", "metrics", "event_matching",
                "fab_definition", "split_policy", "methods", "schema_version"
            ]

            def load_yaml(path):
                with open(path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f)

            def validate_required(payload, required, label):
                missing = [k for k in required if k not in payload]
                if missing:
                    raise ValueError(f"{label} missing required fields: {missing}")

            def validate_injector(payload):
                validate_required(payload, INJECT_REQUIRED, "injector_config")
                if not isinstance(payload["fault_types"], dict):
                    raise ValueError("injector_config fault_types must be a mapping")
                if not isinstance(payload["allowed_channels"], list) or len(payload["allowed_channels"]) == 0:
                    raise ValueError("injector_config allowed_channels must be a non-empty list")

            def validate_eval(payload):
                validate_required(payload, EVAL_REQUIRED, "eval_config")
                required_metrics = {"Precision", "Recall", "EventF1", "MDD", "FAB"}
                if not required_metrics.issubset(set(payload["metrics"])):
                    raise ValueError("eval_config metrics missing required entries")
                if payload["event_matching"].get("overlap_rule") is None:
                    raise ValueError("eval_config event_matching.overlap_rule missing")
                if payload["fab_definition"].get("normalization") is None:
                    raise ValueError("eval_config fab_definition.normalization missing")

            try:
                cfg_dir = Path(__file__).resolve().parent / "configs"
                injector_cfg = load_yaml(cfg_dir / "injection_v2_R001.yaml")
                eval_cfg = load_yaml(cfg_dir / "eval_config.yaml")
                validate_injector(injector_cfg)
                validate_eval(eval_cfg)
                sys.exit(0)
            except Exception:
                sys.exit(1)
        """), encoding="utf-8")

        result = subprocess.run([sys.executable, str(helper)], cwd=tmp)
        return result.returncode


GOOD_INJECT = {
    "run_id": "R001",
    "seed": 1337,
    "split_to_inject": "test",
    "schema_version": "schema_v0_2",
    "fault_types": {"bias": True},
    "magnitude_tiers": {"medium": 2.5},
    "duration_tiers": {"medium": 30},
    "allowed_channels": ["TEMP_CPU"],
}

GOOD_EVAL = {
    "run_id_default": "R001",
    "seed": 1337,
    "metrics": ["Precision", "Recall", "EventF1", "MDD", "FAB"],
    "event_matching": {"overlap_rule": "any_overlap", "delay_reference": "predicted_start_minus_event_start"},
    "fab_definition": {"unit": "count", "normalization": "per_run_window"},
    "split_policy": {"train": "chronological", "val": "chronological", "test": "chronological"},
    "methods": ["baseline_1_raw_threshold"],
    "schema_version": "eval_v0_1",
}


def test_missing_inject_run_id_fails():
    bad = dict(GOOD_INJECT)
    bad.pop("run_id")
    assert run_validator_with_temp_configs(bad, GOOD_EVAL) != 0


def test_missing_inject_fault_types_fails():
    bad = dict(GOOD_INJECT)
    bad.pop("fault_types")
    assert run_validator_with_temp_configs(bad, GOOD_EVAL) != 0


def test_empty_allowed_channels_fails():
    bad = dict(GOOD_INJECT)
    bad["allowed_channels"] = []
    assert run_validator_with_temp_configs(bad, GOOD_EVAL) != 0


def test_missing_eval_metrics_fails():
    bad = dict(GOOD_EVAL)
    bad.pop("metrics")
    assert run_validator_with_temp_configs(GOOD_INJECT, bad) != 0


def test_missing_required_metric_fails():
    bad = dict(GOOD_EVAL)
    bad["metrics"] = ["Precision", "Recall"]
    assert run_validator_with_temp_configs(GOOD_INJECT, bad) != 0


def test_missing_event_overlap_rule_fails():
    bad = dict(GOOD_EVAL)
    bad["event_matching"] = {"delay_reference": "predicted_start_minus_event_start"}
    assert run_validator_with_temp_configs(GOOD_INJECT, bad) != 0


def test_missing_fab_normalization_fails():
    bad = dict(GOOD_EVAL)
    bad["fab_definition"] = {"unit": "count"}
    assert run_validator_with_temp_configs(GOOD_INJECT, bad) != 0


def test_week11_artifacts_exist():
    root = Path(__file__).resolve().parents[1]
    assert (root / "docs" / "repro_metadata.json").exists()
    assert (root / "docs" / "repro_audit.csv").exists()
    assert (root / "docs" / "risk_register.csv").exists()
    assert (root / "docs" / "final_definitions.md").exists()
    assert (root / "docs" / "fastpath_summary.txt").exists()