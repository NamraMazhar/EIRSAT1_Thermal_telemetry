from pathlib import Path
import yaml

FAULT_TYPES = ["bias", "drift"]
MAGNITUDES = ["small", "medium", "large"]
DURATIONS = ["short", "medium", "long"]

MAG_VALUES = {
    "small": 1.0,
    "medium": 2.5,
    "large": 5.0,
}

DUR_VALUES = {
    "short": 10,
    "medium": 30,
    "long": 60,
}

DRIFT_SCALE = {
    "small": 0.02,
    "medium": 0.05,
    "large": 0.08,
}


def make_cfg(run_id, fault_type, mag_key, dur_key):
    return {
        "run_id": run_id,
        "seed": 1337,
        "split_to_inject": "test",
        "schema_version": "schema_v0_2",
        "mixed_faults_enabled": False,
        "dropout_handling_policy": "interpolate_linear",
        "fault_types": {
            "bias": fault_type == "bias",
            "drift": fault_type == "drift",
            "lag": False,
            "stuck_at": False,
            "dropout": False,
            "noise_increase": False,
        },
        "magnitude_tiers": {
            mag_key: MAG_VALUES[mag_key]
        },
        "duration_tiers": {
            dur_key: DUR_VALUES[dur_key]
        },
        "drift_slope_scale": {
            mag_key: DRIFT_SCALE[mag_key]
        },
        "min_separation_samples": 20,
        "events_per_channel": 2,
        "allowed_channels": [
            "TEMP_BAT",
            "TEMP_CPU",
            "TEMP_PANEL_X",
            "TEMP_PANEL_Y",
            "TEMP_PAYLOAD",
            "TEMP_STRUCTURE",
        ],
    }


def main():
    root = Path(__file__).resolve().parents[1]
    cfg_dir = root / "configs"
    cfg_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    run_num = 201

    for fault_type in FAULT_TYPES:
        for mag in MAGNITUDES:
            for dur in DURATIONS:
                run_id = f"R{run_num}"
                cfg = make_cfg(run_id, fault_type, mag, dur)

                out_path = cfg_dir / f"ablation_B_{run_id}_{fault_type}_{mag}_{dur}.yaml"
                with open(out_path, "w", encoding="utf-8") as f:
                    yaml.safe_dump(cfg, f, sort_keys=False)

                rows.append({
                    "run_id": run_id,
                    "fault_type": fault_type,
                    "magnitude": mag,
                    "duration": dur,
                    "config_file": str(out_path.relative_to(root)).replace("\\", "/")
                })
                run_num += 1

    import pandas as pd
    pd.DataFrame(rows).to_csv(root / "data" / "runs" / "week08_config_index.csv", index=False)
    print("Week08 configs generated.")


if __name__ == "__main__":
    main()