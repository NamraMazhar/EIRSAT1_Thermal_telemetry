"""
Week 01 - Ingest Script
Creates canonical SSOT dataset from raw telemetry
"""

import pandas as pd
from pathlib import Path
from src.config import RAW_FILE, PROCESSED_FILE, RUN_ID


def main():
    root = Path(__file__).resolve().parents[1]
    raw_path = root / RAW_FILE
    out_path = root / PROCESSED_FILE
    log_path = root / "data" / "runs" / RUN_ID / "ingest_log.txt"

    if not raw_path.exists():
        raise FileNotFoundError(f"Raw file not found: {raw_path}")

    print("Reading raw dataset...")
    df = pd.read_csv(raw_path)

    required = {"timestamp", "channel", "value"}
    if not required.issubset(df.columns):
        raise ValueError(f"Missing required columns {required}. Found {list(df.columns)}")

    print("Parsing timestamps...")
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    invalid_ts = int(df["timestamp"].isna().sum())
    if invalid_ts > 0:
        print(f"Dropping {invalid_ts} invalid timestamp rows")
        df = df.dropna(subset=["timestamp"])

    df["channel"] = df["channel"].astype(str)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # CRITICAL: No shuffle allowed
    df = df.sort_values(["channel", "timestamp"], kind="mergesort").reset_index(drop=True)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("Week 01 Ingest Log\n")
        f.write("------------------\n")
        f.write(f"Rows: {len(df)}\n")
        f.write(f"Channels: {df['channel'].nunique()}\n")
        f.write(f"Time range: {df['timestamp'].min()} -> {df['timestamp'].max()}\n")
        f.write(f"Dropped invalid timestamps: {invalid_ts}\n")

    print("Ingest complete.")
    print("Processed file written to:", out_path)


if __name__ == "__main__":
    main()