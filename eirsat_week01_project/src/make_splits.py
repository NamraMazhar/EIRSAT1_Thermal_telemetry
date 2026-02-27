import json
import pandas as pd
from pathlib import Path
from src.config import PROCESSED_FILE, SPLITS_FILE, RUN_ID, NO_SHUFFLE


def main():
    assert NO_SHUFFLE is True, "NO_SHUFFLE must be True."

    root = Path(__file__).resolve().parents[1]
    df = pd.read_parquet(root / PROCESSED_FILE)

    # Global time range
    t0 = df["timestamp"].min()
    t3 = df["timestamp"].max()

    total_duration = t3 - t0

    # 70% train, 15% val, 15% test
    t1 = t0 + total_duration * 0.70
    t2 = t0 + total_duration * 0.85

    train = df[df["timestamp"] < t1]
    val = df[(df["timestamp"] >= t1) & (df["timestamp"] < t2)]
    test = df[df["timestamp"] >= t2]

    train_end = train["timestamp"].max()
    val_start = val["timestamp"].min()
    val_end = val["timestamp"].max()
    test_start = test["timestamp"].min()

    # STRICT ASSERTIONS (Leakage guard)
    assert train_end < val_start, f"Leakage risk: train_end {train_end} !< val_start {val_start}"
    assert val_end < test_start, f"Leakage risk: val_end {val_end} !< test_start {test_start}"

    splits = {
        "schema_version": "split_v0_1",
        "policy": {
            "type": "chronological_blocks",
            "train_fraction": 0.70,
            "val_fraction": 0.15,
            "test_fraction": 0.15,
            "no_shuffle": True
        },
        "train": {"start": str(t0), "end": str(t1)},
        "val": {"start": str(t1), "end": str(t2)},
        "test": {"start": str(t2), "end": str(t3)}
    }

    out_path = root / SPLITS_FILE
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(splits, indent=2), encoding="utf-8")

    run_dir = root / "data" / "runs" / RUN_ID
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "splits.json").write_text(json.dumps(splits, indent=2), encoding="utf-8")

    print("Splits created successfully.")
    print("Train rows:", len(train))
    print("Val rows:", len(val))
    print("Test rows:", len(test))


if __name__ == "__main__":
    main()