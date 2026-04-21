from pathlib import Path
import pandas as pd
import json
import numpy as np


def main():
    root = Path(__file__).resolve().parents[1]

    base_run = "R001"
    src_dir = root / "data" / "runs" / base_run

    df = pd.read_csv(src_dir / "telemetry_inj.csv")
    events = json.loads((src_dir / "events.json").read_text(encoding="utf-8"))

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # RS01: timing/orbit-phase shift
    rs01 = df.copy()
    rs01["timestamp"] = rs01["timestamp"] + pd.to_timedelta(15, unit="m")

    # RS02: missingness stress
    rs02 = df.copy()
    rng = np.random.default_rng(1337)
    miss_idx = rng.choice(rs02.index, size=int(0.05 * len(rs02)), replace=False)
    rs02.loc[miss_idx, "value"] = np.nan
    rs02["value"] = rs02.groupby("channel")["value"].transform(lambda s: s.interpolate().bfill().ffill())

    # RS03: noise stress
    rs03 = df.copy()
    rng2 = np.random.default_rng(1337)
    rs03["value"] = rs03["value"] + rng2.normal(0, 1.5, len(rs03))

    for run_id, temp_df in [("RS01", rs01), ("RS02", rs02), ("RS03", rs03)]:
        out_dir = root / "data" / "runs" / run_id
        out_dir.mkdir(parents=True, exist_ok=True)

        temp_df.to_csv(out_dir / "telemetry_inj.csv", index=False)
        (out_dir / "events.json").write_text(json.dumps(events, indent=2), encoding="utf-8")

    print("Week09 stress runs generated.")


if __name__ == "__main__":
    main()