import json
import pandas as pd
from pathlib import Path
from src.config import PROCESSED_FILE, INVENTORY_FILE, RUN_ID


def channel_stats(df_ch: pd.DataFrame) -> dict:
    ts = df_ch["timestamp"]
    diffs = ts.diff()

    # Monotonicity violations
    violations = int((diffs.dt.total_seconds() < 0).sum())

    # Sampling interval estimate
    deltas = diffs.dt.total_seconds()
    deltas_pos = deltas[deltas.notna() & (deltas > 0)]
    median_dt = float(deltas_pos.median()) if len(deltas_pos) else None

    # Missingness
    missing_n = int(df_ch["value"].isna().sum())
    total_n = int(len(df_ch))
    missing_pct = float(missing_n / total_n * 100.0) if total_n else 0.0

    return {
        "samples": total_n,
        "time_min": str(ts.min()),
        "time_max": str(ts.max()),
        "median_dt_seconds": median_dt,
        "missing_n": missing_n,
        "missing_pct": missing_pct,
        "monotonicity_violations": violations,
    }


def main():
    root = Path(__file__).resolve().parents[1]
    df = pd.read_parquet(root / PROCESSED_FILE)

    # Ensure stable sort
    df = df.sort_values(["channel", "timestamp"], kind="mergesort")

    inventory = {
        "schema_version": "inventory_v0_1",
        "total_rows": int(len(df)),
        "n_channels": int(df["channel"].nunique()),
        "global_time_min": str(df["timestamp"].min()),
        "global_time_max": str(df["timestamp"].max()),
        "channels": {},
    }

    for ch, df_ch in df.groupby("channel", sort=False):
        inventory["channels"][str(ch)] = channel_stats(df_ch)

    # Save JSON
    out_json = root / INVENTORY_FILE
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(inventory, indent=2), encoding="utf-8")

    # Save readable summary
    run_dir = root / "data" / "runs" / RUN_ID
    run_dir.mkdir(parents=True, exist_ok=True)
    summary_file = run_dir / "inventory_summary.txt"

    top = sorted(inventory["channels"].items(),
                 key=lambda kv: kv[1]["samples"],
                 reverse=True)[:10]

    with open(summary_file, "w", encoding="utf-8") as f:
        f.write("WEEK 01 INVENTORY SUMMARY\n")
        f.write("--------------------------\n\n")
        f.write(f"Total rows: {inventory['total_rows']}\n")
        f.write(f"Channels: {inventory['n_channels']}\n")
        f.write(f"Global time: {inventory['global_time_min']} -> {inventory['global_time_max']}\n\n")
        f.write("Top channels:\n")

        for ch, stats in top:
            f.write(
                f"- {ch}: samples={stats['samples']}, "
                f"missing={stats['missing_pct']:.2f}%, "
                f"median_dt={stats['median_dt_seconds']} sec, "
                f"mono_viol={stats['monotonicity_violations']}\n"
            )

    print("Inventory complete.")
    print("JSON written to:", out_json)
    print("Summary written to:", summary_file)


if __name__ == "__main__":
    main()