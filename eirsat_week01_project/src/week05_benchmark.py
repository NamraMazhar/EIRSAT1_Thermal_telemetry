import json
from pathlib import Path

import yaml
import pandas as pd

from src.baseline_ml import (
    build_wide,
    fit_ml_reconstruction,
    reconstruct_scores,
    threshold_scores,
    choose_threshold_on_validation,
)
from src.eval_events import alarms_to_events, compute_metrics


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def metrics_row(method_name, precision, recall, f1, mdd, fab, threshold):
    return {
        "Method": method_name,
        "Precision": precision,
        "Recall": recall,
        "EventF1": f1,
        "MDD": mdd,
        "FAB": fab,
        "Threshold": threshold
    }


def main():
    root = Path(__file__).resolve().parents[1]

    cfg = load_yaml(root / "configs" / "week05_ml.yaml")
    run_id = cfg["run_id"]
    seed = int(cfg["seed"])
    channels = cfg["channels_used"]

    telemetry = pd.read_csv(root / "data" / "runs" / run_id / "telemetry_inj.csv")
    telemetry["timestamp"] = pd.to_datetime(telemetry["timestamp"])

    events_payload = json.loads((root / "data" / "runs" / run_id / "events.json").read_text(encoding="utf-8"))
    true_events = pd.DataFrame(events_payload["events"])

    splits = json.loads((root / "data" / "processed" / "splits.json").read_text(encoding="utf-8"))

    train_start = pd.to_datetime(splits["train"]["start"])
    train_end = pd.to_datetime(splits["train"]["end"])
    val_start = pd.to_datetime(splits["val"]["start"])
    val_end = pd.to_datetime(splits["val"]["end"])
    test_start = pd.to_datetime(splits["test"]["start"])
    test_end = pd.to_datetime(splits["test"]["end"])

    train = telemetry[(telemetry["timestamp"] >= train_start) & (telemetry["timestamp"] < train_end)].copy()
    val = telemetry[(telemetry["timestamp"] >= val_start) & (telemetry["timestamp"] < val_end)].copy()
    test = telemetry[(telemetry["timestamp"] >= test_start) & (telemetry["timestamp"] <= test_end)].copy()

    train_wide = build_wide(train, channels)
    val_wide = build_wide(val, channels)
    test_wide = build_wide(test, channels)

    bundle = fit_ml_reconstruction(
        train_wide=train_wide,
        hidden_layers=cfg["hidden_layers"],
        max_iter=int(cfg["max_iter"]),
        solver=cfg["solver"],
        seed=seed
    )

    train_score_wide, infer_train_sec = reconstruct_scores(bundle, train_wide)
    val_score_wide, infer_val_sec = reconstruct_scores(bundle, val_wide)
    test_score_wide, infer_test_sec = reconstruct_scores(bundle, test_wide)

    chosen_thr, sweep_records = choose_threshold_on_validation(
        train_score_wide=train_score_wide,
        val_score_wide=val_score_wide,
        candidates=cfg["val_threshold_candidates"],
        target_alarm_rate=float(cfg["target_val_alarm_rate"])
    )

    train_scores_long = threshold_scores(train_score_wide, train_score_wide, chosen_thr)
    test_scores_long = threshold_scores(train_score_wide, test_score_wide, chosen_thr)

    pred_events = alarms_to_events(test_scores_long)
    p3, r3, f13, mdd3, fab3 = compute_metrics(pred_events, true_events)

    # Save score files (needed for reproducibility hash checks)
    run_dir = root / "data" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    train_scores_long.to_csv(run_dir / "ml_scores_train.csv", index=False, float_format="%.10f")
    test_scores_long.to_csv(run_dir / "ml_scores_test.csv", index=False, float_format="%.10f")

    threshold_record = {
        "selected_on": "validation_only",
        "frozen_threshold": chosen_thr,
        "target_val_alarm_rate": float(cfg["target_val_alarm_rate"]),
        "sweep_records": sweep_records
    }
    (run_dir / "week05_threshold_record.json").write_text(
        json.dumps(threshold_record, indent=2), encoding="utf-8"
    )

    runtime_log = {
        "train_time_sec": float(bundle["train_time_sec"]),
        "infer_time_sec": float(infer_test_sec),
        "seed": seed,
        "solver": cfg["solver"]
    }
    (run_dir / "ml_runtime_log.json").write_text(
        json.dumps(runtime_log, indent=2), encoding="utf-8"
    )

    # Load baseline-1 and baseline-2 from Week04 comparison
    compare_df = pd.read_csv(run_dir / "comparative_metrics.csv")

    ml_row = pd.DataFrame([metrics_row(
        "baseline_3_ml_reconstruction",
        p3, r3, f13, mdd3, fab3, chosen_thr
    )])

    benchmark_df = pd.concat([compare_df, ml_row], ignore_index=True)
    benchmark_df.to_csv(run_dir / "benchmark_3baseline.csv", index=False)

    print("\nWeek05 benchmark table:")
    print(benchmark_df)

    print("\nFrozen threshold:", chosen_thr)
    print("Train time (sec):", bundle["train_time_sec"])
    print("Infer time (sec):", infer_test_sec)


if __name__ == "__main__":
    main()