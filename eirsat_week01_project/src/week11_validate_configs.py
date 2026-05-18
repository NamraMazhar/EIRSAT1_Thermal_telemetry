from pathlib import Path
import sys
import yaml


INJECT_REQUIRED = [
    "run_id",
    "seed",
    "split_to_inject",
    "schema_version",
    "fault_types",
    "magnitude_tiers",
    "duration_tiers",
    "allowed_channels",
]

EVAL_REQUIRED = [
    "run_id_default",
    "seed",
    "metrics",
    "event_matching",
    "fab_definition",
    "split_policy",
    "methods",
    "schema_version",
]


def load_yaml(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_required(payload: dict, required: list[str], label: str):
    missing = [k for k in required if k not in payload]
    if missing:
        raise ValueError(f"{label} missing required fields: {missing}")


def validate_injector(payload: dict):
    validate_required(payload, INJECT_REQUIRED, "injector_config")

    if not isinstance(payload["fault_types"], dict):
        raise ValueError("injector_config fault_types must be a mapping")

    if not isinstance(payload["allowed_channels"], list) or len(payload["allowed_channels"]) == 0:
        raise ValueError("injector_config allowed_channels must be a non-empty list")


def validate_eval(payload: dict):
    validate_required(payload, EVAL_REQUIRED, "eval_config")

    required_metrics = {"Precision", "Recall", "EventF1", "MDD", "FAB"}
    if not required_metrics.issubset(set(payload["metrics"])):
        raise ValueError("eval_config metrics missing required entries")

    if payload["event_matching"].get("overlap_rule") is None:
        raise ValueError("eval_config event_matching.overlap_rule missing")

    if payload["fab_definition"].get("normalization") is None:
        raise ValueError("eval_config fab_definition.normalization missing")


def main():
    root = Path(__file__).resolve().parents[1]

    injector_cfg = load_yaml(root / "configs" / "injection_v2_R001.yaml")
    eval_cfg = load_yaml(root / "configs" / "eval_config.yaml")

    validate_injector(injector_cfg)
    validate_eval(eval_cfg)

    print("Week11 config validation passed.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"VALIDATION ERROR: {e}")
        sys.exit(1)