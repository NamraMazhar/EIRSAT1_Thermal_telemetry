import json
from pathlib import Path

import yaml
import pandas as pd

from src.baseline_threshold import run_baseline
from src.eval_events import alarms_to_events, compute_metrics
from src.baseline_residual import detect_residual_alarms


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

    cfg = load_yaml(root / "configs" / "baseline2.yaml")
    telemetry = pd.read_csv(root / "data" / "runs" / "R001" / "telemetry_inj.csv")
    events_payload = json.loads((root / "data" / "runs" / "R001" / "events.json").read_text(encoding="utf-8"))
    true_events = pd.DataFrame(events_payload["events"])

    telemetry["timestamp"] = pd.to_datetime(telemetry["timestamp"])

    # Load Week01 chronological split boundaries
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

    print("Train rows:", len(train))
    print("Val rows:", len(val))
    print("Test rows:", len(test))

    # -------------------------
    # Baseline-1 on test
    # -------------------------
    b1_test = run_baseline(train, test, threshold=3.0)
    b1_pred_events = alarms_to_events(b1_test)
    p1, r1, f11, mdd1, fab1 = compute_metrics(b1_pred_events, true_events)

    # -------------------------
    # Baseline-2 threshold sweep on validation only
    # -------------------------
    best_threshold = None
    best_f1 = -1
    sweep_records = []

    orbit_period_samples = int(cfg["orbit_period_samples"])
    phase_bins = int(cfg["phase_bins"])

    for thr in cfg["val_threshold_candidates"]:
        all_val = []

        for ch in cfg["channels_used"]:
            tr_ch = train[train["channel"] == ch].copy()
            va_ch = val[val["channel"] == ch].copy()

            if len(tr_ch) == 0 or len(va_ch) == 0:
                continue

            detected, _ = detect_residual_alarms(
                tr_ch, va_ch,
                orbit_period_samples=orbit_period_samples,
                phase_bins=phase_bins,
                threshold=float(thr)
            )
            all_val.append(detected)

        if len(all_val) == 0:
            continue

        val_detected = pd.concat(all_val, ignore_index=True)
        val_pred_events = alarms_to_events(val_detected)
        p, r, f1, mdd, fab = compute_metrics(val_pred_events, true_events)

        sweep_records.append({
            "threshold": thr,
            "Precision": p,
            "Recall": r,
            "EventF1": f1,
            "MDD": mdd,
            "FAB": fab
        })

        if f1 > best_f1:
            best_f1 = f1
            best_threshold = float(thr)

    if best_threshold is None:
        raise ValueError("No valid threshold found on validation split. Check selected channels and val data.")

    threshold_record = {
        "selected_on": "validation_only",
        "frozen_threshold": best_threshold,
        "sweep_records": sweep_records
    }

    (root / "data" / "runs" / "R001" / "threshold_record.json").write_text(
        json.dumps(threshold_record, indent=2), encoding="utf-8"
    )

    # -------------------------
    # Baseline-2 on test using frozen threshold
    # -------------------------
    all_test = []
    template_fit_count = 0

    for ch in cfg["channels_used"]:
        tr_ch = train[train["channel"] == ch].copy()
        te_ch = test[test["channel"] == ch].copy()

        print(f"{ch}: train={len(tr_ch)}, test={len(te_ch)}")

        if len(tr_ch) == 0 or len(te_ch) == 0:
            continue

        detected, _ = detect_residual_alarms(
            tr_ch, te_ch,
            orbit_period_samples=orbit_period_samples,
            phase_bins=phase_bins,
            threshold=best_threshold
        )
        all_test.append(detected)
        template_fit_count += 1

    if len(all_test) == 0:
        raise ValueError("No test objects to concatenate. Check selected channels vs test split coverage.")

    test_detected = pd.concat(all_test, ignore_index=True)
    b2_pred_events = alarms_to_events(test_detected)
    p2, r2, f12, mdd2, fab2 = compute_metrics(b2_pred_events, true_events)

    comparative = pd.DataFrame([
        metrics_row("baseline_1_raw_threshold", p1, r1, f11, mdd1, fab1, 3.0),
        metrics_row("baseline_2_residual_threshold", p2, r2, f12, mdd2, fab2, best_threshold),
    ])

    comparative.to_csv(root / "data" / "runs" / "R001" / "comparative_metrics.csv", index=False)
    test_detected.to_csv(root / "data" / "runs" / "R001" / "baseline2_detected_test.csv", index=False)

    fit_log = {
        "template_fit_count": template_fit_count,
        "channels_used": cfg["channels_used"]
    }

    (root / "data" / "runs" / "R001" / "baseline2_fit_log.json").write_text(
        json.dumps(fit_log, indent=2), encoding="utf-8"
    )

    print("\nComparative metrics:")
    print(comparative)


if __name__ == "__main__":
    main()