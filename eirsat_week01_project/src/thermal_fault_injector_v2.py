import json
import hashlib
from pathlib import Path

import pandas as pd
import yaml
import numpy as np

from src.config import PROCESSED_FILE
from src.fault_ops import (
    apply_bias,
    apply_drift,
    apply_lag,
    apply_stuck_at,
    apply_dropout,
    apply_noise_increase,
)


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deterministic_seed(global_seed: int, event_id: str) -> int:
    s = f"{global_seed}_{event_id}"
    return int(hashlib.sha256(s.encode()).hexdigest(), 16) % (2**32)


def choose_fault_type(cfg, rng):
    enabled = [k for k, v in cfg["fault_types"].items() if v]
    return rng.choice(enabled)


def choose_tier_value(tiers_dict, rng):
    keys = list(tiers_dict.keys())
    key = rng.choice(keys)
    return key, tiers_dict[key]


def apply_fault(df, idxs, fault_type, magnitude, event_seed, cfg, magnitude_tier=None):
    original = df.loc[idxs, "value"].copy()

    if fault_type == "bias":
        modified = apply_bias(original, magnitude)

    elif fault_type == "drift":
        n = len(original)
        slope_scale = cfg["drift_slope_scale"][magnitude_tier]
        drift_mag = slope_scale * n
        modified = apply_drift(original, drift_mag)

    elif fault_type == "lag":
        modified = apply_lag(original, alpha=0.2)

    elif fault_type == "stuck_at":
        modified = apply_stuck_at(original)

    elif fault_type == "dropout":
        modified = apply_dropout(original)

    elif fault_type == "noise_increase":
        modified = apply_noise_increase(original, std=max(0.5, magnitude / 2), seed=event_seed)

    else:
        raise ValueError(f"Unsupported fault type: {fault_type}")

    df.loc[idxs, "value"] = modified


def maybe_handle_dropout(df, cfg):
    policy = cfg.get("dropout_handling_policy", "none")
    if policy == "interpolate_linear":
        df["value"] = df.groupby("channel")["value"].transform(lambda s: s.interpolate().bfill().ffill())
    return df


def main(config_name=None):
    root = Path(__file__).resolve().parents[1]

    if config_name is None:
        raise ValueError("Pass config name, e.g. python -m src.thermal_fault_injector_v2 configs/injection_v2_R001.yaml")

    cfg_path = root / config_name
    cfg = load_yaml(cfg_path)

    run_id = cfg["run_id"]
    global_seed = int(cfg["seed"])
    split_to_inject = cfg["split_to_inject"]

    processed_path = root / PROCESSED_FILE
    splits_path = root / "data" / "processed" / "splits.json"

    df = pd.read_parquet(processed_path)
    splits = json.loads(splits_path.read_text(encoding="utf-8"))

    split_start = pd.to_datetime(splits[split_to_inject]["start"])
    split_end = pd.to_datetime(splits[split_to_inject]["end"])

    df_inj = df.copy()

    target = df_inj[
        (df_inj["timestamp"] >= split_start) &
        (df_inj["timestamp"] < split_end) &
        (df_inj["channel"].isin(cfg["allowed_channels"]))
    ].copy()

    events = []
    events_generated = 0

    min_sep = int(cfg["min_separation_samples"])
    events_per_channel = int(cfg["events_per_channel"])
    mixed_enabled = bool(cfg.get("mixed_faults_enabled", False))

    for channel in cfg["allowed_channels"]:
        ch_df = target[target["channel"] == channel].sort_values("timestamp").copy()
        ch_indices = ch_df.index.to_list()

        if len(ch_indices) < 100:
            continue

        used_ranges = []

        for ev_num in range(events_per_channel):
            event_id = f"{run_id}_{channel}_{ev_num+1:03d}"
            event_seed = deterministic_seed(global_seed, event_id)
            rng = np.random.default_rng(event_seed)

            fault_type = choose_fault_type(cfg, rng)
            magnitude_tier, magnitude = choose_tier_value(cfg["magnitude_tiers"], rng)
            duration_tier, duration = choose_tier_value(cfg["duration_tiers"], rng)

            duration = int(duration)
            if duration >= len(ch_indices):
                duration = max(5, len(ch_indices) // 4)

            placed = False
            for _ in range(100):
                start_pos = int(rng.integers(0, len(ch_indices) - duration))
                end_pos = start_pos + duration - 1

                overlaps = False
                for a, b in used_ranges:
                    if not (end_pos + min_sep < a or start_pos - min_sep > b):
                        overlaps = True
                        break

                if not overlaps:
                    used_ranges.append((start_pos, end_pos))
                    placed = True
                    break

            if not placed:
                continue

            event_indices = ch_indices[start_pos:end_pos + 1]
            start_time = df_inj.loc[event_indices[0], "timestamp"]
            end_time = df_inj.loc[event_indices[-1], "timestamp"]

            apply_fault(df_inj, event_indices, fault_type, float(magnitude), event_seed, cfg, magnitude_tier)

            mixed_fault_type = None
            if mixed_enabled:
                second_fault = choose_fault_type(cfg, rng)
                if second_fault != fault_type:
                    apply_fault(df_inj, event_indices, second_fault, float(magnitude), event_seed + 1, cfg, magnitude_tier)
                    mixed_fault_type = second_fault

            event = {
                "event_id": event_id,
                "channel": channel,
                "start_time": str(start_time),
                "end_time": str(end_time),
                "event_type": fault_type,
                "mixed_fault_type": mixed_fault_type,
                "magnitude_tier": magnitude_tier,
                "magnitude": float(magnitude),
                "duration_tier": duration_tier,
                "duration_samples": int(duration),
                "split": split_to_inject,
                "event_seed": int(event_seed),
                "robustness_only": True if fault_type == "noise_increase" else False,
                "schema_version": cfg["schema_version"]
            }
            events.append(event)
            events_generated += 1

    df_inj = maybe_handle_dropout(df_inj, cfg)

    for ev in events:
        ev_start = pd.to_datetime(ev["start_time"])
        ev_end = pd.to_datetime(ev["end_time"])
        assert ev_start >= split_start
        assert ev_end < split_end

    run_dir = root / "data" / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    out_csv = run_dir / "telemetry_inj.csv"
    out_json = run_dir / "events.json"

    df_inj.to_csv(out_csv, index=False)

    payload = {
        "schema_version": cfg["schema_version"],
        "run_id": run_id,
        "seed": global_seed,
        "split_to_inject": split_to_inject,
        "mixed_faults_enabled": mixed_enabled,
        "dropout_handling_policy": cfg.get("dropout_handling_policy", "none"),
        "events_generated": events_generated,
        "events": events,
    }

    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Injection complete.")
    print("Run ID:", run_id)
    print("Injected CSV:", out_csv)
    print("Events JSON:", out_json)
    print("Events generated:", events_generated)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        raise ValueError("Usage: python -m src.thermal_fault_injector_v2 configs/injection_v2_R001.yaml")
    main(sys.argv[1])