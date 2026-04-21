import json
from pathlib import Path

import pandas as pd
import yaml

from src.baseline_threshold import run_baseline
from src.baseline_residual import detect_residual_alarms
from src.baseline_ml import (
    build_wide,
    fit_ml_reconstruction,
    reconstruct_scores,
    threshold_scores,
    choose_threshold_on_validation,
)
from src.proposed_method import detect_proposed
from src.eval_events import alarms_to_events, compute_metrics


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def metric_row(run_id, method, precision, recall, f1, mdd, fab, threshold):
    return {
        "run_id": run_id,
        "method": method,
        "Precision": precision,
        "Recall": recall,
        "EventF1": f1,
        "MDD": mdd,
        "FAB": fab,
        "Threshold": threshold,
    }


def main():
    root = Path(__file__).resolve().parents[1]
    splits = json.loads((root / "data" / "processed" / "splits.json").read_text(encoding="utf-8"))
    b2_cfg = load_yaml(root / "configs" / "baseline2.yaml")
    ml_cfg = load_yaml(root / "configs" / "week05_ml.yaml")
    prop_cfg = load_yaml(root / "configs" / "week09_proposed.yaml")

    train_start = pd.to_datetime(splits["train"]["start"])
    train_end = pd.to_datetime(splits["train"]["end"])
    val_start = pd.to_datetime(splits["val"]["start"])
    val_end = pd.to_datetime(splits["val"]["end"])
    test_start = pd.to_datetime(splits["test"]["start"])
    test_end = pd.to_datetime(splits["test"]["end"])

    all_rows = []

    for run_id in ["RS01", "RS02", "RS03"]:
        print(f"\nEvaluating {run_id} ...")

        telemetry = pd.read_csv(root / "data" / "runs" / run_id / "telemetry_inj.csv")
        telemetry["timestamp"] = pd.to_datetime(telemetry["timestamp"])

        events_payload = json.loads((root / "data" / "runs" / run_id / "events.json").read_text(encoding="utf-8"))
        true_events = pd.DataFrame(events_payload["events"])

        train = telemetry[(telemetry["timestamp"] >= train_start) & (telemetry["timestamp"] < train_end)].copy()
        val = telemetry[(telemetry["timestamp"] >= val_start) & (telemetry["timestamp"] < val_end)].copy()
        test = telemetry[(telemetry["timestamp"] >= test_start) & (telemetry["timestamp"] <= test_end)].copy()

        # baseline-1
        b1_test = run_baseline(train, test, threshold=3.0)
        b1_pred = alarms_to_events(b1_test)
        p1, r1, f11, mdd1, fab1 = compute_metrics(b1_pred, true_events)
        all_rows.append(metric_row(run_id, "baseline_1_raw_threshold", p1, r1, f11, mdd1, fab1, 3.0))

        # baseline-2
        best_threshold_b2 = 1.5
        all_test = []
        for ch in b2_cfg["channels_used"]:
            tr_ch = train[train["channel"] == ch].copy()
            te_ch = test[test["channel"] == ch].copy()
            if len(tr_ch) == 0 or len(te_ch) == 0:
                continue
            detected, _ = detect_residual_alarms(
                tr_ch, te_ch,
                orbit_period_samples=int(b2_cfg["orbit_period_samples"]),
                phase_bins=int(b2_cfg["phase_bins"]),
                threshold=float(best_threshold_b2)
            )
            all_test.append(detected)

        test_detected = pd.concat(all_test, ignore_index=True)
        b2_pred = alarms_to_events(test_detected)
        p2, r2, f12, mdd2, fab2 = compute_metrics(b2_pred, true_events)
        all_rows.append(metric_row(run_id, "baseline_2_residual_threshold", p2, r2, f12, mdd2, fab2, best_threshold_b2))

        # baseline-3
        channels = ml_cfg["channels_used"]
        train_wide = build_wide(train, channels)
        val_wide = build_wide(val, channels)
        test_wide = build_wide(test, channels)

        bundle = fit_ml_reconstruction(
            train_wide=train_wide,
            hidden_layers=ml_cfg["hidden_layers"],
            max_iter=int(ml_cfg["max_iter"]),
            solver=ml_cfg["solver"],
            seed=int(ml_cfg["seed"])
        )

        train_score_wide, _ = reconstruct_scores(bundle, train_wide)
        val_score_wide, _ = reconstruct_scores(bundle, val_wide)
        test_score_wide, _ = reconstruct_scores(bundle, test_wide)

        thr_ml, _ = choose_threshold_on_validation(
            train_score_wide,
            val_score_wide,
            ml_cfg["val_threshold_candidates"],
            target_alarm_rate=float(ml_cfg["target_val_alarm_rate"])
        )

        test_scores_long = threshold_scores(train_score_wide, test_score_wide, thr_ml)
        b3_pred = alarms_to_events(test_scores_long)
        p3, r3, f13, mdd3, fab3 = compute_metrics(b3_pred, true_events)
        all_rows.append(metric_row(run_id, "baseline_3_ml_reconstruction", p3, r3, f13, mdd3, fab3, thr_ml))

        # proposed method
        all_prop = []
        for ch in prop_cfg["channels_used"]:
            tr_ch = train[train["channel"] == ch].copy()
            te_ch = test[test["channel"] == ch].copy()
            if len(tr_ch) == 0 or len(te_ch) == 0:
                continue
            detected = detect_proposed(
                tr_ch, te_ch,
                orbit_period_samples=int(prop_cfg["orbit_period_samples"]),
                smoothing_window=int(prop_cfg["smoothing_window"]),
                threshold=2.5
            )
            all_prop.append(detected)

        prop_detected = pd.concat(all_prop, ignore_index=True)
        prop_pred = alarms_to_events(prop_detected)
        pp, pr, pf1, pmdd, pfab = compute_metrics(prop_pred, true_events)
        all_rows.append(metric_row(run_id, "proposed_residual_learning", pp, pr, pf1, pmdd, pfab, 2.5))

    out_df = pd.DataFrame(all_rows)
    out_df.to_csv(root / "data" / "runs" / "week09_stress_results.csv", index=False)

    print("\nWeek09 stress results:")
    print(out_df)


if __name__ == "__main__":
    main()